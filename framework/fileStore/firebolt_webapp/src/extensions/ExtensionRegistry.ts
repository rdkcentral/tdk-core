/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2026 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @file Registry for integrator hooks: custom method invokers, external API response handling and lifecycle extensions.
 */

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
