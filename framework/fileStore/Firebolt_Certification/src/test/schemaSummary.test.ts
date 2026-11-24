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
 * @file Tests for describeSchema, the human-readable schema summary.
 */

import { describe, expect, it } from 'vitest';
import { describeSchema } from '../reports/schemaSummary';

describe('describeSchema', () => {
  it('describes scalars with their limits', () => {
    expect(describeSchema({ type: 'integer', minimum: 0, maximum: 4294967295 })).toBe('integer (0 to 4294967295)');
    expect(describeSchema({ type: 'string', minLength: 1 })).toBe('string (not empty)');
    expect(describeSchema({ type: 'boolean' })).toBe('boolean');
    expect(describeSchema({ type: 'null' })).toBe('null');
  });
  it('describes enums, consts and nullable values', () => {
    expect(describeSchema({ type: 'string', enum: ['a', 'b'] })).toBe('one of: "a", "b"');
    expect(describeSchema({ const: 'x' })).toBe('exactly "x"');
    expect(describeSchema({ oneOf: [{ type: 'integer', minimum: 0 }, { type: 'null' }] })).toBe(
      'integer (≥ 0) — or null'
    );
  });
  it('describes objects with nested properties, required flags and additionalProperties', () => {
    expect(
      describeSchema({
        type: 'object',
        required: ['enabled'],
        additionalProperties: false,
        properties: {
          enabled: { type: 'boolean' },
          stats: { type: 'object', properties: { rx: { type: 'integer' } } },
          langs: { type: 'array', items: { type: 'string', pattern: '^[a-z]{3}$' } }
        }
      })
    ).toBe(
      [
        'object with:',
        '  enabled (required): boolean',
        '  stats (optional): object with:',
        '    rx (optional): integer',
        '  langs (optional): array of string (pattern ^[a-z]{3}$)',
        '  (no other properties allowed)'
      ].join('\n')
    );
  });
  it('returns an empty string when there is no schema and survives cycles', () => {
    expect(describeSchema(undefined)).toBe('');
    const loop: any = { type: 'object', title: 'Node', properties: {} };
    loop.properties.next = loop;
    expect(describeSchema(loop)).toContain('Node (see spec)');
  });
});
