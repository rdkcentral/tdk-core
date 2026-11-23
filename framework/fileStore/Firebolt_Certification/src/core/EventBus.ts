type Handler<T = any> = (payload: T) => void;
class EventBus {
  private handlers = new Map<string, Set<Handler>>();
  on<T = any>(event: string, handler: Handler<T>): () => void {
    if (!this.handlers.has(event)) this.handlers.set(event, new Set());
    this.handlers.get(event)!.add(handler as Handler);
    return () => this.handlers.get(event)?.delete(handler as Handler);
  }
  emit<T = any>(event: string, payload: T): void {
    this.handlers.get(event)?.forEach((h) => h(payload));
  }
}
export const eventBus = new EventBus();
