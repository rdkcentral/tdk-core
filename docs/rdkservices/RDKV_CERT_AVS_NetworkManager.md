## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [NetworkManager_Get_Device_Interfaces (NM_01)](#networkmanager_get_device_interfaces-nm_01)
   - [NetworkManager_Get_Primary/Default_Interface (NM_02)](#networkmanager_get_primary-default_interface-nm_02)
   - [NetworkManager_Validate_Public_IPv4_IP (NM_03)](#networkmanager_validate_public_ipv4_ip-nm_03)
   - [NetworkManager_Ping_IPv4_Endpoint (NM_04)](#networkmanager_ping_ipv4_endpoint-nm_04)
   - [NetworkManager_Trace_IPv4_Endpoint (NM_05)](#networkmanager_trace_ipv4_endpoint-nm_05)
   - [NetworkManager_Check_Internet_IPv4_Connectivity (NM_06)](#networkmanager_check_internet_ipv4_connectivity-nm_06)
   - [NetworkManager_GetAvailableInterfaces_With_Enabled/Disabled_Interface (NM_07)](#networkmanager_getavailableinterfaces_with_enabled-disabled_interface-nm_07)
   - [NetworkManager_Check_On_Interface_StateChange_Event (NM_08)](#networkmanager_check_on_interface_statechange_event-nm_08)
   - [NetworkManager_Wifi_Start_Stop_Scan (NM_09)](#networkmanager_wifi_start_stop_scan-nm_09)
   - [NetworkManager_Check_On_AvailableSSIDs_Event (NM_10)](#networkmanager_check_on_availablessids_event-nm_10)
   - [NetworkManager_Get_Interface_State (NM_11)](#networkmanager_get_interface_state-nm_11)
   - [NetworkManager_SetandGet_Interface_State (NM_12)](#networkmanager_setandget_interface_state-nm_12)
   - [NetworkManager_Wifi_Connect_Disconnect (NM_13)](#networkmanager_wifi_connect_disconnect-nm_13)
   - [NetworkManager_Check_Get_Connected_SSID (NM_14)](#networkmanager_check_get_connected_ssid-nm_14)
   - [NetworkManager_Get_Supported_Security_Modes (NM_15)](#networkmanager_get_supported_security_modes-nm_15)
   - [NetworkManager_Check_On_WifiStateChange_Event (NM_16)](#networkmanager_check_on_wifistatechange_event-nm_16)
   - [NetworkManager_Check_WifiConnect_With_Invalid_SSID_Passphrase (NM_17)](#networkmanager_check_wificonnect_with_invalid_ssid_passphrase-nm_17)
   - [NetworkManager_Check_On_AvailableSSIDs_Event_Not_Triggered (NM_18)](#networkmanager_check_on_availablessids_event_not_triggered-nm_18)
   - [NetworkManager_SetandGet_Stun_Endpoint (NM_19)](#networkmanager_setandget_stun_endpoint-nm_19)
   - [NetworkManager_5GHz_Wifi_Connect_Disconnect (NM_20)](#networkmanager_5ghz_wifi_connect_disconnect-nm_20)
   - [NetworkManager_Check_5GHz_Get_Connected_SSID (NM_21)](#networkmanager_check_5ghz_get_connected_ssid-nm_21)
   - [NetworkManager_SetInterfaceState_Without_Enable_Parameter (NM_22)](#networkmanager_setinterfacestate_without_enable_parameter-nm_22)
   - [NetworkManager_SetInterfaceState_Without_Parameter (NM_23)](#networkmanager_setinterfacestate_without_parameter-nm_23)
   - [NetworkManager_GetInterfaceState_With_Invalid_Parameter (NM_24)](#networkmanager_getinterfacestate_with_invalid_parameter-nm_24)
   - [NetworkManager_Check_Logging_Level (NM_25)](#networkmanager_check_logging_level-nm_25)
   - [NetworkManager_Set_Lowest_Logging_Level (NM_26)](#networkmanager_set_lowest_logging_level-nm_26)
   - [NetworkManager_Set_Mid-range_Logging_Level (NM_27)](#networkmanager_set_mid-range_logging_level-nm_27)
   - [NetworkManager_Set_Highest_Logging_Level (NM_28)](#networkmanager_set_highest_logging_level-nm_28)
   - [NetworkManager_Check_Wifi_State (NM_29)](#networkmanager_check_wifi_state-nm_29)
   - [NetworkManager_Connect_Wifi_And_Check_Wifi_State (NM_30)](#networkmanager_connect_wifi_and_check_wifi_state-nm_30)
   - [NetworkManager_Set_Single_Connectivity_Test_Endpoints (NM_31)](#networkmanager_set_single_connectivity_test_endpoints-nm_31)
   - [NetworkManager_Set_Five_Connectivity_Test_Endpoints (NM_32)](#networkmanager_set_five_connectivity_test_endpoints-nm_32)
   - [NetworkManager_Check_Wifi_State_After_Connecting_To_Wifi (NM_33)](#networkmanager_check_wifi_state_after_connecting_to_wifi-nm_33)
   - [NetworkManager_Start_Scan_And_Check_Wifi_State (NM_34)](#networkmanager_start_scan_and_check_wifi_state-nm_34)
   - [NetworkManager_Check_Wifi_State_On_Connecting_To_Invalid_Wifi_SSID (NM_35)](#networkmanager_check_wifi_state_on_connecting_to_invalid_wifi_ssid-nm_35)
   - [NetworkManager_SetandGet_Connectivity_Test_Endpoints (NM_36)](#networkmanager_setandget_connectivity_test_endpoints-nm_36)
   - [NetworkManager_Check_WiFi_StateChange_Event_On_Connecting_To_Wifi (NM_37)](#networkmanager_check_wifi_statechange_event_on_connecting_to_wifi-nm_37)
   - [NetworkManager_Set_Invalid_Interface_State (NM_38)](#networkmanager_set_invalid_interface_state-nm_38)
   - [NetworkManager_GetInterfaceState_With_Empty_Parameter (NM_39)](#networkmanager_getinterfacestate_with_empty_parameter-nm_39)
   - [NetworkManager_Ping_Invalid_Endpoint (NM_40)](#networkmanager_ping_invalid_endpoint-nm_40)
   - [NetworkManager_Ping_Endpoint_With_Invalid_IPVersion (NM_41)](#networkmanager_ping_endpoint_with_invalid_ipversion-nm_41)
   - [NetworkManager_Remove_Invalid_SSID (NM_42)](#networkmanager_remove_invalid_ssid-nm_42)
   - [NetworkManager_Remove_Empty_SSID (NM_43)](#networkmanager_remove_empty_ssid-nm_43)
   - [NetworkManager_GetInterfaceState_Without_Parameter (NM_44)](#networkmanager_getinterfacestate_without_parameter-nm_44)
   - [NetworkManager_Check_Get_Known_SSID (NM_45)](#networkmanager_check_get_known_ssid-nm_45)
   - [NetworkManager_ActivateDeactivate_Event_Test (NM_46)](#networkmanager_activatedeactivate_event_test-nm_46)
   - [NetworkManager_GetIPSettings_With_Invalid_Parameter (NM_47)](#networkmanager_getipsettings_with_invalid_parameter-nm_47)
   - [NetworkManager_Verify_Wifi_Connect_Error (NM_48)](#networkmanager_verify_wifi_connect_error-nm_48)
   - [NetworkManager_SetInterfaceState_Without_Interface_Parameter (NM_49)](#networkmanager_setinterfacestate_without_interface_parameter-nm_49)
   - [NetworkManager_SetInterfaceState_With_Invalid_Parameters (NM_50)](#networkmanager_setinterfacestate_with_invalid_parameters-nm_50)
   - [NetworkManager_Add_and_Remove_SSID (NM_51)](#networkmanager_add_and_remove_ssid-nm_51)
   - [NetworkManager_SetStunEndpoint_With_Invalid_Endpoint (NM_52)](#networkmanager_setstunendpoint_with_invalid_endpoint-nm_52)
   - [NetworkManager_SetStunEndpoint_With_Invalid_Port (NM_53)](#networkmanager_setstunendpoint_with_invalid_port-nm_53)
   - [NetworkManager_SetStunEndpoint_Without_Endpoint (NM_54)](#networkmanager_setstunendpoint_without_endpoint-nm_54)
   - [NetworkManager_SetStunEndpoint_Without_Port (NM_55)](#networkmanager_setstunendpoint_without_port-nm_55)
   - [NetworkManager_SetStunEndpoint_Without_Parameters (NM_56)](#networkmanager_setstunendpoint_without_parameters-nm_56)
   - [NetworkManager_AddToKnownSSIDs_With_Empty_SSID (NM_57)](#networkmanager_addtoknownssids_with_empty_ssid-nm_57)
   - [NetworkManager_AddToKnownSSIDs_With_Empty_Passphrase (NM_58)](#networkmanager_addtoknownssids_with_empty_passphrase-nm_58)
   - [NetworkManager_AddToKnownSSIDs_With_Empty_SSID_Passphrase (NM_59)](#networkmanager_addtoknownssids_with_empty_ssid_passphrase-nm_59)
   - [NetworkManager_AddToKnownSSIDs_Without_Parameters (NM_60)](#networkmanager_addtoknownssids_without_parameters-nm_60)
   - [NetworkManager_SetIPSettings_With_Empty_Interface (NM_61)](#networkmanager_setipsettings_with_empty_interface-nm_61)
   - [NetworkManager_SetIPSettings_With_Invalid_Interface (NM_62)](#networkmanager_setipsettings_with_invalid_interface-nm_62)
   - [NetworkManager_SetIPSettings_With_Empty_Ipversion (NM_63)](#networkmanager_setipsettings_with_empty_ipversion-nm_63)
   - [NetworkManager_SetIPSettings_With_Invalid_Ipversion (NM_64)](#networkmanager_setipsettings_with_invalid_ipversion-nm_64)
   - [NetworkManager_SetIPSettings_With_Invalid_Ipaddress (NM_65)](#networkmanager_setipsettings_with_invalid_ipaddress-nm_65)
   - [NetworkManager_SetIPSettings_With_Invalid_Gateway (NM_66)](#networkmanager_setipsettings_with_invalid_gateway-nm_66)
   - [NetworkManager_SetIPSettings_With_Invalid_PrimaryDNS (NM_67)](#networkmanager_setipsettings_with_invalid_primarydns-nm_67)
   - [NetworkManager_SetIPSettings_With_Invalid_SecondaryDNS (NM_68)](#networkmanager_setipsettings_with_invalid_secondarydns-nm_68)
   - [NetworkManager_Check_GetAvailableInterfaces_Error (NM_69)](#networkmanager_check_getavailableinterfaces_error-nm_69)
   - [NetworkManager_Check_GetPrimaryInterface_Error (NM_70)](#networkmanager_check_getprimaryinterface_error-nm_70)
   - [NetworkManager_Check_GetPublicIP_Error (NM_71)](#networkmanager_check_getpublicip_error-nm_71)
   - [NetworkManager_Check_Ping_Error (NM_72)](#networkmanager_check_ping_error-nm_72)
   - [NetworkManager_Check_Trace_Error (NM_73)](#networkmanager_check_trace_error-nm_73)
   - [NetworkManager_Check_IsConnectedToInternet_Error (NM_74)](#networkmanager_check_isconnectedtointernet_error-nm_74)
   - [NetworkManager_Check_GetInterfaceState_Error (NM_75)](#networkmanager_check_getinterfacestate_error-nm_75)
   - [NetworkManager_Check_SetInterfaceState_Error (NM_76)](#networkmanager_check_setinterfacestate_error-nm_76)
   - [NetworkManager_Check_StopWiFiScan_Error (NM_77)](#networkmanager_check_stopwifiscan_error-nm_77)
   - [NetworkManager_Check_WiFiDisconnect_Error (NM_78)](#networkmanager_check_wifidisconnect_error-nm_78)
   - [NetworkManager_SSID_Frequency_Checker_2.4GHz (NM_79)](#networkmanager_ssid_frequency_checker_2-4ghz-nm_79)
   - [NetworkManager_SSID_Frequency_Checker_5GHz (NM_80)](#networkmanager_ssid_frequency_checker_5ghz-nm_80)
   - [NetworkManager_Scan_Specific_SSID_2.4GHz (NM_81)](#networkmanager_scan_specific_ssid_2-4ghz-nm_81)
   - [NetworkManager_Scan_Specific_SSID_5GHz (NM_82)](#networkmanager_scan_specific_ssid_5ghz-nm_82)
   - [NetworkManager_Trace_Empty_Endpoint (NM_83)](#networkmanager_trace_empty_endpoint-nm_83)
   - [NetworkManager_Trace_Without_Parameter (NM_84)](#networkmanager_trace_without_parameter-nm_84)
   - [NetworkManager_Wifi_Connect_Without_Parameter (NM_85)](#networkmanager_wifi_connect_without_parameter-nm_85)
   - [NetworkManager_Get_Public_IPv6_IP (NM_86)](#networkmanager_get_public_ipv6_ip-nm_86)
   - [NetworkManager_Check_Internet_IPv6_Connectivity (NM_87)](#networkmanager_check_internet_ipv6_connectivity-nm_87)
   - [NetworkManager_Get_IPSettings_IPv6 (NM_88)](#networkmanager_get_ipsettings_ipv6-nm_88)
   - [NetworkManager_Check_Primary_Interface_After_LightSleep (NM_89)](#networkmanager_check_primary_interface_after_lightsleep-nm_89)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **NetworkManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.NetworkManager` (version 1)

**API Coverage**

- **State / Query APIs**: `GetAvailableInterfaces`, `GetConnectedSSID`, `GetConnectivityTestEndpoints`, `GetIPSettings`, `GetInterfaceState`, `GetKnownSSIDs`, `GetLogLevel`, `GetPrimaryInterface`, `GetPublicIP`, `GetStunEndpoint`, `GetSupportedSecurityModes`, `GetWifiState`, `IsConnectedToInternet`
- **Lifecycle / Control APIs**: `StartConnectivityMonitoring`, `StartWiFiScan`, `StopConnectivityMonitoring`, `StopWiFiScan`
- **Configuration APIs**: `AddToKnownSSIDs`, `RemoveKnownSSID`, `SetConnectivityTestEndpoints`, `SetIPSettings`, `SetInterfaceState`, `SetLogLevel`, `SetPrimaryInterface`, `SetStunEndpoint`
- **Events**: `onAvailableSSIDs`, `onInterfaceStateChange`, `onWiFiStateChange`
- **Other APIs**: `Ping`, `Trace`, `WiFiConnect`, `WiFiDisconnect`

### APIs Under Test

| API | Description |
|-----|-------------|
| `AddToKnownSSIDs` | Saves the SSID, passphrase, and security mode for upcoming and future sessions |
| `GetAvailableInterfaces` | Get device supported list of available interface including their state |
| `GetConnectedSSID` | Returns the connected SSID information |
| `GetConnectivityTestEndpoints` | Gets currently used test endpoints |
| `GetIPSettings` | Gets the IP setting for the given interface |
| `GetInterfaceState` | Gets the current Status of the specified interface |
| `GetKnownSSIDs` | Gets list of saved SSIDs. This method returns all the SSIDs that are saved as array |
| `GetLogLevel` | Returns the currently set logging level |
| `GetPrimaryInterface` | Gets the primary/default network interface for the device |
| `GetPublicIP` | Gets the public IP Address of the device |
| `GetStunEndpoint` | Get the STUN endpoint that is used to identify public IP of the device |
| `GetSupportedSecurityModes` | Returns the wifi security modes that the device supports |
| `GetWifiState` | Returns the current Wifi State |
| `IsConnectedToInternet` | Seeks whether the device has internet connectivity. This API might take up to 3s to validate internet connectivity |
| `Ping` | Pings the specified endpoint with the specified number of packets |
| `RemoveKnownSSID` | Remove given SSID from saved SSIDs list |
| `SetConnectivityTestEndpoints` | sets the list of endpoints |
| `SetIPSettings` | Sets the IP settings for the given interface |
| `SetInterfaceState` | Enable or disable the specified interface |
| `SetLogLevel` | Sets the logging level |
| `SetPrimaryInterface` | Sets the primary/default interface for the device |
| `SetStunEndpoint` | Set the STUN endpoint to be used to identify public IP of the device |
| `StartConnectivityMonitoring` | Enable a continuous monitoring of internet connectivity with heart beat interval thats given |
| `StartWiFiScan` | Initiates WiFi scanning |
| `StopConnectivityMonitoring` | Stops the connectivity monitoring |
| `StopWiFiScan` | Stops WiFi scanning |
| `Trace` | Traces the specified endpoint with the specified number of packets using traceroute |
| `WiFiConnect` | Initiates request to connect to the specified SSID with the given passphrase |
| `WiFiDisconnect` | Disconnects from the currently connected SSID |

### Events Under Test

| Event | Description |
|-------|-------------|
| `onAvailableSSIDs` | Triggered when scan completes or when scan cancelled |
| `onInterfaceStateChange` | Triggered when an interface state is changed |
| `onWiFiStateChange` | Triggered when WIFI connection state get changed |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_On_Interface_StateChange` on `NetworkManager` plugin

- Register and listen to event `Event_On_AvailableSSIDs` on `NetworkManager` plugin

- Register and listen to event `Event_On_WiFiStateChange` on `NetworkManager` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

---

## Test Cases

<a id="networkmanager_get_device_interfaces-nm_01"></a>
### NetworkManager_Get_Device_Interfaces (NM_01)

**Objective:** Gets list of interfaces supported by device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Interfaces | Invoke `GetAvailableInterfaces` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | Available Interfaces returned successfully |

---

<a id="networkmanager_get_primary-default_interface-nm_02"></a>
### NetworkManager_Get_Primary/Default_Interface (NM_02)

**Objective:** Gets primary/default interface of the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Interfaces | Invoke `GetAvailableInterfaces` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | Available Interfaces returned successfully |
| 2 | Get Primary/Default Interface | Invoke `GetPrimaryInterface` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPrimaryInterface"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` returned `interface` is one of the values retrieved in step 1 |

---

<a id="networkmanager_validate_public_ipv4_ip-nm_03"></a>
### NetworkManager_Validate_Public_IPv4_IP (NM_03)

**Objective:** Validate public IPv4 IP address of the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Public IP Address | Execute command on the device `curl -s ifconfig.me` | Public IP address string returned successfully |
| 2 | Get Public IPv4 IP | Invoke `GetPublicIP` on `org.rdk.NetworkManager` with `ipversion`: `"IPv4"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPublicIP", "params": {"ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` public ip matches value from step 1 |

---

<a id="networkmanager_ping_ipv4_endpoint-nm_04"></a>
### NetworkManager_Ping_IPv4_Endpoint (NM_04)

**Objective:** Pings the specified end point

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Ping Endpoint | Invoke `Ping` on `org.rdk.NetworkManager` with `endpoint`: `"<PING_IP>"`, `ipversion`: `"IPv4"`, `count`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Ping", "params": {"endpoint": "<PING_IP>", "ipversion": "IPv4", "count": 10}}' http://127.0.0.1:9998/jsonrpc` | Expected `<PING_IP> and 10` |

---

<a id="networkmanager_trace_ipv4_endpoint-nm_05"></a>
### NetworkManager_Trace_IPv4_Endpoint (NM_05)

**Objective:** Traces the specified end point

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Trace Endpoint | Invoke `Trace` on `org.rdk.NetworkManager` with `endpoint`: `"<TRACE_IP>"`, `ipversion`: `"IPv4"`, `packets`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Trace", "params": {"endpoint": "<TRACE_IP>", "ipversion": "IPv4", "packets": 10}}' http://127.0.0.1:9998/jsonrpc` | Expected `<TRACE_IP>` |

---

<a id="networkmanager_check_internet_ipv4_connectivity-nm_06"></a>
### NetworkManager_Check_Internet_IPv4_Connectivity (NM_06)

**Objective:** Seeks whether the device has internet connectivity

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Internet IPv4 Connectivity | Invoke `IsConnectedToInternet` on `org.rdk.NetworkManager` with `ipversion`: `"IPv4"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": {"ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | Expected `true` |

---

<a id="networkmanager_getavailableinterfaces_with_enabled-disabled_interface-nm_07"></a>
### NetworkManager_GetAvailableInterfaces_With_Enabled/Disabled_Interface (NM_07)

**Objective:** Verify that the GetAvailableInterfaces method returns the correct list of available interfaces when interface is enabled or disabled

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"`, `enabled`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>", "enabled": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state matches toggled value from step 1 |
| 4 | Get Device Interfaces | Invoke `GetAvailableInterfaces` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state matches toggled value from step 1 |

---

<a id="networkmanager_check_on_interface_statechange_event-nm_08"></a>
### NetworkManager_Check_On_Interface_StateChange_Event (NM_08)

**Objective:** Check if the event is triggered upon a change in the interface state

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"`, `enabled`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>", "enabled": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Check On Interface StateChange Event | Listen for `Event_On_Interface_StateChange` event (wait 5s) | `onInterfaceStateChange` event received; interface state change validated |
| 4 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state matches toggled value from step 1 |

---

<a id="networkmanager_wifi_start_stop_scan-nm_09"></a>
### NetworkManager_Wifi_Start_Stop_Scan (NM_09)

**Objective:** Check if the start and stop wifi scan methods can successfully initiate and stop the wifi scanning process

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |

---

<a id="networkmanager_check_on_availablessids_event-nm_10"></a>
### NetworkManager_Check_On_AvailableSSIDs_Event (NM_10)

**Objective:** Check if the event is triggered when initiating a wifi scan

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |

---

<a id="networkmanager_get_interface_state-nm_11"></a>
### NetworkManager_Get_Interface_State (NM_11)

**Objective:** Ensure that the GetInterfaceState method successfully returns the state when provided with a valid network interface

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_INTERFACE_DETAILS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_INTERFACE_DETAILS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |

---

<a id="networkmanager_setandget_interface_state-nm_12"></a>
### NetworkManager_SetandGet_Interface_State (NM_12)

**Objective:** Check GetInterfaceState method returns the correct interface state after using the SetInterfaceState method

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"`, `enabled`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>", "enabled": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state matches toggled value from step 1 |

---

<a id="networkmanager_wifi_connect_disconnect-nm_13"></a>
### NetworkManager_Wifi_Connect_Disconnect (NM_13)

**Objective:** Check if the connect and disconnect wifi methods can successfully establish and terminate the wifi connection

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`, `passphrase`: `"<WIFI_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi connected successfully |
| 5 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

---

<a id="networkmanager_check_get_connected_ssid-nm_14"></a>
### NetworkManager_Check_Get_Connected_SSID (NM_14)

**Objective:** Ensure that the GetConnectedSSID method successfully returns the correct SSID information when all parameters are valid

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`, `passphrase`: `"<WIFI_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi connected successfully |
| 5 | Check Get Connected SSID | Invoke `GetConnectedSSID` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` connected SSID returned |
| 6 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

---

<a id="networkmanager_get_supported_security_modes-nm_15"></a>
### NetworkManager_Get_Supported_Security_Modes (NM_15)

**Objective:** Returns the Wifi security modes that the device supports

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Supported Security Modes | Invoke `GetSupportedSecurityModes` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetSupportedSecurityModes"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` non-empty list of supported WiFi security modes returned |

---

<a id="networkmanager_check_on_wifistatechange_event-nm_16"></a>
### NetworkManager_Check_On_WifiStateChange_Event (NM_16)

**Objective:** Check whether the wifistatechange event is triggered upon connecting to and disconnecting from wifi

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`, `passphrase`: `"<WIFI_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi connected successfully |
| 5 | Check On WiFiStateChange Event | Listen for `Event_On_WiFiStateChange` event (wait 10s) | `success`: `true` `state`: `5`, `status`: `WIFI_STATE_CONNECTED` |
| 6 | Check Get Connected SSID | Invoke `GetConnectedSSID` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` connected SSID returned |
| 7 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |
| 8 | Check On WiFiStateChange Event | Listen for `Event_On_WiFiStateChange` event (wait 10s) | `success`: `true` `state`: `2`, `status`: `WIFI_STATE_DISCONNECTED` |

---

<a id="networkmanager_check_wificonnect_with_invalid_ssid_passphrase-nm_17"></a>
### NetworkManager_Check_WifiConnect_With_Invalid_SSID_Passphrase (NM_17)

**Objective:** Check if the wifi connect method fails when provided with an invalid SSID and passphrase

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_INVALID_SSID_NAME>"`, `passphrase`: `"<WIFI_INVALID_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_INVALID_SSID_NAME>", "passphrase": "<WIFI_INVALID_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_check_on_availablessids_event_not_triggered-nm_18"></a>
### NetworkManager_Check_On_AvailableSSIDs_Event_Not_Triggered (NM_18)

**Objective:** Check if the onAvailableSSID event is triggered after stopping the wifi scan

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | Event received and validated |

---

<a id="networkmanager_setandget_stun_endpoint-nm_19"></a>
### NetworkManager_SetandGet_Stun_Endpoint (NM_19)

**Objective:** Check GetStunEndpoint method returns the correct endpoint after using the SetStunEndpoint method

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Stun Endpoint | Invoke `GetStunEndpoint` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetStunEndpoint"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `endpoint` and `port` returned |
| 2 | Set Stun Endpoint | Invoke `SetStunEndpoint` on `org.rdk.NetworkManager` with `endpoint`: `"<result_step_1>"`, `port`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"endpoint": "<result_step_1>", "port": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Stun Endpoint set successfully |
| 3 | Get Stun Endpoint | Invoke `GetStunEndpoint` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetStunEndpoint"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `endpoint` and `port` match values from step 1 |

---

<a id="networkmanager_5ghz_wifi_connect_disconnect-nm_20"></a>
### NetworkManager_5GHz_Wifi_Connect_Disconnect (NM_20)

**Objective:** Check if the connect and disconnect wifi methods can successfully establish and terminate the 5GHz wifi connection

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME_5GHZ>"`, `passphrase`: `"<WIFI_PASSPHRASE_5GHZ>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME_5GHZ>", "passphrase": "<WIFI_PASSPHRASE_5GHZ>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi connected successfully |
| 5 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

---

<a id="networkmanager_check_5ghz_get_connected_ssid-nm_21"></a>
### NetworkManager_Check_5GHz_Get_Connected_SSID (NM_21)

**Objective:** Ensure that the GetConnectedSSID method successfully returns the correct 5Ghz SSID information when all parameters are valid

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME_5GHZ>"`, `passphrase`: `"<WIFI_PASSPHRASE_5GHZ>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME_5GHZ>", "passphrase": "<WIFI_PASSPHRASE_5GHZ>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi connected successfully |
| 5 | Check Get Connected SSID | Invoke `GetConnectedSSID` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` connected SSID returned |
| 6 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

---

<a id="networkmanager_setinterfacestate_without_enable_parameter-nm_22"></a>
### NetworkManager_SetInterfaceState_Without_Enable_Parameter (NM_22)

**Objective:** Check if the SetInterfaceState method returns an error when enabled parameter is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetInterfaceState Without Enable Parameter | Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"eth0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "eth0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setinterfacestate_without_parameter-nm_23"></a>
### NetworkManager_SetInterfaceState_Without_Parameter (NM_23)

**Objective:** Check if the SetInterfaceState method returns an error when parameter is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetInterfaceState Without Parameter | Invoke `SetInterfaceState` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_getinterfacestate_with_invalid_parameter-nm_24"></a>
### NetworkManager_GetInterfaceState_With_Invalid_Parameter (NM_24)

**Objective:** Check if the GetInterfaceState method returns an error when invalid parameter is provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetInterfaceState With Invalid Parameter | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"Invalid"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "Invalid"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_check_logging_level-nm_25"></a>
### NetworkManager_Check_Logging_Level (NM_25)

**Objective:** Checks whether able to set and get various logging level

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Log Level | Invoke `GetLogLevel` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` current log level returned |
| 2 | Set Log Level | Invoke `SetLogLevel` on `org.rdk.NetworkManager` with `level`: each of `0`, `1`, `2`, `3`, `4`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetLogLevel", "params": {"level": "<LEVEL_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Log Level set successfully |
| 3 | Get Log Level | Invoke `GetLogLevel` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` returned value matches the iterated value set in the previous step |

---

<a id="networkmanager_set_lowest_logging_level-nm_26"></a>
### NetworkManager_Set_Lowest_Logging_Level (NM_26)

**Objective:** Check if able to set and get the lowest logging level

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Log Level | Invoke `GetLogLevel` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` current log level returned |
| 2 | Set Log Level | Invoke `SetLogLevel` on `org.rdk.NetworkManager` with `level`: `0`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetLogLevel", "params": {"level": 0}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Log Level set successfully |
| 3 | Get Log Level | Invoke `GetLogLevel` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `level`: `0` |

---

<a id="networkmanager_set_mid-range_logging_level-nm_27"></a>
### NetworkManager_Set_Mid-range_Logging_Level (NM_27)

**Objective:** Check if able to set and get the mid-range logging level

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Log Level | Invoke `GetLogLevel` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` current log level returned |
| 2 | Set Log Level | Invoke `SetLogLevel` on `org.rdk.NetworkManager` with `level`: `2`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetLogLevel", "params": {"level": 2}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Log Level set successfully |
| 3 | Get Log Level | Invoke `GetLogLevel` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `level`: `2` |

---

<a id="networkmanager_set_highest_logging_level-nm_28"></a>
### NetworkManager_Set_Highest_Logging_Level (NM_28)

**Objective:** Check if able to set and get the highest logging level

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Log Level | Invoke `GetLogLevel` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` current log level returned |
| 2 | Set Log Level | Invoke `SetLogLevel` on `org.rdk.NetworkManager` with `level`: `4`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetLogLevel", "params": {"level": 4}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Log Level set successfully |
| 3 | Get Log Level | Invoke `GetLogLevel` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `level`: `4` |

---

<a id="networkmanager_check_wifi_state-nm_29"></a>
### NetworkManager_Check_Wifi_State (NM_29)

**Objective:** Returns the current Wifi State

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Wifi State | Invoke `GetWifiState` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | WiFi State returned successfully |

---

<a id="networkmanager_connect_wifi_and_check_wifi_state-nm_30"></a>
### NetworkManager_Connect_Wifi_And_Check_Wifi_State (NM_30)

**Objective:** Check the wifi state on connecting/disconnecting to the wifi ssid

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`, `passphrase`: `"<WIFI_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi connected successfully |
| 5 | Check Get Connected SSID | Invoke `GetConnectedSSID` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` connected SSID returned |
| 6 | Check Wifi State | Invoke `GetWifiState` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `state`: `5`, `status`: `WIFI_STATE_CONNECTED` |
| 7 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |
| 8 | Check Wifi State | Invoke `GetWifiState` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `state`: `2`, `status`: `WIFI_STATE_DISCONNECTED` |

---

<a id="networkmanager_set_single_connectivity_test_endpoints-nm_31"></a>
### NetworkManager_Set_Single_Connectivity_Test_Endpoints (NM_31)

**Objective:** Check if able to set the valid single test endpoint

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Connectivity Endpoints | Invoke `SetConnectivityTestEndpoints` on `org.rdk.NetworkManager` with `endpoints`: `"<CONNECTIVITY_TEST_ENDPOINTS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetConnectivityTestEndpoints", "params": {"endpoints": "<CONNECTIVITY_TEST_ENDPOINTS>"}}' http://127.0.0.1:9998/jsonrpc` | Connectivity Test Endpoints set successfully |

---

<a id="networkmanager_set_five_connectivity_test_endpoints-nm_32"></a>
### NetworkManager_Set_Five_Connectivity_Test_Endpoints (NM_32)

**Objective:** Check if able to set upto 5 endpoints

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Connectivity Endpoints | Invoke `SetConnectivityTestEndpoints` on `org.rdk.NetworkManager` with `endpoints`: `"<NETWORKMANAGER_MAX_CONNECTIVITY_TEST_ENDPOINTS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetConnectivityTestEndpoints", "params": {"endpoints": "<NETWORKMANAGER_MAX_CONNECTIVITY_TEST_ENDPOINTS>"}}' http://127.0.0.1:9998/jsonrpc` | Connectivity Test Endpoints set successfully |

---

<a id="networkmanager_check_wifi_state_after_connecting_to_wifi-nm_33"></a>
### NetworkManager_Check_Wifi_State_After_Connecting_To_Wifi (NM_33)

**Objective:** Check the wifi state after connecting to the wifi ssid

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`, `passphrase`: `"<WIFI_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi connected successfully |
| 5 | Check Wifi State | Invoke `GetWifiState` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `state`: `5`, `status`: `WIFI_STATE_CONNECTED` |
| 6 | Check Get Connected SSID | Invoke `GetConnectedSSID` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` connected SSID returned |
| 7 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

---

<a id="networkmanager_start_scan_and_check_wifi_state-nm_34"></a>
### NetworkManager_Start_Scan_And_Check_Wifi_State (NM_34)

**Objective:** Check the wifi state on scanning for the wifi

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Check Wifi State | Invoke `GetWifiState` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `state`: `2`, `status`: `WIFI_STATE_DISCONNECTED` |
| 4 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |

---

<a id="networkmanager_check_wifi_state_on_connecting_to_invalid_wifi_ssid-nm_35"></a>
### NetworkManager_Check_Wifi_State_On_Connecting_To_Invalid_Wifi_SSID (NM_35)

**Objective:** Check the wifi state on connecting to the invalid wifi ssid

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_INVALID_SSID_NAME>"`, `passphrase`: `"<WIFI_INVALID_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 2 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_INVALID_SSID_NAME>", "passphrase": "<WIFI_INVALID_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |
| 5 | Check Wifi State | Invoke `GetWifiState` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `state`: `2`, `status`: `WIFI_STATE_DISCONNECTED` |

---

<a id="networkmanager_setandget_connectivity_test_endpoints-nm_36"></a>
### NetworkManager_SetandGet_Connectivity_Test_Endpoints (NM_36)

**Objective:** Check GetConnectivityTestEndpoints method returns the correct test endpoint set using the SetConnectivityTestEndpoints method

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Connectivity Test Endpoints | Invoke `GetConnectivityTestEndpoints` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectivityTestEndpoints"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` connectivity test endpoints returned |
| 2 | Set Connectivity Endpoints | Invoke `SetConnectivityTestEndpoints` on `org.rdk.NetworkManager` with `endpoints`: `"<CONNECTIVITY_TEST_ENDPOINTS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetConnectivityTestEndpoints", "params": {"endpoints": "<CONNECTIVITY_TEST_ENDPOINTS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Connectivity Test Endpoints set successfully |
| 3 | Get Connectivity Test Endpoints | Invoke `GetConnectivityTestEndpoints` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectivityTestEndpoints"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` connectivity test endpoints returned |

---

<a id="networkmanager_check_wifi_statechange_event_on_connecting_to_wifi-nm_37"></a>
### NetworkManager_Check_WiFi_StateChange_Event_On_Connecting_To_Wifi (NM_37)

**Objective:** Check the wifi state change event on connecting to the wifi ssid

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`, `passphrase`: `"<WIFI_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi connected successfully |
| 5 | Check On WiFiStateChange Event | Listen for `Event_On_WiFiStateChange` event (wait 10s) | `success`: `true` `state`: `4`, `status`: `WIFI_STATE_CONNECTING` |
| 6 | Check Get Connected SSID | Invoke `GetConnectedSSID` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` connected SSID returned |
| 7 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

---

<a id="networkmanager_set_invalid_interface_state-nm_38"></a>
### NetworkManager_Set_Invalid_Interface_State (NM_38)

**Objective:** check if the SetInterfaceState method returns error on setting the invalid interface name

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Interface State | Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"invalid"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "invalid", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_getinterfacestate_with_empty_parameter-nm_39"></a>
### NetworkManager_GetInterfaceState_With_Empty_Parameter (NM_39)

**Objective:** Check if the GetInterfaceState method returns an error when empty parameter is provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetInterfaceState With Empty Parameter | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": ""}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_ping_invalid_endpoint-nm_40"></a>
### NetworkManager_Ping_Invalid_Endpoint (NM_40)

**Objective:** Pings the invalid endpoint

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Ping Host | Invoke `Ping` on `org.rdk.NetworkManager` with `endpoint`: `"<NETWORKMANAGER_INVALID_ENDPOINT>"`, `ipversion`: `"IPv4"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Ping", "params": {"endpoint": "<NETWORKMANAGER_INVALID_ENDPOINT>", "ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | Expected `<NETWORKMANAGER_INVALID_ENDPOINT> (could not ping endpoint)` |

---

<a id="networkmanager_ping_endpoint_with_invalid_ipversion-nm_41"></a>
### NetworkManager_Ping_Endpoint_With_Invalid_IPVersion (NM_41)

**Objective:** Pings the endpoint with invalid ipversion

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Ping Host | Invoke `Ping` on `org.rdk.NetworkManager` with `endpoint`: `"<PING_IP>"`, `ipversion`: `"invalid"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Ping", "params": {"endpoint": "<PING_IP>", "ipversion": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | Expected `Could not access requested service` |

---

<a id="networkmanager_remove_invalid_ssid-nm_42"></a>
### NetworkManager_Remove_Invalid_SSID (NM_42)

**Objective:** Check if RemoveKnownSSID method returns an error when parameter is provided with invalid ssid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Remove Known SSID | Invoke `RemoveKnownSSID` on `org.rdk.NetworkManager` with `ssid`: `"invalid"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.RemoveKnownSSID", "params": {"ssid": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_remove_empty_ssid-nm_43"></a>
### NetworkManager_Remove_Empty_SSID (NM_43)

**Objective:** Check if RemoveKnownSSID method returns an error when parameter is provided with empty ssid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Remove Known SSID | Invoke `RemoveKnownSSID` on `org.rdk.NetworkManager` with `ssid`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.RemoveKnownSSID", "params": {"ssid": ""}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Known SSID unregistered successfully |

---

<a id="networkmanager_getinterfacestate_without_parameter-nm_44"></a>
### NetworkManager_GetInterfaceState_Without_Parameter (NM_44)

**Objective:** Check if the GetInterfaceState method returns an error when interface parameter is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetInterfaceState Without Parameter | Invoke `GetInterfaceState` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_check_get_known_ssid-nm_45"></a>
### NetworkManager_Check_Get_Known_SSID (NM_45)

**Objective:** Check if the GetKnownSSIDs method returns the connected SSID name

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |
| 4 | Wifi Connect | Invoke `WiFiConnect` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`, `passphrase`: `"<WIFI_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi connected successfully |
| 5 | Check Get Connected SSID | Invoke `GetConnectedSSID` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` connected SSID returned |
| 6 | Check Get Known SSID | Invoke `GetKnownSSIDs` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` known SSIDs list returned |
| 7 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

---

<a id="networkmanager_activatedeactivate_event_test-nm_46"></a>
### NetworkManager_ActivateDeactivate_Event_Test (NM_46)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Network Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `org.rdk.networkmanager`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate Network Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `org.rdk.networkmanager`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="networkmanager_getipsettings_with_invalid_parameter-nm_47"></a>
### NetworkManager_GetIPSettings_With_Invalid_Parameter (NM_47)

**Objective:** Check if the GetIPSettings method returns an error when invalid interface parameter is provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetIPSettings With Invalid Parameter | Invoke `GetIPSettings` on `org.rdk.NetworkManager` with `interface`: `"invalid"`, `ipversion`: `"IPv4"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetIPSettings", "params": {"interface": "invalid", "ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_verify_wifi_connect_error-nm_48"></a>
### NetworkManager_Verify_Wifi_Connect_Error (NM_48)

**Objective:** Verify that the WifiConnect method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate NetworkManager Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `org.rdk.networkmanager`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check NetworkManager Wifi Connect API Response | Invoke `WiFiConnect` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate NetworkManager Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `org.rdk.networkmanager`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="networkmanager_setinterfacestate_without_interface_parameter-nm_49"></a>
### NetworkManager_SetInterfaceState_Without_Interface_Parameter (NM_49)

**Objective:** Check if the SetInterfaceState method returns an error when interface parameter is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetInterfaceState Without Interface Parameter | Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setinterfacestate_with_invalid_parameters-nm_50"></a>
### NetworkManager_SetInterfaceState_With_Invalid_Parameters (NM_50)

**Objective:** Check if the SetInterfaceState method returns an error when both interface and enabled parameters are provided with invalid values

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetInterfaceState With Invalid Parameters | Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"invalid"`, `enabled`: `"invalid"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "invalid", "enabled": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_add_and_remove_ssid-nm_51"></a>
### NetworkManager_Add_and_Remove_SSID (NM_51)

**Objective:** Check that an SSID can be added and then removed successfully

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Known SSID List | Invoke `GetKnownSSIDs` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | Known SSIDs returned successfully |
| 2 | Remove Known SSID | *(Conditional: executed only if previous step condition is met)*<br>Invoke `RemoveKnownSSID` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.RemoveKnownSSID", "params": {"ssid": "<WIFI_SSID_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Known SSID unregistered successfully |
| 3 | Get Known SSID List | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetKnownSSIDs` on `org.rdk.NetworkManager` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | Known SSIDs returned successfully |
| 4 | Add to Known SSID | Invoke `AddToKnownSSIDs` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`, `passphrase`: `"<WIFI_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` To Known SSIDs registered successfully |
| 5 | Get Known SSID List | Invoke `GetKnownSSIDs` on `org.rdk.NetworkManager` (wait 2 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` known SSIDs list returned |
| 6 | Remove Known SSID | Invoke `RemoveKnownSSID` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.RemoveKnownSSID", "params": {"ssid": "<WIFI_SSID_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Known SSID unregistered successfully |
| 7 | Get Known SSID List | Invoke `GetKnownSSIDs` on `org.rdk.NetworkManager` (wait 2 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | Known SSIDs returned successfully |

---

<a id="networkmanager_setstunendpoint_with_invalid_endpoint-nm_52"></a>
### NetworkManager_SetStunEndpoint_With_Invalid_Endpoint (NM_52)

**Objective:** Check if the SetStunEndpoint method throws an error when an invalid endpoint parameter is passed

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetStunEndpoint With Invalid Endpoint | Invoke `SetStunEndpoint` on `org.rdk.NetworkManager` with `endpoint`: `"<NETWORKMANAGER_INVALID_ENDPOINT>"`, `port`: `"<NETWORKMANAGER_TEST_PORT>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"endpoint": "<NETWORKMANAGER_INVALID_ENDPOINT>", "port": "<NETWORKMANAGER_TEST_PORT>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setstunendpoint_with_invalid_port-nm_53"></a>
### NetworkManager_SetStunEndpoint_With_Invalid_Port (NM_53)

**Objective:** Check if the SetStunEndpoint method throws an error when an invalid port parameter is passed

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetStunEndpoint With Invalid Port | Invoke `SetStunEndpoint` on `org.rdk.NetworkManager` with `endpoint`: `"<NETWORKMANAGER_TEST_IPADDRESS>"`, `port`: `"<NETWORKMANAGER_INVALID_PORT>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"endpoint": "<NETWORKMANAGER_TEST_IPADDRESS>", "port": "<NETWORKMANAGER_INVALID_PORT>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setstunendpoint_without_endpoint-nm_54"></a>
### NetworkManager_SetStunEndpoint_Without_Endpoint (NM_54)

**Objective:** Check if the SetStunEndpoint method throws an error when endpoint parameter is not passed

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetStunEndpoint Without Endpoint | Invoke `SetStunEndpoint` on `org.rdk.NetworkManager` with `port`: `"<NETWORKMANAGER_TEST_PORT>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"port": "<NETWORKMANAGER_TEST_PORT>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setstunendpoint_without_port-nm_55"></a>
### NetworkManager_SetStunEndpoint_Without_Port (NM_55)

**Objective:** Check if the SetStunEndpoint method throws an error when port parameter is not passed

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetStunEndpoint Without Port | Invoke `SetStunEndpoint` on `org.rdk.NetworkManager` with `endpoint`: `"<NETWORKMANAGER_TEST_IPADDRESS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"endpoint": "<NETWORKMANAGER_TEST_IPADDRESS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setstunendpoint_without_parameters-nm_56"></a>
### NetworkManager_SetStunEndpoint_Without_Parameters (NM_56)

**Objective:** Check if the SetStunEndpoint method throws an error when parameters are not passed

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetStunEndpoint Without Parameters | Invoke `SetStunEndpoint` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_addtoknownssids_with_empty_ssid-nm_57"></a>
### NetworkManager_AddToKnownSSIDs_With_Empty_SSID (NM_57)

**Objective:** Check if the AddToKnownSSIDs method returns an error when the SSID parameter is empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | AddToKnownSSIDs With Empty SSID | Invoke `AddToKnownSSIDs` on `org.rdk.NetworkManager` with `ssid`: `""`, `passphrase`: `"<WIFI_PASSPHRASE>"`, `security`: `"<WIFI_SECURITY_MODE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs", "params": {"ssid": "", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_addtoknownssids_with_empty_passphrase-nm_58"></a>
### NetworkManager_AddToKnownSSIDs_With_Empty_Passphrase (NM_58)

**Objective:** Check if the AddToKnownSSIDs method returns an error when the passphrase parameter is empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | AddToKnownSSIDs With Empty Passphrase | Invoke `AddToKnownSSIDs` on `org.rdk.NetworkManager` with `ssid`: `"<WIFI_SSID_NAME>"`, `passphrase`: `""`, `security`: `"<WIFI_SECURITY_MODE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_addtoknownssids_with_empty_ssid_passphrase-nm_59"></a>
### NetworkManager_AddToKnownSSIDs_With_Empty_SSID_Passphrase (NM_59)

**Objective:** Check if the AddToKnownSSIDs method returns an error when the SSID and passphrase parameters are empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | AddToKnownSSIDs With Empty SSID Passphrase | Invoke `AddToKnownSSIDs` on `org.rdk.NetworkManager` with `ssid`: `""`, `passphrase`: `""`, `security`: `"<WIFI_SECURITY_MODE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs", "params": {"ssid": "", "passphrase": "", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_addtoknownssids_without_parameters-nm_60"></a>
### NetworkManager_AddToKnownSSIDs_Without_Parameters (NM_60)

**Objective:** Check if the AddToKnownSSIDs method returns an error when parameters are not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | AddToKnownSSIDs Without Parameters | Invoke `AddToKnownSSIDs` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setipsettings_with_empty_interface-nm_61"></a>
### NetworkManager_SetIPSettings_With_Empty_Interface (NM_61)

**Objective:** Check if the SetIPSettings method returns an error when the interface parameter is empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetIPSettings With Empty Interface | Invoke `SetIPSettings` on `org.rdk.NetworkManager` with `interface`: `""`, `ipversion`: `"<NETWORKMANAGER_TEST_IPVERSION>"`, `autoconfig`: `"<NETWORKMANAGER_TEST_AUTOCONFIG>"`, `ipaddress`: `"<NETWORKMANAGER_TEST_IPADDRESS>"`, `prefix`: `"<NETWORKMANAGER_TEST_PREFIX>"`, `gateway`: `"<NETWORKMANAGER_TEST_GATEWAY>"`, `primarydns`: `"<NETWORKMANAGER_TEST_PRIMARY_DNS>"`, `secondarydns`: `"<NETWORKMANAGER_TEST_SECONDARY_DNS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setipsettings_with_invalid_interface-nm_62"></a>
### NetworkManager_SetIPSettings_With_Invalid_Interface (NM_62)

**Objective:** Check if the SetIPSettings method returns an error when the interface parameter is invalid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetIPSettings With Invalid Interface | Invoke `SetIPSettings` on `org.rdk.NetworkManager` with `interface`: `"invalid"`, `ipversion`: `"<NETWORKMANAGER_TEST_IPVERSION>"`, `autoconfig`: `"<NETWORKMANAGER_TEST_AUTOCONFIG>"`, `ipaddress`: `"<NETWORKMANAGER_TEST_IPADDRESS>"`, `prefix`: `"<NETWORKMANAGER_TEST_PREFIX>"`, `gateway`: `"<NETWORKMANAGER_TEST_GATEWAY>"`, `primarydns`: `"<NETWORKMANAGER_TEST_PRIMARY_DNS>"`, `secondarydns`: `"<NETWORKMANAGER_TEST_SECONDARY_DNS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "invalid", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setipsettings_with_empty_ipversion-nm_63"></a>
### NetworkManager_SetIPSettings_With_Empty_Ipversion (NM_63)

**Objective:** Check if the SetIPSettings method returns an error when the ipversion parameter is empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetIPSettings With Empty Ipversion | Invoke `SetIPSettings` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_TEST_INTERFACE>"`, `ipversion`: `""`, `autoconfig`: `"<NETWORKMANAGER_TEST_AUTOCONFIG>"`, `ipaddress`: `"<NETWORKMANAGER_TEST_IPADDRESS>"`, `prefix`: `"<NETWORKMANAGER_TEST_PREFIX>"`, `gateway`: `"<NETWORKMANAGER_TEST_GATEWAY>"`, `primarydns`: `"<NETWORKMANAGER_TEST_PRIMARY_DNS>"`, `secondarydns`: `"<NETWORKMANAGER_TEST_SECONDARY_DNS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setipsettings_with_invalid_ipversion-nm_64"></a>
### NetworkManager_SetIPSettings_With_Invalid_Ipversion (NM_64)

**Objective:** Check if the SetIPSettings method returns an error when the ipversion parameter is invalid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetIPSettings With Invalid Ipversion | Invoke `SetIPSettings` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_TEST_INTERFACE>"`, `ipversion`: `"invalid"`, `autoconfig`: `"<NETWORKMANAGER_TEST_AUTOCONFIG>"`, `ipaddress`: `"<NETWORKMANAGER_TEST_IPADDRESS>"`, `prefix`: `"<NETWORKMANAGER_TEST_PREFIX>"`, `gateway`: `"<NETWORKMANAGER_TEST_GATEWAY>"`, `primarydns`: `"<NETWORKMANAGER_TEST_PRIMARY_DNS>"`, `secondarydns`: `"<NETWORKMANAGER_TEST_SECONDARY_DNS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "invalid", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setipsettings_with_invalid_ipaddress-nm_65"></a>
### NetworkManager_SetIPSettings_With_Invalid_Ipaddress (NM_65)

**Objective:** Check if the SetIPSettings method returns an error when the ipaddress parameter is invalid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetIPSettings With Invalid Ipaddress | Invoke `SetIPSettings` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_TEST_INTERFACE>"`, `ipversion`: `"<NETWORKMANAGER_TEST_IPVERSION>"`, `autoconfig`: `"<NETWORKMANAGER_TEST_AUTOCONFIG>"`, `ipaddress`: `"<NETWORKMANAGER_INVALID_ENDPOINT>"`, `prefix`: `"<NETWORKMANAGER_TEST_PREFIX>"`, `gateway`: `"<NETWORKMANAGER_TEST_GATEWAY>"`, `primarydns`: `"<NETWORKMANAGER_TEST_PRIMARY_DNS>"`, `secondarydns`: `"<NETWORKMANAGER_TEST_SECONDARY_DNS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_INVALID_ENDPOINT>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setipsettings_with_invalid_gateway-nm_66"></a>
### NetworkManager_SetIPSettings_With_Invalid_Gateway (NM_66)

**Objective:** Check if the SetIPSettings method returns an error when the gateway parameter is invalid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetIPSettings With Invalid Gateway | Invoke `SetIPSettings` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_TEST_INTERFACE>"`, `ipversion`: `"<NETWORKMANAGER_TEST_IPVERSION>"`, `autoconfig`: `"<NETWORKMANAGER_TEST_AUTOCONFIG>"`, `ipaddress`: `"<NETWORKMANAGER_TEST_IPADDRESS>"`, `prefix`: `"<NETWORKMANAGER_TEST_PREFIX>"`, `gateway`: `"<NETWORKMANAGER_INVALID_ENDPOINT>"`, `primarydns`: `"<NETWORKMANAGER_TEST_PRIMARY_DNS>"`, `secondarydns`: `"<NETWORKMANAGER_TEST_SECONDARY_DNS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_INVALID_ENDPOINT>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setipsettings_with_invalid_primarydns-nm_67"></a>
### NetworkManager_SetIPSettings_With_Invalid_PrimaryDNS (NM_67)

**Objective:** Check if the SetIPSettings method returns an error when the primarydns parameter is invalid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetIPSettings With Invalid PrimaryDNS | Invoke `SetIPSettings` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_TEST_INTERFACE>"`, `ipversion`: `"<NETWORKMANAGER_TEST_IPVERSION>"`, `autoconfig`: `"<NETWORKMANAGER_TEST_AUTOCONFIG>"`, `ipaddress`: `"<NETWORKMANAGER_TEST_IPADDRESS>"`, `prefix`: `"<NETWORKMANAGER_TEST_PREFIX>"`, `gateway`: `"<NETWORKMANAGER_TEST_GATEWAY>"`, `primarydns`: `"<NETWORKMANAGER_INVALID_ENDPOINT>"`, `secondarydns`: `"<NETWORKMANAGER_TEST_SECONDARY_DNS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_INVALID_ENDPOINT>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_setipsettings_with_invalid_secondarydns-nm_68"></a>
### NetworkManager_SetIPSettings_With_Invalid_SecondaryDNS (NM_68)

**Objective:** Check if the SetIPSettings method returns an error when the secondarydns parameter is invalid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | SetIPSettings With Invalid SecondaryDNS | Invoke `SetIPSettings` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_TEST_INTERFACE>"`, `ipversion`: `"<NETWORKMANAGER_TEST_IPVERSION>"`, `autoconfig`: `"<NETWORKMANAGER_TEST_AUTOCONFIG>"`, `ipaddress`: `"<NETWORKMANAGER_TEST_IPADDRESS>"`, `prefix`: `"<NETWORKMANAGER_TEST_PREFIX>"`, `gateway`: `"<NETWORKMANAGER_TEST_GATEWAY>"`, `primarydns`: `"<NETWORKMANAGER_TEST_PRIMARY_DNS>"`, `secondarydns`: `"<NETWORKMANAGER_INVALID_ENDPOINT>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_INVALID_ENDPOINT>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_check_getavailableinterfaces_error-nm_69"></a>
### NetworkManager_Check_GetAvailableInterfaces_Error (NM_69)

**Objective:** Check if the GetAvailableInterfaces method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check GetAvailableInterfaces API Response | Invoke `GetAvailableInterfaces` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_getprimaryinterface_error-nm_70"></a>
### NetworkManager_Check_GetPrimaryInterface_Error (NM_70)

**Objective:** Check if the GetPrimaryInterface method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check GetPrimaryInterface API Response | Invoke `GetPrimaryInterface` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPrimaryInterface"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_getpublicip_error-nm_71"></a>
### NetworkManager_Check_GetPublicIP_Error (NM_71)

**Objective:** Check if the GetPublicIP method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check GetPublicIP API Response | Invoke `GetPublicIP` on `org.rdk.NetworkManager` with `ipversion`: `"IPv4"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPublicIP", "params": {"ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_ping_error-nm_72"></a>
### NetworkManager_Check_Ping_Error (NM_72)

**Objective:** Check if the Ping method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Ping API Response | Invoke `Ping` on `org.rdk.NetworkManager` with `endpoint`: `"<PING_IP>"`, `ipversion`: `"IPv4"`, `count`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Ping", "params": {"endpoint": "<PING_IP>", "ipversion": "IPv4", "count": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_trace_error-nm_73"></a>
### NetworkManager_Check_Trace_Error (NM_73)

**Objective:** Check if the Trace method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Trace API Response | Invoke `Trace` on `org.rdk.NetworkManager` with `endpoint`: `"<TRACE_IP>"`, `ipversion`: `"IPv4"`, `count`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Trace", "params": {"endpoint": "<TRACE_IP>", "ipversion": "IPv4", "count": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_isconnectedtointernet_error-nm_74"></a>
### NetworkManager_Check_IsConnectedToInternet_Error (NM_74)

**Objective:** Check if the IsConnectedToInternet method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check IsConnectedToInternet API Response | Invoke `IsConnectedToInternet` on `org.rdk.NetworkManager` with `ipversion`: `"IPv4"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": {"ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_getinterfacestate_error-nm_75"></a>
### NetworkManager_Check_GetInterfaceState_Error (NM_75)

**Objective:** Check if the GetInterfaceState method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check GetInterfaceState API Response | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"eth0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "eth0"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_setinterfacestate_error-nm_76"></a>
### NetworkManager_Check_SetInterfaceState_Error (NM_76)

**Objective:** Check if the SetInterfaceState method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check SetInterfaceState API Response | Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"eth0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "eth0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_stopwifiscan_error-nm_77"></a>
### NetworkManager_Check_StopWiFiScan_Error (NM_77)

**Objective:** Check if the StopWiFiScan method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check StopWiFiScan API Response | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_wifidisconnect_error-nm_78"></a>
### NetworkManager_Check_WiFiDisconnect_Error (NM_78)

**Objective:** Check if the WiFiDisconnect method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check WiFiDisconnect API Response | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_ssid_frequency_checker_2-4ghz-nm_79"></a>
### NetworkManager_SSID_Frequency_Checker_2.4GHz (NM_79)

**Objective:** Scan for 2.4GHz SSIDs and verify that all SSIDs listed in the onAvailableSSIDs event are on the 2.4GHz band

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` with `frequency`: `2.4` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan", "params": {"frequency": 2.4}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; `2.4` found in scanned SSID list |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |

---

<a id="networkmanager_ssid_frequency_checker_5ghz-nm_80"></a>
### NetworkManager_SSID_Frequency_Checker_5GHz (NM_80)

**Objective:** Scan for 5GHz SSIDs and verify that all SSIDs listed in the onAvailableSSIDs event are on the 5GHz band

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` with `frequency`: `5` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan", "params": {"frequency": 5}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; `5` found in scanned SSID list |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |

---

<a id="networkmanager_scan_specific_ssid_2-4ghz-nm_81"></a>
### NetworkManager_Scan_Specific_SSID_2.4GHz (NM_81)

**Objective:** This test case checks if NetworkManager can scan for a specific SSID on the 2.4GHz band and confirm its presence

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` with `frequency`: `2.4`, `ssids`: `"<WIFI_SSID_NAME>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan", "params": {"frequency": 2.4, "ssids": "<WIFI_SSID_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |

---

<a id="networkmanager_scan_specific_ssid_5ghz-nm_82"></a>
### NetworkManager_Scan_Specific_SSID_5GHz (NM_82)

**Objective:** This test case checks if NetworkManager can scan for a specific SSID on the 5GHz band and confirm its presence

**Pre-condition:**

#### Pre-condition 1: Enable_Wifi_Interface

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Interface State | Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `SetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`, `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` Interface State set successfully |
| 3 | Get Interface State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `GetInterfaceState` on `org.rdk.NetworkManager` with `interface`: `"wlan0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Wifi Disconnect | Invoke `WiFiDisconnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi disconnected successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Wifi Scan | Invoke `StartWiFiScan` on `org.rdk.NetworkManager` with `frequency`: `5`, `ssids`: `"<WIFI_SSID_NAME_5GHZ>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan", "params": {"frequency": 5, "ssids": "<WIFI_SSID_NAME_5GHZ>"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan started successfully |
| 2 | Check On AvailableSSIDs Event | Listen for `Event_On_AvailableSSIDs` event (wait 5s) | `onAvailableSSIDs` event received; SSID list validated |
| 3 | Stop Wifi Scan | Invoke `StopWiFiScan` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` WiFi Scan stopped successfully |

---

<a id="networkmanager_trace_empty_endpoint-nm_83"></a>
### NetworkManager_Trace_Empty_Endpoint (NM_83)

**Objective:** Traces the empty endpoint

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Trace Empty Endpoint | Invoke `Trace` on `org.rdk.NetworkManager` with `endpoint`: `""`, `ipversion`: `"IPv4"`, `packets`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Trace", "params": {"endpoint": "", "ipversion": "IPv4", "packets": 10}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_trace_without_parameter-nm_84"></a>
### NetworkManager_Trace_Without_Parameter (NM_84)

**Objective:** Check if the Trace method returns an error when parameters are not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Trace Without Parameter | Invoke `Trace` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Trace"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_wifi_connect_without_parameter-nm_85"></a>
### NetworkManager_Wifi_Connect_Without_Parameter (NM_85)

**Objective:** Check if the WifiConnect method returns an error when parameter is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wifi Connect Without Parameter | Invoke `WiFiConnect` on `org.rdk.NetworkManager` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="networkmanager_get_public_ipv6_ip-nm_86"></a>
### NetworkManager_Get_Public_IPv6_IP (NM_86)

**Objective:** Validate public IPv6 IP address of the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Public IPv6 IP | Invoke `GetPublicIP` on `org.rdk.NetworkManager` with `ipversion`: `"IPv6"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPublicIP", "params": {"ipversion": "IPv6"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` public IP address returned |

---

<a id="networkmanager_check_internet_ipv6_connectivity-nm_87"></a>
### NetworkManager_Check_Internet_IPv6_Connectivity (NM_87)

**Objective:** Seeks whether the device has internet connectivity

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Internet IPv6 Connectivity | Invoke `IsConnectedToInternet` on `org.rdk.NetworkManager` with `ipversion`: `"IPv6"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": {"ipversion": "IPv6"}}' http://127.0.0.1:9998/jsonrpc` | Expected `true` |

---

<a id="networkmanager_get_ipsettings_ipv6-nm_88"></a>
### NetworkManager_Get_IPSettings_IPv6 (NM_88)

**Objective:** Gets the IP setting for the given interface

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get IPSettings | Invoke `GetIPSettings` on `org.rdk.NetworkManager` with `interface`: `"<NETWORKMANAGER_INTERFACE_DETAILS>"`, `ipversion`: `"IPv6"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetIPSettings", "params": {"interface": "<NETWORKMANAGER_INTERFACE_DETAILS>", "ipversion": "IPv6"}}' http://127.0.0.1:9998/jsonrpc` | IP Settings returned successfully |

---

<a id="networkmanager_check_primary_interface_after_lightsleep-nm_89"></a>
### NetworkManager_Check_Primary_Interface_After_LightSleep (NM_89)

**Objective:** Checks the primary interface after the device has been put in sleep mode and then woken up

**Pre-condition:**

#### Pre-condition 1: Activate_System_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.System"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check power state | Invoke `getPowerState` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Power State returned successfully |
| 2 | Set Power State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"<value>"`, `powerState`: `"ON"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Power State set successfully |
| 3 | Get Device Interfaces | Invoke `GetAvailableInterfaces` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | Available Interfaces returned successfully |
| 4 | Get Primary/Default Interface | Invoke `GetPrimaryInterface` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPrimaryInterface"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` returned `interface` is one of the values retrieved in step 3 |
| 5 | Set Power State | Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"<value>"`, `powerState`: `"STANDBY"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Power State set successfully |
| 6 | Get Power State | Invoke `getPowerState` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected `STANDBY` |
| 7 | Set Power State | Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"<value>"`, `powerState`: `"ON"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Power State set successfully |
| 8 | Get Power State | Invoke `getPowerState` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected `ON` |
| 9 | Get Primary/Default Interface | Invoke `GetPrimaryInterface` on `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPrimaryInterface"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` primary interface matches value from step 4 |

**Post-condition:**

#### Post-condition 1: Reverting_PowerState_ON

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check power state | Invoke `getPowerState` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Power State returned successfully |
| 2 | Set Power State | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"<value>"`, `powerState`: `"ON"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Power State set successfully |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M133 |