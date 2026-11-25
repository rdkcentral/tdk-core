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
 * @file Vite build/dev configuration; also starts the Python report server alongside `npm run dev` and `npm run preview`.
 */

import { defineConfig, type Plugin, type PreviewServer, type ViteDevServer } from 'vite';
import preact from '@preact/preset-vite';
import { spawn, type ChildProcess } from 'node:child_process';
import { fileURLToPath } from 'node:url';

// Starts the report server (firebolt_certification_report/http_server.py) alongside `npm run dev` and `npm run preview`.
// Set FIREBOLT_CERTIFICATION_REPORT_SERVER=0 to skip it; the port comes from FIREBOLT_CERTIFICATION_REPORT_PORT (default 8090).
function reportServer(): Plugin {
  let child: ChildProcess | undefined;
  const start = (server: ViteDevServer | PreviewServer) => {
    if (process.env.FIREBOLT_CERTIFICATION_REPORT_SERVER === '0' || child) return;
    const script = fileURLToPath(new URL('./firebolt_certification_report/http_server.py', import.meta.url));
    child = spawn(process.env.PYTHON || 'python3', [script], { stdio: 'inherit' });
    child.on('error', (err) => server.config.logger.warn(`[report-server] failed to start: ${err.message}`));
    const stop = () => {
      child?.kill();
      child = undefined;
    };
    server.httpServer?.on('close', stop);
    process.on('exit', stop);
  };
  return {
    name: 'firebolt-certification-report-server',
    apply: 'serve',
    configureServer: start,
    configurePreviewServer: start
  };
}

export default defineConfig({
  plugins: [preact(), reportServer()],
  base: './',
  build: {
    target: 'es2017',
    cssCodeSplit: false,
    sourcemap: true,
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  },
  server: {
    host: '0.0.0.0'
  }
});
