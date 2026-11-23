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
