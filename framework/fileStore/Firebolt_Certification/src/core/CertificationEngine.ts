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
 * @file Core runner: invokes each OpenRPC method/example (and event subscribe/unsubscribe) through the selected
 * mode, validates responses against the schema and SLA and collects the results for a suite report.
 */

import type {
  CertificationRunOptions,
  CertificationSuiteReport,
  CommunicationMode,
  ExecutionResult,
  OpenRpcMethod,
  ValidationResult
} from '../types';
import { fireboltAdapter } from '../firebolt/FireboltAdapter';
import { openRpcService } from '../schema/OpenRpcService';
import { schemaValidator } from '../schema/SchemaValidator';
import { buildSuiteReport } from '../reports/ReportBuilder';
import { eventBus } from './EventBus';
import { eventManager } from '../firebolt/EventManager';
import { logger } from '../utils/Logger';
import { CONNECTIVITY_PROBE_METHOD } from '../config/runtime';
import { describeSchema } from '../reports/schemaSummary';
import {
  SUBSCRIPTION_REPLY_ERROR,
  UNSUBSCRIBE_REPLY_ERROR,
  entriesToObject,
  isEventMethod,
  normalizeError,
  uid
} from '../utils/helpers';

const DEFAULT_SLA = 300;

/** Firebolt JSON-RPC: a successful subscribe/unsubscribe reply is result: null. */
export function validateSubscriptionReply(reply: unknown): ValidationResult {
  if (reply === null) return { valid: true, errors: [] };
  return {
    valid: false,
    errors: [
      `${SUBSCRIPTION_REPLY_ERROR}: expected null, received ${reply === undefined ? 'no result' : JSON.stringify(reply)}`
    ]
  };
}

export class CertificationEngine {
  private methodResponses = new Map<string, { result: unknown; error: unknown }>();
  private suites: CertificationSuiteReport[] = [];
  private currentAbort: AbortController | null = null;

  async initializeSchemas(): Promise<void> {
    await openRpcService.loadAll();
  }

  async invoke(
    method: string,
    params: unknown[] | Record<string, unknown> = [],
    mode: CommunicationMode = 'Transport',
    timeoutMs = 10000,
    validate = true
  ): Promise<ExecutionResult> {
    logger.info(`Executing ${method} via ${mode}`);
    const result = await fireboltAdapter.invoke({ method, params, mode, timeoutMs });
    const schemaMethod = openRpcService.getMethod(result.method);
    if (validate && result.status === 'PASS' && schemaMethod && isEventMethod(schemaMethod.raw)) {
      // Calling an on* method directly is a subscribe/unsubscribe request: the gateway replies with result: null.
      // The OpenRPC result schema describes the notification payload, not this reply.
      const sdkAcknowledgement =
        mode === 'SDK' &&
        result.response &&
        typeof result.response === 'object' &&
        'subscriptionAccepted' in result.response &&
        'unsubscribed' in result.response;
      result.schemaValidation = sdkAcknowledgement
        ? { valid: true, errors: [] }
        : validateSubscriptionReply(result.response);
      if (!result.schemaValidation.valid) result.status = 'FAIL';
    } else if (validate && result.status === 'PASS' && schemaMethod?.resultSchema) {
      result.schemaValidation = schemaValidator.validate(result.response, schemaMethod.resultSchema);
      if (!result.schemaValidation.valid) result.status = 'FAIL';
    } else if (result.error) {
      result.schemaValidation = schemaValidator.validateError(result.error);
    }
    this.methodResponses.set(result.method.toLowerCase(), {
      result: result.response ?? null,
      error: result.error ?? null
    });
    this.emitResult(result);
    return result;
  }

  private emitResult(result: ExecutionResult): void {
    eventBus.emit('execution', result);
    logger[result.status === 'PASS' ? 'info' : 'error'](
      `${result.method} ${result.status} (${result.durationMs} ms)`,
      result.error
    );
  }

  getSuites(): CertificationSuiteReport[] {
    return [...this.suites];
  }
  getMethodResponse(method: string): { result: unknown; error: unknown } {
    return this.methodResponses.get(method.toLowerCase()) || { result: null, error: null };
  }
  probe(): Promise<ExecutionResult> {
    return this.invoke(CONNECTIVITY_PROBE_METHOD, [], 'Transport', 10000, false);
  }
  stopSuite(): void {
    this.currentAbort?.abort();
    this.currentAbort = null;
  }

  async runSuite(options: CertificationRunOptions): Promise<CertificationSuiteReport> {
    this.stopSuite();
    this.currentAbort = new AbortController();
    const signal = this.currentAbort.signal;
    const started = Date.now();
    const moduleFilter = options.modules?.length ? new Set(options.modules.map((m) => m.toLowerCase())) : null;
    const methods = openRpcService
      .getMethods()
      .filter((m) => !moduleFilter || moduleFilter.has(m.module.toLowerCase()));
    const methodTotal = methods.length;
    let methodIndex = 0;
    let methodsCompleted = 0;
    const results: ExecutionResult[] = [];
    for (const method of methods) {
      if (signal.aborted) break;
      methodIndex++;
      const cases = this.examplesFor(method);
      let complete = true;
      if (!cases.length) {
        results.push(...(await this.runCase(method, this.defaultParams(method), undefined, options)));
      } else {
        for (const example of cases) {
          if (signal.aborted) {
            complete = false;
            break;
          }
          const params = entriesToObject(
            (example.params || []).map((p: any) => [p.name, p.value] as [string, unknown])
          );
          const caseResults = await this.runCase(method, params, example.name, options);
          if (!isEventMethod(method.raw))
            caseResults.forEach((r) => {
              r.exampleResponse = example.result?.value;
            });
          results.push(...caseResults);
        }
      }
      if (complete) methodsCompleted++;
      eventBus.emit('suite-progress', { completed: results.length, current: method.name, methodIndex, methodTotal });
    }
    const byName = new Map<string, OpenRpcMethod>();
    for (const m of methods) byName.set(m.name, m);
    for (const r of results) {
      const m = byName.get(r.method);
      r.description = m?.summary || m?.description || undefined;
      r.expectedFormat =
        (m && isEventMethod(m.raw)
          ? r.response &&
            typeof r.response === 'object' &&
            ('subscriptionAccepted' in r.response || 'unsubscribed' in r.response)
            ? 'SDK listener acknowledgement (not a raw gateway reply)'
            : 'null'
          : describeSchema(m?.resultSchema)) || undefined;
    }
    const scope = options.scopeLabel || (options.modules?.length ? options.modules.join(', ') : 'All modules');
    const title = `Firebolt ${options.mode} Validation - ${scope}`;
    const report = buildSuiteReport(title, options.mode, started, results);
    report.specVersion = openRpcService.specVersion() || undefined;
    // A stopped run is partial: mark it so reports never present it as a completed (PASSED) certification.
    if (methodsCompleted < methodTotal) {
      report.interrupted = true;
      report.methodsNotRun = methodTotal - methodsCompleted;
    }
    this.suites.unshift(report);
    if (this.suites.length > 20) this.suites.length = 20;
    eventBus.emit('suite-complete', report);
    if (this.currentAbort?.signal === signal) this.currentAbort = null;
    return report;
  }

  // Subscribes ({listen: true}) then unsubscribes ({listen: false}); each reply must be null and is reported as its own row.
  // Notification payloads are not validated.
  private async runEventCase(
    method: OpenRpcMethod,
    params: Record<string, unknown>,
    exampleName: string | undefined,
    options: CertificationRunOptions
  ): Promise<ExecutionResult[]> {
    const base = {
      method: method.name,
      mode: options.mode,
      exampleName: exampleName ? `${method.name}.${exampleName}` : undefined
    };
    const record = (
      r: Partial<ExecutionResult> & {
        status: ExecutionResult['status'];
        eventAction: 'subscribe' | 'unsubscribe';
        durationMs: number;
      }
    ): ExecutionResult => {
      const out = { id: uid('exec'), timestamp: Date.now(), ...base, exampleResponse: null, ...r } as ExecutionResult;
      this.methodResponses.set(method.name.toLowerCase(), { result: out.response ?? null, error: out.error ?? null });
      this.emitResult(out);
      return out;
    };
    const timed = async <T>(fn: () => Promise<T>): Promise<[T, number]> => {
      const t = performance.now();
      const value = await fn();
      return [value, Math.round(performance.now() - t)];
    };

    const [registration, subscribeMs] = await timed(() => eventManager.register(method.name, params, options.mode));
    const subscribeError = registration.eventListenerResponse?.error;
    if (subscribeError || !registration.eventListenerId) {
      return [
        record({
          eventAction: 'subscribe',
          params,
          durationMs: subscribeMs,
          status: 'FAIL',
          error: subscribeError ?? 'Event subscription failed',
          schemaValidation: schemaValidator.validateError(subscribeError ?? {})
        })
      ];
    }
    const subscriptionReply = registration.eventListenerResponse?.subscriptionReply ?? null;
    const subErrors = registration.eventListenerResponse?.sdkManaged
      ? []
      : validateSubscriptionReply(registration.eventListenerResponse?.subscriptionReply).errors;
    const subscribeRow = record({
      eventAction: 'subscribe',
      params,
      durationMs: subscribeMs,
      status: subErrors.length ? 'FAIL' : 'PASS',
      response: subscriptionReply,
      schemaValidation: { valid: !subErrors.length, errors: subErrors, rawErrors: [] }
    });

    const [unsub, unsubscribeMs] = await timed(() => eventManager.unsubscribe(registration.eventListenerId));
    const unsubscribeReply = unsub?.unsubscribeReply;
    const unsubErrors = unsub?.error
      ? [
          `${UNSUBSCRIBE_REPLY_ERROR}: request failed (${(unsub.error as { message?: string }).message ?? JSON.stringify(unsub.error)})`
        ]
      : unsub?.sdkManaged
        ? []
        : validateSubscriptionReply(unsubscribeReply).errors.map(
            (e) => UNSUBSCRIBE_REPLY_ERROR + e.slice(SUBSCRIPTION_REPLY_ERROR.length)
          );
    const unsubscribeRow = record({
      eventAction: 'unsubscribe',
      params: { listen: false },
      durationMs: unsubscribeMs,
      status: unsubErrors.length ? 'FAIL' : 'PASS',
      response: unsubscribeReply,
      schemaValidation: { valid: !unsubErrors.length, errors: unsubErrors, rawErrors: [] }
    });
    return [subscribeRow, unsubscribeRow];
  }

  private async runCase(
    method: OpenRpcMethod,
    params: Record<string, unknown>,
    exampleName: string | undefined,
    options: CertificationRunOptions
  ): Promise<ExecutionResult[]> {
    // The spec's generic "Default example" name adds nothing to logs/reports; show just the method.
    if (exampleName?.trim().toLowerCase() === 'default example') exampleName = undefined;
    if (isEventMethod(method.raw)) return this.runEventCase(method, params, exampleName, options);
    return [await this.runSingleCase(method, params, exampleName, options)];
  }

  private async runSingleCase(
    method: OpenRpcMethod,
    params: Record<string, unknown>,
    exampleName: string | undefined,
    options: CertificationRunOptions
  ): Promise<ExecutionResult> {
    const expectedError = this.isException(method.name, params, options.exceptionMethods || []);
    const result = await fireboltAdapter.invoke({ method: method.name, params, mode: options.mode, timeoutMs: 10000 });
    result.exampleName = exampleName ? `${method.name}.${exampleName}` : undefined;
    result.params = params;
    const sdkSetupError =
      options.mode === 'SDK' &&
      result.error &&
      typeof result.error === 'object' &&
      'code' in result.error &&
      typeof result.error.code === 'string' &&
      result.error.code.startsWith('Sdk');
    const infrastructureError =result.error && typeof result.error === 'object' && 'code' in result.error && ['TimeOutError', 'ConnectionError'].includes(String(result.error.code));
    if (expectedError && !sdkSetupError && !infrastructureError) {
      if (!result.error) {
        result.status = 'FAIL';
        result.schemaValidation = { valid: false, errors: ['Expected error, received result'] };
      } else {
        result.schemaValidation = schemaValidator.validateError(result.error);
        result.status = result.schemaValidation.valid ? 'PASS' : 'FAIL';
      }
    } else if (result.error) {
      result.schemaValidation = schemaValidator.validateError(result.error);
      result.status = 'FAIL';
    } else if (method.resultSchema) {
      result.schemaValidation = schemaValidator.validate(result.response, method.resultSchema);
      result.status = result.schemaValidation.valid ? 'PASS' : 'FAIL';
    }
    if (options.slaValidation) {
      const expected = options.globalSla ?? DEFAULT_SLA;
      result.sla = {
        expectedMs: expected,
        actualMs: result.durationMs,
        status: result.durationMs < expected ? 'passed' : 'failed'
      };
      if (result.sla.status === 'failed') result.status = 'FAIL';
    }
    this.methodResponses.set(method.name.toLowerCase(), {
      result: result.response ?? null,
      error: result.error ?? null
    });
    this.emitResult(result);
    return result;
  }

  private examplesFor(method: OpenRpcMethod): any[] {
    return (method.examples || []).filter(
      (e) => !String(e.name || '').startsWith('Subscribe') && !String(e.name || '').startsWith('Set')
    );
  }
  // Used only when a method has no usable OpenRPC example; params without a schema value are left out.
  private defaultParams(method: OpenRpcMethod): Record<string, unknown> {
    const value: Record<string, unknown> = {};
    for (const p of method.params || []) {
      if (p.schema?.default !== undefined) value[p.name] = p.schema.default;
      else if (p.schema?.examples?.length) value[p.name] = p.schema.examples[0];
      else if (p.schema?.example !== undefined) value[p.name] = p.schema.example;
    }
    return value;
  }
  private isException(
    method: string,
    params: Record<string, unknown>,
    exceptions: Array<{ method: string; param?: Record<string, unknown> }>
  ): boolean {
    return exceptions.some(
      (e) =>
        e.method === method &&
        (!e.param || Object.entries(e.param).every(([k, v]) => JSON.stringify(params[k]) === JSON.stringify(v)))
    );
  }

  formatStandaloneCall(task: string, result: ExecutionResult): any {
    let responseCode = 0;
    let schemaValidationStatus = 'PASS';
    if (result.error) {
      const v = schemaValidator.validateError(normalizeError(result.error));
      schemaValidationStatus = v.valid ? 'PASS' : 'FAIL';
      responseCode = v.valid ? 0 : 1;
    } else if (result.response === undefined) {
      responseCode = 2;
      schemaValidationStatus = 'SKIPPED';
    } else if (result.schemaValidation && !result.schemaValidation.valid) {
      responseCode = 1;
      schemaValidationStatus = 'FAIL';
    }
    return {
      method: task,
      params: result.params,
      responseCode,
      apiResponse: { result: result.response ?? null, error: result.error ?? null },
      schemaValidationStatus,
      schemaValidationResponse: result.schemaValidation ?? { valid: true, errors: [] }
    };
  }
}
export const certificationEngine = new CertificationEngine();
