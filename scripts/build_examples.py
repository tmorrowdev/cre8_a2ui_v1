"""Regenerate the deterministic few-shot examples from the pathway assemblers.

Run after changing the catalog or an assembler:  uv run python scripts/build_examples.py
`pricing.json` is hand-curated model output and is not regenerated here.
"""

from __future__ import annotations

import json

from a2ui_apps.demo_llm import DemoLLM
from a2ui_apps.examples import EXAMPLES_DIR
from a2ui_apps.pathways.dashboard import DashboardPathway
from a2ui_apps.pathways.form import FormPathway


def main() -> None:
    llm = DemoLLM()
    for name, pathway, prompt in [
        ("contact_form", FormPathway(), "A contact form"),
        ("sales_dashboard", DashboardPathway(), "A sales dashboard for an online store"),
    ]:
        messages = pathway.assemble(pathway.plan(prompt, llm), f"example_{name}")
        for m in messages:
            m.get("createSurface", {}).pop("sendDataModel", None)
        path = EXAMPLES_DIR / f"{name}.json"
        path.write_text(json.dumps(messages, indent=1) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
