import { logger } from '../utils/Logger';
import { extensionRegistry } from '../extensions/ExtensionRegistry';

// Modules FCS may still send setApiResponse for; their values are acknowledged but not used because providers are not registered.
const PROVIDER_MODULES = new Set(['keyboard', 'pinchallenge', 'ackchallenge', 'userinterest', 'federateddata']);

export class ProviderManager {
  setApiResponse(apiResponse: any): string {
    const module = String(apiResponse?.module || '').toLowerCase();
    if (module === 'external') return extensionRegistry.setExternalApiResponse(apiResponse);
    return PROVIDER_MODULES.has(module) ? 'Received ApiResponse parameters' : 'Selected module provider is not available';
  }

  // Provider capabilities (Keyboard, PinChallenge, AcknowledgeChallenge, Discovery userInterest) are not part of
  // the Firebolt RDK8+ OpenRPC that Firebolt Certification certifies, so Firebolt Certification no longer registers providers.
  async register(provider: string): Promise<string> {
    logger.warn(`Provider registration requested but not supported: ${provider}`);
    return `${provider} provider is not supported: providers are not part of the Firebolt RDK8+ OpenRPC`;
  }
}
export const providerManager = new ProviderManager();
