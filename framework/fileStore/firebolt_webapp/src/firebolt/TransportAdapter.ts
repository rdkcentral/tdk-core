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
 * @file Transport mode: calls Firebolt methods and subscribes to events through the app's own JSON-RPC client.
 */

import { jsonRpcClient, type NotificationHandler } from './JsonRpcClient';

/** Firebolt access over Firebolt Certification's own JSON-RPC client (no @firebolt-js dependency). */
export class TransportAdapter {
  invoke(qualifiedMethod: string, params: Record<string, unknown>, timeoutMs = 10000): Promise<unknown> {
    return jsonRpcClient.call(qualifiedMethod, params, timeoutMs);
  }
  /** Resolves with the gateway's subscription reply; must be result: null. */
  subscribe(
    qualifiedEvent: string,
    handler: NotificationHandler,
    params: Record<string, unknown> = {},
    timeoutMs = 10000
  ): Promise<unknown> {
    return jsonRpcClient.subscribe(qualifiedEvent, handler, params, timeoutMs);
  }
  unsubscribe(
    qualifiedEvent: string,
    handler?: NotificationHandler,
    timeoutMs = 10000,
    force = false
  ): Promise<unknown> {
    return jsonRpcClient.unsubscribe(qualifiedEvent, handler, timeoutMs, force);
  }
}
export const transportAdapter = new TransportAdapter();
