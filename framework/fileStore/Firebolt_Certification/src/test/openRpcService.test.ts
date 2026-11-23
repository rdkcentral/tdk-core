import { beforeEach, describe, expect, it, vi } from 'vitest';

const location = { search: '' };
vi.stubGlobal('window', { location });
vi.stubGlobal('document', { baseURI: 'http://vm:5173/' });
const runtimeConfig: { logLevel: string; specVersion: string } = { logLevel: 'ERROR', specVersion: '' };
vi.mock('../config/runtime', () => ({
  runtimeConfig,
  getConfiguredExclusions: () => [],
  buildExclusionMatcher: () => () => false
}));
const fetchMock = vi.fn();
vi.stubGlobal('fetch', fetchMock);

const { openRpcService, DEFAULT_SPEC_PATH, LATEST_SPEC_VERSION } = await import('../schema/OpenRpcService');
const hosted = {
  methods: [{ name: 'Device.name', params: [], result: { name: 'value', schema: { type: 'string' } } }]
};
const ok = (json: unknown) => ({ ok: true, status: 200, json: async () => json });

describe("OpenRpcService loads only Firebolt Certification's own OpenRPC", () => {
  beforeEach(() => {
    fetchMock.mockReset();
    location.search = '';
    runtimeConfig.specVersion = '';
  });

  it('reads the hosted spec next to the app by default (no URL parameter needed), bypassing the cache', async () => {
    fetchMock.mockResolvedValueOnce(ok(hosted));
    const methods = await openRpcService.load();
    expect(fetchMock).toHaveBeenCalledWith(`http://vm:5173/${DEFAULT_SPEC_PATH}`, { cache: 'no-store' });
    expect(methods.map((m) => m.name)).toEqual(['Device.name']);
    expect(openRpcService.sourceUrl()).toBe(`http://vm:5173/${DEFAULT_SPEC_PATH}`);
  });

  it('fetches the file for the requested specVersion and does not fall back to the bundle for other versions', async () => {
    runtimeConfig.specVersion = '8.0.0';
    fetchMock.mockResolvedValueOnce(ok({ ...hosted, info: { version: '8.0.0' } }));
    await openRpcService.load();
    expect(fetchMock).toHaveBeenCalledWith('http://vm:5173/specs/firebolt_schema_validator-8.0.0.json', {
      cache: 'no-store'
    });
    expect(openRpcService.specVersion()).toBe('8.0.0');
    fetchMock.mockRejectedValueOnce(new Error('404'));
    await expect(openRpcService.load()).rejects.toThrow();
  });

  it('keeps info.version in sync with LATEST_SPEC_VERSION and the filename', async () => {
    fetchMock.mockRejectedValueOnce(new Error('offline'));
    await openRpcService.load();
    expect(openRpcService.specVersion()).toBe(LATEST_SPEC_VERSION);
    expect(DEFAULT_SPEC_PATH).toBe(`specs/firebolt_schema_validator-${LATEST_SPEC_VERSION}.json`);
  });

  it('falls back to the copy bundled at build time when the hosted spec cannot be fetched', async () => {
    fetchMock.mockRejectedValueOnce(new Error('offline'));
    const methods = await openRpcService.load();
    expect(methods.length).toBeGreaterThan(50);
    expect(openRpcService.sourceUrl()).toBe(`bundled:${DEFAULT_SPEC_PATH}`);
  });
});

describe('OpenRpcService.getParameterSets', () => {
  it("carries each example's sample result so the APIs tab can show it on failure", () => {
    const sets = openRpcService.getParameterSets({
      name: 'Device.name',
      module: 'Device',
      method: 'name',
      params: [],
      examples: [
        { name: 'Default', params: [], result: { name: 'Default Result', value: 'Living Room' } as any },
        { name: 'No result', params: [] }
      ]
    } as any);
    expect(sets.map((s) => s.exampleResult)).toEqual(['Living Room', undefined]);
  });
});
