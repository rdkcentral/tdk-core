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
 * @file Tests the bundled OpenRPC spec itself: examples validate, and positive/negative values match the schemas.
 */

import { describe, expect, it } from 'vitest';
import spec from '../../public/specs/firebolt_schema_validator_9.0.0.json';
import { schemaValidator } from '../schema/SchemaValidator';
import { entriesToObject, positionalParams } from '../utils/helpers';

const root = spec as any;
function resolve(node: any, seen: string[] = []): any {
  if (Array.isArray(node)) return node.map((n) => resolve(n, seen));
  if (!node || typeof node !== 'object') return node;
  if (typeof node.$ref === 'string' && node.$ref.startsWith('#/') && !seen.includes(node.$ref)) {
    const target = node.$ref
      .slice(2)
      .split('/')
      .reduce((n: any, part: string) => n?.[part], root);
    const { $ref, ...rest } = node;
    return { ...resolve(target, [...seen, $ref]), ...resolve(rest, seen) };
  }
  return entriesToObject(Object.keys(node).map((k) => [k, resolve(node[k], seen)] as [string, unknown]));
}
const methods: any[] = resolve(root.methods);
const byName = (name: string) => methods.find((m) => m.name === name);
const valid = (value: unknown, schema: any) => schemaValidator.validate(value, schema).valid;

function withUndocumentedProperty(value: any, schema: any): any | undefined {
  if (value && typeof value === 'object' && !Array.isArray(value) && schema?.additionalProperties === false)
    return { ...value, undocumentedProperty: 'x' };
  if (Array.isArray(value) && value.length && schema?.items?.additionalProperties === false)
    return [{ ...value[0], undocumentedProperty: 'x' }, ...value.slice(1)];
  return undefined;
}

describe('Firebolt OpenRPC spec', () => {
  it('gives every method at least one example', () => {
    expect(methods.filter((m) => !m.examples?.length).map((m) => m.name)).toEqual([]);
  });

  it.each(methods.map((m) => [m.name, m]))('%s examples pass their param and result schemas', (_name, m: any) => {
    const declared = new Map<string, any>(m.params.map((p: any) => [p.name, p]));
    for (const example of m.examples) {
      const given = new Map<string, unknown>(example.params.map((p: any) => [p.name, p.value]));
      for (const name of given.keys()) expect(declared.has(name), `undeclared param ${name}`).toBe(true);
      for (const [name, p] of declared) {
        if (p.required) expect(given.has(name), `missing required param ${name}`).toBe(true);
        if (given.has(name)) expect(schemaValidator.validate(given.get(name), p.schema).errors).toEqual([]);
      }
      expect(schemaValidator.validate(example.result.value, m.result.schema).errors).toEqual([]);
    }
    for (const wire of m['x-notification']?.examples || []) {
      if (!('id' in wire.message))
        expect(schemaValidator.validate(wire.message.params, m['x-notification'].params).errors).toEqual([]);
      else if ('result' in wire.message) expect(wire.message.result).toBeNull();
    }
  });

  it('rejects an undocumented property in every object result and notification payload', () => {
    let checked = 0;
    for (const m of methods) {
      const cases: Array<[any, any]> = m.examples.map((e: any) => [e.result.value, m.result.schema]);
      for (const wire of m['x-notification']?.examples || [])
        if (!('id' in wire.message)) cases.push([wire.message.params, m['x-notification'].params]);
      for (const [value, schema] of cases) {
        const tampered = withUndocumentedProperty(value, schema);
        if (tampered === undefined) continue;
        checked++;
        expect(valid(tampered, schema), `${m.name} accepted an undocumented property`).toBe(false);
      }
    }
    expect(checked).toBeGreaterThan(20);
  });

  it('rejects documented negative cases', () => {
    const result = (name: string) => byName(name).result.schema;
    expect(
      valid(
        { ifa: 'bd87dd10-8d1d-4b93-b1a6-a8e5d410e400', ifa_type: 'sspid', lmt: '0', extra: 1 },
        result('Advertising.advertisingId')
      )
    ).toBe(false);
    expect(valid({ ifa: 'not-a-uuid', ifa_type: 'sspid', lmt: '0' }, result('Advertising.advertisingId'))).toBe(false);
    expect(valid({ enabled: true }, result('Accessibility.closedCaptionsSettings'))).toBe(false);
    expect(valid('usa', result('Localization.country'))).toBe(false);
    expect(valid(true, result('Metrics.ready'))).toBe(false);
    expect(valid({ width: 1920, height: 1081 }, result('VideoOutput.resolution'))).toBe(false);
  });

  it('rejects empty strings where a value is required, but accepts them where the spec allows', () => {
    const result = (name: string) => byName(name).result.schema;
    for (const name of ['Device.firmware', 'Device.name', 'Device.onNameChanged']) {
      expect(valid('', result(name)), `${name} accepted ""`).toBe(false);
    }
    expect(valid([''], result('Localization.preferredAudioLanguages'))).toBe(false);
    expect(valid('', result('Localization.country'))).toBe(true);
    expect(valid('', result('Device.osName'))).toBe(true);
    expect(valid('', result('Device.osVersion'))).toBe(true);
  });

  it('accepts documented edge values', () => {
    const result = (name: string) => byName(name).result.schema;
    expect(valid('', result('Localization.country'))).toBe(true);
    expect(valid([], result('Localization.preferredAudioLanguages'))).toBe(true);
  });

  it('accepts an empty Display.colorimetry response', () => {
    const schema = byName('Display.colorimetry').result.schema;
    expect(valid([], schema)).toBe(true);
    expect(valid(['bt709'], schema)).toBe(true);
  });

  it('never passes the OpenRPC listen param positionally to the SDK', () => {
    const event = byName('Device.onNameChanged');
    expect(positionalParams(event.name, event.params).map((p: any) => p.name)).toEqual([]);
  });
});
