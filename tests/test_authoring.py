"""The build-time catalog-authoring agent: rules, checks, repair, and nothing left behind on failure."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from a2ui_apps.authoring import REPO_ROOT, author_composite, check_in_subprocess, system_prompt
from a2ui_apps.authoring.policy import policy_errors
from a2ui_apps.llm import ScriptedLLM

CATALOG_ID = "https://cre8.dev/a2ui/v1_0/catalogs/cre8-wc/3.0.1"

SOURCE = '''"""TestimonialCard: a customer quote."""

from __future__ import annotations

from a2ui.transformers.macros import macro

from a2ui_apps.builders.cre8 import Cre8Card, Cre8Heading, Cre8TextPassage, HtmlDiv, Text


@macro
def TestimonialCard(quote: str, author: str, role: str = "") -> Cre8Card:
    """A customer quote in a card with the person's name and role.

    Args:
        quote: The quote, without quotation marks.
        author: Who said it.
        role: Their title and company, e.g. "CMO, Northwind".
    """
    people = [Cre8Heading(type="label-default", children=[Text(text=author)])]
    if role:
        people.append(Cre8TextPassage(size="small", children=[Text(text=role)]))
    return Cre8Card(slot_default=[HtmlDiv(display="flex", direction="column", gap="12", padding="24", children=[
        Cre8TextPassage(size="large", children=[Text(text=quote)]),
        HtmlDiv(display="flex", direction="column", gap="4", children=people),
    ])])
'''


def example(*extra_props: dict) -> list[dict]:
    second = {"id": "t2", "component": "TestimonialCard", "quote": "Clients read the reports.", "author": "Sam Lee"}
    for props in extra_props:
        second.update(props)
    return [{"version": "1.0", "createSurface": {"surfaceId": "example_customer_stories", "catalogId": CATALOG_ID, "components": [
        {"id": "root", "component": "Cre8LayoutSection", "children": ["body"]},
        {"id": "body", "component": "Section", "title": "What clients say", "children": ["grid"]},
        {"id": "grid", "component": "HtmlDiv", "display": "grid", "columns": 2, "gap": "16", "children": ["t1", "t2"]},
        {"id": "t1", "component": "TestimonialCard", "quote": "We cut reporting time in half.", "author": "Dana Ruiz", "role": "COO, Brightline"},
        second,
    ]}}]


def candidate(source: str = SOURCE, messages: list[dict] | None = None, **overrides) -> dict:
    return {
        "name": "TestimonialCard",
        "module": "testimonial_card",
        "source": source,
        "example_name": "customer_stories",
        "example": messages if messages is not None else example(),
        "summary": "A customer quote with the person's name and role.",
        **overrides,
    }


@pytest.fixture
def repo(tmp_path) -> Path:
    """A scratch copy of the parts of the package the agent reads and writes."""
    for part in ("composites", "examples", "builders"):
        shutil.copytree(REPO_ROOT / "src/a2ui_apps" / part, tmp_path / "src/a2ui_apps" / part)
    return tmp_path


def scripted(*writes: dict) -> ScriptedLLM:
    return ScriptedLLM({"author.select": [{"components": ["Cre8Card", "Cre8TextPassage", "NotAComponent"]}], "author.write": list(writes)})


def new_files(repo: Path) -> set[str]:
    return {p.name for p in (repo / "src/a2ui_apps/composites").glob("testimonial*")} | {
        p.name for p in (repo / "src/a2ui_apps/examples").glob("customer*")
    }


# --- policy ------------------------------------------------------------------------------


def test_policy_accepts_a_good_composite():
    assert policy_errors(SOURCE, "TestimonialCard") == []


@pytest.mark.parametrize(
    ("change", "expected"),
    [
        (lambda s: s.replace("from __future__ import annotations", "import os"), "plain `import`"),
        (lambda s: s.replace("from a2ui.transformers.macros import macro", "from a2ui.transformers.macros import macro\nfrom subprocess import run"), "'subprocess' is not allowed"),
        (lambda s: s.replace('gap="12", padding="24"', 'gap="12", padding="24", background=eval("1")'), "eval() is not allowed"),
        (lambda s: s.replace('size="large"', 'size="large", inverted="#ff0066"'), "raw color or CSS"),
        (lambda s: s.replace("        role: Their title", "        rolez: Their title"), "'role' has no `Args:` description"),
        (lambda s: s + "\n\n@macro\ndef Other(x: str) -> Cre8Card:\n    \"\"\"x.\n\n    Args:\n        x: x.\n    \"\"\"\n    return Cre8Card()\n", "exactly one @macro"),
        (lambda s: s.replace("author: str, role", "author, role"), "'author' needs a type annotation"),
    ],
)
def test_policy_rejects(change, expected):
    errors = policy_errors(change(SOURCE), "TestimonialCard")
    assert any(expected in e for e in errors), errors


def test_policy_checks_the_requested_name():
    assert any("request named it 'QuoteCard'" in e for e in policy_errors(SOURCE, "QuoteCard"))


# --- catalog check (real subprocess) ------------------------------------------------------


def write(tmp_path: Path, source: str, messages: list[dict]) -> tuple[Path, Path]:
    module, ex = tmp_path / "testimonial_card.py", tmp_path / "customer_stories.json"
    module.write_text(source)
    ex.write_text(json.dumps(messages))
    return module, ex


def test_check_passes_a_valid_candidate(tmp_path):
    assert check_in_subprocess(*write(tmp_path, SOURCE, example())) == []


@pytest.mark.parametrize(
    ("source", "messages", "expected"),
    [
        (SOURCE, example({"mood": "happy"}), "unexpected keyword argument 'mood'"),
        (SOURCE.replace('type="label-default"', 'type="shouty"'), example(), "shouty"),
        (SOURCE.replace("def TestimonialCard", "def MetricCard").replace("TestimonialCard:", "MetricCard:"), example(), "already exists"),
        (SOURCE, [{"version": "1.0", "createSurface": {"surfaceId": "s", "catalogId": CATALOG_ID, "components": [{"id": "root", "component": "Text", "text": "x"}]}}], "must use TestimonialCard"),
    ],
)
def test_check_rejects(tmp_path, source, messages, expected):
    errors = check_in_subprocess(*write(tmp_path, source, messages))
    assert any(expected in e for e in errors), errors


# --- the agent loop -----------------------------------------------------------------------


def test_authors_a_composite_and_installs_it(repo):
    llm = scripted(candidate())
    result = author_composite("a testimonial card", llm, root=repo, test_runner=lambda root: [])
    assert result.ok and result.name == "TestimonialCard" and len(result.attempts) == 1
    assert new_files(repo) == {"testimonial_card.py", "customer_stories.json"}
    assert json.loads((repo / "src/a2ui_apps/examples/customer_stories.json").read_text()) == example()
    assert [c["task"] for c in llm.calls] == ["author.select", "author.write"]


def test_prompt_carries_rules_builders_and_existing_composites(repo):
    system = "\n".join(system_prompt(repo, ["Cre8Card", "Cre8TextPassage"]))
    assert "class Cre8Card(" in system and "class Cre8TextPassage(" in system and "class Cre8Chart(" not in system
    assert "- ChartCard:" in system and "- KpiRow:" in system, "existing composites are listed so they are not duplicated"
    assert "def MetricCard(" in system, "a reference composite shows the house style"
    assert "never colors or CSS" in system
    assert " on_keydown:" not in system, "event-handler noise is trimmed from builder signatures"


def test_rejected_attempt_is_fed_back_and_repaired(repo):
    llm = scripted(candidate(messages=example({"mood": "happy"})), candidate())
    result = author_composite("a testimonial card", llm, root=repo, test_runner=lambda root: [])
    assert result.ok and len(result.attempts) == 2
    second_prompt = [c for c in llm.calls if c["task"] == "author.write"][1]["prompt"]
    assert "Attempt 1 was rejected" in second_prompt and "mood" in second_prompt


def test_policy_failures_never_reach_the_import(repo):
    calls = []
    llm = scripted(candidate(source=SOURCE.replace("from __future__ import annotations", "import os")), candidate())
    result = author_composite(
        "a testimonial card", llm, root=repo, test_runner=None,
        checker=lambda m, e: calls.append(m.read_text()) or [],
    )
    assert result.ok and len(calls) == 1 and "import os" not in calls[0]


def test_failing_tests_roll_back_and_retry(repo):
    outcomes = iter([["test suite failed:\nFAILED tests/test_composites.py::x"], []])
    seen = []

    def runner(root):
        seen.append(new_files(root))
        return next(outcomes)

    result = author_composite("a testimonial card", scripted(candidate(), candidate()), root=repo, test_runner=runner)
    assert result.ok and len(result.attempts) == 2
    assert seen[0] == {"testimonial_card.py", "customer_stories.json"}, "tests run with the files in place"
    assert "test suite failed" in result.attempts[0].errors[0]


def test_gives_up_after_max_attempts_and_leaves_nothing(repo):
    bad = candidate(messages=example({"mood": "happy"}))
    result = author_composite("a testimonial card", scripted(bad, bad), root=repo, max_attempts=2, test_runner=lambda root: [])
    assert not result.ok and len(result.attempts) == 2 and result.errors
    assert new_files(repo) == set()


def test_refuses_to_overwrite_an_existing_module(repo):
    result = author_composite(
        "another metric card", scripted(candidate(module="metric_card")), root=repo, max_attempts=1, test_runner=lambda root: []
    )
    assert not result.ok and "metric_card.py already exists" in result.errors[0]
    assert "def MetricCard(" in (repo / "src/a2ui_apps/composites/metric_card.py").read_text()
