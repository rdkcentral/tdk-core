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
 * @file Runtime configuration: reads launch (URL) parameters and defaults, such as mode, endpoints, report publish
 * URL, log level and excluded methods, into runtimeConfig.
 */

import type { CommunicationMode, RuntimeConfig } from '../types';

// Default report publish endpoint used when no reportPublishUrl launch parameter is supplied
// in the app URL. Edit this constant to point at your report upload service without needing
// to pass the URL as a launch parameter. JSON, HTML and Excel reports are all sent here.
export const DEFAULT_REPORT_PUBLISH_URL = '';

// Method called once at launch to check the Firebolt connection (top bar "Firebolt Endpoint" label).
// It must take no parameters. Any non-error reply counts as connected; the reply is not schema-validated.
export const CONNECTIVITY_PROBE_METHOD = 'Device.deviceClass';

/**
 * Methods excluded from the UI and from every suite run. Edit this list instead of the OpenRPC JSON.
 * Entries are case-insensitive full names ("Device.version"); '*' is a wildcard ("Network.*", "*.onChanged").
 * The launch parameter ?excludeMethods=A.b,C.* adds to this list.
 */
export const EXCLUDED_METHODS: string[] = [
  // 'Device.version',
  // 'Network.*',
  'Lifecycle2.close'
];

const query = new URLSearchParams(window.location.search);

export function getConfiguredExclusions(): string[] {
  const fromUrl = (query.get('excludeMethods') || '')
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
  return [...EXCLUDED_METHODS, ...fromUrl];
}

export function buildExclusionMatcher(patterns: string[]): (methodName: string) => boolean {
  const regexes = patterns
    .map((p) => p.trim())
    .filter(Boolean)
    .map(
      (p) =>
        new RegExp(
          `^${p
            .split('*')
            .map((s) => s.replace(/[.+?^${}()|[\]\\]/g, '\\$&'))
            .join('.*')}$`,
          'i'
        )
    );
  return (name) => regexes.some((r) => r.test(name));
}
function q(name: string, fallback = ''): string {
  return query.get(name) ?? fallback;
}
function qb(name: string, fallback = false): boolean {
  const value = q(name, String(fallback)).toLowerCase();
  return ['1', 'true', 'yes', 'y', 'on'].includes(value);
}
function qn(name: string): number | null {
  const value = q(name, '');
  if (!value) return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}
function mode(): CommunicationMode {
  return q('communicationMode', q('mode', 'Transport')).toLowerCase() === 'sdk' ? 'SDK' : 'Transport';
}

export const runtimeConfig: RuntimeConfig = {
  appId: q('appId', 'firebolt-certification'),
  appType: q('appType', ''),
  platform: q('platform', 'default'),
  fireboltEndpoint: q('__firebolt_endpoint', 'ws://127.0.0.1:3473'),
  pubSubUrl: q('pubSubUrl', q('pubsub_url', 'ws://127.0.0.1:8080')),
  pubSubUuid: q('pubsub_uuid', q('macaddress', 'DEFAULT_TOPIC').replace(/:/g, '')),
  pubSubSubscribeSuffix: q('pubSubSubscribeSuffix', q('pubsub_subscribe_suffix', '_FCS')),
  pubSubPublishSuffix: q('pubSubPublishSuffix', q('pubsub_publish_suffix', '_FCA')),
  communicationMode: mode(),
  specVersion: q('specVersion', ''),
  logLevel: q('logLevel', 'INFO').toUpperCase(),
  standalone: qb('standalone', false),
  // Runs the suite for all modules on launch and publishes the reports (Suites page "Run" without a key press).
  autoRun: qb('autoRun', false),
  reportingId: q('reportingId', ''),
  reportPublishUrl: q('reportPublishUrl', q('report_publish_url', DEFAULT_REPORT_PUBLISH_URL)),
  macAddress: q('macaddress', ''),
  globalSla: qn('globalSLA')
};

export function applyRuntimeParams(params: Record<string, any>): void {
  if (!params) return;
  if (params.appId) runtimeConfig.appId = String(params.appId);
  if (params.appType) runtimeConfig.appType = String(params.appType).toLowerCase();
  if (params.pubSubUrl) runtimeConfig.pubSubUrl = String(params.pubSubUrl);
  if (params.macaddress) {
    runtimeConfig.macAddress = String(params.macaddress);
    if (!query.get('pubsub_uuid')) runtimeConfig.pubSubUuid = String(params.macaddress).replace(/:/g, '');
  }
  if (params.pubSubSubscribeSuffix) runtimeConfig.pubSubSubscribeSuffix = String(params.pubSubSubscribeSuffix);
  if (params.pubSubPublishSuffix) runtimeConfig.pubSubPublishSuffix = String(params.pubSubPublishSuffix);
  if (params.reportPublishUrl) runtimeConfig.reportPublishUrl = String(params.reportPublishUrl);
}
