"""The rules every composite module is held to, checked statically (no import).

Used two ways: the authoring agent runs it on the code a model wrote before
that code is ever imported, and `tests/test_composites.py` runs it on every
module in `a2ui_apps.composites`, so hand-written composites follow the same
rules as authored ones.
"""

from __future__ import annotations

import ast
import re

# What a composite may import: builders, the macro decorator, typing helpers.
ALLOWED_IMPORTS = {
    "__future__",
    "typing",
    "collections.abc",
    "pydantic",
    "a2ui.builder.v1_0",
    "a2ui.transformers.macros",
    "a2ui_apps.builders.cre8",
}
BANNED_CALLS = {"eval", "exec", "compile", "open", "__import__", "globals", "locals", "vars", "input", "breakpoint", "getattr", "setattr", "delattr"}
# Styling belongs to the renderer and the theme tokens; a composite never carries raw colors or CSS.
RAW_STYLE = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(|\bvar\(--|\bstyle\s*=|;\s*[a-z-]+\s*:", re.IGNORECASE)
PASCAL = re.compile(r"^[A-Z][A-Za-z0-9]*$")
SNAKE = re.compile(r"^[a-z][a-z0-9_]*$")


def _is_macro_decorator(node: ast.expr) -> bool:
    target = node.func if isinstance(node, ast.Call) else node
    return isinstance(target, ast.Name) and target.id == "macro"


def policy_errors(source: str, expected_name: str | None = None) -> list[str]:
    """Problems with a composite module's source; [] when it follows the rules."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return [f"syntax error: {e.msg} (line {e.lineno})"]

    errors: list[str] = []
    macros: list[ast.FunctionDef] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            errors.append(f"line {node.lineno}: use `from ... import ...`; plain `import` is not allowed")
        elif isinstance(node, ast.ImportFrom):
            if node.module not in ALLOWED_IMPORTS:
                errors.append(f"line {node.lineno}: import from {node.module!r} is not allowed; allowed: {sorted(ALLOWED_IMPORTS)}")
        elif isinstance(node, ast.FunctionDef):
            if any(_is_macro_decorator(d) for d in node.decorator_list):
                macros.append(node)
        elif isinstance(node, ast.ClassDef):
            bases = {b.id for b in node.bases if isinstance(b, ast.Name)}
            if bases != {"BaseModel"}:
                errors.append(f"line {node.lineno}: class {node.name} must subclass BaseModel only (argument models for the macro)")
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            pass  # module constants, e.g. a lookup table
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            pass  # docstring
        else:
            errors.append(f"line {node.lineno}: only imports, constants, BaseModel classes and one @macro function belong in a composite module")

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in BANNED_CALLS:
            errors.append(f"line {node.lineno}: call to {node.func.id}() is not allowed")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__") and node.attr.endswith("__"):
            errors.append(f"line {node.lineno}: dunder attribute access ({node.attr}) is not allowed")
        elif isinstance(node, (ast.Global, ast.Nonlocal, ast.Lambda, ast.AsyncFunctionDef, ast.With, ast.Try)):
            errors.append(f"line {node.lineno}: {type(node).__name__} is not allowed in a composite")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and RAW_STYLE.search(node.value):
            errors.append(f"line {node.lineno}: raw color or CSS in {node.value[:40]!r}; use token props and let the renderer theme it")

    if len(macros) != 1:
        errors.append(f"a composite module defines exactly one @macro function; found {len(macros)}")
        return errors
    fn = macros[0]
    if not PASCAL.match(fn.name):
        errors.append(f"macro name {fn.name!r} must be PascalCase")
    if expected_name and fn.name != expected_name:
        errors.append(f"macro is named {fn.name!r} but the request named it {expected_name!r}")
    doc = ast.get_docstring(fn) or ""
    if not doc:
        errors.append(f"{fn.name} needs a docstring: one summary line, then `Args:` with a line per parameter")
    params = [a.arg for a in [*fn.args.posonlyargs, *fn.args.args, *fn.args.kwonlyargs]]
    for p in params:
        if not re.search(rf"^\s+{re.escape(p)}\s*:", doc, re.MULTILINE):
            errors.append(f"{fn.name}: parameter {p!r} has no `Args:` description (the model reads it)")
        annotation = next(a.annotation for a in [*fn.args.posonlyargs, *fn.args.args, *fn.args.kwonlyargs] if a.arg == p)
        if annotation is None:
            errors.append(f"{fn.name}: parameter {p!r} needs a type annotation")
    if fn.args.vararg or fn.args.kwarg:
        errors.append(f"{fn.name}: *args/**kwargs are not allowed; name every parameter")
    if fn.returns is None:
        errors.append(f"{fn.name}: annotate the return type with the root builder class")
    return errors
