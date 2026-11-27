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
 * @file Builds a CertificationSuiteReport (summary, per-test entries and failure reasons) from execution results.
 */

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
