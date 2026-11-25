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

// Turns an (already dereferenced) JSON schema into a short, human-readable description of the expected value,
// e.g. "integer (0 to 4294967295)" or an indented list of object properties.

const MAX_DEPTH = 6;
const quote = (v: unknown) => JSON.stringify(v);

function flatten<T>(items: T[], fn: (item: T) => string[]): string[] {
  const out: string[] = [];
  for (const item of items) out.push(...fn(item));
  return out;
}

function constraints(s: any): string[] {
  const out: string[] = [];
  if (s.minimum !== undefined && s.maximum !== undefined) out.push(`${s.minimum} to ${s.maximum}`);
  else if (s.minimum !== undefined) out.push(`≥ ${s.minimum}`);
  else if (s.maximum !== undefined) out.push(`≤ ${s.maximum}`);
  if (s.exclusiveMinimum !== undefined) out.push(`> ${s.exclusiveMinimum}`);
  if (s.exclusiveMaximum !== undefined) out.push(`< ${s.exclusiveMaximum}`);
  if (s.minLength !== undefined && s.maxLength !== undefined) out.push(`${s.minLength}–${s.maxLength} characters`);
  else if (s.minLength !== undefined) out.push(s.minLength === 1 ? 'not empty' : `at least ${s.minLength} characters`);
  else if (s.maxLength !== undefined) out.push(`at most ${s.maxLength} characters`);
  if (s.format) out.push(`format ${s.format}`);
  if (s.pattern) out.push(`pattern ${s.pattern}`);
  if (s.minItems !== undefined) out.push(`at least ${s.minItems} item${s.minItems === 1 ? '' : 's'}`);
  if (s.maxItems !== undefined) out.push(`at most ${s.maxItems} item${s.maxItems === 1 ? '' : 's'}`);
  return out;
}

const withConstraints = (base: string, s: any) => {
  const c = constraints(s);
  return c.length ? `${base} (${c.join(', ')})` : base;
};

function describe(schema: any, indent: string, depth: number, seen: Set<unknown>): string[] {
  if (schema === true || schema === undefined || schema === null) return ['any value'];
  if (schema === false) return ['no value allowed'];
  if (typeof schema !== 'object') return [String(schema)];
  if (depth > MAX_DEPTH || seen.has(schema)) return [schema.title ? `${schema.title} (see spec)` : 'object (see spec)'];
  seen = new Set(seen).add(schema);
  const next = `${indent}  `;

  if (schema.const !== undefined) return [`exactly ${quote(schema.const)}`];
  if (Array.isArray(schema.enum)) return [`one of: ${schema.enum.map(quote).join(', ')}`];

  for (const key of ['oneOf', 'anyOf'] as const) {
    if (Array.isArray(schema[key])) {
      const options = schema[key] as any[];
      // Common pattern: { oneOf: [X, { type: 'null' }] } → "X, or null".
      const nonNull = options.filter((o) => o?.type !== 'null');
      if (nonNull.length === 1 && options.length === 2) {
        const [first, ...rest] = describe(nonNull[0], indent, depth + 1, seen);
        return [`${first} — or null`, ...rest];
      }
      return [
        key === 'oneOf' ? 'one of:' : 'any of:',
        ...flatten(options, (o) => bullet(describe(o, next, depth + 1, seen), next))
      ];
    }
  }
  if (Array.isArray(schema.allOf)) {
    return ['all of:', ...flatten(schema.allOf as any[], (o) => bullet(describe(o, next, depth + 1, seen), next))];
  }

  const types: string[] = Array.isArray(schema.type)
    ? schema.type
    : schema.type
      ? [schema.type]
      : schema.properties
        ? ['object']
        : schema.items
          ? ['array']
          : [];
  const nullable = types.includes('null') && types.length > 1;
  const main = types.filter((t) => t !== 'null');
  const suffix = nullable ? ' — or null' : '';

  if (main.length === 1 && main[0] === 'object') {
    const props = schema.properties && typeof schema.properties === 'object' ? Object.entries(schema.properties) : [];
    const required = new Set<string>(Array.isArray(schema.required) ? schema.required : []);
    if (!props.length) {
      const values =
        schema.additionalProperties && typeof schema.additionalProperties === 'object'
          ? ` whose values are ${describe(schema.additionalProperties, next, depth + 1, seen).join(' ')}`
          : '';
      return [`object${values}${suffix}`];
    }
    const lines = [`object${suffix} with:`];
    for (const [name, prop] of props) {
      const [first, ...rest] = describe(prop, next, depth + 1, seen);
      lines.push(`${next}${name} (${required.has(name) ? 'required' : 'optional'}): ${first}`, ...rest);
    }
    if (schema.additionalProperties === false) lines.push(`${next}(no other properties allowed)`);
    return lines;
  }
  if (main.length === 1 && main[0] === 'array') {
    const [first, ...rest] = describe(schema.items, next, depth + 1, seen);
    return [`${withConstraints('array', schema)}${suffix} of ${first}`, ...rest];
  }
  if (main.length) return [`${withConstraints(main.join(' or '), schema)}${suffix}`];
  if (nullable || types.includes('null')) return ['null'];
  return ['any value'];
}

function bullet(lines: string[], indent: string): string[] {
  const [first, ...rest] = lines;
  return [`${indent}- ${first}`, ...rest.map((l) => `  ${l}`)];
}

/** Readable description of what a valid response looks like, or '' when there is no schema. */
export function describeSchema(schema: unknown): string {
  if (schema === undefined || schema === null) return '';
  return describe(schema, '', 0, new Set()).join('\n');
}
