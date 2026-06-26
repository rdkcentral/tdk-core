## TestScript Name
RDKV_CERT_AVS_ScreenCapture

## Table of Contents

1. [Objective](#objective)
2. [APIs Under Test](#apis-under-test)
3. [Events Under Test](#events-under-test)
4. [Plugin Pre-conditions](#plugin-pre-conditions)
5. [Test Cases](#test-cases)
   - [ScreenCapture_Check_Upload_Screen_Invalid_Url](#screencapture_check_upload_screen_invalid_url)
   - [ScreenCapture_Upload_Screen](#screencapture_upload_screen)
   - [ScreenCapture_Check_Upload_Complete_Event](#screencapture_check_upload_complete_event)
   - [ScreenCapture_Check_Upload_Complete_Event_Invalid_Url](#screencapture_check_upload_complete_event_invalid_url)
   - [ScreenCapture_Check_CallGUID](#screencapture_check_callguid)
6. [Plugin Post-conditions](#plugin-post-conditions)
7. [Test Attributes](#test-attributes)

## Objective

The **ScreenCapture** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.ScreenCapture` (version 1)

## APIs Under Test

| API | Description |
|-----|-------------|
| `uploadScreenCapture` | Takes screenshot and uploads it to the specified url |

## Events Under Test

| Event | Description |
|-------|-------------|
| `uploadComplete` | Fired after an upload of screen capture |

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of ScreenCapture Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ScreenCapture"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate ScreenCapture Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.ScreenCapture"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of ScreenCapture Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ScreenCapture"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_Upload_Complete` on `ScreenCapture` plugin

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
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_INVALID_UPLOAD_URL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_INVALID_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |

---

<a id="screencapture_upload_screen"></a>
### TestCase Name
ScreenCapture_Upload_Screen

### TestCase ID
SC_02

### TestCase Objective
Uploads the screenshott

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_UPLOAD_URL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |

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
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_UPLOAD_URL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |
| 2 | Check Upload Complete Event | Listen for Event_Upload_Complete event (wait 10s) | Expected `True` |

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
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_INVALID_UPLOAD_URL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_INVALID_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |
| 2 | Check Upload Complete Event | Listen for Event_Upload_Complete event (wait 10s) | Expected `False` |

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
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke uploadScreenCapture on org.rdk.ScreenCapture with url: "<SC_UPLOAD_URL>", callGUID: "screenshot"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_UPLOAD_URL>", "callGUID": "screenshot"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |
| 2 | Check Upload Complete Event | Listen for Event_Upload_Complete event (wait 10s) | Expected `True`, callGUID `screenshot` |

## Plugin Post-conditions

_No plugin-level post-conditions defined_

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M82 |
