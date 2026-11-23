import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { OpenRpcMethod } from '../types';

vi.stubGlobal('window', { location: { search: '' }, setTimeout, clearTimeout });
vi.mock('../config/runtime', () => ({ runtimeConfig: { logLevel: 'ERROR', communicationMode: 'Transport' } }));
const catalog = [
  { name: 'Actions.start', params: [{ name: 'intent' }, { name: 'handlerAppId' }] },
  { name: 'Metrics.appInfo', params: [{ name: 'build' }] }
];
vi.mock('../schema/OpenRpcService', () => ({
  openRpcService: {
    getMethod: (name: string) => catalog.find((m) => m.name === name) as OpenRpcMethod | undefined,
    getMethods: () => []
  }
}));
const transportInvoke = vi.fn(async (..._args: unknown[]) => 'Transport response');
const transportSubscribe = vi.fn(async (..._args: unknown[]) => null);
const transportUnsubscribe = vi.fn(async (..._args: unknown[]) => null);
vi.mock('../firebolt/TransportAdapter', () => ({
  transportAdapter: {
    invoke: (...args: unknown[]) => transportInvoke(...args),
    subscribe: (...args: unknown[]) => transportSubscribe(...args),
    unsubscribe: (...args: unknown[]) => transportUnsubscribe(...args)
  }
}));
const extensionInvoke = vi.fn(async () => 'Extension response');
vi.mock('../extensions/ExtensionRegistry', () => ({
  extensionRegistry: { findInvoker: (name: string) => (name === 'External.test' ? extensionInvoke : undefined) }
}));
const socket = vi.fn();
vi.stubGlobal('WebSocket', socket);
const name = vi.fn(async () => 'Device SDK response');
const start = vi.fn(async (..._args: unknown[]) => null);
const appInfo = vi.fn(async (..._args: unknown[]) => null);
const stop = vi.fn(async () => undefined);
const listen = vi.fn(async (_callback: (value: unknown) => void): Promise<unknown> => stop);
const client = { Device: { name, onNameChanged: listen }, Actions: { start }, Metrics: { appInfo } };
const get = vi.fn(async () => client);
const { fireboltAdapter } = await import('../firebolt/FireboltAdapter');
const { eventManager } = await import('../firebolt/EventManager');
const { SdkAdapter } = await import('../firebolt/SdkAdapter');
const { runner } = await import('../../.firebolt-sdk/runner.js');
const run = vi.spyOn(runner, 'run');

describe('SDK mode requires the device FireboltServiceManager client', () => {
  beforeEach(async () => {
    await eventManager.clearAll();
    vi.clearAllMocks();
    Object.assign(window, { FireboltServiceManager: { get } });
    name.mockResolvedValue('Device SDK response');
    stop.mockResolvedValue(undefined);
    listen.mockResolvedValue(stop);
    get.mockResolvedValue(client);
  });

  it('fails when the manager is absent, without opening a socket or falling back', async () => {
    Reflect.deleteProperty(window, 'FireboltServiceManager');
    const result = await fireboltAdapter.invoke({ method: 'Device.name', mode: 'SDK', timeoutMs: 15 });
    expect(result).toMatchObject({ status: 'FAIL', error: { code: 'SdkManagerNotAvailable' } });
    expect(get).not.toHaveBeenCalled();
    expect(socket).not.toHaveBeenCalled();
    expect(transportInvoke).not.toHaveBeenCalled();
  });

  it('waits for late device injection and calls get with its receiver', async () => {
    Reflect.deleteProperty(window, 'FireboltServiceManager');
    const manager = { get };
    const pending = new SdkAdapter().invoke('Device.name', {}, 300);
    const timer = setTimeout(() => Object.assign(window, { FireboltServiceManager: manager }), 5);
    try {
      expect(await pending).toBe('Device SDK response');
      expect(get.mock.contexts[0]).toBe(manager);
    } finally {
      clearTimeout(timer);
    }
  });

  it('routes SDK calls through the unchanged upstream runner', async () => {
    const result = await fireboltAdapter.invoke({ method: 'device.name', mode: 'SDK' });
    expect(result).toMatchObject({ status: 'PASS', response: 'Device SDK response', method: 'Device.name' });
    expect(name).toHaveBeenCalledWith();
    expect(run).toHaveBeenCalledOnce();
    expect(run.mock.calls[0][0][0]).toMatchObject({ module: 'Device', method: 'name', args: [] });
    expect(transportInvoke).not.toHaveBeenCalled();
    expect(socket).not.toHaveBeenCalled();
  });

  it('preserves Transport mode and the default mode', async () => {
    const explicit = await fireboltAdapter.invoke({ method: 'Device.name', mode: 'Transport' });
    const implicit = await fireboltAdapter.invoke({ method: 'Device.name' });
    expect([explicit.response, implicit.response, implicit.mode]).toEqual([
      'Transport response',
      'Transport response',
      'Transport'
    ]);
    expect(transportInvoke).toHaveBeenCalledTimes(2);
    expect(run).not.toHaveBeenCalled();
  });

  it('maps positional OpenRPC values to the injected SDK object argument', async () => {
    await fireboltAdapter.invoke({ method: 'Actions.start', params: [{ action: 'home' }, 'app-1'], mode: 'SDK' });
    expect(start).toHaveBeenCalledWith({ intent: { action: 'home' }, handlerAppId: 'app-1' });
  });

  it('uses upstream argument metadata for primitive wrappers without generating any client', async () => {
    await fireboltAdapter.invoke({ method: 'Metrics.appInfo', params: { build: '1.2.3' }, mode: 'SDK' });
    expect(appInfo).toHaveBeenCalledWith('1.2.3');
  });

  it('fails APIs absent from the device client, including extension invokers', async () => {
    for (const method of ['Device.version', 'External.test']) {
      const result = await fireboltAdapter.invoke({ method, mode: 'SDK' });
      expect(result).toMatchObject({
        status: 'FAIL',
        error: { code: 'SdkMethodNotAvailable', message: expect.stringContaining('No fallback') }
      });
    }
    expect(transportInvoke).not.toHaveBeenCalled();
    expect(extensionInvoke).not.toHaveBeenCalled();
    expect(socket).not.toHaveBeenCalled();
  });

  it('allows device methods not present in the pinned upstream argument catalog', async () => {
    const ping = vi.fn(async (..._args: unknown[]) => 'new API');
    Object.assign(window, { FireboltServiceManager: { get: () => ({ Custom: { ping } }) } });
    expect(await new SdkAdapter().invoke('Custom.ping', { value: 1 })).toBe('new API');
    expect(ping).toHaveBeenCalledWith({ value: 1 });
  });

  it('surfaces get failures and invalid device clients without fallback', async () => {
    for (const manager of [
      {
        get: () => {
          throw { code: 'DeviceSdkError', message: 'get failed' };
        }
      },
      { get: () => null },
      {}
    ]) {
      Object.assign(window, { FireboltServiceManager: manager });
      await expect(new SdkAdapter().invoke('Device.name', {})).rejects.toBeTruthy();
    }
    expect(socket).not.toHaveBeenCalled();
    expect(transportInvoke).not.toHaveBeenCalled();
  });

  it('surfaces rejected device SDK calls', async () => {
    name.mockRejectedValueOnce({ code: -32602, message: 'Invalid argument' });
    const result = await fireboltAdapter.invoke({ method: 'Device.name', mode: 'SDK' });
    expect(result).toMatchObject({ status: 'FAIL', error: { code: -32602, message: 'Invalid argument' } });
  });

  it('retains SDK listeners, records notifications, and releases device unsubscribe handles', async () => {
    const registered = await eventManager.register('Device.onNameChanged', { listen: true }, 'SDK');
    expect(registered.eventListenerResponse).toMatchObject({
      subscriptionReply: { subscriptionAccepted: true },
      sdkManaged: true,
      error: null
    });
    expect(stop).not.toHaveBeenCalled();
    listen.mock.calls[0][0]('Den');
    expect(eventManager.getResponse(registered.eventListenerId)[0].value).toBe('Den');
    const cleared = await eventManager.unsubscribe(registered.eventListenerId);
    expect(cleared).toMatchObject({ unsubscribeReply: { unsubscribed: true }, error: null, listenersRemoved: 1 });
    expect(stop).toHaveBeenCalledOnce();
    expect(transportSubscribe).not.toHaveBeenCalled();
    expect(transportUnsubscribe).not.toHaveBeenCalled();
  });

  it('fails event registration when the device lacks its wrapper', async () => {
    const registered = await eventManager.register('Device.onMissingChanged', {}, 'SDK');
    expect(registered.eventListenerId).toBeNull();
    expect(registered.eventListenerResponse.error).toMatchObject({ code: 'SdkMethodNotAvailable' });
    expect(transportSubscribe).not.toHaveBeenCalled();
  });

  it('reports SDK unsubscribe errors rather than pretending it succeeded', async () => {
    const registered = await eventManager.register('Device.onNameChanged', {}, 'SDK');
    stop.mockRejectedValueOnce({ code: -32000, message: 'Unable to stop listening' });
    const result = await eventManager.unsubscribe(registered.eventListenerId);
    expect(result.error).toMatchObject({ code: -32000, message: 'Unable to stop listening' });
  });

  it('clears SDK handles without Transport and rejects unsupported event arguments', async () => {
    const registered = await eventManager.register('Device.onNameChanged', {}, 'SDK');
    expect(await eventManager.clear(registered.eventListenerId)).toBe(true);
    expect(stop).toHaveBeenCalledOnce();
    const invalid = await eventManager.register('Device.onNameChanged', { context: 'app-1' }, 'SDK');
    expect(invalid.eventListenerResponse.error).toMatchObject({ code: 'SdkInvalidParams' });
    expect(transportUnsubscribe).not.toHaveBeenCalled();
  });

  it('fails if the device event wrapper does not return an unsubscribe function', async () => {
    listen.mockResolvedValueOnce(null);
    const result = await eventManager.register('Device.onNameChanged', {}, 'SDK');
    expect(result.eventListenerId).toBeNull();
    expect(result.eventListenerResponse.error.message).toContain('unsubscribe function');
  });

  it('runs direct SDK event calls as a subscribe/unsubscribe smoke check', async () => {
    const result = await fireboltAdapter.invoke({
      method: 'Device.onNameChanged',
      params: { listen: true },
      mode: 'SDK'
    });
    expect(result).toMatchObject({ status: 'PASS', response: { subscriptionAccepted: true, unsubscribed: true } });
    expect(listen).toHaveBeenCalledOnce();
    expect(stop).toHaveBeenCalledOnce();
  });

  it('rejects direct listen:false calls instead of subscribing', async () => {
    const result = await fireboltAdapter.invoke({
      method: 'Device.onNameChanged',
      params: { listen: false },
      mode: 'SDK'
    });
    expect(result).toMatchObject({ status: 'FAIL', error: { code: 'SdkInvalidParams' } });
    expect(listen).not.toHaveBeenCalled();
  });

  it('times out device get() without invoking an API or opening a socket', async () => {
    Object.assign(window, { FireboltServiceManager: { get: () => new Promise(() => {}) } });
    await expect(new SdkAdapter().invoke('Device.name', {}, 10)).rejects.toMatchObject({ code: 'TimeOutError' });
    expect(name).not.toHaveBeenCalled();
    expect(socket).not.toHaveBeenCalled();
  });

  it('releases a device subscription that resolves after the invocation timeout', async () => {
    let resolveListener: ((value: () => void) => void) | undefined;
    const onNameChanged = () =>
      new Promise<() => void>((resolve) => {
        resolveListener = resolve;
      });
    Object.assign(window, { FireboltServiceManager: { get: () => ({ Device: { onNameChanged } }) } });
    await expect(new SdkAdapter().subscribe('Device.onNameChanged', {}, () => {}, 10)).rejects.toMatchObject({
      code: 'TimeOutError'
    });
    resolveListener?.(stop);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(stop).toHaveBeenCalledOnce();
  });
});
