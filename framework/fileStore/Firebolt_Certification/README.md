# Firebolt Certification

A Firebolt API certification app for RDK devices. It invokes Firebolt APIs on the device, validates every response against the Firebolt OpenRPC schema, and produces JSON, HTML and Excel certification reports.

The app is built with **Preact**, **TypeScript** and **Vite**, runs in WPEWebKit, and is designed for remote-control (RCU) navigation.

---

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Scripts](#scripts)
- [Configuration](#configuration)
- [Using the app](#using-the-app)
- [Reports](#reports)
- [Building and deploying](#building-and-deploying)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## Features

- **API testing:** browse Firebolt APIs by module, invoke them with parameters taken from the OpenRPC examples, and inspect the response.
- **Event testing:** subscribe to and unsubscribe from Firebolt events, and validate notification payloads against their schemas.
- **Validation suites:** run all modules or a single module and validate each response against its OpenRPC result schema (AJV). Runs can also start automatically on launch (`autoRun=true`).
- **Two communication modes:** **Transport** (the app's own JSON-RPC 2.0 client over WebSocket) or **SDK** (the device's `FireboltServiceManager`).
- **Reports:** JSON, self-contained interactive HTML, and Excel (`.xlsx`), with readable failure explanations, all publishable to a report server.
- **Built for TV devices:** full spatial navigation with the remote, no on-device text entry, and dark and light themes.

---

## Requirements

| Tool | Version | Purpose |
| --- | --- | --- |
| [Node.js](https://nodejs.org/) | 24+ (LTS recommended) | Build, dev server and tests |
| npm | 11+ | Dependency management |
| [Python](https://www.python.org/) | 3.12+ | Report server (standard library only) |

`npm install` needs internet access, because the Firebolt runner dependency is downloaded from GitHub.

Only the built static files in `dist/` run on the device. Node.js, npm and Python are needed only on the build and host machine.

### Dependencies

| Package | Version | Type | Purpose |
| --- | --- | --- | --- |
| `preact` | 10.29.8 | runtime | UI framework |
| `ajv` | 8.20.0 | runtime | JSON Schema validation |
| `firebolt-generator` | commit `d93b830` | runtime | Upstream certification runner and SDK argument metadata ([rdkcentral/firebolt-js-client](https://github.com/rdkcentral/firebolt-js-client)) |
| `vite` | 6.4.3 | dev | Dev server and bundler |
| `@preact/preset-vite` | 2.10.6 | dev | Preact integration for Vite |
| `typescript` | 7.0.2 | dev | Type checking |
| `vitest` | 2.1.9 | dev | Unit tests |

---

## Quick start

```bash
# 1. Install dependencies (also prepares the Firebolt runner in .firebolt-sdk/)
npm install

# 2. Start the app and the report server
npm run dev
```

| Service | Default URL |
| --- | --- |
| App (Vite dev server) | `http://localhost:5173/` |
| Report server | `http://localhost:8090/` |

Open the app with `standalone=true` (for example `http://localhost:5173/?standalone=true`). Both services listen on all network interfaces, so a device on the same network can open `http://<your-machine-ip>:5173/?standalone=true`. If a port is busy, the next free port is used and printed in the terminal. Press `Ctrl+C` to stop both.

---

## Scripts

| Command | Description |
| --- | --- |
| `npm install` | Install dependencies and generate `.firebolt-sdk/` |
| `npm run dev` | Start the dev server with live reload, plus the report server |
| `npm run build` | Type-check and build the production app into `dist/` |
| `npm run build:clean` | Clean install (`npm ci`), build, then remove `node_modules/` |
| `npm run preview` | Serve the production build from `dist/`, plus the report server |
| `npm run typecheck` | Run the TypeScript type check |
| `npm test` | Run the unit tests (Vitest) |
| `npm run generate:sdk` | Regenerate `.firebolt-sdk/` (runs automatically after install) |

---

## Configuration

### Launch parameters

The app is configured through URL query parameters (see [runtime.ts](src/config/runtime.ts)).

| Parameter | Default | Description |
| --- | --- | --- |
| `__firebolt_endpoint` | `ws://127.0.0.1:3473` | Firebolt gateway WebSocket. Used as given. |
| `communicationMode` | `Transport` | `Transport` or `SDK` |
| `version` | latest (`M155`) | TDK monthly tag of the Firebolt schema validator spec to load, e.g. `M155`. Can be given alone; the Firebolt version is then looked up in `specs/index.json` |
| `fireboltVersion` | latest (`9.0.0`) | Firebolt version of the spec to load, e.g. `9.0.0`. Can be given alone; the newest matching TDK tag is then looked up in `specs/index.json` |
| `excludeMethods` | — | Comma-separated methods to exclude; wildcards allowed (`Device.version,Network.*`) |
| `reportPublishUrl` | `DEFAULT_REPORT_PUBLISH_URL` | Report upload endpoint (see [Publishing](#publishing)) |
| `standalone` | `false` | **Set to `true`** to run as the on-screen validation app, without any external test server |
| `autoRun` | `false` | On launch, run the suite for all modules and publish the reports (see [Automatic run](#automatic-run)) |


Example:

```text
http://<host>:5173/?standalone=true&__firebolt_endpoint=ws://127.0.0.1:3473&reportPublishUrl=http://<host>:8090/
```

### Source defaults

[runtime.ts](src/config/runtime.ts) also defines:

- `DEFAULT_REPORT_PUBLISH_URL`: the report server used when `reportPublishUrl` is not supplied. **Set this to your own report server.**
- `EXCLUDED_METHODS`: methods that are always excluded from the UI and from suite runs. By default this is `Lifecycle2.close`, because closing the app would end the session.
- `CONNECTIVITY_PROBE_METHOD`: the parameterless API called once at launch to check the Firebolt connection (any non-error reply counts as connected).

### Report server environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `FIREBOLT_CERTIFICATION_REPORT_PORT` | `8090` | Report server port |
| `FIREBOLT_CERTIFICATION_REPORT_PORT_TRIES` | `20` | Number of ports to try if the port is busy |
| `FIREBOLT_CERTIFICATION_REPORT_SERVER` | — | Set to `0` to run `npm run dev` or `npm run preview` without the report server |

---

## Using the app

| Page | Purpose |
| --- | --- |
| **APIs** | Select a module and an API, choose a parameter set and a mode, invoke it and view the response. |
| **Events** | Register and clear event listeners and review received notifications. |
| **Suites** | Run validation for all modules or one module, in Transport or SDK mode. Results are paginated for device performance. |
| **Reports** | Browse past runs, then generate and publish JSON, HTML or Excel reports. |

### Remote control

| Key | Action |
| --- | --- |
| Arrow keys | Move focus |
| Enter / OK | Activate the focused control |
| Back / Escape / Backspace | Return focus to the navigation menu |
| Page Up / Page Down | Scroll the active list or result |

Parameters always come from the OpenRPC spec: first the method's examples, then the schema `default`, `examples[0]` and `example`. If a required parameter has no value, invocation is disabled rather than asking for on-device typing.

---

## Reports

### Formats

| Format | Contents |
| --- | --- |
| **JSON** | Run metadata (`id`, `title`, `mode`, `version`, start and end times), `summary` (`totalTestCases`, `passed`, `failed`, `validatedApis`, `validatedEvents`, `durationMs`), and per-module `modules[]` with `totalTestCases`, `passed`, `failed`, `validatedApis`, `validatedEvents`, `passRate` and `results` (`slNo`, `method`, `description`, `status`, `log`). Mocha-style `stats` and `suites` blocks are kept for downstream tools. |
| **HTML** | A self-contained, interactive page with module and status filters, search, expandable log cells, Validated APIs / Validated Events counts, and a Passed/Failed success-rate donut chart. |
| **Excel** | A Summary sheet (per-module Total test cases, Passed, Failed, Validated APIs, Validated events, Pass rate) and a Success rate doughnut chart of the Passed/Failed totals to the right of the tables, plus one sheet per module (Sl No, Method, Description, Status, Log). |

Each result's log includes the method, parameters, expected response format, actual response, failure reason (for failures) and the sample response from the spec. Validated API and event counts are distinct methods: an event counts once even though it has Subscribe and Unsubscribe rows. Every report names the **Firebolt Schema Validator** and records the **Version** (TDK monthly tag) used for the run.

Report files are named `<reportingId | appId>-refAppExecReport-<UTC timestamp>.<json|html|xlsx>`.

### Report server

[http_server.py](firebolt_certification_report/http_server.py) starts automatically with `npm run dev` and `npm run preview`. To run it on its own:

```bash
python3 firebolt_certification_report/http_server.py
```

| Endpoint | Description |
| --- | --- |
| `GET /` | Lists all received reports |
| `POST /<file name>` | Saves a report into `reports/json/`, `reports/html/` or `reports/xlsx/` |
| `GET /reports/<format>/<file name>` | Downloads or views a report |
| `GET /health` | Health check, used by the app to find the server if it moved port |

### Publishing

Reports are sent with `POST` to `reportPublishUrl`. The URL may contain the placeholders `{filename}`, `{format}` and `{reportId}`. If the URL has no placeholder or query string and ends with `/`, the file name is appended. The request carries the headers `x-firebolt-certification-report-name` and `x-firebolt-certification-report-format`.

### Automatic run

Add `autoRun=true` to the launch URL to certify a device without any remote-control input. The app opens the Suites page, waits for the OpenRPC spec to load and the Firebolt connection check to finish, then runs **all modules** once in the configured `communicationMode` and publishes the JSON, HTML and Excel reports to `reportPublishUrl`. Progress and results are shown on screen as in a manual run.

```text
https://<host>/firebolt-certification/index.html?standalone=true&autoRun=true&reportPublishUrl=http://<report-host>:8090/
```

The run happens once per launch; relaunch the app to run it again.

---

## Building and deploying

```bash
npm install
npm run typecheck
npm test
npm run build
```

The deployable app is written to `dist/`. Host its contents on any static web server; the device needs nothing else.

Device launch example:

```text
https://<host>/firebolt-certification/index.html
  ?standalone=true
  &appId=firebolt-certification
  &__firebolt_endpoint=ws://127.0.0.1:3473
  &reportPublishUrl=http://<report-host>:8090/
```

| Change | Action |
| --- | --- |
| Fresh clone, or dependencies changed | `npm install` |
| App source changed | `npm run build` |
| OpenRPC spec in `public/specs/` edited on the host | Relaunch the app (the spec is fetched at launch) |
| Device SDK changed | Relaunch the app on the device |

### Firebolt runner (postinstall)

`npm install` runs [generate-firebolt-sdk.mjs](scripts/generate-firebolt-sdk.mjs). It copies the unchanged upstream certification runner and SDK argument metadata from a pinned `firebolt-js-client` archive into `.firebolt-sdk/`. No SDK client is generated or bundled. In SDK mode the device must provide `window.FireboltServiceManager`. If you install with `--ignore-scripts`, run `npm run generate:sdk` manually.

---

## Architecture

```text
                    RDK App Manager → WPEWebKit
                              │
                  Preact UI (RCU navigation)
                              │
                       CertificationEngine
                              │
              ┌───────────────────────────────────┼───────────────────────────┐
              │                                   │                           │
        FireboltAdapter                 OpenRpcService + AJV            ReportBuilder
     Transport │ SDK                    (schema validation)          JSON / HTML / Excel
              │                                                           │
   Firebolt gateway (:3473)                                        Report server
```

### Firebolt transport

- The app uses its own JSON-RPC 2.0 client ([JsonRpcClient.ts](src/firebolt/JsonRpcClient.ts)). It connects to the endpoint as given, with the `jsonrpc` WebSocket sub-protocol.
- The endpoint is resolved in [index.html](index.html), in this order: the `__firebolt_endpoint` parameter, then an endpoint injected by the launcher, then `ws://127.0.0.1:3473`.
- Events are subscribed with `{"listen": true}` and unsubscribed with `{"listen": false}`. Both must reply `result: null`; any other reply is reported as a failure. Notifications are validated against the event's OpenRPC `result` schema.

### SDK mode

[SdkAdapter.ts](src/firebolt/SdkAdapter.ts) waits for the device's `window.FireboltServiceManager`, obtains the client and calls its API wrappers through the upstream `FireboltCertificationRunner`. A missing manager or API wrapper (`SdkMethodNotAvailable`) fails the call; there is no fallback to Transport.

### OpenRPC specification

The spec is named by Firebolt version and TDK monthly tag as [public/specs/firebolt_schema_validator_&lt;fireboltVersion&gt;_&lt;releaseVersion&gt;.json](public/specs/firebolt_schema_validator_9.0.0_M155.json), and its `info` block records both (`version` is the TDK monthly tag, e.g. `M155`; `firebolt-version` is the Firebolt version, e.g. `9.0.0`). It is fetched from the host at launch (`cache: 'no-store'`).

- With neither `version` nor `fireboltVersion`, the latest spec is loaded; if the fetch fails, the copy bundled at build time is used.
- With both, that file is loaded directly. With only one, the first matching entry in [public/specs/index.json](public/specs/index.json) supplies the other.
- When a version is requested, a missing file, a missing index entry or an unreadable index stops the load with an error; the bundled copy is never used in its place.

To add a spec, add the file, list it in `index.json` (newest first) and bump `LATEST_RELEASE_VERSION` (and `FIREBOLT_VERSION` if it changed) in [OpenRpcService.ts](src/schema/OpenRpcService.ts).

---

## Project structure

```text
├── index.html                      # Entry page; resolves the Firebolt endpoint
├── public/specs/                   # Versioned Firebolt OpenRPC specs
├── scripts/                        # postinstall: Firebolt runner setup
├── firebolt_certification_report/  # Python report server and received reports
└── src/
    ├── app/          # Pages and main UI (App.tsx)
    ├── components/   # Shared UI components and spatial navigation
    ├── config/       # Launch parameters and defaults
    ├── core/         # CertificationEngine, EventBus, Bootstrap, CommandRouter (Pub/Sub commands)
    ├── firebolt/     # JSON-RPC client, Transport/SDK adapters, event manager
    ├── schema/       # OpenRPC loading and AJV validation
    ├── reports/      # Report building, failure explanations, JSON/HTML/Excel export
    ├── pubsub/       # Pub/Sub client (not used in standalone mode)
    ├── lifecycle/    # Lifecycle handling (not used in standalone mode)
    ├── providers/    # Provider handling (not used in standalone mode)
    ├── extensions/   # Extension registry for vendor hooks
    ├── utils/        # Logging and helpers
    ├── styles/       # Global CSS and theme tokens
    └── test/         # Vitest unit tests
```

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Editor shows import errors | Run `npm install`, then restart the TypeScript server. |
| `npm install` fails | Check the Node.js version and internet access (one dependency comes from GitHub). |
| `[report-server] failed to start` | Install Python 3, or set `PYTHON` to your interpreter. |
| App opens on port 5174 instead of 5173 | Port 5173 is busy; use the URL printed in the terminal. |
| Device cannot open the app | Use the machine's IP address rather than `localhost`, and allow ports 5173 and 8090 through the firewall. |
| Top bar shows a red "Firebolt_Certification_Framework" status | Add `standalone=true` to the launch URL. |
| Reports are not received | Set `reportPublishUrl=http://<machine-ip>:8090/`, or update `DEFAULT_REPORT_PUBLISH_URL`. |
| `SdkMethodNotAvailable` | The device SDK does not provide that API. Use Transport mode or update the device SDK. |
