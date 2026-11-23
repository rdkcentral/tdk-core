import { runtimeConfig } from '../config/runtime';

type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR';
const priorities: Record<string, number> = { DEBUG: 10, INFO: 20, WARN: 30, ERROR: 40 };

function write(level: LogLevel, message: string, data?: unknown): void {
  if ((priorities[level] || 20) < (priorities[runtimeConfig.logLevel] || 20)) return;
  const fn =
    level === 'ERROR'
      ? console.error
      : level === 'WARN'
        ? console.warn
        : level === 'DEBUG'
          ? console.debug
          : console.info;
  fn(`[Firebolt Certification] ${message}`, data ?? '');
}
export const logger = {
  debug: (m: string, d?: unknown) => write('DEBUG', m, d),
  info: (m: string, d?: unknown) => write('INFO', m, d),
  warn: (m: string, d?: unknown) => write('WARN', m, d),
  error: (m: string, d?: unknown) => write('ERROR', m, d)
};
