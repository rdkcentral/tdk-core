##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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

import subprocess
import os
import pty
import select
import sys
import re
import tty
import termios
import shlex
import time
import yaml
import importlib
import urllib.request
import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
import paramiko
from typing import Optional, List, Iterable
from datetime import datetime
from log_to_excel import *
from vts_common_config import PLATFORM_EXPORTS

# ====================================
# Dynamic target -> config module
# ===================================
VALID_TARGETS = {
    "dsHost": "vtsconfig_dsHost",      
    "dsDisplay": "vtsconfig_dsDisplay",
    "dsVideoDevice": "vtsconfig_dsVideoDevice",
    "dsVideoPort": "vtsconfig_dsVideoPort",
    "dsAudio": "vtsconfig_dsAudio",
    "deepsleep": "vtsconfig_deepsleep",
    "rmfaudiocapture": "vtsconfig_rmfaudiocapture"
}

config = None  # will be set after loading the target module


def load_config_for_target(target: str):
    """Import and return the config module for the selected target."""
    if target not in VALID_TARGETS:
        print("module needed")
        print("Usage: python test.py dsHost|dsDisplay|dsVideoDevice|dsVideoPort|dsAudio|deepsleep|rmfaudiocapure [--config|--validate|--update-config|--help]")
        sys.exit(1)
    module_name = VALID_TARGETS[target]
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        print(f"[ERROR] Could not import '{module_name}': {e}")
        sys.exit(2)

#============= CLONING THE REPO AND RAFT INSTALLATION ======================

def setup_halif_test():
    """
    Clone the test repo and installation of RAFT using values from vtsconfig_<target>.py
    """
    repo_url = getattr(config, "REPO_URL")
    repo_dir = getattr(config, "REPO_DIR")
    checkout_ver = getattr(config, "CHECKOUT_VER")
    host_dir = os.path.join(repo_dir, "host")
    print("REPO DIR " , repo_dir)
    print("host_dir ", host_dir)
    try:
        # Step 1: Clone the repo
        if not os.path.exists(repo_dir):
            print("📦 Cloning RAFT repo...")
            subprocess.run(["git", "clone", repo_url], check=True)
        else:
            print("📁 Repo already exists. Skipping clone.")

        # Step 2: Checkout specified tag/branch
        print("🔀 Checking out ...")
        subprocess.run(["git", "checkout", checkout_ver], cwd=repo_dir, check=True)

        # Step 3: Run install.sh
        print("⚙️ Running initial install.sh...")
        try:
            subprocess.run(["bash", "-c", "pwd && ./install.sh"], cwd=host_dir, check=False)
        except subprocess.CalledProcessError:
            print("ℹ️ Initial install.sh exited with non-zero status (expected). Proceeding to activate venv...")
            
        # Step 4: Source activate_venv.sh and rerun install.sh
        print("🧪 Activating virtual environment and rerunning install.sh...")
        subprocess.run(["bash", "-c", "source ./activate_venv.sh && ./install.sh"], cwd=host_dir, check=False)

        print("✅ RAFT setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during RAFT setup: {e}")

# ============= SCP MODIFICATION FUNCTIONS =============

def modify_scpCopy_to_skip():
    """
    Modify the scpCopy function in the given file to return 'skipped' immediately.
    
    Returns:
        bool: True if modification was successful, False otherwise
    """
    try:
        file_path = config.UTBASEUTILS_PATH

        if not os.path.exists(file_path):
            print(f"Warning: utBaseUtils.py not found at {config.UTBASEUTILS_PATH}")
            return

        # Read the file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if already modified
        if re.search(r'def scpCopy\(.*?\):\s*\n\s*return "skipped"', content):
            print(f"✓ scpCopy in {file_path} is already modified to return 'skipped'")
            return True
        
        # Pattern to find the function and modify it
        pattern = r'(def scpCopy\([^)]*\):\s*\n)(.*?)(\s*""".*?""")'
        
        def replacement(match):
            func_def = match.group(1)
            return_statement = '        return "skipped"\n'
            docstring = match.group(3)
            return func_def + return_statement + docstring
        
        # Apply the modification
        modified_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Check if modification was made
        if modified_content == content:
            print(f"No scpCopy function found in {file_path}")
            return False
        
        # Write back to file
        with open(file_path, 'w') as f:
            f.write(modified_content)
        
        print(f"✓ Successfully modified scpCopy function in {file_path}")
        return True
        
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return False
    except Exception as e:
        print(f"Error modifying {file_path}: {e}")
        return False

def modify_waitForBoot_to_return_true_if_needed():
    """
    Modify waitForBoot(self) to immediately return True,
    ONLY if the first executable statement is not already 'return True'.

    Returns:
        bool: True if already patched OR successfully patched, False otherwise
    """
    try:
        utBasePath = os.path.dirname(config.UTBASEUTILS_PATH)
        file_path = utBasePath + "/utHelper.py"
        print(file_path)

        if not os.path.exists(file_path):
            print(f"Warning: utHelper.py not found at {config.UTBASEUTILS_PATH}")
            return
        
        with open(file_path, "r") as f:
            content = f.read()

        # Find function definition
        func_def_pattern = r'(^[ \t]*def[ \t]+waitForBoot[ \t]*\([ \t]*self[ \t]*\)[ \t]*:[ \t]*\n)'
        m = re.search(func_def_pattern, content, flags=re.MULTILINE)

        if not m:
            print(f"❌ waitForBoot(self) not found in {file_path}")
            return False

        def_start = m.start(1)
        def_end = m.end(1)

        # Determine indentation (spaces/tabs before "def")
        def_line = m.group(1)
        base_indent = re.match(r'^([ \t]*)def', def_line).group(1)

        # Indentation for function body (one level inside)
        body_indent = base_indent + "    "

        # Extract content after def line
        after_def = content[def_end:]

        # Take a small chunk to inspect first lines inside function
        # (we don't need the full file; first ~30 lines is enough)
        preview = after_def.splitlines(True)[:40]  # keep newline chars
        preview_text = "".join(preview)

        # Remove leading blank lines
        preview_text_no_blank = re.sub(r'^(?:[ \t]*\n)+', '', preview_text)

        # If function starts with docstring, skip it
        # Handles """...""" or '''...'''
        docstring_pattern = (
            r'^([ \t]*("""|\'\'\')'
            r'(?:.|\n)*?'
            r'\2[ \t]*\n)'
        )
        preview_wo_doc = re.sub(docstring_pattern, '', preview_text_no_blank, flags=re.DOTALL)

        # Remove leading comments and blank lines again
        preview_wo_doc = re.sub(r'^(?:[ \t]*#.*\n|[ \t]*\n)+', '', preview_wo_doc)

        # Now check the first executable line
        first_exec_line = preview_wo_doc.splitlines()[0] if preview_wo_doc.strip() else ""

        if re.match(r'^[ \t]*return[ \t]+True[ \t]*$', first_exec_line):
            print(f"✅ waitForBoot(self) already starts with 'return True' in {file_path} (no change needed)")
            return True

        # If not already returning True, patch it by inserting return True right after def
        patched_content = (
            content[:def_end] +
            f"{body_indent}return True\n" +
            content[def_end:]
        )

        with open(file_path, "w") as f:
            f.write(patched_content)

        print(f"✅ Patched waitForBoot(self) to return True in {file_path}")
        return True

    except Exception as e:
        print(f"❌ Error modifying {file_path}: {e}")
        return False

def patch_testCleanSingleAsset_skip_cleanup(TARGET_DIR,target):
    """
    Patch <testModule>HelperClass.py to skip cleanup in:
        def testCleanSingleAsset(self):

    Replace:
        self.deleteFromDevice(self.testStreams)

    With:
        print("Cleanup handled by external framework")
        return

    Args:
        TARGET_DIR (str): Path to test directory
        target (str): Test module name (example: dsVideoPort)

    Returns:
        bool: True if patched or already patched, False otherwise
    """
    file_path = TARGET_DIR + "/" + target + "HelperClass.py"
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    with open(file_path, "r") as f:
        content = f.read()

    # ✅ Check function exists
    func_pattern = r'def\s+testCleanSingleAsset\s*\(\s*self\s*\)\s*:'
    func_pattern = r'def\s+testCleanAssets\s*\(\s*self\s*\)\s*:'
    if not re.search(func_pattern, content):
        print(f"❌ testCleanSingleAsset(self) not found in {file_path}")
        return False

    # ✅ Already patched check (print + return exists inside function)
    already_pattern = r'def\s+testCleanSingleAsset\s*\(\s*self\s*\)\s*:\s*[\s\S]*?print\(\s*[\'"]Cleanup handled by external framework[\'"]\s*\)\s*[\s\S]*?return'
    already_pattern = r'def\s+testCleanAssets\s*\(\s*self\s*\)\s*:\s*[\s\S]*?print\(\s*[\'"]Cleanup handled by external framework[\'"]\s*\)\s*[\s\S]*?return'
    if re.search(already_pattern, content):
        print(f"✅ Already patched: testCleanSingleAsset() in {file_path}")
        return True

    # ✅ Replace the exact cleanup call line (simple + safe)
    old_line_pattern = r'^[ \t]*self\.deleteFromDevice\(\s*self\.testStreams\s*\)[ \t]*$'

    if not re.search(old_line_pattern, content, flags=re.MULTILINE):
        print(f"❌ Cleanup line not found: self.deleteFromDevice(self.testStreams) in {file_path}")
        return False

    replacement_block = (
        '        print("Cleanup handled by external framework")\n'
        '        return'
    )

    modified_content = re.sub(
        old_line_pattern,
        replacement_block,
        content,
        flags=re.MULTILINE,
        count=1
    )

    with open(file_path, "w") as f:
        f.write(modified_content)

    print(f"✅ Patched successfully: Cleanup skipped in {file_path}")
    return True

# ============= CONFIG FILE GENERATION FUNCTIONS =============

def generate_rack_config():
    """Generate rack configuration dictionary with current parameters"""
    rack_config = {
        'globalConfig': {
            'includes': {
                'deviceConfig': 'deviceConfig.yml'
            },
            'local': {
                'log': {
                    'directory': config.LOG_DIRECTORY,
                    'delimiter': '/'
                }
            }
        },
        'rackConfig': {
            'rack1': {
                'name': 'rack1',
                'description': 'Generated config',
                'slot1': {
                    'name': 'slot1',
                    'devices': [
                        {
                            'dut': {
                                'ip': config.DEVICE_IP,
                                'description': config.DEVICE_DESCRIPTION,
                                'platform': config.DEVICE_PLATFORM,
                                'consoles': [
                                    {
                                        'default': {
                                            'type': 'ssh',
                                            'port': config.SSH_PORT,
                                            'username': config.SSH_USERNAME,
                                            'ip': config.DEVICE_IP,
                                            'password': config.SSH_PASSWORD
                                        }
                                    },
                                    {
                                        'ssh_player': {
                                            'type': 'ssh',
                                            'port': config.SSH_PORT,
                                            'username': config.SSH_USERNAME,
                                            'ip': config.DEVICE_IP,
                                            'password': config.SSH_PASSWORD
                                        }
                                    },
                                    {
                                        'ssh_player_secondary': {
                                            'type': 'ssh',
                                            'port': config.SSH_PORT,
                                            'username': config.SSH_USERNAME,
                                            'ip': config.DEVICE_IP,
                                            'password': config.SSH_PASSWORD
                                        }
                                    },
                                    {
                                        'ssh_hal_test': {
                                            'type': 'ssh',
                                            'port': config.SSH_PORT,
                                            'username': config.SSH_USERNAME,
                                            'ip': config.DEVICE_IP,
                                            'password': config.SSH_PASSWORD
                                        }
                                    },
                                    {
                                        'ssh_hal_deepsleep_test': {
                                            'type': 'ssh',
                                            'port': config.SSH_PORT,
                                            'username': config.SSH_USERNAME,
                                            'ip': config.DEVICE_IP,
                                            'password': config.SSH_PASSWORD
                                        }
                                    },
                                    {
                                        'ssh_hal_power_test': {
                                            'type': 'ssh',
                                            'port': config.SSH_PORT,
                                            'username': config.SSH_USERNAME,
                                            'ip': config.DEVICE_IP,
                                            'password': config.SSH_PASSWORD
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
    }
    return rack_config

def generate_device_config():
    """Generate device configuration dictionary with current parameters"""
    device_config = {
        'deviceConfig': {
            'cpe1': {
                'platform': 'llama.uk',
                'model': '65',
                'target_directory': '/tmp/',
                'test': {
                    'profile': '../../../profiles/deepsleepmanagerExtendedEnumsNotSupported.yaml'
                }
            },
            'cpe2': {
                'platform': 'test',
                'model': 'test',
                'target_directory': '/tmp',
                'prompt': '',
                'test': {}
            },
            'cpe3': {
                'platform': config.CPE_PLATFORM,
                'model': config.CPE_MODEL,
                'soc_vendor' : config.SOC_VENDOR,
                'target_directory': config.TARGET_DIRECTORY,
                'prompt': '',
                'test': {
                    'profile': config.PROFILE_PATH,
                    'streams_download_url': config.STREAM_DOWNLOAD_PATH
                }
            }
        }
    }
    return device_config

def update_rack_config():
    """Update rack configuration file with current parameters"""
    try:
        rack_config = generate_rack_config()
        with open(config.RACK_CONFIG_PATH, 'w') as f:
            yaml.dump(rack_config, f, default_flow_style=config.YAML_DEFAULT_FLOW_STYLE, indent=config.YAML_INDENT)
        print(f"✓ Rack configuration updated: {config.RACK_CONFIG_PATH}")
        return True
    except ImportError:
        print("✗ Error: PyYAML module not found. Please install it with 'pip install pyyaml' or run from virtual environment.")
        return False
    except Exception as e:
        print(f"✗ Error updating rack config: {e}")
        return False

def update_device_config():
    """Update device configuration file with current parameters"""
    try:
        device_config = generate_device_config()
        with open(config.DEVICE_CONFIG_PATH, 'w') as f:
            yaml.dump(device_config, f, default_flow_style=config.YAML_DEFAULT_FLOW_STYLE, indent=config.YAML_INDENT)
        print(f"✓ Device configuration updated: {config.DEVICE_CONFIG_PATH}")
        return True
    except ImportError:
        print("✗ Error: PyYAML module not found. Please install it or run from virtual environment.")
        return False
    except Exception as e:
        print(f"✗ Error updating device config: {e}")
        return False

def update_all_configs():
    """Update both configuration files"""
    print("Updating configuration files...")
    rack_success = update_rack_config()
    device_success = update_device_config()
    
    if rack_success and device_success:
        print("✓ All configuration files updated successfully!")
        return True
    else:
        print("✗ Some configuration files failed to update!")
        return False

def print_current_config():
    """Print current configuration parameters"""
    print("\n" + "="*50)
    print("CURRENT CONFIGURATION PARAMETERS")
    print("="*50)
    print("Base Configuration:")
    print(f"  Base Path: {config.BASE_PATH}")
    print("\nDevice Settings:")
    print(f"  IP Address: {config.DEVICE_IP}")
    print(f"  Platform: {config.DEVICE_PLATFORM}")
    print(f"  Description: {config.DEVICE_DESCRIPTION}")
    print(f"  SSH Username: {config.SSH_USERNAME}")
    print(f"  SSH Password: {'(empty)' if not config.SSH_PASSWORD else '(set)'}")
    print(f"  SSH Port: {config.SSH_PORT}")
    print("\nTest Settings:")
    print(f"  CPE Platform: {config.CPE_PLATFORM}")
    print(f"  CPE Model: {config.CPE_MODEL}")
    print(f"  Soc vendor: {config.SOC_VENDOR}")
    print(f"  Target Directory: {config.TARGET_DIRECTORY}")
    print(f"  Profile Path: {config.PROFILE_PATH}")
    print(f"  Stream Path: {config.STREAM_DOWNLOAD_PATH}")
    print(f"  Log Directory: {config.LOG_DIRECTORY}")
    print("\nFile Paths:")
    print(f"  VENV Script: {config.VENV_SCRIPT}")
    print(f"  Target Dir: {config.TARGET_DIR}")
    print(f"  Rack Config: {config.RACK_CONFIG_PATH}")
    print(f"  Device Config: {config.DEVICE_CONFIG_PATH}")
    print("="*50)

#================UPDATING MONITOR DETAILS================================

def update_monitor_yaml(create_backup: bool = True) -> int:
    """
    Replace the 'Monitor' list in the YAML at vtsconfig.MONITOR_YAML_PATH
    with vtsconfig.MONITOR_DETAILS, using an exact format

    """
    yaml_path = getattr(config, "MONITOR_YAML_PATH", None)
    if not yaml_path:
        raise ValueError("MONITOR_YAML_PATH is not set in vtsconfig_dsDisplay.py")

    monitors = getattr(config, "MONITOR_DETAILS", None)
    if not monitors or not isinstance(monitors, list):
        raise ValueError("MONITOR_DETAILS in vtsconfig.py must be a non-empty list of dicts.")

    yaml_abs = os.path.abspath(yaml_path)
    if not os.path.exists(yaml_abs):
        raise FileNotFoundError(f"Monitor YAML not found at: {yaml_abs}")

    # Optional backup
    if create_backup:
        backup_path = yaml_abs + ".bak"
        with open(yaml_abs, "rb") as src, open(backup_path, "wb") as dst:
            dst.write(src.read())

    # Build the content manually to ensure exact spacing
    lines = ["Monitor:"]
    dash_indent = "   "      
    key_indent  = "     "    
    for m in monitors:
        product = str(m.get("Product", "")).strip()
        mfr     = str(m.get("manufacturerId", "")).strip()
        name    = str(m.get("monitorName", "")).strip()

        # Basic validation
        if not product or not mfr or not name:
            raise ValueError("Each monitor must have Product, manufacturerId, and monitorName.")

        # Sequence entry header (dash line)
        lines.append(f"{dash_indent}- Product: {product}")
        # Subsequent mapping keys
        lines.append(f"{key_indent}manufacturerId: {mfr}")
        lines.append(f"{key_indent}monitorName: {name}")

    content = "\n".join(lines) + "\n"

    # Write and flush to disk
    with open(yaml_abs, "w", encoding="utf-8") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())

    print(f"[monitor-yaml] Updated '{yaml_abs}' with {len(monitors)} monitor entries.")
    
#===================== DOWNLOADING STREAMS ==============================================

# Only these modules need stream downloads
ALLOWED_DOWNLOAD_MODULES = {
    "dsVideoDevice":    "dsVideoDevice_L3_testSetup.yml",
    "dsAudio":          "dsAudio_L3_testSetup.yml",
    "dsVideoPort":      "dsVideoPort_L3_testSetup.yml",
    "rmfaudiocapture":  "rmfAudio_L3_testSetup.yml",
}

def _resolve_yaml_path_for_target(target: str, config) -> Optional[str]:
    """
    Locate the YAML that lists streams for the selected target
    """
    fname = ALLOWED_DOWNLOAD_MODULES.get(target)
    if not fname:
        return None

    if target == "rmfaudiocapture":
        base_path = getattr(config, "BASE_PATH", ".")
        helper_dir = os.path.join(base_path, "host", "tests", "rmfAudio_L3_TestCases")
        candidate = os.path.join(helper_dir, fname)
        if os.path.exists(candidate):
            return candidate

    # Prefer inside repo/module dir (host path)
    candidate = os.path.join(getattr(config, "TARGET_DIR", "."), fname)
    if os.path.exists(candidate):
        return candidate

    # Fallback: local file next to test.py
    if os.path.exists(fname):
        return fname

    return None


def _collect_streams_from_yaml(yaml_path: str) -> List[str]:
    """
    Parse the YAML and collect every string under any `streams:` list.
    Preserves order and de-duplicates.
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    found = []

    def walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "streams" and isinstance(v, list):
                    for item in v:
                        if isinstance(item, str):
                            found.append(item)
                else:
                    walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(doc)

    # Deduplicate (preserve order)
    seen = set()
    out = []
    for s in found:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def get_normalized_streams_for_target(target: str,config,remove_empty: bool = True,dedupe: bool = True,) -> list[str]:
    """
    Read the target's *_L3_testSetup.yml, collect all 'streams' entries,
    and normalize them using rename rules defined in test.py.
    """
    yaml_path = _resolve_yaml_path_for_target(target, config)
    if not yaml_path:
        print(f"[streams-rename] YAML not found for '{target}'. Expected one of:\n"
              f"  - {os.path.join(getattr(config, 'TARGET_DIR', '.'), ALLOWED_DOWNLOAD_MODULES.get(target, '<unknown>'))}\n"
              f"  - {ALLOWED_DOWNLOAD_MODULES.get(target, '<unknown>')} in current directory")
        return []

    streams = _collect_streams_from_yaml(yaml_path)
 
    mapping = getattr(config, "STREAM_RENAME_MAP", None)
    if mapping is None:
         mapping = config.STREAM_RENAME_MAP_BY_MODULE.get(target, {}) or {}

    rules = getattr(config, "STREAM_RENAME_RULES", None)
    if rules is None:
        rules = config.STREAM_RENAME_RULES_BY_MODULE.get(target, []) or []


    def apply_rules(name: str) -> str:
        for rule in rules:
            if isinstance(rule, dict) and "regex" in rule and "replace" in rule:
                name = re.sub(rule["regex"], rule["replace"], name)
        return name

    normalized = []
    seen = set()
    for s in streams:
        if not isinstance(s, str):
                       continue
        t = s.strip()
        if remove_empty and t == "":
            continue

        t = mapping.get(t, t)
        t = apply_rules(t)
        
        if dedupe:
            if t in seen:
                continue
            seen.add(t)
        normalized.append(t)

    print(f"[streams-rename] {target}: {len(streams)} → {len(normalized)} after normalization")


def rewrite_testsetup_yaml_streams_with_renames(target: str,config,remove_empty: bool = True,dedupe: bool = True,) -> int:
    """
    Rewrite the target's *_L3_testSetup.yml in place, applying the module's
    stream rename map and rules to every 'streams:' list.

    Args:
        target (str): Test module name (example: dsAudio).
        config: Loaded vtsconfig_<target> module.
        remove_empty (bool): Drop empty stream entries when True.
        dedupe (bool): Remove duplicate entries when True.

    Returns:
        int: Number of changes applied to the YAML.
    """
    yaml_path = _resolve_yaml_path_for_target(target, config)
    if not yaml_path or not os.path.exists(yaml_path):
        print(f"[streams-rename] Cannot rewrite: YAML not found for '{target}'. Path={yaml_path}")
        return 0

    with open(yaml_path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    
    mapping = getattr(config, "STREAM_RENAME_MAP", None)
    if mapping is None:
         mapping = config.STREAM_RENAME_MAP_BY_MODULE.get(target, {}) or {}

    rules = getattr(config, "STREAM_RENAME_RULES", None)
    if rules is None:
        rules = config.STREAM_RENAME_RULES_BY_MODULE.get(target, []) or []


    def apply_rules(name: str) -> str:
        for rule in rules:
            if isinstance(rule, dict) and "regex" in rule and "replace" in rule:
                name = re.sub(rule["regex"], rule["replace"], name)
        return name

    def normalize_list(items: list[str]) -> list[str]:
        out, seen = [], set()
        for s in items:
            if not isinstance(s, str):
                continue
            raw = s.strip()
            if remove_empty and raw == "":
                continue

            base = raw.split("/")[-1]  # basename
            new_base = mapping.get(base, base)
            new_base = apply_rules(new_base)

            # Enforce module-specific format in YAML
            if target == "dsAudio":
                final = f"streams/{new_base}"         
            elif target == "dsVideoPort":
                final = new_base                      
            else:
                prefix = "/".join(raw.split("/")[:-1])
                final = f"{prefix}/{new_base}" if prefix else new_base

            if dedupe:
                if final in seen:
                    continue
                seen.add(final)
            out.append(final)
        return out

    changes = 0

    def walk_and_update(obj):
        nonlocal changes
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "streams":
                    if isinstance(v, list):
                        new_list = normalize_list(v)
                        
                        for old, new in zip(v, new_list):
                            if old != new:
                                changes += 1
                        if len(v) != len(new_list):
                            changes += abs(len(v) - len(new_list))
                        obj[k] = new_list if new_list else None 
                    elif v is None:
                        obj[k] = None
                    else:
                        obj[k] = None
                else:
                    walk_and_update(v)
        elif isinstance(obj, list):
            for v in obj:
                walk_and_update(v)

    walk_and_update(doc)

    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True)

    with open(yaml_path, "r", encoding="utf-8") as f:
        content = f.read()

    
    content = re.sub(r'(^\s*streams:\s*)\[\]\s*$', r'\1', content, flags=re.MULTILINE)
    content = re.sub(r'(^\s*streams:\s*)null\s*$', r'\1', content, flags=re.MULTILINE)

    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(content)    

    print(f"[streams-rename] Rewrote {yaml_path}. Changes applied: {changes}")
    return changes

def startSession(hostname, username, password, port):
    """Open an interactive SSH shell session. Uses invoke_shell() rather than
    exec_command(), which is what works reliably against this device's sshd."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password, port=port)
        session = client.invoke_shell()
        print("Created ssh session")
        return client, session
    except Exception as e:
        print("Login to device failed")
        print(e)
        return None, None


def closeSession(client):
    """Close an SSH client session if it is open, ignoring any errors."""
    if client is not None:
        try:
            client.close()
        except Exception:
            pass


def _run_shell_cmd(session, cmd, timeout=60, end_marker="__CMD_DONE__", drain_grace=0.5):
    """
    Run a command over an interactive SSH shell and capture its output.

    Appends an end marker to detect completion and parse the exit status.

    Args:
        session: Active paramiko shell session.
        cmd (str): Command to execute on the device.
        timeout (int): Seconds to wait for the command to finish.
        end_marker (str): Sentinel used to detect command completion.
        drain_grace (float): Extra time to drain trailing output.

    Returns:
        tuple[int, str]: The command exit status and captured output.

    Raises:
        TimeoutError: If the command does not complete within timeout.
    """
    full_cmd = f'{cmd}; echo "{end_marker}:$?"\n'
    session.send(full_cmd)

    output = ""
    start = time.time()
    pattern = re.compile(rf"{end_marker}:(\d+)")

    while time.time() - start < timeout:
        if session.recv_ready():
            chunk = session.recv(4096).decode(errors="replace")
            output += chunk
            match = pattern.search(output)
            if match:
                break
        else:
            time.sleep(0.2)
    else:
        raise TimeoutError(f"Command timed out after {timeout}s: {cmd}")

    # drain trailing bytes
    drain_start = time.time()
    while time.time() - drain_start < drain_grace:
        if session.recv_ready():
            output += session.recv(4096).decode(errors="replace")
            drain_start = time.time()
        else:
            time.sleep(0.05)

    exit_status = int(match.group(1))
    return exit_status, output

def get_stream_url(stream_name, index_url="https://vts-streams.rdkcentral.com/index.html"):
    """
    Fetches the VTS streams index page and returns the full URL
    matching the given stream filename.

    :param stream_name: The filename to search for, e.g.
                         "vts_h265_2160p_hlg_60.0f_BT2020_yuv420p_60M_ac3_48k_6ch_512k_a1875_v3600_60sec.mp4"
    :param index_url: URL of the index.html to search (default: VTS streams dashboard)
    :return: Full matching URL as a string, or None if not found
    """
    try:
        with urllib.request.urlopen(index_url) as response:
            html = response.read().decode("utf-8")
    except Exception as e:
        print(f"Failed to fetch index page: {e}")
        return None

    # Find all vts-streams URLs in the HTML
    urls = re.findall(r'https://vts-streams[^"]+', html)

    # Look for the one that ends with the given stream_name
    for url in urls:
        if url.endswith(stream_name):
            return url

    return None

def _download_delete_streams(download, streams, remote_dir, device_ip, ssh_port, ssh_user,
                       ssh_password=None, target=None, stream_base=None,
                       timeout=60, stop_on_failure=False):
    """
    Download or delete stream files on the device over SSH.

    Args:
        download (bool): Download streams when True, delete them when False.
        streams (list[str]): Stream names or paths to process.
        remote_dir (str): Remote directory on the device.
        device_ip (str): Device IP address.
        ssh_port (int): SSH port.
        ssh_user (str): SSH username.
        ssh_password (str): SSH password.
        target (str): Test module name.
        stream_base (str): Base URL/path used to build stream download URLs.
        timeout (int): Per-command timeout in seconds.
        stop_on_failure (bool): Raise on the first failure when True.

    Returns:
        list[str]: Names of streams that failed to process.
    """
    delete = not download
    if download:
        action = "Downloading"
    else:
        action = "Deleting"

    print(f"[streams] {action} {len(streams)} items for '{target}' into {remote_dir} on device {device_ip} ...")

    client, session = startSession(device_ip, ssh_user, ssh_password or "", ssh_port)
    if client is None or session is None:
        raise RuntimeError(f"Failed to establish SSH session with {device_ip}")

    failures = []
    try:
        # drain any initial banner/motd
        time.sleep(0.5)
        if session.recv_ready():
            session.recv(4096)

        exit_status, out = _run_shell_cmd(session, f'mkdir -p "{remote_dir}"', timeout=timeout)
        
        if exit_status != 0:
            raise RuntimeError(f"mkdir failed on {device_ip}: {out}")

        for i, s in enumerate(streams, 1):
            fname = s.split("/")[-1].split("?")[0]
            print(f"[streams] ({i}/{len(streams)}) {action} {fname} ...")

            if download:
                s = os.path.basename(s)
                stream_present = get_stream_url(s)
                if stream_present:
                    stream_path = stream_present
                else:
                    stream_path = f'{stream_base}{s}'
                cmd = (
                    f'cd {remote_dir} && '
                    f'curl -sS -L --retry 3 --retry-connrefused -O {stream_path}'
                )
                print(cmd)
            else:
                s = os.path.basename(s)
                cmd = (
                    f'cd {remote_dir} && '
                    f'rm -f {stream_base}{s}'
                )
            #print("Executing command : ",cmd)
            timeout=90
            exit_status, out = _run_shell_cmd(session, cmd, timeout=timeout)
            if exit_status == -1:
                print(f"[streams] TIMEOUT (or unparsed output) for {fname} □~@~T command may still be running on device")
                failures.append(fname)
            elif exit_status != 0:
                print(f"[streams] FAILED: {fname} (exit {exit_status})")
                failures.append(fname)

            if stop_on_failure:
                raise RuntimeError(f"{action} failed for {fname} on {device_ip}")

    finally:
        closeSession(client)

    if failures:
        print(f"[streams] Completed with {len(failures)} failure(s): {failures}")
    else:
        print(f"[streams] All {len(streams)} {action.lower()} completed successfully.")

    return failures


def download_streams_for_target(target: str, streams, config, use_sshpass: bool = False,
                                 allow_self_signed_tls: bool = True,
                                 targetDirectory: str = "NONE") -> None:
    """
    Download the given streams for a target module onto the device.

    Args:
        target (str): Test module name (must be in ALLOWED_DOWNLOAD_MODULES).
        streams (list[str]): Stream names to download.
        config: Loaded vtsconfig_<target> module.
        use_sshpass (bool): Reserved flag for sshpass-based auth.
        allow_self_signed_tls (bool): Reserved flag for self-signed TLS.
        targetDirectory (str): Sub-directory under the device target root.
    """
    if target not in ALLOWED_DOWNLOAD_MODULES:
        return
    stream_base = getattr(config, "STREAM_DOWNLOAD_PATH", None)
    if not stream_base:
        print("[streams] STREAM_DOWNLOAD_PATH is not set in vtsconfig. Skipping download.")
        return
    device_ip    = getattr(config, "DEVICE_IP")
    ssh_user     = getattr(config, "SSH_USERNAME")
    ssh_password = getattr(config, "SSH_PASSWORD", "") or ""
    ssh_port     = getattr(config, "SSH_PORT", 22)
    target_root  = getattr(config, "TARGET_DIRECTORY", "/opt/HAL/").rstrip("/")
    remote_dir   = f"{target_root}/{targetDirectory}"

    yaml_path = _resolve_yaml_path_for_target(target, config)
    if not yaml_path:
        print(f"[streams] YAML not found for '{target}'. Expected one of:\n"
              f"  - {os.path.join(getattr(config, 'TARGET_DIR', '.'), ALLOWED_DOWNLOAD_MODULES[target])}\n"
              f"  - {ALLOWED_DOWNLOAD_MODULES[target]} in current directory")
        return

    if not streams:
        print(f"[streams] No streams listed in YAML for '{target}'. Nothing to download.")
        return

    _download_delete_streams(True, streams, remote_dir, device_ip, ssh_port, ssh_user,
                       ssh_password, target, stream_base,
                       timeout=30, stop_on_failure=False)

#================== REMOVE THE DOWNLOADED STREAMS=============================================


def cleanup_streams_for_target(target: str, streams, config,use_sshpass: bool = False,remove_dir: bool = False,dry_run: bool = False,verbose: bool = True, targetDirectory: str = "NONE") -> None:
    """
    Remove downloaded stream files from the device for the selected target.
    """
    if target not in ALLOWED_DOWNLOAD_MODULES:
        if verbose:
            print(f"[streams-clean] Target '{target}' not in ALLOWED_DOWNLOAD_MODULES; skipping.")
        return

    # Device connection details
    device_ip  = getattr(config, "DEVICE_IP")
    ssh_user   = getattr(config, "SSH_USERNAME")
    ssh_password = getattr(config, "SSH_PASSWORD", "") or ""
    ssh_port   = getattr(config, "SSH_PORT", 22)
    ssh_pass   = getattr(config, "SSH_PASSWORD", "")

    # Remote directory
    target_root = getattr(config, "TARGET_DIRECTORY", "/opt/HAL/").rstrip("/")
    remote_dir  = f"{target_root}/{targetDirectory}"

    yaml_path = _resolve_yaml_path_for_target(target, config)
    if not yaml_path or not os.path.exists(yaml_path):
        if verbose:
            print(f"[streams-clean] YAML not found for '{target}'. Path={yaml_path} → nothing to clean.")
        return

    #streams = _collect_streams_from_yaml(yaml_path)

    mapping = config.STREAM_RENAME_MAP
    rules   = config.STREAM_RENAME_RULES
    def apply_rules(name: str) -> str:
        for rule in rules:
            if isinstance(rule, dict) and "regex" in rule and "replace" in rule:
                name = re.sub(rule["regex"], rule["replace"], name)
        return name

    files_to_delete = []
    seen = set()
    for s in streams:
        if not isinstance(s, str):
            continue
        t = (s or "").strip()
        if not t:
            continue
        
        t = t.split("/")[-1]
        t = mapping.get(t, t)
        t = apply_rules(t)
        
        t = t.split("/")[-1]
        if t and t not in seen:
            seen.add(t)
            files_to_delete.append(t)

    if not files_to_delete and not remove_dir:
        if verbose:
            print(f"[streams-clean] No files resolved for '{target}'. Nothing to delete.")
        return

    if dry_run and verbose:
        print(f"[streams-clean] (dry-run) Would remove from {remote_dir}: {files_to_delete}")
        if remove_dir:
            print(f"[streams-clean] (dry-run) Would also remove directory: {remote_dir}")
        return

    if verbose:
        if remove_dir:
            print(f"[streams-clean] Removing files and directory for '{target}' at {remote_dir} on {device_ip} ...")
        else:
            print(f"[streams-clean] Removing {len(files_to_delete)} files for '{target}' at {remote_dir} on {device_ip} ...")

    _download_delete_streams(False, streams, remote_dir, device_ip, ssh_port, ssh_user, ssh_password, target, "", timeout=30, stop_on_failure=False)

    if verbose:
        print(f"[streams-clean] Cleanup complete for '{target}'.")

#=================== CLEANING THE TEST ASSETS ===================================================

def ensure_preserve_streams_cleanup_override(target: str, config) -> None:
    """
    For stream modules only: comment out 'self.deleteFromDevice(self.testStreams)'
    inside testCleanAssets(self) to preserve downloaded streams on the DUT.
    """
    # Only stream-enabled modules should be modified
    if target not in ALLOWED_DOWNLOAD_MODULES:
        return
    
    base_path = getattr(config, "BASE_PATH", ".")
    host_tests_root = os.path.join(base_path, "host", "tests")

    # Handling rmfaudiocapture
    if target == "rmfaudiocapture":
        helper_dir = os.path.join(host_tests_root, "rmfAudio_L3_TestCases")
        candidate_files = [
            os.path.join(helper_dir, "rmfAudioHelperClass.py"),
            os.path.join(helper_dir, "rmfAudio_HelperClass.py"),  # fallback naming variant
        ]
    else:

        helper_dir = os.path.join(getattr(config, "BASE_PATH", "."), "host", "tests", "L3_TestCases", target)
        candidate_files = [
             os.path.join(helper_dir, f"{target}HelperClass.py"),
             os.path.join(helper_dir, f"{target}_HelperClass.py"),
       ]
    helper_path = next((p for p in candidate_files if os.path.exists(p)), None)
    if not helper_path:
        print(f"[streams-preserve] Helper class not found for target '{target}'. Tried: {candidate_files}")
        return

    try:
        with open(helper_path, "r", encoding="utf-8") as f:
            content = f.read()

        # If already commented, do nothing
        if "self.deleteFromDevice(self.testStreams)" not in content:
            print(f"[streams-preserve] No deletion call found in {helper_path}. Nothing to change.")
            return
        if "# self.deleteFromDevice(self.testStreams)" in content:
            print(f"[streams-preserve] Deletion already commented in {helper_path}.")
            return

        # Replace the exact line with a commented version
        lines = content.splitlines()
        modified = []
        for line in lines:
            if line.strip() == "self.deleteFromDevice(self.testStreams)":
                indent = line[:len(line) - len(line.lstrip())]
                modified.append(indent + "# Stream modules: keep downloaded streams on device.")
                modified.append(indent + "# self.deleteFromDevice(self.testStreams)")
            else:
                modified.append(line)

        new_content = "\n".join(modified)
        with open(helper_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[streams-preserve] Updated cleanup behavior in {helper_path} for target '{target}'.")
    except Exception as e:
        print(f"[streams-preserve] Failed to update {helper_path}: {e}")

# ============= utPlayerConfig.yml UPDATE ===================================================

def add_platform_config_if_missing(config_file, platform, platform_export):
    """
    Append a vendor-specific gstreamer player config block to utPlayerConfig.yml
    if the platform is not already present.

    Args:
        config_file (str): Path to utPlayerConfig.yml.
        platform (str): Platform/vendor key to add (example: broadcom).
        platform_export (str): Newline-separated export lines used as prerequisites.

    Returns:
        bool: True if the platform is present after the operation, False otherwise.
    """
    # Read the existing YAML file
    with open(config_file, "r") as file:
        content = file.read()

    # Check whether platform already exists as a top-level YAML key
    platform_exists = any(
        line.strip() == f"{platform}:"
        for line in content.splitlines()
    )

    if platform_exists:
        print(f"{platform} player config already exists")
        return False

    # Convert platform_export into YAML prerequisite entries
    prerequisites = []
    for line in platform_export.strip().splitlines():
        line = line.strip()
        if line:
            prerequisites.append(f"      - {line}")

    # Build new platform configuration
    platform_config = (
        f"\n{platform}:\n"
        f"  gstreamer:\n"
        f"    prerequisites:\n"
        + "\n".join(prerequisites)
        + "\n"
        f"    play_command: gst-play-1.0\n"
        f"    stop_command: \"\\x03\" # CNTRL-C\n"
        f"    primary_mixer_input_config: \"\"\n"
        f"    secondary_mixer_input_config: \"\"\n"
    )

    # Append to YAML
    with open(config_file, "a") as file:
        file.write(platform_config)

    # Verify that it was actually written
    with open(config_file, "r") as file:
        updated_content = file.read()

    if f"{platform}:" not in updated_content:
        raise RuntimeError(
            f"Failed to add platform '{platform}' to {config_file}"
        )

    print(f"Added {platform} player config values")
    print(
        f"✓ utPlayerConfig.yml updated for vendor '{platform}' "
        f"at {config_file}"
    )

    print(f"Checking file: {config_file}")

    with open(config_file, "r") as file:
        content = file.read()

    print(f"{platform} present: {'platform:' in content}")
    return (platform in content)

def update_ut_player_config():
    """
    Ensure utPlayerConfig.yml contains the vendor-specific gstreamer 'prerequisites' block
    for config.SOC_VENDOR (default: 'broadcom').
    """
    vendor = getattr(config, 'SOC_VENDOR', 'broadcom').lower()
    file_name = getattr(config, 'UTPLAYERCONFIG_FILE', 'utPlayerConfig.yml')
    default_path = os.path.join(getattr(config, 'BASE_PATH', '.'),
                                'host','tests','raft','framework','plugins','ut_raft','configs', file_name)
    yml_path = getattr(config, 'UTPLAYERCONFIG_PATH', default_path)

    if not os.path.exists(yml_path):
        raise FileNotFoundError(f"utPlayerConfig.yml not found at: {yml_path}")

    with open(yml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    vendor_re = re.compile(rf"^\\n?{vendor}:\\s*\\n(?:[\\s\\S]*?)(?=^\\w+:|\\Z)", re.MULTILINE)

    if vendor == 'broadcom':
        existing_broadcom_re = re.compile(r"^\n?broadcom:\s*\n(?:[\s\S]*?)(?=^\w+:|\Z)", re.MULTILINE)
        if re.search(existing_broadcom_re, content):
            print("✓ 'broadcom' block already present in utPlayerConfig.yml. No changes applied.")
        else:
            print("⚠ Adding broadcom player config values before execution")
            added = add_platform_config_if_missing(yml_path, vendor, PLATFORM_EXPORTS)
            if added:
                print(f"Added broadcom player config values")
            else:
                print(f"Platform already exists: {vendor}")


            #content = content.rstrip() + "\n" + broadcom_block
            #print("✓ Appended 'broadcom' block to utPlayerConfig.yml.")
    
    elif vendor in ('realtek', 'amlogic'):
        if re.search(vendor_re, content):
            print(f"✓ utPlayerConfig.yml already contains vendor '{vendor}' block. No changes applied.")
        else:
            print(f"⚠ Vendor '{vendor}' block not found in utPlayerConfig.yml. Skipping update for '{vendor}'.")

    else:
        raise ValueError(f"Unsupported vendor '{vendor}'.Supported vendors: broadcom, realtek, amlogic.")

    #with open(yml_path, 'w', encoding='utf-8') as f:
    #    f.write(content)

    print(f"✓ utPlayerConfig.yml updated for vendor '{vendor}' at {yml_path}")


#=================== COMMENT OUT DOWNLOAD CALLS=================================================

def comment_download_calls_in_helper(target: str,base_path: str,enabled_targets: Optional[Iterable[str]] = None,note_text: Optional[str] = None,) -> None:
    """
    Comment out ONLY the precise call:
        self.downloadToDevice(url, self.targetWorkspace, self.rackDevice)
    """
    
    if enabled_targets is not None and target not in enabled_targets:
        print(f"[download-comment] Target '{target}' not enabled; skipping.")
        return

    if target == "rmfaudiocapture":
        helper_dir = os.path.join(base_path, "host", "tests", "rmfAudio_L3_TestCases")
        candidate_files = [
            os.path.join(helper_dir, "rmfAudioHelperClass.py"),
            os.path.join(helper_dir, "rmfAudio_HelperClass.py"),  
        ]
    else:

        helper_dir = os.path.join(base_path, "host", "tests", "L3_TestCases", target)
        candidate_files = [
              os.path.join(helper_dir, f"{target}HelperClass.py"),
              os.path.join(helper_dir, f"{target}_HelperClass.py"),   
        ]
    helper_path = next((p for p in candidate_files if os.path.exists(p)), None)
    if not helper_path:
        print(f"[download-comment] Helper class not found for target '{target}'. Tried: {candidate_files}")
        return

    strict_call_pattern = re.compile(
        r"""^(\s*)                                   # capture indentation
            self\.downloadToDevice\(
                \s*url\s*,\s*self\.targetWorkspace\s*,\s*self\.rackDevice\s*
            \)\s*$""",
        re.VERBOSE | re.MULTILINE
    )

    # Already-commented detection for the exact call
    already_commented_pattern = re.compile(
        r"""^\s*#\s*self\.downloadToDevice\(
                \s*url\s*,\s*self\.targetWorkspace\s*,\s*self\.rackDevice\s*
            \)\s*$""",
        re.VERBOSE | re.MULTILINE
    )

    if note_text is None:
        note_text = "Downloads disabled (policy/config); keeping DUT clean."

    try:
        with open(helper_path, "r", encoding="utf-8") as f:
            content = f.read()

        occurrences = len(re.findall(strict_call_pattern, content))
        already = len(re.findall(already_commented_pattern, content))

        if occurrences == 0 and already == 0:
            print(f"[download-comment] No matching precise download calls found in {helper_path}. Nothing to change.")
            return
        if occurrences == 0 and already > 0:
            print(f"[download-comment] All precise calls already commented in {helper_path}.")
            return

        def replacer(match: re.Match) -> str:
            indent = match.group(1)
            note = indent + f"# {note_text}\n"
            commented = indent + "# self.downloadToDevice(url, self.targetWorkspace, self.rackDevice)"
            return note + commented

        new_content, replacements = re.subn(strict_call_pattern, replacer, content)

        if replacements > 0:
            with open(helper_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[download-comment] Commented {replacements} precise download call(s) in {helper_path}.")
        else:
            print(f"[download-comment] No new changes applied in {helper_path} (possibly already commented).")

    except Exception as e:
        print(f"[download-comment] Failed to update {helper_path}: {e}")

#=============== RUNNING ONE BY ONE TESTCASES SEQUENTIALLY=====================================

def _run_one_script_with_logging(script_path: str, logfile):
    """
    Run a single script in a pseudo-terminal, forwarding output to console and logfile.
    """
    master, slave = pty.openpty()

    # Build command: source venv, cd to target dir, run script with args
    command = f"""
        source {shlex.quote(config.VENV_SCRIPT)} && \
        cd {shlex.quote(config.TARGET_DIR)} && \
        python {shlex.quote(script_path)} --config {shlex.quote(config.RACK_CONFIG_ARG)} --deviceConfig {shlex.quote(config.DEVICE_CONFIG_ARG)}
    """

    process = subprocess.Popen(
        ["/bin/bash", "-c", command],
        stdin=slave,
        stdout=slave,
        stderr=slave,
        close_fds=True
    )

    
    os.close(slave)

    stdin_fd = sys.stdin.fileno()
    orig_attr = termios.tcgetattr(stdin_fd)
    tty.setraw(stdin_fd)  

    try:
        while process.poll() is None:
            # Wait for output or user input
            ready, _, _ = select.select([master, sys.stdin], [], [], config.SELECT_TIMEOUT)

            if master in ready:
                try:
                    data = os.read(master, config.TERMINAL_BUFFER_SIZE)
                except OSError:
                    break

                if data:
                    decoded = data.decode("utf-8", errors="ignore")
                    sys.stdout.write(decoded)
                    sys.stdout.flush()
                    logfile.write(decoded)
                    if "core dumped" in str(decoded):
                        print("\nERROR: Exiting from test, Observed crash during execution")
                        logfile.write("ERROR: Observed crash during execution")
                    if "symbol lookup error" in  str(decoded):
                        print("\nERROR: Exiting from test, symbol lookup error observed during execution")
                        logfile.write("ERROR: Exiting from test, symbol lookup error observed during execution")
                    if "Segmentation fault" in  str(decoded):
                        print("\nERROR: Exiting from test, segmentation fault observed during execution")
                        logfile.write("ERROR: Exiting from test, segmentation fault observed during execution")
                    logfile.flush()
                    if "core dumped" in str(decoded) or "symbol lookup error" in  str(decoded) or "Segmentation fault" in  str(decoded):
                        return 0

            # Read single keypress from user
            if sys.stdin in ready:
                try:
                    user_input = sys.stdin.read(1)  # single character
                    if user_input:
                        # === Ctrl+Z stop immediately ===
                        if user_input == '\x1A':
                            
                            try:
                                process.terminate()
                            except Exception:
                                pass
                            # Return a conventional "user-terminated" code
                            # so the caller can stop the remaining scripts.
                            return 130

                    os.write(master, user_input.encode())
                except (OSError, IOError):
                    break

    except KeyboardInterrupt:
        try:
            process.terminate()
        except Exception:
            pass
    finally:
        # Restore terminal settings even if errors occur
        try:
            termios.tcsetattr(stdin_fd, termios.TCSANOW, orig_attr)
        except Exception:
            pass

        try:
            os.close(master)
        except OSError:
            pass

    return process.wait()


def get_streams_for_testfile(py_filename, repo_root="."):
    """
    Given a test filename like:
        dsAudio_test01_EnableDisableAndVerifyAudioPortStatus.py

    Finds the file under repo_root, locates the module's *_L3_testSetup.yml
    in the same folder, and returns the list of stream basenames configured
    for that specific test.
    """
    # 1. Find the .py file anywhere under repo_root
    found_path = None
    for dirpath, _, filenames in os.walk(repo_root):
        if py_filename in filenames:
            found_path = os.path.join(dirpath, py_filename)
            break

    if not found_path:
        raise FileNotFoundError(f"{py_filename} not found under {repo_root}")

    module_dir = os.path.dirname(found_path)

    # 2. Find the L3_testSetup.yml in the same directory
    yml_file = None
    for f in os.listdir(module_dir):
        if f.lower().endswith("l3_testsetup.yml"):
            yml_file = os.path.join(module_dir, f)
            break

    if not yml_file:
        raise FileNotFoundError(f"No *_L3_testSetup.yml found in {module_dir}")

    # 3. Derive the test key, e.g. "dsAudio_test01_..." -> "test01_..."
    module_name = os.path.basename(module_dir)  # e.g. dsAudio
    base = os.path.splitext(py_filename)[0]
    prefix = module_name + "_"
    test_key = base[len(prefix):] if base.startswith(prefix) else base

    # 4. Parse the yml for that key's "streams:" block (indentation-based, no pyyaml needed)
    return extract_streams_for_key(yml_file, test_key)


def extract_streams_for_key(yml_path, test_key):
    """
    Extract the list of stream basenames configured under a specific test key
    in a *_L3_testSetup.yml file using indentation-based parsing.

    Args:
        yml_path (str): Path to the test setup YAML file.
        test_key (str): Test key whose 'streams:' block should be read.

    Returns:
        list[str]: Stream basenames configured for the given test key.
    """
    stream_pattern = re.compile(r'^\s*-\s*(?:"([^"]*)"|\'([^\']*)\'|(\S+))\s*$')
    key_pattern = re.compile(rf'^(\s*){re.escape(test_key)}\s*:\s*$')

    streams = []
    in_block = False
    key_indent = None

    with open(yml_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            stripped = line.rstrip("\n")

            m = key_pattern.match(stripped)
            if m:
                in_block = True
                key_indent = len(m.group(1))
                continue

            if in_block:
                if stripped.strip() == "":
                    continue
                cur_indent = len(stripped) - len(stripped.lstrip())
                if cur_indent <= key_indent:
                    break  # left the test's block
                sm = stream_pattern.match(stripped)
                if sm:
                    name = sm.group(1) or sm.group(2) or sm.group(3)
                    if name and name.strip():
                        streams.append(name.strip())

    # return basenames only, e.g. "streams/tones_string_48k_stereo.ac3" -> "tones_string_48k_stereo.ac3"
    return [s.rsplit("/", 1)[-1] for s in streams]


def run_interactive_with_logging(config, target, log_path : str = "test_run.log"):
    """
    Run one or more interactive tests sequentially with logging.
    """
    
    ts = getattr(config, "TEST_SCRIPT", None)
    if ts is None:
        raise ValueError("config.TEST_SCRIPT is not set")
    scripts = ts if isinstance(ts, (list, tuple)) else [ts]

    #log_path = getattr(config, "LOG_FILE", "test_run.log")
    #os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)

    results = []

    with open(log_path, "w") as logfile:
        total = len(scripts)
        for idx, script in enumerate(scripts, start=1):
            header = (
                f"\n===== [{idx}/{total}] Running {os.path.basename(script)} "
                f"at {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n"
            )
            sys.stdout.write(header); sys.stdout.flush()
            logfile.write(header); logfile.flush()
            streams = get_streams_for_testfile(script)
            if streams:
                testModule = target
                download_streams_for_target(target, streams, config,use_sshpass=bool(getattr(config, "SSH_PASSWORD","")),allow_self_signed_tls=True, targetDirectory=testModule)
                ensure_preserve_streams_cleanup_override(testModule, config)
            try:
                rc = _run_one_script_with_logging(script, logfile)
            finally:
                if streams:
                    cleanup_streams_for_target(target, streams, config, targetDirectory=testModule)
            results.append((script, rc))

            footer = (
                f"\n----- Completed {os.path.basename(script)} "
                f"with exit code {rc} -----\n"
            )
            sys.stdout.write(footer); sys.stdout.flush()
            logfile.write(footer); logfile.flush()

            # Stop immediately if user pressed Ctrl+Z (rc == 130)
            if rc == 130:
                sys.stdout.write("\n[runner] Stop requested by user (Ctrl+Z). Halting remaining scripts.\n")
                sys.stdout.flush()
                break

            if getattr(config, "STOP_ON_FAILURE", False) and rc != 0:
                break

    # Summary
    summary_lines = ["\nSummary:"]
    for script, rc in results:
        status = "EXECUTED" if rc == 0 else f"NOT EXECUTED({rc})"
        summary_lines.append(f" - {os.path.basename(script)}: {status}")
    sys.stdout.write("\n".join(summary_lines) + "\n")
    sys.stdout.flush()

    # Return True if all passed
    return all(rc == 0 for _, rc in results)


def patch_targetWorkspace(repo_dir, moduleName, testModule):
    """
    Patch <testModule>HelperClass.py to replace:
        self.targetWorkspace = os.path.join(self.targetWorkspace, self.moduleName)
    with:
        self.targetWorkspace = os.path.join(self.targetWorkspace, "<moduleName>")

    Args:
        repo_dir (str): Path to repo root
        moduleName (str): module name to hardcode (example: device_settings)
        testModule (str): test module name (example: dsVideoPort)

    Returns:
        bool: True if patched or already patched, False otherwise
    """

    file_path = os.path.join(
        repo_dir,
        f"{testModule}HelperClass.py"
    )

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    with open(file_path, "r") as f:
        content = f.read()

    # ✅ If already patched with requested moduleName
    already_pattern = rf'self\.targetWorkspace\s*=\s*os\.path\.join\(\s*self\.targetWorkspace\s*,\s*"{re.escape(moduleName)}"\s*\)'
    if re.search(already_pattern, content):
        print(f"✅ Already patched: moduleName='{moduleName}' in {file_path}")
        return True

    # ✅ Look for original line
    old_pattern = r'self\.targetWorkspace\s*=\s*os\.path\.join\(\s*self\.targetWorkspace\s*,\s*self\.moduleName\s*\)'

    if not re.search(old_pattern, content):
        print(f"❌ Original targetWorkspace line not found in {file_path}")
        return False

    # ✅ Replace with hardcoded moduleName
    new_line = f'self.targetWorkspace = os.path.join(self.targetWorkspace, "{moduleName}")'
    modified_content = re.sub(old_pattern, new_line, content, count=1)

    with open(file_path, "w") as f:
        f.write(modified_content)

    print(f"✅ Patched successfully: {file_path}")
    return True

#============================================================================================

def main():
    """Main function with options"""
    # Parse positional target (dsHost|dsDisplay) and optional flag
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print("Usage:")
        print("  python vts_l3_executor.py dsHost|dsDisplay|dsVideoDevice|dsVideoPort                 # Run L3 tests for selected target")
        print("  python vts_l3_executor.py dsHost --config                  # Show current configuration (Host)")
        print("  python vts_l3_executor.py dsHost --validate                # Validate configuration and paths (Host)")
        print("  python vts_l3_executor.py dsHost --update-config           # Update config files with current parameters (Host)")
        print("  python vts_l3_executor.py dsDisplay --config               # Show current configuration (Display)")
        print("  python vts_l3_executor.py dsDisplay --validate             # Validate configuration and paths (Display)")
        print("  python vts_l3_executor.py dsDisplay --update-config        # Update config files with current parameters (Display)")
        print("  python vts_l3_executor.py dsVideoDevice --config               # Show current configuration (VideoDevice)")
        print("  python vts_l3_executor.py dsVideoDevice --validate             # Validate configuration and paths (VideoDevice)")
        print("  python vts_l3_executor.py dsVideoDevice --update-config        # Update config files with current parameters (VideoDevice)")
        print("  python vts_l3_executor.py dsVideoPort --config               # Show current configuration (VideoPort)")
        print("  python vts_l3_executor.py dsVideoPort --validate             # Validate configuration and paths (VideoPort)")
        print("  python vts_l3_executor.py dsVideoPort --update-config        # Update config files with current parameters (VideoPort)")
        print("  python vts_l3_executor.py dsAudio --config               # Show current configuration (Audio")
        print("  python vts_l3_executor.py dsAudio --validate             # Validate configuration and paths (Audio)")
        print("  python vts_l3_executor.py dsAudio --update-config        # Update config files with current parameters (Audio)")
        print("  python vts_l3_executor.py deepsleep --config               # Show current configuration (Deepsleep)")
        print("  python vts_l3_executor.py deepsleep --validate             # Validate configuration and paths (Deepsleep)")
        print("  python vts_l3_executor.py deepsleep --update-config        # Update config files with current parameters (Deepsleep)")
        print("  python vts_l3_executor.py rmfaudiocapture --config               # Show current configuration (RmfAudioCapture)")
        print("  python vts_l3_executor.py rmfaudiocapture --validate             # Validate configuration and paths (RmfAudioCapture)")
        print("  python vts_l3_executor.py rmfaudiocapture --update-config        # Update config files with current parameters (RmfAudioCapture)")
        print("\nEnvironment Variables:")
        print("  VTS_DEVICE_IP           # Override device IP")
        print("  VTS_BASE_PATH           # Override base path")
        return

    target = sys.argv[1]
    global config
    config = load_config_for_target(target)  
    setup_halif_test()

    unique_string = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    # Always ensure SCP is skipped at startup
    modify_scpCopy_to_skip()
    modify_waitForBoot_to_return_true_if_needed()
    if target == "dsVideoPort" or target == "dsAudio" or target == "dsVideoDevice" or target == "rmfaudiocapture":
        testModule = target
        #if target == "rmfaudiocapture":
        #    testModule = "rmf_audio_capture"
        #else:
        #    testModule = "device_settings"
        patch_targetWorkspace(config.TARGET_DIR, testModule, target)
        patch_testCleanSingleAsset_skip_cleanup(config.TARGET_DIR, target)
    
    # Optional flag after the target
    flag = sys.argv[2] if len(sys.argv) > 2 else None
    if flag == '--config':
        try:
            config.print_config()
        except AttributeError:
            print_current_config()
        return
    elif flag == '--validate':
        # Use module's print_config() as validation output
        try:
            config.print_config()
        except AttributeError:
            print_current_config()
        return
    elif flag == '--update-config':
        # Update only the selected target's YAML config files
        # Only dsDisplay needs monitor YAML updates
        if target == 'dsDisplay':
            update_monitor_yaml()
        update_all_configs()
        update_ut_player_config()
        return
    elif flag in ('--help', '-h'):
        # Already covered above
        return

    # No flags → run L3 tests for the selected target
    print(f"Target: {target}")
    print("Starting VTS L3 Test Framework...")
    print("Virtual environment will be activated automatically...")
    base_path = getattr(config, "BASE_PATH", "<unknown>")
    print(f"Base Path: {base_path}")
    print("=" * 60)

    if target in ('dsVideoPort','dsAudio'):
            # Preview normalized names
            normalized = get_normalized_streams_for_target(target, config)
            print(f"[streams-rename] Preview ({target}): {normalized}")
            rewrite_testsetup_yaml_streams_with_renames(target, config)
    #if target in ALLOWED_DOWNLOAD_MODULES:
    #        download_streams_for_target(target, config,use_sshpass=bool(getattr(config, "SSH_PASSWORD","")),allow_self_signed_tls=True, targetDirectory=testModule)
    #        ensure_preserve_streams_cleanup_override(testModule, config)
    if target in ('dsVideoPort','dsAudio','rmfaudiocapture'):
            comment_download_calls_in_helper(target=target,base_path=config.BASE_PATH,enabled_targets=None,note_text="Skipping asset downloads on DUT for this run.")

    log_path = target + "_" + unique_string + ".log"
    run_interactive_with_logging(config, target, log_path)
    excel_sheet_path = target + "_" + unique_string + ".xlsx"
    print("Removing embedded characters from log file")
    subprocess.run(["sed", "-i", "-e", "s/\r//g", log_path],check=True)
    #if target in ALLOWED_DOWNLOAD_MODULES:
    #        # Remove only files (keep directory)
    #        cleanup_streams_for_target(target=target,config=config,use_sshpass=bool(getattr(config, "SSH_PASSWORD", "")),
    #                                         remove_dir=False,      # set True if you want to remove /opt/HAL/<target> entirely
    #                                         dry_run=False,         # set True to preview without deleting
    #                                         verbose=True,targetDirectory=testModule)

    excel_path = target + "_" + unique_string + ".xlsx"
    saved_path = process_log_to_excel(log_path, excel_path)
    print(f"Report Generated : {saved_path}")

if __name__ == "__main__":
    main()
