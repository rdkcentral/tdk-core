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
