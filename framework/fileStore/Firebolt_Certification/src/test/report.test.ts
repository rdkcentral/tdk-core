import { describe, expect, it } from 'vitest';
import { buildSuiteReport } from '../reports/ReportBuilder';

describe('report builder', () => {
  it('summarizes statuses', () => {
    const r = buildSuiteReport('x', 'SDK', Date.now() - 5, [
      { id: '1', method: 'Device.version', mode: 'SDK', status: 'PASS', durationMs: 1, timestamp: Date.now() },
      { id: '2', method: 'Device.id', mode: 'SDK', status: 'FAIL', durationMs: 1, timestamp: Date.now() }
    ]);
    expect(r.summary.passed).toBe(1);
    expect(r.summary.failed).toBe(1);
    expect(r.stats.tests).toBe(2);
  });
});
