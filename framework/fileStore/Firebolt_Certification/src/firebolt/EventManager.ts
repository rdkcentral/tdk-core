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
 * @file Registers and clears Firebolt event listeners and records each notification, validated against the event's
 * OpenRPC result schema.
 */

import type { CommunicationMode, EventRecord } from '../types';
import { transportAdapter } from './TransportAdapter';
import { sdkAdapter } from './SdkAdapter';
import { UNSUBSCRIBE_NOT_SENT, type NotificationHandler } from './JsonRpcClient';
import { openRpcService } from '../schema/OpenRpcService';
import { schemaValidator } from '../schema/SchemaValidator';
import { entriesToObject, normalizeError, uid } from '../utils/helpers';
import { logger } from '../utils/Logger';

interface ListenerInfo {
  key: string;
  event: string;
  handler: NotificationHandler;
  listenerId: string;
  history: EventRecord[];
  unsubscribe?: () => Promise<unknown>;
  sdkManaged?: boolean;
}

export class EventManager {
  private listeners = new Map<string, ListenerInfo>();

  /**
   * Subscribes ({listen: true}) and records every notification, validated against the event's OpenRPC result schema.
   * eventListenerResponse.subscriptionReply holds the gateway's raw reply (must be null).
   */
  async register(
    event: string,
    params: Record<string, unknown> = {},
    mode: CommunicationMode = 'Transport'
  ): Promise<any> {
    const eventMethod = openRpcService.getMethod(event);
    const listenerId = uid('listener');
    const history: EventRecord[] = [];
    const handler: NotificationHandler = (value) => {
      const validation = eventMethod?.resultSchema
        ? schemaValidator.validate(value, eventMethod.resultSchema)
        : { valid: true, errors: [] };
      history.push({
        event,
        listenerId,
        value,
        timestamp: Date.now(),
        schemaValidation: validation
      });
      if (history.length > 100) history.shift();
      logger.info(`Event ${event}`, value);
    };
    try {
      const subscribeParams = entriesToObject(Object.entries(params || {}).filter(([k]) => k !== 'listen'));
      const subscription =
        mode === 'SDK'
          ? await sdkAdapter.subscribe(event, subscribeParams, (value) =>
              handler(value, { method: event, params: value })
            )
          : undefined;
      const subscriptionReply = subscription
        ? subscription.reply
        : await transportAdapter.subscribe(event, handler, subscribeParams);
      const key = `${event}-${listenerId}`;
      this.listeners.set(key, {
        key,
        event,
        handler,
        listenerId,
        history,
        unsubscribe: subscription?.unsubscribe,
        sdkManaged: subscription?.sdkManaged
      });
      return {
        eventName: event,
        eventListenerId: key,
        eventListenerResponse: { subscriptionReply, sdkManaged: subscription?.sdkManaged ?? false, error: null }
      };
    } catch (error) {
      const err = normalizeError(error);
      return { eventName: event, eventListenerId: null, eventListenerResponse: { error: err } };
    }
  }

  getResponse(listenerKey: string, count = 1): EventRecord[] {
    return (this.listeners.get(listenerKey)?.history || []).slice(-count);
  }
  getAll(): Array<{ key: string; event: string; listenerId: any; count: number }> {
    return [...this.listeners.values()].map((l) => ({
      key: l.key,
      event: l.event,
      listenerId: l.listenerId,
      count: l.history.length
    }));
  }

  /** UI unsubscribe: sends {listen: false} and reports exactly what was sent and what the device replied (expected: null). */
  async unsubscribe(listenerOrEvent: string): Promise<any> {
    const entries = [...this.listeners.values()].filter(
      (l) => l.key === listenerOrEvent || l.event.toLowerCase() === listenerOrEvent.toLowerCase()
    );
    if (!entries.length) return { result: 'No active listener (already unsubscribed or never subscribed)' };
    const eventName = entries[0].event;
    // Reported reply, in order of precedence: a non-null (malformed) reply, then a missing one, then null.
    let reply: unknown = null;
    let missing = false;
    let error: unknown = null;
    let removed = 0;
    let notSent = 0;
    for (const entry of entries) {
      try {
        const r = entry.unsubscribe
          ? await entry.unsubscribe()
          : await transportAdapter.unsubscribe(entry.event, entry.handler, 10000);
        if (r === UNSUBSCRIBE_NOT_SENT) notSent++;
        else if (r === undefined) missing = true;
        else if (r !== null) reply = r;
        this.listeners.delete(entry.key);
        removed++;
      } catch (e) {
        // Keep the entry (and its cleanup handle) so the unsubscribe can be retried.
        logger.warn(`Unable to unsubscribe ${entry.event}`, e);
        error = normalizeError(e);
      }
    }
    // Only local handlers were removed: there is no gateway reply to report, so none is fabricated.
    if (removed && notSent === removed)
      return {
        eventName,
        params: { listen: false },
        listenersRemoved: removed,
        wireUnsubscribeSent: false,
        result: `Listener removed locally; {listen: false} was not sent because another listener for ${eventName} is still active`,
        error
      };
    if (reply === null && missing) reply = undefined;
    return {
      eventName,
      params: { listen: false },
      listenersRemoved: removed,
      unsubscribeReply: reply,
      sdkManaged: entries.every((entry) => entry.sdkManaged),
      error
    };
  }

  async clear(listenerOrEvent: string): Promise<any> {
    const entries = [...this.listeners.values()].filter(
      (l) => l.key === listenerOrEvent || l.event.toLowerCase() === listenerOrEvent.toLowerCase()
    );
    if (!entries.length) return 'No active listener';
    const errors: unknown[] = [];
    for (const entry of entries) {
      try {
        if (entry.unsubscribe) await entry.unsubscribe();
        else await transportAdapter.unsubscribe(entry.event, entry.handler);
        this.listeners.delete(entry.key);
      } catch (e) {
        // Keep the entry (and its cleanup handle) so clearing can be retried.
        logger.warn(`Unable to clear ${entry.event}`, e);
        errors.push(normalizeError(e));
      }
    }
    return errors.length ? { cleared: entries.length - errors.length, errors } : true;
  }

  async clearAll(): Promise<string> {
    const keys = [...this.listeners.keys()];
    for (const key of keys) await this.clear(key);
    // clear() keeps listeners whose unsubscribe failed, so anything left was not cleared.
    const remaining = keys.filter((key) => this.listeners.has(key)).length;
    return remaining
      ? `Unable to clear ${remaining} listener(s)`
      : keys.length
        ? 'Cleared Listeners'
        : 'No active listeners';
  }
}
export const eventManager = new EventManager();
