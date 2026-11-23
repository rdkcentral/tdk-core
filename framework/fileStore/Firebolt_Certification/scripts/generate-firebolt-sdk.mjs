import { mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const upstream = dirname(require.resolve('firebolt-generator/package.json'));
const output = join(root, '.firebolt-sdk');
await mkdir(output, { recursive: true });

const shapes = {};
const specs = join(upstream, 'src', 'openrpc');
for (const file of await readdir(specs)) {
  if (!file.endsWith('.json') || file === 'shared.json') continue;
  const document = JSON.parse(await readFile(join(specs, file), 'utf8'));
  for (const method of document.methods) {
    let shape = { kind: method.params.length ? 'WithObjectParam' : 'NoParams' };
    if (/\.on[A-Z]/.test(method.name)) {
      shape = { kind: 'Subscribe' };
    } else if (method.params.length === 1) {
      const ref = method.params[0].schema?.$ref;
      const schema = ref?.startsWith('#/components/schemas/')
        ? document.components?.schemas?.[ref.slice('#/components/schemas/'.length)]
        : undefined;
      const properties = Object.entries(schema?.properties || {});
      // Match the upstream SDK's single required primitive-property wrapper convention.
      if (
        schema?.type === 'object' &&
        properties.length === 1 &&
        schema.required?.includes(properties[0][0]) &&
        ['string', 'boolean', 'number', 'integer'].includes(properties[0][1].type)
      ) {
        shape = { kind: 'WithPrimitiveWrap', parameter: properties[0][0] };
      }
    }
    shapes[method.name] = shape;
  }
}
if (!Object.keys(shapes).length) throw new Error('Upstream SDK argument metadata is empty');
await writeFile(join(output, 'method-shapes.json'), JSON.stringify(shapes, null, 2) + '\n');
const runner = await readFile(join(upstream, 'src', 'certification', 'runner.js'), 'utf8');
await writeFile(
  join(output, 'runner.js'),
  runner +
    '\nexport const runner = (typeof window !== "undefined" ? window : globalThis).FireboltCertificationRunner;\n'
);
console.log(
  'Upstream certification runner and SDK argument metadata are ready. SDK clients must be supplied by the device.'
);
