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
 * @file Shared TypeScript types: runtime config, OpenRPC document/method shapes, execution results and reports.
 */

export type ConnectionState = 'connected' | 'connecting' | 'disconnected' | 'error' | 'disabled';
export type ResultStatus = 'PASS' | 'FAIL';
export type CommunicationMode = 'SDK' | 'Transport';

export interface RuntimeConfig {
  appId: string;
  appType: string;
  platform: string;
  fireboltEndpoint: string;
  pubSubUrl: string;
  pubSubUuid: string;
  pubSubSubscribeSuffix: string;
  pubSubPublishSuffix: string;
  communicationMode: CommunicationMode;
  logLevel: string;
  standalone: boolean;
  autoRun: boolean;
  reportingId: string;
  reportPublishUrl: string;
  macAddress: string;
  globalSla: number | null;
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  rawErrors?: unknown[];
}

export interface ExecutionResult {
  id: string;
  method: string;
  mode: CommunicationMode;
  status: ResultStatus;
  durationMs: number;
  timestamp: number;
  params?: unknown;
  response?: unknown;
  error?: unknown;
  schemaValidation?: ValidationResult;
  sla?: { expectedMs: number | null; actualMs: number; status: 'passed' | 'failed' };
  exampleName?: string;
  /** Event methods produce two rows per case: the subscribe ({listen: true}) and the unsubscribe ({listen: false}) call. */
  eventAction?: 'subscribe' | 'unsubscribe';
  /** Sample result of the OpenRPC example this case was run with. */
  exampleResponse?: unknown;
  /** OpenRPC summary (or description) of the method. Filled in for suite runs. */
  description?: string;
  /** Readable description of the OpenRPC result schema (what a valid response looks like). Filled in for suite runs. */
  expectedFormat?: string;
  /** Plain-English explanation of a failure (what mismatched, expected vs received). Filled in when a report is built. */
  failureReason?: string[];
}

export interface OpenRpcExampleParam {
  name: string;
  value: unknown;
}
export interface OpenRpcExample {
  name: string;
  params?: OpenRpcExampleParam[];
  result?: unknown;
}
export interface OpenRpcParam {
  name: string;
  required?: boolean;
  description?: string;
  schema?: any;
}
export interface OpenRpcMethod {
  name: string;
  module: string;
  method: string;
  summary?: string;
  description?: string;
  params: OpenRpcParam[];
  examples: OpenRpcExample[];
  resultSchema?: any;
  raw: any;
}
export interface OpenRpcDocument {
  openrpc?: string;
  info?: any;
  methods: any[];
  components?: any;
  [key: string]: any;
}

export interface OpenRpcParameterSet {
  name: string;
  params: Record<string, unknown>;
  source: 'example' | 'default';
  usable: boolean;
  reason?: string;
  /** Sample result of the OpenRPC example these params come from (undefined when none). */
  exampleResult?: unknown;
}

export interface CertificationRunOptions {
  mode: CommunicationMode;
  /** Optional module filter (e.g. ['Device']). Omitted = every module. */
  modules?: string[];
  /** Optional human-readable scope used in the report title (e.g. 'All modules'). Defaults to the module list. */
  scopeLabel?: string;
  exceptionMethods?: Array<{ method: string; param?: Record<string, unknown> }>;
  slaValidation?: boolean;
  globalSla?: number | null;
}

export interface SuiteSummary {
  total: number;
  passed: number;
  failed: number;
  durationMs: number;
}
export interface CertificationSuiteReport {
  id: string;
  title: string;
  mode: CommunicationMode;
  startedAt: number;
  endedAt: number;
  summary: SuiteSummary;
  /** True when the run was stopped before every method in scope was tested; the report is partial. */
  interrupted?: boolean;
  /** Methods in scope that were not (fully) tested because the run was stopped. */
  methodsNotRun?: number;
  results: ExecutionResult[];
  stats: {
    suites: number;
    tests: number;
    passes: number;
    failures: number;
    start: string;
    end: string;
    duration: number;
  };
  suites: Array<{
    uuid: string;
    title: string;
    tests: any[];
    suites: any[];
    root: boolean;
    fullFile: string;
    file: string;
    passes: string[];
    failures: string[];
    duration: number;
  }>;
}

export type ReportFormat = 'json' | 'html' | 'xlsx';

export interface ReportPublishResult {
  ok: boolean;
  format: ReportFormat;
  fileName: string;
  url?: string;
  status?: number;
  message: string;
}

export interface EventRecord {
  event: string;
  listenerId: number | string;
  value: unknown;
  timestamp: number;
  schemaValidation?: ValidationResult;
}
export interface LifecycleRecord {
  event: string;
  value?: unknown;
  timestamp: number;
  source: 'firebolt' | 'browser' | 'firebolt-certification';
}
export interface FireboltCertificationCommand {
  task?: string;
  command?: string;
  action?: string;
  context?: any;
  params?: any;
  payload?: any;
  standalone?: boolean;
  responseTimeout?: number;
}
