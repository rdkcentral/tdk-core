import type { LifecycleRecord } from '../types';
import { fireboltAdapter } from '../firebolt/FireboltAdapter';
import { logger } from '../utils/Logger';
import { runtimeConfig } from '../config/runtime';
import { extensionRegistry } from '../extensions/ExtensionRegistry';

export class LifecycleManager {
  private history: LifecycleRecord[] = [];
  private recording = false;

  constructor() {
    document.addEventListener('visibilitychange', () =>
      this.record('visibilityState', document.visibilityState, 'browser')
    );
    window.addEventListener('pageshow', () => this.record('pageshow', undefined, 'browser'));
    window.addEventListener('pagehide', () => this.record('pagehide', undefined, 'browser'));
  }
  start(appId: string): string {
    this.recording = true;
    this.history = [];
    this.record('recording-started', appId, 'firebolt-certification');
    return `Lifecycle History Recording has been started for ${appId}`;
  }
  stop(appId: string): { appId: string; history: LifecycleRecord[] } {
    this.record('recording-stopped', appId, 'firebolt-certification');
    this.recording = false;
    const out = { appId, history: [...this.history] };
    this.history = [];
    return out;
  }
  record(event: string, value?: unknown, source: LifecycleRecord['source'] = 'firebolt'): void {
    if (!this.recording && source === 'firebolt') return;
    this.history.push({ event, value, timestamp: Date.now(), source });
    if (this.history.length > 300) this.history.shift();
  }
  async call(
    method: string,
    params: unknown[] | Record<string, unknown> = [],
    mode: 'SDK' | 'Transport' = 'Transport'
  ): Promise<any> {
    const extension = extensionRegistry.lifecycleHandler(runtimeConfig.appType, method);
    if (extension) {
      const response = await Promise.resolve(extension(params));
      this.record(method, response, 'firebolt');
      return { method, response, status: 'PASS', mode, durationMs: 0, timestamp: Date.now() };
    }
    const qualified = method.includes('.') ? method : `Lifecycle.${method}`;
    const result = await fireboltAdapter.invoke({ method: qualified, params, mode });
    this.record(qualified, result.response ?? result.error, 'firebolt');
    logger.info(`Lifecycle ${qualified} ${result.status}`);
    return result;
  }
}
export const lifecycleManager = new LifecycleManager();
