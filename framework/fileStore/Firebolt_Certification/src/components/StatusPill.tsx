export function StatusPill({
  label,
  status = 'ok',
  title
}: {
  label: string;
  status?: 'ok' | 'warn' | 'bad';
  title?: string;
}) {
  return (
    <span class={`status-pill ${status}`} title={title}>
      <span class="status-dot" />
      <span class="status-label">{label}</span>
    </span>
  );
}
