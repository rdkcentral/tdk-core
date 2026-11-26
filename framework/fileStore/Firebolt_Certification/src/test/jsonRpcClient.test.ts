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
 * @file Tests for JsonRpcClient: connection, params, errors, timeouts, reconnects and event subscriptions.
 */

import { describe, expect, it, vi } from 'vitest';
vi.mock('../config/runtime', () => ({ runtimeConfig: { logLevel: 'ERROR', fireboltEndpoint: 'ws://127.0.0.1:3473' } }));
import {
  JsonRpcClient,
  UNSUBSCRIBE_NOT_SENT,
  notificationPayload,
  wireMethodName
} from '../firebolt/JsonRpcClient';

function fakeSocket() {
  const listeners: Record<string, Array<(e: any) => void>> = {};
  const sock = {
    readyState: 0,
    sent: [] as any[],
    url: '',
    protocols: [] as string[],
    send(d: string) {
      sock.sent.push(JSON.parse(d));
    },
    close() {
      listeners.close?.forEach((l) => l({}));
    },
    addEventListener(t: string, l: (e: any) => void) {
      (listeners[t] ||= []).push(l);
    },
    open() {
      sock.readyState = 1;
      listeners.open?.forEach((l) => l({}));
    },
    reply(m: unknown) {
      listeners.message?.forEach((l) => l({ data: JSON.stringify(m) }));
    },
    drop() {
      sock.readyState = 3;
      listeners.close?.forEach((l) => l({}));
    }
  };
  return sock;
}
function client() {
  const sock = fakeSocket();
  let connects = 0;
  const c = new JsonRpcClient(
    () => 'ws://127.0.0.1:3473',
    (url, protocols) => {
      connects++;
      sock.url = url;
      sock.protocols = protocols;
      return sock;
    }
  );
  return { c, sock, connects: () => connects };
}

describe('JsonRpcClient (Firebolt JSON-RPC)', () => {
  it('connects once to the endpoint as given with the jsonrpc sub-protocol, queues until open, and omits empty params', async () => {
    const { c, sock, connects } = client();
    const p = c.call('Device.name', {});
    const q = c.call('Device.id');
    expect(sock.url).toBe('ws://127.0.0.1:3473');
    expect(sock.protocols).toEqual(['jsonrpc']);
    expect(sock.sent).toEqual([]);
    sock.open();
    expect(connects()).toBe(1);
    expect(sock.sent).toEqual([
      { jsonrpc: '2.0', id: 1, method: 'device.name' },
      { jsonrpc: '2.0', id: 2, method: 'device.id' }
    ]);
    sock.reply({ jsonrpc: '2.0', id: 2, result: 'abc' });
    sock.reply({ jsonrpc: '2.0', id: 1, result: 'Living Room' });
    await expect(p).resolves.toBe('Living Room');
    await expect(q).resolves.toBe('abc');
  });

  it('sends params as an object, rejects with the JSON-RPC error, and times out', async () => {
    const { c, sock } = client();
    sock.open();
    const p = c.call('Network.interfaceStatus', { interfaceName: 'wlan0' });
    expect(sock.sent[0]).toEqual({
      jsonrpc: '2.0',
      id: 1,
      method: 'network.interfaceStatus',
      params: { interfaceName: 'wlan0' }
    });
    sock.reply({ jsonrpc: '2.0', id: 1, error: { code: -32601, message: 'Method not found' } });
    await expect(p).rejects.toEqual({ code: -32601, message: 'Method not found' });
    vi.useFakeTimers();
    const t = c.call('Device.slow', {}, 50);
    vi.advanceTimersByTime(60);
    await expect(t).rejects.toMatchObject({ code: 'TimeOutError' });
    vi.useRealTimers();
  });

  it('fails in-flight calls when the connection closes, and reconnects on the next call', async () => {
    const { c, sock, connects } = client();
    sock.open();
    const p = c.call('Device.name');
    sock.drop();
    await expect(p).rejects.toMatchObject({ code: 'ConnectionError' });
    void c.call('Device.name').catch(() => undefined);
    expect(connects()).toBe(2);
  });

  it('subscribes with {listen: true}, returns the reply (null), delivers id-less notifications and unsubscribes', async () => {
    const { c, sock } = client();
    sock.open();
    const got: unknown[] = [];
    const sub = c.subscribe('Accessibility.onHighContrastUIChanged', (v) => got.push(v));
    expect(sock.sent[0]).toEqual({
      jsonrpc: '2.0',
      id: 1,
      method: 'accessibility.onHighContrastUIChanged',
      params: { listen: true }
    });
    sock.reply({ jsonrpc: '2.0', id: 1, result: null });
    await expect(sub).resolves.toBeNull();
    sock.reply({ jsonrpc: '2.0', method: 'accessibility.onHighContrastUIChanged', params: { value: true } });
    sock.reply({ jsonrpc: '2.0', method: 'Accessibility.onHighContrastUIChanged', params: { value: false } });
    sock.reply({
      jsonrpc: '2.0',
      method: 'accessibility.onVoiceGuidanceSettingsChanged',
      params: { enabled: true, rate: 1 }
    });
    expect(got).toEqual([true, false]);
    const un = c.unsubscribe('Accessibility.onHighContrastUIChanged');
    expect(sock.sent[1]).toEqual({
      jsonrpc: '2.0',
      id: 2,
      method: 'accessibility.onHighContrastUIChanged',
      params: { listen: false }
    });
    sock.reply({ jsonrpc: '2.0', id: 2, result: null });
    await un;
    sock.reply({ jsonrpc: '2.0', method: 'accessibility.onHighContrastUIChanged', params: { value: true } });
    expect(got).toEqual([true, false]);
  });

  it('returns a non-null (Firebolt 1.x) subscription reply as-is so Firebolt Certification can fail it', async () => {
    const { c, sock } = client();
    sock.open();
    const sub = c.subscribe('Accessibility.onHighContrastUIChanged', () => undefined);
    sock.reply({ jsonrpc: '2.0', id: 1, result: { listening: true, event: 'accessibility.onHighContrastUIChanged' } });
    await expect(sub).resolves.toEqual({ listening: true, event: 'accessibility.onHighContrastUIChanged' });
  });

  it('keeps the gateway subscription while another handler for the same event is still registered', async () => {
    const { c, sock } = client();
    sock.open();
    const a = vi.fn();
    const b = vi.fn();
    const s1 = c.subscribe('Device.onNameChanged', a);
    sock.reply({ jsonrpc: '2.0', id: 1, result: null });
    await s1;
    const s2 = c.subscribe('Device.onNameChanged', b);
    sock.reply({ jsonrpc: '2.0', id: 2, result: null });
    await s2;
    await expect(c.unsubscribe('Device.onNameChanged', a)).resolves.toBe(UNSUBSCRIBE_NOT_SENT);
    expect(sock.sent).toHaveLength(2);
    sock.reply({ jsonrpc: '2.0', method: 'device.onNameChanged', params: { value: 'Kitchen' } });
    expect(a).not.toHaveBeenCalled();
    expect(b).toHaveBeenCalledWith('Kitchen', expect.anything());
  });

  it('keeps the handler registered when the unsubscribe request fails, so it can be retried', async () => {
    const { c, sock } = client();
    sock.open();
    const a = vi.fn();
    const s = c.subscribe('Device.onNameChanged', a);
    sock.reply({ jsonrpc: '2.0', id: 1, result: null });
    await s;
    const un = c.unsubscribe('Device.onNameChanged', a);
    sock.reply({ jsonrpc: '2.0', id: 2, error: { code: -32603, message: 'boom' } });
    await expect(un).rejects.toMatchObject({ message: 'boom' });
    sock.reply({ jsonrpc: '2.0', method: 'device.onNameChanged', params: { value: 'Kitchen' } });
    expect(a).toHaveBeenCalledTimes(1);
    const retry = c.unsubscribe('Device.onNameChanged', a);
    expect(sock.sent[2]).toMatchObject({ method: 'device.onNameChanged', params: { listen: false } });
    sock.reply({ jsonrpc: '2.0', id: 3, result: null });
    await expect(retry).resolves.toBeNull();
  });

  it('helpers', () => {
    expect(wireMethodName('Accessibility.highContrastUI')).toBe('accessibility.highContrastUI');
    expect(notificationPayload({ value: 42 })).toBe(42);
    expect(notificationPayload({ enabled: true, rate: 1 })).toEqual({ enabled: true, rate: 1 });
    expect(notificationPayload(['a'])).toEqual(['a']);
  });
});
