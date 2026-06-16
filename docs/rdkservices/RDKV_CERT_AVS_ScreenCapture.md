## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [ScreenCapture_Check_Upload_Screen_Invalid_Url (SC_01)](#screencapture_check_upload_screen_invalid_url-sc_01)
   - [ScreenCapture_Upload_Screen (SC_02)](#screencapture_upload_screen-sc_02)
   - [ScreenCapture_Check_Upload_Complete_Event (SC_03)](#screencapture_check_upload_complete_event-sc_03)
   - [ScreenCapture_Check_Upload_Complete_Event_Invalid_Url (SC_04)](#screencapture_check_upload_complete_event_invalid_url-sc_04)
   - [ScreenCapture_Check_CallGUID (SC_05)](#screencapture_check_callguid-sc_05)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **ScreenCapture** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.ScreenCapture` (version 1)

**API Coverage**

- **Events**: `uploadComplete`
- **Other APIs**: `uploadScreenCapture`

### APIs Under Test

| API | Description |
|-----|-------------|
| `uploadScreenCapture` | Takes screenshot and uploads it to the specified url |

### Events Under Test

| Event | Description |
|-------|-------------|
| `uploadComplete` | Fired after an upload of screen capture |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ScreenCapture"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.ScreenCapture"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.ScreenCapture"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ScreenCapture"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_Upload_Complete` on `ScreenCapture` plugin

---

## Test Cases

<a id="screencapture_check_upload_screen_invalid_url-sc_01"></a>
### ScreenCapture_Check_Upload_Screen_Invalid_Url (SC_01)

**Objective:** Check screen upload with invalid url

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke `uploadScreenCapture` on `org.rdk.ScreenCapture` with `url`: `"<SC_INVALID_UPLOAD_URL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_INVALID_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |

---

<a id="screencapture_upload_screen-sc_02"></a>
### ScreenCapture_Upload_Screen (SC_02)

**Objective:** Uploads the screenshott

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke `uploadScreenCapture` on `org.rdk.ScreenCapture` with `url`: `"<SC_UPLOAD_URL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |

---

<a id="screencapture_check_upload_complete_event-sc_03"></a>
### ScreenCapture_Check_Upload_Complete_Event (SC_03)

**Objective:** Upload screen and receive uploadComplete Event

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke `uploadScreenCapture` on `org.rdk.ScreenCapture` with `url`: `"<SC_UPLOAD_URL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |
| 2 | Check Upload Complete Event | Listen for `Event_Upload_Complete` event (wait 10s) | Expected `True` |

---

<a id="screencapture_check_upload_complete_event_invalid_url-sc_04"></a>
### ScreenCapture_Check_Upload_Complete_Event_Invalid_Url (SC_04)

**Objective:** Uploads screen and checks if uploadComplete Event is received for invalid url

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke `uploadScreenCapture` on `org.rdk.ScreenCapture` with `url`: `"<SC_INVALID_UPLOAD_URL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_INVALID_UPLOAD_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |
| 2 | Check Upload Complete Event | Listen for `Event_Upload_Complete` event (wait 10s) | Expected `False` |

---

<a id="screencapture_check_callguid-sc_05"></a>
### ScreenCapture_Check_CallGUID (SC_05)

**Objective:** Upload screen and check GUID in  uploadComplete Event

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Upload Screen Capture | Invoke `uploadScreenCapture` on `org.rdk.ScreenCapture` with `url`: `"<SC_UPLOAD_URL>"`, `callGUID`: `"screenshot"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ScreenCapture.1.uploadScreenCapture", "params": {"url": "<SC_UPLOAD_URL>", "callGUID": "screenshot"}}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |
| 2 | Check Upload Complete Event | Listen for `Event_Upload_Complete` event (wait 10s) | Expected `True`, callGUID `screenshot` |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M82 |