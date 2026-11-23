import type { CommunicationMode, EventRecord } from '../types';
import { transportAdapter } from './TransportAdapter';
import { sdkAdapter } from './SdkAdapter';
import type { NotificationHandler } from './JsonRpcClient';
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
   * eventListenerResponse.subscriptionReply holds the gateway's raw reply (RDK8+ requires null).
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

  /** UI unsubscribe: sends {listen: false} and reports exactly what was sent and what the device replied (RDK8+: null). */
  async unsubscribe(listenerOrEvent: string): Promise<any> {
    const entries = [...this.listeners.values()].filter(
      (l) => l.key === listenerOrEvent || l.event.toLowerCase() === listenerOrEvent.toLowerCase()
    );
    if (!entries.length) return { result: 'No active listener (already unsubscribed or never subscribed)' };
    const single = entries.length === 1 || entries.some((l) => l.key === listenerOrEvent);
    const eventName = entries[0].event;
    let reply: unknown = null;
    let error: unknown = null;
    for (const entry of entries) {
      try {
        const r = entry.unsubscribe
          ? await entry.unsubscribe()
          : await transportAdapter.unsubscribe(entry.event, entry.handler, 10000, single);
        if (r !== null && r !== undefined) reply = r;
      } catch (e) {
        logger.warn(`Unable to unsubscribe ${entry.event}`, e);
        error = normalizeError(e);
      }
      this.listeners.delete(entry.key);
    }
    return {
      eventName,
      params: { listen: false },
      listenersRemoved: entries.length,
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
      } catch (e) {
        logger.warn(`Unable to clear ${entry.event}`, e);
        errors.push(normalizeError(e));
      }
      this.listeners.delete(entry.key);
    }
    return errors.length ? { cleared: entries.length - errors.length, errors } : true;
  }

  async clearAll(): Promise<string> {
    const keys = [...this.listeners.keys()];
    for (const key of keys) await this.clear(key);
    return keys.length ? 'Cleared Listeners' : 'No active listeners';
  }
}
export const eventManager = new EventManager();
