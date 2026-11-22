# Training the freeform composer

A small open model (Qwen3-4B) distilled from the freeform pathway's compose step. It
writes A2UI Express against the pruned cre8 catalog, the same way the big model does,
from a prompt about a quarter the size. At runtime `RoutedLLM` sends it first-attempt
composes only; repairs, edits and everything structured stay on the planner. The
validator is unchanged, so a weak composer costs latency, never correctness.

```
 distill.py (teacher)        Kaggle (free T4)         Modal ($30/mo credit) or Ollama
 real pathway, accepted ──►  QLoRA, 8k context  ──►   vLLM, OpenAI API, scale to zero
 replies, slim prompt        push to HF (private)       │
                                                        ▼
                         A2UI_APPS_COMPOSER_URL ─► RoutedLLM ─► freeform pathway
```

| Step | Where | Cost |
|---|---|---|
| Distill | your teacher: Claude, or Kimi on Ollama Cloud | teacher tokens |
| Fine-tune | Kaggle Notebooks, about 30 GPU-hours a week | $0 |
| Serve | Modal Starter credit, L4, off after 5 idle minutes | $0 within credit |
| Or serve locally | Ollama on your own machine (Q4_K_M GGUF) | $0 |

## 1. Distill

```bash
uv run python scripts/distill.py --n 40                   # smoke test; read training/data/examples.jsonl
uv run python scripts/distill.py --n 1200 --workers 4     # resumable
```

The teacher writes varied requests (25 domains × 25 surfaces × 5 voices). Each request then runs through
the **real** `FreeformPathway`: component selection, the full prompt, streaming validation and repair.
Only accepted replies are kept, paired with `slim_system(...)`, which is what the composer is served. About
30% of prompts carry a viewer line, as the renderer RPC adds at runtime. Failures go to `rejects.jsonl`.

Teacher: Claude by default. For Kimi instead, set `A2UI_APPS_PLANNER_URL=https://ollama.com/v1`,
`A2UI_APPS_PLANNER_MODEL=kimi-k2.6` and `A2UI_APPS_PLANNER_KEY`. The student can only be as good as the
teacher's first tries, which the script reports.

**The slim prompt is the contract.** Change `slim_system`, the SDK's Express prompt, the catalog or the
composites, and re-distill and retrain. A composer trained on the old prompt will miss the new parts. The
pathway will still catch and repair the mistakes, but more slowly.

## 2. Fine-tune on Kaggle

```bash
pip install kaggle && kaggle auth login
KAGGLE_USER=yourname training/kaggle/push.sh
```

The script uploads `train.jsonl` and `val.jsonl` as a private dataset and pushes the notebook. **First run
only:** on kaggle.com, set Accelerator to GPU T4 x2 and turn Internet on, add an `HF_TOKEN` (write)
secret, set `HF_REPO`, then **Save & Run All**. The notebook trains QLoRA (r=32, 2 epochs, loss on the
reply only) and pushes three private repos: `-lora`, the merged 16-bit model, and `-GGUF`.

## 3. Serve

```bash
uv run --with modal modal setup
uv run --with modal modal secret create huggingface-secret HF_TOKEN=hf_...
uv run --with modal modal secret create a2ui-composer-key VLLM_API_KEY=$(openssl rand -hex 24)
A2UI_COMPOSER_HF=you/a2ui-apps-composer-4b uv run --with modal modal deploy training/serve_modal.py
A2UI_COMPOSER_HF=you/a2ui-apps-composer-4b VLLM_API_KEY=... uv run --with modal modal run training/serve_modal.py
```

`modal run` waits for the server, then builds one surface through the real pathway and reports how many
attempts it took. The first request after an idle period includes a cold start of about 1–2 minutes.
The router falls back to the planner if the composer can't be reached before anything has streamed.

**Or run it on your own machine:**

```bash
ollama run hf.co/you/a2ui-apps-composer-4b-GGUF:Q4_K_M
```

Then use `A2UI_APPS_COMPOSER_URL=http://localhost:11434/v1` and set `A2UI_APPS_COMPOSER_MODEL` to that
model name. Because the repo is private, add your Ollama SSH key to Hugging Face first.

## 4. Measure, then switch it on

```bash
uv run python scripts/eval_composer.py --url $A2UI_APPS_COMPOSER_URL --key $A2UI_APPS_COMPOSER_KEY
uv run python scripts/eval_composer.py --teacher claude      # baseline
```

The eval replays each held-out request's recorded component selection, so only composing is measured.
It reports first-try validity, validity within three attempts, and latency.

Turn the composer on when its first-try rate is close to the teacher's. If it isn't, look at the most
common errors, distill more examples of those surfaces, and retrain. Then set:

```bash
A2UI_APPS_COMPOSER_URL=https://<workspace>--a2ui-apps-composer-server.modal.run/v1
A2UI_APPS_COMPOSER_KEY=...
uv run uvicorn a2ui_apps.server:app
```
