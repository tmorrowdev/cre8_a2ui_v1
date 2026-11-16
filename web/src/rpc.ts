/**
 * Function RPC for the cre8 surface, both directions.
 *
 * - Renderer functions (agentOnly in the catalog): implemented here. The agent
 *   sends callRendererFunction; web_core runs the implementation and hands the
 *   rendererFunctionResponse to the outbound listener, which posts it.
 * - Agent functions: declared in the catalog without an implementation.
 *   web_core 0.15.0 has no automatic routing for those (it landed after 0.15.0),
 *   so each gets a forwarding implementation here: it returns a signal and fills
 *   it from processor.callAgentFunction, which makes a property binding like
 *   `daysUntil($/event/date)` update when the agent answers.
 */

import {
  createFunctionImplementation,
  setValue,
  signal,
  type Catalog,
  type DataContext,
  type FunctionImplementation,
  type MessageProcessor,
} from '@a2ui/web_core/v1_0';

const RENDERER_FUNCTIONS: Record<string, () => unknown> = {
  // The app renders in the stage pane, not the window: report the space it actually gets.
  getViewport: () => {
    const surface = document.getElementById('surface');
    return surface
      ? {width: surface.clientWidth, height: surface.clientHeight}
      : {width: window.innerWidth, height: window.innerHeight};
  },
  getPreferences: () => ({
    colorScheme: matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
    reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches,
    locale: navigator.language,
  }),
};

type ProcessorRef = {current?: MessageProcessor<any>};

/** The catalog with implementations attached for every function it declares. */
export function withFunctionImplementations(catalog: Catalog<any, any>, processor: ProcessorRef, catalogId: string): Catalog<any, any> {
  const implementations: FunctionImplementation[] = [];
  for (const api of catalog.functions.values()) {
    const local = RENDERER_FUNCTIONS[api.name];
    if (local) {
      implementations.push(createFunctionImplementation(api as any, () => local() as any));
    } else if (api.allowedCallers !== 'agentOnly') {
      implementations.push(createFunctionImplementation(api as any, ((args: Record<string, unknown>, context: DataContext) => {
        const result = signal<unknown>(undefined);
        const surfaceId = (context as any)?.surface?.id;
        processor.current
          ?.callAgentFunction(surfaceId, {'@call': api.name, catalogId, args} as any)
          .then(value => setValue(result, value))
          .catch(err => console.warn(`agent function ${api.name} failed`, err));
        return result;
      }) as any));
    }
  }
  return catalog.withEntries([...catalog.components.values()], implementations);
}

/** Post one renderer-to-agent message; feed the agent's replies back to the processor. */
export async function postRpc(message: unknown, processor: MessageProcessor<any>): Promise<void> {
  const res = await fetch('/api/rpc', {
    method: 'POST',
    headers: {'content-type': 'application/json'},
    body: JSON.stringify(message),
  });
  if (!res.ok) throw new Error(`rpc ${res.status}`);
  const text = await res.text();
  for (const line of text.split('\n')) {
    if (line.trim()) processor.processMessages(JSON.parse(line));
  }
}
