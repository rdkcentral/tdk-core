import { describe, expect, it, vi } from 'vitest';
import { buildSuiteReport } from '../reports/ReportBuilder';
import { generateReportXlsx, logText, reportFileName } from '../reports/ReportExporter';
import type { ExecutionResult } from '../types';

vi.mock('../config/runtime', () => ({
  runtimeConfig: { logLevel: 'ERROR', reportingId: '', macAddress: '', appId: 'firebolt-certification' }
}));

const results: ExecutionResult[] = [
  {
    id: '1',
    method: 'Device.name',
    mode: 'SDK',
    status: 'FAIL',
    durationMs: 12,
    timestamp: 0,
    params: {},
    expectedFormat: 'string (not empty)',
    exampleResponse: 'Living Room',
    response: 'Kitchen <TV> & "box"',
    description: 'Returns the device name',
    failureReason: ['Name is too long']
  },
  {
    id: '2',
    method: 'Accessibility.onVoiceGuidanceSettingsChanged',
    mode: 'SDK',
    status: 'PASS',
    durationMs: 3000,
    timestamp: 0,
    params: { listen: true },
    expectedFormat: 'null',
    eventAction: 'subscribe',
    response: null
  }
];

const captures = (re: RegExp, source: string): string[] => {
  const out: string[] = [];
  for (let m = re.exec(source); m; m = re.exec(source)) out.push(m[1]);
  return out;
};

describe('Excel report', () => {
  const report = buildSuiteReport('Firebolt SDK Validation - Accessibility, Device', 'SDK', Date.now(), results);
  const bytes = generateReportXlsx(report);
  const text = new TextDecoder().decode(bytes);

  it('is a ZIP package with the workbook parts', () => {
    expect([...bytes.slice(0, 4)]).toEqual([0x50, 0x4b, 0x03, 0x04]);
    for (const part of [
      '[Content_Types].xml',
      'xl/workbook.xml',
      'xl/styles.xml',
      'xl/worksheets/sheet1.xml',
      'xl/worksheets/sheet3.xml'
    ])
      expect(text).toContain(part);
  });
  it('puts the Summary sheet first, then one sheet per module in name order', () => {
    const sheets = captures(/<sheet name="([^"]+)" sheetId/g, text);
    expect(sheets).toEqual(['Summary', 'Accessibility', 'Device']);
  });
  it('summarises overall and per-module results with links to the module sheets', () => {
    expect(text).toContain('Firebolt Certification Report');
    expect(text).toContain('Results by module');
    expect(text).toContain(`location="'Accessibility'!A1"`);
    expect(text).toContain(`location="'Device'!A1"`);
  });
  it('module sheets have Method, Description, Status and Log columns', () => {
    const device = text.slice(text.indexOf('xl/worksheets/sheet3.xml<?xml'));
    const headers = captures(
      /<c r="[A-Z]1" t="inlineStr" s="\d+"><is><t xml:space="preserve">([^<]+)<\/t>/g,
      device.slice(0, device.indexOf('</worksheet>'))
    );
    expect(headers).toEqual(['Sl No', 'Method', 'Description', 'Status', 'Log']);
    expect(device).toContain('Returns the device name');
  });
  it('Log order: expected format, actual response, failure reason (failures only), then sample response (XML-escaped)', () => {
    // No parameters → no Parameters section.
    expect(logText(results[0])).toBe(
      'Method:\nDevice.name\n\nExpected response format (OpenRPC schema):\nstring (not empty)\n\nActual response:\n"Kitchen <TV> & \\"box\\""\n\nFailure reason:\nName is too long\n\nSample response:\n"Living Room"'
    );
    // Passing result → no Failure reason section.
    expect(logText(results[1])).toBe(
      'Method:\nAccessibility.onVoiceGuidanceSettingsChanged (Subscribe)\n\nParameters:\n{\n  "listen": true\n}\n\nExpected response format (OpenRPC schema):\nnull\n\nActual response:\nnull'
    );
    expect(logText(results[0])).not.toContain('illustration only');
    expect(text).toContain('Kitchen &lt;TV&gt; &amp;');
  });
  it('summary has no suite name and no SDK, overall-result or footnote rows', () => {
    const summary = text.slice(
      text.indexOf('xl/worksheets/sheet1.xml<?xml'),
      text.indexOf('xl/worksheets/sheet2.xml<?xml')
    );
    expect(summary).not.toContain('Firebolt SDK Validation');
    expect(summary).not.toContain('>Suite<');
    for (const gone of ['>core<', 'Overall result', 'Generated ', 'Pass rate *', 'Pass rate = '])
      expect(summary).not.toContain(gone);
    expect(text).not.toContain('<tabColor');
  });
  it('uses the .xlsx file name', () => {
    expect(reportFileName(report, 'xlsx')).toMatch(/^firebolt-certification-refAppExecReport-\d{8}-\d{6}\.xlsx$/);
  });
});
