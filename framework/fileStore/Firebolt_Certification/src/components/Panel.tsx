import type { ComponentChildren } from 'preact';
export function Panel({
  title,
  children,
  className = ''
}: {
  title?: string;
  children: ComponentChildren;
  className?: string;
}) {
  return (
    <section class={`panel ${className}`}>
      {title && <h3>{title}</h3>}
      {children}
    </section>
  );
}
