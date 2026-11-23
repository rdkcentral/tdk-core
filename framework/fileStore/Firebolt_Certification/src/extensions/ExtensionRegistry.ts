import type { CommunicationMode } from '../types';

export type ExtensionInvokeContext = {
  method: string;
  params: unknown[] | Record<string, unknown>;
  mode: CommunicationMode;
};
export type ExtensionInvoker = (context: ExtensionInvokeContext) => Promise<unknown> | unknown;
export type ExternalResponseHandler = (apiResponse: any) => string;
export type LifecycleExtension = (params: unknown[] | Record<string, unknown>) => Promise<unknown> | unknown;

/**
 * Replacement for the original Firebolt Certification webpack plugin hooks. Integrators can register
 * additional SDK/module invokers without coupling them to the Preact UI.
 */
export class ExtensionRegistry {
  private invokers = new Map<string, ExtensionInvoker>();
  private externalResponseHandler: ExternalResponseHandler | null = null;
  private lifecycle = new Map<string, LifecycleExtension>();

  registerInvoker(methodPrefix: string, invoker: ExtensionInvoker): void {
    this.invokers.set(methodPrefix.toLowerCase(), invoker);
  }
  findInvoker(method: string): ExtensionInvoker | undefined {
    const lower = method.toLowerCase();
    const key = [...this.invokers.keys()].find((candidate) => lower.startsWith(candidate));
    return key ? this.invokers.get(key) : undefined;
  }
  registerExternalResponseHandler(handler: ExternalResponseHandler): void {
    this.externalResponseHandler = handler;
  }
  setExternalApiResponse(apiResponse: any): string {
    return this.externalResponseHandler
      ? this.externalResponseHandler(apiResponse)
      : 'Unable to import and set the data for external module';
  }
  registerLifecycle(appType: string, method: string, handler: LifecycleExtension): void {
    this.lifecycle.set(`${appType.toLowerCase()}:${method.toLowerCase()}`, handler);
  }
  lifecycleHandler(appType: string, method: string): LifecycleExtension | undefined {
    return this.lifecycle.get(`${appType.toLowerCase()}:${method.toLowerCase()}`);
  }
}
export const extensionRegistry = new ExtensionRegistry();
