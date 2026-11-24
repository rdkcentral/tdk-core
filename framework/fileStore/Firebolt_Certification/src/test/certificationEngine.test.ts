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
 * @file Tests for CertificationEngine: module scoping, SDK/Transport mode handling and event subscribe/unsubscribe results.
 */

import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { OpenRpcMethod } from '../types';

const m = (name: string, extra: Partial<OpenRpcMethod> = {}): OpenRpcMethod => {
  const [module, method] = name.split('.');
  return { name, module, method, params: [], examples: [], raw: { name }, ...extra };
};
const catalog: OpenRpcMethod[] = [
  m('Device.version'),
  m('Device.onNameChanged'),
  m('Device.name'),
  m('Account.id'),
  m('HDMIInput.ports')
];

vi.mock('../config/runtime', () => ({
  runtimeConfig: { logLevel: 'ERROR' }
}));
vi.mock('../schema/OpenRpcService', () => ({
  openRpcService: { getMethods: () => [...catalog], getMethod: () => undefined, specVersion: () => '9.0.0' }
}));
const invoke = vi.fn(async ({ method, mode }: any) => ({
  id: method,
  method,
  mode,
  status: 'PASS',
  durationMs: 1,
  timestamp: Date.now(),
  response: 'ok'
}));
vi.mock('../firebolt/FireboltAdapter', () => ({ fireboltAdapter: { invoke: (o: any) => invoke(o) } }));
const register = vi.fn(async () => ({
  eventListenerId: 'L1',
  eventListenerResponse: { subscriptionReply: null, error: null }
}));
const getResponse = vi.fn((): any[] => []);
const clear = vi.fn(async (_key: string) => true);
const unsubscribe = vi.fn(async (_key: string): Promise<any> => ({
  eventName: 'Device.onNameChanged',
  params: { listen: false },
  listenersRemoved: 1,
  unsubscribeReply: null,
  error: null
}));
vi.mock('../firebolt/EventManager', () => ({
  eventManager: {
    register: (...a: any[]) => (register as any)(...a),
    getResponse: () => getResponse(),
    clear: (k: string) => clear(k),
    unsubscribe: (k: string) => unsubscribe(k)
  }
}));
vi.spyOn(console, 'error').mockImplementation(() => undefined);

const { certificationEngine } = await import('../core/CertificationEngine');

describe('runSuite module scope', () => {
  beforeEach(() => {
    invoke.mockClear();
    register.mockClear();
    clear.mockClear();
    unsubscribe.mockClear();
    getResponse.mockReturnValue([]);
  });

  it('marks a stopped run as interrupted, even when every executed case passed', async () => {
    invoke.mockImplementationOnce(async ({ method, mode }: any) => {
      certificationEngine.stopSuite();
      return { id: method, method, mode, status: 'PASS', durationMs: 1, timestamp: Date.now(), response: 'ok' };
    });
    const report = await certificationEngine.runSuite({ modules: ['Device'], mode: 'Transport' });
    expect(report.results.map((r) => `${r.method}:${r.status}`)).toEqual(['Device.version:PASS']);
    expect(report.summary.failed).toBe(0);
    expect(report.interrupted).toBe(true);
    expect(report.methodsNotRun).toBe(2);
  });

  it('does not mark a run that tested every method as interrupted', async () => {
    const report = await certificationEngine.runSuite({ modules: ['Device'], mode: 'Transport' });
    expect(report.interrupted).toBeUndefined();
  });

  it("runs only the selected module of Firebolt Certification's OpenRPC", async () => {
    const report = await certificationEngine.runSuite({
      modules: ['Device'],
      scopeLabel: 'Device',
      mode: 'SDK'
    });
    expect(report.results.map((r) => `${r.method}:${r.status}`)).toEqual([
      'Device.version:PASS',
      'Device.onNameChanged:PASS',
      'Device.onNameChanged:PASS',
      'Device.name:PASS'
    ]);
    expect(invoke.mock.calls.map(([o]) => o.method)).toEqual(['Device.version', 'Device.name']);
    expect(report.title).toBe('Firebolt SDK Validation - Device');
  });

  it('passes the selected mode through and matches modules case-insensitively', async () => {
    const report = await certificationEngine.runSuite({ modules: ['hdmiinput'], mode: 'Transport' });
    expect(invoke.mock.calls.map(([o]) => `${o.method}:${o.mode}`)).toEqual(['HDMIInput.ports:Transport']);
    expect(report.title).toBe('Firebolt Transport Validation - hdmiinput');
  });

  it('still calls a method without examples when a required param has no schema value', async () => {
    const method = catalog[3];
    method.params = [
      { name: 'id', required: true, schema: { type: 'string' } },
      { name: 'lang', required: true, schema: { type: 'string', default: 'en' } }
    ];
    try {
      const report = await certificationEngine.runSuite({ modules: ['Account'], mode: 'Transport' });
      expect(invoke.mock.calls.map(([o]) => o.params)).toEqual([{ lang: 'en' }]);
      expect(report.results.map((r) => `${r.method}:${r.status}`)).toEqual(['Account.id:PASS']);
    } finally {
      method.params = [];
    }
  });

  it('fails a missing device SDK wrapper instead of skipping an rpc-only API', async () => {
    const method = catalog[0];
    invoke.mockResolvedValueOnce({
      id: method.name,
      method: method.name,
      mode: 'SDK',
      status: 'FAIL',
      durationMs: 1,
      timestamp: Date.now(),
      error: { code: 'SdkMethodNotAvailable', message: 'Device wrapper missing' }
    } as any);
    const report = await certificationEngine.runSuite({ modules: ['Device'], mode: 'SDK' });
    expect(report.results[0]).toMatchObject({
      method: 'Device.version',
      status: 'FAIL',
      error: { code: 'SdkMethodNotAvailable' }
    });
    expect(invoke.mock.calls[0][0].method).toBe('Device.version');
  });

  it('does not count a missing SDK wrapper as a passing expected API error', async () => {
    invoke.mockResolvedValueOnce({
      id: 'Device.version',
      method: 'Device.version',
      mode: 'SDK',
      status: 'FAIL',
      durationMs: 1,
      timestamp: Date.now(),
      error: { code: 'SdkMethodNotAvailable', message: 'Device wrapper missing' }
    } as any);
    const report = await certificationEngine.runSuite({
      modules: ['Device'],
      mode: 'SDK',
      exceptionMethods: [{ method: 'Device.version' }]
    });
    expect(report.results[0].status).toBe('FAIL');
  });

  it('runs every method when no module scope is given', async () => {
    const run = await certificationEngine.runSuite({ mode: 'SDK' });
    // the one event method in the catalog yields two rows (subscribe + unsubscribe)
    expect(run.results).toHaveLength(catalog.length + 1);
    expect(run.title).toBe('Firebolt SDK Validation - All modules');
  });

  it('labels a UI "All modules" run without changing what is executed', async () => {
    const all = await certificationEngine.runSuite({ scopeLabel: 'All modules', mode: 'SDK' });
    expect(all.title).toBe('Firebolt SDK Validation - All modules');
    expect(all.results).toHaveLength(catalog.length + 1);
  });

  describe('event methods', () => {
    const run = () => certificationEngine.runSuite({ modules: ['Device'], mode: 'SDK' });
    const rows = (r: any) => r.results.filter((x: any) => x.method === 'Device.onNameChanged');
    const subscribeRow = (r: any) => rows(r).find((x: any) => x.eventAction === 'subscribe');
    const unsubscribeRow = (r: any) => rows(r).find((x: any) => x.eventAction === 'unsubscribe');

    it('reports subscribe and unsubscribe as two separate rows', async () => {
      const report = await run();
      expect(rows(report).map((x: any) => `${x.eventAction}:${x.status}`)).toEqual([
        'subscribe:PASS',
        'unsubscribe:PASS'
      ]);
      expect(subscribeRow(report).params).toEqual({});
      expect(unsubscribeRow(report).params).toEqual({ listen: false });
      expect(subscribeRow(report).expectedFormat).toBe('null');
      expect(unsubscribeRow(report).response).toBeNull();
      expect(register).toHaveBeenCalledWith('Device.onNameChanged', {}, 'SDK');
      expect(unsubscribe).toHaveBeenCalledWith('L1');
    });

    it('labels injected SDK listener acknowledgements without claiming a raw gateway reply', async () => {
      register.mockResolvedValueOnce({
        eventListenerId: 'L1',
        eventListenerResponse: { subscriptionReply: { subscriptionAccepted: true }, sdkManaged: true, error: null }
      } as any);
      unsubscribe.mockResolvedValueOnce({ unsubscribeReply: { unsubscribed: true }, sdkManaged: true, error: null });
      const report = await run();
      expect(rows(report).map((row: any) => row.status)).toEqual(['PASS', 'PASS']);
      expect(subscribeRow(report).expectedFormat).toContain('not a raw gateway reply');
      expect(unsubscribeRow(report).response).toEqual({ unsubscribed: true });
    });

    it('fails only the unsubscribe row when the unsubscribe reply is not null', async () => {
      unsubscribe.mockResolvedValueOnce({ unsubscribeReply: { listening: false }, error: null });
      const report = await run();
      expect(subscribeRow(report).status).toBe('PASS');
      const result = unsubscribeRow(report);
      expect(result.status).toBe('FAIL');
      expect(result.schemaValidation.errors).toEqual([
        'unsubscribe reply: expected null, received {"listening":false}'
      ]);
      expect(result.failureReason[0]).toBe('Expected null, received {"listening":false}.');
    });

    it('fails the unsubscribe row when the unsubscribe request errors', async () => {
      unsubscribe.mockResolvedValueOnce({ unsubscribeReply: null, error: { code: -32000, message: 'boom' } });
      const result = unsubscribeRow(await run());
      expect(result.status).toBe('FAIL');
      expect(result.schemaValidation.errors).toEqual(['unsubscribe reply: request failed (boom)']);
    });

    it.each([
      ['the unsubscribe reply has no result', { unsubscribeReply: undefined, error: null }],
      ['the listener was already cleared and no request was sent', { result: 'No active listener' }]
    ])('fails the unsubscribe row when %s', async (_, reply) => {
      unsubscribe.mockResolvedValueOnce(reply);
      const result = unsubscribeRow(await run());
      expect(result.status).toBe('FAIL');
      expect(result.schemaValidation.errors).toEqual(['unsubscribe reply: expected null, received no result']);
    });

    it('ignores received notifications: only the subscribe and unsubscribe replies decide the results', async () => {
      getResponse.mockReturnValue([{ value: 5, schemaValidation: { valid: false, errors: ['/ must be string'] } }]);
      const report = await run();
      expect(subscribeRow(report).status).toBe('PASS');
      expect(unsubscribeRow(report).status).toBe('PASS');
      expect(subscribeRow(report).response).toBeNull();
    });

    it('fails when the subscription itself is rejected, with no unsubscribe row', async () => {
      register.mockResolvedValueOnce({
        eventListenerId: null,
        eventListenerResponse: { error: { code: -32601, message: 'Method not known' } }
      } as any);
      const report = await run();
      expect(rows(report)).toHaveLength(1);
      expect(subscribeRow(report).status).toBe('FAIL');
      expect(unsubscribe).not.toHaveBeenCalled();
    });

    it('fails the subscribe row when the reply is the Firebolt 1.x {listening, event} instead of null', async () => {
      const legacy = { listening: true, event: 'device.onNameChanged' };
      register.mockResolvedValueOnce({
        eventListenerId: 'L1',
        eventListenerResponse: { subscriptionReply: legacy, error: null }
      } as any);
      const report = await run();
      const result = subscribeRow(report);
      expect(result.status).toBe('FAIL');
      expect(result.response).toEqual(legacy);
      expect(result.schemaValidation.errors).toEqual([
        `subscription reply: expected null, received ${JSON.stringify(legacy)}`
      ]);
      expect(result.failureReason[0]).toBe(`Expected null, received ${JSON.stringify(legacy)}.`);
      expect(unsubscribeRow(report).status).toBe('PASS');
    });
  });
});

describe('direct invoke of an event method (APIs / FCS callMethod)', () => {
  it('validates the reply as a subscription reply (null), not against the notification schema', async () => {
    const { validateSubscriptionReply } = await import('../core/CertificationEngine');
    expect(validateSubscriptionReply(null)).toEqual({ valid: true, errors: [] });
    expect(validateSubscriptionReply({ listening: true, event: 'accessibility.onHighContrastUIChanged' }).valid).toBe(
      false
    );
    expect(validateSubscriptionReply(undefined).errors[0]).toBe(
      'subscription reply: expected null, received no result'
    );
  });
});
