"""Skill export (SkillGenerator) for third-party agents."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_script():
    path = Path(__file__).resolve().parents[1] / "scripts" / "export_skills.py"
    spec = importlib.util.spec_from_file_location("export_skills", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_skills_export_as_packages_without_agent_only_features(tmp_path):
    script = load_script()
    written = script.build_skillset().export_to_directory(str(tmp_path))
    assert set(written) == {"a2ui-express/SKILL.md", "cre8-wc-a2ui/SKILL.md"}
    catalog = (tmp_path / "cre8-wc-a2ui" / "SKILL.md").read_text()
    core = (tmp_path / "a2ui-express" / "SKILL.md").read_text()
    assert catalog.startswith("---\nname: cre8-wc-a2ui\n") and core.startswith("---\nname: a2ui-express\n")
    assert catalog.count("\n• ") >= 96, "every cre8 component signature"
    assert catalog.count("<a2ui>") >= 3, "the examples, decompiled into Express"
    for agent_only in ("PricingTier", "MetricCard", "getViewport", "daysUntil"):
        assert agent_only not in catalog + core, f"{agent_only} needs this server; a stock renderer lacks it"
