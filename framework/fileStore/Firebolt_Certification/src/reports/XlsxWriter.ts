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

// Minimal .xlsx (Office Open XML) writer: inline-string cells packed into an uncompressed ZIP by fflate.

import { zipSync, type Zippable } from 'fflate';

/** Built-in cell styles; see STYLES for the matching cellXfs entries (same order). */
export type XlsxStyle =
  | 'default'
  | 'header'
  | 'body'
  | 'title'
  | 'section'
  | 'label'
  | 'value'
  | 'number'
  | 'pass'
  | 'fail'
  | 'percent'
  | 'link'
  | 'total'
  | 'totalLabel'
  | 'totalPercent';
const STYLE_INDEX: Record<XlsxStyle, number> = {
  default: 0,
  header: 1,
  body: 2,
  title: 3,
  section: 4,
  label: 5,
  value: 6,
  number: 7,
  pass: 8,
  fail: 9,
  percent: 10,
  link: 11,
  total: 12,
  totalLabel: 13,
  totalPercent: 14
};

export type XlsxCell =
  | string
  | number
  | null
  | undefined
  | { value: string | number; style?: XlsxStyle; /** Name of a sheet in this workbook to link to. */ link?: string };

export interface XlsxSheet {
  name: string;
  rows: XlsxCell[][];
  columnWidths?: number[];
  /** Style for plain string/number cells (default 'body'). */
  defaultStyle?: XlsxStyle;
  /** Number of top rows to freeze. */
  freezeRows?: number;
  /** Range such as "A1:F20" to enable column filters on. */
  autoFilter?: string;
  merges?: string[];
  /** Row heights in points, keyed by 0-based row index. */
  rowHeights?: Record<number, number>;
  showGridLines?: boolean;
}

const MAX_CELL_CHARS = 32767;
const encoder = new TextEncoder();

function xml(value: string): string {
  return value
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\uFFFE\uFFFF]/g, '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function columnName(index: number): string {
  let name = '';
  for (let n = index + 1; n > 0; n = Math.floor((n - 1) / 26)) name = String.fromCharCode(65 + ((n - 1) % 26)) + name;
  return name;
}

/** Returns a valid, workbook-unique sheet name (max 31 chars, no []:*?/\' characters, case-insensitive unique). */
export function safeSheetName(name: string, used: Set<string>): string {
  const base = (name.replace(/[\\/?*[\]:']/g, ' ').trim() || 'Sheet').slice(0, 31);
  let candidate = base;
  for (let i = 2; used.has(candidate.toLowerCase()); i++)
    candidate = `${base.slice(0, 31 - String(i).length - 1)}~${i}`;
  used.add(candidate.toLowerCase());
  return candidate;
}

const absolute = (range: string) => range.replace(/([A-Z]+)(\d+)/g, '$$$1$$$2');

function cellXml(cell: XlsxCell, ref: string, fallback: XlsxStyle): string {
  if (cell === null || cell === undefined || cell === '') return '';
  const { value, style } = typeof cell === 'object' ? cell : { value: cell, style: undefined };
  const s = STYLE_INDEX[style ?? fallback];
  if (typeof value === 'number') return Number.isFinite(value) ? `<c r="${ref}" s="${s}"><v>${value}</v></c>` : '';
  const text = value.length > MAX_CELL_CHARS ? `${value.slice(0, MAX_CELL_CHARS - 15)}…[truncated]` : value;
  return `<c r="${ref}" t="inlineStr" s="${s}"><is><t xml:space="preserve">${xml(text)}</t></is></c>`;
}

function sheetXml(sheet: XlsxSheet): string {
  const fallback = sheet.defaultStyle ?? 'body';
  const grid = sheet.showGridLines === false ? ' showGridLines="0"' : '';
  const freeze = sheet.freezeRows
    ? `<pane ySplit="${sheet.freezeRows}" topLeftCell="A${sheet.freezeRows + 1}" activePane="bottomLeft" state="frozen"/>`
    : '';
  const views = `<sheetViews><sheetView workbookViewId="0"${grid}>${freeze}</sheetView></sheetViews>`;
  const cols = sheet.columnWidths?.length
    ? `<cols>${sheet.columnWidths.map((w, i) => `<col min="${i + 1}" max="${i + 1}" width="${w}" customWidth="1"/>`).join('')}</cols>`
    : '';
  const links: string[] = [];
  const rows = sheet.rows
    .map((row, r) => {
      const height = sheet.rowHeights?.[r];
      const cells = row
        .map((cell, c) => {
          const ref = `${columnName(c)}${r + 1}`;
          if (cell && typeof cell === 'object' && cell.link)
            links.push(
              `<hyperlink ref="${ref}" location="${xml(`'${cell.link}'!A1`)}" display="${xml(String(cell.value))}"/>`
            );
          return cellXml(cell, ref, fallback);
        })
        .join('');
      return `<row r="${r + 1}"${height ? ` ht="${height}" customHeight="1"` : ''}>${cells}</row>`;
    })
    .join('');
  const filter = sheet.autoFilter ? `<autoFilter ref="${sheet.autoFilter}"/>` : '';
  const merges = sheet.merges?.length
    ? `<mergeCells count="${sheet.merges.length}">${sheet.merges.map((m) => `<mergeCell ref="${m}"/>`).join('')}</mergeCells>`
    : '';
  const hyperlinks = links.length ? `<hyperlinks>${links.join('')}</hyperlinks>` : '';
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">${views}<sheetFormatPr defaultRowHeight="15"/>${cols}<sheetData>${rows}</sheetData>${filter}${merges}${hyperlinks}<pageMargins left="0.5" right="0.5" top="0.75" bottom="0.75" header="0.3" footer="0.3"/><pageSetup orientation="landscape" fitToWidth="1" fitToHeight="0"/></worksheet>`;
}

const NAVY = 'FF1F3864';
const GRID = 'FFBFBFBF';
const thin = `<left style="thin"><color rgb="${GRID}"/></left><right style="thin"><color rgb="${GRID}"/></right><top style="thin"><color rgb="${GRID}"/></top><bottom style="thin"><color rgb="${GRID}"/></bottom><diagonal/>`;
const font = (opts: string, color?: string, size = 11) =>
  `<font>${opts}<sz val="${size}"/>${color ? `<color rgb="${color}"/>` : ''}<name val="Calibri"/><family val="2"/></font>`;
const fill = (rgb: string) =>
  `<fill><patternFill patternType="solid"><fgColor rgb="${rgb}"/><bgColor indexed="64"/></patternFill></fill>`;
const xf = (fontId: number, fillId: number, borderId: number, align = '', numFmtId = 0) =>
  `<xf numFmtId="${numFmtId}" fontId="${fontId}" fillId="${fillId}" borderId="${borderId}" xfId="0" applyFont="1" applyFill="1" applyBorder="1"${numFmtId ? ' applyNumberFormat="1"' : ''}${align ? ` applyAlignment="1"><alignment ${align}/></xf>` : '/>'}`;

// fonts: 0 normal, 1 header (bold white), 2 title, 3 section, 4 bold, 5 pass, 6 fail, 7 link
const FONTS = [
  font(''),
  font('<b/>', 'FFFFFFFF'),
  font('<b/>', NAVY, 18),
  font('<b/>', NAVY, 13),
  font('<b/>'),
  font('<b/>', 'FF006100'),
  font('<b/>', 'FF9C0006'),
  font('<u/>', 'FF0563C1')
];
// fills: 0 none, 1 gray125 (both required), 2 navy, 3 light grey, 4 green, 5 red, 6 light blue
const FILLS = [
  '<fill><patternFill patternType="none"/></fill>',
  '<fill><patternFill patternType="gray125"/></fill>',
  fill(NAVY),
  fill('FFF2F2F2'),
  fill('FFC6EFCE'),
  fill('FFFFC7CE'),
  fill('FFD9E1F2')
];
// borders: 0 none, 1 thin grid, 2 navy underline
const BORDERS = [
  '<border><left/><right/><top/><bottom/><diagonal/></border>',
  `<border>${thin}</border>`,
  `<border><left/><right/><top/><bottom style="medium"><color rgb="${NAVY}"/></bottom><diagonal/></border>`
];
const PERCENT = 164;
const top = 'vertical="top" wrapText="1"';
const centered = 'horizontal="center" vertical="top"';
const XFS = [
  xf(0, 0, 0), // default
  xf(1, 2, 1, 'horizontal="center" vertical="center" wrapText="1"'), // header
  xf(0, 0, 1, top), // body
  xf(2, 0, 0, 'vertical="center"'), // title
  xf(3, 0, 2, 'vertical="bottom"'), // section
  xf(4, 3, 1, 'vertical="top"'), // label
  xf(0, 0, 1, top), // value
  xf(0, 0, 1, centered), // number
  xf(5, 4, 1, centered), // pass
  xf(6, 5, 1, centered), // fail
  xf(0, 0, 1, centered, PERCENT), // percent
  xf(7, 0, 1, 'vertical="top"'), // link
  xf(4, 6, 1, centered), // total
  xf(4, 6, 1, 'vertical="top"'), // totalLabel
  xf(4, 6, 1, centered, PERCENT) // totalPercent
];

const STYLES = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="1"><numFmt numFmtId="${PERCENT}" formatCode="0.0%"/></numFmts>
<fonts count="${FONTS.length}">${FONTS.join('')}</fonts>
<fills count="${FILLS.length}">${FILLS.join('')}</fills>
<borders count="${BORDERS.length}">${BORDERS.join('')}</borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="${XFS.length}">${XFS.join('')}</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>`;

function packageFiles(sheets: XlsxSheet[]): Array<[string, string]> {
  const definedNames = sheets
    .map((s, i) =>
      s.autoFilter
        ? `<definedName name="_xlnm._FilterDatabase" localSheetId="${i}" hidden="1">${xml(`'${s.name}'!${absolute(s.autoFilter)}`)}</definedName>`
        : ''
    )
    .join('');
  return [
    [
      '[Content_Types].xml',
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>${sheets.map((_, i) => `<Override PartName="/xl/worksheets/sheet${i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join('')}</Types>`
    ],
    [
      '_rels/.rels',
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`
    ],
    [
      'xl/workbook.xml',
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><bookViews><workbookView activeTab="0"/></bookViews><sheets>${sheets.map((s, i) => `<sheet name="${xml(s.name)}" sheetId="${i + 1}" r:id="rId${i + 1}"/>`).join('')}</sheets>${definedNames ? `<definedNames>${definedNames}</definedNames>` : ''}</workbook>`
    ],
    [
      'xl/_rels/workbook.xml.rels',
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${sheets.map((_, i) => `<Relationship Id="rId${i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i + 1}.xml"/>`).join('')}<Relationship Id="rId${sheets.length + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`
    ],
    ['xl/styles.xml', STYLES],
    ...sheets.map((s, i) => [`xl/worksheets/sheet${i + 1}.xml`, sheetXml(s)] as [string, string])
  ];
}

export function buildXlsx(sheets: XlsxSheet[]): Uint8Array {
  const files: Zippable = {};
  for (const [name, content] of packageFiles(sheets)) files[name] = encoder.encode(content);
  // Stored (uncompressed) entries keep the package simple to inspect; .xlsx readers accept either.
  return zipSync(files, { level: 0 });
}
