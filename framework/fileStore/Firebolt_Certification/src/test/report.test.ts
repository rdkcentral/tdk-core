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
 * @file Tests for the suite report builder summary.
 */

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
