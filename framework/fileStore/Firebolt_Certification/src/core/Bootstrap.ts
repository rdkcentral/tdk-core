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
import { logger } from '../utils/Logger';

export async function initializeFromFireboltParameters(): Promise<void> {
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
    if (query?.task)
      window.setTimeout(() => {
        void commandRouter.handle(query);
      }, 1000);
  } catch (error) {
    logger.warn('Parameters.initialization unavailable; using URL/default runtime config', error);
  }
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
