import '@tmorrow/cre8-wc';
import '@tmorrow/cre8-wc/design-tokens/brands/cre8/css/tokens_cre8.css';
import './status.css';
import './page.css';

import {
  Catalog,
  effect,
  getValue,
  MessageProcessor,
  NodeResolver,
  type ActionPayload,
  type SurfaceModel,
} from '@a2ui/web_core/v1_0';
import {Cre8Mapping, Cre8Renderer} from './cre8-renderer';
import {postRpc, withFunctionImplementations} from './rpc';
import {applyTheme, DEFAULT_THEME, FONTS, googleFontStack, loadTheme, parseGoogleFont, saveTheme, type Theme} from './theme';

const $ = <T extends Element>(sel: string) => document.querySelector(sel) as T;
const form = $<HTMLFormElement>('#prompt-form');
const input = $<HTMLTextAreaElement>('#prompt');
const host = $<HTMLElement>('#surface');
const traceEl = $<HTMLElement>('#trace');
const statusEl = $<HTMLElement>('#status');
const agentEl = $<HTMLElement>('#agent');
const formatEl = $<HTMLSelectElement>('#format');
const editBtn = $<HTMLButtonElement>('#edit');
let currentSurfaceId: string | undefined;

let processor: MessageProcessor;
// Set by setupTheme: merges a partial theme, applies it to the surface and syncs the panel.
let patchTheme: (patch: Partial<Theme>) => void = () => {};

/** Seeds chosen by the agent's theme tool (a {"theme"} event or a cre8_theme surface extension). */
function applyAgentTheme(seeds: Record<string, any>) {
  const patch: Partial<Theme> = {};
  if (seeds.mode === 'auto' || seeds.mode === 'light' || seeds.mode === 'dark') patch.mode = seeds.mode;
  for (const key of ['primary', 'accent', 'neutral'] as const) if (typeof seeds[key] === 'string') patch[key] = seeds[key];
  if (typeof seeds.radius === 'number') patch.radius = seeds.radius;
  if (typeof seeds.font === 'string' && FONTS[seeds.font]) patch.font = FONTS[seeds.font];
  const google = parseGoogleFont(seeds.googleFont);
  if (google) {
    patch.googleFont = google;
    patch.font = googleFontStack(google, seeds.font);
  }
  patchTheme(patch);
}
let renderer: Cre8Renderer;
let teardown: (() => void) | undefined;

function setStatus(text: string, kind: 'info' | 'error' = 'info') {
  statusEl.textContent = text;
  statusEl.dataset.kind = kind;
}

async function readJsonl(res: Response, onLine: (value: any) => void) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body?.detail?.message ?? `HTTP ${res.status}`);
  }
  const reader = res.body!.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = '';
  for (;;) {
    const {value, done} = await reader.read();
    if (value) buffer += value;
    let nl: number;
    while ((nl = buffer.indexOf('\n')) >= 0) {
      const line = buffer.slice(0, nl).trim();
      buffer = buffer.slice(nl + 1);
      if (line) onLine(JSON.parse(line));
    }
    if (done) break;
  }
  if (buffer.trim()) onLine(JSON.parse(buffer));
}

type Step = {name: string; deterministic: boolean; detail: string};

/** One line from /api/generate (an event) or /api/action (a bare A2UI message). */
function apply(line: any) {
  if (line.a2ui) processor.processMessages(line.a2ui);
  else if (line.version) processor.processMessages(line);
  else if (line.text) agentEl.textContent = (agentEl.textContent ?? '') + line.text;
  else if (line.theme) applyAgentTheme(line.theme);
  else if (line.step) {
    // A repair restarts the answer: drop the rejected attempt's sentence.
    if (line.step.name === 'repair') agentEl.textContent = '';
    appendStep(line.step);
  }
  else if (line.error) throw new Error(line.error.message ?? 'generation failed');
  else if (line.trace) {
    renderTrace(line.trace.steps);
    currentSurfaceId = line.trace.surfaceId;
    editBtn.disabled = false;
  }
}

async function sendAction(action: ActionPayload) {
  const surfaces = (processor.getRendererDataModel('1.0') as any)?.surfaces ?? {};
  setStatus(`action "${action.name}" sent…`);
  try {
    await readJsonl(
      await fetch('/api/action', {
        method: 'POST',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({message: {version: '1.0', action}, dataModel: surfaces[action.surfaceId]}),
      }),
      apply,
    );
    setStatus(`action "${action.name}" handled`);
  } catch (e) {
    setStatus(String((e as Error).message), 'error');
  }
}

function mountSurface(surface: SurfaceModel<any>) {
  teardown?.();
  // A2UI v1.0 keeps branding out of createSurface; the agent's seeds ride in an extension.
  const seeds = (surface as any).metadata?.extensions?.cre8_theme;
  if (seeds) applyAgentTheme(seeds);
  const resolver = new NodeResolver(surface);
  const stop = effect(() => {
    const root = getValue(resolver.rootNode);
    host.replaceChildren(...(root ? [renderer.mount(root)] : []));
  });
  teardown = () => {
    stop();
    resolver.dispose();
  };
}

function stepItem(step: Step): HTMLLIElement {
  const li = document.createElement('li');
  li.dataset.deterministic = String(step.deterministic);
  li.append(Object.assign(document.createElement('b'), {textContent: `${step.name}${step.deterministic ? '' : ' · model'}`}), ' ');
  li.append(Object.assign(document.createElement('span'), {textContent: step.detail}));
  return li;
}

function appendStep(step: Step) {
  traceEl.append(stepItem(step));
}

function renderTrace(steps: Step[]) {
  traceEl.replaceChildren(...steps.map(stepItem));
}

async function generate(prompt: string, editSurfaceId?: string) {
  setStatus('generating…');
  traceEl.replaceChildren();
  agentEl.textContent = '';
  try {
    await readJsonl(
      await fetch('/api/generate', {
        method: 'POST',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({prompt, format: formatEl.value, surfaceId: editSurfaceId, rendererFunctions: true}),
      }),
      apply,
    );
    setStatus('ready');
  } catch (e) {
    setStatus(String((e as Error).message), 'error');
  }
}

function setupTheme() {
  const panel = $<HTMLFieldSetElement>('#theme');
  const field = <T extends Element>(name: string) => panel.querySelector(`[name="${name}"]`) as T;
  const fontSelect = field<HTMLSelectElement>('font');
  for (const [label, stack] of Object.entries(FONTS)) fontSelect.add(new Option(label, stack));
  // One extra option for the Google font in the theme (or a stack the presets do not cover).
  const extraFont = new Option('', '');
  const syncFontOption = () => {
    const preset = Object.values(FONTS).includes(theme.font);
    extraFont.value = theme.font;
    extraFont.text = theme.googleFont ? `${theme.googleFont.family} (Google)` : theme.font;
    if (preset && !theme.googleFont) extraFont.remove();
    else if (!extraFont.parentElement) fontSelect.add(extraFont);
  };

  let theme = loadTheme();
  const sync = () => {
    field<HTMLSelectElement>('mode').value = theme.mode;
    field<HTMLInputElement>('primary').value = theme.primary;
    field<HTMLInputElement>('accent').value = theme.accent;
    field<HTMLInputElement>('neutral').value = theme.neutral;
    field<HTMLInputElement>('radius').value = String(theme.radius);
    field<HTMLOutputElement>('radiusOut').value = `${theme.radius}px`;
    syncFontOption();
    fontSelect.value = theme.font;
  };
  const update = (patch: Partial<Theme>) => {
    theme = {...theme, ...patch};
    applyTheme(host, theme);
    saveTheme(theme);
    sync();
  };
  patchTheme = update;
  panel.addEventListener('input', e => {
    const el = e.target as HTMLInputElement | HTMLSelectElement;
    if (el.name === 'radius') update({radius: Number(el.value)});
    else if (el.name in DEFAULT_THEME) update({[el.name]: el.value} as Partial<Theme>);
  });
  field<HTMLButtonElement>('reset').addEventListener('click', () => update({...DEFAULT_THEME}));
  applyTheme(host, theme);
  sync();
}

const CHAT_WIDTH_KEY = 'a2ui-apps.chatWidth';

/** Draggable divider between chat and stage (keyboard: arrow keys), plus true full screen for the stage. */
function setupLayout() {
  const splitter = $<HTMLElement>('#splitter');
  const setWidth = (px: number) => {
    const width = Math.round(Math.min(Math.max(px, 280), window.innerWidth * 0.6));
    document.body.style.setProperty('--chat-width', `${width}px`);
    return width;
  };
  try {
    const stored = Number(localStorage.getItem(CHAT_WIDTH_KEY));
    if (stored) setWidth(stored);
  } catch {
    // Storage blocked: default width.
  }
  const save = () => {
    try {
      localStorage.setItem(CHAT_WIDTH_KEY, String($<HTMLElement>('#chat').offsetWidth));
    } catch {
      // Non-essential.
    }
  };
  splitter.addEventListener('pointerdown', e => {
    splitter.setPointerCapture(e.pointerId);
    splitter.classList.add('dragging');
    const move = (ev: PointerEvent) => setWidth(ev.clientX);
    const up = () => {
      splitter.classList.remove('dragging');
      splitter.removeEventListener('pointermove', move);
      save();
    };
    splitter.addEventListener('pointermove', move);
    splitter.addEventListener('pointerup', up, {once: true});
  });
  splitter.addEventListener('keydown', e => {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    e.preventDefault();
    setWidth($<HTMLElement>('#chat').offsetWidth + (e.key === 'ArrowRight' ? 24 : -24));
    save();
  });

  const stage = $<HTMLElement>('#stage');
  const button = $<HTMLButtonElement>('#fullscreen');
  if (!document.fullscreenEnabled) button.hidden = true;
  button.addEventListener('click', () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else stage.requestFullscreen().catch(err => setStatus(`full screen unavailable: ${err.message}`, 'error'));
  });
  document.addEventListener('fullscreenchange', () => {
    button.textContent = document.fullscreenElement ? 'Exit full screen' : 'Full screen';
  });
}

async function boot() {
  setupLayout();
  setupTheme();
  const catalogDoc = await (await fetch('/api/catalog')).json();
  const ref: {current?: MessageProcessor<any>} = {};
  const catalog = withFunctionImplementations(Catalog.fromJson(catalogDoc, '1.0') as Catalog<any>, ref, catalogDoc.catalogId);
  renderer = new Cre8Renderer(new Cre8Mapping(catalogDoc));
  processor = new MessageProcessor([catalog], action => sendAction(action), {
    version: '1.0',
    reportErrorsOnly: true,
    errorHandler: err => setStatus(`${err.error.code}: ${err.error.message}`, 'error'),
    // Renderer-to-agent RPC: rendererFunctionResponse and callAgentFunction go to /api/rpc.
    outboundListener: message => postRpc(message, processor).catch(e => setStatus(String(e), 'error')),
  });
  ref.current = processor;
  processor.onSurfaceCreated(mountSurface);
  if (import.meta.env.DEV) (window as any).__a2ui = {processor, renderer};
  editBtn.addEventListener('click', () => {
    if (input.value.trim() && currentSurfaceId) void generate(input.value.trim(), currentSurfaceId);
  });
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (input.value.trim()) void generate(input.value.trim());
  });
  for (const chip of document.querySelectorAll<HTMLButtonElement>('[data-example]')) {
    chip.addEventListener('click', () => {
      input.value = chip.dataset.example!;
      void generate(input.value);
    });
  }
  setStatus('ready');
}

void boot();
