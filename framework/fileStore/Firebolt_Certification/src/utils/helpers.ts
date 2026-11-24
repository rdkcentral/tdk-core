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
 * @file General helpers: ids, timeouts, error normalization, safe JSON stringify and event method/param utilities.
 */

export function uid(prefix = 'firebolt-certification'): string {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}
export async function withTimeout<T>(promise: Promise<T>, ms = 10000): Promise<T> {
  let timer = 0;
  const timeout = new Promise<never>((_, reject) => {
    timer = window.setTimeout(() => reject({ code: 'TimeOutError', message: `Timed out in ${ms} ms.` }), ms);
  });
  try {
    return await Promise.race([promise, timeout]);
  } finally {
    window.clearTimeout(timer);
  }
}
export function normalizeError(error: any): any {
  if (error == null) return null;
  // Only copy plain, serializable fields so raw Transport/WebSocket error objects
  // (which may hold circular refs to sockets/targets) can't leak into reports.
  if (typeof error === 'object' && ('code' in error || 'message' in error)) {
    const { code, message, name, stack } = error;
    return {
      code: code ?? 'FireboltCertificationError',
      message: message ?? String(error),
      ...(name ? { name } : {}),
      ...(typeof stack === 'string' ? { stack } : {})
    };
  }
  return { code: 'FireboltCertificationError', message: error instanceof Error ? error.message : String(error) };
}
// JSON.stringify replacer that drops circular references instead of throwing,
// so a single non-serializable response/error can't block report generation.
function circularSafeReplacer() {
  const seen = new WeakSet();
  return (_key: string, value: unknown) => {
    if (typeof value === 'object' && value !== null) {
      if (seen.has(value)) return '[Circular]';
      seen.add(value);
    }
    return value;
  };
}
export function safeStringify(value: unknown, space = 2): string {
  try {
    return JSON.stringify(value, null, space);
  } catch {
    try {
      return JSON.stringify(value, circularSafeReplacer(), space);
    } catch {
      return String(value);
    }
  }
}
/** Prefix of the validation error recorded when a subscription reply is not result: null. */
export const SUBSCRIPTION_REPLY_ERROR = 'subscription reply';
export const UNSUBSCRIBE_REPLY_ERROR = 'unsubscribe reply';
export function isEventMethod(method: any): boolean {
  return (
    !!method?.tags?.some((t: any) => t?.name === 'event') || /^on[A-Z]/.test(String(method?.name?.split('.')[1] || ''))
  );
}
// OpenRPC event methods declare a `listen` param for the JSON-RPC subscribe request; the SDK expresses
// subscription through listen() itself, so that param must never be passed positionally.
export function positionalParams<T extends { name: string }>(qualifiedMethod: string, params: T[]): T[] {
  return /^on[A-Z]/.test(String(qualifiedMethod.split('.')[1] || ''))
    ? params.filter((p) => p.name !== 'listen')
    : params;
}
export function entriesToObject<T = unknown>(entries: Array<[string, T]>): Record<string, T> {
  const result: Record<string, T> = {};
  for (const [key, value] of entries) result[key] = value;
  return result;
}
