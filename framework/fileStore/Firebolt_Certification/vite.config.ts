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
