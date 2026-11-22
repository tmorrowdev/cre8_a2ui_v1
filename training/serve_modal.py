"""Serve the fine-tuned composer on Modal with vLLM: OpenAI-compatible, scales to zero.

One-time setup:
    uv run --with modal modal setup
    uv run --with modal modal secret create huggingface-secret HF_TOKEN=hf_...      # reads your private repo
    uv run --with modal modal secret create a2ui-composer-key VLLM_API_KEY=$(openssl rand -hex 24)

Deploy, then check it end to end through the real freeform pathway:
    A2UI_COMPOSER_HF=you/a2ui-apps-composer-4b uv run --with modal modal deploy training/serve_modal.py
    A2UI_COMPOSER_HF=you/a2ui-apps-composer-4b VLLM_API_KEY=... uv run --with modal modal run training/serve_modal.py

Then point the app at it:
    A2UI_APPS_COMPOSER_URL=https://<workspace>--a2ui-apps-composer-server.modal.run/v1
    A2UI_APPS_COMPOSER_KEY=<the VLLM_API_KEY>

Billing runs only while a container is up; it stops SCALEDOWN minutes after the last request.
`modal app stop a2ui-apps-composer` turns it off completely.
"""

import os
import time

import modal

MODEL_NAME = os.environ.get("A2UI_COMPOSER_HF", "YOUR_HF_USERNAME/a2ui-apps-composer-4b")
MODEL_REVISION = os.environ.get("A2UI_COMPOSER_REVISION", "main")  # pin a commit sha once it evaluates well
SERVED_NAME = "a2ui-composer"     # what A2UI_APPS_COMPOSER_MODEL defaults to

GPU = "L4"            # 24 GB: a 4B model in bf16 with room for a 16k context. "A10G"/"L40S" for an 8B.
FAST_BOOT = True      # --enforce-eager: quicker cold starts, slightly slower decoding; right for scale-to-zero
SCALEDOWN = 5         # idle minutes before the container (and billing) stops
MAX_MODEL_LEN = 16384 # slim prompt (2-5k tokens) + 4096 output, with headroom
MINUTES = 60
VLLM_PORT = 8000

vllm_image = (
    modal.Image.from_registry("nvidia/cuda:12.9.0-devel-ubuntu22.04", add_python="3.12")
    .entrypoint([])
    .uv_pip_install("vllm==0.21.0", "transformers==5.8.1")
    .env({"HF_XET_HIGH_PERFORMANCE": "1"})
)

hf_cache_vol = modal.Volume.from_name("huggingface-cache", create_if_missing=True)
vllm_cache_vol = modal.Volume.from_name("vllm-cache", create_if_missing=True)

app = modal.App("a2ui-apps-composer")


@app.server(
    image=vllm_image,
    gpu=GPU,
    scaledown_window=SCALEDOWN * MINUTES,
    startup_timeout=10 * MINUTES,
    volumes={"/root/.cache/huggingface": hf_cache_vol, "/root/.cache/vllm": vllm_cache_vol},
    secrets=[modal.Secret.from_name("huggingface-secret"), modal.Secret.from_name("a2ui-composer-key")],
    port=VLLM_PORT,
    target_concurrency=16,
    # Modal-level auth is off so standard OpenAI clients work; vLLM checks the bearer key.
    unauthenticated=True,
)
class Server:
    @modal.enter()
    def start(self):
        import subprocess

        key = os.environ["VLLM_API_KEY"]
        cmd = [
            "vllm", "serve", MODEL_NAME,
            "--revision", MODEL_REVISION,
            "--served-model-name", SERVED_NAME,
            "--host", "0.0.0.0",
            "--port", str(VLLM_PORT),
            "--api-key", key,
            "--max-model-len", str(MAX_MODEL_LEN),
            "--enable-prefix-caching",   # the slim prompt's grammar prefix is shared by every request
            "--uvicorn-log-level=info",
            "--enforce-eager" if FAST_BOOT else "--no-enforce-eager",
        ]
        print(*["***" if c == key else c for c in cmd])
        self.process = subprocess.Popen(cmd)

    @modal.exit()
    def stop(self):
        self.process.terminate()


@app.local_entrypoint()
def check(prompt: str = "A sign-in screen for a telehealth clinic with email, password and a forgot-password link"):
    """Runs locally: wait for the server, then build one surface through the real freeform pathway."""
    import httpx

    from a2ui_apps.composer import ReplaySelection, RoutedLLM
    from a2ui_apps.llm import OpenAICompatLLM
    from a2ui_apps.pathways.base import PathwayFailed
    from a2ui_apps.pathways.freeform import FreeformPathway
    from a2ui_apps.sdk import AppState

    key = os.environ.get("VLLM_API_KEY") or exit("export VLLM_API_KEY (the a2ui-composer-key secret's value)")
    url = Server.get_url()
    deadline = time.time() + 12 * MINUTES
    while time.time() < deadline:
        try:
            if httpx.get(f"{url}/health", headers={"Authorization": f"Bearer {key}"}, timeout=60).status_code == 200:
                break
        except httpx.HTTPError:
            pass
        time.sleep(3)
    else:
        exit(f"{url} never became healthy")
    print(f"healthy: {url}")

    composer = OpenAICompatLLM(base_url=f"{url}/v1", model=SERVED_NAME, api_key=key, max_tokens=4096)
    selection = ["Cre8Card", "Cre8Field", "Cre8Button", "Cre8Checkbox", "Cre8Link", "Cre8Heading", "Cre8TextPassage"]
    llm = RoutedLLM(planner=ReplaySelection(selection), composer=composer, escalate_repairs=False)
    t0 = time.time()
    runner = FreeformPathway().run(prompt, llm, surface_id="app", state=AppState())
    try:
        while True:
            event = next(runner)
            if "step" in event:
                print("step:", event["step"]["name"], event["step"]["detail"][:120])
    except StopIteration as done:
        print(f"valid surface in {time.time() - t0:.1f}s after {done.value.attempts} attempt(s), "
              f"{len(done.value.messages)} messages")
    except PathwayFailed as e:
        print(f"still invalid after 3 attempts: {e.errors[:2]}")
