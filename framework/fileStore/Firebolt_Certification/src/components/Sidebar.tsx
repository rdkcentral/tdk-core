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
 * @file Left navigation menu for switching between the app pages.
 */

import { Icon } from './Icons';
const items = [
  ['apis', 'APIs'],
  ['events', 'Events'],
  ['suites', 'Suites'],
  ['reports', 'Reports']
] as const;
export function Sidebar({ active, onSelect }: { active: string; onSelect: (value: string) => void }) {
  return (
    <aside class="sidebar">
      <nav>
        {items.map(([id, label]) => (
          <button
            key={id}
            data-focusable="true"
            class={active === id ? 'nav-item active' : 'nav-item'}
            onClick={() => onSelect(id)}
          >
            <Icon name={id} />
            <span>{label}</span>
          </button>
        ))}
      </nav>
      <div class="sidebar-footer">RCU: ↑ ↓ ← → &nbsp; OK &nbsp; Back</div>
    </aside>
  );
}
