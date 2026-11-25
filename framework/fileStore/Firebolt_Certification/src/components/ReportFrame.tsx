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
 * @file Renders a suite report's HTML inside an iframe, keeps its theme in sync with the app and makes it RCU-navigable.
 */

import { useLayoutEffect, useMemo, useRef } from 'preact/hooks';
import { generateReportHtml } from '../reports/ReportExporter';
import { handleNavigationKey } from './SpatialNavigation';
import type { CertificationSuiteReport } from '../types';

export type UiTheme = 'dark' | 'light';

/** Disables CSS transitions on a document for a moment so a theme switch repaints everything at once instead of fading piece by piece. */
export function suppressTransitions(root: HTMLElement | null | undefined) {
  if (!root) return;
  root.classList.add('no-motion');
  window.setTimeout(() => root.classList.remove('no-motion'), 100);
}

/** Report controls reachable with the RCU: filter cards, module filter, search, expand/collapse and each example/log cell. */
const NAVIGABLE = '.card, #f-module, .dd-opt, #f-search, button.tool, .clip';

function applyTheme(frame: HTMLIFrameElement | null, theme: UiTheme) {
  const root = frame?.contentDocument?.documentElement;
  if (root && root.classList.contains('light') !== (theme === 'light')) suppressTransitions(root);
  root?.classList.toggle('light', theme === 'light');
}

/** Renders the exact HTML report that is generated/published for a suite run, themed and navigable like the rest of the app. */
export function ReportFrame({ report, theme }: { report: CertificationSuiteReport; theme: UiTheme }) {
  const ref = useRef<HTMLIFrameElement>(null);
  const themeRef = useRef(theme);
  themeRef.current = theme;
  // The logo is only for the downloaded/published report, not this in-app view. Built with the current theme so the first paint is already correct; later theme switches are applied in place below without reloading the frame.
  const html = useMemo(() => generateReportHtml(report, themeRef.current, false), [report]);
  // Layout effect: applied in the same commit as the app's theme class, so the report repaints in the same frame.
  useLayoutEffect(() => applyTheme(ref.current, theme), [theme]);

  function onLoad() {
    const frame = ref.current;
    const doc = frame?.contentDocument;
    const win = frame?.contentWindow;
    if (!doc || !win) return;
    applyTheme(frame, theme);
    doc.querySelectorAll<HTMLElement>(NAVIGABLE).forEach((el) => el.setAttribute('data-focusable', 'true'));
    // Capture phase on the frame window runs before the report's own handlers, so OK is not handled twice.
    win.addEventListener(
      'keydown',
      (e: KeyboardEvent) => {
        const target = e.target as HTMLElement | null;
        const typing = target?.tagName === 'INPUT';
        // Let the search box keep normal text editing keys.
        if (typing && (e.key === 'Backspace' || e.key === 'ArrowLeft' || e.key === 'ArrowRight')) return;
        // Back inside an open dropdown closes it (handled by the report) instead of leaving the report.
        const isBack =
          e.key === 'Escape' ||
          e.key === 'Backspace' ||
          e.key === 'BrowserBack' ||
          e.keyCode === 461 ||
          e.keyCode === 8;
        if (isBack && target?.closest?.('.dd-menu:not([hidden])')) {
          e.preventDefault();
          e.stopPropagation();
          target.ownerDocument.getElementById('f-module')?.click();
          target.ownerDocument.getElementById('f-module')?.focus();
          return;
        }
        if (handleNavigationKey(e)) e.stopPropagation();
      },
      true
    );
  }

  return (
    <iframe
      ref={ref}
      class="report-frame"
      title={report.title}
      srcDoc={html}
      data-scroll-region="true"
      onLoad={onLoad}
    />
  );
}
