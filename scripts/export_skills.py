"""Export Claude skills (SKILL.md) that teach any agent to write cre8 UIs in A2UI Express.

Uses a2ui-agent-sdk's SkillGenerator. The skills describe what a third-party
agent can use with a stock cre8 renderer, so they are built from the plain cre8
catalog: no macros (those need this server's expander) and no functions (the
renderer functions and agent functions need this server's RPC).

    uv run python scripts/export_skills.py [output_dir]     (default: skills/)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from a2ui.catalog_transformers.pruning import FunctionPruningTransformer
from a2ui.core.catalog import Catalog
from a2ui.inference_formats.express.format import ExpressFormatFactory
from a2ui.parser.messages import to_message_models
from a2ui.processor.catalog_config import CatalogConfig
from a2ui.processor.generator import A2uiGenerator
from a2ui.skill.generator import SkillGenerator
from a2ui.skill.skill import SkillSet

from a2ui_apps.catalog.build import CATALOG_PATH
from a2ui_apps.examples import all_examples

CORE_NAME = "a2ui-express"
CATALOG_NAME = "cre8-wc-a2ui"


def build_skillset() -> SkillSet:
    document = json.loads(CATALOG_PATH.read_text())
    base = Catalog.from_json(document, protocol_version="1.0")
    config = CatalogConfig(base, [FunctionPruningTransformer([])])
    examples = [to_message_models(messages) for messages in all_examples().values()]
    processor = A2uiGenerator([config], examples=examples).create_processor(
        {"1.0": {"supportedCatalogIds": [document["catalogId"]]}},
        ExpressFormatFactory(allowed_messages=["createSurface", "updateComponents", "updateDataModel", "deleteSurface"]),
    )
    generator = SkillGenerator(processor.format)
    core = generator.generate_core_skill(
        name=CORE_NAME,
        description="Write A2UI v1.0 user interfaces in the Express DSL: grammar, data binding, events, surfaces. "
        "Use with a catalog skill such as cre8-wc-a2ui.",
    )
    catalog = generator.generate_catalog_skill(
        catalog=processor.active_catalogs[0],
        name=CATALOG_NAME,
        description=f"The cre8-wc web component catalog ({document['catalogId']}) for A2UI v1.0: every component's "
        "signature, plus worked examples. Use when generating cre8 UIs with A2UI Express.",
        include_examples=True,
    )
    # SkillSet keys are output paths, not names: each skill is a <name>/SKILL.md package.
    return SkillSet({f"{skill.name}/SKILL.md": skill for skill in (core, catalog)})


def main(argv: list[str]) -> int:
    out = Path(argv[1] if len(argv) > 1 else "skills")
    written = build_skillset().export_to_directory(str(out))  # {relative path: content}
    for path, content in written.items():
        print(f"{out / path} ({len(content) // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
