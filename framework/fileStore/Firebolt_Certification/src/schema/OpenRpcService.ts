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
 * @file Loads the versioned OpenRPC spec, resolves $refs and exposes its methods, schemas and example parameter sets.
 */

import latestOpenRpc from '../../public/specs/firebolt_schema_validator_9.0.0_M155.json';
import { buildExclusionMatcher, getConfiguredExclusions, runtimeConfig } from '../config/runtime';
import type { OpenRpcDocument, OpenRpcMethod, OpenRpcParameterSet } from '../types';
import { logger } from '../utils/Logger';
import { entriesToObject } from '../utils/helpers';

// Firebolt Certification certifies only against its own OpenRPC.
// At launch the spec is read from the server that hosts Firebolt Certification (public/specs/…), so editing that file only needs an app
// reload. The copy bundled at build time is used if it cannot be fetched.
// Spec files are named by Firebolt version and TDK monthly tag: specs/firebolt_schema_validator_<fireboltVersion>_<releaseVersion>.json.
// LATEST_RELEASE_VERSION is used unless the version (TDK monthly tag) and/or fireboltVersion launch parameters select another
// file; when only one is given, the file is looked up in specs/index.json. When a new file is added, list it in
// index.json (newest first) and bump LATEST_RELEASE_VERSION (and FIREBOLT_VERSION if it changed).
export const LATEST_RELEASE_VERSION = 'M155';
export const FIREBOLT_VERSION = '9.0.0';
export const SPEC_INDEX_PATH = 'specs/index.json';
export const specPathFor = (releaseVersion: string, fireboltVersion: string = FIREBOLT_VERSION): string =>
  `specs/firebolt_schema_validator_${fireboltVersion}_${releaseVersion}.json`;
export const DEFAULT_SPEC_PATH = specPathFor(LATEST_RELEASE_VERSION);
const bundledSpec = latestOpenRpc as unknown as OpenRpcDocument;

interface SpecIndexEntry {
  fireboltVersion: string;
  releaseVersion: string;
}
function pointer(root: any, ref: string): any {
  if (!ref.startsWith('#/')) return undefined;
  return ref
    .slice(2)
    .split('/')
    .reduce((node, part) => node?.[part.replace(/~1/g, '/').replace(/~0/g, '~')], root);
}
function dereference(root: any, node: any, seen = new Set<string>()): any {
  if (Array.isArray(node)) return node.map((v) => dereference(root, v, new Set(seen)));
  if (!node || typeof node !== 'object') return node;
  if (typeof node.$ref === 'string' && node.$ref.startsWith('#/')) {
    if (seen.has(node.$ref)) return { ...node };
    const target = pointer(root, node.$ref);
    if (target) {
      const next = new Set(seen);
      next.add(node.$ref);
      return {
        ...dereference(root, target, next),
        ...entriesToObject(Object.entries(node).filter(([k]) => k !== '$ref') as Array<[string, any]>)
      };
    }
  }
  const result: any = {};
  for (const [key, value] of Object.entries(node)) result[key] = dereference(root, value, new Set(seen));
  return result;
}
export class OpenRpcService {
  private doc: OpenRpcDocument | undefined;
  private methods: OpenRpcMethod[] = [];
  private source = '';

  /** Where the loaded spec came from: a URL, or "bundled:<path>" when the build-time copy was used. */
  sourceUrl(): string {
    return this.source;
  }
  /** Version of the loaded spec (info.version), or '' when nothing is loaded. */
  specVersion(): string {
    return String(this.doc?.info?.version || '');
  }

  async load(): Promise<OpenRpcMethod[]> {
    const releaseVersion = (runtimeConfig.version || '').trim();
    const fireboltVersion = (runtimeConfig.fireboltVersion || '').trim();
    let raw: OpenRpcDocument;
    if (releaseVersion || fireboltVersion) {
      // An explicitly requested spec must load as asked; falling back to the bundled copy would certify the wrong version.
      const url = new URL(await this.resolveSpecPath(fireboltVersion, releaseVersion), document.baseURI).toString();
      raw = await this.fetchSpec(url);
      this.source = url;
    } else {
      const url = new URL(DEFAULT_SPEC_PATH, document.baseURI).toString();
      try {
        raw = await this.fetchSpec(url);
        this.source = url;
      } catch (error) {
        logger.warn('Hosted OpenRPC unavailable; using the copy bundled at build time', { url, error });
        raw = bundledSpec;
        this.source = `bundled:${DEFAULT_SPEC_PATH}`;
      }
    }
    this.doc = dereference(raw, raw) as OpenRpcDocument;
    const isExcluded = buildExclusionMatcher(getConfiguredExclusions());
    const all = (this.doc.methods || []).map((m: any) => this.toMethod(m));
    this.methods = all.filter((m) => !isExcluded(m.name));
    logger.info(
      `Loaded OpenRPC document (${this.methods.length} methods, ${all.length - this.methods.length} excluded)`,
      { url: this.source, specVersion: this.specVersion() }
    );
    return this.methods;
  }

  async loadAll(): Promise<void> {
    try {
      await this.load();
    } catch (error) {
      logger.warn('Unable to load the OpenRPC document', { error });
      this.methods = [];
    }
  }

  private async fetchSpec(url: string): Promise<OpenRpcDocument> {
    const response = await fetch(url, { cache: 'no-store' });
    if (!response.ok) throw new Error(`OpenRPC HTTP ${response.status} (${url})`);
    const json = await response.json();
    if (!Array.isArray(json?.methods)) throw new Error(`OpenRPC document has no methods (${url})`);
    return json;
  }

  /**
   * Spec path for the requested versions. With both, the file name is built directly; with only one, the first
   * (newest) matching entry in specs/index.json supplies the other.
   */
  private async resolveSpecPath(fireboltVersion: string, releaseVersion: string): Promise<string> {
    if (fireboltVersion && releaseVersion) return specPathFor(releaseVersion, fireboltVersion);
    const requested = fireboltVersion ? `fireboltVersion ${fireboltVersion}` : `version ${releaseVersion}`;
    const url = new URL(SPEC_INDEX_PATH, document.baseURI).toString();
    let specs: unknown;
    try {
      const response = await fetch(url, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      specs = (await response.json())?.specs;
    } catch (error) {
      throw new Error(
        `Unable to read the spec index (${url}) to resolve ${requested}: ${error instanceof Error ? error.message : String(error)}`
      );
    }
    const match = (Array.isArray(specs) ? (specs as SpecIndexEntry[]) : []).find(
      (s) =>
        (!fireboltVersion || s?.fireboltVersion === fireboltVersion) &&
        (!releaseVersion || s?.releaseVersion === releaseVersion)
    );
    if (!match) throw new Error(`No OpenRPC spec listed in ${SPEC_INDEX_PATH} for ${requested}`);
    return specPathFor(match.releaseVersion, match.fireboltVersion);
  }

  private toMethod(m: any): OpenRpcMethod {
    const [module, ...rest] = String(m.name || '').split('.');
    return {
      name: m.name,
      module: module || 'Unknown',
      method: rest.join('.') || module || 'unknown',
      summary: m.summary || '',
      description: m.description || '',
      params: m.params || [],
      examples: m.examples || [],
      resultSchema: m.result?.schema,
      raw: m
    };
  }
  getMethods(): OpenRpcMethod[] {
    return [...this.methods];
  }

  getParameterSets(method: OpenRpcMethod): OpenRpcParameterSet[] {
    const examples = (method.examples || []).map((example, index) => ({
      name: example.name || `Example ${index + 1}`,
      params: entriesToObject((example.params || []).map((p) => [p.name, p.value] as [string, unknown])),
      source: 'example' as const,
      usable: true,
      exampleResult: (example.result as any)?.value
    }));
    if (examples.length) return examples;

    const params: Record<string, unknown> = {};
    const missing: string[] = [];
    for (const p of method.params || []) {
      if (p.schema?.default !== undefined) params[p.name] = p.schema.default;
      else if (Array.isArray(p.schema?.examples) && p.schema.examples.length) params[p.name] = p.schema.examples[0];
      else if (p.schema?.example !== undefined) params[p.name] = p.schema.example;
      else if (p.required) missing.push(p.name);
    }
    if (missing.length) {
      return [
        {
          name: 'OpenRPC defaults',
          params,
          source: 'default',
          usable: false,
          reason: `OpenRPC has no example/default for required parameter(s): ${missing.join(', ')}`
        }
      ];
    }
    return [
      {
        name: Object.keys(params).length ? 'OpenRPC defaults' : 'No parameters',
        params,
        source: 'default',
        usable: true
      }
    ];
  }
  getMethod(name: string): OpenRpcMethod | undefined {
    return this.methods.find((m) => m.name.toLowerCase() === name.toLowerCase());
  }
}
export const openRpcService = new OpenRpcService();
