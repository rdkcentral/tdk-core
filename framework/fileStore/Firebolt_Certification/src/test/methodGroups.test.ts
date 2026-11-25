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
 * @file Tests for grouping OpenRPC methods by module.
 */

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
