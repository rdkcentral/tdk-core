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
