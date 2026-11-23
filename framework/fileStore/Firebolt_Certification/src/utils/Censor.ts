import censorData from '../data/censorData.json';

export function censor(methodName: string, input: any): any {
  try {
    const config = (censorData as any)[methodName.charAt(0).toUpperCase() + methodName.slice(1)];
    if (!config) return input;
    const clone = input && typeof input === 'object' ? JSON.parse(JSON.stringify(input)) : input;
    for (const field of config.field || []) {
      if (!field && typeof clone === 'string') return mask(clone);
      if (clone && typeof clone === 'object' && typeof clone[field] === 'string') clone[field] = mask(clone[field]);
    }
    return clone;
  } catch {
    return input;
  }
}
function mask(value: string): string {
  return value.length <= 4 ? '****' : value.slice(0, 2) + '*******' + value.slice(-2);
}
