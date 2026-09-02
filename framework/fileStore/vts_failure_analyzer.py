#!/usr/bin/env python3
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################
"""Analyze a CUnit/UT failure log and reconstruct the failing test function
code up to the failing assertion.

It works out three things from the log:
  1. The failing source file and line number (from the ``UT_ASSERT*`` line).
  2. The test function that was running (from the ``In <function> [..]`` line).
  3. The relevant C statements of that function, up to and including the
     failing line, with the noise removed:
       - the ``gTestID = ..;`` line is ignored
       - every ``UT_LOG_*`` print statement is ignored

Usage:
    Paste the failure log into the FAILURE_LOG multiline string below, set
    SOURCE_DIR to the directory that holds the HAL test source, then run:
        python analyze_failure.py
"""

import os
import re
import sys

# ---------------------------------------------------------------------------
# Configuration: paste the failure log here and point SOURCE_DIR at the source.
# ---------------------------------------------------------------------------
SOURCE_DIR = ""

FAILURE_LOG = ""

CONFIG_YAML = r""

# Log line that records the failure. Two forms are supported:
#   ... ASSERT , test_l2_dsAudio.c,  2034 : UT_ASSERT_EQUAL:"capabilities"
#   ... FAIL   , test_l2_dsHost.c,    186 : Invalid SocID
# Group 1 = level (ASSERT|FAIL), 2 = file, 3 = line, 4 = detail (macro / message).
FAILURE_RE = re.compile(
    r",\s*(ASSERT|FAIL)\s*,\s*([\w./-]+\.c)\s*,\s*(\d+)\s*:\s*(.+?)\s*$",
    re.IGNORECASE,
)

# Log line that records the running function, e.g.
#   ... : In test_l2_dsAudio_GetAudioCapabilities [02027]
FUNCTION_RE = re.compile(r"\bIn\s+(\w+)\s*\[")

# Statements to drop from the reconstructed function body: every UT_* macro
# (UT_LOG_*, UT_ASSERT_*, ...) and the gTestID bookkeeping line. The single
# failing assertion is re-added afterwards.
UT_MACRO_RE = re.compile(r"^\s*UT_\w*\s*\(")
GTESTID_RE = re.compile(r"^\s*gTestID\b")

# CHECK_FOR_EXTENDED_ERROR_CODE(result, enhanced, old) — assertion macro that
# picks between two error codes depending on extendedEnumsSupported.
CHECK_EXTENDED_RE = re.compile(
    r"CHECK_FOR_EXTENDED_ERROR_CODE\s*\(\s*(\w+)\s*,\s*(\w+)\s*,\s*(\w+)\s*\)"
)


#-------------------------------------------------------------------------
# Function:    parse_log
# Description: Parses the CUnit/UT failure log to extract the failing
#              source file, line number, failure kind, detail message,
#              and the running test function name.
# Parameters:
#              - text: The raw CUnit/UT failure log text.
# Return:
#              - tuple: (source_file, line_no, failure_kind, detail,
#                        function_name).
#-------------------------------------------------------------------------
def parse_log(text):
    """Return (source_file, line_no, failure_kind, detail, function_name) from the log."""
    source_file = line_no = failure_kind = detail = function_name = None

    for line in text.splitlines():
        m = FUNCTION_RE.search(line)
        if m:
            function_name = m.group(1)
        m = FAILURE_RE.search(line)
        if m:
            failure_kind = m.group(1).upper()
            source_file = os.path.basename(m.group(2))
            line_no = int(m.group(3))
            detail = m.group(4)

    if not (source_file and line_no):
        sys.exit("ERROR: could not find a UT_ASSERT or FAIL failure line in the log.")
    if not function_name:
        sys.exit("ERROR: could not find the running function ('In <function> [..]') in the log.")

    return source_file, line_no, failure_kind, detail, function_name


#-------------------------------------------------------------------------
# Function:    find_source
# Description: Locates the given source file within a directory tree,
#              searching recursively when not found directly.
# Parameters:
#              - source_file: Name of the source file to locate.
#              - source_dir: Directory to search under.
# Return:
#              - str: Absolute path to the located source file.
#-------------------------------------------------------------------------
def find_source(source_file, source_dir):
    """Locate source_file under source_dir (recursively)."""
    direct = os.path.join(source_dir, source_file)
    if os.path.isfile(direct):
        return direct
    for root, _dirs, files in os.walk(source_dir):
        if source_file in files:
            return os.path.join(root, source_file)
    sys.exit(f"ERROR: source file '{source_file}' not found under '{source_dir}'.")


#-------------------------------------------------------------------------
# Function:    find_function_body_start
# Description: Finds the line index immediately after a function's opening
#              brace, distinguishing the definition from call sites.
# Parameters:
#              - lines: List of source lines.
#              - function_name: Name of the function to locate.
# Return:
#              - int: 0-based index of the line after the opening '{'.
#-------------------------------------------------------------------------
def find_function_body_start(lines, function_name):
    """Return the 0-based index of the line right after the function's '{'.

    Matches a definition ('<type> <function>(') and skips call sites where the
    name is not immediately followed by '('.
    """
    def_re = re.compile(r"^\s*[\w\*]+[\w\s\*]*\b" + re.escape(function_name) + r"\s*\(")
    for i, line in enumerate(lines):
        if def_re.match(line):
            # Find the opening brace on this or a following line.
            for j in range(i, len(lines)):
                if "{" in lines[j]:
                    return j + 1
    sys.exit(f"ERROR: definition of function '{function_name}' not found in source.")


#-------------------------------------------------------------------------
# Function:    strip_comments
# Description: Removes C-style block and line comments from a source line
#              and trims surrounding whitespace.
# Parameters:
#              - text: The source text to strip comments from.
# Return:
#              - str: The text with comments removed.
#-------------------------------------------------------------------------
def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", "", text)
    text = re.sub(r"//.*$", "", text)
    return text.strip()


#-------------------------------------------------------------------------
# Function:    collect_statements
# Description: Groups source lines between the function body start and the
#              failing line into logical statements, dropping UT_LOG_*
#              prints and the gTestID bookkeeping line.
# Parameters:
#              - lines: List of source lines.
#              - body_start: 0-based index of the function body start.
#              - failure_line: 1-based line number of the failure.
# Return:
#              - list: Cleaned logical statements up to the failure.
#-------------------------------------------------------------------------
def collect_statements(lines, body_start, failure_line):
    """Group source lines [body_start, failure_line] into logical statements,
    dropping UT_LOG_* prints and the gTestID line.
    """
    kept = []
    buffer = ""

    # failure_line is 1-based; body_start is 0-based index.
    for idx in range(body_start, failure_line):
        raw = strip_comments(lines[idx])
        if not raw:
            continue
        buffer = (buffer + " " + raw).strip() if buffer else raw
        # A statement is complete when it ends with ; { or }.
        if buffer.endswith((";", "{", "}")):
            statement = re.sub(r"\s+", " ", buffer)
            buffer = ""
            if UT_MACRO_RE.match(statement) or GTESTID_RE.match(statement):
                continue
            kept.append(statement)

    if buffer:
        statement = re.sub(r"\s+", " ", buffer.strip())
        if not (UT_MACRO_RE.match(statement) or GTESTID_RE.match(statement)):
            kept.append(statement)

    return prune_empty_blocks(kept)


#-------------------------------------------------------------------------
# Function:    prune_empty_blocks
# Description: Removes blocks left empty after UT_* / gTestID lines were
#              stripped, collapsing nested empty blocks repeatedly.
# Parameters:
#              - statements: List of logical statements.
# Return:
#              - list: Statements with empty blocks removed.
#-------------------------------------------------------------------------
def prune_empty_blocks(statements):
    """Drop blocks left empty after UT_* / gTestID lines were removed, i.e. an
    opening-brace statement ('if (...) {', 'for (...) {', ...) immediately
    followed by its closing '}'. Repeats to collapse nested empty blocks.
    """
    changed = True
    while changed:
        changed = False
        pruned = []
        i = 0
        while i < len(statements):
            cur = statements[i]
            nxt = statements[i + 1] if i + 1 < len(statements) else None
            if cur.endswith("{") and nxt is not None and nxt.strip() == "}":
                # Empty block: skip both the opener and its closer.
                i += 2
                changed = True
                continue
            pruned.append(cur)
            i += 1
        statements = pruned
    return statements


#-------------------------------------------------------------------------
# Function:    failing_statement
# Description: Reconstructs the complete C statement that ends at the
#              failing line, including any continuation lines.
# Parameters:
#              - lines: List of source lines.
#              - failure_line: 1-based line number of the failure.
# Return:
#              - str: The reconstructed failing statement.
#-------------------------------------------------------------------------
def failing_statement(lines, failure_line):
    """Reconstruct the C statement that ends at the failing line number."""
    buffer = ""
    # Walk backwards to include any continuation lines of a multi-line assert.
    start = failure_line - 1
    while start > 0:
        prev = strip_comments(lines[start - 1])
        if not prev or prev.endswith((";", "{", "}")):
            break
        start -= 1
    for idx in range(start, failure_line):
        raw = strip_comments(lines[idx])
        if not raw:
            continue
        buffer = (buffer + " " + raw).strip() if buffer else raw
    return re.sub(r"\s+", " ", buffer)


# C keywords that begin a control-flow statement rather than an API call.

CONTROL_KEYWORDS = {"if", "for", "while", "switch", "else", "do", "return", "sizeof"}
CALLEE_RE = re.compile(r"(\w+)\s*\(")

# C primitive type tokens that signal a variable declaration.
_C_TYPE_TOKENS = {
    "int", "char", "bool", "float", "double", "void", "long", "short",
    "unsigned", "signed", "const", "static", "extern", "volatile",
    "struct", "enum", "union", "auto", "register",
}


#-------------------------------------------------------------------------
# Function:    _declaration_variable
# Description: Detects whether a statement is a C variable declaration and
#              returns the declared variable name when it is.
# Parameters:
#              - statement: The C statement to inspect.
# Return:
#              - str: The variable name, or None if not a declaration.
#-------------------------------------------------------------------------
def _declaration_variable(statement):
    """If *statement* looks like a C variable declaration, return the variable name.

    Recognises:
      int handle = 0;
      HDMI_CEC_STATUS result = HDMI_CEC_IO_SUCCESS;
      intptr_t handle = 0;
      bool isConnected = false;

    Returns None when the statement is not a declaration.
    """
    tokens = re.findall(r"\b([A-Za-z_]\w*)\b", statement)
    if len(tokens) < 2:
        return None
    first = tokens[0]
    # The first token must look like a C type:
    #   - known primitive keyword
    #   - ends with _t  (e.g. dsError_t, intptr_t)
    #   - UPPER_CASE_WITH_UNDERSCORES  (e.g. HDMI_CEC_STATUS)
    is_type = (
        first in _C_TYPE_TOKENS
        or first.endswith("_t")
        or (first == first.upper() and "_" in first and len(first) > 2)
    )
    if not is_type:
        return None
    return tokens[1]  # second token = variable name


#-------------------------------------------------------------------------
# Function:    failure_flow
# Description: Reduces the full function flow to the essential API-call
#              sequence, dropping declarations, control-flow, and test
#              infrastructure helpers, and prepends referenced declarations.
# Parameters:
#              - statements: List of logical statements from the function.
#              - fail_stmt: The failing statement, always appended last.
# Return:
#              - list: The reduced API-call flow leading to the failure.
#-------------------------------------------------------------------------
def failure_flow(statements, fail_stmt):
    """Reduce the full function flow to the essential API-call sequence.

    Keeps statements that invoke a device-under-test API (an assignment or bare
    call), dropping variable declarations, control-flow, and test-infrastructure
    helpers (ut_*/UT_* macros and kvp/profile reads). The failing statement is
    always appended last.

    After building the API-call sequence, any declared variable that is
    referenced in the flow is prepended as a declaration line so the reader
    can see initial values (e.g. ``int handle = 0;``).
    """
    decl_map = {}   # variable_name -> declaration statement
    # Common return-value variable names — their declarations are skipped since
    # every API call overwrites them and showing the initial value adds no value.
    RETURN_VAR_NAMES = {"ret", "result", "status", "rc", "retVal", "retval", "returnStatus"}
    flow = []
    for statement in statements:
        if statement == fail_stmt:
            continue
        m = CALLEE_RE.search(statement)
        if not m:
            # No function-call pattern — could be a declaration; record it.
            var = _declaration_variable(statement)
            if var and var not in RETURN_VAR_NAMES:
                decl_map[var] = statement
            continue
        callee = m.group(1)
        if callee in CONTROL_KEYWORDS:
            continue
        lowered = callee.lower()
        if lowered.startswith("ut_") and not lowered.startswith("ut_kvp_get"):
            continue  # drop UT_* macros / ut helpers, but keep ut_kvp_get*Field
        if callee == "CHECK_FOR_EXTENDED_ERROR_CODE":
            continue  # assertion macro — filtered here, re-added if it is fail_stmt
        flow.append(statement)
    if fail_stmt:
        # Surface the condition on the line before the failing assert/fail.
        # If that preceding statement is an `if (...)`, render it in words
        # (e.g. `if(!isConnected)` -> `if not isConnected`).
        idx = statements.index(fail_stmt) if fail_stmt in statements else len(statements)
        if idx > 0:
            condition = render_condition(statements[idx - 1])
            if condition:
                flow.append(condition)
        flow.append(fail_stmt)

    # Prepend declarations for variables that are actually referenced in the flow.
    if decl_map and flow:
        flow_text = " ".join(flow)
        needed = {
            var: stmt for var, stmt in decl_map.items()
            if re.search(r"\b" + re.escape(var) + r"\b", flow_text)
        }
        if needed:
            # Preserve the original source order of declarations.
            ordered = [s for s in statements if s in needed.values()]
            flow = ordered + flow

    return flow


# ---------------------------------------------------------------------------
# YAML profile parsing + config-reference resolution.
# ---------------------------------------------------------------------------

# A config reference in test code, e.g. gDSVideoPortConfiguration[port].typeid
CONFIG_REF_RE = re.compile(r"g(\w+?)Configuration\s*\[\s*(\w+)\s*\]\s*\.\s*(\w+)")


#-------------------------------------------------------------------------
# Function:    _strip_yaml_comment
# Description: Removes a trailing ' # ...' comment from a YAML value while
#              preserving '#' characters that appear inside quotes.
# Parameters:
#              - value: The raw YAML value string.
# Return:
#              - str: The value with any trailing comment removed.
#-------------------------------------------------------------------------
def _strip_yaml_comment(value):
    """Remove a trailing ' # ...' comment that is not inside quotes."""
    in_quote = None
    for i, ch in enumerate(value):
        if ch in ("'", '"'):
            if in_quote is None:
                in_quote = ch
            elif in_quote == ch:
                in_quote = None
        elif ch == "#" and in_quote is None and (i == 0 or value[i - 1] in " \t"):
            return value[:i].strip()
    return value.strip()


#-------------------------------------------------------------------------
# Function:    parse_yaml
# Description: Minimal indentation-based YAML parser supporting the
#              mapping subset used by device profiles, preserving scalar
#              values as their raw strings.
# Parameters:
#              - text: The YAML profile text to parse.
# Return:
#              - dict: Nested dictionary representing the YAML content.
#-------------------------------------------------------------------------
def parse_yaml(text):
    """Minimal indentation-based YAML parser.

    Only supports the ``key:`` / ``key: value`` mapping subset used by the
    device profiles. Scalar values are kept as their raw strings so that the
    original formatting (e.g. ``0x06``) is preserved. Returns a nested dict.
    """
    if not text.strip():
        return None

    root = {}
    # Stack of (indent, container) pairs; container is the dict at that level.
    stack = [(-1, root)]

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = _strip_yaml_comment(raw_line.strip())
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        # Pop back to the parent whose indent is smaller than this line's.
        while stack and stack[-1][0] >= indent:
            stack.pop()
        if not stack:
            stack = [(-1, root)]
        parent = stack[-1][1]

        if value == "":
            child = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            # Strip surrounding quotes from scalar values.
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            parent[key] = value

    return root


#-------------------------------------------------------------------------
# Function:    _find_key
# Description: Performs a case-insensitive key lookup within a dictionary.
# Parameters:
#              - mapping: Dictionary to search.
#              - name: Key name to look up (case-insensitive).
# Return:
#              - The matching value, or None if not found.
#-------------------------------------------------------------------------
def _find_key(mapping, name):
    """Case-insensitive key lookup in a dict."""
    if not isinstance(mapping, dict):
        return None
    lowered = name.lower()
    for key in mapping:
        if str(key).lower() == lowered:
            return mapping[key]
    return None


#-------------------------------------------------------------------------
# Function:    lookup_config
# Description: Resolves a g<root_name>Configuration[index].field reference
#              against the parsed device profile, trying several candidate
#              module names and mapping the index to a 1-based port entry.
# Parameters:
#              - config: Parsed profile dictionary.
#              - root_name: Configuration root name (e.g. 'DSVideoPort').
#              - index: Array index or loop variable.
#              - field: Field name within the port entry.
# Return:
#              - str: The resolved value, or None if not found.
#-------------------------------------------------------------------------
def lookup_config(config, root_name, index, field):
    """Resolve g<root_name>Configuration[index].field against the profile.

    root_name e.g. 'DSVideoPort' -> profile top-level key 'dsVideoPort'.
    'DSAudioPort' -> tries 'DSAudioPort', 'AudioPort', 'DSAudio', 'Audio'.
    The array index maps to the 1-based 'Ports' entries (a literal 0 or a loop
    variable both resolve to the first port).
    """
    # Build candidate names to try, from most-specific to least-specific.
    # 1. The name as-is.
    # 2. Strip a leading 'DS' prefix.
    # 3. Strip a trailing capitalised word (e.g. 'Port' from 'DSAudioPort').
    # 4. Strip DS prefix from (3).
    _trailing_word = re.match(r'^(.*[a-z])([A-Z][a-z]+)$', root_name)
    no_suffix = _trailing_word.group(1) if _trailing_word else None
    candidates = [root_name]
    if root_name[:2].lower() == "ds":
        candidates.append(root_name[2:])
    if no_suffix:
        candidates.append(no_suffix)
        if no_suffix[:2].lower() == "ds":
            candidates.append(no_suffix[2:])

    module = None
    for candidate in candidates:
        module = _find_key(config, candidate)
        if isinstance(module, dict):
            break
    if not isinstance(module, dict):
        return None

    ports = _find_key(module, "Ports")
    if not isinstance(ports, dict):
        return None

    port_no = int(index) + 1 if index.isdigit() else 1
    port = _find_key(ports, str(port_no))
    if not isinstance(port, dict):
        return None

    value = _find_key(port, field)
    return None if value is None else str(value)


#-------------------------------------------------------------------------
# Function:    resolve_config_refs
# Description: Replaces config-array references within a statement with
#              their resolved values from the device profile.
# Parameters:
#              - statement: The C statement containing config references.
#              - config: Parsed profile dictionary.
# Return:
#              - str: The statement with config references resolved.
#-------------------------------------------------------------------------
def resolve_config_refs(statement, config):
    """Replace config references in a statement with their profile values."""
    if not config:
        return statement

    def repl(match):
        resolved = lookup_config(config, match.group(1), match.group(2), match.group(3))
        return resolved if resolved is not None else match.group(0)

    return CONFIG_REF_RE.sub(repl, statement)


# A quoted YAML dotted-path key as used by ut_kvp_get*Field(), e.g.

#   ut_kvp_getStringField(ut_kvp_profile_getInstance(), "dsHost.socID", ...)
YAML_PATH_RE = re.compile(r'"([A-Za-z_]\w*(?:\.\w+)+)"')


#-------------------------------------------------------------------------
# Function:    lookup_config_path
# Description: Resolves a dotted YAML path (e.g. 'dsHost.socID') to its
#              scalar value within the parsed profile.
# Parameters:
#              - config: Parsed profile dictionary.
#              - path: Dotted YAML path to resolve.
# Return:
#              - str: The resolved scalar value, or None if not found.
#-------------------------------------------------------------------------
def lookup_config_path(config, path):
    """Resolve a dotted YAML path (e.g. 'dsHost.socID') to its scalar value."""
    node = config
    for part in path.split("."):
        node = _find_key(node, part)
        if node is None:
            return None
    return None if isinstance(node, dict) else str(node)


#-------------------------------------------------------------------------
# Function:    resolve_yaml_paths
# Description: Replaces quoted YAML dotted-path keys within a statement
#              with their resolved profile values.
# Parameters:
#              - statement: The C statement containing YAML path keys.
#              - config: Parsed profile dictionary.
# Return:
#              - str: The statement with YAML paths resolved.
#-------------------------------------------------------------------------
def resolve_yaml_paths(statement, config):
    """Replace quoted YAML dotted-path keys with their profile values.

    e.g. ut_kvp_getStringField(..., "dsHost.socID", ...) becomes
         ut_kvp_getStringField(..., "0600850A21F2CA94", ...)
    """
    if not config:
        return statement

    def repl(match):
        resolved = lookup_config_path(config, match.group(1))
        return f'"{resolved}"' if resolved is not None else match.group(0)

    return YAML_PATH_RE.sub(repl, statement)


#-------------------------------------------------------------------------
# Function:    resolve_all
# Description: Applies config-array, YAML dotted-path, and #define
#              constant resolution to a statement in sequence.
# Parameters:
#              - statement: The C statement to resolve.
#              - config: Parsed profile dictionary.
#              - defines: Optional #define constant map.
# Return:
#              - str: The fully resolved statement.
#-------------------------------------------------------------------------
def resolve_all(statement, config, defines=None):
    """Apply config-array, YAML dotted-path, and #define constant resolution."""
    resolved = resolve_yaml_paths(resolve_config_refs(statement, config), config)
    return resolve_constants(resolved, defines)


# ---------------------------------------------------------------------------
# C ``#define`` constant resolution.
# ---------------------------------------------------------------------------

# An object-like macro definition, e.g.
#   #define DS_VIDEO_PORT_DEFAULT_COLORDEPTH      8
# The mandatory whitespace after the name excludes function-like macros
# (``#define FOO(x) ...``), whose name is immediately followed by ``(``.
DEFINE_RE = re.compile(r"^\s*#define\s+([A-Za-z_]\w*)\s+(\S.*?)\s*$")

# A bare identifier token used when substituting known constants.
CONSTANT_TOKEN_RE = re.compile(r"\b([A-Za-z_]\w*)\b")


#-------------------------------------------------------------------------
# Function:    collect_defines
# Description: Scans .h/.c files under a directory for object-like #define
#              macros, keeping the first definition seen for each name.
# Parameters:
#              - source_dir: Directory tree to scan.
# Return:
#              - dict: Mapping of macro name to its value.
#-------------------------------------------------------------------------
def collect_defines(source_dir):
    """Scan .h/.c files under source_dir for object-like ``#define`` macros.

    Returns a ``{name: value}`` dict. The first definition seen for a name wins.
    """
    defines = {}
    for root, _dirs, files in os.walk(source_dir):
        for fname in files:
            if not fname.endswith((".h", ".c")):
                continue
            path = os.path.join(root, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        m = DEFINE_RE.match(line)
                        if not m:
                            continue
                        name = m.group(1)
                        value = strip_comments(m.group(2)).strip()
                        if value and name not in defines:
                            defines[name] = value
            except OSError:
                continue
    return defines


#-------------------------------------------------------------------------
# Function:    resolve_constants
# Description: Replaces known #define constants within a statement with
#              their values, expanding nested constants iteratively.
# Parameters:
#              - statement: The C statement to expand.
#              - defines: Mapping of macro name to value.
# Return:
#              - str: The statement with constants resolved.
#-------------------------------------------------------------------------
def resolve_constants(statement, defines):
    """Replace known ``#define`` constants in a statement with their values.

    e.g. ``UT_ASSERT_EQUAL(color_depth, DS_VIDEO_PORT_DEFAULT_COLORDEPTH)``
         becomes ``UT_ASSERT_EQUAL(color_depth, 8)``.
    Resolution is repeated (bounded) so a constant defined in terms of another
    constant is fully expanded.
    """
    if not defines:
        return statement

    def repl(match):
        return defines.get(match.group(1), match.group(1))

    for _ in range(5):
        expanded = CONSTANT_TOKEN_RE.sub(repl, statement)
        if expanded == statement:
            break
        statement = expanded
    return statement


# A ut_kvp_get*Field() call carrying a quoted dotted YAML path plus the
# destination variable the fetched value is stored into, e.g.
#   status = ut_kvp_getStringField(ut_kvp_profile_getInstance(),
#                                   "dsHost.socID", socIDProfile, ...)
KVP_GET_RE = re.compile(
    r'\but_kvp_get\w*\s*\(.*?"([A-Za-z_]\w*(?:\.\w+)+)"\s*,\s*&?\s*(\w+)'
)

# A comparison call used inside a control condition, e.g.
#   if(!strstr(socID, socIDProfile))
COMPARE_RE = re.compile(r"\b(?:strstr|strcmp|strncmp|memcmp)\s*\(\s*(\w+)\s*,\s*(\w+)")


#-------------------------------------------------------------------------
# Function:    _get_extended_enums_supported
# Description: Determines whether extendedEnumsSupported is enabled in any
#              module's features block of the config YAML, defaulting to
#              True when the entry is absent.
# Parameters:
#              - config: Parsed profile dictionary.
# Return:
#              - bool: True if extended enums are supported.
#-------------------------------------------------------------------------
def _get_extended_enums_supported(config):
    """Return True if extendedEnumsSupported is true in any module's features
    block of the config YAML. Defaults to True (VTS always runs with extended
    enums, and a missing entry should not suppress the extended error code).
    """
    if not isinstance(config, dict):
        return True
    for module_data in config.values():
        if not isinstance(module_data, dict):
            continue
        features = _find_key(module_data, "features")
        if not isinstance(features, dict):
            continue
        val = _find_key(features, "extendedEnumsSupported")
        if val is not None:
            return str(val).strip().lower() not in ("false", "0", "no")
    return True  # default: extended enums assumed


#-------------------------------------------------------------------------
# Function:    render_flow_statement
# Description: Renders a flow statement for display, expanding
#              ut_kvp_get*Field() lookups and CHECK_FOR_EXTENDED_ERROR_CODE
#              macros, and resolving config references and constants.
# Parameters:
#              - statement: The flow statement to render.
#              - config: Parsed profile dictionary.
#              - defines: Optional #define constant map.
# Return:
#              - str: The rendered, human-readable statement.
#-------------------------------------------------------------------------
def render_flow_statement(statement, config, defines=None):
    """Render a flow statement for display.

    A ut_kvp_get*Field() call is rendered as a profile lookup line:
        (<path> from yaml file) <destVar> = <value>
    or, when the value cannot be resolved:
        ERROR : Unable to fetch  <path> from yaml
    A CHECK_FOR_EXTENDED_ERROR_CODE(result, enhanced, old) call is expanded
    to the UT_ASSERT_EQUAL branch that actually fires, based on
    extendedEnumsSupported in the config YAML.
    All other statements get inline config-reference and #define constant
    resolution.
    """
    # Expand CHECK_FOR_EXTENDED_ERROR_CODE macro
    m_ext = CHECK_EXTENDED_RE.search(statement)
    if m_ext:
        result_var = m_ext.group(1)
        enhanced   = m_ext.group(2)
        old        = m_ext.group(3)
        ext = _get_extended_enums_supported(config)
        expected = enhanced if ext else old
        return "UT_ASSERT_EQUAL({}, {})".format(expected, result_var)
    match = KVP_GET_RE.search(statement)
    if match:
        path = match.group(1)
        dest = match.group(2)
        value = lookup_config_path(config, path)
        if value is None:
            return f"ERROR : Unable to fetch  {path} from yaml"
        return f"({path} from yaml file) {dest} = {value}"
    return resolve_all(statement, config, defines)


#-------------------------------------------------------------------------
# Function:    render_compare_statement
# Description: Renders a comparison control statement as a human-readable
#              'Comparing X and Y' line.
# Parameters:
#              - statement: The statement containing a comparison call.
# Return:
#              - str: The rendered line, or None if no comparison found.
#-------------------------------------------------------------------------
def render_compare_statement(statement):
    """Render a comparison control statement as a human-readable line.

    e.g. `if(!strstr(socID, socIDProfile))` -> `Comparing socID and socIDProfile`
    Returns None if the statement carries no recognised comparison call.
    """
    m = COMPARE_RE.search(statement)
    if not m:
        return None
    return f"Comparing {m.group(1)} and {m.group(2)}"


# An `if (...)` condition guarding the failing statement.
# Accepts a guard that
# opens a block (`if (...) {`), a bare condition, and an inline single-statement
# body such as `if (handle == 0) break;` or `if (cond) continue;`.
#   if(!isConnected) {
IF_COND_RE = re.compile(r"^\s*if\s*\((.*)\)\s*(?:\{|[A-Za-z_].*?;)?\s*$")


#-------------------------------------------------------------------------
# Function:    render_condition
# Description: Renders an `if (...)` guard as a human-readable line,
#              expanding comparisons and bare negations into explicit form.
# Parameters:
#              - statement: The statement containing an `if` condition.
# Return:
#              - str: The rendered condition, or None if not an `if`.
#-------------------------------------------------------------------------
def render_condition(statement):
    """Render an `if (...)` guard as a human-readable line.

    - A comparison call becomes ``Comparing X and Y``.
    - Otherwise the condition is kept in its literal C form, except a bare
      negation is expanded to an explicit ``== false`` comparison:
        ``if(!isConnected)``            -> ``if isConnected == false``
        ``if(isConnected == "kilo")``   -> ``if isConnected == "kilo"``
        ``if(a != b && c)``             -> ``if a != b && c``
    Returns None if the statement is not an `if` condition.
    """
    m = IF_COND_RE.match(statement)
    if not m:
        return None

    compare = render_compare_statement(statement)
    if compare:
        return compare

    cond = m.group(1).strip()
    # Expand a bare `!operand` (not `!=`) into `operand == false`.
    cond = re.sub(r"!\s*([A-Za-z_][\w.]*(?:->\w+)*)", r"\1 == false", cond)
    cond = re.sub(r"\s+", " ", cond).strip()
    return f"if {cond}"


#-------------------------------------------------------------------------
# Function:    parse_return_statuses
# Description: Extracts a mapping of source line numbers to returned status
#              values from DEBUG 'Return[ed] status: N' log entries.
# Parameters:
#              - log_text: The raw failure log text.
# Return:
#              - dict: Mapping of source line number to status integer.
#-------------------------------------------------------------------------
def parse_return_statuses(log_text):
    """Return {source_line_no: status_int} from DEBUG 'Return[ed] status: N' log entries."""
    status_map = {}
    re_status = re.compile(
        r",\s*DEBUG\s*,\s*[\w./\\-]+\.c\s*,\s*(\d+)\s*:.*?Return(?:ed)?\s+status\s*:\s*([-\d]+)",
        re.IGNORECASE,
    )
    for m in re_status.finditer(log_text):
        status_map[int(m.group(1))] = int(m.group(2))
    return status_map


#-------------------------------------------------------------------------
# Function:    get_statement_end_lines
# Description: Maps each logical statement to the 1-based source line where
#              it ends, for statements in [body_start, failure_line).
# Parameters:
#              - lines: List of source lines.
#              - body_start: 0-based index of the function body start.
#              - failure_line: 1-based line number of the failure.
# Return:
#              - dict: Mapping of statement text to its ending line number.
#-------------------------------------------------------------------------
def get_statement_end_lines(lines, body_start, failure_line):
    """Return {statement_text: last_1based_source_line_no} for statements in [body_start, failure_line)."""
    result = {}
    buffer = ""
    buf_end = None
    for idx in range(body_start, failure_line):
        raw = strip_comments(lines[idx])
        if not raw:
            continue
        buffer = (buffer + " " + raw).strip() if buffer else raw
        buf_end = idx + 1  # convert 0-based index to 1-based line number
        if buffer.endswith((";", "{", "}")):
            result[re.sub(r"\s+", " ", buffer)] = buf_end
            buffer = ""
            buf_end = None
    if buffer and buf_end:
        result[re.sub(r"\s+", " ", buffer.strip())] = buf_end
    return result


#-------------------------------------------------------------------------
# Function:    analyze_failure
# Description: Analyzes a CUnit/UT failure log and reconstructs the failing
#              flow, annotating API calls with SUCCESS/FAILURE and adding an
#              Expected/Actual diagnostic for UT_ASSERT_EQUAL failures.
# Parameters:
#              - source_dir: Directory holding the HAL test source.
#              - failure_log: The raw CUnit/UT failure log text.
#              - config_yaml: Optional device profile YAML text.
# Return:
#              - tuple: (failure_flow, full_failurelog) strings.
#-------------------------------------------------------------------------
def analyze_failure(source_dir, failure_log, config_yaml=""):
    """Analyze a CUnit/UT failure log and reconstruct the failing flow.

    Args:
        source_dir: Directory holding the HAL test source (searched recursively).
        failure_log: The raw CUnit/UT failure log text.
        config_yaml: Optional device profile YAML text used to resolve config
            references and ``ut_kvp_get*Field`` lookups in the flow.

    Returns:
        A ``(failure_flow, full_failurelog)`` tuple of strings:
          - ``failure_flow``: the filtered, enriched FAILURE FLOW block with the
            failing statement marked ``--> FAILURE``.
          - ``full_failurelog``: the raw reconstructed function flow, one
            statement per line.
    """
    config = parse_yaml(config_yaml) if config_yaml else {}

    source_file, line_no, failure_kind, detail, function_name = parse_log(failure_log)
    source_path = find_source(source_file, source_dir)
    defines = collect_defines(source_dir)

    with open(source_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    body_start = find_function_body_start(lines, function_name)
    statements = collect_statements(lines, body_start, line_no)
    fail_stmt = failing_statement(lines, line_no)
    if fail_stmt:
        statements.append(fail_stmt)

    flow = failure_flow(statements, fail_stmt)

    # Annotate each API call in the flow with --> SUCCESS / --> FAILURE based
    # on the return-status DEBUG lines recorded in the log.
    return_statuses = parse_return_statuses(failure_log)
    stmt_end_lines = get_statement_end_lines(lines, body_start, line_no)
    sorted_status_lines = sorted(return_statuses)

    annotated_flow = []
    for s in flow:
        rendered = render_flow_statement(s, config, defines)
        if s == fail_stmt:
            annotated_flow.append(rendered + "  --> FAILURE")
            continue
        # Only annotate lines that are actual API calls (contain a function call).
        # Declaration lines (int handle = 0;) have no callee and get no annotation.
        if CALLEE_RE.search(s):
            end_line = stmt_end_lines.get(s)
            if end_line is not None:
                matched_ln = next((ln for ln in sorted_status_lines if ln > end_line), None)
                if matched_ln is not None and return_statuses[matched_ln] == 0:
                    rendered += "  --> SUCCESS"
        annotated_flow.append(rendered)
    flow = annotated_flow

    # Prefix the flow with a header naming the failing statement. The separator
    # length matches the longest line in the header + flow.
    if fail_stmt:
        rendered_fail = render_flow_statement(fail_stmt, config, defines)
        header = f"FAILURE at : {rendered_fail}"
        width = max(len(line) for line in [header] + flow)
        flow = [header, "=" * width] + flow

    # ── Expected / Actual diagnostic for UT_ASSERT_EQUAL ─────────────────
    # If the failing statement is a UT_ASSERT_EQUAL(expected, var), find the
    # last API call in the flow that assigned to <var> and produce a plain-
    # English summary, e.g.:
    #   Expected result : dsERR_ALREADY_INITIALIZED must be returned
    #   Actual result   : dsAudioPortInit did not return dsERR_ALREADY_INITIALIZED
    _assert_eq_re = re.compile(
        r"UT_ASSERT_EQUAL\s*\(\s*([^,)]+?)\s*,\s*([^,)]+?)\s*\)", re.IGNORECASE
    )
    _eq_m = _assert_eq_re.search(render_flow_statement(fail_stmt, config, defines) if fail_stmt else "")
    if _eq_m:
        expected_val = _eq_m.group(1).strip()
        checked_var  = _eq_m.group(2).strip()
        # Scan annotated_flow (excluding the FAILURE line) to find the last
        # assignment to <checked_var>, e.g. "result = dsAudioPortInit(...)".
        assign_re = re.compile(
            r"^\s*(?:[\w\s\*]+\s+)?" + re.escape(checked_var) + r"\s*=\s*(\w+)\s*\("
        )
        origin_fn = None
        for s in flow:
            m = assign_re.match(s)
            if m:
                origin_fn = m.group(1)
        if origin_fn:
            flow.append("")
            flow.append(f"Expected result : {expected_val} must be returned")
            flow.append(f"Actual result   : {origin_fn} did not return {expected_val}")

    failure_flow_text = "\n".join(flow)
    full_failurelog_text = "\n".join(statements)
    return failure_flow_text, full_failurelog_text


#-------------------------------------------------------------------------
# Function:    main
# Description: Entry point that parses the configured failure log, locates
#              the source, runs the failure analysis, and prints the
#              reconstructed flow and full function flow.
# Parameters:
#              - None
# Return:
#              - None
#-------------------------------------------------------------------------
def main():
    config = parse_yaml(CONFIG_YAML)
    source_file, line_no, failure_kind, detail, function_name = parse_log(FAILURE_LOG)
    source_path = find_source(source_file, SOURCE_DIR)

    if failure_kind == "FAIL":
        failure_desc = f'UT_FAIL ("{detail}")'
    else:
        failure_desc = detail

    failure_flow_text, full_failurelog_text = analyze_failure(
        SOURCE_DIR, FAILURE_LOG, CONFIG_YAML
    )

    print(f"Failure   : {failure_desc} at {source_file}:{line_no}")
    print(f"Function  : {function_name}")
    print(f"Source    : {source_path}")
    print()
    print(failure_flow_text)
    print("=" * 22)
    print("Full function flow:")
    print(full_failurelog_text)


if __name__ == "__main__":
    main()
