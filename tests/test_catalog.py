from __future__ import annotations


import pytest

from a2ui_apps.catalog.build import build_mapping, is_uax31
from a2ui_apps.validate import load_catalog, validate_messages
from conftest import errors_of


def surface(components, data=None):
    body = {"surfaceId": "s", "catalogId": load_catalog().catalog_id, "components": components}
    if data is not None:
        body["dataModel"] = data
    return {"version": "1.0", "createSurface": body}


VALID_TREE = [
    {"id": "root", "component": "Cre8LayoutSection", "children": ["title", "email", "send"]},
    {"id": "title", "component": "Cre8Heading", "type": "headline-large", "children": ["title_text"]},
    {"id": "title_text", "component": "Text", "text": "Contact"},
    {"id": "email", "component": "Cre8Field", "label": "Email", "value": {"@path": "/email"}},
    {
        "id": "send",
        "component": "Cre8Button",
        "text": "Send",
        "variant": "primary",
        "on_click": {"event": {"name": "submit", "context": {"email": {"@path": "/email"}}}},
    },
]


def test_catalog_conforms_to_official_catalog_definition(catalog_definition_validator, catalog_doc):
    assert errors_of(catalog_definition_validator, catalog_doc) == []


def test_catalog_definition_validator_is_not_vacuous(catalog_definition_validator, catalog_doc):
    broken = {k: v for k, v in catalog_doc.items() if k != "catalogId"} | {"bogusTopLevel": 1}
    assert errors_of(catalog_definition_validator, broken)


def test_catalog_covers_cre8_wc_3_0_1(catalog_doc):
    assert catalog_doc["catalogId"].endswith("/cre8-wc/3.0.1")
    assert catalog_doc["protocolVersion"] == "1.0"
    names = set(catalog_doc["components"])
    cre8 = {n for n in names if n.startswith("Cre8")}
    html = {n for n in names if n.startswith("Html")}
    assert len(cre8) == 88 and len(names) == 96
    assert html == {"HtmlDiv", "HtmlSection", "HtmlArticle", "HtmlAside", "HtmlHeader", "HtmlFooter", "HtmlNav"}
    assert all(is_uax31(n) for n in names)


def test_catalog_maps_colliding_and_hyphenated_names(catalog_doc):
    card = catalog_doc["components"]["Cre8Card"]["allOf"][-1]["properties"]
    assert card["slot_header"]["x-cre8-slot"] == "header"
    keys = [k for c in catalog_doc["components"].values() for part in c.get("allOf", [c]) for k in part.get("properties", {})]
    assert all(is_uax31(k) for k in keys)
    renamed = {v["x-cre8-prop"] for c in catalog_doc["components"].values() for part in c.get("allOf", [c])
               for v in part.get("properties", {}).values() if "x-cre8-prop" in v}
    assert "aria-label" in renamed
    tabs = catalog_doc["components"]["Cre8Tabs"]["allOf"][-1]["properties"]
    assert tabs["on_tab_change"]["x-cre8-event"] == "tab-change"


def test_mapping_rejects_collisions():
    source = {
        "x-native-events": ["click"],
        "$defs": {
            "components": {
                "cre8-x": {"properties": {"props": {"properties": {"on_click": {"type": "string"}}}}},
            }
        },
    }
    with pytest.raises(ValueError, match="both map to 'on_click'"):
        build_mapping(source)


def test_valid_tree_passes_official_envelope_and_a2ui_core(envelope_validator):
    message = surface(VALID_TREE, {"email": ""})
    assert errors_of(envelope_validator, message) == []
    assert validate_messages([message]) == []


@pytest.mark.parametrize(
    "name, components, code",
    [
        ("unknown property", [{"id": "root", "component": "Cre8Button", "bogus": 1}], "VALIDATION_FAILED"),
        ("enum violation", [{"id": "root", "component": "Cre8Button", "variant": "bogus"}], "VALIDATION_FAILED"),
        ("basic catalog type", [{"id": "root", "component": "Row"}], "VALIDATION_FAILED"),
        ("string in ChildList", [{"id": "root", "component": "Cre8LayoutSection", "children": [{"text": "x"}]}], "VALIDATION_FAILED"),
        ("dangling child", [{"id": "root", "component": "Cre8LayoutSection", "children": ["ghost"]}], "INTEGRITY_ERROR"),
        ("orphan", [{"id": "root", "component": "Cre8Button"}, {"id": "o", "component": "Text", "text": "x"}], "INTEGRITY_ERROR"),
        (
            "non-UAX#31 id",
            [{"id": "root", "component": "Cre8LayoutSection", "children": ["a-b"]}, {"id": "a-b", "component": "Text", "text": "x"}],
            "VALIDATION_FAILED",
        ),
    ],
)
def test_invalid_trees_are_rejected(name, components, code):
    errors = validate_messages([surface(components)])
    assert errors, f"{name} was accepted"
    assert errors[0]["error"]["code"] == code


@pytest.mark.parametrize(
    "components",
    [
        [{"id": "root", "component": "Cre8Button", "bogus": 1}],
        [{"id": "root", "component": "Cre8Button", "variant": "bogus"}],
        [{"id": "root", "component": "Row"}],
    ],
)
def test_official_envelope_validator_is_not_vacuous(envelope_validator, components):
    assert errors_of(envelope_validator, surface(components))


# ─── Structural HTML and token styling ───────────────────────────────────────

HTML_TREE = [
    {"id": "root", "component": "HtmlDiv", "display": "flex", "direction": "column", "gap": "16",
     "padding": "24", "background": "subtle", "radius": "large", "children": ["head", "body", "foot"]},
    {"id": "head", "component": "HtmlHeader", "paddingY": "8", "border": "default", "background": "brand", "children": ["title"]},
    {"id": "title", "component": "Cre8Heading", "type": "headline-large", "children": ["title_text"]},
    {"id": "title_text", "component": "Text", "text": "Title"},
    {"id": "body", "component": "HtmlSection", "display": "grid", "columns": 2, "gap": "24", "children": ["left", "right"]},
    {"id": "left", "component": "Cre8TextPassage", "padding": "8", "children": ["left_text"]},
    {"id": "left_text", "component": "Text", "text": "Left"},
    {"id": "right", "component": "Cre8Button", "text": "Go", "paddingX": "8", "marginY": "16"},
    {"id": "foot", "component": "HtmlFooter", "textAlign": "center", "maxWidth": "prose", "children": ["note"]},
    {"id": "note", "component": "Cre8TextPassage", "children": ["note_text"]},
    {"id": "note_text", "component": "Text", "text": "Footer"},
]


def test_structural_tree_passes_official_envelope_and_a2ui_core(envelope_validator):
    message = surface(HTML_TREE)
    assert errors_of(envelope_validator, message) == []
    assert validate_messages([message]) == []


@pytest.mark.parametrize(
    "name, components",
    [
        ("off-scale padding", [{"id": "root", "component": "HtmlDiv", "padding": "17"}]),
        ("free CSS colour", [{"id": "root", "component": "HtmlDiv", "background": "red"}]),
        ("non-flipping status tint", [{"id": "root", "component": "HtmlDiv", "background": "info"}]),
        ("columns out of range", [{"id": "root", "component": "HtmlDiv", "columns": 9}]),
        ("typography on a container", [{"id": "root", "component": "HtmlDiv", "fontWeight": "bold"}]),
        ("text colour on a container", [{"id": "root", "component": "HtmlDiv", "color": "brand"}]),
        ("layout prop on a cre8 component", [{"id": "root", "component": "Cre8Button", "gap": "8"}]),
        ("off-scale padding on cre8", [{"id": "root", "component": "Cre8Button", "padding": "huge"}]),
        ("content element (paragraph)", [{"id": "root", "component": "HtmlP"}]),
        ("content element (link)", [{"id": "root", "component": "HtmlA"}]),
        ("content element (image)", [{"id": "root", "component": "HtmlImg"}]),
    ],
)
def test_structural_and_style_constraints(name, components):
    errors = validate_messages([surface(components)])
    assert errors, f"{name} was accepted"
    assert errors[0]["error"]["code"] == "VALIDATION_FAILED"


def test_style_props_are_annotated_for_the_renderer(catalog_doc):
    defs = catalog_doc["$defs"]
    assert all("x-style" in p for p in defs["SpacingProps"]["properties"].values())
    assert all("x-style" in p for p in defs["BoxStyle"]["properties"].values())
    assert not {"color", "fontWeight"} & set(defs["BoxStyle"]["properties"])
    for name, schema in catalog_doc["components"].items():
        if name.startswith("Html"):
            assert schema["x-html-tag"] in {"div", "section", "article", "aside", "header", "footer", "nav"}
        if name.startswith(("Html", "Cre8")):
            assert {"$ref": "#/$defs/SpacingProps"} in schema["allOf"], name
