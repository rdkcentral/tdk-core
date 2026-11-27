## TestScript Name
RDKV_CERT_AVS_AppPackageManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [AppPackageManager_ListPackages_Functionality](#apppackagemanager_listpackages_functionality)
   - [AppPackageManager_Install_ValidParameters](#apppackagemanager_install_validparameters)
   - [AppPackageManager_Uninstall_ValidParameters](#apppackagemanager_uninstall_validparameters)
   - [AppPackageManager_GetPackageState_EmptyParameters](#apppackagemanager_getpackagestate_emptyparameters)
   - [AppPackageManager_GetPackageState_InvalidParameters](#apppackagemanager_getpackagestate_invalidparameters)
   - [AppPackageManager_Uninstall_InvalidParameter](#apppackagemanager_uninstall_invalidparameter)
   - [AppPackageManager_Install_InvalidParameters](#apppackagemanager_install_invalidparameters)
   - [AppPackageManager_Uninstall_EmptyParameters](#apppackagemanager_uninstall_emptyparameters)
   - [AppPackageManager_Uninstall_TwoTimes](#apppackagemanager_uninstall_twotimes)
   - [AppPackageManager_Install_EmptyParameters](#apppackagemanager_install_emptyparameters)
   - [AppPackageManager_Package_State_After_Install](#apppackagemanager_package_state_after_install)
   - [AppPackageManager_Package_State_After_Uninstall](#apppackagemanager_package_state_after_uninstall)
   - [AppPackageManager_Config_ValidParameters](#apppackagemanager_config_validparameters)
   - [AppPackageManager_Config_EmptyParameters](#apppackagemanager_config_emptyparameters)
   - [AppPackageManager_Config_InvalidParameters](#apppackagemanager_config_invalidparameters)
   - [AppPackageManager_Config_EmptyPackageId_ValidVersion](#apppackagemanager_config_emptypackageid_validversion)
   - [AppPackageManager_Config_ValidPackageId_EmptyVersion](#apppackagemanager_config_validpackageid_emptyversion)
   - [AppPackageManager_On_AppInstallationStatus_Event](#apppackagemanager_on_appinstallationstatus_event)
   - [AppPackageManager_GetPackageState_ValidPackageId_InvalidVersion](#apppackagemanager_getpackagestate_validpackageid_invalidversion)
   - [AppPackageManager_GetPackageState_InvalidPackageId_ValidVersion](#apppackagemanager_getpackagestate_invalidpackageid_validversion)
   - [AppPackageManager_GetPackageState_NoParameters](#apppackagemanager_getpackagestate_noparameters)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **PackageManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.AppPackageManager` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_AppStorageManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of AppStorageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppStorageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of AppStorageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_PackageManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of AppPackageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppPackageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppPackageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppPackageManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of AppPackageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppPackageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onAppInstallationStatus event | Register a WebSocket event listener for `onAppInstallationStatus` to receive `onAppInstallationStatus` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.register", "params": {"event": "onAppInstallationStatus", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 4: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure application name | `PACKAGEMANAGER_APPLICATION_NAME` must be set to the application/package name to be installed | The `PACKAGEMANAGER_APPLICATION_NAME` value should be correctly configured in the device-specific config file |
| 2 | Configure application version | `PACKAGEMANAGER_APPLICATION_VERSION` must be set to the application version to be installed | The `PACKAGEMANAGER_APPLICATION_VERSION` value should be correctly configured in the device-specific config file |
| 3 | Configure application hosted URL | `PACKAGEMANAGER_APPLICATION_HOSTEDURL` must be set to the hosted URL of the primary application/package | The `PACKAGEMANAGER_APPLICATION_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 4 | Configure additionalmetadata name | `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` must be set to the additional metadata key associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` value should be correctly configured in the device-specific config file |
| 5 | Configure additionalmetadata value | `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` must be set to the additional metadata value associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` value should be correctly configured in the device-specific config file |
| 6 | Configure application MD5 checksum value | `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` must be set to the expected MD5 checksum of the application package for download integrity verification | The `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="apppackagemanager_listpackages_functionality"></a>
### TestCase Name
AppPackageManager_ListPackages_Functionality

### TestCase ID
PM_01

### TestCase Objective
Verify that the listPackages method functions correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | List all installed packages | Invoke listPackages on org.rdk.AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |

---

<a id="apppackagemanager_install_validparameters"></a>
### TestCase Name
AppPackageManager_Install_ValidParameters

### TestCase ID
PM_02

### TestCase Objective
Verify that the install method works correctly with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Check_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | Uninstall on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download valid parameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install package on device | Invoke install on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", fileLocator: "<result_step_2>", name: "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", value: "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify installed package | Invoke listPackages on org.rdk.AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

---

<a id="apppackagemanager_uninstall_validparameters"></a>
### TestCase Name
AppPackageManager_Uninstall_ValidParameters

### TestCase ID
PM_03

### TestCase Objective
Verify that the uninstall method works correctly with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | Uninstall on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download valid parameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install package on device | Install on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify installed package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall package from device | Invoke uninstall on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Verify uninstalled package | Invoke listPackages on org.rdk.AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the package is successfully uninstalled |

---

<a id="apppackagemanager_getpackagestate_emptyparameters"></a>
### TestCase Name
AppPackageManager_GetPackageState_EmptyParameters

### TestCase ID
PM_04

### TestCase Objective
Verify that the getPackageState method handles empty parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetPackageState empty parameters | Invoke packageState on org.rdk.AppPackageManager with packageId: "", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.packageState", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_getpackagestate_invalidparameters"></a>
### TestCase Name
AppPackageManager_GetPackageState_InvalidParameters

### TestCase ID
PM_05

### TestCase Objective
Verify that the getPackageState method handles invalid parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetPackageState invalid parameters | Invoke packageState on org.rdk.AppPackageManager with packageId: "invalid_package_id", version: "invalid_version"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.packageState", "params": {"packageId": "invalid_package_id", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_uninstall_invalidparameter"></a>
### TestCase Name
AppPackageManager_Uninstall_InvalidParameter

### TestCase ID
PM_06

### TestCase Objective
Verify that the uninstall method handles invalid parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall invalid parameter | Invoke uninstall on org.rdk.AppPackageManager with packageId: "invalid_package_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "invalid_package_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_install_invalidparameters"></a>
### TestCase Name
AppPackageManager_Install_InvalidParameters

### TestCase ID
PM_07

### TestCase Objective
Verify that the install method handles invalid parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Install invalid parameters | Invoke install on org.rdk.AppPackageManager with packageId: "invalid_package_id", version: "invalid_version", fileLocator: "invalid_file_locator", name: "invalid_name", value: "invalid_value"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.install", "params": {"packageId": "invalid_package_id", "version": "invalid_version", "fileLocator": "invalid_file_locator", "name": "invalid_name", "value": "invalid_value"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_uninstall_emptyparameters"></a>
### TestCase Name
AppPackageManager_Uninstall_EmptyParameters

### TestCase ID
PM_08

### TestCase Objective
Verify that the uninstall method handles empty parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall empty parameters | Invoke uninstall on org.rdk.AppPackageManager with packageId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_uninstall_twotimes"></a>
### TestCase Name
AppPackageManager_Uninstall_TwoTimes

### TestCase ID
PM_09

### TestCase Objective
Verify uninstall method with valid parameters and perform two consecutive uninstall operations

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | Uninstall on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download valid parameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install package on device | Install on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify installed package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall package (initial attempt) | Invoke uninstall on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Verify uninstalled package | Invoke listPackages on org.rdk.AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the package is successfully uninstalled |
| 3 | Attempt uninstall of already-removed package (error case) | Invoke uninstall on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_install_emptyparameters"></a>
### TestCase Name
AppPackageManager_Install_EmptyParameters

### TestCase ID
PM_10

### TestCase Objective
Verify that the install method handles empty parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Install empty parameters | Invoke install on org.rdk.AppPackageManager with packageId: "", version: "", fileLocator: "", name: "", value: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.install", "params": {"packageId": "", "version": "", "fileLocator": "", "name": "", "value": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Requested version is not supported.` |

---

<a id="apppackagemanager_package_state_after_install"></a>
### TestCase Name
AppPackageManager_Package_State_After_Install

### TestCase ID
PM_11

### TestCase Objective
Verify that the package state method works correctly after installing a package with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | Uninstall on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download valid parameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install package on device | Install on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check package state | Invoke packageState on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the installation status is `INSTALLED`, confirming the package was installed successfully  |

---

<a id="apppackagemanager_package_state_after_uninstall"></a>
### TestCase Name
AppPackageManager_Package_State_After_Uninstall

### TestCase ID
PM_12

### TestCase Objective
Verify that the package state method works correctly after uninstalling a package with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | Uninstall on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download valid parameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install package on device | Install on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify installed package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall package from device | Invoke uninstall on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check package state | Invoke packageState on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the package status is `UNINSTALLED`, confirming successful uninstallation  |

---

<a id="apppackagemanager_config_validparameters"></a>
### TestCase Name
AppPackageManager_Config_ValidParameters

### TestCase ID
PM_13

### TestCase Objective
Verify that the config method works correctly with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Check_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | Uninstall on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download valid parameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install package on device | Invoke install on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", fileLocator: "<result_step_2>", name: "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", value: "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify installed package | Invoke listPackages on org.rdk.AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |
| 4 | Get installed app config | Invoke config on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.config", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call is successful and returns a non-null, non-empty response  |

---

<a id="apppackagemanager_config_emptyparameters"></a>
### TestCase Name
AppPackageManager_Config_EmptyParameters

### TestCase ID
PM_14

### TestCase Objective
Verify that the config method handles empty parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Config empty parameters | Invoke config on org.rdk.AppPackageManager with packageId: "", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.config", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_config_invalidparameters"></a>
### TestCase Name
AppPackageManager_Config_InvalidParameters

### TestCase ID
PM_15

### TestCase Objective
Verify that the config method handles invalid parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Config invalid parameters | Invoke config on org.rdk.AppPackageManager with packageId: "invalid_package_id", version: "invalid_version"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.config", "params": {"packageId": "invalid_package_id", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_config_emptypackageid_validversion"></a>
### TestCase Name
AppPackageManager_Config_EmptyPackageId_ValidVersion

### TestCase ID
PM_16

### TestCase Objective
Verify that the config method handles empty packageId with valid version correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Config EmptyPackageId ValidVersion | Invoke config on org.rdk.AppPackageManager with packageId: "", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.config", "params": {"packageId": "", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_config_validpackageid_emptyversion"></a>
### TestCase Name
AppPackageManager_Config_ValidPackageId_EmptyVersion

### TestCase ID
PM_17

### TestCase Objective
Verify that the config method handles valid packageId with empty version correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Config ValidPackageId EmptyVersion | Invoke config on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.config", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_on_appinstallationstatus_event"></a>
### TestCase Name
AppPackageManager_On_AppInstallationStatus_Event

### TestCase ID
PM_18

### TestCase Objective
Verify that the appInstallationStatus event is triggered with correct status during app installation and uninstallation

### TestCase Pre-condition

#### TestCase Pre-condition 1: Check_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download valid parameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install package on device | Invoke install on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", fileLocator: "<result_step_2>", name: "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", value: "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | GetPackageState valid parameters | Invoke packageState on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the installation status is `INSTALLED`, confirming the package was installed successfully  |
| 4 | Check event on app installation status | Listen for event Event_On_AppInstallationStatus | Verify that event data is validated successfully |
| 5 | Uninstall package from device | Invoke uninstall on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 6 | GetPackageState after uninstall | Invoke packageState on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the package status is `UNINSTALLED`, confirming successful uninstallation  |
| 7 | Check event on app installation status | Listen for event Event_On_AppInstallationStatus | Verify that event data is validated successfully |

---

<a id="apppackagemanager_getpackagestate_validpackageid_invalidversion"></a>
### TestCase Name
AppPackageManager_GetPackageState_ValidPackageId_InvalidVersion

### TestCase ID
PM_19

### TestCase Objective
Verify that the getPackageState method handles valid packageId with invalid version correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetPackageState ValidPackageId InvalidVersion | Invoke packageState on org.rdk.AppPackageManager with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "invalid_version"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_getpackagestate_invalidpackageid_validversion"></a>
### TestCase Name
AppPackageManager_GetPackageState_InvalidPackageId_ValidVersion

### TestCase ID
PM_20

### TestCase Objective
Verify that the getPackageState method handles invalid packageId with valid version correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetPackageState InvalidPackageId ValidVersion | Invoke packageState on org.rdk.AppPackageManager with packageId: "invalid_package_id", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.packageState", "params": {"packageId": "invalid_package_id", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="apppackagemanager_getpackagestate_noparameters"></a>
### TestCase Name
AppPackageManager_GetPackageState_NoParameters

### TestCase ID
PM_21

### TestCase Objective
Verify that the getPackageState method handles missing parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get package state without required parameters (error case) | Invoke packageState on org.rdk.AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.packageState"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onAppInstallationStatus event | Unregister the WebSocket event listener for `onAppInstallationStatus` to stop receiving `onAppInstallationStatus` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.unregister", "params": {"event": "onAppInstallationStatus", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |

### Plugin Post-condition 2: Uninstall_Package

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on AppPackageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 20 mins

**Priority** : High

**Release Version** : M147

<div align="right"><a href="#testscript-name">Go to Top</a></div>
