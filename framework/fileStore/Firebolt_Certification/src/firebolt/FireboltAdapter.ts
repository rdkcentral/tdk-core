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
 * @file Single entry point for Firebolt calls: routes each method to the Transport or SDK adapter (or a registered
 * extension) and returns a uniform ExecutionResult.
 */

import type { CommunicationMode, ExecutionResult } from '../types';
import { transportAdapter } from './TransportAdapter';
import { sdkAdapter } from './SdkAdapter';
import { openRpcService } from '../schema/OpenRpcService';
import { entriesToObject, normalizeError, positionalParams, uid, withTimeout } from '../utils/helpers';
import { extensionRegistry } from '../extensions/ExtensionRegistry';

export interface InvokeOptions {
  method: string;
  params?: unknown[] | Record<string, unknown>;
  mode?: CommunicationMode;
  timeoutMs?: number;
}

export class FireboltAdapter {
  async invoke(options: InvokeOptions): Promise<ExecutionResult> {
    const started = performance.now();
    const method = options.method.charAt(0).toUpperCase() + options.method.slice(1);
    const mode = options.mode || 'Transport';
    const params = options.params ?? [];
    const timeoutMs = options.timeoutMs || 10000;
    try {
      let response: unknown;
      const extensionInvoker = extensionRegistry.findInvoker(method);
      if (mode === 'SDK') {
        response = await sdkAdapter.invoke(method, params, timeoutMs);
      } else if (extensionInvoker) {
        response = await withTimeout(Promise.resolve(extensionInvoker({ method, params, mode })), timeoutMs);
      } else {
        response = await transportAdapter.invoke(method, this.toNamedParams(method, params), timeoutMs);
      }
      return {
        id: uid('exec'),
        method,
        mode,
        status: 'PASS',
        durationMs: Math.round(performance.now() - started),
        timestamp: Date.now(),
        params,
        response
      };
    } catch (error) {
      return {
        id: uid('exec'),
        method,
        mode,
        status: 'FAIL',
        durationMs: Math.round(performance.now() - started),
        timestamp: Date.now(),
        params,
        error: normalizeError(error)
      };
    }
  }

  /** JSON-RPC params are always an object; positional arrays are mapped onto the OpenRPC param names. */
  toNamedParams(method: string, params: unknown[] | Record<string, unknown>): Record<string, unknown> {
    if (!Array.isArray(params)) return params;
    const schemaMethod = openRpcService.getMethod(method);
    const names =
      (schemaMethod?.params ? positionalParams(method, schemaMethod.params) : undefined)?.map((p) => p.name) ||
      params.map((_, i) => `arg${i}`);
    return entriesToObject(params.map((value, i) => [names[i] || `arg${i}`, value] as [string, unknown]));
  }
}
export const fireboltAdapter = new FireboltAdapter();
