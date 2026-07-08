## TestScript Name
RDKV_CERT_AVS_ScreenCapture

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [ScreenCapture_Check_Upload_Screen_Invalid_Url](#screencapture_check_upload_screen_invalid_url)
   - [ScreenCapture_Upload_Screen](#screencapture_upload_screen)
   - [ScreenCapture_Check_Upload_Complete_Event](#screencapture_check_upload_complete_event)
   - [ScreenCapture_Check_Upload_Complete_Event_Invalid_Url](#screencapture_check_upload_complete_event_invalid_url)
   - [ScreenCapture_Check_CallGUID](#screencapture_check_callguid)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **ScreenCapture** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.ScreenCapture` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of ScreenCapture Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ScreenCapture"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate ScreenCapture Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.ScreenCapture"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of ScreenCapture Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ScreenCapture"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the uploadComplete event | Register a WebSocket event listener for `uploadComplete` to receive `uploadComplete` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.register", "params": {"event": "uploadComplete", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure SC Invalid Upload URL | `SC_INVALID_UPLOAD_URL` must be set to the invalid image upload URL used for negative test scenarios (unreachable server) | The `SC_INVALID_UPLOAD_URL` value should be correctly configured in the device-specific config file |
| 2 | Configure SC Upload URL | `SC_UPLOAD_URL` must be set to the CGI server URL for uploading the captured image PNG data | The `SC_UPLOAD_URL` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="screencapture_check_upload_screen_invalid_url"></a>
### TestCase Name
ScreenCapture_Check_Upload_Screen_Invalid_Url

### TestCase ID
SC_01

### TestCase Objective
Check screen upload with invalid url

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_INVALID_UPLOAD_URL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_INVALID_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` indicating the upload request was accepted |

---

<a id="screencapture_upload_screen"></a>
### TestCase Name
ScreenCapture_Upload_Screen

### TestCase ID
SC_02

### TestCase Objective
Uploads the screenshot

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_UPLOAD_URL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` indicating the screen capture upload is initiated successfully |

---

<a id="screencapture_check_upload_complete_event"></a>
### TestCase Name
ScreenCapture_Check_Upload_Complete_Event

### TestCase ID
SC_03

### TestCase Objective
Upload screen and receive uploadComplete Event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_UPLOAD_URL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` indicating the screen capture upload is initiated successfully |
| 2 | Check Upload Complete Event | Listen for `uploadComplete` event and wait up to 10 second(s) | Ensure the `uploadComplete` event is received with `status`: `true` indicating successful screen capture upload |

---

<a id="screencapture_check_upload_complete_event_invalid_url"></a>
### TestCase Name
ScreenCapture_Check_Upload_Complete_Event_Invalid_Url

### TestCase ID
SC_04

### TestCase Objective
Uploads screen and checks if uploadComplete Event is received for invalid url

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_INVALID_UPLOAD_URL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_INVALID_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` indicating the upload request was accepted |
| 2 | Check Upload Complete Event | Listen for `uploadComplete` event and wait up to 10 second(s) | Ensure the `uploadComplete` event is received with `status`: `false` indicating upload failure due to invalid URL |

---

<a id="screencapture_check_callguid"></a>
### TestCase Name
ScreenCapture_Check_CallGUID

### TestCase ID
SC_05

### TestCase Objective
Upload screen and check GUID in  uploadComplete Event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_UPLOAD_URL>", callGUID: "screenshot"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_UPLOAD_URL>", "callGUID": "screenshot"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` indicating the screen capture upload is initiated successfully |
| 2 | Check Upload Complete Event | Listen for `uploadComplete` event and wait up to 10 second(s) | Ensure the `uploadComplete` event is received with `status`: `true` and `callGUID` as `screenshot` |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the uploadComplete event | Unregister the WebSocket event listener for `uploadComplete` to stop receiving `uploadComplete` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.unregister", "params": {"event": "uploadComplete", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI-Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M82 |

<div align="right"><a href="#testscript-name">&#8593; Go to Top</a></div>
