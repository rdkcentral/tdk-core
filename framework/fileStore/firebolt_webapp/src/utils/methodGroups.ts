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
 * @file Groups OpenRPC methods by module (the part before the dot), sorted for display.
 */

import type { OpenRpcMethod } from '../types';

export interface ModuleGroup {
  module: string;
  methods: OpenRpcMethod[];
}

/** Unique key of a method in Firebolt Certification's OpenRPC (method names are unique). */
export function methodKey(method: Pick<OpenRpcMethod, 'name'>): string {
  return method.name;
}

/** Groups methods by module name. Modules are sorted alphabetically and methods by name. */
export function groupMethodsByModule(methods: OpenRpcMethod[]): ModuleGroup[] {
  const groups = new Map<string, OpenRpcMethod[]>();
  for (const m of methods) {
    const list = groups.get(m.module);
    if (list) list.push(m);
    else groups.set(m.module, [m]);
  }
  return [...groups.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([module, list]) => ({ module, methods: [...list].sort((a, b) => a.method.localeCompare(b.method)) }));
}
