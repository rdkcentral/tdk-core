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
 * @file Main UI: header, sidebar and the APIs, Suites, Events and Reports pages. Loads the OpenRPC spec, runs
 * certification through CertificationEngine and shows, exports and publishes reports.
 */

import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'preact/hooks';
import { Sidebar } from '../components/Sidebar';
import { StatusPill } from '../components/StatusPill';
import { Panel } from '../components/Panel';
import { Icon } from '../components/Icons';
import tdkLogo from '../assets/tdk-logo-report.png';
import { installSpatialNavigation, focusSelector } from '../components/SpatialNavigation';
import { certificationEngine, validateSubscriptionReply } from '../core/CertificationEngine';
import { schemaValidator } from '../schema/SchemaValidator';
import { eventBus } from '../core/EventBus';
import { pubSubClient } from '../pubsub/PubSubClient';
import { runtimeConfig } from '../config/runtime';
import { openRpcService } from '../schema/OpenRpcService';
import { eventManager } from '../firebolt/EventManager';
import { dispatchLaunchTask, initializeFromFireboltParameters, resolveCurrentAppId } from '../core/Bootstrap';
import { isEventMethod, safeStringify } from '../utils/helpers';
import { groupMethodsByModule, methodKey, type ModuleGroup } from '../utils/methodGroups';
import { publishReport, resolveReportPublishUrl, resolveAutomationContext } from '../reports/ReportExporter';
import { explainFailure } from '../reports/failureExplanation';
import { describeSchema } from '../reports/schemaSummary';
import { ReportFrame, suppressTransitions, type UiTheme } from '../components/ReportFrame';
import type {
  CertificationSuiteReport,
  CommunicationMode,
  ConnectionState,
  EventRecord,
  ExecutionResult,
  OpenRpcMethod,
  OpenRpcParameterSet,
  ReportPublishResult
} from '../types';

type Page = 'apis' | 'suites' | 'reports' | 'events';
type SchemaState = 'loading' | 'loaded' | 'error';
const MODE_OPTIONS: CommunicationMode[] = ['SDK', 'Transport'];
const ALL_MODULES = 'All modules';
const NO_METHODS: OpenRpcMethod[] = [];
// Module-level so leaving and re-opening the Suites page does not start the automatic run again.
let autoRunStarted = false;
// Read-only boxes the RCU can focus; Up/Down scrolls their content before moving on.
const READABLE_BOX = { 'data-focusable': 'true', 'data-scroll-region': 'true', tabIndex: 0 } as const;

export function App() {
  const [page, setPage] = useState<Page>(runtimeConfig.autoRun ? 'suites' : 'apis');
  // Every launch starts in the light theme; the header toggle only changes the current session.
  const [theme, setTheme] = useState<'dark' | 'light'>('light');
  const [pubSubState, setPubSubState] = useState<ConnectionState>(
    runtimeConfig.standalone ? 'disabled' : 'disconnected'
  );
  const [fireboltState, setFireboltState] = useState<ConnectionState>('connecting');
  const [fireboltError, setFireboltError] = useState('');
  const [schemaState, setSchemaState] = useState<SchemaState>('loading');
  const [lastResult, setLastResult] = useState<ExecutionResult | null>(null);
  const [methods, setMethods] = useState<OpenRpcMethod[]>([]);
  const apiMethods = useMemo(() => methods.filter((m) => !isEventMethod(m)), [methods]);

  useEffect(() => installSpatialNavigation(), []);
  useLayoutEffect(() => suppressTransitions(document.documentElement), [theme]);
  useEffect(() => {
    const offState = eventBus.on<ConnectionState>('pubsub-state', setPubSubState);
    const offResult = eventBus.on<ExecutionResult>('execution', setLastResult);
    void (async () => {
      const launchTask = await initializeFromFireboltParameters();
      // standalone mode runs sanity testing locally and skips the Pub/Sub connection
      // and the live appId lookup used only to correlate Pub/Sub topics.
      if (runtimeConfig.standalone) {
        setPubSubState('disabled');
      } else {
        await resolveCurrentAppId();
        pubSubClient.connect();
      }
      await certificationEngine.initializeSchemas();
      const loaded = openRpcService.getMethods();
      setMethods(loaded);
      setSchemaState(loaded.length ? 'loaded' : 'error');
      try {
        const probe = await certificationEngine.probe();
        setFireboltState(probe.status === 'PASS' ? 'connected' : 'error');
        setFireboltError(
          probe.status === 'PASS' ? '' : errorReason(probe.error) || `Probe ${probe.status.toLowerCase()}`
        );
      } catch (err) {
        setFireboltState('error');
        setFireboltError(errorReason(err) || 'Unknown error');
      }
      if (launchTask) await dispatchLaunchTask(launchTask);
      // Provider registration is intentionally not started from the UI.
      // Legacy provider commands remain in CommandRouter for backward compatibility.
    })();
    return () => {
      offState();
      offResult();
      pubSubClient.close();
    };
  }, []);

  return (
    <div class={`tv-shell${theme === 'light' ? ' theme-light' : ''}`}>
      <Header
        firebolt={fireboltState}
        fireboltError={fireboltError}
        fcs={pubSubState}
        theme={theme}
        onToggleTheme={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}
      />
      <div class="app-body">
        <Sidebar active={page} onSelect={(p) => setPage(p as Page)} />
        <main class="main-content">
          {page === 'apis' && <ApisPage methods={apiMethods} lastResult={lastResult} schema={schemaState} />}
          {page === 'suites' && (
            <SuitesPage
              methods={methods}
              schema={schemaState}
              theme={theme}
              onOpenReports={() => setPage('reports')}
              autoRun={runtimeConfig.autoRun && fireboltState !== 'connecting'}
            />
          )}
          {page === 'reports' && <Reports theme={theme} />}
          {page === 'events' && <Events methods={methods} schema={schemaState} />}
        </main>
      </div>
    </div>
  );
}

function fireboltEndpointLabel(state: ConnectionState, error: string): string {
  if (state === 'connected') return 'Firebolt Endpoint Connected';
  if (state === 'connecting') return 'Connecting to Firebolt Endpoint…';
  if (state === 'error') return `Firebolt Endpoint ${shortErrorReason(error)}`;
  return `Firebolt Endpoint ${pretty(state)}`;
}

function shortErrorReason(error: string): string {
  if (!error) return 'Error';
  if (/time ?d? ?out/i.test(error)) return 'Timeout';
  if (/not (available|found|supported)|unavailable|undefined|no transport/i.test(error)) return 'Unavailable';
  if (/refused|closed|disconnect|network|websocket/i.test(error)) return 'Unreachable';
  return 'Error';
}

function errorReason(err: unknown): string {
  if (err == null) return '';
  if (typeof err === 'string') return err;
  if (err instanceof Error) return err.message;
  if (typeof err === 'object') {
    const e = err as { message?: unknown; code?: unknown };
    if (typeof e.message === 'string' && e.message)
      return e.code != null ? `${e.message} (${String(e.code)})` : e.message;
    try {
      return JSON.stringify(err);
    } catch {
      return String(err);
    }
  }
  return String(err);
}

function Header({
  firebolt,
  fireboltError,
  fcs,
  theme,
  onToggleTheme
}: {
  firebolt: ConnectionState;
  fireboltError: string;
  fcs: ConnectionState;
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
}) {
  return (
    <header class="topbar">
      <div class="brand">
        <img
          class="brand-logo"
          src={tdkLogo}
          alt=""
          onError={(e: any) => {
            e.currentTarget.style.display = 'none';
          }}
        />
        <strong>Firebolt Certification</strong>
      </div>
      <div class="top-status">
        <StatusPill
          label={fireboltEndpointLabel(firebolt, fireboltError)}
          title={
            firebolt === 'error'
              ? `Firebolt endpoint error: ${fireboltError || 'Unknown error'}`
              : fireboltEndpointLabel(firebolt, fireboltError)
          }
          status={firebolt === 'connected' ? 'ok' : firebolt === 'connecting' ? 'warn' : 'bad'}
        />
        {!runtimeConfig.standalone && (
          <StatusPill
            label={`Firebolt_Certification_Framework  ${pretty(fcs)}`}
            status={fcs === 'connected' ? 'ok' : fcs === 'connecting' ? 'warn' : 'bad'}
          />
        )}
        {!runtimeConfig.standalone && (
          <span class="device-label">
            {runtimeConfig.platform} &nbsp;|&nbsp; {runtimeConfig.appId}
          </span>
        )}
        <button
          data-focusable="true"
          class="theme-toggle"
          title={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
          onClick={onToggleTheme}
        >
          <Icon name={theme === 'dark' ? 'sun' : 'moon'} />
        </button>
      </div>
    </header>
  );
}

function ChoiceButtons<T extends string>({
  values,
  value,
  onChange,
  className = ''
}: {
  values: T[];
  value: T;
  onChange: (value: T) => void;
  className?: string;
}) {
  return (
    <div class={`choice-buttons ${className}`}>
      {values.map((item) => (
        <button
          key={item}
          data-focusable="true"
          class={value === item ? 'choice active' : 'choice'}
          onClick={() => onChange(item)}
        >
          {item}
        </button>
      ))}
    </div>
  );
}

function ApisPage({
  methods,
  lastResult,
  schema
}: {
  methods: OpenRpcMethod[];
  lastResult: ExecutionResult | null;
  schema: SchemaState;
}) {
  const [mode, setMode] = useState<CommunicationMode>(runtimeConfig.communicationMode);
  const groups = useMemo(() => groupMethodsByModule(methods), [methods]);
  const [moduleName, setModuleName] = useState('');
  const moduleMethods = useMemo(
    () => groups.find((g) => g.module === moduleName)?.methods || NO_METHODS,
    [groups, moduleName]
  );
  const [selected, setSelected] = useState('');
  const current = moduleMethods.find((m) => methodKey(m) === selected) || moduleMethods[0];
  const currentKey = current ? methodKey(current) : '';
  const [parameterIndex, setParameterIndex] = useState(0);
  const [result, setResult] = useState<ExecutionResult | null>(null);

  // Drop stale selections when OpenRPC (re)loads; reset the API selection only when the module changes.
  useEffect(() => {
    if (moduleName && !groups.some((g) => g.module === moduleName)) setModuleName('');
  }, [groups, moduleName]);
  useEffect(() => {
    setSelected(moduleMethods[0] ? methodKey(moduleMethods[0]) : '');
  }, [moduleName]);
  useEffect(() => {
    if (selected && !moduleMethods.some((m) => methodKey(m) === selected))
      setSelected(moduleMethods[0] ? methodKey(moduleMethods[0]) : '');
  }, [moduleMethods, selected]);
  useEffect(() => {
    setParameterIndex(0);
    setResult(null);
  }, [currentKey]);
  useEffect(() => {
    if (current && lastResult?.method === current.name) setResult(lastResult);
  }, [lastResult, currentKey]);

  const parameterSets: OpenRpcParameterSet[] = current ? openRpcService.getParameterSets(current) : [];
  const parameterSet = parameterSets[Math.min(parameterIndex, Math.max(0, parameterSets.length - 1))];

  const isEvent = !!current && isEventMethod(current.raw);
  const expectedResponse = !current
    ? ''
    : isEvent
      ? 'null'
      : (current.resultSchema ? describeSchema(current.resultSchema) : '') || 'No result schema defined in OpenRPC.';
  const sampleResponse = isEvent
    ? null
    : result?.exampleResponse !== undefined && result.exampleResponse !== null
      ? result.exampleResponse
      : parameterSet?.exampleResult;
  const failureReason =
    result?.status === 'FAIL' ? (result.failureReason?.length ? result.failureReason : explainFailure(result)) : [];

  async function invoke() {
    if (!current || !parameterSet?.usable) return;
    setResult(await certificationEngine.invoke(current.name, parameterSet.params, mode, 10000, true));
  }
  function stepParameter(delta: number) {
    if (!parameterSets.length) return;
    setParameterIndex((parameterIndex + delta + parameterSets.length) % parameterSets.length);
    setResult(null);
  }

  function openModule(mod: string) {
    setModuleName(mod);
    focusSelector('.method-list .selection-item.active');
  }
  function closeModule() {
    const prev = moduleName;
    setModuleName('');
    focusSelector(`.module-list [data-module="${prev}"]`);
  }

  const toolbar = (
    <div class="api-toolbar rcu-toolbar">
      <div class="toolbar-group">
        <small>Invocation</small>
        <ChoiceButtons values={MODE_OPTIONS} value={mode} onChange={setMode} />
      </div>
    </div>
  );

  return (
    <div class="page apis-page">
      {!moduleName ? (
        <div class="api-browse-shell">
          {toolbar}
          <Panel className="selection-panel module-select-panel">
            <h3>
              Module{' '}
              <span class="selection-count">
                {groups.length} modules · {methods.length} APIs
              </span>
            </h3>
            <ModuleList
              groups={groups}
              onSelect={openModule}
              emptyText={schema === 'loading' ? 'Loading OpenRPC modules…' : 'No modules loaded.'}
            />
          </Panel>
        </div>
      ) : (
        <>
          {toolbar}
          <div class="api-two-column">
            <Panel className="selection-panel">
              <div class="selection-panel-head">
                <button data-focusable="true" class="secondary back-button" onClick={closeModule}>
                  ‹ Back
                </button>
                <h3>
                  {moduleName} <span class="selection-count">{moduleMethods.length}</span>
                </h3>
              </div>
              <div class="selection-list method-list" data-scroll-region="true">
                {moduleMethods.length ? (
                  moduleMethods.map((method) => {
                    const key = methodKey(method);
                    return (
                      <button
                        key={key}
                        data-key={key}
                        data-focusable="true"
                        class={currentKey === key ? 'selection-item active' : 'selection-item'}
                        onClick={() => setSelected(key)}
                      >
                        <span class="selection-item-label">{method.method}</span>
                        <span class="selection-item-chevron">›</span>
                      </button>
                    );
                  })
                ) : (
                  <Empty text="No APIs in this module." />
                )}
              </div>
            </Panel>

            <Panel className="method-panel device-method-panel">
              {current ? (
                <>
                  <div class="method-head">
                    <div>
                      <h2>{current.name}</h2>
                      <p>{current.summary || current.description || 'Firebolt API'}</p>
                    </div>
                    <span class="badge">{mode}</span>
                  </div>
                  <div class="parameter-preview">
                    <div class="parameter-head">
                      <h4>Parameters</h4>
                      {parameterSet?.name?.toLowerCase() !== 'default example' && (
                        <span class="parameter-head-note">{parameterSet?.name || 'No parameter set'}</span>
                      )}
                    </div>
                    {parameterSets.length > 1 && (
                      <div class="button-row compact">
                        <button data-focusable="true" class="secondary" onClick={() => stepParameter(-1)}>
                          ◀ Previous
                        </button>
                        <span>
                          {parameterIndex + 1} / {parameterSets.length}
                        </span>
                        <button data-focusable="true" class="secondary" onClick={() => stepParameter(1)}>
                          Next ▶
                        </button>
                      </div>
                    )}
                    <pre class="code parameter-code" {...READABLE_BOX}>{parameterSet ? safeStringify(parameterSet.params) : '{}'}</pre>
                    {!parameterSet?.usable && <p class="warning-text">{parameterSet?.reason}</p>}
                  </div>
                  <button
                    data-focusable="true"
                    class="primary invoke-button"
                    disabled={!parameterSet?.usable}
                    onClick={invoke}
                  >
                    Invoke API
                  </button>
                  <div class="response-head">
                    <h4>Result</h4>
                    {result && (
                      <span class={`result ${result.status.toLowerCase()}`}>
                        {result.status} · {result.durationMs} ms
                      </span>
                    )}
                  </div>
                  <div class="result-details" data-scroll-region="true">
                    {!result && (
                      <div class="result-placeholder">Invoke the API to view the expected and actual response.</div>
                    )}
                    {failureReason.length > 0 && (
                      <section class="result-section failure-section">
                        <h5>Failure reason</h5>
                        <pre class="code failure-code" {...READABLE_BOX}>
                          {failureReason.join('\n')}
                        </pre>
                      </section>
                    )}
                    {result && (
                      <section class="result-section">
                        <h5>Expected response</h5>
                        <pre class="code expected-code" {...READABLE_BOX}>
                          {expectedResponse}
                        </pre>
                      </section>
                    )}
                    {result && (
                      <section class="result-section">
                        <h5>Actual response</h5>
                        <pre class="code response-code" {...READABLE_BOX}>
                          {safeStringify(result.error ?? result.response ?? null)}
                        </pre>
                      </section>
                    )}
                    {result?.status === 'FAIL' && !isEvent && (
                      <section class="result-section">
                        <h5>Sample response (OpenRPC example)</h5>
                        <pre class="code sample-code" {...READABLE_BOX}>
                          {sampleResponse !== undefined
                            ? safeStringify(sampleResponse)
                            : 'No sample response defined in OpenRPC.'}
                        </pre>
                      </section>
                    )}
                  </div>
                </>
              ) : (
                <Empty text="Select an API." />
              )}
            </Panel>
          </div>
        </>
      )}
    </div>
  );
}

function SuitesPage({
  methods,
  schema,
  theme,
  onOpenReports,
  autoRun
}: {
  methods: OpenRpcMethod[];
  schema: SchemaState;
  theme: UiTheme;
  onOpenReports: () => void;
  autoRun: boolean;
}) {
  // Empty selection means "All modules".
  const [selectedModules, setSelectedModules] = useState<string[]>([]);
  const [pickingScope, setPickingScope] = useState(false);
  const [mode, setMode] = useState<CommunicationMode>(runtimeConfig.communicationMode);
  const [running, setRunning] = useState(false);
  const [liveLogs, setLiveLogs] = useState<ExecutionResult[]>([]);
  const [report, setReport] = useState<CertificationSuiteReport | null>(null);
  const [progress, setProgress] = useState('');
  const [publishResults, setPublishResults] = useState<ReportPublishResult[]>([]);
  const [publishNote, setPublishNote] = useState('');
  const groups = useMemo(() => groupMethodsByModule(methods), [methods]);
  const allSelected = selectedModules.length === 0;
  const scopeCount = allSelected
    ? methods.length
    : groups.filter((g) => selectedModules.includes(g.module)).reduce((n, g) => n + g.methods.length, 0);
  const scopeLabel = allSelected ? ALL_MODULES : selectedModules.join(', ');
  const scopeButtonLabel = allSelected
    ? ALL_MODULES
    : selectedModules.length === 1
      ? selectedModules[0]
      : `${selectedModules.length} modules`;
  useEffect(
    () =>
      eventBus.on<any>('suite-progress', (p) =>
        setProgress(`${p.completed} results · method ${p.methodIndex}/${p.methodTotal} · ${p.current}`)
      ),
    []
  );
  useEffect(() => {
    const valid = selectedModules.filter((m) => groups.some((g) => g.module === m));
    if (valid.length !== selectedModules.length) setSelectedModules(valid);
  }, [groups, selectedModules]);
  // autoRun launch parameter: once the spec is loaded and the Firebolt probe has finished, run all modules once.
  useEffect(() => {
    if (!autoRun || autoRunStarted || schema !== 'loaded' || !methods.length) return;
    autoRunStarted = true;
    void run();
  }, [autoRun, schema, methods]);

  function openScopePicker() {
    setPickingScope(true);
    focusSelector('.scope-list .selection-item');
  }
  function closeScopePicker() {
    setPickingScope(false);
    focusSelector('.scope-button');
  }
  function toggleModule(mod: string) {
    setSelectedModules((prev) => {
      const next = prev.includes(mod) ? prev.filter((m) => m !== mod) : [...prev, mod];
      // Keep schema order so labels/report titles are stable.
      return groups.map((g) => g.module).filter((m) => next.includes(m));
    });
  }

  async function run() {
    setRunning(true);
    setPickingScope(false);
    setProgress('Starting...');
    setPublishResults([]);
    setPublishNote('');
    setLiveLogs([]);
    // Subscribe before the suite starts: an effect would attach after the first method already logged, dropping its lines.
    const stopLogs = eventBus.on<ExecutionResult>('execution', (r) => setLiveLogs((prev) => [r, ...prev.slice(0, 499)]));
    try {
      if (runtimeConfig.autoRun) {
        // Find the report server's actual port first, then fetch this device's TDK reportingId so report names match the execution.
        await resolveReportPublishUrl();
        await resolveAutomationContext();
      }
      // Runs Firebolt Certification's OpenRPC; module scope is applied per method inside runSuite.
      const generated = await certificationEngine.runSuite({
        modules: allSelected ? undefined : selectedModules,
        scopeLabel,
        mode,
        slaValidation: false
      });
      setReport(generated);
      setProgress('');
      if (generated.interrupted) {
        // A stopped run is partial, so it is never published as a completed certification.
        setProgress(`Stopped · ${generated.methodsNotRun ?? 0} method(s) not tested`);
        setPublishNote('Run was stopped: the partial report was not published.');
      } else if (runtimeConfig.reportPublishUrl) {
        await resolveReportPublishUrl();
        const published = await Promise.all(
          (['json', 'html', 'xlsx'] as const).map((format) => publishReport(generated, format))
        );
        setPublishResults(published);
      } else setPublishNote('Configure reportPublishUrl to publish reports automatically.');
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      setProgress(`Suite failed · ${message}`);
      setPublishNote(`Report was not generated/uploaded: ${message}`);
    } finally {
      stopLogs();
      setRunning(false);
    }
  }
  return (
    <div class="page suites-page">
      <div class="suites-toolbar-row">
        <div class="api-toolbar rcu-toolbar">
          <div class="toolbar-group">
            <small>Scope</small>
            <div class="choice-buttons">
              <button
                data-focusable="true"
                class="choice active scope-button"
                disabled={running}
                onClick={openScopePicker}
                title={scopeLabel}
              >
                {scopeButtonLabel} ▾
              </button>
            </div>
          </div>
          <div class="toolbar-divider" />
          <div class="toolbar-group">
            <small>Invocation</small>
            <ChoiceButtons values={MODE_OPTIONS} value={mode} onChange={setMode} />
          </div>
        </div>
        <div class="suites-actions">
          <button data-focusable="true" class="primary" disabled={running || !methods.length} onClick={run}>
            ▶ Run Suite
          </button>
          <button
            data-focusable="true"
            class="secondary"
            disabled={!running}
            onClick={() => certificationEngine.stopSuite()}
          >
            ■ Stop
          </button>
          {report && (
            <button data-focusable="true" class="secondary" onClick={onOpenReports}>
              View Report
            </button>
          )}
        </div>
      </div>
      {progress && (
        <div class="run-progress-line">
          <strong>{progress}</strong>
        </div>
      )}
      {(publishNote || publishResults.length > 0) && (
        <div class="publish-panel">
          {publishNote && <p class="publish-note">{publishNote}</p>}
          {publishResults.length > 0 && publishResults.every((p) => p.ok) ? (
            <p class="publish-note">
              JSON, HTML, and XLSX reports published successfully to {runtimeConfig.reportPublishUrl}.
            </p>
          ) : (
            publishResults.map((p) => (
              <div key={p.format} class={`publish-row ${p.ok ? 'ok' : 'fail'}`}>
                <span class="publish-dot" />
                <span class="publish-format">{p.format.toUpperCase()}</span>
                <span class="publish-message" title={p.message}>
                  {p.message}
                </span>
              </div>
            ))
          )}
        </div>
      )}
      {pickingScope ? (
        <Panel className="suites-panel selection-panel scope-panel">
          <div class="selection-panel-head">
            <button data-focusable="true" class="secondary back-button" onClick={closeScopePicker}>
              ‹ Back
            </button>
            <h3>
              Select modules{' '}
              <span class="selection-count">
                {allSelected ? 'All' : `${selectedModules.length} selected`} · {scopeCount} APIs
              </span>
            </h3>
            <button data-focusable="true" class="primary scope-done-button" onClick={closeScopePicker}>
              Done
            </button>
          </div>
          <div class="selection-list scope-list" data-scroll-region="true">
            <button
              data-focusable="true"
              role="checkbox"
              aria-checked={allSelected}
              class={allSelected ? 'selection-item active' : 'selection-item'}
              onClick={() => setSelectedModules([])}
            >
              <span class={allSelected ? 'scope-check checked' : 'scope-check'} />
              <span class="selection-item-label">{ALL_MODULES}</span>
              <span class="selection-item-meta">
                <span class="selection-count">{methods.length}</span>
              </span>
            </button>
            {groups.map((g) => {
              const on = selectedModules.includes(g.module);
              return (
                <button
                  key={g.module}
                  data-focusable="true"
                  role="checkbox"
                  aria-checked={on}
                  class={on ? 'selection-item active' : 'selection-item'}
                  onClick={() => toggleModule(g.module)}
                >
                  <span class={on ? 'scope-check checked' : 'scope-check'} />
                  <span class="selection-item-label">{g.module}</span>
                  <ModuleMeta group={g} />
                </button>
              );
            })}
          </div>
        </Panel>
      ) : (
        <Panel className="suites-panel">
          {running ? (
            <div class="logs" data-scroll-region="true">
              <div class="log-row header">
                <span>Time</span>
                <span>Status</span>
                <span>Message</span>
              </div>
              {liveLogs.map((r) => (
                <div key={r.id} class="log-row">
                  <span>{new Date(r.timestamp).toLocaleTimeString()}</span>
                  <span class={`log-status ${r.status.toLowerCase()}`}>{r.status}</span>
                  <span>{liveLogMessage(r)}</span>
                </div>
              ))}
            </div>
          ) : report ? (
            <ReportFrame key={report.id} report={report} theme={theme} />
          ) : (
            <Empty text={schema === 'loading' ? 'Loading OpenRPC modules…' : 'Run a suite to populate results.'} />
          )}
        </Panel>
      )}
    </div>
  );
}

function Reports({ theme }: { theme: UiTheme }) {
  const [reports, setReports] = useState<CertificationSuiteReport[]>(certificationEngine.getSuites());
  const [selectedId, setSelectedId] = useState(reports[0]?.id || '');
  useEffect(
    () =>
      eventBus.on<CertificationSuiteReport>('suite-complete', () => {
        const next = certificationEngine.getSuites();
        setReports(next);
        if (next[0]) setSelectedId(next[0].id);
      }),
    []
  );
  const current = reports.find((r) => r.id === selectedId) || reports[0];

  return (
    <div class="page">
      <PageTitle title="Reports" />
      <div class="split report-split">
        <Panel className="report-list-panel">
          <h3>Generated Reports</h3>
          <div class="report-list" data-scroll-region="true">
            {reports.length ? (
              reports.map((report) => (
                <button
                  key={report.id}
                  data-focusable="true"
                  class={current?.id === report.id ? 'report-item active' : 'report-item'}
                  onClick={() => setSelectedId(report.id)}
                >
                  <strong>{reportScope(report)}</strong>
                  <span>Mode: {report.mode}</span>
                  <span>{new Date(report.endedAt).toLocaleString()}</span>
                  <small>
                    {report.summary.passed} pass · {report.summary.failed} fail · {report.summary.total} total
                    {report.interrupted ? ' · interrupted' : ''}                  </small>
                </button>
              ))
            ) : (
              <Empty text="No reports yet. Run a suite first." />
            )}
          </div>
        </Panel>
        <Panel className="report-detail-panel">
          {current ? (
            <ReportFrame key={current.id} report={current} theme={theme} />
          ) : (
            <Empty text="Select a report." />
          )}
        </Panel>
      </div>
    </div>
  );
}

function Events({ methods, schema }: { methods: OpenRpcMethod[]; schema: SchemaState }) {
  const allEvents = useMemo(() => methods.filter((m) => isEventMethod(m)), [methods]);
  const groups = useMemo(() => groupMethodsByModule(allEvents), [allEvents]);
  const [moduleName, setModuleName] = useState('');
  const moduleEvents = useMemo(
    () => groups.find((g) => g.module === moduleName)?.methods || NO_METHODS,
    [groups, moduleName]
  );
  const [eventName, setEventName] = useState('');
  const eventMethod = moduleEvents.find((m) => methodKey(m) === eventName) || moduleEvents[0];
  const eventKey = eventMethod ? methodKey(eventMethod) : '';
  const [mode, setMode] = useState<CommunicationMode>(runtimeConfig.communicationMode);
  const [listeners, setListeners] = useState(eventManager.getAll());
  const [eventOutput, setEventOutput] = useState('');
  const parameterSet = eventMethod ? openRpcService.getParameterSets(eventMethod)[0] : undefined;

  useEffect(() => {
    if (moduleName && !groups.some((g) => g.module === moduleName)) setModuleName('');
  }, [groups, moduleName]);
  useEffect(() => {
    setEventName(moduleEvents[0] ? methodKey(moduleEvents[0]) : '');
  }, [moduleName]);
  useEffect(() => {
    if (eventName && !moduleEvents.some((m) => methodKey(m) === eventName))
      setEventName(moduleEvents[0] ? methodKey(moduleEvents[0]) : '');
  }, [moduleEvents, eventName]);
  const [eventStatus, setEventStatus] = useState<{
    status: 'PASS' | 'FAIL';
    durationMs: number;
    expected?: string;
    failureReason: string[];
  } | null>(null);
  const pendingSubscribe = useRef(new Set<string>());
  // 'reply' = subscribe/unsubscribe reply (must be null, or an SDK acknowledgement in SDK mode); 'records' = received notifications (already validated per event)
  function showEvent(
    body: unknown,
    error: unknown,
    opts: { startedAt?: number; kind?: 'reply' | 'records'; event?: string; sdkManaged?: boolean } = {}
  ) {
    const { startedAt, kind, event, sdkManaged } = opts;
    const explain = (r: Partial<ExecutionResult>) =>
      explainFailure({
        id: '',
        method: event || eventMethod?.name || '',
        mode,
        status: 'FAIL',
        durationMs: 0,
        timestamp: 0,
        ...r
      });
    let failed = false;
    let failureReason: string[] = [];
    let expected: string | undefined;
    if (kind === 'reply')
      expected = sdkManaged
        ? 'SDK listener acknowledgement (not a raw gateway reply)'
        : 'null';
    if (kind === 'records') {
      const resultSchema = event ? openRpcService.getMethod(event)?.resultSchema : undefined;
      expected = `Each event payload: ${(resultSchema ? describeSchema(resultSchema) : '') || 'no result schema defined in OpenRPC'}`;
    }
    if (error) {
      failed = true;
      failureReason = explain({ error, schemaValidation: schemaValidator.validateError(error) });
    } else if (kind === 'reply' && !sdkManaged) {
      const schema = validateSubscriptionReply(body);
      if (!schema.valid) {
        failed = true;
        failureReason = explain({ response: body, schemaValidation: schema });
      }
    } else if (kind === 'records' && Array.isArray(body)) {
      body.forEach((r: EventRecord, i) => {
        if (r.schemaValidation?.valid !== false) return;
        failed = true;
        failureReason.push(
          `Event ${i + 1} (${new Date(r.timestamp).toLocaleTimeString()}):`,
          ...explain({ response: r.value, schemaValidation: r.schemaValidation }).map((l) => `  ${l}`)
        );
      });
    }
    setEventStatus({
      status: failed ? 'FAIL' : 'PASS',
      durationMs: startedAt ? Math.round(performance.now() - startedAt) : 0,
      expected,
      failureReason
    });
    const out = error ?? body;
    setEventOutput(typeof out === 'string' ? out : safeStringify(out ?? null));
  }
  async function register() {
    if (!eventMethod || !parameterSet?.usable) return;
    const name = eventMethod.name;
    const clean = name.toLowerCase();
    if (pendingSubscribe.current.has(clean) || eventManager.getAll().some((l) => l.event.toLowerCase() === clean))
      return;
    pendingSubscribe.current.add(clean);
    try {
      const t = performance.now();
      const r = await eventManager.register(name, parameterSet.params, mode);
      setListeners(eventManager.getAll());
      showEvent(r.eventListenerResponse?.subscriptionReply, r.eventListenerResponse?.error, {
        startedAt: t,
        kind: 'reply',
        event: name,
        sdkManaged: r.eventListenerResponse?.sdkManaged
      });
    } finally {
      pendingSubscribe.current.delete(clean);
    }
  }
  async function unsubscribe(target: string) {
    const t = performance.now();
    const r = await eventManager.unsubscribe(target);
    setListeners(eventManager.getAll());
    showEvent(r.unsubscribeReply ?? r.result, r.error, {
      startedAt: t,
      kind: 'unsubscribeReply' in r ? 'reply' : undefined,
      event: r.eventName,
      sdkManaged: r.sdkManaged
    });
  }
  function openModule(mod: string) {
    setModuleName(mod);
    focusSelector('.method-list .selection-item.active');
  }
  function closeModule() {
    const prev = moduleName;
    setModuleName('');
    focusSelector(`.module-list [data-module="${prev}"]`);
  }

  const toolbar = (
    <div class="api-toolbar rcu-toolbar">
      <div class="toolbar-group">
        <small>Invocation</small>
        <ChoiceButtons values={MODE_OPTIONS} value={mode} onChange={setMode} />
      </div>
    </div>
  );

  return (
    <div class="page events-page">
      {!moduleName ? (
        <div class="api-browse-shell">
          {toolbar}
          <Panel className="selection-panel module-select-panel">
            <h3>
              Module{' '}
              <span class="selection-count">
                {groups.length} modules · {allEvents.length} events
              </span>
            </h3>
            <ModuleList
              groups={groups}
              onSelect={openModule}
              emptyText={schema === 'loading' ? 'Loading OpenRPC events…' : 'No events loaded.'}
            />
          </Panel>
        </div>
      ) : (
        <>
          {toolbar}
          <div class="api-two-column">
            <Panel className="selection-panel">
              <div class="selection-panel-head">
                <button data-focusable="true" class="secondary back-button" onClick={closeModule}>
                  ‹ Back
                </button>
                <h3>
                  {moduleName} <span class="selection-count">{moduleEvents.length}</span>
                </h3>
              </div>
              <div class="selection-list method-list" data-scroll-region="true">
                {moduleEvents.length ? (
                  moduleEvents.map((method) => {
                    const key = methodKey(method);
                    return (
                      <button
                        key={key}
                        data-key={key}
                        data-focusable="true"
                        class={eventKey === key ? 'selection-item active' : 'selection-item'}
                        onClick={() => setEventName(key)}
                      >
                        <span class="selection-item-label">{method.method}</span>
                        <span class="selection-item-chevron">›</span>
                      </button>
                    );
                  })
                ) : (
                  <Empty text="No events in this module." />
                )}
              </div>
            </Panel>
            <Panel className="event-detail">
              <h3>{eventMethod?.name || 'Select event'}</h3>
              <h4>Subscribe parameters</h4>
              <pre class="code event-param-code">{safeStringify(parameterSet?.params || {})}</pre>
              {!parameterSet?.usable && <p class="warning-text">{parameterSet?.reason}</p>}
              <h4>Unsubscribe parameters</h4>
              <pre class="code event-param-code">{safeStringify({ listen: false })}</pre>
              <div class="button-row">
                <button
                  data-focusable="true"
                  class="primary"
                  disabled={!eventMethod || !parameterSet?.usable}
                  onClick={register}
                >
                  Subscribe
                </button>
                <button
                  data-focusable="true"
                  class="secondary"
                  disabled={!eventMethod}
                  onClick={() => eventMethod && unsubscribe(eventMethod.name)}
                >
                  Unsubscribe
                </button>
              </div>
              <div class="listener-list">
                {listeners.map((listener) => (
                  <div key={listener.key} style="display:flex;gap:8px;align-items:stretch">
                    <button
                      data-focusable="true"
                      class="listener-item"
                      style="flex:1"
                      onClick={() =>
                        showEvent(eventManager.getResponse(listener.key, 10), null, {
                          kind: 'records',
                          event: listener.event
                        })
                      }
                    >
                      {listener.event}
                      <small>{listener.count} events</small>
                    </button>
                    <button
                      data-focusable="true"
                      class="danger"
                      title="Unsubscribe this listener"
                      onClick={() => unsubscribe(listener.key)}
                    >
                      X
                    </button>
                  </div>
                ))}
              </div>
              <div class="response-head">
                <h4>Result</h4>
                {eventStatus && (
                  <span class={`result ${eventStatus.status.toLowerCase()}`}>
                    {eventStatus.status}
                    {eventStatus.durationMs ? ` · ${eventStatus.durationMs} ms` : ''}
                  </span>
                )}
              </div>
              <div class="result-details" data-scroll-region="true">
                {!eventStatus && (
                  <div class="result-placeholder">
                    Subscribe, unsubscribe or select a listener to view the expected and actual response.
                  </div>
                )}
                {eventStatus && eventStatus.failureReason.length > 0 && (
                  <section class="result-section failure-section">
                    <h5>Failure reason</h5>
                    <pre class="code failure-code" {...READABLE_BOX}>
                      {eventStatus.failureReason.join('\n')}
                    </pre>
                  </section>
                )}
                {eventStatus?.expected && (
                  <section class="result-section">
                    <h5>Expected response</h5>
                    <pre class="code expected-code" {...READABLE_BOX}>
                      {eventStatus.expected}
                    </pre>
                  </section>
                )}
                {eventStatus && (
                  <section class="result-section">
                    <h5>Actual response</h5>
                    <pre class="code response-code" {...READABLE_BOX}>
                      {eventOutput}
                    </pre>
                  </section>
                )}
              </div>
            </Panel>
          </div>
        </>
      )}
    </div>
  );
}

function PageTitle({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div class="page-title">
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}
    </div>
  );
}
function ModuleMeta({ group }: { group: ModuleGroup }) {
  return (
    <span class="selection-item-meta">
      <span class="selection-count">{group.methods.length}</span>
    </span>
  );
}
function liveLogMessage(r: ExecutionResult): string {
  const name = [r.exampleName || r.method, r.eventAction].filter(Boolean).join(' ');
  return `${name} (${r.durationMs} ms)`;
}

function ModuleList({
  groups,
  onSelect,
  emptyText
}: {
  groups: ModuleGroup[];
  onSelect: (module: string) => void;
  emptyText: string;
}) {
  return (
    <div class="selection-list module-list" data-scroll-region="true">
      {groups.length ? (
        groups.map((g) => (
          <button
            key={g.module}
            data-module={g.module}
            data-focusable="true"
            class="selection-item"
            onClick={() => onSelect(g.module)}
          >
            <span class="selection-item-label">{g.module}</span>
            <ModuleMeta group={g} />
            <span class="selection-item-chevron">›</span>
          </button>
        ))
      ) : (
        <Empty text={emptyText} />
      )}
    </div>
  );
}

function reportScope(report: CertificationSuiteReport): string {
  const i = report.title.lastIndexOf(' - ');
  return i >= 0 ? report.title.slice(i + 3) : ALL_MODULES;
}
function Empty({ text }: { text: string }) {
  return <div class="empty">{text}</div>;
}
function pretty(s: string) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
