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
 * @file Stub for Firebolt provider handling: acknowledges provider API responses; provider registration is not supported.
 */

import { logger } from '../utils/Logger';
import { extensionRegistry } from '../extensions/ExtensionRegistry';

// Modules that may still receive setApiResponse; their values are acknowledged but not used because providers are not registered.
const PROVIDER_MODULES = new Set(['keyboard', 'pinchallenge', 'ackchallenge', 'userinterest', 'federateddata']);

export class ProviderManager {
  setApiResponse(apiResponse: any): string {
    const module = String(apiResponse?.module || '').toLowerCase();
    if (module === 'external') return extensionRegistry.setExternalApiResponse(apiResponse);
    return PROVIDER_MODULES.has(module) ? 'Received ApiResponse parameters' : 'Selected module provider is not available';
  }

  // Provider capabilities (Keyboard, PinChallenge, AcknowledgeChallenge, Discovery userInterest) are not part of
  // the Firebolt OpenRPC that Firebolt Certification certifies, so Firebolt Certification no longer registers providers.
  async register(provider: string): Promise<string> {
    logger.warn(`Provider registration requested but not supported: ${provider}`);
    return `${provider} provider is not supported: providers are not part of the Firebolt OpenRPC`;
  }
}
export const providerManager = new ProviderManager();
