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
 * @file Console logger with levels, filtered by the configured log level.
 */

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
