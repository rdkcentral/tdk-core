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
 * @file Tests for failure explanations and the HTML report layout (module filter, event rows).
 */

import { describe, expect, it, vi } from 'vitest';
import { explainFailure } from '../reports/failureExplanation';
import { buildSuiteReport } from '../reports/ReportBuilder';
import { generateReportHtml } from '../reports/ReportExporter';
import { schemaValidator } from '../schema/SchemaValidator';
import type { ExecutionResult } from '../types';

vi.mock('../config/runtime', () => ({
  runtimeConfig: { logLevel: 'ERROR', reportingId: '', macAddress: '', appId: 'firebolt-certification' }
}));

const settings = {
  type: 'object',
  additionalProperties: false,
  required: ['enabled', 'preferredLanguages'],
  properties: {
    enabled: { type: 'boolean' },
    preferredLanguages: { type: 'array', items: { type: 'string', pattern: '^[a-z]{3}$' } }
  }
};
const failing = (response: unknown, schema: any, extra: Partial<ExecutionResult> = {}): ExecutionResult => ({
  id: '1',
  method: 'Accessibility.closedCaptionsSettings',
  mode: 'SDK',
  status: 'FAIL',
  durationMs: 5,
  timestamp: 0,
  response,
  schemaValidation: schemaValidator.validate(response, schema),
  ...extra
});
const text = (r: ExecutionResult) => explainFailure(r).join('\n');

describe('failure explanations', () => {
  it('explains a wrong type with expected and received', () => {
    expect(text(failing({ enabled: 'yes', preferredLanguages: [] }, settings))).toContain(
      'response.enabled: wrong type. Expected boolean, received string "yes".'
    );
  });
  it('explains a missing property', () => {
    expect(text(failing({ enabled: true }, settings))).toContain(
      'response: required property "preferredLanguages" is missing.'
    );
  });
  it('explains an undocumented property', () => {
    expect(text(failing({ enabled: true, preferredLanguages: [], extra: 1 }, settings))).toContain(
      'response: unexpected property "extra" (value 1) is not defined in the spec.'
    );
  });
  it('points at the failing list item', () => {
    expect(text(failing({ enabled: true, preferredLanguages: ['eng', 'usa1'] }, settings))).toContain(
      'response.preferredLanguages[1]: value "usa1" does not have the expected format'
    );
  });
  it('explains enums, ranges and empty strings', () => {
    expect(text(failing('2', { type: 'string', enum: ['0', '1'] }))).toContain(
      'value "2" is not allowed. Expected one of: "0", "1".'
    );
    expect(text(failing(101, { type: 'integer', minimum: 0, maximum: 100 }))).toContain(
      'value 101 is too large. Expected <= 100.'
    );
    expect(text(failing('', { type: 'string', minLength: 1 }))).toContain(
      'response: value is an empty string. Expected at least 1 character(s).'
    );
  });
  it('explains an empty response', () => {
    expect(
      text(
        failing(
          undefined,
          { type: 'boolean' },
          {
            schemaValidation: {
              valid: false,
              errors: [],
              rawErrors: [{ keyword: 'type', instancePath: '', params: { type: 'boolean' } }]
            }
          }
        )
      )
    ).toContain('Expected boolean, received nothing (no value).');
  });
  it('explains a device error', () => {
    const r: ExecutionResult = {
      id: '1',
      method: 'Device.foo',
      mode: 'SDK',
      status: 'FAIL',
      durationMs: 1,
      timestamp: 0,
      error: { code: -32601, message: 'Method not known' }
    };
    expect(text(r)).toBe('Device returned an error (code -32601): Method not known');
  });
  it('explains a subscription reply that is not null', () => {
    const r: ExecutionResult = {
      id: '1',
      method: 'Accessibility.onHighContrastUIChanged',
      mode: 'SDK',
      status: 'FAIL',
      durationMs: 1,
      timestamp: 0,
      response: { listening: true },
      schemaValidation: {
        valid: false,
        errors: ['subscription reply: expected null, received {"listening":true}'],
        rawErrors: []
      }
    };
    expect(text(r)).toContain('Expected null, received {"listening":true}.');
  });
  it('explains slow responses and ignores passing results', () => {
    const slow: ExecutionResult = {
      id: '1',
      method: 'Device.uid',
      mode: 'SDK',
      status: 'FAIL',
      durationMs: 900,
      timestamp: 0,
      response: 'x',
      sla: { expectedMs: 300, actualMs: 900, status: 'failed' }
    };
    expect(text(slow)).toBe('Too slow: took 900 ms, the limit is 300 ms.');
    expect(explainFailure({ ...slow, status: 'PASS' })).toEqual([]);
  });
  it('falls back to the recorded messages when no raw errors exist', () => {
    const r: ExecutionResult = {
      id: '1',
      method: 'X.y',
      mode: 'SDK',
      status: 'FAIL',
      durationMs: 1,
      timestamp: 0,
      schemaValidation: { valid: false, errors: ['Expected error, received result'] }
    };
    expect(text(r)).toContain('Expected error, received result');
  });
});

describe('report output', () => {
  const results = [failing({ enabled: 'yes', preferredLanguages: [] }, settings)];
  it('adds the explanation to the JSON report', () => {
    const report = buildSuiteReport('t', 'SDK', Date.now(), results);
    expect(report.results[0].failureReason?.join('\n')).toContain('Expected boolean, received string "yes"');
    expect(report.suites[0].tests[0].err).toEqual({ err: expect.stringContaining('Expected boolean') });
  });
  it('shows the failure reason in the HTML Log cell, after the actual response', () => {
    const html = generateReportHtml(buildSuiteReport('t', 'SDK', Date.now(), results));
    expect(html).toContain('<th class="sl">Sl No</th><th>APIs/Events</th><th>Description</th><th>Status</th><th>Log</th>');
    expect(html).not.toContain('<th>Duration</th>');
    expect(html).not.toContain('<th>Example</th>');
    expect(html.indexOf('>Actual response</div>')).toBeLessThan(html.indexOf('>Failure reason</div>'));
    expect(html).toContain('Expected boolean, received string &quot;yes&quot;');
  });
});

describe('event rows', () => {
  const ev = (eventAction: 'subscribe' | 'unsubscribe', response: unknown): ExecutionResult => ({
    id: 'e',
    method: 'Accessibility.onVoiceGuidanceSettingsChanged',
    mode: 'SDK',
    status: 'PASS',
    durationMs: 1,
    timestamp: 0,
    expectedFormat: 'null',
    eventAction,
    params: { listen: eventAction === 'subscribe' },
    response
  });
  const html = (...rs: ExecutionResult[]) => generateReportHtml(buildSuiteReport('t', 'SDK', Date.now(), rs));
  it('shows subscribe and unsubscribe as separate rows with expected null', () => {
    const out = html(ev('subscribe', null), ev('unsubscribe', null));
    expect(out).toContain('Accessibility.<wbr>onVoiceGuidanceSettingsChanged (Subscribe)');
    expect(out).toContain('Accessibility.<wbr>onVoiceGuidanceSettingsChanged (Unsubscribe)');
    expect(out).toContain('>Expected response format (OpenRPC schema)</div>');
    expect(out).not.toContain('notification');
    expect(out).not.toContain('Sample response');
  });
  it('shows a non-null reply as the actual response', () => {
    const out = html(ev('unsubscribe', { listening: false }));
    expect(out).toContain('&quot;listening&quot;: false');
  });
});

describe('HTML report layout', () => {
  it('uses the same Log sections as the Excel report and no suite name or module list in the header', () => {
    const res: ExecutionResult = {
      id: 'x',
      method: 'Device.timeInActiveState',
      mode: 'Transport',
      status: 'PASS',
      durationMs: 1,
      timestamp: 0,
      params: {},
      expectedFormat: 'integer (0 to 4294967295)',
      exampleResponse: 3600,
      response: 73278
    };
    const out = generateReportHtml(
      buildSuiteReport('Firebolt Transport Validation - Accessibility, Device', 'Transport', Date.now(), [res])
    );
    expect(out).toContain('<title>Firebolt Certification Report</title>');
    expect(out).not.toContain('Firebolt Transport Validation');
    expect(out).not.toContain('FIREBOLT-ALL');
    expect(out).not.toContain('Accessibility, Device');
    const order = ['>Method</div>', '>Expected response format (OpenRPC schema)</div>', '>Actual response</div>'];
    const at = order.map((l) => out.indexOf(l));
    expect(at.every((i) => i > 0)).toBe(true);
    expect([...at].sort((x, y) => x - y)).toEqual(at);
    expect(out).not.toContain('>Sample response</div>');
    expect(out).not.toContain('illustration only');
    expect(out).not.toContain('>Failure reason</div>');
    expect(out).not.toContain('>Parameters</div>');
    expect(out).toContain('integer (0 to 4294967295)');
  });
  it('shows the sample response only for failed tests', () => {
    const res: ExecutionResult = {
      id: 'x',
      method: 'Device.timeInActiveState',
      mode: 'Transport',
      status: 'FAIL',
      durationMs: 1,
      timestamp: 0,
      expectedFormat: 'integer (0 to 4294967295)',
      exampleResponse: 3600,
      response: 'oops',
      schemaValidation: { valid: false, errors: ['/ must be integer'] }
    };
    const out = generateReportHtml(buildSuiteReport('Firebolt Transport Validation', 'Transport', Date.now(), [res]));
    expect(out).toContain('>Sample response</div>');
  });
  const r = (method: string, status: ExecutionResult['status'], description?: string): ExecutionResult => ({
    id: method,
    method,
    mode: 'SDK',
    status,
    durationMs: 1,
    timestamp: 0,
    response: 'ok',
    description
  });
  const html = generateReportHtml(
    buildSuiteReport('t', 'SDK', Date.now(), [
      r('Device.name', 'PASS', 'Returns the device name'),
      r('Device.id', 'FAIL'),
      r('Accessibility.audioDescription', 'PASS')
    ])
  );
  it('offers a module filter with per-module counts (none on "All modules"), sorted by name', () => {
    expect(html).toContain(
      'data-value="">All modules</button><button type="button" class="dd-opt" role="option" aria-selected="false" data-value="Accessibility">Accessibility (1)</button><button type="button" class="dd-opt" role="option" aria-selected="false" data-value="Device">Device (2)</button>'
    );
    expect(html).toContain('data-module="Device" data-status="FAIL"');
  });
  it('shows the method description and status filter cards', () => {
    expect(html).toContain('<td class="desc">Returns the device name</td>');
    expect(html).toContain('data-status="FAIL"');
    expect(html).toContain('id="f-search"');
  });
});
