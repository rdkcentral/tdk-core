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
 * @file SDK mode: waits for the device's window.FireboltServiceManager and calls its API wrappers through the
 * upstream certification runner.
 */

import { runner } from '../../.firebolt-sdk/runner.js';
import methodShapes from '../../.firebolt-sdk/method-shapes.json';
import { openRpcService } from '../schema/OpenRpcService.js';
import { entriesToObject, positionalParams, withTimeout } from '../utils/helpers.js';
import { logger } from '../utils/Logger.js';

export type SdkMethod = (...args: unknown[]) => unknown;
export type FireboltClient = Record<string, Record<string, SdkMethod>>;
export interface RunnerEntry {
  module: string;
  method: string;
  name: string;
  kind: 'call' | 'subscribe';
  args: unknown[];
}
export interface RunnerResult {
  name: string;
  ok: boolean;
  value?: unknown;
  error?: string;
  requestTime: number;
  responseTime: number;
  duration: number;
}
export interface SdkSubscription {
  reply: unknown;
  sdkManaged: boolean;
  unsubscribe: () => Promise<unknown>;
}
interface MethodShape {
  kind: string;
  parameter?: string;
}
interface SdkWindow extends Window {
  FireboltServiceManager?: { get(): FireboltClient | Promise<FireboltClient> };
}

export class SdkAdapter {
  private client: Promise<FireboltClient> | undefined;

  private async waitForManager(timeoutMs: number): Promise<NonNullable<SdkWindow['FireboltServiceManager']>> {
    const deadline = Date.now() + timeoutMs;
    while (true) {
      const manager = (window as SdkWindow).FireboltServiceManager;
      if (manager !== undefined) {
        if (!manager || typeof manager.get !== 'function')
          throw { code: 'SdkManagerInvalid', message: 'Device FireboltServiceManager does not expose get().' };
        return manager;
      }
      const remaining = deadline - Date.now();
      if (remaining <= 0)
        throw {
          code: 'SdkManagerNotAvailable',
          message: `Device did not supply FireboltServiceManager within ${timeoutMs} ms. SDK calls require the device-provided client; no fallback is allowed.`
        };
      await new Promise<void>((resolve) => window.setTimeout(resolve, Math.min(100, remaining)));
    }
  }

  private getClient(timeoutMs: number): Promise<FireboltClient> {
    if (this.client) return withTimeout(this.client, timeoutMs);
    if (!this.client) {
      const deadline = Date.now() + timeoutMs;
      this.client = this.waitForManager(timeoutMs)
        .then(async (manager) => {
          const client = await withTimeout(
            Promise.resolve().then(() => manager.get()),
            Math.max(1, deadline - Date.now())
          );
          if (!client || typeof client !== 'object' || Array.isArray(client))
            throw {
              code: 'SdkClientInvalid',
              message: 'Device FireboltServiceManager.get() did not return a Firebolt client.'
            };
          return client;
        })
        .catch((error: unknown) => {
          this.client = undefined;
          throw error;
        });
    }
    return this.client;
  }

  private shape(method: string): [string, MethodShape] {
    const name = Object.keys(methodShapes).find((key) => key.toLowerCase() === method.toLowerCase());
    if (!name) {
      const schema = openRpcService.getMethod(method);
      return [
        schema?.name || method,
        { kind: /\.on[A-Z]/.test(method) ? 'Subscribe' : schema?.params.length === 0 ? 'NoParams' : 'WithObjectParam' }
      ];
    }
    return [name, methodShapes[name as keyof typeof methodShapes]];
  }

  private namedParams(method: string, params: unknown[] | Record<string, unknown>): Record<string, unknown> {
    if (!Array.isArray(params)) return params;
    if (!params.length) return {};
    const schema = openRpcService.getMethod(method);
    if (!schema)
      throw {
        code: 'SdkInvalidParams',
        message: `OpenRPC metadata is required to map positional parameters for ${method}.`
      };
    const names = positionalParams(method, schema.params).map((p) => p.name);
    if (params.length > names.length)
      throw { code: 'SdkInvalidParams', message: `Too many positional parameters for ${method}.` };
    return entriesToObject(params.map((value, index) => [names[index], value]));
  }

  private async run(name: string, args: unknown[], timeoutMs: number): Promise<unknown> {
    const deadline = Date.now() + timeoutMs;
    const client = await this.getClient(timeoutMs);
    const [moduleName, methodName] = name.split('.');
    const moduleKey =
      moduleName in client
        ? moduleName
        : Object.keys(client).find((key) => key.toLowerCase() === moduleName.toLowerCase());
    const module = moduleKey ? client[moduleKey] : undefined;
    const method = module && module[methodName];
    if (typeof method !== 'function')
      throw {
        code: 'SdkMethodNotAvailable',
        message: `Device FireboltServiceManager client does not provide an SDK wrapper for ${name}. No fallback is allowed.`
      };
    let failure: unknown;
    let failed = false;
    let result: RunnerResult | undefined;
    const boundClient: FireboltClient = {
      [moduleName]: {
        [methodName]: async (...values: unknown[]) => {
          let abandoned = false;
          try {
            const operation = Promise.resolve(method.apply(module, values));
            void operation.then(
              (value) => {
                if (abandoned && typeof value === 'function') {
                  void Promise.resolve()
                    .then(() => value())
                    .catch((error: unknown) => logger.warn(`Unable to release timed-out SDK listener ${name}`, error));
                }
              },
              () => {}
            );
            return await withTimeout(operation, Math.max(1, deadline - Date.now()));
          } catch (error) {
            abandoned = true;
            failed = true;
            failure = error;
            throw error;
          }
        }
      }
    };
    // Use call entries for subscriptions too: the upstream subscribe kind immediately discards its listener.
    await runner.run([{ module: moduleName, method: methodName, name, kind: 'call', args }], boundClient, (row) => {
      result = row;
    });
    if (failed) throw failure;
    if (!result?.ok) throw new Error(result?.error || `The Firebolt runner returned no result for ${name}.`);
    return result.value;
  }

  async invoke(method: string, params: unknown[] | Record<string, unknown>, timeoutMs = 10000): Promise<unknown> {
    const [name, shape] = this.shape(method);
    if (shape.kind === 'Subscribe') {
      const named = this.namedParams(name, params);
      if (named.listen === false)
        throw {
          code: 'SdkInvalidParams',
          message: `Use the Events page or clearEventHandler to release an active SDK listener for ${name}.`
        };
      const subscription = await this.subscribe(name, named, () => {}, timeoutMs);
      await subscription.unsubscribe();
      return { subscriptionAccepted: true, unsubscribed: true };
    }
    const named = this.namedParams(name, params);
    if (shape.kind === 'NoParams' && Object.keys(named).length)
      throw { code: 'SdkInvalidParams', message: `${name} does not accept SDK parameters.` };
    if (
      shape.kind === 'WithPrimitiveWrap' &&
      (!shape.parameter || Object.keys(named).some((key) => key !== shape.parameter))
    ) {
      throw { code: 'SdkInvalidParams', message: `${name} accepts only the ${shape.parameter} SDK parameter.` };
    }
    const args =
      shape.kind === 'NoParams'
        ? []
        : shape.kind === 'WithPrimitiveWrap' && shape.parameter
          ? [named[shape.parameter]]
          : [named];
    return this.run(name, args, timeoutMs);
  }

  async subscribe(
    method: string,
    params: Record<string, unknown>,
    callback: (value: unknown) => void,
    timeoutMs = 10000
  ): Promise<SdkSubscription> {
    const [name, shape] = this.shape(method);
    if (shape.kind !== 'Subscribe') throw { code: 'SdkInvalidParams', message: `${name} is not an SDK event.` };
    if (Object.keys(params).some((key) => key !== 'listen'))
      throw {
        code: 'SdkInvalidParams',
        message: `${name} accepts only a callback in the device Firebolt web SDK; contextual event parameters are not supported.`
      };
    const unsubscribe = await this.run(name, [callback], timeoutMs);
    if (typeof unsubscribe !== 'function')
      throw new Error(`SDK subscription ${name} did not return an unsubscribe function.`);
    return {
      sdkManaged: true,
      reply: { subscriptionAccepted: true },
      unsubscribe: async () => {
        await withTimeout(Promise.resolve().then(() => unsubscribe()), timeoutMs);
        return { unsubscribed: true };
      }
    };
  }
}

export const sdkAdapter = new SdkAdapter();
