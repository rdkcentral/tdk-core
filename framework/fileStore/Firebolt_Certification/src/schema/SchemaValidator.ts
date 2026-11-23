import Ajv from 'ajv';
import type { ValidationResult } from '../types';

export class SchemaValidator {
  private ajv = new Ajv({ allErrors: true, strict: false, allowUnionTypes: true, validateFormats: false });

  validate(value: unknown, schema: any): ValidationResult {
    if (!schema || typeof schema !== 'object') return { valid: true, errors: [] };
    try {
      const validate = this.ajv.compile(schema);
      const valid = !!validate(value);
      const rawErrors = validate.errors ? [...validate.errors] : [];
      return {
        valid,
        errors: rawErrors.map((e) => `${e.instancePath || '/'} ${e.message || 'schema validation error'}`.trim()),
        rawErrors
      };
    } catch (error) {
      return {
        valid: false,
        errors: [`Schema compilation failed: ${error instanceof Error ? error.message : String(error)}`]
      };
    }
  }

  validateError(error: unknown): ValidationResult {
    return this.validate(error, {
      type: 'object',
      required: ['code', 'message'],
      properties: {
        code: { anyOf: [{ type: 'integer' }, { type: 'string' }] },
        message: { type: 'string' },
        data: {}
      },
      additionalProperties: true
    });
  }
}
export const schemaValidator = new SchemaValidator();
