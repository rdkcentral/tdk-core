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
 * @file Handles certification commands (tasks such as runTest, callMethod, registerEvent, healthCheck) received
 * from launch parameters or Pub/Sub, and returns their responses.
 */

import type { CommunicationMode, FireboltCertificationCommand } from '../types';
import { runtimeConfig } from '../config/runtime';
import { certificationEngine } from './CertificationEngine';
import { eventManager } from '../firebolt/EventManager';
import { providerManager } from '../providers/ProviderManager';
import { lifecycleManager } from '../lifecycle/LifecycleManager';
import { logger } from '../utils/Logger';
import { generateReportHtml, generateReportJson, generateReportXlsx, publishReport } from '../reports/ReportExporter';
import type { ReportFormat } from '../types';

function parseFormat(input?: string): ReportFormat {
  const format = String(input || 'json').toLowerCase();
  return format === 'html' || format === 'xlsx' ? format : 'json';
}

function toBase64(bytes: Uint8Array): string {
  let binary = '';
  for (let i = 0; i < bytes.length; i += 0x8000) binary += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(binary);
}

export class CommandRouter {
  private id = 0;

  async handle(message: FireboltCertificationCommand): Promise<any> {
    const task = message?.task || message?.command;
    const params = message?.params || message?.payload || {};
    message = { ...message, params };
    const standalone = message.standalone ?? runtimeConfig.standalone;
    if (!task) return { code: 'FireboltCertificationError', message: 'No task in request' };
    logger.info(`Intent received: ${task}`);
    try {
      switch (task) {
        case 'getPubSubStatus':
          return { pubSubStatus: 'Connection successful' };
        case 'healthCheck':
        case 'health':
          return { status: 'OK', appId: runtimeConfig.appId, state: 'READY', timestamp: Date.now(), version: '2.0.0' };
        case 'dataFetch':
          return undefined;
        case 'visibilityState':
          return { report: params.params === 'language' ? navigator.language : document.visibilityState };
        case 'callMethod':
        case 'firebolt.invoke':
          return await this.callMethod(message, standalone);
        case 'getMethodResponse':
          return { report: certificationEngine.getMethodResponse(params.method) };
        case 'registerEvent':
          return await this.registerEvent(message, standalone);
        case 'getEventResponse':
          return this.getEventResponse(message, standalone);
        case 'clearEventHandler':
          return { report: await eventManager.clear(params.event || '') };
        case 'clearAllListeners':
          return { report: await eventManager.clearAll() };
        case 'registerProviderHandler':
          return { report: await providerManager.register(params.provider || '') };
        case 'setApiResponse':
          return { report: providerManager.setApiResponse(params.apiResponse) };
        case 'startLifecycleRecording':
          return this.lifecycleRecord(true, params.appId);
        case 'stopLifecycleRecording':
          return this.lifecycleRecord(false, params.appId);
        case 'callLifecycle':
          return await this.callLifecycle(message, standalone);
        case 'runTest':
          return await this.runTest(message);
        case 'getReports':
          return { report: certificationEngine.getSuites() };
        case 'getReport':
          return this.getReport(params.reportId || params.id);
        case 'generateReport':
          return this.generateReport(params.reportId || params.id, params.format);
        case 'publishReport':
          return await this.publishReport(params.reportId || params.id, params.format);
        default:
          return { error: 'Invalid request. Provide valid method' };
      }
    } catch (error) {
      logger.error(`Task failed: ${task}`, error);
      return standalone
        ? {
            report: {
              responseCode: 1,
              error: {
                code: 'FireboltCertificationError',
                message: `Firebolt Certification in exception block: ${error instanceof Error ? error.message : String(error)}`
              }
            }
          }
        : {
            jsonrpc: '2.0',
            error: {
              code: 'FireboltCertificationError',
              message: error instanceof Error ? error.message : String(error)
            },
            id: ++this.id
          };
    }
  }

  // Transport is the default; SDK uses the shared Firebolt certification runner when explicitly requested.
  private mode(message: FireboltCertificationCommand): CommunicationMode {
    return String(message.context?.communicationMode || runtimeConfig.communicationMode).toLowerCase() === 'sdk'
      ? 'SDK'
      : 'Transport';
  }
  // Only Firebolt Certification's own OpenRPC exists, so there is no SDK/spec selection.

  private async callMethod(message: FireboltCertificationCommand, standalone: boolean): Promise<any> {
    const params = message.params || {};
    const method = params.method || params.methodName;
    if (!method)
      return standalone
        ? { report: { responseCode: 1, error: { code: 'FireboltCertificationError', message: 'Missing method' } } }
        : { jsonrpc: '2.0', error: { code: -32600, message: 'Missing method' }, id: ++this.id };
    const result = await certificationEngine.invoke(
      method,
      params.methodParams ?? params.args ?? {},
      this.mode(message),
      message.responseTimeout || 10000,
      standalone
    );
    if (standalone) return { report: certificationEngine.formatStandaloneCall('callMethod', result) };
    const id = ++this.id;
    return result.error ? { jsonrpc: '2.0', error: result.error, id } : { jsonrpc: '2.0', result: result.response, id };
  }

  private async registerEvent(message: FireboltCertificationCommand, standalone: boolean): Promise<any> {
    const params = message.params || {};
    const report = await eventManager.register(params.event, params.params || {}, this.mode(message));
    return standalone ? { report } : report;
  }
  private getEventResponse(message: FireboltCertificationCommand, standalone: boolean): any {
    const params = message.params || {};
    const rows = eventManager.getResponse(params.event || params.listenerId || '', Number(params.numberOfEvents || 1));
    const report = rows.length === 1 ? rows[0] : rows;
    return standalone ? { report } : { jsonrpc: '2.0', result: report, id: ++this.id };
  }
  private lifecycleRecord(start: boolean, appId: string): any {
    if (appId && appId !== runtimeConfig.appId)
      return { report: `AppId ${appId} passed does not match launched app ${runtimeConfig.appId}` };
    return { report: start ? lifecycleManager.start(runtimeConfig.appId) : lifecycleManager.stop(runtimeConfig.appId) };
  }
  private async callLifecycle(message: FireboltCertificationCommand, standalone: boolean): Promise<any> {
    const p = message.params || {};
    const method = p.methodName || p.method || p.name;
    const result = await lifecycleManager.call(method, p.methodParams ?? p.params ?? [], this.mode(message));
    if (standalone) return { report: result };
    return result.error
      ? { jsonrpc: '2.0', error: result.error, id: ++this.id }
      : { jsonrpc: '2.0', result: result.response, id: ++this.id };
  }

  private getReport(reportId?: string): any {
    const reports = certificationEngine.getSuites();
    const report = reportId ? reports.find((r) => r.id === reportId) : reports[0];
    return { report: report || null };
  }
  private generateReport(reportId?: string, formatInput?: string): any {
    const reports = certificationEngine.getSuites();
    const report = reportId ? reports.find((r) => r.id === reportId) : reports[0];
    if (!report) return { report: null, error: 'No generated report available' };
    const format = parseFormat(formatInput);
    if (format === 'xlsx')
      return { reportId: report.id, format, encoding: 'base64', content: toBase64(generateReportXlsx(report)) };
    return {
      reportId: report.id,
      format,
      content: format === 'html' ? generateReportHtml(report) : generateReportJson(report)
    };
  }
  private async publishReport(reportId?: string, formatInput?: string): Promise<any> {
    const reports = certificationEngine.getSuites();
    const report = reportId ? reports.find((r) => r.id === reportId) : reports[0];
    if (!report) return { report: null, error: 'No generated report available' };
    return { report: await publishReport(report, parseFormat(formatInput)) };
  }

  private async runTest(message: FireboltCertificationCommand): Promise<any> {
    const p = message.params || {};
    if (String(message.action) === 'Lifecycle.validation') {
      const method = p.methodName || p.method;
      return { report: await lifecycleManager.call(method, p.methodParams ?? [], 'Transport') };
    }
    const report = await certificationEngine.runSuite({
      mode: this.mode(message),
      exceptionMethods: p.exceptionMethods || [],
      slaValidation: !!p['sla-validation'],
      globalSla: p.globalSLA ?? runtimeConfig.globalSla
    });
    return { report };
  }
}
export const commandRouter = new CommandRouter();
