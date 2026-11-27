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
 * @file AJV-based JSON schema validator used to check API responses and event payloads.
 */

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
