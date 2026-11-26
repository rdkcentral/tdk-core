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
 * @file Tests for OpenRpcService spec loading (hosted file, version/fireboltVersion, spec index and bundled fallback) and parameter sets.
 */

import { beforeEach, describe, expect, it, vi } from 'vitest';
import bundled from '../../public/specs/firebolt_schema_validator_9.0.0_M155.json';
import specIndex from '../../public/specs/index.json';

const location = { search: '' };
vi.stubGlobal('window', { location });
vi.stubGlobal('document', { baseURI: 'http://vm:5173/' });
const runtimeConfig: { logLevel: string; version: string; fireboltVersion: string } = {
  logLevel: 'ERROR',
  version: '',
  fireboltVersion: ''
};
vi.mock('../config/runtime', () => ({
  runtimeConfig,
  getConfiguredExclusions: () => [],
  buildExclusionMatcher: () => () => false
}));
const fetchMock = vi.fn();
vi.stubGlobal('fetch', fetchMock);

const { openRpcService, DEFAULT_SPEC_PATH, LATEST_RELEASE_VERSION, FIREBOLT_VERSION } = await import(
  '../schema/OpenRpcService'
);
const hosted = {
  methods: [{ name: 'Device.name', params: [], result: { name: 'value', schema: { type: 'string' } } }]
};
const ok = (json: unknown) => ({ ok: true, status: 200, json: async () => json });

describe("OpenRpcService loads only Firebolt Certification's own OpenRPC", () => {
  beforeEach(() => {
    fetchMock.mockReset();
    location.search = '';
    runtimeConfig.version = '';
    runtimeConfig.fireboltVersion = '';
  });

  it('reads the hosted spec next to the app by default (no URL parameter needed), bypassing the cache', async () => {
    fetchMock.mockResolvedValueOnce(ok(hosted));
    const methods = await openRpcService.load();
    expect(fetchMock).toHaveBeenCalledWith(`http://vm:5173/${DEFAULT_SPEC_PATH}`, { cache: 'no-store' });
    expect(methods.map((m) => m.name)).toEqual(['Device.name']);
    expect(openRpcService.sourceUrl()).toBe(`http://vm:5173/${DEFAULT_SPEC_PATH}`);
  });

  it('fetches the file for the requested versions and does not fall back to the bundle', async () => {
    runtimeConfig.version = 'M153';
    runtimeConfig.fireboltVersion = '8.0.0';
    fetchMock.mockResolvedValueOnce(ok({ ...hosted, info: { version: 'M153' } }));
    await openRpcService.load();
    expect(fetchMock).toHaveBeenCalledWith('http://vm:5173/specs/firebolt_schema_validator_8.0.0_M153.json', {
      cache: 'no-store'
    });
    expect(openRpcService.specVersion()).toBe('M153');
    fetchMock.mockRejectedValueOnce(new Error('404'));
    await expect(openRpcService.load()).rejects.toThrow();
  });

  it('builds the path directly, without the index, when both version and fireboltVersion are given', async () => {
    runtimeConfig.version = ' M155 ';
    runtimeConfig.fireboltVersion = ' 9.0.0 ';
    fetchMock.mockResolvedValueOnce(ok(hosted));
    await openRpcService.load();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(openRpcService.sourceUrl()).toBe('http://vm:5173/specs/firebolt_schema_validator_9.0.0_M155.json');
  });

  const index = {
    specs: [
      { fireboltVersion: '9.0.0', releaseVersion: 'M155' },
      { fireboltVersion: '9.0.0', releaseVersion: 'M154' },
      { fireboltVersion: '8.0.0', releaseVersion: 'M153' }
    ]
  };

  it('looks up the newest release for fireboltVersion alone in specs/index.json', async () => {
    runtimeConfig.fireboltVersion = '9.0.0';
    fetchMock.mockResolvedValueOnce(ok(index)).mockResolvedValueOnce(ok(hosted));
    await openRpcService.load();
    expect(fetchMock).toHaveBeenNthCalledWith(1, 'http://vm:5173/specs/index.json', { cache: 'no-store' });
    expect(fetchMock).toHaveBeenNthCalledWith(2, 'http://vm:5173/specs/firebolt_schema_validator_9.0.0_M155.json', {
      cache: 'no-store'
    });
  });

  it('looks up the Firebolt version for version alone in specs/index.json', async () => {
    runtimeConfig.version = 'M153';
    fetchMock.mockResolvedValueOnce(ok(index)).mockResolvedValueOnce(ok(hosted));
    await openRpcService.load();
    expect(fetchMock).toHaveBeenNthCalledWith(1, 'http://vm:5173/specs/index.json', { cache: 'no-store' });
    expect(openRpcService.sourceUrl()).toBe('http://vm:5173/specs/firebolt_schema_validator_8.0.0_M153.json');
  });

  it('fails clearly, without the bundle, when the index has no match or cannot be read', async () => {
    runtimeConfig.version = 'M999';
    fetchMock.mockResolvedValueOnce(ok(index));
    await expect(openRpcService.load()).rejects.toThrow('No OpenRPC spec listed in specs/index.json for version M999');
    fetchMock.mockResolvedValueOnce({ ok: false, status: 404, json: async () => ({}) });
    await expect(openRpcService.load()).rejects.toThrow('Unable to read the spec index');
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it('keeps info.version and firebolt-version in sync with the constants and the filename', async () => {
    fetchMock.mockRejectedValueOnce(new Error('offline'));
    await openRpcService.load();
    expect(openRpcService.specVersion()).toBe(LATEST_RELEASE_VERSION);
    expect(bundled.info['firebolt-version']).toBe(FIREBOLT_VERSION);
    expect(specIndex.specs[0]).toEqual({ fireboltVersion: FIREBOLT_VERSION, releaseVersion: LATEST_RELEASE_VERSION });
    expect(DEFAULT_SPEC_PATH).toBe(`specs/firebolt_schema_validator_${FIREBOLT_VERSION}_${LATEST_RELEASE_VERSION}.json`);
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
