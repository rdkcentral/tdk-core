import { jsonRpcClient, type NotificationHandler } from './JsonRpcClient';

/** Firebolt access over Firebolt Certification's own RDK8+ JSON-RPC client (no @firebolt-js dependency). */
export class TransportAdapter {
  invoke(qualifiedMethod: string, params: Record<string, unknown>, timeoutMs = 10000): Promise<unknown> {
    return jsonRpcClient.call(qualifiedMethod, params, timeoutMs);
  }
  /** Resolves with the gateway's subscription reply; RDK8+ requires result: null. */
  subscribe(
    qualifiedEvent: string,
    handler: NotificationHandler,
    params: Record<string, unknown> = {},
    timeoutMs = 10000
  ): Promise<unknown> {
    return jsonRpcClient.subscribe(qualifiedEvent, handler, params, timeoutMs);
  }
  unsubscribe(
    qualifiedEvent: string,
    handler?: NotificationHandler,
    timeoutMs = 10000,
    force = false
  ): Promise<unknown> {
    return jsonRpcClient.unsubscribe(qualifiedEvent, handler, timeoutMs, force);
  }
}
export const transportAdapter = new TransportAdapter();
