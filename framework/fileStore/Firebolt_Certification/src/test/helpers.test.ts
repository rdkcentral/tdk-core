import { describe, expect, it } from 'vitest';
import { normalizeError } from '../utils/helpers';

describe('Firebolt Certification helpers', () => {
  it('normalizes string errors', () =>
    expect(normalizeError('bad')).toEqual({ code: 'FireboltCertificationError', message: 'bad' }));
});
