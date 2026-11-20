"""Build-time catalog authoring: a coding agent that grows the composite catalog.

This is the build-time half of the hybrid setup. The runtime agent (the
freeform pathway) may only compose from the catalog; when a request needs a
UI pattern the catalog lacks, a developer runs this agent instead:

    uv run python scripts/author_composite.py "a testimonial card with quote, author and avatar"

It asks the model for one new composite module plus a gold few-shot example,
then holds both to the same bar as hand-written composites before writing
anything into the package:

1. `policy_errors`: static rules on the source (allowed imports, one @macro,
   documented typed parameters, no raw colors or CSS). Runs before the code is
   ever imported.
2. `a2ui_apps.authoring.check` in a subprocess: the expander accepts the
   macro, the example validates against the inference catalog, and the
   expanded example is valid cre8.
3. The test suite, with the files in place (`tests/test_composites.py` covers
   every composite and example automatically).

Any failure goes back to the model with the errors, up to `max_attempts`; if
it still fails, nothing is left behind. Success leaves new, uncommitted files
for a person to review and merge: the agent never commits, pushes or opens a
pull request.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from a2ui_apps.authoring.policy import SNAKE, policy_errors
from a2ui_apps.llm import LLM

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path("src/a2ui_apps")
MAX_ATTEMPTS = 3
CHECK_TIMEOUT_S = 180
TEST_TIMEOUT_S = 900
# Reference composites shown to the model as the house style.
STYLE_REFERENCES = ("metric_card.py", "form_section.py")


class AuthoredComposite(BaseModel):
    name: str = Field(description="PascalCase component name the runtime model will write, e.g. 'TestimonialCard'")
    module: str = Field(description="snake_case module file name without .py, e.g. 'testimonial_card'")
    source: str = Field(description="The complete Python module source")
    example_name: str = Field(description="snake_case name for the gold example, e.g. 'customer_stories'")
    example: list[dict[str, Any]] = Field(
        description="A2UI v1.0 messages: exactly one createSurface whose components use the new composite"
    )
    summary: str = Field(description="One sentence: what the composite renders and when to use it")


class ComponentSelection(BaseModel):
    components: list[str] = Field(description="cre8 catalog components the new composite should be built from")


@dataclass
class Attempt:
    candidate: AuthoredComposite
    errors: list[str]


@dataclass
class AuthoringResult:
    ok: bool
    name: str | None = None
    files: list[Path] = field(default_factory=list)
    attempts: list[Attempt] = field(default_factory=list)

    @property
    def errors(self) -> list[str]:
        return self.attempts[-1].errors if self.attempts else []


Checker = Callable[[Path, Path], list[str]]
TestRunner = Callable[[Path], list[str]]


def composites_dir(root: Path) -> Path:
    return root / PACKAGE / "composites"


def examples_dir(root: Path) -> Path:
    return root / PACKAGE / "examples"


def check_in_subprocess(module_path: Path, example_path: Path) -> list[str]:
    """Run `a2ui_apps.authoring.check` in a fresh interpreter; its errors, or the crash."""
    proc = subprocess.run(
        [sys.executable, "-m", "a2ui_apps.authoring.check", str(module_path), str(example_path)],
        capture_output=True,
        text=True,
        timeout=CHECK_TIMEOUT_S,
    )
    if proc.returncode != 0:
        return [f"checker crashed: {proc.stderr.strip()[-800:]}"]
    try:
        return list(json.loads(proc.stdout.strip().splitlines()[-1]))
    except (json.JSONDecodeError, IndexError):
        return [f"checker printed no result: {proc.stdout[-400:]} {proc.stderr[-400:]}"]


def run_test_suite(root: Path) -> list[str]:
    """The repo's tests with the new files in place; [] when they pass."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-x", "--no-header", "-p", "no:cacheprovider"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=TEST_TIMEOUT_S,
    )
    if proc.returncode == 0:
        return []
    return [f"test suite failed:\n{proc.stdout[-2500:]}"]


def _class_source(builders: str, name: str) -> str:
    """One builder class from builders/cre8.py, without the event-handler noise."""
    match = re.search(rf"^class {re.escape(name)}\(.*?(?=^class |\Z)", builders, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    keep = [line for line in match.group(0).rstrip().splitlines() if not re.match(r"\s+on_(?!click|change)\w+:", line)]
    return "\n".join(keep)


def system_prompt(root: Path, components: list[str]) -> list[str]:
    from a2ui_apps.composites import discover, macro_name
    from a2ui_apps.sdk import component_menu

    builders = (root / PACKAGE / "builders" / "cre8.py").read_text()
    signatures = "\n\n".join(s for s in (_class_source(builders, c) for c in ["Text", *components]) if s)
    existing = "\n".join(
        f"- {macro_name(m)}: {(m.__a2ui_macro__.description or '').splitlines()[0]}" for m in discover()
    )
    references = "\n\n".join(
        f"# composites/{f}\n{(composites_dir(root) / f).read_text()}" for f in STYLE_REFERENCES if (composites_dir(root) / f).exists()
    )
    from a2ui_apps.composites import __doc__ as rules

    return [
        "You extend a design-system catalog for a UI-generating agent. You write ONE new composite component: "
        "a Python `@macro` function that builds a reusable pattern from cre8 builder classes, plus one gold-standard "
        "example screen that uses it. The runtime agent will only ever compose catalog components, so the composite "
        "must look right for any valid arguments.\n\n" + (rules or ""),
        "Existing composites (do not duplicate; you may suggest using one inside your example):\n" + existing,
        "Style references, follow them closely:\n\n" + references,
        "cre8 builder classes you may use (all from a2ui_apps.builders.cre8). Props typed with Literal are design "
        "tokens; use only those values:\n\n" + signatures,
        "The full cre8 catalog, for the example screen:\n" + component_menu(),
        "The example is A2UI v1.0 JSON: a list with one message, "
        '{"version": "1.0", "createSurface": {"surfaceId": "example_<example_name>", '
        '"catalogId": "https://cre8.dev/a2ui/v1_0/catalogs/cre8-wc/3.0.1", "components": [...], "dataModel": {...}}}. '
        'Components are a flat list with unique snake_case ids; one has id "root". Children are id lists. A composite '
        'appears as {"id": "...", "component": "<Name>", <its parameters by name>}; ChildList parameters are id lists, '
        'Action parameters are {"event": {"name": "...", "context": {...}}}, data bindings are {"@path": "/..."}. '
        "Make the example realistic and small (10-30 components), the kind of screen a user would ask for.",
    ]


def _prompt(request: str, previous: list[Attempt]) -> str:
    text = f"Write a composite for this pattern: {request}"
    for i, attempt in enumerate(previous, 1):
        c = attempt.candidate
        text += (
            f"\n\nAttempt {i} was rejected.\n# composites/{c.module}.py\n{c.source}\n# example {c.example_name}\n"
            f"{json.dumps(c.example)[:6000]}\nProblems:\n" + "\n".join(f"- {e}" for e in attempt.errors)
        )
    if previous:
        text += "\n\nFix every problem and return the complete module and example again."
    return text


def select_components(request: str, llm: LLM) -> list[str]:
    from a2ui_apps.sdk import component_menu
    from a2ui_apps.validate import load_catalog

    known = set(load_catalog().document["components"])
    choice = llm.structured(
        task="author.select",
        system=["Pick the cre8 components a reusable UI pattern should be built from.\n" + component_menu()],
        prompt=request,
        schema=ComponentSelection,
        effort="low",
    )
    return sorted({c for c in choice.components if c in known} | {"HtmlDiv", "Cre8Heading", "Cre8TextPassage", "Cre8Card"})


def _shape_errors(candidate: AuthoredComposite, root: Path) -> list[str]:
    errors = []
    if not SNAKE.match(candidate.module) or candidate.module.startswith("_"):
        errors.append(f"module name {candidate.module!r} must be snake_case")
    if not SNAKE.match(candidate.example_name):
        errors.append(f"example name {candidate.example_name!r} must be snake_case")
    if (composites_dir(root) / f"{candidate.module}.py").exists():
        errors.append(f"composites/{candidate.module}.py already exists; choose another module name")
    if (examples_dir(root) / f"{candidate.example_name}.json").exists():
        errors.append(f"examples/{candidate.example_name}.json already exists; choose another example name")
    return errors + policy_errors(candidate.source, candidate.name)


def author_composite(
    request: str,
    llm: LLM,
    *,
    root: Path = REPO_ROOT,
    max_attempts: int = MAX_ATTEMPTS,
    checker: Checker = check_in_subprocess,
    test_runner: TestRunner | None = run_test_suite,
    log: Callable[[str], None] = lambda _msg: None,
) -> AuthoringResult:
    """Write, validate and install one composite; see the module docstring."""
    components = select_components(request, llm)
    log(f"building from: {', '.join(components)}")
    system = system_prompt(root, components)
    result = AuthoringResult(ok=False)
    for n in range(1, max_attempts + 1):
        candidate = llm.structured(
            task="author.write", system=system, prompt=_prompt(request, result.attempts), schema=AuthoredComposite, effort="high"
        )
        log(f"attempt {n}: {candidate.name} ({candidate.module}.py, example {candidate.example_name})")
        errors = _shape_errors(candidate, root)
        if not errors:
            with tempfile.TemporaryDirectory(prefix="a2ui-author-") as tmp:
                module_path = Path(tmp) / f"{candidate.module}.py"
                example_path = Path(tmp) / f"{candidate.example_name}.json"
                module_path.write_text(candidate.source)
                example_path.write_text(json.dumps(candidate.example, indent=1) + "\n")
                errors = checker(module_path, example_path)
        files: list[Path] = []
        if not errors:
            files = _install(candidate, root)
            if test_runner is not None:
                log("checks passed; running the test suite")
                errors = test_runner(root)
        result.attempts.append(Attempt(candidate, errors))
        if errors:
            for f in files:  # leave nothing behind from a rejected attempt
                f.unlink(missing_ok=True)
            log(f"attempt {n} rejected: {errors[0][:200]}")
            continue
        result.ok, result.name, result.files = True, candidate.name, files
        return result
    return result


def _install(candidate: AuthoredComposite, root: Path) -> list[Path]:
    module_path = composites_dir(root) / f"{candidate.module}.py"
    example_path = examples_dir(root) / f"{candidate.example_name}.json"
    source = candidate.source if candidate.source.endswith("\n") else candidate.source + "\n"
    module_path.write_text(source)
    example_path.write_text(json.dumps(candidate.example, indent=1) + "\n")
    return [module_path, example_path]
