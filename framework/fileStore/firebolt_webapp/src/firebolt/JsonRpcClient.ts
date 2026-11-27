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

// Firebolt Certification's own Firebolt JSON-RPC 2.0 client over WebSocket. It replaces the @firebolt-js/sdk Transport.
// - Connects to the configured endpoint as given, with the "jsonrpc" WebSocket sub-protocol.
// - A call without parameters omits "params"; otherwise "params" is an object (never an array).
// - Subscribe/unsubscribe: call the on* method with {"listen": true|false}; a successful reply is result: null.
// - Notifications are JSON-RPC messages without an id: {"method": "module.onSomething", "params": {...}}.
//   A primitive payload arrives as params.value; an object payload arrives as params itself.

import { runtimeConfig } from '../config/runtime';
import { logger } from '../utils/Logger';

export interface JsonRpcError {
  code: number | string;
  message: string;
  data?: unknown;
}
export type NotificationHandler = (value: unknown, raw: { method: string; params: unknown }) => void;

export interface SocketLike {
  readyState: number;
  send(data: string): void;
  close(): void;
  addEventListener(type: string, listener: (event: any) => void): void;
}
export type SocketFactory = (url: string, protocols: string[]) => SocketLike;

interface Pending {
  method: string;
  resolve: (v: unknown) => void;
  reject: (e: unknown) => void;
  timer: ReturnType<typeof setTimeout> | null;
}

const OPEN = 1;
const MAX_QUEUED = 200;
/** unsubscribe() result when {listen: false} was not sent because other handlers still use the subscription. */
export const UNSUBSCRIBE_NOT_SENT: unique symbol = Symbol('unsubscribe-not-sent');

/** "Accessibility.highContrastUI" → "accessibility.highContrastUI" (module lower-cased, as the Firebolt gateway expects). */
export function wireMethodName(qualified: string): string {
  const dot = qualified.indexOf('.');
  return dot < 0 ? qualified : `${qualified.slice(0, dot).toLowerCase()}${qualified.slice(dot)}`;
}

/** Turns notification params into the payload described by the event's OpenRPC result schema. */
export function notificationPayload(params: unknown): unknown {
  if (params && typeof params === 'object' && !Array.isArray(params)) {
    const keys = Object.keys(params as Record<string, unknown>);
    if (keys.length === 1 && keys[0] === 'value') return (params as Record<string, unknown>).value;
  }
  return params;
}

function isEmptyParams(params: unknown): boolean {
  return (
    params == null || (typeof params === 'object' && !Array.isArray(params) && !Object.keys(params as object).length)
  );
}

function defaultEndpoint(): string {
  const injected = typeof window !== 'undefined' ? (window as any).__firebolt?.endpoint : undefined;
  return injected || runtimeConfig.fireboltEndpoint || 'ws://127.0.0.1:3473';
}

function defaultSocketFactory(url: string, protocols: string[]): SocketLike {
  return new WebSocket(url, protocols) as unknown as SocketLike;
}

export class JsonRpcClient {
  private socket: SocketLike | null = null;
  private nextId = 1;
  private pending = new Map<number, Pending>();
  private queue: string[] = [];
  private handlers = new Map<string, Set<NotificationHandler>>();

  constructor(
    private readonly endpoint: () => string = defaultEndpoint,
    private readonly socketFactory: SocketFactory = defaultSocketFactory
  ) {}

  /** Sends a request; resolves with its result, rejects with the JSON-RPC error, a timeout or a closed connection. */
  call(method: string, params?: Record<string, unknown>, timeoutMs = 10000): Promise<unknown> {
    const id = this.nextId++;
    const wire = wireMethodName(method);
    const message: Record<string, unknown> = { jsonrpc: '2.0', id, method: wire };
    if (!isEmptyParams(params)) message.params = params;
    return new Promise((resolve, reject) => {
      const timer =
        timeoutMs > 0
          ? setTimeout(() => {
              this.pending.delete(id);
              this.queue = this.queue.filter((data) => JSON.parse(data).id !== id);
              reject({ code: 'TimeOutError', message: `Timed out in ${timeoutMs} ms.` });
            }, timeoutMs)
          : null;
      this.pending.set(id, { method: wire, resolve, reject, timer });
      this.send(JSON.stringify(message));
    });
  }

  /** Sends {listen: true} and resolves with the gateway's subscription reply (expected: null). */
  async subscribe(
    event: string,
    handler: NotificationHandler,
    params: Record<string, unknown> = {},
    timeoutMs = 10000
  ): Promise<unknown> {
    const key = wireMethodName(event).toLowerCase();
    let set = this.handlers.get(key);
    if (!set) {
      set = new Set();
      this.handlers.set(key, set);
    }
    set.add(handler);
    try {
      return await this.call(event, { ...params, listen: true }, timeoutMs);
    } catch (error) {
      set.delete(handler);
      if (!set.size) this.handlers.delete(key);
      throw error;
    }
  }

  /**
   * Removes a handler; when it was the last one for the event (or none is given), sends {listen: false}. `force` always sends it.
   * Returns UNSUBSCRIBE_NOT_SENT when only the local handler was removed because other handlers still need the subscription.
   * If the request fails, the removed handlers are restored so the caller can retry.
   */
  async unsubscribe(event: string, handler?: NotificationHandler, timeoutMs = 10000, force = false): Promise<unknown> {
    const key = wireMethodName(event).toLowerCase();
    const set = this.handlers.get(key);
    let removed: NotificationHandler[] = [];
    if (set && handler) {
      if (set.delete(handler)) removed = [handler];
      if (set.size && !force) return UNSUBSCRIBE_NOT_SENT;
    }
    if (set && !handler) removed = [...set];
    if (set && (!handler || !set.size)) this.handlers.delete(key);
    try {
      return await this.call(event, { listen: false }, timeoutMs);
    } catch (error) {
      this.restoreHandlers(key, removed);
      throw error;
    }
  }

  private restoreHandlers(key: string, handlers: NotificationHandler[]): void {
    if (!handlers.length) return;
    // A subscribe may have created a new set for this event while the request was in flight.
    let set = this.handlers.get(key);
    if (!set) {
      set = new Set();
      this.handlers.set(key, set);
    }
    for (const h of handlers) set.add(h);
  }

  private send(data: string): void {
    const socket = this.connect();
    if (socket.readyState === OPEN) socket.send(data);
    else if (this.queue.length < MAX_QUEUED) this.queue.push(data);
    else logger.warn('Firebolt request dropped: send queue is full');
  }

  private connect(): SocketLike {
    if (this.socket) return this.socket;
    const url = this.endpoint();
    const socket = this.socketFactory(url, ['jsonrpc']);
    this.socket = socket;
    socket.addEventListener('open', () => {
      const queued = this.queue;
      this.queue = [];
      for (const message of queued) socket.send(message);
    });
    socket.addEventListener('message', (event: any) => this.receive(String(event?.data ?? '')));
    socket.addEventListener('close', () => {
      if (this.socket !== socket) return;
      this.socket = null;
      this.queue = [];
      this.failPending('Firebolt connection closed');
    });
    socket.addEventListener('error', () => logger.warn(`Firebolt WebSocket error (${url})`));
    return socket;
  }

  private failPending(reason: string): void {
    for (const [id, p] of this.pending) {
      if (p.timer) clearTimeout(p.timer);
      p.reject({ code: 'ConnectionError', message: `${reason} before ${p.method} replied.` });
      this.pending.delete(id);
    }
  }

  private receive(text: string): void {
    let message: any;
    try {
      message = JSON.parse(text);
    } catch {
      logger.warn('Ignoring non-JSON message from the Firebolt gateway', text);
      return;
    }
    for (const m of Array.isArray(message) ? message : [message]) this.dispatch(m);
  }

  private dispatch(message: any): void {
    if (!message || typeof message !== 'object') return;
    const hasId = message.id !== undefined && message.id !== null;
    if (hasId && ('result' in message || 'error' in message)) {
      const p = this.pending.get(Number(message.id));
      if (!p) return;
      this.pending.delete(Number(message.id));
      if (p.timer) clearTimeout(p.timer);
      if (message.error) p.reject(message.error as JsonRpcError);
      else p.resolve(message.result);
      return;
    }
    if (!hasId && typeof message.method === 'string') {
      const set = this.handlers.get(message.method.toLowerCase());
      if (!set?.size) return;
      const value = notificationPayload(message.params);
      for (const handler of [...set]) {
        try {
          handler(value, { method: message.method, params: message.params });
        } catch (error) {
          logger.warn(`Notification handler for ${message.method} failed`, error);
        }
      }
    }
  }
}

export const jsonRpcClient = new JsonRpcClient();
