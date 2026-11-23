import { describe, expect, it } from 'vitest';
import { groupMethodsByModule, methodKey } from '../utils/methodGroups';
import type { OpenRpcMethod } from '../types';

const m = (name: string): OpenRpcMethod => {
  const [module, method] = name.split('.');
  return { name, module, method, params: [], examples: [], raw: { name } };
};

describe('module grouping', () => {
  const methods = [m('Device.version'), m('HDMIInput.ports'), m('Device.name'), m('Account.id')];
  const groups = groupMethodsByModule(methods);

  it('groups by module, sorted alphabetically, with methods sorted by name', () => {
    expect(groups.map((g) => g.module)).toEqual(['Account', 'Device', 'HDMIInput']);
    expect(groups.find((g) => g.module === 'Device')!.methods.map(methodKey)).toEqual([
      'Device.name',
      'Device.version'
    ]);
    expect(groups.reduce((n, g) => n + g.methods.length, 0)).toBe(methods.length);
  });
});
