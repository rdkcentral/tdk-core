import type { JSX } from 'preact';

export function Icon({ name }: { name: string }): JSX.Element {
  const common = {
    width: 20,
    height: 20,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 1.8,
    strokeLinecap: 'round' as const,
    strokeLinejoin: 'round' as const
  };
  const paths: Record<string, JSX.Element> = {
    apis: (
      <>
        <path d="M8 4H5a2 2 0 0 0-2 2v3" />
        <path d="M16 20h3a2 2 0 0 0 2-2v-3" />
        <path d="M21 9V6a2 2 0 0 0-2-2h-3" />
        <path d="M3 15v3a2 2 0 0 0 2 2h3" />
        <path d="m9 15 6-6" />
        <path d="M10 9h5v5" />
      </>
    ),
    suites: (
      <>
        <path d="M5 4h10l4 4v12H5z" />
        <path d="M15 4v5h5" />
        <path d="m9 13 5 3-5 3z" />
      </>
    ),
    reports: (
      <>
        <path d="M5 3h14v18H5z" />
        <path d="M8 8h8M8 12h8M8 16h5" />
      </>
    ),
    events: (
      <>
        <path d="M4 7h16v10H4z" />
        <path d="m8 10 4 3 4-3" />
      </>
    ),
    sun: (
      <>
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
      </>
    ),
    moon: <path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z" />
  };
  return <svg {...common}>{paths[name]}</svg>;
}
