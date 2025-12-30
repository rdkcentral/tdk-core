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
import pandas as pd
import shlex
import time
import yaml
import importlib
from collections import OrderedDict
from typing import Optional, List, Iterable

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
            subprocess.run(["./install.sh"], cwd=host_dir, check=True)
        except subprocess.CalledProcessError:
            print("ℹ️ Initial install.sh exited with non-zero status (expected). Proceeding to activate venv...")
            
        # Step 4: Source activate_venv.sh and rerun install.sh
        print("🧪 Activating virtual environment and rerunning install.sh...")
        subprocess.run(["bash", "-c", "source ./activate_venv.sh && ./install.sh"], cwd=host_dir, check=True)

        print("✅ RAFT setup completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error during RAFT setup: {e}")

# ============= SCP MODIFICATION FUNCTIONS =============

def modify_scpCopy_to_skip(file_path):
    """
    Modify the scpCopy function in the given file to return 'skipped' immediately.
    
    Args:
        file_path (str): Path to the Python file containing scpCopy function
    
    Returns:
        bool: True if modification was successful, False otherwise
    """
    try:
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

def ensure_scp_skipped():
    """Ensure scpCopy function is skipped by default"""
    print("Checking and modifying SCP function...")
    if os.path.exists(config.UTBASEUTILS_PATH):
        modify_scpCopy_to_skip(config.UTBASEUTILS_PATH)
    else:
        print(f"Warning: utBaseUtils.py not found at {config.UTBASEUTILS_PATH}")

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
        import yaml
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
        import yaml
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
        raise ValueError("MONITOR_YAML_PATH is not set in vtsconfig.py")

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
         mapping = STREAM_RENAME_MAP_BY_MODULE.get(target, {}) or {}

    rules = getattr(config, "STREAM_RENAME_RULES", None)
    if rules is None:
        rules = STREAM_RENAME_RULES_BY_MODULE.get(target, []) or []


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

    yaml_path = _resolve_yaml_path_for_target(target, config)
    if not yaml_path or not os.path.exists(yaml_path):
        print(f"[streams-rename] Cannot rewrite: YAML not found for '{target}'. Path={yaml_path}")
        return 0

    with open(yaml_path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    
    mapping = getattr(config, "STREAM_RENAME_MAP", None)
    if mapping is None:
         mapping = STREAM_RENAME_MAP_BY_MODULE.get(target, {}) or {}

    rules = getattr(config, "STREAM_RENAME_RULES", None)
    if rules is None:
        rules = STREAM_RENAME_RULES_BY_MODULE.get(target, []) or []


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

def _build_url_and_filename(stream: str, base_url: str):
    """
    If the YAML stream entry is a full URL, use it.
    Otherwise join with base_url. Local filename is the URL basename.
    """
    if stream.startswith(("http://", "https://")):
        url = stream
        filename = os.path.basename(stream.split("?")[0])
    else:
        url = base_url.rstrip("/") + "/" + stream.lstrip("/")
        filename = os.path.basename(stream.split("?")[0])
    return url, filename

def download_streams_for_target(target: str,config,use_sshpass: bool = False,allow_self_signed_tls: bool = True) -> None:
    """
    Download streams for the selected target *only* if it is in ALLOWED_DOWNLOAD_MODULES.
    """
    if target not in ALLOWED_DOWNLOAD_MODULES:
        return

    stream_base = getattr(config, "STREAM_DOWNLOAD_PATH", None)
    if not stream_base:
        print("[streams] STREAM_DOWNLOAD_PATH is not set in vtsconfig. Skipping download.")
        return

    device_ip  = getattr(config, "DEVICE_IP")
    ssh_user   = getattr(config, "SSH_USERNAME")
    ssh_port   = getattr(config, "SSH_PORT", 22)

    target_root = getattr(config, "TARGET_DIRECTORY", "/opt/HAL/").rstrip("/")
    remote_dir  = f"{target_root}/{target}"

    yaml_path = _resolve_yaml_path_for_target(target, config)
    if not yaml_path:
        print(f"[streams] YAML not found for '{target}'. Expected one of:\n"
              f"  - {os.path.join(getattr(config, 'TARGET_DIR', '.'), ALLOWED_DOWNLOAD_MODULES[target])}\n"
              f"  - {ALLOWED_DOWNLOAD_MODULES[target]} in current directory")
        return

    streams = _collect_streams_from_yaml(yaml_path)
    if not streams:
        print(f"[streams] No streams listed in YAML for '{target}'. Nothing to download.")
        return

    prelude_cmds = [
        f'mkdir -p "{remote_dir}"',
        f'cd "{remote_dir}"',
    ]

    wget_flags = ["-nv", "-c", "--timeout=30"]
    #wget_flags = ["-q", "-c", "-T", "30"]
    if allow_self_signed_tls:
        wget_flags.append("--no-check-certificate")

    wget_cmds = []
    for s in streams:
        url, fname = _build_url_and_filename(s, stream_base)
        wget_cmds.append(f'wget {" ".join(wget_flags)} "{url}" -O "{fname}"')

    check_wget = "command -v wget >/dev/null 2>&1"
    fallback_curl = (
        'echo "wget not found. Using curl..." && '
        f'cd "{remote_dir}" && '
        "for u in " + " ".join([f'"{_build_url_and_filename(s, stream_base)[0]}"' for s in streams]) + "; do "
        'fname=$(basename "${u%%\\?*}"); '
        'curl -L --retry 3 --retry-connrefused -o "$fname" "$u" || exit 1; '
        "done"
    )

    remote_cmd = (
        f"{check_wget} && ( " +
        " && ".join(prelude_cmds + wget_cmds) +
        f" ) || ( {fallback_curl} )" 
    )

    ssh_cmd = [
        "ssh",
        "-p", str(ssh_port),
        f"{ssh_user}@{device_ip}",
        remote_cmd,
    ]
    ssh_password = getattr(config, "SSH_PASSWORD", "")
    if use_sshpass and ssh_password:
        ssh_cmd = ["sshpass", "-p", ssh_password] + ssh_cmd

    
    print(f"[streams] Downloading {len(streams)} items for '{target}' into {remote_dir} on device {device_ip} ...")
    subprocess.run(ssh_cmd, check=True)

    # Final list from the device
    ls_cmd = [
        "ssh", "-p", str(ssh_port),
        f"{ssh_user}@{device_ip}",
        f'ls -lh "{remote_dir}"'
    ]
    subprocess.run(ls_cmd, check=True)
    print(f"[streams] Download complete for '{target}'.")

#================== REMOVE THE DOWNLOADED STREAMS=============================================

def cleanup_streams_for_target(target: str,config,use_sshpass: bool = False,remove_dir: bool = False,dry_run: bool = False,verbose: bool = True,) -> None:
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
    ssh_port   = getattr(config, "SSH_PORT", 22)
    ssh_pass   = getattr(config, "SSH_PASSWORD", "")

    # Remote directory
    target_root = getattr(config, "TARGET_DIRECTORY", "/opt/HAL/").rstrip("/")
    remote_dir  = f"{target_root}/{target}"

    yaml_path = _resolve_yaml_path_for_target(target, config)
    if not yaml_path or not os.path.exists(yaml_path):
        if verbose:
            print(f"[streams-clean] YAML not found for '{target}'. Path={yaml_path} → nothing to clean.")
        
        if remove_dir:
            _cleanup_remote_dir(remote_dir, device_ip, ssh_user, ssh_port, ssh_pass, use_sshpass, dry_run, verbose)
        return

    streams = _collect_streams_from_yaml(yaml_path)

    mapping = STREAM_RENAME_MAP_BY_MODULE.get(target, {}) or {}
    rules   = STREAM_RENAME_RULES_BY_MODULE.get(target, []) or []

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

    cmds = [f'mkdir -p "{remote_dir}"', f'cd "{remote_dir}"']
    if files_to_delete:
        rm_files = " && ".join([f'rm -f -- "{fn}"' for fn in files_to_delete])
        cmds.append(rm_files)


    if remove_dir:
        # Go to parent and remove the target dir
        parent = target_root
        cmds.append(f'cd "{parent}"')
        cmds.append(f'rm -rf -- "{target}"')

    remote_cmd = " && ".join(cmds)

    
    ssh_cmd = [
        "ssh",
        "-p", str(ssh_port),
        f"{ssh_user}@{device_ip}",
        remote_cmd,
    ]
    if use_sshpass and ssh_pass:
        ssh_cmd = ["sshpass", "-p", ssh_pass] + ssh_cmd

    if verbose:
        if remove_dir:
            print(f"[streams-clean] Removing files and directory for '{target}' at {remote_dir} on {device_ip} ...")
        else:
            print(f"[streams-clean] Removing {len(files_to_delete)} files for '{target}' at {remote_dir} on {device_ip} ...")

    subprocess.run(ssh_cmd, check=True)

    # Final list
    if not remove_dir:
        ls_cmd = [
            "ssh", "-p", str(ssh_port),
            f"{ssh_user}@{device_ip}",
            f'ls -lh "{remote_dir}" || true'
        ]
        subprocess.run(ls_cmd, check=False)

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

    # Exact Broadcom block (spec as provided)
    broadcom_block = (
        "broadcom:\n"
        "  gstreamer:\n"
        "    prerequisites:\n"
        "      - export WAYLAND_DISPLAY=wayland-0\n"
        "      - export WESTEROS_SINK_USE_ESSRMGR=1\n"
        "      - export AAMP_ENABLE_WESTEROS_SINK=1\n"
        "      - export GST_ENABLE_SVP=1\n"
        "      - export GST_VIRTUAL_DISP_WIDTH=1920\n"
        "      - export GST_VIRTUAL_DISP_HEIGHT=1080\n"
        "      - export GST_VIRTUAL_SD_DISP_WIDTH=1920\n"
        "      - export GST_VIRTUAL_SD_DISP_HEIGHT=1080\n"
        "      - export do_not_change_display=true\n"
        "      - export SAGEBIN_PATH=/usr/bin/\n"
        "      - export XDG_RUNTIME_DIR=/run\n"
        "      - export LD_PRELOAD=libwayland-client.so.0:libwayland-egl.so.1:libnxclient.so:libsrai.so:liboemcrypto_tl.so:libwesteros_gl.so.0.0.0\n"
        "      - export WESTEROS_DRM_CARD=/dev/dri/card1\n"
        "      - export WESTEROS_GL_GRAPHICS_MAX_SIZE=1920x1080\n"
        "      - export WESTEROS_GL_MODE=1920x1080x60\n"
        "      - export WESTEROS_GL_USE_REFRESH_LOCK=1\n"
        "      - export WESTEROS_GL_FPS=1\n"
        "    play_command: gst-play-1.0\n"
        "    stop_command: \"\\x03\" # CNTRL-C\n"
        "    primary_mixer_input_config: \"\"\n"
        "    secondary_mixer_input_config: \"\"\n"
    )

    vendor_re = re.compile(rf"^\\n?{vendor}:\\s*\\n(?:[\\s\\S]*?)(?=^\\w+:|\\Z)", re.MULTILINE)

    if vendor == 'broadcom':
        existing_broadcom_re = re.compile(r"^\n?broadcom:\s*\n(?:[\s\S]*?)(?=^\w+:|\Z)", re.MULTILINE)
        if re.search(existing_broadcom_re, content):
            print("✓ 'broadcom' block already present in utPlayerConfig.yml. No changes applied.")
        else:
            content = content.rstrip() + "\n" + broadcom_block
            print("✓ Appended 'broadcom' block to utPlayerConfig.yml.")
    
    elif vendor in ('realtek', 'amlogic'):
        if re.search(vendor_re, content):
            print(f"✓ utPlayerConfig.yml already contains vendor '{vendor}' block. No changes applied.")
        else:
            print(f"⚠ Vendor '{vendor}' block not found in utPlayerConfig.yml. Skipping update for '{vendor}'.")

    else:
        raise ValueError(f"Unsupported vendor '{vendor}'.Supported vendors: broadcom, realtek, amlogic.")

    with open(yml_path, 'w', encoding='utf-8') as f:
        f.write(content)

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
                    logfile.flush()

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

def run_interactive_with_logging():
    """
    Run one or more interactive tests sequentially with logging.
    """
    
    ts = getattr(config, "TEST_SCRIPT", None)
    if ts is None:
        raise ValueError("config.TEST_SCRIPT is not set")
    scripts = ts if isinstance(ts, (list, tuple)) else [ts]

    log_path = getattr(config, "LOG_FILE", "test_run.log")
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)

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

            rc = _run_one_script_with_logging(script, logfile)
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

#================= EXCEL GENERATION ===================================================

def generate_excel_from_log(target: str,log_path: str = "menu.log",excel_path: str = "final_test_results.xlsx",wait_for_log_close_secs: float = 0.5):
    """
    Parse RAFT output from `menu.log` and write `final_test_results.xlsx`.
    """

    time.sleep(wait_for_log_close_secs)

    log_path = os.path.abspath(log_path)
    excel_path = os.path.abspath(excel_path)

    if not os.path.exists(log_path):
        print(f"✗ Log not found: {log_path} (cwd={os.getcwd()})")
        return

    ansi_re = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [ansi_re.sub('', line.rstrip('\n')) for line in f]

    # Summary-level FAIL marker
    summary_fail_re = re.compile(r"TEST_RESULT\s*:\s*\[FAILED\]", re.IGNORECASE)

    # Start / completion markers
    found_re      = re.compile(r"Found test:\s*\[(.*?)\]", re.IGNORECASE)
    running_re    = re.compile(r"Running Test\s*:\s*'([^']+)'", re.IGNORECASE)
    complete_re   = re.compile(r"Test Complete\s*:\s*'(.*?)'", re.IGNORECASE)
    suite_line_re = re.compile(r"Suite:\s*\[(.*?)\]", re.IGNORECASE)

    
    expected_suite_frag = f"L3 {target}"

    def classify_result(test_name: str, log_text: str):
        pass_patterns = [
            r"Result\s+.*\[\s*dsERR_NONE\s*\]",
            r"\bPASSED\b",
        ]
        fail_patterns = [
            r"\bFAILED\b",
            r"undefined symbol",
            r"symbol lookup error",
            r"segmentation fault",
            r"\bassert\b",
            r"\bexception\b",
            r"\btraceback\b",
            r"command not found",
            r"error:\s*",
        ]
        completes = set(complete_re.findall(log_text))
        passed_hits = [p for p in pass_patterns if re.search(p, log_text, re.IGNORECASE)]
        failed_hits = [p for p in fail_patterns if re.search(p, log_text, re.IGNORECASE)]

        if failed_hits:
            return "FAILED", f"Failure markers found: {', '.join(failed_hits)}"
        if passed_hits and (test_name in completes):
            return "PASSED", f"Found PASSED markers ({', '.join(passed_hits)}) and matching 'Test Complete' for '{test_name}'"
        if passed_hits and (test_name not in completes):
            return "FAILED", f"Found PASSED markers ({', '.join(passed_hits)}) but missing 'Test Complete' for '{test_name}'"
        if test_name in completes:
            return "PASSED", "No explicit markers, but found matching 'Test Complete'"
        return "FAILED", "Missing 'Test Complete' and no explicit pass markers"

    # Parse with target filtering
    test_data = OrderedDict()
    current_test = None
    current_log  = []
    current_suite = None  

    def finalize_current():
        if current_test is None:
            return
        
        block_text = "\n".join(current_log)
        
        suite_match = suite_line_re.search(block_text)
        suite_name = suite_match.group(1) if suite_match else current_suite
        if suite_name and expected_suite_frag.lower() not in suite_name.lower():
            # Wrong suite → discard this block
            return
        # Classify & store
        if summary_fail_re.search(block_text):
            result, _ = "FAILED", "Summary indicates FAILED"
        else:
            result, _ = classify_result(current_test, block_text)
        test_data[current_test] = {"result": result, "logs": block_text}

    for line in lines:
        
        m_suite = suite_line_re.search(line)
        if m_suite:
            current_suite = m_suite.group(1)  

        # Start markers: either "Found test: [..]" or "Running Test : '...'"
        m_found = found_re.search(line)
        m_run   = running_re.search(line)

        start_name = m_found.group(1) if m_found else (m_run.group(1) if m_run else None)
        if start_name:
            # If we were in a previous block, finalize it first
            if current_test is not None:
                finalize_current()
            current_test = start_name
            current_log  = [line]
            continue

        
        if current_test is not None:
            current_log.append(line)
            m_complete = complete_re.search(line)
            if m_complete and m_complete.group(1) == current_test:
                finalize_current()
                current_test = None
                current_log  = []
                current_suite = None
                continue

    if current_test is not None:
        finalize_current()

    if not test_data:
        full_text = "\n".join(lines)
        # Only write if the file contains the expected suite at all
        if re.search(re.escape(expected_suite_frag), full_text, re.IGNORECASE):
            result, _ = classify_result("L3_Run", full_text)
            test_data["L3_Run"] = {"result": result, "logs": full_text}
        else:
            test_data[f"{target}_NoSuiteFound"] = {"result": "FAILED", "logs": "No matching suite found in log."}

    # Write Excel
    rows = [[name, data["result"], data["logs"]] for name, data in test_data.items()]
    df = pd.DataFrame(rows, columns=["Testcase Name", "Result", "Log"])
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Results")
        wb = writer.book
        ws = writer.sheets["Results"]
        wrap = wb.add_format({'text_wrap': True, 'valign': 'top'})
        ws.set_column('A:A', 30)
        ws.set_column('B:B', 12)
        ws.set_column('C:C', 100, wrap)
        ws.set_default_row(18)
   
    print(f" Excel file '{excel_path}' created successfully with full logs.")

#================= MODIFICATION OF START FUNCTION======================================

def ensure_single_command_override(file_path):
    """
    Ensures the command override line is present only once in the start function.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        command_line = "        command = \"cd /VTS_Package/device_settings; ./hal_test_dshal -p Source_HostSettings.yaml\"\n"
        modified_lines = []
        inside_start = False
        command_inserted = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("def start"):
                inside_start = True

            # Skip duplicate command lines
            if inside_start and stripped == command_line.strip():
                continue

            # Insert command line before session.write if not already inserted
            if inside_start and stripped.startswith("self.session.write(command)") and not command_inserted:
                modified_lines.append(command_line)
                command_inserted = True

            modified_lines.append(line)

            if inside_start and stripped.startswith("return result"):
                inside_start = False

        with open(file_path, 'w') as f:
            f.writelines(modified_lines)

        print(f"✅ Ensured single command override in start function of {file_path}.")

    except Exception as e:
        print(f"❌ Failed to update {file_path}: {e}")

def ensure_add_command():
    print("Checking and modifying start function...")
    if os.path.exists(config.UTSUITENAVIGATOR_PATH):
        ensure_single_command_override(config.UTSUITENAVIGATOR_PATH)
    else:
        print(f"Warning: utBaseUtils.py not found at {config.UTBASEUTILS_PATH}")
        
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
    # Always ensure SCP is skipped at startup
    ensure_scp_skipped()
    # ensure_add_command()
    
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
    if target in ALLOWED_DOWNLOAD_MODULES:
            download_streams_for_target(target, config,use_sshpass=bool(getattr(config, "SSH_PASSWORD","")),allow_self_signed_tls=True)
            ensure_preserve_streams_cleanup_override(target, config)
    if target in ('dsVideoPort','dsAudio','rmfaudiocapture'):
            comment_download_calls_in_helper(target=target,base_path=config.BASE_PATH,enabled_targets=None,note_text="Skipping asset downloads on DUT for this run.")

    run_interactive_with_logging()
    generate_excel_from_log(target=target)
    if target in ALLOWED_DOWNLOAD_MODULES:
            # Remove only files (keep directory)
            cleanup_streams_for_target(target=target,config=config,use_sshpass=bool(getattr(config, "SSH_PASSWORD", "")),
                                             remove_dir=False,      # set True if you want to remove /opt/HAL/<target> entirely
                                             dry_run=False,         # set True to preview without deleting
                                             verbose=True)


if __name__ == "__main__":
    main()
