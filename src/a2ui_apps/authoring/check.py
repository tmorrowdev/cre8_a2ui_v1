"""Validate one candidate composite and its example, in a fresh process.

    python -m a2ui_apps.authoring.check <module.py> <example.json>

Prints a JSON list of error strings ([] when the candidate is good) and exits
0 either way; a crash exits non-zero. The authoring agent runs this in a
subprocess so model-written code is imported only after `policy_errors` has
passed, and never into the agent's own process (whose catalog caches it would
also make stale).

Checks, in order:
1. the module follows the composite rules (`policy_errors`);
2. it imports and defines exactly one macro whose name is new to the catalog;
3. the expander accepts it next to every existing composite;
4. the example is valid against the inference catalog (cre8 + composites +
   candidate), uses the candidate, and still validates as pure cre8 after
   every composite is expanded.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def check(module_path: Path, example_path: Path) -> list[str]:
    from a2ui_apps.authoring.policy import policy_errors

    source = module_path.read_text()
    errors = policy_errors(source)
    if errors:
        return errors

    from a2ui.core.exceptions import A2uiError
    from a2ui.parser.messages import to_message_models
    from a2ui.utils.renderer_state import validate_payload

    from a2ui_apps.composites import macro_name, macros_in
    from a2ui_apps.examples import components_of
    from a2ui_apps.macros import MACROS, build_expander
    from a2ui_apps.sdk import to_dicts
    from a2ui_apps.validate import load_catalog, validate_messages

    spec = importlib.util.spec_from_file_location(f"a2ui_apps.composites.{module_path.stem}", module_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:  # noqa: BLE001 - any import failure is feedback for the model
        return [f"importing the module failed: {type(e).__name__}: {e}"]
    found = macros_in(module)
    if len(found) != 1:
        return [f"expected one @macro in the module, found {len(found)}"]
    candidate = found[0]
    name = macro_name(candidate)
    taken = set(load_catalog().document["components"]) | {macro_name(m) for m in MACROS}
    if name in taken:
        return [f"{name!r} already exists in the catalog; pick a new name or extend the existing component"]

    try:
        expander = build_expander([*MACROS, candidate])
        inference = expander.transform_to_inference_catalog(load_catalog().api)
    except Exception as e:  # noqa: BLE001
        return [f"the macro expander rejected {name}: {type(e).__name__}: {e}"]

    try:
        example: list[dict[str, Any]] = json.loads(example_path.read_text())
    except json.JSONDecodeError as e:
        return [f"example is not valid JSON: {e}"]
    if not isinstance(example, list) or len(example) != 1 or "createSurface" not in example[0]:
        return ["the example must be a JSON array holding exactly one createSurface message"]
    if name not in components_of(example):
        return [f"the example must use {name} at least once"]
    try:
        validate_payload([inference], example)
    except A2uiError as e:
        return [f"example rejected by the inference catalog: {e}"]
    try:
        lowered = to_dicts(expander.transform_to_transport(to_message_models(example)))
    except Exception as e:  # noqa: BLE001
        return [f"expanding the example failed: {type(e).__name__}: {e}"]
    leftover = components_of(lowered) & (taken | {name}) - set(load_catalog().document["components"])
    if leftover:
        return [f"composites left after expansion: {sorted(leftover)}"]
    return [f"expanded example is not valid cre8: {e.get('error', e).get('message')}" for e in validate_messages(lowered)]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    print(json.dumps(check(Path(argv[1]), Path(argv[2]))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
