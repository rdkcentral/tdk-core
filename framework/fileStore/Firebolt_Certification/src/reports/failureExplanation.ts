import type { ExecutionResult } from '../types';
import { SUBSCRIPTION_REPLY_ERROR, UNSUBSCRIBE_REPLY_ERROR } from '../utils/helpers';

interface AjvLikeError {
  keyword?: string;
  instancePath?: string;
  message?: string;
  params?: Record<string, any>;
}

function show(value: unknown): string {
  if (value === undefined) return 'nothing (no value)';
  let text: string;
  try {
    text = JSON.stringify(value);
  } catch {
    text = String(value);
  }
  if (text === undefined) text = String(value);
  return text.length > 80 ? `${text.slice(0, 77)}...` : text;
}

function typeOf(value: unknown): string {
  if (value === null) return 'null';
  if (Array.isArray(value)) return 'array';
  if (value === undefined) return 'nothing';
  return typeof value === 'number' && Math.floor(value) === value ? 'integer' : typeof value;
}

function valueAt(root: unknown, path: string): unknown {
  let node: any = root;
  for (const part of path.split('/').slice(1)) {
    if (node === null || node === undefined) return undefined;
    node = node[part.replace(/~1/g, '/').replace(/~0/g, '~')];
  }
  return node;
}

function label(path: string, root: string): string {
  if (!path) return root;
  return (
    root +
    path
      .split('/')
      .slice(1)
      .map((p) => (/^\d+$/.test(p) ? `[${p}]` : `.${p}`))
      .join('')
  );
}

function list(values: unknown[]): string {
  return values.map((v) => show(v)).join(', ');
}

function describe(e: AjvLikeError, response: unknown, root: string): string | null {
  const path = e.instancePath || '';
  const where = label(path, root);
  const p = e.params || {};
  const received = valueAt(response, path);
  switch (e.keyword) {
    case 'type': {
      const expected = Array.isArray(p.type) ? p.type.join(' or ') : p.type;
      return `${where}: wrong type. Expected ${expected}, received ${received === undefined ? 'nothing (no value)' : `${typeOf(received)} ${show(received)}`}.`;
    }
    case 'required':
      return `${where}: required property "${p.missingProperty}" is missing.`;
    case 'additionalProperties': {
      const extra = valueAt(response, `${path}/${p.additionalProperty}`);
      return `${where}: unexpected property "${p.additionalProperty}" (value ${show(extra)}) is not defined in the spec.`;
    }
    case 'enum':
      return `${where}: value ${show(received)} is not allowed. Expected one of: ${list(p.allowedValues || [])}.`;
    case 'const':
      return `${where}: value ${show(received)} is not allowed. Expected exactly ${show(p.allowedValue)}.`;
    case 'minLength':
      return received === ''
        ? `${where}: value is an empty string. Expected at least ${p.limit} character(s).`
        : `${where}: value ${show(received)} is too short. Expected at least ${p.limit} character(s).`;
    case 'maxLength':
      return `${where}: value ${show(received)} is too long. Expected at most ${p.limit} character(s).`;
    case 'pattern':
      return `${where}: value ${show(received)} does not have the expected format (pattern ${p.pattern}).`;
    case 'minimum':
    case 'exclusiveMinimum':
      return `${where}: value ${show(received)} is too small. Expected ${p.comparison || '>='} ${p.limit}.`;
    case 'maximum':
    case 'exclusiveMaximum':
      return `${where}: value ${show(received)} is too large. Expected ${p.comparison || '<='} ${p.limit}.`;
    case 'minItems':
      return `${where}: list has ${Array.isArray(received) ? received.length : '?'} item(s). Expected at least ${p.limit}.`;
    case 'maxItems':
      return `${where}: list has ${Array.isArray(received) ? received.length : '?'} item(s). Expected at most ${p.limit}.`;
    case 'format':
      return `${where}: value ${show(received)} is not a valid ${p.format}.`;
    case 'anyOf':
    case 'oneOf':
    case 'if':
    case 'allOf':
      return null;
    default:
      return `${where}: ${e.message || 'does not match the schema'} (received ${show(received)}).`;
  }
}

function describeAll(errors: AjvLikeError[], response: unknown, root: string): string[] {
  const out: string[] = [];
  let wrapperOnly = false;
  for (const e of errors) {
    const line = describe(e, response, root);
    if (line === null) wrapperOnly = true;
    else if (out.indexOf(line) < 0) out.push(line);
  }
  if (!out.length && wrapperOnly) {
    const first = errors[0];
    out.push(
      `${label(first?.instancePath || '', root)}: value ${show(valueAt(response, first?.instancePath || ''))} does not match any of the shapes allowed by the spec.`
    );
  }
  return out;
}

function errorLine(error: unknown): string {
  if (error && typeof error === 'object') {
    const { code, message } = error as { code?: unknown; message?: unknown };
    if (typeof code === 'string' && code.startsWith('Sdk')) return String(message ?? code);
    if (code !== undefined || message !== undefined)
      return `Device returned an error${code !== undefined ? ` (code ${String(code)})` : ''}: ${String(message ?? 'no message')}`;
  }
  return `Device returned an error: ${show(error)}`;
}

// Turns a failed result into plain-English lines: what went wrong, where, and what was expected vs received.
export function explainFailure(r: ExecutionResult): string[] {
  if (r.status !== 'FAIL') return [];
  const lines: string[] = [];
  const sv = r.schemaValidation;
  if (r.error !== undefined && r.error !== null) {
    lines.push(errorLine(r.error));
    if (sv && !sv.valid) lines.push('The error object itself is not in the expected shape {code, message}.');
  } else if (sv && !sv.valid) {
    // Reply errors look like "<prefix>: expected null, received …"; show only the part after the prefix.
    const replyDetail = (e: string, prefix: string) => {
      const detail = e.slice(prefix.length).replace(/^:\s*/, '');
      return `${detail.charAt(0).toUpperCase()}${detail.slice(1)}.`;
    };
    sv.errors
      .filter((e) => e.startsWith(SUBSCRIPTION_REPLY_ERROR))
      .forEach((e) => lines.push(replyDetail(e, SUBSCRIPTION_REPLY_ERROR)));
    sv.errors
      .filter((e) => e.startsWith(UNSUBSCRIBE_REPLY_ERROR))
      .forEach((e) => lines.push(replyDetail(e, UNSUBSCRIBE_REPLY_ERROR)));
    const otherErrors = sv.errors.filter(
      (e) => !e.startsWith(SUBSCRIPTION_REPLY_ERROR) && !e.startsWith(UNSUBSCRIBE_REPLY_ERROR)
    );
    const detail =
      sv.rawErrors && sv.rawErrors.length
        ? describeAll(sv.rawErrors as AjvLikeError[], r.response, 'response')
        : otherErrors;
    if (detail.length) {
      lines.push('The device response does not match the OpenRPC schema:');
      detail.forEach((d) => lines.push(`  - ${d}`));
    }
  }
  if (r.sla && r.sla.status === 'failed')
    lines.push(`Too slow: took ${r.sla.actualMs} ms, the limit is ${r.sla.expectedMs} ms.`);
  if (!lines.length) lines.push('The call was marked FAIL but no error or schema mismatch was recorded.');
  return lines;
}
