"""Official A2UI v1.0 schemas, vendored from a2ui-project/a2ui at the commit
a2ui-core is pinned to (pyproject [tool.uv.sources]), and a validator for the
agent-to-renderer envelope with `catalog.json` mapped to the cre8 catalog, as
the spec instructs.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import regex
from jsonschema import Draft202012Validator, validators
from referencing import Registry, Resource

from a2ui_apps.validate import load_catalog

FIXTURES = Path(__file__).parent / "fixtures" / "a2ui_v1"
V1_BASE = "https://a2ui.org/specification/v1_0/"


def _pattern_properties(validator, patterns, instance, schema):
    """patternProperties with the `regex` module: the v1.0 schemas use \\p{XID_Start}
    (UAX #31) for extension keys, which Python's `re` cannot compile."""
    if not validator.is_type(instance, "object"):
        return
    for pattern, subschema in patterns.items():
        compiled = regex.compile(pattern)
        for key, value in instance.items():
            if compiled.search(key):
                yield from validator.descend(value, subschema, path=key, schema_path=pattern)


# additionalProperties consults patternProperties through the same `re`, so it is redone too.
def _additional_properties(validator, additional, instance, schema):
    if not validator.is_type(instance, "object"):
        return
    known = set(schema.get("properties", {}))
    patterns = [regex.compile(p) for p in schema.get("patternProperties", {})]
    extras = [k for k in instance if k not in known and not any(p.search(k) for p in patterns)]
    if validator.is_type(additional, "object"):
        for key in extras:
            yield from validator.descend(instance[key], additional, path=key)
    elif not additional and extras:
        from jsonschema.exceptions import ValidationError

        yield ValidationError(f"Additional properties are not allowed ({', '.join(map(repr, extras))} unexpected)")


A2uiValidator = validators.extend(
    Draft202012Validator,
    {"patternProperties": _pattern_properties, "additionalProperties": _additional_properties},
)


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


@pytest.fixture(scope="session")
def catalog_doc() -> dict:
    return load_catalog().document


@pytest.fixture(scope="session")
def registry(catalog_doc) -> Registry:
    common = _fixture("common_types.json")
    mapped_catalog = {**catalog_doc, "$id": f"{V1_BASE}catalog.json"}
    return Registry().with_resources(
        [
            (common["$id"], Resource.from_contents(common)),
            (mapped_catalog["$id"], Resource.from_contents(mapped_catalog)),
        ]
    )


@pytest.fixture(scope="session")
def envelope_validator(registry) -> Draft202012Validator:
    return A2uiValidator(_fixture("agent_to_renderer.json"), registry=registry)


@pytest.fixture(scope="session")
def catalog_definition_validator(registry) -> Draft202012Validator:
    return A2uiValidator(_fixture("catalog_definition.json"), registry=registry)


def errors_of(validator, instance) -> list[str]:
    return [f"{'/'.join(map(str, e.absolute_path))}: {e.message[:200]}" for e in validator.iter_errors(instance)][:5]
