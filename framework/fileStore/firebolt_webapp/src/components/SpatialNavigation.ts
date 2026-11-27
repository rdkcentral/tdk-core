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
 * @file Remote-control (arrow key) spatial navigation: moves focus to the nearest focusable element, scrolls
 * readable regions and reaches into the embedded report iframe.
 */

const FRAME_SELECTOR = 'iframe.report-frame';

function frameDocuments(): Document[] {
  return Array.from(document.querySelectorAll<HTMLIFrameElement>(FRAME_SELECTOR))
    .filter((f) => f.offsetParent !== null)
    .map((f) => {
      try {
        return f.contentDocument;
      } catch {
        return null;
      }
    })
    .filter((d): d is Document => !!d);
}
function focusables(): HTMLElement[] {
  const all: HTMLElement[] = [];
  for (const d of [document, ...frameDocuments()])
    all.push(...Array.from(d.querySelectorAll<HTMLElement>('[data-focusable="true"]')));
  return all.filter((el) => !el.hasAttribute('disabled') && el.offsetParent !== null);
}
/** The focused element, looking inside the embedded report frame when it has focus. */
function activeElement(): HTMLElement | null {
  const a = document.activeElement;
  if (a instanceof HTMLIFrameElement) {
    try {
      const inner = a.contentDocument?.activeElement;
      if (inner && inner !== a.contentDocument?.body) return inner as HTMLElement;
    } catch {
      /* cross-origin */
    }
  }
  return a as HTMLElement | null;
}
/** Bounding rect in top-level viewport coordinates (adds the frame offset for elements inside the report). */
function rect(el: HTMLElement) {
  const r = el.getBoundingClientRect();
  const frame = el.ownerDocument.defaultView?.frameElement as HTMLElement | null;
  if (!frame || el.ownerDocument === document) return r;
  const f = frame.getBoundingClientRect();
  const dx = f.left + frame.clientLeft,
    dy = f.top + frame.clientTop;
  return {
    left: r.left + dx,
    top: r.top + dy,
    width: r.width,
    height: r.height,
    bottom: r.bottom + dy,
    right: r.right + dx
  };
}
function center(el: HTMLElement) {
  const r = rect(el);
  return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
}
function ensureVisible(el: HTMLElement) {
  try {
    el.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  } catch {
    el.scrollIntoView(false);
  }
}
function focus(el: HTMLElement | undefined) {
  if (!el) return;
  if (el.ownerDocument === document && activeElement()?.ownerDocument !== document) window.focus();
  el.focus();
  ensureVisible(el);
}
/** A focused read-only box (focusable scroll region) scrolls its own content until it reaches the edge. */
function scrollFocusedBox(el: HTMLElement, sign: 1 | -1): boolean {
  if (el.getAttribute('data-scroll-region') !== 'true') return false;
  const room = sign > 0 ? el.scrollHeight - el.clientHeight - el.scrollTop : el.scrollTop;
  if (room <= 1) return false;
  el.scrollTop += sign * Math.max(40, Math.round(el.clientHeight * 0.8));
  return true;
}
function move(direction: 'up' | 'down' | 'left' | 'right') {
  const items = focusables();
  if (!items.length) return;
  const active = activeElement();
  const current = active && items.includes(active) ? active : items[0];
  if (active !== current) {
    focus(current);
    return;
  }
  if ((direction === 'up' || direction === 'down') && scrollFocusedBox(current, direction === 'down' ? 1 : -1)) return;
  const vertical = direction === 'up' || direction === 'down';
  const a = center(current),
    ar = rect(current);
  let best: { el: HTMLElement; score: number } | null = null;
  for (const el of items) {
    if (el === current) continue;
    const b = center(el);
    const dx = b.x - a.x,
      dy = b.y - a.y;
    if (direction === 'up' && dy >= -4) continue;
    if (direction === 'down' && dy <= 4) continue;
    if (direction === 'left' && dx >= -4) continue;
    if (direction === 'right' && dx <= 4) continue;
    const primary = vertical ? Math.abs(dy) : Math.abs(dx);
    const secondary = vertical ? Math.abs(dx) : Math.abs(dy);
    // Up/Down stays in the same column: items that horizontally overlap the current one win over items in other columns.
    const br = vertical ? rect(el) : null;
    const outOfColumn = !!br && (br.right <= ar.left || br.left >= ar.right);
    const score = primary + secondary * 2.4 + (outOfColumn ? 1e6 : 0);
    if (!best || score < best.score) best = { el, score };
  }
  focus(best?.el);
}
function backToMenu() {
  const active =
    document.querySelector<HTMLElement>('.sidebar .nav-item.active') ||
    document.querySelector<HTMLElement>('.sidebar .nav-item');
  focus(active || undefined);
}
function scrollRegion(delta: number) {
  const active = activeElement();
  const report = document.querySelector<HTMLIFrameElement>(FRAME_SELECTOR);
  // The embedded HTML report is the primary scroll target on pages that show one.
  if (report && !active?.closest('.selection-list')) {
    report.contentWindow?.scrollBy(0, delta);
    return;
  }
  const region =
    active?.closest<HTMLElement>('[data-scroll-region="true"]') ||
    document.querySelector<HTMLElement>('[data-scroll-region="true"]');
  if (!region) return;
  region.scrollTop += delta;
  // Keep RCU focus inside the visible part of a long list so the next arrow press continues from what is on screen.
  const box = region.getBoundingClientRect();
  const visible = focusables()
    .filter((el) => region.contains(el))
    .filter((el) => {
      const r = el.getBoundingClientRect();
      return r.top >= box.top - 1 && r.bottom <= box.bottom + 1;
    });
  if (!visible.length || (active && visible.includes(active))) return;
  (delta > 0 ? visible[0] : visible[visible.length - 1]).focus({ preventScroll: true } as FocusOptions);
}
/** Handles an RCU/keyboard key. Returns true when the key was consumed. */
export function handleNavigationKey(e: KeyboardEvent): boolean {
  const key = e.key;
  const map: Record<string, 'up' | 'down' | 'left' | 'right'> = {
    ArrowUp: 'up',
    ArrowDown: 'down',
    ArrowLeft: 'left',
    ArrowRight: 'right'
  };
  if (map[key]) {
    e.preventDefault();
    move(map[key]);
    return true;
  }
  if (key === 'Enter' || key === 'OK' || e.keyCode === 13) {
    e.preventDefault();
    const active = activeElement();
    if (active && typeof active.click === 'function') active.click();
    return true;
  }
  if (key === 'Backspace' || key === 'Escape' || key === 'BrowserBack' || e.keyCode === 461 || e.keyCode === 8) {
    e.preventDefault();
    backToMenu();
    return true;
  }
  if (key === 'PageDown') {
    e.preventDefault();
    scrollRegion(260);
    return true;
  }
  if (key === 'PageUp') {
    e.preventDefault();
    scrollRegion(-260);
    return true;
  }
  return false;
}
/** Focus the first visible focusable matching `selector` after the next render (used after list/selection changes). */
export function focusSelector(selector: string): void {
  window.setTimeout(() => {
    const el = focusables().find((e) => e.matches(selector));
    if (el) focus(el);
  }, 0);
}
export function installSpatialNavigation(): () => void {
  const handler = (e: KeyboardEvent) => {
    handleNavigationKey(e);
  };
  window.addEventListener('keydown', handler);
  window.setTimeout(() => focus(focusables()[0]), 80);
  return () => window.removeEventListener('keydown', handler);
}
