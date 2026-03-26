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
AI 2.0 Manager Test Utilities

Shared utility module for all AI 2.0 service managers (AppManager, StorageManager, 
PackageManager, DownloadManager, etc.) to read configuration values from 
the Video_Accelerator.config file.

Usage:
    from aiutils import get_config_value
    
    port = get_config_value('APPMANAGER_JSONRPC_PORT', 9998)
    app_id = get_config_value('APPMANAGER_TEST_APP_ID', 'com.rdk.app.cobalt25_rpi4')
"""

import os


def get_config_value(key, default=None):
    """
    Read configuration value from Video_Accelerator.config
    
    This function reads configuration key-value pairs from the Video_Accelerator.config
    file, which is shared across all AI 2.0 service manager tests.
    
    Args:
        key (str): Configuration key to look up (e.g., 'APPMANAGER_JSONRPC_PORT')
        default: Default value to return if key is not found (default: None)
    
    Returns:
        str or default: Configuration value as string, or default if not found
    
    Supported configuration keys (examples):
        - APPMANAGER_JSONRPC_PORT: JSON-RPC port for AppManager (default: 9998)
        - APPMANAGER_SERVICE_NAME: SystemD service name for AppManager
        - APPMANAGER_TEST_APP_ID: Test application ID for AppManager tests
        - APPMANAGER_TEST_SYSTEM_APP_ID: Test system app ID for system app tests
        - STORAGEMANAGER_JSONRPC_PORT: JSON-RPC port for StorageManager (future)
        - PACKAGEMANAGER_JSONRPC_PORT: JSON-RPC port for PackageManager (future)
        - DOWNLOADMANAGER_JSONRPC_PORT: JSON-RPC port for DownloadManager (future)
    
    Example:
        >>> port = get_config_value('APPMANAGER_JSONRPC_PORT', 9998)
        >>> app_id = get_config_value('APPMANAGER_TEST_APP_ID', 'com.rdk.app.default')
    """
    # Config file path: framework/fileStore/tdkvRDKServiceConfig/Video_Accelerator.config
    config_file = os.path.join(os.path.dirname(__file__), 'tdkvRDKServiceConfig', 'Video_Accelerator.config')
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                for line in f:
                    # Strip whitespace
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key=value pairs
                    if '=' in line:
                        cfg_key, cfg_value = line.split('=', 1)
                        if cfg_key.strip() == key:
                            return cfg_value.strip()
    except Exception as e:
        print(f"[DEBUG] Config read failed for {key}: {e}")
    
    # Return default if key not found
    return default
