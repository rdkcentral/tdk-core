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
##########################################################################
"""
DAC Utilities Module

Common utility functions for DAC (Distributed Application Catalog) based Package Manager tests.
Provides reusable helpers for:
- Fetching DAC configuration and catalog listings
- JSON-RPC calls to Package Manager plugin
- Application download, install, list, launch, and uninstall operations
"""

import json
import os
import requests
import time
from typing import Optional

# Bootstrap: define globals for harnesses that inject bare literals in Python context
try:
    import builtins as _builtins  # type: ignore
    if not hasattr(_builtins, 'null'):
        _builtins.null = None  # type: ignore
    if not hasattr(_builtins, 'true'):
        _builtins.true = True  # type: ignore
    if not hasattr(_builtins, 'false'):
        _builtins.false = False  # type: ignore
except Exception:
    # Best-effort; do not fail utils import if builtins patching is restricted
    pass
import subprocess
from typing import Any, Dict, List, Optional, Tuple
from requests.exceptions import RequestException
# Avoid importing helpers that may depend on unavailable modules on some harnesses

#############################
# Local AI2.0 config loader #
#############################

# Cached local AI2.0 config
AI2_LOCAL_CFG = None

def _load_local_ai2_config() -> dict:
    global AI2_LOCAL_CFG
    if AI2_LOCAL_CFG is not None:
        return AI2_LOCAL_CFG
    candidates = [
        os.path.join(os.path.dirname(__file__), "ai_2_0_cpe.json"),
        os.path.join(os.path.dirname(__file__), "dac_cpe.json"),
        os.path.join(os.path.dirname(__file__), "catalog_config.json"),
    ]
    for path in candidates:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    AI2_LOCAL_CFG = json.load(f)
                return AI2_LOCAL_CFG
        except Exception:
            continue
    AI2_LOCAL_CFG = {}
    return AI2_LOCAL_CFG

def get_ai2_setting(path: str, default=None):
    """
    Retrieve a config value from local AI2.0 config file using dotted path.
    Example: get_ai2_setting('packageManager.maxDownloads', 5)
    """
    cfg = _load_local_ai2_config()
    node = cfg
    for key in path.split('.'):
        if isinstance(node, dict) and key in node:
            node = node[key]
        else:
            return default
    return node

# Configurable defaults (env > local config > hardcoded)
DEFAULT_DAC_CONFIG_URL = os.environ.get(
    "AI2_DAC_CONFIG_URL",
    str(get_ai2_setting('dac.configUrl', "https://dac.config.dev.fireboltconnect.com/configuration/cpe.json"))
)
DEFAULT_JSONRPC_URL = os.environ.get(
    "AI2_THUNDER_JSONRPC_URL",
    f"http://{get_ai2_setting('thunder.host','127.0.0.1')}:{get_ai2_setting('thunder.port', 9998)}/jsonrpc"
)

# Timeout constants
socket_timeout = int(get_ai2_setting('timeouts.socket', 10))
http_timeout = int(get_ai2_setting('timeouts.http', 30))

"""
# Thunder-based testing - no direct JSON-RPC needed
# Removed older activate helper with retries to avoid confusion; use jsonrpc_activate_plugin
"""

# JSON-RPC id generator
_JSONRPC_COUNTER = int(time.time() * 1000)
def next_jsonrpc_id() -> int:
    global _JSONRPC_COUNTER
    _JSONRPC_COUNTER += 1
    return _JSONRPC_COUNTER


#############################
# Generic JSON-RPC callers  #
#############################

def jsonrpc_call_with_versions(callsign: str, method: str, params: Optional[Dict[str, Any]] = None, jsonrpc_url: str = DEFAULT_JSONRPC_URL, timeout: int = http_timeout, versions: tuple = (None, '1')) -> Tuple[bool, Any]:
    """
    Perform a JSON-RPC call trying unversioned and versioned method names.

    Example tries: org.rdk.PackageManager.method then org.rdk.PackageManager.1.method

    Returns (True, response_dict) on success or (False, last_error_string) on failure.
    """
    last_err = None
    for ver in versions:
        full_method = f"{callsign}.{method}" if ver is None else f"{callsign}.{ver}.{method}"
        payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": next_jsonrpc_id(), "method": full_method}
        if params is not None:
            payload["params"] = params
        try:
            resp = requests.post(jsonrpc_url, json=payload, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            return True, data
        except Exception as e:
            last_err = str(e)
            continue
    return False, last_err


def jsonrpc_call_device(ip: str, port: Optional[int], callsign: str, method: str, params: Optional[Dict[str, Any]] = None, timeout: int = http_timeout, versions: tuple = (None, '1')) -> Tuple[bool, Any]:
    """
    Convenience wrapper that builds jsonrpc_url from device ip/port and calls jsonrpc_call_with_versions.
    """
    jsonrpc_url = _build_jsonrpc_url_from_ip_port(ip, port)
    return jsonrpc_call_with_versions(callsign, method, params=params, jsonrpc_url=jsonrpc_url, timeout=timeout, versions=versions)


def thunder_get_plugin_status(callsign: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL, timeout: int = 10) -> Optional[Dict[str, Any]]:
    """
    Get Thunder plugin status using Controller.1.status@<callsign>.

    Args:
        callsign: Full plugin callsign (e.g., 'org.rdk.PackageManagerRDKEMS')
        jsonrpc_url: Thunder JSON-RPC endpoint

    Returns:
        Status dict for the plugin if available, else None
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": f"Controller.1.status@{callsign}"
    }
    try:
        resp = requests.post(jsonrpc_url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        result = data.get("result")
        if isinstance(result, list) and result:
            return result[0]
        return None
    except RequestException as e:
        print(f"[WARN] thunder_get_plugin_status({callsign}) request failed: {e}")
        return None
    except ValueError as e:
        print(f"[WARN] thunder_get_plugin_status({callsign}) returned invalid JSON: {e}")
        return None


def thunder_is_plugin_active(callsign: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL, timeout: int = 10) -> bool:
    """
    Check if a Thunder plugin is active using Controller.1.status@<callsign>.

    Returns True if status.state == 'activated'. No retries.
    """
    status = thunder_get_plugin_status(callsign, jsonrpc_url, timeout)
    return bool(status and status.get('state') == 'activated')


# --- Direct JSON-RPC helpers aligned to provided curl commands ---
def jsonrpc_activate_plugin(callsign: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL, timeout: int = http_timeout) -> bool:
    """
    Activate plugin via JSON-RPC: Controller.1.activate with {callsign}.
    Mirrors: curl -X POST ... '{"method":"Controller.1.activate","params":{"callsign":"..."}}'
    """
    payload = {
        "jsonrpc": "2.0",
        "id": next_jsonrpc_id(),
        "method": "Controller.1.activate",
        "params": {"callsign": callsign}
    }
    try:
        resp = requests.post(jsonrpc_url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # Accept presence of 'result' as success
        return 'result' in data
    except Exception as e:
        print(f"[ERROR] jsonrpc_activate_plugin({callsign}) failed: {e}")
        return False


def jsonrpc_install_package(package_id: str, version: str, file_locator: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL, timeout: int = http_timeout) -> bool:
    """
    Install via JSON-RPC per curl:
    method: org.rdk.PackageManagerRDKEMS.install
    params: {packageId, version, fileLocator}
    """
    params = {
        "packageId": package_id,
        "version": version,
        "fileLocator": file_locator
    }
    ok, data = jsonrpc_call_with_versions("org.rdk.PackageManagerRDKEMS", "install", params=params, jsonrpc_url=jsonrpc_url, timeout=timeout)
    if ok and isinstance(data, dict):
        if 'result' in data:
            return True
        return bool(data.get('success') is True)
    return False



def jsonrpc_download_package(bundle_url: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL, timeout: int = http_timeout) -> Optional[str]:
    """
    Download via JSON-RPC per curl:
    method: org.rdk.PackageManagerRDKEMS.download
    params: {url}

    Returns downloadId on success, None otherwise.
    """
    params = {"url": bundle_url}
    ok, data = jsonrpc_call_with_versions("org.rdk.PackageManagerRDKEMS", "download", params=params, jsonrpc_url=jsonrpc_url, timeout=timeout)
    if ok and isinstance(data, dict):
        result = data.get('result') or {}
        if isinstance(result, dict):
            return result.get('downloadId')
    return None


def jsonrpc_close_app(app_id: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL, timeout: int = http_timeout) -> bool:
    """
    Close app via JSON-RPC per curl:
    method: org.rdk.AppManager.1.closeApp, params: {appId}
    """
    payload = {
        "jsonrpc": "2.0",
        "id": next_jsonrpc_id(),
        "method": "org.rdk.AppManager.1.closeApp",
        "params": {"appId": app_id}
    }
    try:
        resp = requests.post(jsonrpc_url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get('result') is not None or data.get('success') is True:
            return True
        return False
    except Exception as e:
        print(f"[ERROR] jsonrpc_close_app({app_id}) failed: {e}")
        return False


def jsonrpc_terminate_app(app_id: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL, timeout: int = http_timeout) -> bool:
    """
    Terminate app via JSON-RPC per curl:
    method: org.rdk.AppManager.1.terminateApp, params: {appId}
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1013,
        "method": "org.rdk.AppManager.1.terminateApp",
        "params": {"appId": app_id}
    }
    try:
        resp = requests.post(jsonrpc_url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get('result') is not None or data.get('success') is True:
            return True
        return False
    except Exception as e:
        print(f"[ERROR] jsonrpc_terminate_app({app_id}) failed: {e}")
        return False


def jsonrpc_kill_app(app_id: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL, timeout: int = http_timeout) -> bool:
    """
    Kill app via JSON-RPC per curl:
    method: org.rdk.AppManager.1.killApp, params: {appId}
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1013,
        "method": "org.rdk.AppManager.1.killApp",
        "params": {"appId": app_id}
    }
    try:
        resp = requests.post(jsonrpc_url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get('result') is not None or data.get('success') is True:
            return True
        return False
    except Exception as e:
        print(f"[ERROR] jsonrpc_kill_app({app_id}) failed: {e}")
        return False


def _build_jsonrpc_url_from_ip_port(ip: str, port: Optional[int]) -> str:
    """
    Build a JSON-RPC URL using device IP and port. If port is None, use config.
    """
    cfg_port = get_ai2_setting('packageManager.jsonRpcPort', get_ai2_setting('thunder.port', 9998))
    use_port = port if port else cfg_port
    return f"http://{ip}:{use_port}/jsonrpc"


def create_tdk_test_step(tdk_obj, step_name: str, step_description: str = "") -> Any:
    """
    Create a TDK test step for tracking individual operations.
    
    Args:
        tdk_obj: TDK scripting library object
        step_name: Name of the test step (e.g., 'Download_Package', 'Install_App')
        step_description: Optional description for the step
        
    Returns:
        TDK test step object
    """
    # Create a generic RdkService_Test step without extra parameters.
    # Some primitives reject unknown parameters like 'step_name' or 'description'.
    tdkTestObj = tdk_obj.createTestStep('RdkService_Test')
    return tdkTestObj


def set_test_step_status(tdkTestObj, status: str, details: str = ""):
    """
    Set TDK test step status with optional details.
    
    Args:
        tdkTestObj: TDK test step object
        status: "SUCCESS" or "FAILURE"
        details: Optional details message
    """
    if details:
        print(f"  [TDK STEP] {status}: {details}")
    
    # Set the basic properties that TDK framework expects
    try:
        # For test steps created with create_tdk_test_step, we need to manually
        # set the result field to avoid the "result not found" error
        if not hasattr(tdkTestObj, 'result') or not tdkTestObj.result:
            # Create a minimal valid result structure that TDK expects
            tdkTestObj.result = f'{{"TDK__#@$00_result":"{status}","TDK__#@$00_details":"{details}"}}'
            tdkTestObj.resultStr = status
        tdkTestObj.setResultStatus(status)
    except Exception as e:
        print(f"Warning: Could not set TDK test step status: {e}")


def thunder_call(tdk_obj, callsign_short: str, request_type: str, params: Optional[Dict[str, Any]] = None, expectedresult: str = "SUCCESS") -> Tuple[bool, Any]:
    """
    Generic Thunder call via TDK primitives with automatic primitive selection.

    Uses appropriate TDK primitive based on the method call:
    - rdkservice_getValue for method calls with no parameters (like listPackages)
    - rdkservice_setValue for method calls with parameters

    Args:
        tdk_obj: TDK scripting library object
        callsign_short: Plugin short name (e.g., 'PackageManager' or 'PackageManagerRDKEMS')
        request_type: Method name (e.g., 'listPackages', 'download', 'install')
        params: Dict to be JSON-encoded for the params argument
        expectedresult: TDK expected result string

    Returns:
        (ok, response) where response is a dict on success or raw details/string on failure
    """
    import json as _json
    
    # Build the full method name
    full_callsign = callsign_short if '.' in callsign_short else f"org.rdk.{callsign_short}"
    full_method = f"{full_callsign}.1.{request_type}"
    
    try:
        # Choose primitive based on whether we have parameters
        if params is None or len(params) == 0:
            # Use rdkservice_getValue for calls without parameters
            t = tdk_obj.createTestStep('rdkservice_getValue')
            t.addParameter("method", full_method)
        else:
            # Use rdkservice_setValue for calls with parameters
            t = tdk_obj.createTestStep('rdkservice_setValue')
            t.addParameter("method", full_method)
            t.addParameter("value", _json.dumps(params))
        
        t.executeTestCase(expectedresult)
        res = (t.getResult() or '').upper()
        det = t.getResultDetails() or ''
        
        if "SUCCESS" in res:
            try:
                data = _json.loads(det)
                return True, data
            except Exception:
                # If details aren't JSON, return as raw data
                return True, {"raw": det, "details": det}
        return False, det
        
    except Exception as e:
        return False, str(e)


# ---- TDK wrappers for service/process checks (thin wrappers around ExecuteCmd) ----
def verify_process_exists_tdk(tdk_obj, process_name: str):
    """
    Check if a process exists on the device using TDK ExecuteCmd (pidof).
    Returns: (tdkTestObj, actualresult, pid)
    """
    command = f"pidof {process_name}"
    print(f"Command : {command}")
    tdkTestObj = tdk_obj.createTestStep('ExecuteCmd')
    try:
        # Use ExecuteCmd primitive directly to avoid extra dependencies
        tdkTestObj.addParameter('command', command)
        expectedresult = 'SUCCESS'
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult() or ''
        details = tdkTestObj.getResultDetails() or ''
    except Exception as e:
        print(f"[ERROR] ExecuteCmd failed: {e}")
        actualresult = 'FAILURE'
        details = ''

    pid = details.strip()
    print(f"Process PID: {pid}")
    if (actualresult and 'SUCCESS' in actualresult.upper()) and pid and pid.isdigit():
        actualresult = 'SUCCESS'
    else:
        actualresult = 'FAILURE'
        pid = ''
    return tdkTestObj, actualresult, pid

# ---- End wrappers ----


def fetch_dac_config(config_url: str = DEFAULT_DAC_CONFIG_URL, timeout: int = 30) -> Tuple[str, str, str]:
    """
    Fetch DAC catalog configuration.
    
    Returns:
        Tuple of (catalog_url, username, password)
    """
    # Allow override of catalog URL directly via env if present
    env_catalog_url = os.environ.get("AI2_DAC_CATALOG_URL")
    env_catalog_user = os.environ.get("AI2_DAC_USER")
    env_catalog_pass = os.environ.get("AI2_DAC_PASSWORD")
    if env_catalog_url and env_catalog_user and env_catalog_pass:
        return env_catalog_url, env_catalog_user, env_catalog_pass

    # Attempt remote fetch first
    try:
        resp = requests.get(config_url, timeout=timeout)
        resp.raise_for_status()
        cfg = resp.json()
        

        catalog = cfg['appstore-catalog']
        url_val = catalog['url']
        user_val = catalog['authentication']['user']
        password_val = catalog['authentication']['password']

        return url_val, user_val, password_val
    except Exception as e:
        # Fallback to local config file if available (prefer ai_2_0_cpe.json)
        cfg = _load_local_ai2_config()
        catalog = cfg.get('appstore-catalog', {}) if isinstance(cfg, dict) else {}
        url_val = catalog.get('url')
        auth = catalog.get('authentication', {})
        user_val = auth.get('user')
        password_val = auth.get('password')
        if url_val and user_val and password_val:
            print("[INFO] Using offline DAC config from local AI2.0 config")
            return url_val, user_val, password_val
        raise Exception(f"Failed to fetch DAC config: {str(e)}. Set env AI2_DAC_CATALOG_URL/AI2_DAC_USER/AI2_DAC_PASSWORD or provide local ai_2_0_cpe.json.")


# --------------------------
# Simple Package Manager helpers
# --------------------------

def get_jsonrpc_url_for_device(ip: str) -> str:
    """Construct JSON-RPC URL from device IP and configured port."""
    port = get_ai2_setting('packageManager.jsonRpcPort', 9998)
    return f"http://{ip}:{port}/jsonrpc"


def pm_download(tdk_obj, ip: str, download_url: str, app_name: str = "") -> Optional[str]:
    """
    Simplified download orchestration honoring preferJsonRpc with automatic fallback.

    Returns a download ID (string) on success, or None.
    """
    prefer_jsonrpc = bool(get_ai2_setting('packageManager.preferJsonRpc', True))
    jsonrpc_url = get_jsonrpc_url_for_device(ip)

    try:
        if prefer_jsonrpc:
            dlid = jsonrpc_download_package(download_url, jsonrpc_url=jsonrpc_url)
            if dlid:
                return dlid
            # fallback
            return thunder_download_package(tdk_obj, download_url, app_name)
        else:
            dlid = thunder_download_package(tdk_obj, download_url, app_name)
            if dlid:
                return dlid
            # fallback
            return jsonrpc_download_package(download_url, jsonrpc_url=jsonrpc_url)
    except Exception:
        # Last chance: try opposite path once
        try:
            if prefer_jsonrpc:
                return thunder_download_package(tdk_obj, download_url, app_name)
            else:
                return jsonrpc_download_package(download_url, jsonrpc_url=jsonrpc_url)
        except Exception:
            return None


def pm_install(tdk_obj, ip: str, app_id: str, app_version: str, download_id: str, additional_metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    Simplified install orchestration honoring preferJsonRpc with automatic fallback.

    Returns True on success, else False.
    """
    prefer_jsonrpc = bool(get_ai2_setting('packageManager.preferJsonRpc', True))
    jsonrpc_url = get_jsonrpc_url_for_device(ip)
    file_locator = f"/opt/CDL/package{download_id}"

    try:
        if prefer_jsonrpc:
            ok = jsonrpc_install_package(app_id, app_version, file_locator, jsonrpc_url=jsonrpc_url)
            if ok:
                return True
            # fallback to Thunder
            return bool(thunder_install_package(tdk_obj, app_id, app_version, download_id, additional_metadata, app_id))
        else:
            ok = bool(thunder_install_package(tdk_obj, app_id, app_version, download_id, additional_metadata, app_id))
            if ok:
                return True
            # fallback to JSON-RPC
            return jsonrpc_install_package(app_id, app_version, file_locator, jsonrpc_url=jsonrpc_url)
    except Exception:
        # Last chance: try opposite path once
        try:
            if prefer_jsonrpc:
                return bool(thunder_install_package(tdk_obj, app_id, app_version, download_id, additional_metadata, app_id))
            else:
                return jsonrpc_install_package(app_id, app_version, file_locator, jsonrpc_url=jsonrpc_url)
        except Exception:
            return False


def list_dac_packages(catalog_url: str, username: str, password: str, 
                      platform_name: str, firmware_ver: str, timeout: int = 30) -> List[Dict[str, Any]]:
    """
    List packages from DAC catalog for given platform and firmware version.
    
    Args:
        catalog_url: Base DAC catalog URL
        username: Authentication username
        password: Authentication password
        platform_name: Platform name (e.g., 'rpi4')
        firmware_ver: Firmware version
    
    Returns:
        List of application dictionaries with id, name, version, etc.
    """
    try:
        url = f"{catalog_url}/apps"
        params = {
            'platformName': platform_name,
            'firmwareVer': firmware_ver
        }
        
        resp = requests.get(url, auth=(username, password), params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        # Handle different response structures
        if isinstance(data, dict):
            if 'applications' in data:
                return data['applications']
            elif 'apps' in data:
                return data['apps']
        elif isinstance(data, list):
            return data
        
        return []
    except Exception as e:
        raise Exception(f"Failed to list DAC packages: {str(e)}")


def get_app_details(catalog_url: str, username: str, password: str,
                    package_id: str, platform_name: str, firmware_ver: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Get detailed information for a specific application.
    
    Returns:
        Dictionary with application details
    """
    try:
        url = f"{catalog_url}/apps/{package_id}"
        params = {
            'platformName': platform_name,
            'firmwareVer': firmware_ver
        }
        
        resp = requests.get(url, auth=(username, password), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise Exception(f"Failed to get app details: {str(e)}")


def build_download_url(catalog_url: str, package_id: str, version: str, 
                       platform_name: str, firmware_ver: str) -> str:
    """
    Build the download URL for a package bundle.
    
    Args:
        catalog_url: Base DAC catalog URL
        package_id: Application package ID
        version: Application version
        platform_name: Platform name
        firmware_ver: Firmware version
    
    Returns:
        Complete download URL for the package bundle
    """
    return f"{catalog_url}/bundles/{package_id}/{version}/{platform_name}/{firmware_ver}"


# JSON-RPC function removed - Thunder interface doesn't require direct JSON-RPC calls
# Use Thunder RdkService_Test primitive instead


def build_additional_metadata(app_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Build additional metadata list from application data.
    
    Args:
        app_data: Application dictionary from DAC catalog
    
    Returns:
        List of metadata dictionaries suitable for install call
    """
    metadata = []
    
    if 'name' in app_data:
        metadata.append({'name': 'appName', 'value': app_data['name']})
    
    if 'category' in app_data:
        metadata.append({'name': 'category', 'value': app_data['category']})
    
    if 'type' in app_data:
        metadata.append({'name': 'type', 'value': app_data['type']})
    
    return metadata



def get_device_info_from_json(json_path: str = None) -> Tuple[str, str]:
    """
    Get device firmware version and platform.

    Primary source: `/version.txt` on device.
    - Platform inferred from `imagename:` line (e.g., contains `RPI4`).
    - Firmware version from `VERSION=` line.

    Additionally, confirm whether PackageManagerRDKEMS.json exists in standard paths.

    Returns: (firmware_version, platform_name)
    """
    import os

    # 1) Try reading /version.txt
    firmware_ver = None
    platform_name = None
    # Version file path is configurable via local config
    version_file = str(get_ai2_setting('device.versionFilePath', "/version.txt"))
    if os.path.exists(version_file):
        try:
            with open(version_file, "r", encoding="utf-8", errors="ignore") as vf:
                for line in vf:
                    ls = line.strip()
                    if ls.startswith("imagename:"):
                        # imagename:lib32-application-test-image-RPI4-20251126122407
                        payload = ls.split(":", 1)[1]
                        parts = payload.split("-")
                        known = ["RPI4", "rpi4", "rtd1325", "rtd1319", "brcm974116sff", "mesonsc2"] #need to modify for 1319 and amlogic platforms
                        for token in parts:
                            if token in known:
                                platform_name = token.upper()
                                break
                        # Fallback: last alpha token
                        if not platform_name:
                            for token in reversed(parts):
                                if any(c.isalpha() for c in token):
                                    platform_name = token.upper()
                                    break
                    elif ls.startswith("VERSION="):
                        firmware_ver = ls.split("=", 1)[1].strip()
                    if firmware_ver and platform_name:
                        break
        except Exception:
            pass

    # 2) Confirm presence of PackageManagerRDKEMS.json (informational; do not fail test)
    possible_paths = [
        "/etc/WPEFramework/plugins/PackageManagerRDKEMS.json",
     
    ]
    found_plugin_cfg = None
    for path in ([json_path] if json_path else []) + possible_paths:
        if path and os.path.exists(path):
            found_plugin_cfg = path
            break
    if found_plugin_cfg:
        print(f"[INFO] PackageManagerRDKEMS config present at: {found_plugin_cfg}")
    else:
        print(f"[WARN] PackageManagerRDKEMS.json not found in: {possible_paths}")

    # Fallback to JSON content if available
    json_src = found_plugin_cfg or json_path
    if json_src and os.path.exists(json_src):
        try:
            with open(json_src, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
            fw = str(data.get("FirmwareCompatibilityKey", "") or "")
            plat = str(data.get("dacBundlePlatformNameOverride", "") or "")
            if fw and plat:
                return fw, plat
        except Exception:
            pass

    # Final fallback: return defaults to avoid hard failure
    # Default to RPi4 values if nothing could be parsed
    return (
        get_ai2_setting("firmware.defaultVersion", "1.0.0-b34e9a38a2675d4cd02cf89f7fc72874a4c99eb0-dbg"),
        get_ai2_setting("platform.defaultName", "rpi4")

    )


# NOTE: Legacy JSON-RPC precondition helper removed to avoid ambiguity.


def safe_unload_module(obj, module_name: str) -> None:
    """
    Safely unload a TDK module with error handling.
    
    Args:
        obj: TDK library object
        module_name: Module name to unload
    """
    try:
        print(f"Unloading Module : {module_name}")
        obj.unloadModule(module_name)
        print("Unload Module Status : Success")
    except AttributeError as e:
        if "'NoneType' object has no attribute 'close'" in str(e):
            print("Unload Module Status : Success (connection already closed)")
        else:
            print(f"Unload Module Status : Error - {str(e)}")
    except Exception as e:
        print(f"Unload Module Status : Error - {str(e)}")


def test_tdk_agent_connectivity(ip: str, port: int = 8087) -> bool:
    """
    Test connectivity to TDK Agent without requiring execution IDs.
    
    Args:
        ip: Device IP address
        port: TDK Agent port
        
    Returns:
        True if TDK Agent is accessible, False otherwise
    """
    import socket
    import requests
    
    print(f"Testing TDK Agent connectivity at {ip}:{port}...")
    
    # Test 1: Socket connectivity
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(socket_timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            print(f"[PASS] Socket connection successful to {ip}:{port}")
        else:
            print(f"[FAIL] Socket connection failed to {ip}:{port}")
            return False
    except Exception as e:
        print(f"[FAIL] Socket test failed: {str(e)}")
        return False
    
    # Test 2: HTTP connectivity (basic TDK Agent endpoint)
    try:
        base_url = f"http://{ip}:{port}"
        response = requests.get(f"{base_url}/", timeout=http_timeout)
        print(f"[PASS] HTTP connection successful - Status: {response.status_code}")
        print(f"[INFO] TDK Agent URL: {base_url}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] HTTP connection failed - TDK Agent not responding at {base_url}")
        return False
    except requests.exceptions.Timeout:
        print(f"[FAIL] HTTP connection timeout - TDK Agent slow/unresponsive at {base_url}")
        return False
    except Exception as e:
        print(f"[FAIL] HTTP test failed: {str(e)}")
        return False

def check_thunder_plugin_status(tdk_obj, plugin_name: str) -> bool:
    """
    Check Thunder plugin status using TDK RdkService_Test.
    
    Args:
        tdk_obj: TDK scripting library object
        plugin_name: Plugin name (e.g., 'PackageManagerRDKEMS')
        
    Returns:
        True if plugin is available and active, False otherwise
    """
    try:
        tdkTestObj = tdk_obj.createTestStep('RdkService_Test')
        tdkTestObj.addParameter("xml_name", plugin_name)
        tdkTestObj.addParameter("request_type", "status")
        tdkTestObj.executeTestCase("SUCCESS")
        result = tdkTestObj.getResult()
        
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS")
            return True
        else:
            tdkTestObj.setResultStatus("FAILURE")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to check plugin status for {plugin_name}: {str(e)}")
        return False


def ensure_plugin_active(tdk_obj, callsign: str, jsonrpc_url: Optional[str] = None, wait_seconds: float = 1.0) -> bool:
    """
    Ensure a Thunder plugin is active. Tries Thunder Controller activation first,
    then falls back to JSON-RPC Controller.1.activate if provided.

    Args:
        tdk_obj: TDK scripting library object
        callsign: Full or short callsign (e.g., 'org.rdk.PackageManagerRDKEMS' or 'PackageManagerRDKEMS')
        jsonrpc_url: Optional JSON-RPC endpoint for fallback activation
        wait_seconds: Delay before re-checking status after activation

    Returns:
        True if plugin is active at end, else False
    """
    # Build short/full variants
    short = callsign.split('.')[-1]
    full = callsign if '.' in callsign else f"org.rdk.{callsign}"

    # Quick status check via JSON-RPC Controller status
    try:
        if thunder_is_plugin_active(full, jsonrpc_url=jsonrpc_url):
            return True
    except Exception:
        pass

    # Try Thunder Controller activate with full then short
    try:
        ok, _ = thunder_call(tdk_obj, "Controller", "activate", {"callsign": full})
        if not ok:
            ok, _ = thunder_call(tdk_obj, "Controller", "activate", {"callsign": short})
    except Exception:
        ok = False

    # Fallback to JSON-RPC activate if provided
    if not ok and jsonrpc_url:
        try:
            ok = jsonrpc_activate_plugin(full, jsonrpc_url=jsonrpc_url) or \
                 jsonrpc_activate_plugin(short, jsonrpc_url=jsonrpc_url)
        except Exception:
            ok = False

    # Re-check status
    try:
        time.sleep(wait_seconds)
    except Exception:
        pass
    try:
        return thunder_is_plugin_active(full, jsonrpc_url=jsonrpc_url)
    except Exception:
        return False


def check_and_activate_ai2_managers(tdk_obj=None, jsonrpc_url: str = None, required_only: bool = True) -> Tuple[bool, List[str]]:
    """
    Check AI2.0 Manager plugins (Thunder-only).

    Args:
        tdk_obj: TDK scripting library object (required)
        jsonrpc_url: Deprecated. Ignored.
        required_only: If True, only check core plugins

    Returns:
        Tuple of (all_available_activated: bool, failed_plugins: List[str])
    """
    if tdk_obj is not None:
        return check_and_activate_ai2_managers_thunder(tdk_obj, required_only)
    # Legacy JSON-RPC path removed to avoid ambiguity; guide callers to Thunder path
    print("[WARN] check_and_activate_ai2_managers: JSON-RPC path deprecated; provide tdk_obj for Thunder mode")
    return False, ["JSON-RPC path deprecated"]


def check_and_activate_ai2_managers_thunder(tdk_obj, required_only: bool = True) -> Tuple[bool, List[str]]:
    """
    Check AI2.0 Manager plugins using Thunder interface via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        required_only: If True, only check core plugins
        
    Returns:
        Tuple of (all_available_activated: bool, failed_plugins: List[str])
    """
    # Core plugins that are essential for AI2.0
    core_plugins = [
        "PackageManagerRDKEMS", 
        "AppManager"
    ]
    
    # Extended list for full AI2.0 stack
    all_plugins = [
        "StorageManager",
        "PackageManagerRDKEMS",
        "DownloadManager", 
        "RDKWindowManager",
        "RuntimeManager",
        "LifecycleManager",
        "AppManager",
        "PreinstallManager"
    ]
    
    plugins_to_check = core_plugins if required_only else all_plugins
    
    available_plugins = []
    failed_plugins = []
    
    print("\n" + "="*80)
    print("PRECONDITION: Checking AI2.0 Manager Plugins via Thunder")
    print("="*80)
    
    # Check which plugins are available via Thunder
    print(f"\n🔍 Discovering available plugins...")
    for plugin in plugins_to_check:
        print(f"  Checking {plugin}...")
        
        if check_thunder_plugin_status(tdk_obj, plugin):
            available_plugins.append(plugin)
            print(f"  ✓ {plugin} - Available and active")
        else:
            failed_plugins.append(plugin)
            print(f"  ✗ {plugin} - Not available or inactive")
    
    # Summary
    print("\n" + "="*80)
    
    print("📋 Plugin Status Summary:")
    print(f"  Available: {len(available_plugins)}")
    print(f"  Missing: {len(failed_plugins)}")
    
    if failed_plugins:
        print(f"\n⚠ Missing/Inactive plugins:")
        for plugin in failed_plugins:
            print(f"    - {plugin}")
    
    if available_plugins:
        print("✅ Available plugins:")
        for plugin in available_plugins:
            print(f"    - {plugin}")
        print("="*80)
        return True, []
    else:
        print("❌ No AI2.0 plugins available")
        print("="*80)
        return False, failed_plugins


def thunder_download_package(tdk_obj, download_url: str, app_name: str = "") -> Optional[str]:
    """
    Download a package using Thunder PackageManagerRDKEMS via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        download_url: URL to download package from
        app_name: Application name for logging
        
    Returns:
        Download ID if successful, None if failed
    """
    import json
    
    try:
        ok, resp = thunder_call(tdk_obj, "PackageManagerRDKEMS", "download", {"url": download_url})
        if ok and isinstance(resp, dict):
            rid = None
            result = resp.get('result') if isinstance(resp.get('result'), dict) else resp.get('result')
            if isinstance(result, dict):
                rid = result.get('downloadId') or result.get('id')
            if not rid:
                # Some implementations may return top-level downloadId
                rid = resp.get('downloadId') or resp.get('id')
            if rid:
                print(f"    ✓ Download successful - ID: {rid}")
                return str(rid)
        print(f"    ✗ Download failed - No download ID returned")
        return None
    except Exception as e:
        print(f"    ✗ Download error: {str(e)}")
        return None


def thunder_install_package(tdk_obj, app_id: str, version: str, download_id: str, 
                           additional_metadata: Dict[str, Any] = None, app_name: str = "") -> bool:
    """
    Install a downloaded package using Thunder PackageManagerRDKEMS via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        app_id: Application ID
        version: Application version
        download_id: Download ID from download operation
        additional_metadata: Additional metadata for installation
        app_name: Application name for logging
        
    Returns:
        True if successful, False if failed
    """
    import json
    
    try:
        install_params = {
            "appId": app_id,
            "version": version,
            "downloadId": download_id
        }
        
        if additional_metadata:
            install_params["additionalMetadata"] = additional_metadata
        
        ok, resp = thunder_call(tdk_obj, "PackageManagerRDKEMS", "install", install_params)
        if ok and isinstance(resp, dict):
            if resp.get('success') is True:
                print(f"    ✓ Install successful for {app_name or app_id}")
                return True
            # Some implementations return a non-empty 'result' to indicate success
            if resp.get('result') is not None:
                print(f"    ✓ Install completed for {app_name or app_id}")
                return True
            error_msg = resp.get('error', 'Unknown install error')
            print(f"    ✗ Install failed for {app_name or app_id}: {error_msg}")
            return False
        print(f"    ✗ Install failed for {app_name or app_id} - Thunder execution failed")
        return False
            
    except Exception as e:
        print(f"    ✗ Install error for {app_name or app_id}: {str(e)}")
        return False


def thunder_uninstall_package(tdk_obj, app_id: str, app_name: str = "") -> bool:
    """
    Uninstall a package using Thunder PackageManagerRDKEMS via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        app_id: Application ID to uninstall
        app_name: Application name for logging
        
    Returns:
        True if successful, False if failed
    """
    import json
    
    try:
        ok, resp = thunder_call(tdk_obj, "PackageManagerRDKEMS", "uninstall", {"appId": app_id})
        if ok and isinstance(resp, dict):
            if resp.get('success') is True or resp.get('result') is not None:
                print(f"    ✓ Uninstall successful for {app_name or app_id}")
                return True
            error_msg = resp.get('error', 'Unknown uninstall error')
            print(f"    ✗ Uninstall failed for {app_name or app_id}: {error_msg}")
            return False
        print(f"    ✗ Uninstall failed for {app_name or app_id} - Thunder execution failed")
        return False
            
    except Exception as e:
        print(f"    ✗ Uninstall error for {app_name or app_id}: {str(e)}")
        return False


# Removed deprecated legacy helpers to avoid confusion; use explicit JSON-RPC helpers or Thunder ones


def thunder_list_installed_packages(tdk_obj) -> List[Dict[str, Any]]:
    """
    List installed packages using Thunder PackageManagerRDKEMS via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        
    Returns:
        List of installed packages
    """
    import json
    
    try:
        ok, resp = thunder_call(tdk_obj, "PackageManagerRDKEMS", "listPackages", {})
        if ok and isinstance(resp, dict):
            result = resp.get('result') or {}
            packages = []
            if isinstance(result, dict):
                packages = result.get('packages') or result.get('Packages') or []
            if isinstance(packages, dict):
                packages = packages.get('packages') or []
            packages = packages if isinstance(packages, list) else []
            print(f"    ✓ Found {len(packages)} installed packages")
            return packages
        print(f"    ✗ Failed to list packages - Thunder execution failed")
        return []
    except Exception as e:
        print(f"    ✗ List packages error: {str(e)}")
        return []


def thunder_launch_app(tdk_obj, app_id: str, app_name: str = "") -> bool:
    """
    Launch an application using Thunder AppManager via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        app_id: Application ID to launch
        app_name: Application name for logging
        
    Returns:
        True if successful, False if failed
    """
    import json
    # If tdk_obj provided, prefer TDK primitive which will translate to Thunder JSON-RPC
    if tdk_obj is not None:
        try:
            ok, resp = thunder_call(tdk_obj, "AppManager", "launchApp", {"appId": app_id})
            if ok and isinstance(resp, dict):
                if resp.get('success') is True:
                    print(f"    ✓ Launch successful for {app_name or app_id}")
                    return True
                if resp.get('result') is not None:
                    print(f"    ✓ Launch completed for {app_name or app_id}")
                    return True
                error_msg = resp.get('error', 'Unknown launch error')
                print(f"    ✗ Launch failed for {app_name or app_id}: {error_msg}")
                return False
            print(f"    ✗ Launch failed for {app_name or app_id} - Thunder execution failed")
            return False
        except Exception as e:
            print(f"    ✗ Launch error for {app_name or app_id}: {str(e)}")
            return False

    # If no tdk_obj provided, attempt a direct JSON-RPC call to the AppManager
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1013,
            "method": "org.rdk.AppManager.1.launchApp",
            "params": {"appId": app_id}
        }
        resp = requests.post(DEFAULT_JSONRPC_URL, json=payload, timeout=http_timeout)
        resp.raise_for_status()
        data = resp.json()

        # JSON-RPC success if 'result' present and non-empty
        if data.get('result') is not None:
            print(f"    ✓ Launch successful for {app_name or app_id} (JSON-RPC)")
            return True
        # Some implementations may return an explicit success boolean
        if data.get('success') is True:
            print(f"    ✓ Launch successful for {app_name or app_id} (JSON-RPC success flag)")
            return True

        print(f"    ✗ Launch failed for {app_name or app_id} - Response: {data}")
        return False
    except Exception as e:
        print(f"    ✗ Launch JSON-RPC error for {app_name or app_id}: {str(e)}")
        return False


def thunder_verify_package_installed(tdk_obj, app_id: str, app_name: str = "") -> bool:
    """
    Verify if a package is installed using Thunder PackageManagerRDKEMS via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        app_id: Application ID to verify
        app_name: Application name for logging
        
    Returns:
        True if installed, False if not installed
    """
    packages = thunder_list_installed_packages(tdk_obj)
    
    for package in packages:
        if package.get('packageId') == app_id:
            install_state = package.get('installState', 'unknown')
            print(f"    ✓ Package {app_name or app_id} is installed (state: {install_state})")
            return True
    
    print(f"    ✗ Package {app_name or app_id} is not installed")
    return False
