"""Build-time catalog authoring: add a composite the runtime agent can compose with.

    uv run python scripts/author_composite.py "a testimonial card with quote, author and avatar"
    uv run python scripts/author_composite.py --no-tests "an FAQ list"   # skip the test-suite gate

Needs ANTHROPIC_API_KEY. Writes a new module to src/a2ui_apps/composites/ and a
gold example to src/a2ui_apps/examples/, only after both pass the composite
rules, the catalog check and the test suite. Nothing is committed: review the
diff, then open a pull request. See a2ui_apps.authoring for the details.
"""

from __future__ import annotations

import argparse
import sys

from a2ui_apps.authoring import MAX_ATTEMPTS, author_composite, run_test_suite
from a2ui_apps.llm import AnthropicLLM


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("request", help="The UI pattern the catalog lacks, in plain words")
    parser.add_argument("--attempts", type=int, default=MAX_ATTEMPTS, help="Model attempts before giving up")
    parser.add_argument("--no-tests", action="store_true", help="Skip running the test suite (the catalog check still runs)")
    args = parser.parse_args(argv)

    result = author_composite(
        args.request,
        AnthropicLLM(),
        max_attempts=args.attempts,
        test_runner=None if args.no_tests else run_test_suite,
        log=lambda msg: print(msg, file=sys.stderr),
    )
    if not result.ok:
        print(f"No composite added after {len(result.attempts)} attempt(s). Last problems:", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Added {result.name}:")
    for path in result.files:
        print(f"  {path}")
    print("Review the diff, run `uv run pytest`, then open a pull request. Nothing was committed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
