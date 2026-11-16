/**
 * Catalog style props (`x-style`) -> CSS declarations over cre8 tokens.
 *
 * The catalog constrains every value to an enum, and this table only knows
 * those values, so nothing an agent sends can become arbitrary CSS: an
 * unexpected value produces no declaration at all.
 */

type Decls = Record<string, string>;

const SPACE = new Set(['0', '4', '8', '12', '16', '24', '32', '48', '64', '96']);
const RADIUS = new Set(['none', 'small', 'field', 'large', 'container', 'pill']);
// Mode-safe choices only (see catalog/html.py). `bg-brand` is white in light
// mode, so the brand option uses the brand tint that flips with mode.
const BACKGROUND: Record<string, string> = {
  default: 'var(--cre8-color-bg-default)',
  subtle: 'var(--cre8-color-bg-subtle)',
  brand: 'var(--cre8-color-bg-brand-hover)',
};
const BORDER = new Set(['default', 'strong', 'brand']);
const DISPLAY = new Set(['block', 'inline', 'inline-block', 'flex', 'inline-flex', 'grid', 'none']);
const ALIGN: Record<string, string> = {start: 'flex-start', center: 'center', end: 'flex-end', stretch: 'stretch', baseline: 'baseline'};
const JUSTIFY: Record<string, string> = {start: 'flex-start', center: 'center', end: 'flex-end', between: 'space-between', around: 'space-around', evenly: 'space-evenly'};
const WIDTH: Record<string, string> = {auto: 'auto', full: '100%', fit: 'fit-content'};
const MAX_WIDTH: Record<string, string> = {sm: '24rem', md: '40rem', lg: '64rem', xl: '80rem', prose: '65ch', none: 'none'};
const TEXT_ALIGN = new Set(['start', 'center', 'end']);

const space = (v: unknown) => (typeof v === 'string' && SPACE.has(v) ? `var(--cre8-spacing-${v})` : undefined);

const SPACING: Record<string, string[]> = {
  padding: ['padding'],
  paddingX: ['padding-inline'],
  paddingY: ['padding-block'],
  margin: ['margin'],
  marginX: ['margin-inline'],
  marginY: ['margin-block'],
};

/** Declarations for every style prop present, given as {xStyleName: value}. */
export function tokenStyles(values: Record<string, unknown>): Decls {
  const out: Decls = {};
  for (const [name, value] of Object.entries(values)) {
    if (name in SPACING) {
      const v = space(value);
      if (v) for (const prop of SPACING[name]) out[prop] = v;
      continue;
    }
    switch (name) {
      case 'display':
        if (typeof value === 'string' && DISPLAY.has(value)) out.display = value;
        break;
      case 'direction':
        if (value === 'row' || value === 'column') out['flex-direction'] = value;
        break;
      case 'gap': {
        const v = space(value);
        if (v) out.gap = v;
        break;
      }
      case 'align':
        if (typeof value === 'string' && ALIGN[value]) out['align-items'] = ALIGN[value];
        break;
      case 'justify':
        if (typeof value === 'string' && JUSTIFY[value]) out['justify-content'] = JUSTIFY[value];
        break;
      case 'wrap':
        if (typeof value === 'boolean') out['flex-wrap'] = value ? 'wrap' : 'nowrap';
        break;
      case 'columns':
        if (Number.isInteger(value) && (value as number) >= 1 && (value as number) <= 6) {
          out['grid-template-columns'] = `repeat(${value}, minmax(0, 1fr))`;
        }
        break;
      case 'background':
        if (typeof value === 'string' && BACKGROUND[value]) out.background = BACKGROUND[value];
        break;
      case 'border':
        if (typeof value === 'string' && BORDER.has(value)) {
          out.border = `var(--cre8-seed-border-width, 1px) solid var(--cre8-color-border-${value})`;
        }
        break;
      case 'radius':
        if (typeof value === 'string' && RADIUS.has(value)) out['border-radius'] = `var(--cre8-radius-${value})`;
        break;
      case 'width':
        if (typeof value === 'string' && WIDTH[value]) out.width = WIDTH[value];
        break;
      case 'maxWidth':
        if (typeof value === 'string' && MAX_WIDTH[value]) out['max-width'] = MAX_WIDTH[value];
        break;
      case 'textAlign':
        if (typeof value === 'string' && TEXT_ALIGN.has(value)) out['text-align'] = value;
        break;
    }
  }
  // Layout props imply their display when none was given.
  if (!out.display && ('flex-direction' in out || 'justify-content' in out || 'flex-wrap' in out)) out.display = 'flex';
  if (!out.display && 'grid-template-columns' in out) out.display = 'grid';
  return out;
}
