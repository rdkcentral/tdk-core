import type { CertificationSuiteReport, CommunicationMode, ExecutionResult } from '../types';
import { safeStringify, uid } from '../utils/helpers';
import { explainFailure } from './failureExplanation';

export function buildSuiteReport(
  title: string,
  mode: CommunicationMode,
  startedAt: number,
  rawResults: ExecutionResult[]
): CertificationSuiteReport {
  const results = rawResults.map((r) => (r.status === 'FAIL' ? { ...r, failureReason: explainFailure(r) } : r));
  const endedAt = Date.now();
  const passed = results.filter((r) => r.status === 'PASS').length;
  const failed = results.filter((r) => r.status === 'FAIL').length;
  const suiteId = uid('suite');
  const tests = results.map((r) => {
    const suffix = r.eventAction ? ` (${r.eventAction === 'subscribe' ? 'Subscribe' : 'Unsubscribe'})` : '';
    return {
      title: `${r.exampleName || r.method}${suffix}`,
      fullTitle: `${r.method}${suffix}`,
      duration: r.durationMs,
      state: r.status.toLowerCase(),
      pass: r.status === 'PASS',
      fail: r.status === 'FAIL',
      code: safeStringify({
        'Failure reason': r.failureReason,
        'Schema Validation': r.schemaValidation,
        'SLA Validation': r.sla,
        response: r.response
      }),
      err: r.failureReason
        ? { err: r.failureReason.join('\n') }
        : r.error
          ? { err: r.error }
          : { err: 'No error found' },
      uuid: r.id,
      parentUUID: suiteId,
      timedOut: false,
      speed: 'fast',
      context: safeStringify({ result: r.response, error: r.error, params: r.params }),
      isHook: false
    };
  });
  return {
    id: suiteId,
    title,
    mode,
    startedAt,
    endedAt,
    summary: { total: results.length, passed, failed, durationMs: endedAt - startedAt },
    results,
    stats: {
      suites: 1,
      tests: results.length,
      passes: passed,
      failures: failed,
      start: new Date(startedAt).toISOString(),
      end: new Date(endedAt).toISOString(),
      duration: endedAt - startedAt
    },
    suites: [
      {
        uuid: suiteId,
        title,
        tests,
        suites: [],
        root: false,
        fullFile: '',
        file: '',
        passes: tests.filter((t) => t.pass).map((t) => t.uuid),
        failures: tests.filter((t) => t.fail).map((t) => t.uuid),
        duration: endedAt - startedAt
      }
    ]
  };
}
