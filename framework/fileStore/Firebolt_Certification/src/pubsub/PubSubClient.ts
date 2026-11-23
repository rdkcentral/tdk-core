import { runtimeConfig } from '../config/runtime';
import { commandRouter } from '../core/CommandRouter';
import { eventBus } from '../core/EventBus';
import { logger } from '../utils/Logger';
import type { ConnectionState } from '../types';

export class PubSubClient {
  private ws: WebSocket | null = null;
  private reconnectTimer: number | null = null;
  private attempts = 0;
  private manuallyClosed = false;

  get subscribeTopic(): string {
    return `${runtimeConfig.pubSubUuid}_${runtimeConfig.appId}${runtimeConfig.pubSubSubscribeSuffix}`;
  }
  get publishTopic(): string {
    return `${runtimeConfig.pubSubUuid}_${runtimeConfig.appId}${runtimeConfig.pubSubPublishSuffix}`;
  }

  connect(): void {
    if (
      !runtimeConfig.pubSubUrl ||
      this.ws?.readyState === WebSocket.OPEN ||
      this.ws?.readyState === WebSocket.CONNECTING
    )
      return;
    this.manuallyClosed = false;
    this.state('connecting');
    try {
      this.ws = new WebSocket(runtimeConfig.pubSubUrl);
      this.ws.addEventListener('open', () => {
        this.attempts = 0;
        this.state('connected');
        this.send({ operation: 'sub', topic: this.subscribeTopic });
        logger.info(`Pub/Sub connected ${runtimeConfig.pubSubUrl}; subscribed ${this.subscribeTopic}`);
      });
      this.ws.addEventListener('message', (event) => this.onMessage(String(event.data)));
      this.ws.addEventListener('close', () => {
        this.state('disconnected');
        if (!this.manuallyClosed) this.scheduleReconnect();
      });
      this.ws.addEventListener('error', (e) => {
        this.state('error');
        logger.warn('Pub/Sub WebSocket error', e);
      });
    } catch (error) {
      this.state('error');
      logger.error('Unable to establish Pub/Sub connection', error);
      this.scheduleReconnect();
    }
  }

  close(): void {
    this.manuallyClosed = true;
    if (this.reconnectTimer) window.clearTimeout(this.reconnectTimer);
    this.reconnectTimer = null;
    this.ws?.close();
    this.ws = null;
    this.state('disconnected');
  }
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  publish(topic: string, message: unknown, headers?: unknown): boolean {
    if (!topic || !this.isConnected()) return false;
    const payload: any = { message: typeof message === 'string' ? message : JSON.stringify(message) };
    if (headers) payload.headers = headers;
    return this.send({ operation: 'pub', topic, payload });
  }

  private async onMessage(raw: string): Promise<void> {
    const unwrapped = this.unwrap(raw);
    if (!unwrapped) return;
    const { command, headers } = unwrapped;
    const responseTopic = command?.params?.responseTopic || command?.responseTopic || this.publishTopic;
    try {
      const response = await commandRouter.handle(command);
      if (response !== undefined) this.publish(responseTopic, response, headers);
    } catch (error) {
      this.publish(
        responseTopic,
        { code: 'FireboltCertificationError', message: error instanceof Error ? error.message : String(error) },
        headers
      );
    }
  }

  private unwrap(raw: string): { command: any; headers?: unknown } | null {
    try {
      const frame = JSON.parse(raw);
      let payload: any = frame?.payload?.message ?? frame?.payload ?? frame;
      const headers = frame?.payload?.headers || frame?.headers;
      if (typeof payload === 'string') payload = JSON.parse(payload);
      // Current Firebolt Certification/FCS server wrapper: { operation, topic, payload: "{\"data\":{\"query\":\"...\"}}" }
      if (payload?.data?.query !== undefined) {
        let query: any = payload.data.query;
        for (let i = 0; i < 3 && typeof query === 'string'; i++) {
          try {
            query = JSON.parse(query);
          } catch {
            break;
          }
        }
        payload = query;
      }
      return { command: payload, headers };
    } catch (error) {
      logger.warn('Pub/Sub notification parse failed', { raw, error });
      return null;
    }
  }
  private send(message: unknown): boolean {
    if (!this.isConnected()) return false;
    try {
      this.ws!.send(JSON.stringify(message));
      return true;
    } catch (error) {
      logger.error('Pub/Sub send failed', error);
      return false;
    }
  }
  private state(state: ConnectionState): void {
    eventBus.emit('pubsub-state', state);
  }
  private scheduleReconnect(): void {
    if (this.reconnectTimer || this.manuallyClosed) return;
    const delay = Math.min(30000, 1000 * Math.pow(2, this.attempts++));
    this.reconnectTimer = window.setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, delay);
  }
}
export const pubSubClient = new PubSubClient();
