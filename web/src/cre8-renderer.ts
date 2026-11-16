/**
 * Renders a web_core ComponentNode tree as real cre8 elements.
 *
 * web_core's own Lit wrappers put an element between every parent and child.
 * cre8 containers that inspect their direct children (tabs, table rows,
 * selects) would see the wrapper instead, so this renderer walks the resolved
 * node tree and emits <cre8-*> elements directly. web_core still owns the
 * protocol: message processing, data binding, actions and two-way writes.
 *
 * The catalog's annotations map v1.0 names back to the DOM:
 *   x-cre8-tag / x-html-tag (element), x-cre8-prop (renamed prop),
 *   x-cre8-slot, x-cre8-event, and x-style (a token style prop).
 */

import {
  effect,
  getValue,
  isComponentNode,
  isWritable,
  ResolvedBinding,
  type ComponentNode,
} from '@a2ui/web_core/v1_0';
import {tokenStyles} from './token-styles';

type Json = Record<string, any>;

/**
 * Shadow-DOM fixes for cre8-wc 3.0.1 bugs that no token or part can reach.
 * cre8-alert renders into an unstyled <dialog>, whose UA background (Canvas)
 * shows as a white or near-black block around the alert.
 */
const SHADOW_PATCHES: Record<string, string> = {
  'cre8-alert': 'dialog { background: transparent; }',
};
const patchSheets = new Map<string, CSSStyleSheet>();

function patchShadow(el: HTMLElement & Json): void {
  const css = SHADOW_PATCHES[el.localName];
  if (!css || !el.updateComplete) return;
  let sheet = patchSheets.get(css);
  if (!sheet) {
    sheet = new CSSStyleSheet();
    sheet.replaceSync(css);
    patchSheets.set(css, sheet);
  }
  // Lit assigns adoptedStyleSheets when it creates the shadow root, so append after first render.
  el.updateComplete.then(() => {
    const root = el.shadowRoot;
    if (root && !root.adoptedStyleSheets.includes(sheet!)) root.adoptedStyleSheets = [...root.adoptedStyleSheets, sheet!];
  });
}

interface PropSpec {
  kind: 'prop' | 'children' | 'slot' | 'event' | 'style';
  name: string; // cre8 prop, slot, event, or x-style name
}

interface TypeSpec {
  tag: string;
  props: Map<string, PropSpec>;
}

export class Cre8Mapping {
  readonly types = new Map<string, TypeSpec>();

  constructor(catalog: Json) {
    const defs: Json = catalog.$defs ?? {};
    for (const [type, schema] of Object.entries<Json>(catalog.components)) {
      if (type === 'Text') continue;
      const props = new Map<string, PropSpec>();
      const parts: Json[] = schema.allOf ?? [schema];
      for (const part of parts) {
        // Traits (NativeEventHandlers, SpacingProps, BoxStyle) are $refs into $defs.
        const ref: string = part.$ref ?? '';
        const source: Json = ref.startsWith('#/$defs/') ? defs[ref.slice('#/$defs/'.length)] ?? {} : part;
        for (const [key, def] of Object.entries<Json>(source.properties ?? {})) {
          if (key === 'component') continue;
          if (key === 'children') props.set(key, {kind: 'children', name: ''});
          else if (def['x-cre8-slot']) props.set(key, {kind: 'slot', name: def['x-cre8-slot']});
          else if (def['x-cre8-event']) props.set(key, {kind: 'event', name: def['x-cre8-event']});
          else if (def['x-style']) props.set(key, {kind: 'style', name: def['x-style']});
          else props.set(key, {kind: 'prop', name: def['x-cre8-prop'] ?? key});
        }
      }
      props.set('ariaLabel', props.get('ariaLabel') ?? {kind: 'prop', name: 'aria-label'});
      this.types.set(type, {tag: schema['x-cre8-tag'] ?? schema['x-html-tag'], props});
    }
  }
}

interface Mounted {
  el: Element | Text;
  dispose: () => void;
}

const unwrap = (value: unknown): unknown => (value instanceof ResolvedBinding ? value.value : value);

export class Cre8Renderer {
  private readonly mounted = new Map<string, Mounted>();

  constructor(private readonly mapping: Cre8Mapping) {}

  /** Element for a node, created once per node id and kept in sync by an effect. */
  mount(node: ComponentNode): Element | Text {
    const existing = this.mounted.get(node.id);
    if (existing) return existing.el;

    if (node.type === 'Text') {
      const text = document.createTextNode('');
      const dispose = effect(() => {
        text.data = String(unwrap(getValue(node.props).text) ?? '');
      });
      return this.remember(node, text, dispose);
    }

    const spec = this.mapping.types.get(node.type);
    if (!spec) {
      const missing = document.createElement('span');
      missing.textContent = `[unknown component ${node.type}]`;
      return this.remember(node, missing, () => {});
    }

    const el = document.createElement(spec.tag) as HTMLElement & Json;
    el.__a2uiNode = node; // for debugging: the ComponentNode this element renders
    patchShadow(el);
    const listeners = new Map<string, EventListener>();
    const writes: Record<string, (v: unknown) => void> = {};
    const onInput = () => {
      if (writes.value && 'value' in el) writes.value(el.value);
      if (writes.checked && 'checked' in el) writes.checked(el.checked);
    };
    el.addEventListener('input', onInput);
    el.addEventListener('change', onInput);

    // A prop the agent stops sending must go back to the element's own default,
    // or an update that drops `isError` would leave the error showing.
    const defaults = new Map<string, unknown>();
    let applied = new Set<string>();
    let appliedCss = new Set<string>();

    const dispose = effect(() => {
      const props = getValue(node.props) as Json;
      const content: Array<[ComponentNode, string | null]> = [];
      const current = new Set<string>();
      const styleValues: Record<string, unknown> = {};
      for (const key of Object.keys(writes)) delete writes[key];

      for (const [key, raw] of Object.entries(props)) {
        const p = spec.props.get(key) ?? {kind: 'prop' as const, name: key};
        if (p.kind === 'children' || p.kind === 'slot') {
          for (const child of (unwrap(raw) as unknown[]) ?? []) {
            if (isComponentNode(child)) content.push([child, p.kind === 'slot' ? p.name : null]);
          }
        } else if (p.kind === 'style') {
          const value = unwrap(raw);
          if (value !== undefined) styleValues[p.name] = value;
        } else if (p.kind === 'event') {
          const prior = listeners.get(p.name);
          if (prior) el.removeEventListener(p.name, prior);
          if (typeof raw === 'function') {
            const handler = () => void (raw as () => unknown)();
            listeners.set(p.name, handler);
            el.addEventListener(p.name, handler);
          }
        } else {
          // The binder lists every catalog prop; unset ones resolve to undefined.
          if (unwrap(raw) === undefined) continue;
          if (raw instanceof ResolvedBinding && isWritable(raw)) writes[p.name] = raw.set;
          if (!defaults.has(p.name)) defaults.set(p.name, p.name.includes('-') ? undefined : el[p.name]);
          current.add(p.name);
          this.setProp(el, p.name, unwrap(raw));
        }
      }
      for (const name of applied) {
        if (!current.has(name)) this.setProp(el, name, defaults.get(name));
      }
      applied = current;
      appliedCss = this.applyStyles(el, tokenStyles(styleValues), appliedCss);
      this.reconcile(el, content);
    });

    return this.remember(node, el, () => {
      dispose();
      for (const [name, handler] of listeners) el.removeEventListener(name, handler);
      el.removeEventListener('input', onInput);
      el.removeEventListener('change', onInput);
    });
  }

  private remember(node: ComponentNode, el: Element | Text, dispose: () => void): Element | Text {
    this.mounted.set(node.id, {el, dispose});
    node.onDestroyed.subscribe(() => {
      dispose();
      this.mounted.delete(node.id);
    });
    return el;
  }

  /** Set these declarations and remove the ones this renderer set last time but not now. */
  private applyStyles(el: HTMLElement, decls: Record<string, string>, previous: Set<string>): Set<string> {
    for (const prop of previous) if (!(prop in decls)) el.style.removeProperty(prop);
    for (const [prop, value] of Object.entries(decls)) el.style.setProperty(prop, value);
    return new Set(Object.keys(decls));
  }

  private setProp(el: HTMLElement & Json, name: string, value: unknown): void {
    if (name.includes('-')) {
      if (value === undefined || value === null || value === false) el.removeAttribute(name);
      else el.setAttribute(name, value === true ? '' : String(value));
      return;
    }
    // Keep the caret where it is when the data model echoes what was typed.
    if (name === 'value' && el.value === value) return;
    el[name] = value;
    // cre8 does not reflect `status`; mirrored so status.css can color per status (help).
    if (name === 'status') {
      if (typeof value === 'string') el.dataset.status = value;
      else delete el.dataset.status;
    }
  }

  /** Make `el`'s children exactly `content`, in order, moving rather than recreating. */
  private reconcile(el: Element, content: Array<[ComponentNode, string | null]>): void {
    const wanted: Node[] = content.map(([child, slot]) => {
      const node = this.mount(child);
      if (slot === null || slot === 'default') {
        if (node instanceof Element) node.removeAttribute('slot');
        return node;
      }
      if (node instanceof Element) {
        node.setAttribute('slot', slot);
        return node;
      }
      // Text can only be slotted through an element.
      const span = document.createElement('span');
      span.setAttribute('slot', slot);
      span.append(node);
      return span;
    });
    wanted.forEach((node, i) => {
      if (el.childNodes[i] !== node) el.insertBefore(node, el.childNodes[i] ?? null);
    });
    while (el.childNodes.length > wanted.length) el.lastChild!.remove();
  }
}
