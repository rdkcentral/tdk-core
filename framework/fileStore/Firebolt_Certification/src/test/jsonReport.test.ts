import { describe, expect, it, vi } from 'vitest';
import { generateReportJson } from '../reports/ReportExporter';
import type { CertificationSuiteReport, ExecutionResult } from '../types';

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
    response: 'Kitchen',
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
// Hand-built report (bypasses buildSuiteReport's failureReason rewrite) so this test only exercises generateReportJson.
const report: CertificationSuiteReport = {
  id: 'r1',
  title: 'Firebolt SDK Validation - Accessibility, Device',
  mode: 'SDK',
  specVersion: '9.0.0',
  startedAt: 0,
  endedAt: 1,
  summary: { total: 2, passed: 1, failed: 1, durationMs: 1 },
  results,
  stats: { suites: 1, tests: 2, passes: 1, failures: 1, start: '', end: '', duration: 1 },
  suites: [
    {
      uuid: 's1',
      title: 'x',
      tests: [{ uuid: '1' }, { uuid: '2' }],
      suites: [],
      root: false,
      fullFile: '',
      file: '',
      passes: ['2'],
      failures: ['1'],
      duration: 1
    }
  ]
};

describe('JSON report', () => {
  const json = JSON.parse(generateReportJson(report));

  it('groups results by module, alphabetically, like the Excel sheets', () => {
    expect(json.modules.map((m: any) => m.module)).toEqual(['Accessibility', 'Device']);
    expect(json.results).toBeUndefined();
  });

  it('replaces the flat results array with Sl No/Method/Description/Status/Log per module', () => {
    const device = json.modules.find((m: any) => m.module === 'Device');
    expect(device.results).toEqual([
      { slNo: 1, method: 'Device.name', description: 'Returns the device name', status: 'FAIL', log: expect.any(Array) }
    ]);
    expect(device.results[0].log.map((s: any) => s.label)).toEqual([
      'Method',
      'Expected response format (OpenRPC schema)',
      'Actual response',
      'Failure reason',
      'Sample response'
    ]);
    expect(device.results[0].log.find((s: any) => s.label === 'Failure reason').text).toBe('Name is too long');
  });

  it('includes Parameters only when there are any, matching the HTML/Excel Log', () => {
    const acc = json.modules.find((m: any) => m.module === 'Accessibility');
    expect(acc.results[0].log.map((s: any) => s.label)).toEqual([
      'Method',
      'Parameters',
      'Expected response format (OpenRPC schema)',
      'Actual response'
    ]);
  });

  it('gives each module the same counts as the Excel Summary sheet, plus a pass rate', () => {
    expect(json.modules.find((m: any) => m.module === 'Device')).toMatchObject({
      total: 1,
      passed: 0,
      failed: 1,
      passRate: 0
    });
    expect(json.modules.find((m: any) => m.module === 'Accessibility')).toMatchObject({
      total: 1,
      passed: 1,
      failed: 0,
      passRate: 1
    });
  });

  it('keeps id/title/summary/stats/suites for FCS/Mocha-style compatibility', () => {
    expect(json).toMatchObject({ id: 'r1', title: report.title, mode: 'SDK', summary: report.summary });
    expect(json.stats.tests).toBe(2);
    expect(json.suites[0].tests).toHaveLength(2);
  });

  it('labels the spec version as fireboltSchemaValidatorSpecVersion', () => {
    expect(json.fireboltSchemaValidatorSpecVersion).toBe('9.0.0');
    expect(json.specVersion).toBeUndefined();
  });

  it('has no pending/skipped fields', () => {
    expect(generateReportJson(report)).not.toMatch(/"(pending|skipped|pendingTests)"/i);
  });
});
