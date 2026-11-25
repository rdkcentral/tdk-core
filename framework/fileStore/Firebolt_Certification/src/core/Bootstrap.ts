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
 * @file Startup helpers: applies launch parameters from Firebolt Parameters.initialization and resolves the app id.
 */

import { fireboltAdapter } from '../firebolt/FireboltAdapter';
import { applyRuntimeParams, runtimeConfig } from '../config/runtime';
import { commandRouter } from './CommandRouter';
import { openRpcService } from '../schema/OpenRpcService';
import { logger } from '../utils/Logger';
import type { FireboltCertificationCommand } from '../types';

/** Applies launch parameters and returns the launch task (if any) for the caller to dispatch once initialization is done. */
export async function initializeFromFireboltParameters(): Promise<FireboltCertificationCommand | undefined> {
  try {
    const result = await fireboltAdapter.invoke({
      method: 'Parameters.initialization',
      mode: 'Transport',
      params: [],
      timeoutMs: 8000
    });
    if (result.status !== 'PASS' || !result.response) return;
    const navigate = (result.response as any)?.discovery?.navigateTo;
    if (navigate?.action !== 'search' || navigate?.data?.query == null) return;
    let query: any = navigate.data.query;
    for (let i = 0; i < 3 && typeof query === 'string'; i++) {
      try {
        query = JSON.parse(query);
      } catch {
        break;
      }
    }
    applyRuntimeParams(query?.params || {});
    logger.info('Applied Parameters.initialization launch values', {
      appId: runtimeConfig.appId,
      pubSubUrl: runtimeConfig.pubSubUrl
    });
    return query?.task ? query : undefined;
  } catch (error) {
    logger.warn('Parameters.initialization unavailable; using URL/default runtime config', error);
  }
  return undefined;
}

/** Dispatches the launch task; must be called only after schemas/runtime are initialized. */
export async function dispatchLaunchTask(task: FireboltCertificationCommand): Promise<void> {
  // Without a method catalog a runTest would produce an empty, falsely passing report.
  if (!openRpcService.getMethods().length) {
    logger.error(`Launch task "${task.task}" not run: OpenRPC method catalog failed to load`);
    return;
  }
  await commandRouter.handle(task);
}

export async function resolveCurrentAppId(): Promise<void> {
  if (new URLSearchParams(window.location.search).get('appId')) return;
  try {
    const r = await fireboltAdapter.invoke({ method: 'Advertising.appBundleId', mode: 'Transport', params: [] });
    if (r.status === 'PASS' && typeof r.response === 'string') {
      const last = r.response.lastIndexOf('.');
      runtimeConfig.appId = last > 0 ? r.response.slice(0, last) : r.response;
    }
  } catch {
    /* optional */
  }
}
