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
