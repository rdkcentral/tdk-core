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
 * @file Minimal in-app publish/subscribe event bus used to share state changes between modules and the UI.
 */

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
