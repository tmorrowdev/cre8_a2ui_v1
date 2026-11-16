/**
 * cre8-a2ui theming for the generated surface: light/dark mode plus seed overrides.
 *
 * The cre8 brand in cre8-wc 3.0.1 is the a2ui token set. Every tier is
 * derived from `--cre8-seed-*` and declared on `:root, [data-cre8-theme]`, so
 * putting `data-cre8-theme` on the surface makes seed overrides and
 * `data-mode` resolve inside it alone.
 *
 * One gap: the 246 composite typography tokens (tokens_cre8.css) are declared
 * on `:root` only, so a scoped font seed would never reach them. They are
 * re-declared here on `[data-cre8-theme]`, straight from the shipped sheet.
 */

import typographySheet from '@tmorrow/cre8-wc/design-tokens/brands/cre8/css/tokens_cre8.css?raw';

export type Mode = 'auto' | 'light' | 'dark';

export interface Theme {
  mode: Mode;
  primary: string;
  accent: string;
  neutral: string;
  radius: number; // px
  font: string; // CSS font stack
  googleFont: GoogleFont | null; // loaded from Google Fonts when set
}

export interface GoogleFont {
  family: string;
  weights: number[];
}

/** The a2ui seed values, as shipped. */
export const DEFAULT_THEME: Theme = {
  mode: 'auto',
  primary: '#3b82f6',
  accent: '#7c3aed',
  neutral: '#64748b',
  radius: 24,
  font: '"Plus Jakarta Sans", sans-serif',
  googleFont: null,
};

export const FONTS: Record<string, string> = {
  'Plus Jakarta Sans': '"Plus Jakarta Sans", sans-serif',
  System: 'system-ui, -apple-system, "Segoe UI", sans-serif',
  Serif: 'Georgia, "Times New Roman", serif',
  Mono: 'ui-monospace, "SF Mono", Menlo, monospace',
};

// The font category's generic family, used behind a Google font.
export const FALLBACKS: Record<string, string> = {Serif: 'serif', Mono: 'monospace'};

const FAMILY = /^[A-Za-z0-9][A-Za-z0-9 ]{0,58}[A-Za-z0-9]$/;

/** A Google font from untrusted input (agent seeds, storage), or null if it is not well formed. */
export function parseGoogleFont(value: unknown): GoogleFont | null {
  const v = value as Partial<GoogleFont> | null;
  if (!v || typeof v.family !== 'string' || !FAMILY.test(v.family) || !Array.isArray(v.weights)) return null;
  const weights = v.weights.filter(w => Number.isInteger(w) && w >= 100 && w <= 900 && w % 100 === 0);
  return weights.length ? {family: v.family, weights: [...new Set(weights)].sort((a, b) => a - b)} : null;
}

export const googleFontStack = (font: GoogleFont, category?: string) =>
  `"${font.family}", ${FALLBACKS[category ?? ''] ?? 'sans-serif'}`;

/** The stylesheet URL is built here from a validated family; a URL from agent output is never loaded. */
function loadGoogleFont(font: GoogleFont): void {
  const id = `gf-${font.family.replace(/ /g, '-')}`;
  if (document.getElementById(id)) return;
  const link = document.createElement('link');
  link.id = id;
  link.rel = 'stylesheet';
  link.href = `https://fonts.googleapis.com/css2?family=${font.family.replace(/ /g, '+')}:wght@${font.weights.join(';')}&display=swap`;
  document.head.append(link);
}

const STORAGE_KEY = 'a2ui-apps.theme';

let scopedTypographyInstalled = false;

function installScopedTypography(): void {
  if (scopedTypographyInstalled) return;
  const start = typographySheet.indexOf(':root{');
  if (start < 0) {
    console.warn('tokens_cre8.css changed shape; scoped font seeds will not apply');
    return;
  }
  const style = document.createElement('style');
  style.id = 'cre8-scoped-typography';
  style.textContent = '[data-cre8-theme]{' + typographySheet.slice(start + ':root{'.length);
  document.head.append(style);
  scopedTypographyInstalled = true;
}

export function applyTheme(host: HTMLElement, theme: Theme): void {
  installScopedTypography();
  if (theme.googleFont) loadGoogleFont(theme.googleFont);
  host.setAttribute('data-cre8-theme', '');
  // The token sheet knows "auto" (follows prefers-color-scheme) and "inverse" (dark).
  if (theme.mode === 'auto') host.dataset.mode = 'auto';
  else if (theme.mode === 'dark') host.dataset.mode = 'inverse';
  else delete host.dataset.mode;

  host.style.setProperty('--cre8-seed-primary', theme.primary);
  host.style.setProperty('--cre8-seed-accent', theme.accent);
  host.style.setProperty('--cre8-seed-neutral', theme.neutral);
  host.style.setProperty('--cre8-seed-radius', `${theme.radius}px`);
  host.style.setProperty('--cre8-seed-font', theme.font);
}

export function loadTheme(): Theme {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const stored = JSON.parse(raw);
      return {...DEFAULT_THEME, ...stored, googleFont: parseGoogleFont(stored.googleFont)};
    }
  } catch {
    // Storage blocked or corrupt: fall back to the shipped brand.
  }
  return {...DEFAULT_THEME};
}

export function saveTheme(theme: Theme): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(theme));
  } catch {
    // Non-essential: the theme still applies for this session.
  }
}
