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
/** Prefix of the validation error recorded when a subscription reply is not the RDK8+ result: null. */
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
