# a2ui-apps

Generate A2UI v1.0 apps from prompts and render them with cre8 web components.
Built on [a2ui-agent-sdk](https://github.com/a2ui-project/a2ui) (catalogs,
inference formats, parsing, validation, macros) and Claude.

```
uv sync
uv run uvicorn a2ui_apps.server:app --reload     # A2UI_APPS_FAKE_LLM=1 for canned plans, no API key
cd web && pnpm install && pnpm dev               # the cre8 renderer
uv run pytest                                    # no API key needed; the model is scripted
```

## The hybrid setup

A runtime A2UI agent can only be as good as the catalog it composes from. A
free-form coding agent can write any layout it likes, which is why it often
looks better, but it is slow, unvalidated and off-brand. This repo splits the
work so each agent does what it is good at:

```
            BUILD TIME (a person reviews and merges)                     RUNTIME (every request)
 ┌──────────────────────────────────────────────────┐      ┌──────────────────────────────────────────────────┐
 │ scripts/author_composite.py "an FAQ list"        │      │ prompt ─► router ─► form / dashboard (assembled) │
 │   coding agent writes                            │      │                  └► freeform: the model composes  │
 │     composites/faq_list.py   (@macro)            │ PR   │      catalog = cre8 + composites (inference)      │
 │     examples/help_center.json (gold example)     │ ───► │      few-shot = closest gold example              │
 │   gates: policy ─► catalog check ─► test suite   │      │      validate ─► repair (≤3 tries) ─► expand      │
 │   repair loop on any failure, then hand-off      │      │      renderer gets pure cre8; it owns styling     │
 └──────────────────────────────────────────────────┘      └──────────────────────────────────────────────────┘
```

**Runtime: compose only.** The freeform pathway (`pathways/freeform.py`) never
writes layout code. It writes A2UI (Express by default) against the inference
catalog, which is the cre8 catalog plus every composite. Per request it:

1. prunes the catalog to the components the app needs (composites always stay);
2. adds the gold example closest to that selection as a few-shot
   (`examples/`, validated with the SDK's `load_examples`);
3. streams and validates every message against a `RendererState` transaction
   plus an unknown-property check. That is the stateful form of the SDK's
   `validate_payload`, so a half-built stream rolls back whole;
4. on any error, deletes what the browser was sent, returns the error to the
   model and retries, up to `MAX_ATTEMPTS = 3`;
5. expands every composite to cre8 primitives (`macros.expand`) before
   anything leaves the agent, so the renderer only needs the cre8 catalog.

Styling never travels in the payload. Composites and the model only set
token-valued props (`gap="16"`, `type="headline-large"`, `variant="primary"`);
the renderer (`web/src/token-styles.ts`, `theme.ts`) and the theme step own
colors, fonts and radius. So every valid payload is on-brand.

**Build time: grow the catalog.** When a request needs a pattern the catalog
lacks, add a composite instead of hoping the runtime model improvises one:

```
uv run python scripts/author_composite.py "a testimonial card with quote, author and avatar"
uv run python scripts/author_composite.py --no-tests --attempts 2 "an FAQ list"
```

The authoring agent (`a2ui_apps/authoring/`) picks the cre8 components to build
from, shows the model their builder signatures, the existing composites (so it
does not duplicate one) and two house-style references, and asks for one
`@macro` module plus one gold example. Before anything is written into the
package, the candidate must clear three gates:

1. **Policy** (`authoring/policy.py`), static, before the code is imported:
   allowed imports only, exactly one PascalCase `@macro`, typed parameters with
   an `Args:` line each (the runtime model reads them), no raw colors or CSS,
   no `eval`/`open`/dunder tricks.
2. **Catalog check** (`python -m a2ui_apps.authoring.check`), in a separate
   process: the name is new, the expander accepts the macro next to every
   existing composite, the example validates against the inference catalog,
   uses the new composite, and is valid cre8 once expanded.
3. **Test suite**, with the files in place. `tests/test_composites.py` covers
   every composite and example automatically, so a new module is tested with
   no test edits.

A failure at any gate goes back to the model with the errors, up to
`--attempts` (default 3). If it still fails, nothing is left behind. On
success you get two new, uncommitted files; review the diff and open a pull
request. The agent never commits, pushes or opens a PR. It needs
`ANTHROPIC_API_KEY`; the tests use `ScriptedLLM`.

**Where the halves meet: `a2ui_apps/composites/`.** One module per composite;
`discover()` collects them, so a merged module is in the prompt, the parser
and the expander with no registration. The same rules hold whether a person
or the authoring agent wrote it.

| Composite | Lowers to | Use for |
| --- | --- | --- |
| `MetricCard` | Cre8Card, Cre8Heading, Cre8Badge | one headline number with a trend badge |
| `KpiRow` | Cre8Grid, Cre8GridItem | a row of metrics sized to their count |
| `ChartCard` | Cre8Card, Cre8Chart | a titled line, bar, pie or doughnut chart; colors from the theme |
| `HeroBanner` | Cre8Hero, Cre8Heading, Cre8Button | a landing-page opener with up to two calls to action |
| `PricingTier` | Cre8Card, Cre8List, Cre8Button | one plan in a pricing table |
| `FormSection` | Cre8Card, Cre8Button | a titled form with one submit button |
| `FormField` | Cre8Field | an input bound to the data model |
| `Section` | HtmlSection, Cre8Heading | a titled group of content |

## Optional: a fine-tuned composer

The freeform pathway's first compose can run on a small distilled model, served
from Modal or Ollama, with the planner (Claude, or Kimi via an OpenAI-compatible
URL) behind it:

```
A2UI_APPS_PLANNER_URL / _MODEL / _KEY     optional: any OpenAI-compatible planner instead of Claude
A2UI_APPS_COMPOSER_URL / _MODEL / _KEY    optional: the fine-tuned composer
```

`a2ui_apps.composer.RoutedLLM` sends first-attempt composes to the composer with
a slim prompt: the grammar and positional signatures, with no per-argument docs
and no examples. Repairs go to the planner with the full prompt and the
validator's errors. Edits, structured calls and other formats also stay on the
planner. If the composer can't be reached before anything has streamed, the
planner takes over. Validation does not change. `scripts/distill.py` builds the
training set from the real pathway, `training/` fine-tunes on Kaggle and serves
on Modal, and `scripts/eval_composer.py` scores it. See
[training/README.md](training/README.md).

## Layout

```
src/a2ui_apps/
  engine.py, router.py         route a prompt; run a pathway; edits and actions
  llm.py, composer.py          model boundary (Claude, OpenAI-compatible); composer routing and fallback
  pathways/                    form and dashboard (model fills slots, Python assembles), freeform (model composes)
  sdk.py                       a2ui-agent-sdk wiring: catalogs, formats, processors, renderer state
  validate.py                  a2ui_core STRICT validation + unknown-property check
  composites/                  the composite catalog layer (one @macro per module)
  macros.py                    expander, inference catalog and expansion over the composites
  examples/                    gold few-shot examples (JSON v1.0 messages; may use composites)
  authoring/                   build-time catalog-authoring agent, policy and catalog check
  builders/cre8.py             typed builders, generated by scripts/generate_builders.py
  catalog/                     the cre8 v1.0 catalog
scripts/
  author_composite.py          build-time: add a composite + example
  build_examples.py            regenerate the assembled examples
  export_skills.py             export SKILL.md files for third-party agents (composites expanded)
  distill.py, eval_composer.py build and score the fine-tuned composer
training/                      Kaggle fine-tune notebook, Modal server
  generate_builders.py         regenerate builders/cre8.py from the catalog
web/                           the cre8 renderer (web_core + cre8-wc)
```
