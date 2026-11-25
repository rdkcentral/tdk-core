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
 * @file Tests for the report theme tokens and logo in the generated HTML.
 */

import { describe, expect, it, vi } from 'vitest';
import { buildSuiteReport } from '../reports/ReportBuilder';
import { generateReportHtml } from '../reports/ReportExporter';

vi.mock('../config/runtime', () => ({
  runtimeConfig: { logLevel: 'ERROR', reportingId: '', macAddress: '', appId: 'firebolt-certification' }
}));

const report = () =>
  buildSuiteReport('t', 'SDK', Date.now(), [
    { id: '1', method: 'Device.version', mode: 'SDK', status: 'PASS', durationMs: 1, timestamp: Date.now() }
  ]);

describe('report theme', () => {
  it('report HTML embeds the Graphite & Teal tokens for dark and light', () => {
    const html = generateReportHtml(report());
    expect(html).toContain('<html lang="en" class="light"><head>');
    expect(generateReportHtml(report(), 'dark')).toContain('<html lang="en"><head>');
    expect(html).toContain(':root{--bg:#121417;');
    expect(html).toContain('html.light{--bg:#eceef0;');
    expect(html).not.toContain('data-palette');
  });

  it('report HTML includes the logo unless it is rendered inside the app', () => {
    expect(generateReportHtml(report())).toContain('class="report-logo"');
    expect(generateReportHtml(report(), 'light', false)).not.toContain('report-logo"');
  });
});
