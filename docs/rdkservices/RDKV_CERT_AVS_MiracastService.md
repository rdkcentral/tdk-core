## TestScript Name
RDKV_CERT_AVS_MiracastService

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [MiracastService_Get_Enable](#miracastservice_get_enable)
   - [MiracastService_Set_Get_Enable](#miracastservice_set_get_enable)
   - [MiracastService_Set_Enable_Without_Parameter](#miracastservice_set_enable_without_parameter)
   - [MiracastService_Accept_Client_Connection](#miracastservice_accept_client_connection)
   - [MiracastService_Reject_Client_Connection](#miracastservice_reject_client_connection)
   - [MiracastService_Set_VideoRectangle](#miracastservice_set_videorectangle)
   - [MiracastService_ActivateDeactivate_Event_Test](#miracastservice_activatedeactivate_event_test)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **MiracastService** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.MiracastService` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_MiracastService_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of MiracastService Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MiracastService"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MiracastService Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.MiracastService"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of MiracastService Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MiracastService"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_MiracastPlayer_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of MiracastPlayer Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MiracastPlayer"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MiracastPlayer Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.MiracastPlayer"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of MiracastPlayer Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MiracastPlayer"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

## Test Cases

<a id="miracastservice_get_enable"></a>
### TestCase Name
MiracastService_Get_Enable

### TestCase ID
Miracast_01

### TestCase Objective
Check if the getEnable method correctly returns the valid enable status of the miracast feature

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Enable | Invoke getEnable on org.rdk.MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.getEnable"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` value returned (`true` or `false`)  |

---

<a id="miracastservice_set_get_enable"></a>
### TestCase Name
MiracastService_Set_Get_Enable

### TestCase ID
Miracast_02

### TestCase Objective
Check if the miracast feature can be enabled or disabled using the setEnable API

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Enable | Invoke getEnable on org.rdk.MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.getEnable"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` value returned (`true` or `false`)  |
| 2 | Set Enable | *(Toggles the enabled value from Step 1: if Step 1 returned true, sets false; if false, sets true)*<br>Invoke setEnable on org.rdk.MiracastService with enabled: "<toggled_value_from_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.setEnable", "params": {"enabled": "<toggled_value_from_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Enable set to toggled value successfully  |
| 3 | Get Enable | Invoke getEnable on org.rdk.MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.getEnable"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the toggled value set in step 1  |

#### TestCase Post-condition 1: Revert_Enable

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Revert Enable | Set Enable on MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.setEnable", "params": {"enabled": "<original_value_from_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Enable reverted successfully  |
| 2 | Verify Reverted Enable | Get Enable from MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.getEnable"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the original value captured in step 1  |

---

<a id="miracastservice_set_enable_without_parameter"></a>
### TestCase Name
MiracastService_Set_Enable_Without_Parameter

### TestCase ID
Miracast_03

### TestCase Objective
Check if the setEnable method returns an error when parameter is not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Enable Without Parameter | Invoke setEnable on org.rdk.MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.setEnable"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="miracastservice_accept_client_connection"></a>
### TestCase Name
MiracastService_Accept_Client_Connection

### TestCase ID
Miracast_04

### TestCase Objective
Check if the method acceptClientConnection successfully accepts a new client connection request

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Miracast_Feature

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Enable | Get Enable from MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.getEnable"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` value returned (`true` or `false`)  |
| 2 | Set Enable | *(Conditional statement executed only if previous step condition is met)*<br>Set Enable on MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.setEnable", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Enable set successfully  |
| 3 | Get Enable | *(Conditional statement executed only if previous step condition is met)*<br>Get Enable from MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.getEnable"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled`: `true` (Miracast feature is enabled)  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Accept Client Connection | Invoke acceptClientConnection on org.rdk.MiracastService with requestStatus: "Accept"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.acceptClientConnection", "params": {"requestStatus": "Accept"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`  |

---

<a id="miracastservice_reject_client_connection"></a>
### TestCase Name
MiracastService_Reject_Client_Connection

### TestCase ID
Miracast_05

### TestCase Objective
Check if the method acceptClientConnection successfully reject a new client connection request

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Miracast_Feature

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Enable | Get Enable from MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.getEnable"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` value returned (`true` or `false`)  |
| 2 | Set Enable | *(Conditional statement executed only if previous step condition is met)*<br>Set Enable on MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.setEnable", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Enable set successfully  |
| 3 | Get Enable | *(Conditional statement executed only if previous step condition is met)*<br>Get Enable from MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.getEnable"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled`: `true` (Miracast feature is enabled)  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reject Client Connection | Invoke acceptClientConnection on org.rdk.MiracastService with requestStatus: "Reject"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastService.1.acceptClientConnection", "params": {"requestStatus": "Reject"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`  |

---

<a id="miracastservice_set_videorectangle"></a>
### TestCase Name
MiracastService_Set_VideoRectangle

### TestCase ID
Miracast_06

### TestCase Objective
Check if the device is able to successfully set the video rectangle

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set VideoRectangle | Invoke setVideoRectangle on org.rdk.MiracastPlayer<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MiracastPlayer.1.setVideoRectangle", "params": {"X": 0, "Y": 0, "W": 1920, "H": 1080}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Video Rectangle set successfully  |

---

<a id="miracastservice_activatedeactivate_event_test"></a>
### TestCase Name
MiracastService_ActivateDeactivate_Event_Test

### TestCase ID
Miracast_07

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of MiracastService Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MiracastService"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MiracastService Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.MiracastService"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of MiracastService Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MiracastService"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate MiracastService Plugin | Invoke deactivate on Controller with callsign: "org.rdk.MiracastService"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.MiracastService"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `org.rdk.miracastservice` with state `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MiracastService"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate MiracastService Plugin | Invoke activate on Controller with callsign: "org.rdk.MiracastService"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.MiracastService"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `org.rdk.miracastservice` with state `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.MiracastService<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MiracastService"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 15 mins

**Priority** : Medium

**Release Version** : M142

<div align="right"><a href="#testscript-name">Go to Top</a></div>
