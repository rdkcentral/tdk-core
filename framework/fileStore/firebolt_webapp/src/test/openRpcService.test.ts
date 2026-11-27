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
 * @file Tests for OpenRpcService spec loading (hosted file and bundled fallback) and parameter sets.
 */

import { beforeEach, describe, expect, it, vi } from 'vitest';

vi.stubGlobal('window', { location: { search: '' } });
vi.stubGlobal('document', { baseURI: 'http://vm:5173/' });
vi.mock('../config/runtime', () => ({
  runtimeConfig: { logLevel: 'ERROR' },
  getConfiguredExclusions: () => [],
  buildExclusionMatcher: () => () => false
}));
const fetchMock = vi.fn();
vi.stubGlobal('fetch', fetchMock);

const { openRpcService, SPEC_PATH } = await import('../schema/OpenRpcService');
const hosted = {
  methods: [{ name: 'Device.name', params: [], result: { name: 'value', schema: { type: 'string' } } }]
};
const ok = (json: unknown) => ({ ok: true, status: 200, json: async () => json });

describe("OpenRpcService loads only Firebolt Certification's own OpenRPC", () => {
  beforeEach(() => {
    fetchMock.mockReset();
  });

  it('reads the hosted spec next to the app, bypassing the cache', async () => {
    fetchMock.mockResolvedValueOnce(ok(hosted));
    const methods = await openRpcService.load();
    expect(SPEC_PATH).toBe('specs/firebolt_schema_validator_9.0.0.json');
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock).toHaveBeenCalledWith(`http://vm:5173/${SPEC_PATH}`, { cache: 'no-store' });
    expect(methods.map((m) => m.name)).toEqual(['Device.name']);
    expect(openRpcService.sourceUrl()).toBe(`http://vm:5173/${SPEC_PATH}`);
  });

  it('falls back to the copy bundled at build time when the hosted spec cannot be fetched', async () => {
    fetchMock.mockRejectedValueOnce(new Error('offline'));
    const methods = await openRpcService.load();
    expect(methods.length).toBeGreaterThan(50);
    expect(openRpcService.sourceUrl()).toBe(`bundled:${SPEC_PATH}`);
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
