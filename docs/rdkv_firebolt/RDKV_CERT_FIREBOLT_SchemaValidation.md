## TestCase ID
RDKV_CERT_FIREBOLT_01
## TestCase Name
RDKV_CERT_FIREBOLT_SchemaValidation
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Firebolt certification application can be installed and launched on the device through the App Manager plugins, executes the Firebolt schema validation suite, and publishes the JSON, HTML and Excel certification reports to the report server so that they can be collected by the TDK framework.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device connectivity | The device under test must be reachable over the network and the WPEFramework (Thunder) JSON-RPC service must be running on the configured device IP and port. | The device should respond to JSON-RPC requests and the rdkv_firebolt test module should load successfully. |
| 2 | Confirm required plugins are available | The plugins org.rdk.DownloadManager, org.rdk.AppPackageManager and org.rdk.AppManager must be available on the device. The test activates them if they are not already in the activated state. | The three plugins should be present on the device and should be capable of reaching the activated state. |
| 3 | Confirm Firebolt application settings | The variables `firebolt_bundle` (application bundle file name), `firebolt_app_id` (application package ID) and `app_download_url` (bundle download URL) must be configured in the Firebolt test variables file so that the application bundle can be downloaded from `app_download_url/firebolt_bundle`. | The bundle URL should be valid and the bundle should be downloadable by the device. |
| 4 | Confirm device configuration key for package location | The device configuration key `PACKAGEMANAGER_FILE_LOCATOR` must be set in the device or device-type configuration file. It is used to build the file location of the downloaded bundle for installation. | The key should be present and must contain a non-empty value. |
| 5 | Confirm report server availability | The Firebolt certification report server (`http_server.py`) must be running and reachable at the URL configured in `report_server_url`. The URL must match the report publish URL used by the Firebolt application. | The report server should accept requests from the TDK framework and from the device. |
| 6 | Confirm report storage location | The directory configured in `reports_directory` (relative to the TDK fileStore, or an absolute path on the Test Manager host) must be the folder where the report server stores the uploaded reports in the json, html and xlsx sub folders. | The directory should be accessible to the TDK framework and should be populated by the report server with the uploaded reports. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check the status of the required plugins | Query the current state of each of the three plugins using the Controller status API.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}`<br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppPackageManager"}`<br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` | The status request for each plugin should return successfully along with the current plugin state. |
| 2 | Activate the plugins that are not activated | If any of the plugins is not in the activated state, activate the plugins using the Controller activate API and wait for 10 seconds.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}`<br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppPackageManager"}}`<br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}` | The activate request for each plugin should return success. The plugins org.rdk.DownloadManager, org.rdk.AppPackageManager and org.rdk.AppManager should be in the activated state. |
| 3 | Register the Firebolt report run with the report server | Send a POST request to the report server at `report_server_url` + `automation/runs` with the device IP, a reporting ID built from the TDK execution ID (`tdk_<execution id>`) and a timeout of 4500 seconds. The Firebolt application later reads this reporting ID to name its reports.<br>`POST <report_server_url>automation/runs`<br>`{"deviceIp": "<DUT IP>", "reportingId": "tdk_<execution id>", "timeout": 4500}` | The report server should accept the request and respond with HTTP 201 and the reporting ID. The run should get registered for the device IP. |
| 4 | Get the list of installed packages | Retrieve the packages installed on the device and check whether the Firebolt application package (`firebolt_app_id`) is present with state INSTALLED.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppPackageManager.1.listPackages"}` | The request should return success. If the package is already listed as installed, the download and installation steps (steps 5 to 9) must be skipped. |
| 5 | Check the status of the required plugins before installation | If the application is not installed, query the state of the three plugins again and activate them, as in steps 1 and 2, when they are not activated.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}`<br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppPackageManager"}`<br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` | All three plugins should be in the activated state. |
| 6 | Download the Firebolt application bundle | Download the bundle from `app_download_url` followed by `/firebolt_bundle` using the Download Manager, then wait for 10 seconds.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<firebolt_bundle>"}}` | The download request should return success along with the downloaded file details. The bundle should get downloaded to the device. |
| 7 | Read the package file locator from the device configuration | Read the key `PACKAGEMANAGER_FILE_LOCATOR` from the device configuration file and append the downloaded file details returned by the download request to build the file locator. | The key should be available with a non-empty value and the file locator should be formed successfully. |
| 8 | Install the Firebolt application package | Install the downloaded package using the App Package Manager.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppPackageManager.install", "params": {"packageId": "<firebolt_app_id>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR><downloaded file details>"}}` | The install request should return success. |
| 9 | Verify the application installation | Retrieve the installed packages again and check that the package is listed.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppPackageManager.1.listPackages"}` | The Firebolt application package (`firebolt_app_id`) should be listed with state INSTALLED. |
| 10 | Launch the Firebolt application | Launch the application using the App Manager.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<firebolt_app_id>", "intent": "", "launchArgs": ""}}` | The launch request should return success. |
| 11 | Verify the application is loaded and active | Wait for 10 seconds and retrieve the loaded applications from the App Manager.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | The Firebolt application (`firebolt_app_id`) should be listed in the loaded apps with lifecycleState `APP_STATE_ACTIVE`. The application should start the Firebolt schema validation run automatically. |
| 12 | Wait for the test run to start | Wait for 10 seconds after the application launch before looking for the reports. During the run the application reads the reporting ID registered in step 3 from the report server and uploads the JSON, HTML and Excel reports once the suite completes.<br>`GET <report_server_url>automation/context?deviceIp=<DUT IP>` | The application should receive the reporting ID `tdk_<execution id>` and should begin executing the Firebolt schema validation suite. |
| 13 | Search for the generated reports | Search the `reports_directory` under the TDK fileStore, including the json, html and xlsx sub folders, for files whose names start with `tdk_<execution id>`. The search is attempted up to 10 times with a 3 second wait between attempts. | At least one report file starting with `tdk_<execution id>` should be found within the retry period. If no report is found, the test must be marked as failed. |
| 14 | Copy the HTML and Excel reports to the execution log folder | For each report found with the extension .html or .xlsx, copy the file to the execution log path using the file name format `<log path><execution id>_<device id>_<result id>_<report file name>`. | The HTML and Excel reports should get copied to the execution log folder and should be available as part of the test result. |
| 15 | Terminate the Firebolt application | Terminate the application using the App Manager.<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<firebolt_app_id>"}}` | The terminate request should return success and the application should get closed. |
| 16 | Unload the test module | Unload the rdkv_firebolt test module after the execution completes. | The module should get unloaded successfully and the overall test result should be reported as SUCCESS when all the above steps pass. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 5 minutes

**Priority** : High

**Release Version** : M156<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
