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
 * @file Exports suite reports as JSON, HTML and Excel files, downloads them and uploads them to the report server.
 */

import { DEFAULT_REPORT_PUBLISH_URL, runtimeConfig } from '../config/runtime';
import { safeStringify } from '../utils/helpers';
import type { CertificationSuiteReport, ExecutionResult, ReportFormat, ReportPublishResult } from '../types';
import LOGO_DATA_URI from '../assets/tdk-logo-report.png?inline';
import {
  buildXlsx,
  safeSheetName,
  type XlsxCell,
  type XlsxDoughnutChart,
  type XlsxSheet,
  type XlsxStyle
} from './XlsxWriter';

function escapeHtml(value: unknown): string {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function stamp(ms: number): string {
  const d = new Date(ms);
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${d.getUTCFullYear()}${pad(d.getUTCMonth() + 1)}${pad(d.getUTCDate())}-${pad(d.getUTCHours())}${pad(d.getUTCMinutes())}${pad(d.getUTCSeconds())}`;
}

export function reportFileName(report: CertificationSuiteReport, format: ReportFormat): string {
  const prefix =
    runtimeConfig.reportingId ||
    runtimeConfig.macAddress.replace(/:/g, '') ||
    runtimeConfig.appId ||
    'firebolt-certification';
  return `${prefix}-refAppExecReport-${stamp(report.endedAt)}.${format}`;
}

/** A stopped run is reported as INTERRUPTED, never PASSED, because the remaining methods were not tested. */
export function overallStatus(report: CertificationSuiteReport): 'PASSED' | 'FAILED' | 'INTERRUPTED' {
  if (report.interrupted) return 'INTERRUPTED';
  return report.results.some((r) => r.status === 'FAIL') ? 'FAILED' : 'PASSED';
}

/**
 * JSON report: the same grouping and columns as the HTML page and the Excel module sheets (Sl No, Method,
 * Description, Status, Log), grouped by module. `stats`/`suites` are kept for Mocha-style downstream
 * compatibility; the old flat `results` array is replaced by `modules`.
 */
export function generateReportJson(report: CertificationSuiteReport): string {
  const modules = groupByModule(report.results).map(({ module, results }) => toJsonModule(module, results));
  return safeStringify({
    id: report.id,
    title: report.title,
    mode: report.mode,
    version: report.specVersion,
    startedAt: report.startedAt,
    endedAt: report.endedAt,
    overallStatus: overallStatus(report),
    ...(report.interrupted ? { interrupted: true, methodsNotRun: report.methodsNotRun } : {}),
    summary: {
      totalTestCases: report.summary.total,
      passed: report.summary.passed,
      failed: report.summary.failed,
      ...validatedCounts(report.results),
      durationMs: report.summary.durationMs
    },
    modules,
    stats: report.stats,
    suites: report.suites
  });
}

const pretty = (value: unknown) => safeStringify(value) ?? String(value);

export function exampleText(r: ExecutionResult): string {
  return r.exampleResponse === undefined ? '' : pretty(r.exampleResponse);
}

// Actual response cell: the error when the call failed, otherwise the response (event subscribe/unsubscribe replies: expected null).
export function responseText(r: ExecutionResult): string {
  return pretty(r.error ?? r.response ?? null);
}

/** Method name as shown in the reports; event methods get a Subscribe/Unsubscribe suffix because each has two rows. */
export const methodLabel = (r: ExecutionResult) =>
  r.eventAction ? `${r.method} (${r.eventAction === 'subscribe' ? 'Subscribe' : 'Unsubscribe'})` : r.method;

const moduleOf = (r: ExecutionResult) => r.method.split('.')[0] || 'Other';

export interface ValidatedCounts {
  validatedApis: number;
  validatedEvents: number;
}

/** Distinct APIs and events validated; an event's Subscribe and Unsubscribe rows count as one event. */
export function validatedCounts(results: ExecutionResult[]): ValidatedCounts {
  const apis = new Set<string>();
  const events = new Set<string>();
  for (const r of results) (r.eventAction ? events : apis).add(r.method);
  for (const e of events) apis.delete(e);
  return { validatedApis: apis.size, validatedEvents: events.size };
}

/** Groups results by Firebolt module, alphabetically, matching the Excel module sheets and the HTML module filter. */
function groupByModule(results: ExecutionResult[]): Array<{ module: string; results: ExecutionResult[] }> {
  const byModule = new Map<string, ExecutionResult[]>();
  for (const r of results) {
    const module = moduleOf(r);
    byModule.set(module, [...(byModule.get(module) || []), r]);
  }
  return [...byModule.keys()]
    .sort((x, y) => x.localeCompare(y))
    .map((module) => ({ module, results: byModule.get(module)! }));
}

interface JsonLogSection {
  label: string;
  text: string;
}
interface JsonModuleResult {
  slNo: number;
  method: string;
  description: string;
  status: ExecutionResult['status'];
  log: JsonLogSection[];
}
interface JsonModule extends ValidatedCounts {
  module: string;
  totalTestCases: number;
  passed: number;
  failed: number;
  passRate: number | null;
  results: JsonModuleResult[];
}

function toJsonModule(module: string, results: ExecutionResult[]): JsonModule {
  const counts = countResults(results);
  return {
    module,
    totalTestCases: counts.total,
    passed: counts.passed,
    failed: counts.failed,
    ...validatedCounts(results),
    passRate: passRateNumber(counts),
    results: results.map((r, i) => ({
      slNo: i + 1,
      method: methodLabel(r),
      description: r.description || '',
      status: r.status,
      log: logSections(r).map(({ label, text }) => ({ label, text }))
    }))
  };
}

// Response and failure reason shown together in one expandable "Log" cell.
function logCell(r: ExecutionResult): string {
  const body = logSections(r)
    .map(({ label, text, kind }) => {
      const value =
        kind === 'text'
          ? `<p class="plain">${escapeHtml(text)}</p>`
          : `<pre${kind === 'reason' ? ' class="reason"' : ''}>${escapeHtml(text)}</pre>`;
      return `<div class="label${kind === 'reason' ? ' reason-label' : ''}">${escapeHtml(label)}</div>${value}`;
    })
    .join('');
  return `<div class="clip" tabindex="0">${body}</div>`;
}

// Report design tokens: same token names/values as the app (src/styles/global.css). The mode is chosen by the "light" class on <html>.
const REPORT_TOKENS = `
:root{--bg:#121417;--surface:#1b1e23;--surface-2:#24282e;--row-hover:#24282e;--border:#343a42;--text:#e8ecef;--text-soft:#c9d1d9;--text-muted:#a3adb8;--code-text:#c9d1d9;--accent:#2dd4bf;--accent-soft:#123a36;--focus:#5eead4;--focus-ring:0 0 0 2px var(--bg),0 0 0 5px var(--focus);--focus-ring-sm:0 0 0 2px var(--surface),0 0 0 4px var(--focus);--pass:#34d399;--fail:#f87171;--fail-text:#f87171;--sunken:#101215;--sunken-fade:rgba(16,18,21,0);--clip-open-bg:#24282e;--shadow:rgba(0,0,0,.45);--shadow-lg:0 4px 18px var(--shadow);color-scheme:dark}
html.light{--bg:#eceef0;--surface:#f5f6f7;--surface-2:#e6e9ec;--row-hover:#e6e9ec;--border:#d3d8dd;--text:#16191d;--text-soft:#333b44;--text-muted:#5a6470;--code-text:#333b44;--accent:#0d6b64;--accent-soft:#d6eeea;--focus:#134e4a;--pass:#137535;--fail:#b91c1c;--fail-text:#b91c1c;--sunken:#eef0f2;--sunken-fade:rgba(238,240,242,0);--clip-open-bg:#f5f6f7;--shadow:rgba(22,25,29,.12);--shadow-lg:0 4px 14px var(--shadow);color-scheme:light}`;

const HTML_STYLE = `${REPORT_TOKENS}
*{box-sizing:border-box}body{position:relative;font-family:Segoe UI,Arial,sans-serif;background:var(--bg);color:var(--text);margin:0;padding:24px 28px}
h1{margin:0 0 4px;font-size:24px}.meta{color:var(--text-muted);font-size:13px}
.top{display:flex;flex-wrap:wrap;align-items:center;gap:0 24px;padding-right:48px}.top-main{flex:1 1 640px;min-width:0}
.report-head{display:flex;align-items:center;gap:16px}.report-logo{height:64px;width:auto;flex:none;display:block}.report-title{min-width:0}
/* Embedded in the app (whose header owns the theme): hidden from the first paint, before the body script removes it. */
html.embedded .theme-toggle{display:none!important}
button.theme-toggle{position:absolute;top:22px;right:28px;width:34px;height:34px;padding:0;display:flex;align-items:center;justify-content:center;border-radius:50%}
.theme-toggle svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.theme-toggle .i-sun{display:block}.theme-toggle .i-moon{display:none}
html.light .theme-toggle .i-sun{display:none}html.light .theme-toggle .i-moon{display:block}
.summary{display:flex;flex-wrap:wrap;align-items:stretch;gap:12px;margin:18px 0}
.chart{margin:12px 0 12px auto;flex:none;display:flex;align-items:center;gap:18px;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 22px;color:var(--text-muted);font-size:14px}
.chart svg{width:120px;height:120px;flex:none}.chart .track{stroke:var(--surface-2)}.chart .ok{stroke:var(--pass)}.chart .ko{stroke:var(--fail)}
.chart .pct{fill:var(--text);font-size:7.5px;font-weight:700}.chart .cap{fill:var(--text-muted);font-size:4.5px}
.chart ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}.chart li b{color:var(--text)}
.chart i{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:8px;vertical-align:-1px}.chart i.ok{background:var(--pass)}.chart i.ko{background:var(--fail)}
.card,.stat{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 18px;min-width:110px;color:var(--text-muted);font:inherit;font-size:13px;text-align:left;cursor:pointer}
.stat{cursor:default}
.card,.stat{display:flex;flex-direction:column;justify-content:center;align-items:flex-start}
.card b,.stat b{display:block;font-size:24px;margin-top:2px;color:var(--text)}.card.pass b{color:var(--pass)}.card.fail b{color:var(--fail)}
.card:hover{border-color:var(--accent)}.card.active{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent) inset;background:var(--accent-soft)}
.toolbar{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;align-items:center;gap:10px;padding:10px 0;background:var(--bg);border-bottom:1px solid var(--border)}
.toolbar label{color:var(--text-muted);font-size:13px}
input,button.tool{background:var(--surface);color:var(--text);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font:inherit;font-size:13px}
input{min-width:240px}button.tool{cursor:pointer}button.tool:hover,input:focus{border-color:var(--accent);outline:none}
.dd{position:relative}.dd-btn{display:inline-flex;align-items:center;gap:10px;min-width:200px;justify-content:space-between;text-align:left}.dd-caret{color:var(--text-muted);font-size:11px}
.dd-menu{position:absolute;top:calc(100% + 4px);left:0;z-index:5;min-width:100%;max-height:320px;overflow:auto;display:flex;flex-direction:column;padding:4px;background:var(--surface);border:1px solid var(--border);border-radius:8px;box-shadow:0 8px 24px var(--shadow)}
.dd-menu[hidden]{display:none}
.dd-opt{background:transparent;color:var(--text);border:1px solid transparent;border-radius:5px;padding:8px 10px;font:inherit;font-size:13px;text-align:left;white-space:nowrap;cursor:pointer}
.dd-opt:hover{background:var(--surface-2)}.dd-opt.selected{color:var(--accent);font-weight:600}
.dd-opt:focus{outline:none;border-color:var(--accent);background:var(--surface-2);box-shadow:var(--focus-ring-sm)}
.count{margin-left:auto;color:var(--text-muted);font-size:13px}
.table-wrap{overflow-x:auto;margin-top:12px}table{width:100%;min-width:1100px;border-collapse:collapse;background:var(--surface);table-layout:fixed}
th,td{padding:10px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top;overflow-wrap:break-word}pre{overflow-wrap:anywhere}
th{color:var(--text-muted);background:var(--surface-2);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
tr.result:hover td{background:var(--row-hover)}.method{font-weight:600}.desc{color:var(--text-soft);font-size:13px}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:700;border:1px solid}
.badge.pass{color:var(--pass);border-color:var(--pass)}.badge.fail{color:var(--fail);border-color:var(--fail)}
pre{white-space:pre-wrap;margin:0;font-size:11.5px;color:var(--code-text);font-family:Consolas,Menlo,monospace}
pre.reason{color:var(--fail-text)}
.label{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--text-muted);margin:10px 0 3px}.label:first-child{margin-top:0}.reason-label{color:var(--fail)}.plain{margin:0;font-size:12.5px}.sl{color:var(--text-muted);text-align:right}
.clip{position:relative;max-height:80px;overflow:hidden;border-radius:6px;padding:6px 8px;background:var(--sunken);border:1px solid transparent;transition:background .15s,border-color .15s}
html.no-motion *{transition:none!important}
.clip.overflowing{cursor:zoom-in}.clip.overflowing:hover{border-color:var(--border)}
.clip.overflowing:not(.open)::after{content:"Click to expand";position:absolute;left:0;right:0;bottom:0;height:34px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:4px;font-size:11px;color:var(--accent);background:linear-gradient(var(--sunken-fade),var(--sunken) 70%)}
.clip.open{max-height:none;cursor:zoom-out;border-color:var(--accent);background:var(--clip-open-bg);box-shadow:var(--shadow-lg)}
.empty{padding:28px;text-align:center;color:var(--text-muted)}
.clip,.card,.toolbar,tr.result{scroll-margin-top:64px;scroll-margin-bottom:12px}
.card:focus,.clip:focus,input:focus,button.tool:focus{outline:none;border-color:var(--accent);box-shadow:var(--focus-ring)}
@media (prefers-reduced-motion:reduce){.clip{transition:none}}`;

const HTML_SCRIPT = `
(function(){
  var root=document.documentElement,themeBtn=document.getElementById('f-theme'),KEY='firebolt-certification-report-theme';
  if(window.parent!==window){themeBtn.remove();}else{
    // Opened on its own (downloaded/published): remember the reader's choice. Inside the app the app header controls the theme.
    var saved;try{saved=localStorage.getItem(KEY);}catch(e){}
    if(saved==='light'||saved==='dark')root.classList.toggle('light',saved==='light');
    var syncTheme=function(){var label=root.classList.contains('light')?'Switch to dark theme':'Switch to light theme';themeBtn.setAttribute('aria-label',label);themeBtn.title=label;};
    themeBtn.addEventListener('click',function(){
      root.classList.add('no-motion');
      var light=root.classList.toggle('light');
      try{localStorage.setItem(KEY,light?'light':'dark');}catch(e){}
      syncTheme();setTimeout(function(){root.classList.remove('no-motion');},100);
    });
    syncTheme();
  }
  var rows=[].slice.call(document.querySelectorAll('tr.result'));
  var ddBtn=document.getElementById('f-module'),ddMenu=document.querySelector('#f-module-dd .dd-menu'),ddLabel=ddBtn.querySelector('.dd-label'),moduleValue='',search=document.getElementById('f-search'),count=document.getElementById('f-count'),empty=document.getElementById('f-empty');
  var cards=[].slice.call(document.querySelectorAll('.card')),status='';
  function markOverflow(){[].forEach.call(document.querySelectorAll('.clip:not(.open)'),function(c){c.classList.toggle('overflowing',c.scrollHeight>c.clientHeight+2);});syncToggle();}
  function syncToggle(){var t=document.getElementById('f-toggle');var allOpen=!!document.querySelector('.clip.open')&&!document.querySelector('.clip.overflowing:not(.open)');t.textContent=allOpen?'Collapse all':'Expand all';t.setAttribute('aria-pressed',String(allOpen));}
  function apply(){
    var m=moduleValue,t=search.value.trim().toLowerCase(),shown=0;
    rows.forEach(function(r){
      var ok=(!m||r.getAttribute('data-module')===m)&&(!status||r.getAttribute('data-status')===status)&&(!t||r.textContent.toLowerCase().indexOf(t)>=0);
      r.hidden=!ok;if(ok){shown++;r.cells[0].textContent=shown;}
    });
    count.textContent='Showing '+shown+' of '+rows.length+' results';empty.hidden=shown>0;markOverflow();
  }
  cards.forEach(function(c){c.addEventListener('click',function(){
    status=c.getAttribute('data-status');
    cards.forEach(function(x){x.classList.toggle('active',x===c);});apply();
  });});
  function openMenu(open){ddMenu.hidden=!open;ddBtn.setAttribute('aria-expanded',String(open));if(open){var sel=ddMenu.querySelector('.dd-opt.selected');if(sel)sel.focus();}}
  ddBtn.addEventListener('click',function(){openMenu(ddMenu.hidden);});
  [].forEach.call(ddMenu.querySelectorAll('.dd-opt'),function(o){o.addEventListener('click',function(){
    moduleValue=o.getAttribute('data-value');ddLabel.textContent=o.textContent;
    [].forEach.call(ddMenu.querySelectorAll('.dd-opt'),function(x){var on=x===o;x.classList.toggle('selected',on);x.setAttribute('aria-selected',String(on));});
    openMenu(false);ddBtn.focus();apply();
  });});
  document.addEventListener('click',function(e){if(!ddMenu.hidden&&!e.target.closest('#f-module-dd'))openMenu(false);});
  document.getElementById('f-module-dd').addEventListener('focusout',function(e){if(!e.relatedTarget||!e.relatedTarget.closest||!e.relatedTarget.closest('#f-module-dd'))setTimeout(function(){if(!document.getElementById('f-module-dd').contains(document.activeElement))openMenu(false);},0);});
  document.getElementById('f-module-dd').addEventListener('keydown',function(e){if(e.key==='Escape'&&!ddMenu.hidden){e.preventDefault();e.stopPropagation();openMenu(false);ddBtn.focus();}});
  search.addEventListener('input',apply);
  function toggle(c){if(c.classList.contains('open')){c.classList.remove('open');markOverflow();}else if(c.classList.contains('overflowing')){c.classList.add('open');syncToggle();}}
  document.addEventListener('click',function(e){
    var c=e.target.closest&&e.target.closest('.clip');
    if(!c||String(window.getSelection&&window.getSelection())!=='')return;toggle(c);
  });
  document.addEventListener('keydown',function(e){if((e.key==='Enter'||e.key===' ')&&e.target.classList&&e.target.classList.contains('clip')){e.preventDefault();toggle(e.target);}});
  document.getElementById('f-toggle').addEventListener('click',function(){
    if(this.getAttribute('aria-pressed')==='true'){[].forEach.call(document.querySelectorAll('.clip.open'),function(c){c.classList.remove('open');});markOverflow();}
    else{[].forEach.call(document.querySelectorAll('.clip.overflowing'),function(c){c.classList.add('open');});syncToggle();}
  });
  window.addEventListener('resize',markOverflow);
  apply();
})();`;

/** Inline SVG donut of passed vs failed test cases (circumference 100, so dash lengths are percentages). */
function successChart(passed: number, failed: number): string {
  const total = passed + failed;
  const p = total ? (passed / total) * 100 : 0;
  const f = total ? 100 - p : 0;
  const arc = (cls: string, len: number, start: number) =>
    len > 0
      ? `<circle class="${cls}" cx="21" cy="21" r="15.9155" fill="none" stroke-width="5" stroke-dasharray="${len.toFixed(2)} ${(100 - len).toFixed(2)}" stroke-dashoffset="${(25 - start).toFixed(2)}"/>`
      : '';
  const pct = total ? `${p.toFixed(1)}%` : '—';
  return `<div class="chart" role="img" aria-label="Success rate ${pct}: ${passed} passed, ${failed} failed"><svg viewBox="0 0 42 42" aria-hidden="true"><circle class="track" cx="21" cy="21" r="15.9155" fill="none" stroke-width="5"/>${arc('ok', p, 0)}${arc('ko', f, p)}<text class="pct" x="21" y="22" text-anchor="middle">${pct}</text><text class="cap" x="21" y="28" text-anchor="middle">success</text></svg><ul><li><b>Success rate</b></li><li><i class="ok"></i>Passed <b>${passed}</b></li><li><i class="ko"></i>Failed <b>${failed}</b></li></ul></div>`;
}

export function generateReportHtml(
  report: CertificationSuiteReport,
  theme: 'dark' | 'light' = 'light',
  showLogo = true
): string {
  const { summary } = report;
  const moduleCounts = new Map<string, number>();
  for (const r of report.results) moduleCounts.set(moduleOf(r), (moduleCounts.get(moduleOf(r)) || 0) + 1);
  const moduleOptions = [...moduleCounts.keys()]
    .sort((x, y) => x.localeCompare(y))
    .map(
      (m) =>
        `<button type="button" class="dd-opt" role="option" aria-selected="false" data-value="${escapeHtml(m)}">${escapeHtml(m)} (${moduleCounts.get(m)})</button>`
    )
    .join('');
  const allModules = `All modules`;
  const card = (label: string, value: number, statusValue: string, cls: string) =>
    `<button type="button" class="card ${cls}${statusValue ? '' : ' active'}" data-status="${statusValue}" title="${statusValue ? `Show only ${label.toLowerCase()} results` : 'Show all results'}">${label}<b>${value}</b></button>`;
  // Informational tiles, not status filters, so they avoid the .card class the filter script binds to.
  const validated = validatedCounts(report.results);
  const stat = (label: string, value: number) => `<div class="stat">${label}<b>${value}</b></div>`;
  const rows = report.results
    .map((r) => {
      const status = r.status.toLowerCase();
      return `
    <tr class="result" data-module="${escapeHtml(moduleOf(r))}" data-status="${escapeHtml(r.status)}">
      <td class="sl"></td>
      <td class="method">${escapeHtml(methodLabel(r)).replace(/\./g, '.<wbr>')}</td>
      <td class="desc">${escapeHtml(r.description || '')}</td>
      <td><span class="badge ${status}">${escapeHtml(r.status)}</span></td>
      <td>${logCell(r)}</td>
    </tr>`;
    })
    .join('');
  return `<!doctype html>
<html lang="en"${theme === 'light' ? ' class="light"' : ''}><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Firebolt Certification Report</title>
<style>${HTML_STYLE}</style><script>if(window.parent!==window)document.documentElement.classList.add('embedded');</script></head>
<body><button type="button" class="tool theme-toggle" id="f-theme" aria-label="Switch theme"><svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg><svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button><div class="top"><div class="top-main"><div class="report-head">${showLogo ? `<img class="report-logo" src="${LOGO_DATA_URI}" alt="TDK logo">` : ''}<div class="report-title"><h1>Firebolt Certification Report</h1>
<div class="meta">${escapeHtml(report.mode)}${report.specVersion ? ` · Firebolt Schema Validator · Version ${escapeHtml(report.specVersion)}` : ''} · Overall <span class="badge ${overallStatus(report) === 'PASSED' ? 'pass' : 'fail'}">${overallStatus(report)}</span>${report.interrupted ? ` · Stopped before ${report.methodsNotRun ?? 0} method${report.methodsNotRun === 1 ? '' : 's'} could be tested` : ''}</div></div></div>
<div class="summary">${card('Total test cases', summary.total, '', 'total')}${card('Pass', summary.passed, 'PASS', 'pass')}${card('Fail', summary.failed, 'FAIL', 'fail')}${stat('Validated APIs', validated.validatedApis)}${stat('Validated Events', validated.validatedEvents)}</div></div>${successChart(summary.passed, summary.failed)}</div>
<div class="toolbar">
  <label for="f-module">Module</label><div class="dd" id="f-module-dd"><button type="button" class="tool dd-btn" id="f-module" aria-haspopup="listbox" aria-expanded="false" data-value=""><span class="dd-label">${allModules}</span><span class="dd-caret">▾</span></button><div class="dd-menu" role="listbox" hidden><button type="button" class="dd-opt selected" role="option" aria-selected="true" data-value="">${allModules}</button>${moduleOptions}</div></div>
  <input id="f-search" type="search" placeholder="Search API/event, description or log…" aria-label="Search">
  <button type="button" class="tool" id="f-toggle" aria-pressed="false">Expand all</button>
  <span class="count" id="f-count"></span>
</div>
<div class="table-wrap"><table><colgroup><col style="width:60px"><col style="width:20%"><col style="width:24%"><col style="width:90px"><col></colgroup>
<thead><tr><th class="sl">Sl No</th><th>APIs/Events</th><th>Description</th><th>Status</th><th>Log</th></tr></thead>
<tbody>${rows}</tbody></table></div>
<div class="empty" id="f-empty" hidden>No results match the current filters.</div>
<script>${HTML_SCRIPT}</script>
</body></html>`;
}

const STATUS_STYLE: Record<string, XlsxStyle> = { PASS: 'pass', FAIL: 'fail' };

interface Counts {
  total: number;
  passed: number;
  failed: number;
}

function countResults(results: ExecutionResult[]): Counts {
  const c: Counts = { total: results.length, passed: 0, failed: 0 };
  for (const r of results) {
    if (r.status === 'PASS') c.passed++;
    else if (r.status === 'FAIL') c.failed++;
  }
  return c;
}

function passRateNumber(c: Counts): number | null {
  const executed = c.passed + c.failed;
  return executed ? c.passed / executed : null;
}
function passRate(c: Counts, style: 'percent' | 'totalPercent' = 'percent'): XlsxCell {
  const value = passRateNumber(c);
  return value === null ? { value: '—', style: style === 'percent' ? 'number' : 'total' } : { value, style };
}

function formatDuration(ms: number): string {
  const totalSeconds = Math.max(0, Math.round(ms / 1000));
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const sec = totalSeconds % 60;
  const pad = (n: number) => String(n).padStart(2, '0');
  if (h) return `${h}h ${pad(m)}m ${pad(sec)}s`;
  if (m) return `${m}m ${pad(sec)}s`;
  return ms < 1000 ? `${ms} ms` : `${sec}s`;
}

const formatTime = (ms: number) => `${new Date(ms).toISOString().replace('T', ' ').slice(0, 19)} UTC`;

const hasParams = (params: unknown) =>
  params !== undefined &&
  params !== null &&
  !(typeof params === 'object' && !Array.isArray(params) && !Object.keys(params).length);

type LogKind = 'text' | 'code' | 'reason';
interface LogSection {
  label: string;
  text: string;
  kind: LogKind;
}

/**
 * Log contents shared by the HTML and Excel reports: method, parameters (if any), the expected response format
 * (from the schema), the actual response, and, for failures only, the failure reason and a sample response from the spec.
 */
export function logSections(r: ExecutionResult): LogSection[] {
  const sections: LogSection[] = [{ label: 'Method', text: methodLabel(r), kind: 'text' }];
  if (hasParams(r.params)) sections.push({ label: 'Parameters', text: pretty(r.params), kind: 'code' });
  if (r.expectedFormat)
    sections.push({ label: 'Expected response format (OpenRPC schema)', text: r.expectedFormat, kind: 'code' });
  sections.push({ label: 'Actual response', text: responseText(r), kind: 'code' });
  if (r.failureReason?.length)
    sections.push({ label: 'Failure reason', text: r.failureReason.join('\n'), kind: 'reason' });
  if (r.status === 'FAIL' && r.exampleResponse !== undefined)
    sections.push({ label: 'Sample response', text: exampleText(r), kind: 'code' });
  return sections;
}

/** Excel "Log" cell text. */
export function logText(r: ExecutionResult): string {
  return logSections(r)
    .map((s) => `${s.label}:\n${s.text}`)
    .join('\n\n');
}

function moduleSheet(name: string, results: ExecutionResult[]): XlsxSheet {
  return {
    name,
    freezeRows: 1,
    autoFilter: `A1:E${results.length + 1}`,
    columnWidths: [7, 42, 50, 11, 90],
    rowHeights: { 0: 22 },
    rows: [
      ['Sl No', 'APIs/Events', 'Description', 'Status', 'Log'].map((value) => ({ value, style: 'header' as const })),
      ...results.map((r, i) => [
        { value: i + 1, style: 'number' as const },
        methodLabel(r),
        r.description || '',
        { value: r.status, style: STATUS_STYLE[r.status] ?? 'number' },
        logText(r)
      ])
    ]
  };
}

function summarySheet(
  report: CertificationSuiteReport,
  name: string,
  modules: Array<{ module: string; sheet: string; counts: Counts; results: ExecutionResult[] }>
): XlsxSheet {
  const overall = countResults(report.results);
  const rows: XlsxCell[][] = [];
  const merges: string[] = [];
  const rowHeights: Record<number, number> = {};
  const add = (row: XlsxCell[], merge?: string) => {
    rows.push(row);
    if (merge) merges.push(merge.replace(/#/g, String(rows.length)));
  };
  const section = (title: string) => {
    add([]);
    add([{ value: title, style: 'section' }, ...Array(6).fill({ value: '', style: 'section' })]);
    rowHeights[rows.length - 1] = 22;
  };
  const detail = (label: string, value: XlsxCell) =>
    add(
      [
        { value: label, style: 'label' },
        typeof value === 'object' && value ? value : { value: value ?? '', style: 'value' },
        ...Array(5).fill({ value: '', style: 'value' })
      ],
      'B#:G#'
    );
  const count = (n: number, style: XlsxStyle): XlsxCell => ({ value: n, style: n ? style : 'number' });

  add([{ value: 'Firebolt Certification Report', style: 'title' }], 'A#:G#');
  rowHeights[0] = 34;
  add([{ value: 'Firebolt Schema Validator', style: 'subtitle' }], 'A#:G#');
  rowHeights[1] = 20;

  section('Run details');
  detail('Communication mode', report.mode);
  if (report.specVersion) detail('Version', report.specVersion);
  detail('Started', formatTime(report.startedAt));
  detail('Finished', formatTime(report.endedAt));
  detail('Duration', formatDuration(report.endedAt - report.startedAt));
  detail('Modules tested', String(modules.length));
  const status = overallStatus(report);
  detail('Overall status', { value: status, style: status === 'PASSED' ? 'pass' : 'fail' });
  if (report.interrupted) detail('Methods not run', String(report.methodsNotRun ?? 0));

  section('Results by module');
  add(
    ['Module', 'Total test cases', 'Passed', 'Failed', 'Validated APIs', 'Validated events', 'Pass rate'].map((value) => ({
      value,
      style: 'header' as const
    }))
  );
  rowHeights[rows.length - 1] = 22;
  const headerRow = rows.length - 1;
  const resultsSectionRow = headerRow - 1;
  for (const m of modules) {
    const v = validatedCounts(m.results);
    add([
      { value: m.module, style: 'link', link: m.sheet },
      { value: m.counts.total, style: 'number' },
      count(m.counts.passed, 'pass'),
      count(m.counts.failed, 'fail'),
      { value: v.validatedApis, style: 'number' },
      { value: v.validatedEvents, style: 'number' },
      passRate(m.counts)
    ]);
  }
  const v = validatedCounts(report.results);
  add([
    { value: 'Total', style: 'totalLabel' },
    ...[overall.total, overall.passed, overall.failed, v.validatedApis, v.validatedEvents].map((value) => ({
      value,
      style: 'total' as const
    })),
    passRate(overall, 'totalPercent')
  ]);
  const totalRow = rows.length - 1;

  // Success chart of the overall Passed/Failed totals (columns C and D of the Total row),
  // placed to the right of the Results by module table (from column I, leaving H as a gap), level with its heading.
  let chart: XlsxDoughnutChart | undefined;
  if (overall.total) {
    chart = {
      title: `Success rate ${((overall.passed / overall.total) * 100).toFixed(1)}%`,
      seriesName: 'Test cases',
      categories: [
        { label: 'Passed', cell: [headerRow, 2] },
        { label: 'Failed', cell: [headerRow, 3] }
      ],
      values: [
        { value: overall.passed, cell: [totalRow, 2] },
        { value: overall.failed, cell: [totalRow, 3] }
      ],
      colors: ['34A853', 'E5484D'],
      from: [resultsSectionRow, 8],
      to: [resultsSectionRow + 18, 13]
    };
  }

  return {
    name,
    rows,
    merges,
    rowHeights,
    showGridLines: false,
    defaultStyle: 'value',
    columnWidths: [30, 18, 14, 14, 16, 18, 14, 3],
    chart
  };
}

/** Excel workbook: a Summary sheet first, then one sheet per Firebolt module (e.g. Accessibility, Device). */
export function generateReportXlsx(report: CertificationSuiteReport): Uint8Array {
  const used = new Set<string>();
  const summaryName = safeSheetName('Summary', used);
  const modules = groupByModule(report.results).map(({ module, results }) => ({
    module,
    sheet: safeSheetName(module, used),
    results,
    counts: countResults(results)
  }));
  return buildXlsx([
    summarySheet(report, summaryName, modules),
    ...modules.map((m) => moduleSheet(m.sheet, m.results))
  ]);
}

const CONTENT_TYPES: Record<ReportFormat, string> = {
  json: 'application/json',
  html: 'text/html; charset=utf-8',
  xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
};

function reportBody(report: CertificationSuiteReport, format: ReportFormat): string | ArrayBuffer {
  if (format === 'xlsx') return generateReportXlsx(report).buffer as ArrayBuffer;
  return format === 'json' ? generateReportJson(report) : generateReportHtml(report);
}

function endpointFor(report: CertificationSuiteReport, format: ReportFormat): { url: string; fileName: string } | null {
  const fileName = reportFileName(report, format);
  const template = runtimeConfig.reportPublishUrl;
  if (!template) return null;
  const encoded = encodeURIComponent(fileName);
  let url = template
    .replace(/\{filename\}/g, encoded)
    .replace(/\{format\}/g, format)
    .replace(/\{reportId\}/g, encodeURIComponent(report.id));
  if (!/[?{]/.test(template) && template.endsWith('/')) url = `${template}${encoded}`;
  return { url, fileName };
}

const PORT_SCAN_RANGE = 20;
const PROBE_TIMEOUT_MS = 2500;
let resolvedPublishUrl = '';

async function isReportServer(url: URL): Promise<boolean> {
  const controller = typeof AbortController !== 'undefined' ? new AbortController() : undefined;
  const timer = setTimeout(() => controller?.abort(), PROBE_TIMEOUT_MS);
  try {
    const response = await fetch(new URL('health', url).toString(), { signal: controller?.signal });
    return response.ok && (await response.json()).service === 'firebolt-certification-report';
  } catch {
    return false;
  } finally {
    clearTimeout(timer);
  }
}

/**
 * The report server moves to the next free port when its default port is busy. While the default
 * publish URL is in use, find the port the server actually bound to and publish there.
 */
export async function resolveReportPublishUrl(): Promise<string> {
  const current = runtimeConfig.reportPublishUrl;
  if (current !== DEFAULT_REPORT_PUBLISH_URL && current !== resolvedPublishUrl) return current;
  let base: URL;
  try {
    base = new URL(DEFAULT_REPORT_PUBLISH_URL);
  } catch {
    return current;
  }
  const startPort = Number(base.port) || 80;
  const candidates = Array.from({ length: PORT_SCAN_RANGE }, (_, i) => {
    const candidate = new URL(base.toString());
    candidate.port = String(startPort + i);
    return candidate;
  });
  const found = (await Promise.all(candidates.map(isReportServer))).findIndex(Boolean);
  if (found >= 0) {
    resolvedPublishUrl = candidates[found].toString();
    runtimeConfig.reportPublishUrl = resolvedPublishUrl;
  }
  return runtimeConfig.reportPublishUrl;
}

const THUNDER_URL = 'http://127.0.0.1:9998/jsonrpc';
const IP_QUERY_METHOD = 'org.rdk.NetworkManager.GetIPSettings';
const IP_QUERY_PARAMS = { interface: 'eth0', ipversion: 'IPv4' };

/** The report server matches executions to devices by IP, so the app reports its own address from Thunder. */
async function resolveDeviceIp(signal: AbortSignal): Promise<string> {
  const response = await fetch(THUNDER_URL, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: IP_QUERY_METHOD, params: IP_QUERY_PARAMS }),
    signal
  });
  const body: unknown = await response.json();
  const ip = (body as { result?: { ipaddress?: unknown } }).result?.ipaddress;
  if (typeof ip === 'string' && /^[0-9a-fA-F:.]+$/.test(ip) && ip !== '0.0.0.0') return ip;
  throw new Error('Unable to determine the eth0 IP address from Thunder.');
}

export async function resolveAutomationContext(): Promise<void> {
  if (!runtimeConfig.autoRun || !runtimeConfig.reportPublishUrl) return;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 10000);
  try {
    const url = new URL('automation/context', runtimeConfig.reportPublishUrl);
    url.searchParams.set('deviceIp', await resolveDeviceIp(controller.signal));
    const response = await fetch(url.toString(), { cache: 'no-store', signal: controller.signal });
    if (response.status === 404) {
      console.info('No TDK execution registered for this device; using configured report naming.');
      return;
    }
    if (!response.ok) throw new Error(`TDK execution registration failed: HTTP ${response.status}`);
    const context: unknown = await response.json();
    if (
      typeof context !== 'object' || context === null ||
      !('reportingId' in context) || typeof context.reportingId !== 'string' ||
      !/^[A-Za-z0-9_-]{1,160}$/.test(context.reportingId)
    ) throw new Error('Report server returned an invalid TDK reportingId.');
    runtimeConfig.reportingId = context.reportingId;
  } finally {
    clearTimeout(timer);
  }
}

export async function publishReport(
  report: CertificationSuiteReport,
  format: ReportFormat
): Promise<ReportPublishResult> {
  const endpoint = endpointFor(report, format);
  const fileName = reportFileName(report, format);
  if (!endpoint) return { ok: false, format, fileName, message: 'No reportPublishUrl launch parameter configured.' };
  try {
    const body = reportBody(report, format);
    const response = await fetch(endpoint.url, {
      method: 'POST',
      headers: {
        'content-type': CONTENT_TYPES[format],
        'x-firebolt-certification-report-name': endpoint.fileName,
        'x-firebolt-certification-report-format': format
      },
      body
    });
    const text = await response.text();
    let returnedUrl = '';
    try {
      const parsed = JSON.parse(text);
      returnedUrl = parsed.url || parsed.reportUrl || parsed.location || '';
    } catch {
      returnedUrl = text.startsWith('http') ? text.trim() : '';
    }
    return {
      ok: response.ok,
      format,
      fileName,
      url: returnedUrl || endpoint.url,
      status: response.status,
      message: response.ok ? 'Report published successfully.' : `Report publish failed: HTTP ${response.status}`
    };
  } catch (error) {
    return {
      ok: false,
      format,
      fileName,
      url: endpoint.url,
      message: error instanceof Error ? error.message : String(error)
    };
  }
}
