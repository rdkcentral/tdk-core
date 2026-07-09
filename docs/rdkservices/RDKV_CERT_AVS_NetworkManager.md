## TestScript Name
RDKV_CERT_AVS_NetworkManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [NetworkManager_Get_Device_Interfaces](#networkmanager_get_device_interfaces)
   - [NetworkManager_Get_Primary/Default_Interface](#networkmanager_get_primary-default_interface)
   - [NetworkManager_Validate_Public_IPv4_IP](#networkmanager_validate_public_ipv4_ip)
   - [NetworkManager_Ping_IPv4_Endpoint](#networkmanager_ping_ipv4_endpoint)
   - [NetworkManager_Trace_IPv4_Endpoint](#networkmanager_trace_ipv4_endpoint)
   - [NetworkManager_Check_Internet_IPv4_Connectivity](#networkmanager_check_internet_ipv4_connectivity)
   - [NetworkManager_GetAvailableInterfaces_With_Enabled/Disabled_Interface](#networkmanager_getavailableinterfaces_with_enabled-disabled_interface)
   - [NetworkManager_Check_On_Interface_StateChange_Event](#networkmanager_check_on_interface_statechange_event)
   - [NetworkManager_Wifi_Start_Stop_Scan](#networkmanager_wifi_start_stop_scan)
   - [NetworkManager_Check_On_AvailableSSIDs_Event](#networkmanager_check_on_availablessids_event)
   - [NetworkManager_Get_Interface_State](#networkmanager_get_interface_state)
   - [NetworkManager_SetandGet_Interface_State](#networkmanager_setandget_interface_state)
   - [NetworkManager_Wifi_Connect_Disconnect](#networkmanager_wifi_connect_disconnect)
   - [NetworkManager_Check_Get_Connected_SSID](#networkmanager_check_get_connected_ssid)
   - [NetworkManager_Get_Supported_Security_Modes](#networkmanager_get_supported_security_modes)
   - [NetworkManager_Check_On_WifiStateChange_Event](#networkmanager_check_on_wifistatechange_event)
   - [NetworkManager_Check_WifiConnect_With_Invalid_SSID_Passphrase](#networkmanager_check_wificonnect_with_invalid_ssid_passphrase)
   - [NetworkManager_Check_On_AvailableSSIDs_Event_Not_Triggered](#networkmanager_check_on_availablessids_event_not_triggered)
   - [NetworkManager_SetandGet_Stun_Endpoint](#networkmanager_setandget_stun_endpoint)
   - [NetworkManager_5GHz_Wifi_Connect_Disconnect](#networkmanager_5ghz_wifi_connect_disconnect)
   - [NetworkManager_Check_5GHz_Get_Connected_SSID](#networkmanager_check_5ghz_get_connected_ssid)
   - [NetworkManager_SetInterfaceState_Without_Enable_Parameter](#networkmanager_setinterfacestate_without_enable_parameter)
   - [NetworkManager_SetInterfaceState_Without_Parameter](#networkmanager_setinterfacestate_without_parameter)
   - [NetworkManager_GetInterfaceState_With_Invalid_Parameter](#networkmanager_getinterfacestate_with_invalid_parameter)
   - [NetworkManager_Check_Logging_Level](#networkmanager_check_logging_level)
   - [NetworkManager_Set_Lowest_Logging_Level](#networkmanager_set_lowest_logging_level)
   - [NetworkManager_Set_Mid-range_Logging_Level](#networkmanager_set_mid-range_logging_level)
   - [NetworkManager_Set_Highest_Logging_Level](#networkmanager_set_highest_logging_level)
   - [NetworkManager_Check_Wifi_State](#networkmanager_check_wifi_state)
   - [NetworkManager_Connect_Wifi_And_Check_Wifi_State](#networkmanager_connect_wifi_and_check_wifi_state)
   - [NetworkManager_Set_Single_Connectivity_Test_Endpoints](#networkmanager_set_single_connectivity_test_endpoints)
   - [NetworkManager_Set_Five_Connectivity_Test_Endpoints](#networkmanager_set_five_connectivity_test_endpoints)
   - [NetworkManager_Check_Wifi_State_After_Connecting_To_Wifi](#networkmanager_check_wifi_state_after_connecting_to_wifi)
   - [NetworkManager_Start_Scan_And_Check_Wifi_State](#networkmanager_start_scan_and_check_wifi_state)
   - [NetworkManager_Check_Wifi_State_On_Connecting_To_Invalid_Wifi_SSID](#networkmanager_check_wifi_state_on_connecting_to_invalid_wifi_ssid)
   - [NetworkManager_SetandGet_Connectivity_Test_Endpoints](#networkmanager_setandget_connectivity_test_endpoints)
   - [NetworkManager_Check_WiFi_StateChange_Event_On_Connecting_To_Wifi](#networkmanager_check_wifi_statechange_event_on_connecting_to_wifi)
   - [NetworkManager_Set_Invalid_Interface_State](#networkmanager_set_invalid_interface_state)
   - [NetworkManager_GetInterfaceState_With_Empty_Parameter](#networkmanager_getinterfacestate_with_empty_parameter)
   - [NetworkManager_Ping_Invalid_Endpoint](#networkmanager_ping_invalid_endpoint)
   - [NetworkManager_Ping_Endpoint_With_Invalid_IPVersion](#networkmanager_ping_endpoint_with_invalid_ipversion)
   - [NetworkManager_Remove_Invalid_SSID](#networkmanager_remove_invalid_ssid)
   - [NetworkManager_Remove_Empty_SSID](#networkmanager_remove_empty_ssid)
   - [NetworkManager_GetInterfaceState_Without_Parameter](#networkmanager_getinterfacestate_without_parameter)
   - [NetworkManager_Check_Get_Known_SSID](#networkmanager_check_get_known_ssid)
   - [NetworkManager_ActivateDeactivate_Event_Test](#networkmanager_activatedeactivate_event_test)
   - [NetworkManager_GetIPSettings_With_Invalid_Parameter](#networkmanager_getipsettings_with_invalid_parameter)
   - [NetworkManager_Verify_Wifi_Connect_Error](#networkmanager_verify_wifi_connect_error)
   - [NetworkManager_SetInterfaceState_Without_Interface_Parameter](#networkmanager_setinterfacestate_without_interface_parameter)
   - [NetworkManager_SetInterfaceState_With_Invalid_Parameters](#networkmanager_setinterfacestate_with_invalid_parameters)
   - [NetworkManager_Add_and_Remove_SSID](#networkmanager_add_and_remove_ssid)
   - [NetworkManager_SetStunEndpoint_With_Invalid_Endpoint](#networkmanager_setstunendpoint_with_invalid_endpoint)
   - [NetworkManager_SetStunEndpoint_With_Invalid_Port](#networkmanager_setstunendpoint_with_invalid_port)
   - [NetworkManager_SetStunEndpoint_Without_Endpoint](#networkmanager_setstunendpoint_without_endpoint)
   - [NetworkManager_SetStunEndpoint_Without_Port](#networkmanager_setstunendpoint_without_port)
   - [NetworkManager_SetStunEndpoint_Without_Parameters](#networkmanager_setstunendpoint_without_parameters)
   - [NetworkManager_AddToKnownSSIDs_With_Empty_SSID](#networkmanager_addtoknownssids_with_empty_ssid)
   - [NetworkManager_AddToKnownSSIDs_With_Empty_Passphrase](#networkmanager_addtoknownssids_with_empty_passphrase)
   - [NetworkManager_AddToKnownSSIDs_With_Empty_SSID_Passphrase](#networkmanager_addtoknownssids_with_empty_ssid_passphrase)
   - [NetworkManager_AddToKnownSSIDs_Without_Parameters](#networkmanager_addtoknownssids_without_parameters)
   - [NetworkManager_SetIPSettings_With_Empty_Interface](#networkmanager_setipsettings_with_empty_interface)
   - [NetworkManager_SetIPSettings_With_Invalid_Interface](#networkmanager_setipsettings_with_invalid_interface)
   - [NetworkManager_SetIPSettings_With_Empty_Ipversion](#networkmanager_setipsettings_with_empty_ipversion)
   - [NetworkManager_SetIPSettings_With_Invalid_Ipversion](#networkmanager_setipsettings_with_invalid_ipversion)
   - [NetworkManager_SetIPSettings_With_Invalid_Ipaddress](#networkmanager_setipsettings_with_invalid_ipaddress)
   - [NetworkManager_SetIPSettings_With_Invalid_Gateway](#networkmanager_setipsettings_with_invalid_gateway)
   - [NetworkManager_SetIPSettings_With_Invalid_PrimaryDNS](#networkmanager_setipsettings_with_invalid_primarydns)
   - [NetworkManager_SetIPSettings_With_Invalid_SecondaryDNS](#networkmanager_setipsettings_with_invalid_secondarydns)
   - [NetworkManager_Check_GetAvailableInterfaces_Error](#networkmanager_check_getavailableinterfaces_error)
   - [NetworkManager_Check_GetPrimaryInterface_Error](#networkmanager_check_getprimaryinterface_error)
   - [NetworkManager_Check_GetPublicIP_Error](#networkmanager_check_getpublicip_error)
   - [NetworkManager_Check_Ping_Error](#networkmanager_check_ping_error)
   - [NetworkManager_Check_Trace_Error](#networkmanager_check_trace_error)
   - [NetworkManager_Check_IsConnectedToInternet_Error](#networkmanager_check_isconnectedtointernet_error)
   - [NetworkManager_Check_GetInterfaceState_Error](#networkmanager_check_getinterfacestate_error)
   - [NetworkManager_Check_SetInterfaceState_Error](#networkmanager_check_setinterfacestate_error)
   - [NetworkManager_Check_StopWiFiScan_Error](#networkmanager_check_stopwifiscan_error)
   - [NetworkManager_Check_WiFiDisconnect_Error](#networkmanager_check_wifidisconnect_error)
   - [NetworkManager_SSID_Frequency_Checker_2.4GHz](#networkmanager_ssid_frequency_checker_2-4ghz)
   - [NetworkManager_SSID_Frequency_Checker_5GHz](#networkmanager_ssid_frequency_checker_5ghz)
   - [NetworkManager_Scan_Specific_SSID_2.4GHz](#networkmanager_scan_specific_ssid_2-4ghz)
   - [NetworkManager_Scan_Specific_SSID_5GHz](#networkmanager_scan_specific_ssid_5ghz)
   - [NetworkManager_Trace_Empty_Endpoint](#networkmanager_trace_empty_endpoint)
   - [NetworkManager_Trace_Without_Parameter](#networkmanager_trace_without_parameter)
   - [NetworkManager_Wifi_Connect_Without_Parameter](#networkmanager_wifi_connect_without_parameter)
   - [NetworkManager_Get_Public_IPv6_IP](#networkmanager_get_public_ipv6_ip)
   - [NetworkManager_Check_Internet_IPv6_Connectivity](#networkmanager_check_internet_ipv6_connectivity)
   - [NetworkManager_Get_IPSettings_IPv6](#networkmanager_get_ipsettings_ipv6)
   - [NetworkManager_Check_Primary_Interface_After_LightSleep](#networkmanager_check_primary_interface_after_lightsleep)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **NetworkManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.NetworkManager` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onInterfaceStateChange event | Register a WebSocket event listener for `onInterfaceStateChange` to receive `onInterfaceStateChange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.register", "params": {"event": "onInterfaceStateChange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the onAvailableSSIDs event | Register a WebSocket event listener for `onAvailableSSIDs` to receive `onAvailableSSIDs` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.register", "params": {"event": "onAvailableSSIDs", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 3 | Subscribe to the onWiFiStateChange event | Register a WebSocket event listener for `onWiFiStateChange` to receive `onWiFiStateChange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.register", "params": {"event": "onWiFiStateChange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 4 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure Custom Timeout For Ping And Trace | `CUSTOM_TIMEOUT_FOR_PING_AND_TRACE` must be set to the custom timeout to ping or trace the particular endpoint | The `CUSTOM_TIMEOUT_FOR_PING_AND_TRACE` value should be correctly configured in the device-specific config file |
| 2 | Configure Connectivity Test Endpoints | `CONNECTIVITY_TEST_ENDPOINTS` must be configured with a maximum of 5 endpoints | The `CONNECTIVITY_TEST_ENDPOINTS` value should be correctly configured in the device-specific config file |
| 3 | Configure Wifi Security Mode | `WIFI_SECURITY_MODE` must be set to the security mode used for 2.4GHZ connecting | The `WIFI_SECURITY_MODE` value should be correctly configured in the device-specific config file |
| 4 | Configure Wifi Security Mode 5ghz | `WIFI_SECURITY_MODE_5GHZ` must be set to the security mode used for 5GHZ connecting | The `WIFI_SECURITY_MODE_5GHZ` value should be correctly configured in the device-specific config file |
| 5 | Configure Wifi Invalid Passphrase | `WIFI_INVALID_PASSPHRASE` must be set to the invalid passphrase for negative test case | The `WIFI_INVALID_PASSPHRASE` value should be correctly configured in the device-specific config file |
| 6 | Configure Wifi Invalid SSID Name | `WIFI_INVALID_SSID_NAME` must be set to the invalid SSID name for negative test case | The `WIFI_INVALID_SSID_NAME` value should be correctly configured in the device-specific config file |
| 7 | Configure Enable Disable Interfacename | `NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME` must be set to the name of the interface to enable or disable Example : eth0 or wlan0 | The `NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME` value should be correctly configured in the device-specific config file |
| 8 | Configure Interface Details | `NETWORKMANAGER_INTERFACE_DETAILS` must be set to the name of the current interface Example : eth0 or wlan0 | The `NETWORKMANAGER_INTERFACE_DETAILS` value should be correctly configured in the device-specific config file |
| 9 | Configure Ethernet Cableconnected Status | `NETWORKMANAGER_ETHERNET_CABLECONNECTED_STATUS` must be set to 'yes' if the device is connected to an ethernet cable, otherwise 'no' | The `NETWORKMANAGER_ETHERNET_CABLECONNECTED_STATUS` value should be correctly configured in the device-specific config file |
| 10 | Configure Ipv6 Support | `NETWORKMANAGER_IPV6_SUPPORT` must be set to 'yes' if IPv6 support is available in the environment otherwise set to 'no' | The `NETWORKMANAGER_IPV6_SUPPORT` value should be correctly configured in the device-specific config file |
| 11 | Configure Max Connectivity Test Endpoints | `NETWORKMANAGER_MAX_CONNECTIVITY_TEST_ENDPOINTS` must be set to the endpoints value required for the test | The `NETWORKMANAGER_MAX_CONNECTIVITY_TEST_ENDPOINTS` value should be correctly configured in the device-specific config file |
| 12 | Configure Invalid Endpoint | `NETWORKMANAGER_INVALID_ENDPOINT` must be set to the endpoint value required for the test | The `NETWORKMANAGER_INVALID_ENDPOINT` value should be correctly configured in the device-specific config file |
| 13 | Configure Invalid Port | `NETWORKMANAGER_INVALID_PORT` must be set to the port value required for the test | The `NETWORKMANAGER_INVALID_PORT` value should be correctly configured in the device-specific config file |
| 14 | Configure Test Ipaddress | `NETWORKMANAGER_TEST_IPADDRESS` must be set to the endpoint value required for the test | The `NETWORKMANAGER_TEST_IPADDRESS` value should be correctly configured in the device-specific config file |
| 15 | Configure Test Port | `NETWORKMANAGER_TEST_PORT` must be set to the port value required for the test | The `NETWORKMANAGER_TEST_PORT` value should be correctly configured in the device-specific config file |
| 16 | Configure Test Interface | `NETWORKMANAGER_TEST_INTERFACE` must be set to the interface value required for the test | The `NETWORKMANAGER_TEST_INTERFACE` value should be correctly configured in the device-specific config file |
| 17 | Configure Test Ipversion | `NETWORKMANAGER_TEST_IPVERSION` must be set to the IP version value required for the test | The `NETWORKMANAGER_TEST_IPVERSION` value should be correctly configured in the device-specific config file |
| 18 | Configure Test Autoconfig | `NETWORKMANAGER_TEST_AUTOCONFIG` must be set to the auto-configuration value required for the test | The `NETWORKMANAGER_TEST_AUTOCONFIG` value should be correctly configured in the device-specific config file |
| 19 | Configure Test Prefix | `NETWORKMANAGER_TEST_PREFIX` must be set to the prefix value required for the test | The `NETWORKMANAGER_TEST_PREFIX` value should be correctly configured in the device-specific config file |
| 20 | Configure Test Gateway | `NETWORKMANAGER_TEST_GATEWAY` must be set to the gateway value required for the test | The `NETWORKMANAGER_TEST_GATEWAY` value should be correctly configured in the device-specific config file |
| 21 | Configure Test Primary DNS | `NETWORKMANAGER_TEST_PRIMARY_DNS` must be set to the primary DNS value required for the test | The `NETWORKMANAGER_TEST_PRIMARY_DNS` value should be correctly configured in the device-specific config file |
| 22 | Configure Test Secondary DNS | `NETWORKMANAGER_TEST_SECONDARY_DNS` must be set to the secondary DNS value required for the test | The `NETWORKMANAGER_TEST_SECONDARY_DNS` value should be correctly configured in the device-specific config file |
| 23 | Configure Ping IP | `PING_IP` must be set to the IP address which is accessible from Device under test | The `PING_IP` value should be correctly configured in the device-specific config file |
| 24 | Configure Trace IP | `TRACE_IP` must be set to the endpoint value required for the test | The `TRACE_IP` value should be correctly configured in the device-specific config file |
| 25 | Configure Wifi SSID Name | `WIFI_SSID_NAME` must be set to the wifi 2.4GHZ SSID of the End Point | The `WIFI_SSID_NAME` value should be correctly configured in the device-specific config file |
| 26 | Configure Wifi Passphrase | `WIFI_PASSPHRASE` must be set to the passphrase of the 2.4GHZ SSID | The `WIFI_PASSPHRASE` value should be correctly configured in the device-specific config file |
| 27 | Configure Wifi SSID Name 5ghz | `WIFI_SSID_NAME_5GHZ` must be set to the wifi 5GHZ SSID of the End Point | The `WIFI_SSID_NAME_5GHZ` value should be correctly configured in the device-specific config file |
| 28 | Configure Wifi Passphrase 5ghz | `WIFI_PASSPHRASE_5GHZ` must be set to the passphrase of the 5GHZ SSID | The `WIFI_PASSPHRASE_5GHZ` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="networkmanager_get_device_interfaces"></a>
### TestCase Name
NetworkManager_Get_Device_Interfaces

### TestCase ID
NM_01

### TestCase Objective
Gets list of interfaces supported by device

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Device Interfaces | Invoke GetAvailableInterfaces on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that the available interfaces are returned successfully |

---

<a id="networkmanager_get_primary-default_interface"></a>
### TestCase Name
NetworkManager_Get_Primary/Default_Interface

### TestCase ID
NM_02

### TestCase Objective
Gets primary/default interface of the device

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Device Interfaces | Invoke GetAvailableInterfaces on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that the available interfaces are returned successfully |
| 2 | Get Primary/Default Interface | Invoke GetPrimaryInterface on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPrimaryInterface"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` returned `interface` is one of the values retrieved in step 1  |

---

<a id="networkmanager_validate_public_ipv4_ip"></a>
### TestCase Name
NetworkManager_Validate_Public_IPv4_IP

### TestCase ID
NM_03

### TestCase Objective
Validate public IPv4 IP address of the device

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Public IP Address | Execute command on the device curl -s ifconfig.me | Verify that the public IP address is returned successfully |
| 2 | Get Public IPv4 IP | Invoke GetPublicIP on org.rdk.NetworkManager with ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPublicIP", "params": {"ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` public ip matches value from step 1  |

---

<a id="networkmanager_ping_ipv4_endpoint"></a>
### TestCase Name
NetworkManager_Ping_IPv4_Endpoint

### TestCase ID
NM_04

### TestCase Objective
Pings the specified end point

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Ping Endpoint | Invoke Ping on org.rdk.NetworkManager with endpoint: "<PING_IP>", ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Ping", "params": {"endpoint": "<PING_IP>", "ipversion": "IPv4", "count": 10}}' http://127.0.0.1:9998/jsonrpc` | Verify that the ping to `<PING_IP>` succeeds with `10` packets as expected  |

---

<a id="networkmanager_trace_ipv4_endpoint"></a>
### TestCase Name
NetworkManager_Trace_IPv4_Endpoint

### TestCase ID
NM_05

### TestCase Objective
Traces the specified end point

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Trace Endpoint | Invoke Trace on org.rdk.NetworkManager with endpoint: "<TRACE_IP>", ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Trace", "params": {"endpoint": "<TRACE_IP>", "ipversion": "IPv4", "packets": 10}}' http://127.0.0.1:9998/jsonrpc` | Verify that the trace route to `<TRACE_IP>` completes successfully as expected  |

---

<a id="networkmanager_check_internet_ipv4_connectivity"></a>
### TestCase Name
NetworkManager_Check_Internet_IPv4_Connectivity

### TestCase ID
NM_06

### TestCase Objective
Seeks whether the device has internet connectivity

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Internet IPv4 Connectivity | Invoke IsConnectedToInternet on org.rdk.NetworkManager with ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": {"ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API returns `true` as the expected result  |

---

<a id="networkmanager_getavailableinterfaces_with_enabled-disabled_interface"></a>
### TestCase Name
NetworkManager_GetAvailableInterfaces_With_Enabled/Disabled_Interface

### TestCase ID
NM_07

### TestCase Objective
Verify that the GetAvailableInterfaces method returns the correct list of available interfaces when interface is enabled or disabled

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | Invoke SetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>", enabled: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>", "enabled": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state matches toggled value from step 1  |
| 4 | Get Device Interfaces | Invoke GetAvailableInterfaces on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state matches toggled value from step 1  |

---

<a id="networkmanager_check_on_interface_statechange_event"></a>
### TestCase Name
NetworkManager_Check_On_Interface_StateChange_Event

### TestCase ID
NM_08

### TestCase Objective
Check if the event is triggered upon a change in the interface state

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | Invoke SetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>", enabled: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>", "enabled": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Check On Interface StateChange Event | Listen for Event_On_Interface_StateChange event (wait 5s) | Ensure the `onInterfaceStateChange` event is received and the interface state change is validated |
| 4 | Get Interface State | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state matches toggled value from step 1  |

---

<a id="networkmanager_wifi_start_stop_scan"></a>
### TestCase Name
NetworkManager_Wifi_Start_Stop_Scan

### TestCase ID
NM_09

### TestCase Objective
Check if the start and stop wifi scan methods can successfully initiate and stop the wifi scanning process

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |

---

<a id="networkmanager_check_on_availablessids_event"></a>
### TestCase Name
NetworkManager_Check_On_AvailableSSIDs_Event

### TestCase ID
NM_10

### TestCase Objective
Check if the event is triggered when initiating a wifi scan

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |

---

<a id="networkmanager_get_interface_state"></a>
### TestCase Name
NetworkManager_Get_Interface_State

### TestCase ID
NM_11

### TestCase Objective
Ensure that the GetInterfaceState method successfully returns the state when provided with a valid network interface

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_INTERFACE_DETAILS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_INTERFACE_DETAILS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |

---

<a id="networkmanager_setandget_interface_state"></a>
### TestCase Name
NetworkManager_SetandGet_Interface_State

### TestCase ID
NM_12

### TestCase Objective
Check GetInterfaceState method returns the correct interface state after using the SetInterfaceState method

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | Invoke SetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>", enabled: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>", "enabled": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "<NETWORKMANAGER_ENABLE_DISABLE_INTERFACENAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state matches toggled value from step 1  |

---

<a id="networkmanager_wifi_connect_disconnect"></a>
### TestCase Name
NetworkManager_Wifi_Connect_Disconnect

### TestCase ID
NM_13

### TestCase Objective
Check if the connect and disconnect wifi methods can successfully establish and terminate the wifi connection

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>", passphrase: "<WIFI_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi connected successfully  |
| 5 | Wifi Disconnect | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

---

<a id="networkmanager_check_get_connected_ssid"></a>
### TestCase Name
NetworkManager_Check_Get_Connected_SSID

### TestCase ID
NM_14

### TestCase Objective
Ensure that the GetConnectedSSID method successfully returns the correct SSID information when all parameters are valid

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>", passphrase: "<WIFI_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi connected successfully  |
| 5 | Check Get Connected SSID | Invoke GetConnectedSSID on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` connected SSID returned  |
| 6 | Wifi Disconnect | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

---

<a id="networkmanager_get_supported_security_modes"></a>
### TestCase Name
NetworkManager_Get_Supported_Security_Modes

### TestCase ID
NM_15

### TestCase Objective
Returns the Wifi security modes that the device supports

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Supported Security Modes | Invoke GetSupportedSecurityModes on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetSupportedSecurityModes"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` non-empty list of supported WiFi security modes returned  |

---

<a id="networkmanager_check_on_wifistatechange_event"></a>
### TestCase Name
NetworkManager_Check_On_WifiStateChange_Event

### TestCase ID
NM_16

### TestCase Objective
Check whether the wifistatechange event is triggered upon connecting to and disconnecting from wifi

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>", passphrase: "<WIFI_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi connected successfully  |
| 5 | Check On WiFiStateChange Event | Listen for Event_On_WiFiStateChange event (wait 10s) | Verify that `success` : `true` `state`: `5`, `status`: `WIFI_STATE_CONNECTED`  |
| 6 | Check Get Connected SSID | Invoke GetConnectedSSID on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` connected SSID returned  |
| 7 | Wifi Disconnect | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |
| 8 | Check On WiFiStateChange Event | Listen for Event_On_WiFiStateChange event (wait 10s) | Verify that `success` : `true` `state`: `2`, `status`: `WIFI_STATE_DISCONNECTED`  |

---

<a id="networkmanager_check_wificonnect_with_invalid_ssid_passphrase"></a>
### TestCase Name
NetworkManager_Check_WifiConnect_With_Invalid_SSID_Passphrase

### TestCase ID
NM_17

### TestCase Objective
Check if the wifi connect method fails when provided with an invalid SSID and passphrase

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_INVALID_SSID_NAME>", passphrase: "<WIFI_INVALID_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_INVALID_SSID_NAME>", "passphrase": "<WIFI_INVALID_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_check_on_availablessids_event_not_triggered"></a>
### TestCase Name
NetworkManager_Check_On_AvailableSSIDs_Event_Not_Triggered

### TestCase ID
NM_18

### TestCase Objective
Check if the onAvailableSSID event is triggered after stopping the wifi scan

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Verify that the event is received and validated |

---

<a id="networkmanager_setandget_stun_endpoint"></a>
### TestCase Name
NetworkManager_SetandGet_Stun_Endpoint

### TestCase ID
NM_19

### TestCase Objective
Check GetStunEndpoint method returns the correct endpoint after using the SetStunEndpoint method

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Stun Endpoint | Invoke GetStunEndpoint on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetStunEndpoint"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `endpoint` and `port` returned  |
| 2 | Set Stun Endpoint | Invoke SetStunEndpoint on org.rdk.NetworkManager with endpoint: "<result_step_1>", port: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"endpoint": "<result_step_1>", "port": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Stun Endpoint set successfully  |
| 3 | Get Stun Endpoint | Invoke GetStunEndpoint on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetStunEndpoint"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `endpoint` and `port` match values from step 1  |

---

<a id="networkmanager_5ghz_wifi_connect_disconnect"></a>
### TestCase Name
NetworkManager_5GHz_Wifi_Connect_Disconnect

### TestCase ID
NM_20

### TestCase Objective
Check if the connect and disconnect wifi methods can successfully establish and terminate the 5GHz wifi connection

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME_5GHZ>", passphrase: "<WIFI_PASSPHRASE_5GHZ>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME_5GHZ>", "passphrase": "<WIFI_PASSPHRASE_5GHZ>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi connected successfully  |
| 5 | Wifi Disconnect | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

---

<a id="networkmanager_check_5ghz_get_connected_ssid"></a>
### TestCase Name
NetworkManager_Check_5GHz_Get_Connected_SSID

### TestCase ID
NM_21

### TestCase Objective
Ensure that the GetConnectedSSID method successfully returns the correct 5Ghz SSID information when all parameters are valid

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME_5GHZ>", passphrase: "<WIFI_PASSPHRASE_5GHZ>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME_5GHZ>", "passphrase": "<WIFI_PASSPHRASE_5GHZ>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi connected successfully  |
| 5 | Check Get Connected SSID | Invoke GetConnectedSSID on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` connected SSID returned  |
| 6 | Wifi Disconnect | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

---

<a id="networkmanager_setinterfacestate_without_enable_parameter"></a>
### TestCase Name
NetworkManager_SetInterfaceState_Without_Enable_Parameter

### TestCase ID
NM_22

### TestCase Objective
Check if the SetInterfaceState method returns an error when enabled parameter is not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetInterfaceState Without Enable Parameter | Invoke SetInterfaceState on org.rdk.NetworkManager with interface: "eth0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "eth0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setinterfacestate_without_parameter"></a>
### TestCase Name
NetworkManager_SetInterfaceState_Without_Parameter

### TestCase ID
NM_23

### TestCase Objective
Check if the SetInterfaceState method returns an error when parameter is not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetInterfaceState Without Parameter | Invoke SetInterfaceState on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_getinterfacestate_with_invalid_parameter"></a>
### TestCase Name
NetworkManager_GetInterfaceState_With_Invalid_Parameter

### TestCase ID
NM_24

### TestCase Objective
Check if the GetInterfaceState method returns an error when invalid parameter is provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetInterfaceState With Invalid Parameter | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: "Invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "Invalid"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_check_logging_level"></a>
### TestCase Name
NetworkManager_Check_Logging_Level

### TestCase ID
NM_25

### TestCase Objective
Checks whether able to set and get various logging level

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Log Level | Invoke GetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` current log level returned  |
| 2 | Set Log Level | Invoke SetLogLevel on org.rdk.NetworkManager with level: "<LEVEL_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetLogLevel", "params": {"level": "<LEVEL_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Log Level set successfully  |
| 3 | Get Log Level | Invoke GetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |

---

<a id="networkmanager_set_lowest_logging_level"></a>
### TestCase Name
NetworkManager_Set_Lowest_Logging_Level

### TestCase ID
NM_26

### TestCase Objective
Check if able to set and get the lowest logging level

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Log Level | Invoke GetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` current log level returned  |
| 2 | Set Log Level | Invoke SetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetLogLevel", "params": {"level": 0}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Log Level set successfully  |
| 3 | Get Log Level | Invoke GetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `level`: `0`  |

---

<a id="networkmanager_set_mid-range_logging_level"></a>
### TestCase Name
NetworkManager_Set_Mid-range_Logging_Level

### TestCase ID
NM_27

### TestCase Objective
Check if able to set and get the mid-range logging level

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Log Level | Invoke GetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` current log level returned  |
| 2 | Set Log Level | Invoke SetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetLogLevel", "params": {"level": 2}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Log Level set successfully  |
| 3 | Get Log Level | Invoke GetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `level`: `2`  |

---

<a id="networkmanager_set_highest_logging_level"></a>
### TestCase Name
NetworkManager_Set_Highest_Logging_Level

### TestCase ID
NM_28

### TestCase Objective
Check if able to set and get the highest logging level

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Log Level | Invoke GetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` current log level returned  |
| 2 | Set Log Level | Invoke SetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetLogLevel", "params": {"level": 4}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Log Level set successfully  |
| 3 | Get Log Level | Invoke GetLogLevel on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetLogLevel"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `level`: `4`  |

---

<a id="networkmanager_check_wifi_state"></a>
### TestCase Name
NetworkManager_Check_Wifi_State

### TestCase ID
NM_29

### TestCase Objective
Returns the current Wifi State

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Wifi State | Invoke GetWifiState on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the WiFi state is returned successfully |

---

<a id="networkmanager_connect_wifi_and_check_wifi_state"></a>
### TestCase Name
NetworkManager_Connect_Wifi_And_Check_Wifi_State

### TestCase ID
NM_30

### TestCase Objective
Check the wifi state on connecting/disconnecting to the wifi ssid

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>", passphrase: "<WIFI_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi connected successfully  |
| 5 | Check Get Connected SSID | Invoke GetConnectedSSID on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` connected SSID returned  |
| 6 | Check Wifi State | Invoke GetWifiState on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `state`: `5`, `status`: `WIFI_STATE_CONNECTED`  |
| 7 | Wifi Disconnect | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |
| 8 | Check Wifi State | Invoke GetWifiState on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `state`: `2`, `status`: `WIFI_STATE_DISCONNECTED`  |

---

<a id="networkmanager_set_single_connectivity_test_endpoints"></a>
### TestCase Name
NetworkManager_Set_Single_Connectivity_Test_Endpoints

### TestCase ID
NM_31

### TestCase Objective
Check if able to set the valid single test endpoint

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Connectivity Endpoints | Invoke SetConnectivityTestEndpoints on org.rdk.NetworkManager with endpoints: "<CONNECTIVITY_TEST_ENDPOINTS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetConnectivityTestEndpoints", "params": {"endpoints": "<CONNECTIVITY_TEST_ENDPOINTS>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that connectivity test endpoints are set successfully |

---

<a id="networkmanager_set_five_connectivity_test_endpoints"></a>
### TestCase Name
NetworkManager_Set_Five_Connectivity_Test_Endpoints

### TestCase ID
NM_32

### TestCase Objective
Check if able to set upto 5 endpoints

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Connectivity Endpoints | Invoke SetConnectivityTestEndpoints on org.rdk.NetworkManager with endpoints: "<NETWORKMANAGER_MAX_CONNECTIVITY_TEST_ENDPOINTS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetConnectivityTestEndpoints", "params": {"endpoints": "<NETWORKMANAGER_MAX_CONNECTIVITY_TEST_ENDPOINTS>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that connectivity test endpoints are set successfully |

---

<a id="networkmanager_check_wifi_state_after_connecting_to_wifi"></a>
### TestCase Name
NetworkManager_Check_Wifi_State_After_Connecting_To_Wifi

### TestCase ID
NM_33

### TestCase Objective
Check the wifi state after connecting to the wifi ssid

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>", passphrase: "<WIFI_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi connected successfully  |
| 5 | Check Wifi State | Invoke GetWifiState on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `state`: `5`, `status`: `WIFI_STATE_CONNECTED`  |
| 6 | Check Get Connected SSID | Invoke GetConnectedSSID on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` connected SSID returned  |
| 7 | Wifi Disconnect | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

---

<a id="networkmanager_start_scan_and_check_wifi_state"></a>
### TestCase Name
NetworkManager_Start_Scan_And_Check_Wifi_State

### TestCase ID
NM_34

### TestCase Objective
Check the wifi state on scanning for the wifi

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Check Wifi State | Invoke GetWifiState on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `state`: `2`, `status`: `WIFI_STATE_DISCONNECTED`  |
| 4 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |

---

<a id="networkmanager_check_wifi_state_on_connecting_to_invalid_wifi_ssid"></a>
### TestCase Name
NetworkManager_Check_Wifi_State_On_Connecting_To_Invalid_Wifi_SSID

### TestCase ID
NM_35

### TestCase Objective
Check the wifi state on connecting to the invalid wifi ssid

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_INVALID_SSID_NAME>", passphrase: "<WIFI_INVALID_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_INVALID_SSID_NAME>", "passphrase": "<WIFI_INVALID_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |
| 5 | Check Wifi State | Invoke GetWifiState on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetWifiState"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `state`: `2`, `status`: `WIFI_STATE_DISCONNECTED`  |

---

<a id="networkmanager_setandget_connectivity_test_endpoints"></a>
### TestCase Name
NetworkManager_SetandGet_Connectivity_Test_Endpoints

### TestCase ID
NM_36

### TestCase Objective
Check GetConnectivityTestEndpoints method returns the correct test endpoint set using the SetConnectivityTestEndpoints method

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Connectivity Test Endpoints | Invoke GetConnectivityTestEndpoints on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectivityTestEndpoints"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` connectivity test endpoints returned  |
| 2 | Set Connectivity Endpoints | Invoke SetConnectivityTestEndpoints on org.rdk.NetworkManager with endpoints: "<CONNECTIVITY_TEST_ENDPOINTS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetConnectivityTestEndpoints", "params": {"endpoints": "<CONNECTIVITY_TEST_ENDPOINTS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Connectivity Test Endpoints set successfully  |
| 3 | Get Connectivity Test Endpoints | Invoke GetConnectivityTestEndpoints on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectivityTestEndpoints"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` connectivity test endpoints returned  |

---

<a id="networkmanager_check_wifi_statechange_event_on_connecting_to_wifi"></a>
### TestCase Name
NetworkManager_Check_WiFi_StateChange_Event_On_Connecting_To_Wifi

### TestCase ID
NM_37

### TestCase Objective
Check the wifi state change event on connecting to the wifi ssid

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>", passphrase: "<WIFI_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi connected successfully  |
| 5 | Check On WiFiStateChange Event | Listen for Event_On_WiFiStateChange event (wait 10s) | Verify that `success` : `true` `state`: `4`, `status`: `WIFI_STATE_CONNECTING`  |
| 6 | Check Get Connected SSID | Invoke GetConnectedSSID on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` connected SSID returned  |
| 7 | Wifi Disconnect | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

---

<a id="networkmanager_set_invalid_interface_state"></a>
### TestCase Name
NetworkManager_Set_Invalid_Interface_State

### TestCase ID
NM_38

### TestCase Objective
check if the SetInterfaceState method returns error on setting the invalid interface name

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Interface State | Invoke SetInterfaceState on org.rdk.NetworkManager with interface: "invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "invalid", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_getinterfacestate_with_empty_parameter"></a>
### TestCase Name
NetworkManager_GetInterfaceState_With_Empty_Parameter

### TestCase ID
NM_39

### TestCase Objective
Check if the GetInterfaceState method returns an error when empty parameter is provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetInterfaceState With Empty Parameter | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_ping_invalid_endpoint"></a>
### TestCase Name
NetworkManager_Ping_Invalid_Endpoint

### TestCase ID
NM_40

### TestCase Objective
Pings the invalid endpoint

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Ping Host | Invoke Ping on org.rdk.NetworkManager with endpoint: "<NETWORKMANAGER_INVALID_ENDPOINT>", ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Ping", "params": {"endpoint": "<NETWORKMANAGER_INVALID_ENDPOINT>", "ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the ping fails with error `could not ping endpoint` for the invalid endpoint `<NETWORKMANAGER_INVALID_ENDPOINT>`  |

---

<a id="networkmanager_ping_endpoint_with_invalid_ipversion"></a>
### TestCase Name
NetworkManager_Ping_Endpoint_With_Invalid_IPVersion

### TestCase ID
NM_41

### TestCase Objective
Pings the endpoint with invalid ipversion

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Ping Host | Invoke Ping on org.rdk.NetworkManager with endpoint: "<PING_IP>", ipversion: "invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Ping", "params": {"endpoint": "<PING_IP>", "ipversion": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API returns the expected error message `Could not access requested service`  |

---

<a id="networkmanager_remove_invalid_ssid"></a>
### TestCase Name
NetworkManager_Remove_Invalid_SSID

### TestCase ID
NM_42

### TestCase Objective
Check if RemoveKnownSSID method returns an error when parameter is provided with invalid ssid

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Remove Known SSID | Invoke RemoveKnownSSID on org.rdk.NetworkManager with ssid: "invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.RemoveKnownSSID", "params": {"ssid": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_remove_empty_ssid"></a>
### TestCase Name
NetworkManager_Remove_Empty_SSID

### TestCase ID
NM_43

### TestCase Objective
Check if RemoveKnownSSID method returns an error when parameter is provided with empty ssid

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Remove Known SSID | Invoke RemoveKnownSSID on org.rdk.NetworkManager with ssid: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.RemoveKnownSSID", "params": {"ssid": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Known SSID unregistered successfully  |

---

<a id="networkmanager_getinterfacestate_without_parameter"></a>
### TestCase Name
NetworkManager_GetInterfaceState_Without_Parameter

### TestCase ID
NM_44

### TestCase Objective
Check if the GetInterfaceState method returns an error when interface parameter is not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetInterfaceState Without Parameter | Invoke GetInterfaceState on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_check_get_known_ssid"></a>
### TestCase Name
NetworkManager_Check_Get_Known_SSID

### TestCase ID
NM_45

### TestCase Objective
Check if the GetKnownSSIDs method returns the connected SSID name

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |
| 4 | Wifi Connect | Invoke WiFiConnect on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>", passphrase: "<WIFI_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi connected successfully  |
| 5 | Check Get Connected SSID | Invoke GetConnectedSSID on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` connected SSID returned  |
| 6 | Check Get Known SSID | Invoke GetKnownSSIDs on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` known SSIDs list returned  |
| 7 | Wifi Disconnect | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

---

<a id="networkmanager_activatedeactivate_event_test"></a>
### TestCase Name
NetworkManager_ActivateDeactivate_Event_Test

### TestCase ID
NM_46

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate Network Plugin | Invoke deactivate on Controller with callsign: "org.rdk.NetworkManager"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `org.rdk.networkmanager` with state `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate Network Plugin | Invoke activate on Controller with callsign: "org.rdk.NetworkManager"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `org.rdk.networkmanager` with state `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="networkmanager_getipsettings_with_invalid_parameter"></a>
### TestCase Name
NetworkManager_GetIPSettings_With_Invalid_Parameter

### TestCase ID
NM_47

### TestCase Objective
Check if the GetIPSettings method returns an error when invalid interface parameter is provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetIPSettings With Invalid Parameter | Invoke GetIPSettings on org.rdk.NetworkManager with interface: "invalid", ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetIPSettings", "params": {"interface": "invalid", "ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_verify_wifi_connect_error"></a>
### TestCase Name
NetworkManager_Verify_Wifi_Connect_Error

### TestCase ID
NM_48

### TestCase Objective
Verify that the WifiConnect method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate NetworkManager Plugin | Invoke deactivate on Controller with callsign: "org.rdk.NetworkManager"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `org.rdk.networkmanager` with state `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Check NetworkManager Wifi Connect API Response | Invoke WiFiConnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate NetworkManager Plugin | Invoke activate on Controller with callsign: "org.rdk.NetworkManager"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `org.rdk.networkmanager` with state `"activated"` |
| 7 | Check PluginActive Status | Invoke status on Controller for org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="networkmanager_setinterfacestate_without_interface_parameter"></a>
### TestCase Name
NetworkManager_SetInterfaceState_Without_Interface_Parameter

### TestCase ID
NM_49

### TestCase Objective
Check if the SetInterfaceState method returns an error when interface parameter is not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetInterfaceState Without Interface Parameter | Invoke SetInterfaceState on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setinterfacestate_with_invalid_parameters"></a>
### TestCase Name
NetworkManager_SetInterfaceState_With_Invalid_Parameters

### TestCase ID
NM_50

### TestCase Objective
Check if the SetInterfaceState method returns an error when both interface and enabled parameters are provided with invalid values

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetInterfaceState With Invalid Parameters | Invoke SetInterfaceState on org.rdk.NetworkManager with interface: "invalid", enabled: "invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "invalid", "enabled": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_add_and_remove_ssid"></a>
### TestCase Name
NetworkManager_Add_and_Remove_SSID

### TestCase ID
NM_51

### TestCase Objective
Check that an SSID can be added and then removed successfully

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Known SSID List | Invoke GetKnownSSIDs on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | Verify that known SSIDs are returned successfully |
| 2 | Remove Known SSID | *(Conditional statement executed only if previous step condition is met)*<br>Invoke RemoveKnownSSID on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.RemoveKnownSSID", "params": {"ssid": "<WIFI_SSID_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Known SSID unregistered successfully  |
| 3 | Get Known SSID List | *(Conditional statement executed only if previous step condition is met)*<br>Invoke GetKnownSSIDs on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | Verify that known SSIDs are returned successfully |
| 4 | Add to Known SSID | Invoke AddToKnownSSIDs on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>", passphrase: "<WIFI_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` To Known SSIDs registered successfully  |
| 5 | Get Known SSID List | Invoke GetKnownSSIDs on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` known SSIDs list returned  |
| 6 | Remove Known SSID | Invoke RemoveKnownSSID on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.RemoveKnownSSID", "params": {"ssid": "<WIFI_SSID_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Known SSID unregistered successfully  |
| 7 | Get Known SSID List | Invoke GetKnownSSIDs on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | Verify that known SSIDs are returned successfully |

---

<a id="networkmanager_setstunendpoint_with_invalid_endpoint"></a>
### TestCase Name
NetworkManager_SetStunEndpoint_With_Invalid_Endpoint

### TestCase ID
NM_52

### TestCase Objective
Check if the SetStunEndpoint method throws an error when an invalid endpoint parameter is passed

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetStunEndpoint With Invalid Endpoint | Invoke SetStunEndpoint on org.rdk.NetworkManager with endpoint: "<NETWORKMANAGER_INVALID_ENDPOINT>", port: "<NETWORKMANAGER_TEST_PORT>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"endpoint": "<NETWORKMANAGER_INVALID_ENDPOINT>", "port": "<NETWORKMANAGER_TEST_PORT>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setstunendpoint_with_invalid_port"></a>
### TestCase Name
NetworkManager_SetStunEndpoint_With_Invalid_Port

### TestCase ID
NM_53

### TestCase Objective
Check if the SetStunEndpoint method throws an error when an invalid port parameter is passed

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetStunEndpoint With Invalid Port | Invoke SetStunEndpoint on org.rdk.NetworkManager with endpoint: "<NETWORKMANAGER_TEST_IPADDRESS>", port: "<NETWORKMANAGER_INVALID_PORT>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"endpoint": "<NETWORKMANAGER_TEST_IPADDRESS>", "port": "<NETWORKMANAGER_INVALID_PORT>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setstunendpoint_without_endpoint"></a>
### TestCase Name
NetworkManager_SetStunEndpoint_Without_Endpoint

### TestCase ID
NM_54

### TestCase Objective
Check if the SetStunEndpoint method throws an error when endpoint parameter is not passed

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetStunEndpoint Without Endpoint | Invoke SetStunEndpoint on org.rdk.NetworkManager with port: "<NETWORKMANAGER_TEST_PORT>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"port": "<NETWORKMANAGER_TEST_PORT>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setstunendpoint_without_port"></a>
### TestCase Name
NetworkManager_SetStunEndpoint_Without_Port

### TestCase ID
NM_55

### TestCase Objective
Check if the SetStunEndpoint method throws an error when port parameter is not passed

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetStunEndpoint Without Port | Invoke SetStunEndpoint on org.rdk.NetworkManager with endpoint: "<NETWORKMANAGER_TEST_IPADDRESS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint", "params": {"endpoint": "<NETWORKMANAGER_TEST_IPADDRESS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setstunendpoint_without_parameters"></a>
### TestCase Name
NetworkManager_SetStunEndpoint_Without_Parameters

### TestCase ID
NM_56

### TestCase Objective
Check if the SetStunEndpoint method throws an error when parameters are not passed

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetStunEndpoint Without Parameters | Invoke SetStunEndpoint on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetStunEndpoint"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_addtoknownssids_with_empty_ssid"></a>
### TestCase Name
NetworkManager_AddToKnownSSIDs_With_Empty_SSID

### TestCase ID
NM_57

### TestCase Objective
Check if the AddToKnownSSIDs method returns an error when the SSID parameter is empty

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | AddToKnownSSIDs With Empty SSID | Invoke AddToKnownSSIDs on org.rdk.NetworkManager with ssid: "", passphrase: "<WIFI_PASSPHRASE>", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs", "params": {"ssid": "", "passphrase": "<WIFI_PASSPHRASE>", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_addtoknownssids_with_empty_passphrase"></a>
### TestCase Name
NetworkManager_AddToKnownSSIDs_With_Empty_Passphrase

### TestCase ID
NM_58

### TestCase Objective
Check if the AddToKnownSSIDs method returns an error when the passphrase parameter is empty

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | AddToKnownSSIDs With Empty Passphrase | Invoke AddToKnownSSIDs on org.rdk.NetworkManager with ssid: "<WIFI_SSID_NAME>", passphrase: "", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs", "params": {"ssid": "<WIFI_SSID_NAME>", "passphrase": "", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_addtoknownssids_with_empty_ssid_passphrase"></a>
### TestCase Name
NetworkManager_AddToKnownSSIDs_With_Empty_SSID_Passphrase

### TestCase ID
NM_59

### TestCase Objective
Check if the AddToKnownSSIDs method returns an error when the SSID and passphrase parameters are empty

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | AddToKnownSSIDs With Empty SSID Passphrase | Invoke AddToKnownSSIDs on org.rdk.NetworkManager with ssid: "", passphrase: "", security: "<WIFI_SECURITY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs", "params": {"ssid": "", "passphrase": "", "security": "<WIFI_SECURITY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_addtoknownssids_without_parameters"></a>
### TestCase Name
NetworkManager_AddToKnownSSIDs_Without_Parameters

### TestCase ID
NM_60

### TestCase Objective
Check if the AddToKnownSSIDs method returns an error when parameters are not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | AddToKnownSSIDs Without Parameters | Invoke AddToKnownSSIDs on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.AddToKnownSSIDs"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setipsettings_with_empty_interface"></a>
### TestCase Name
NetworkManager_SetIPSettings_With_Empty_Interface

### TestCase ID
NM_61

### TestCase Objective
Check if the SetIPSettings method returns an error when the interface parameter is empty

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetIPSettings With Empty Interface | Invoke SetIPSettings on org.rdk.NetworkManager with interface: "", ipversion: "<NETWORKMANAGER_TEST_IPVERSION>", autoconfig: "<NETWORKMANAGER_TEST_AUTOCONFIG>", ipaddress: "<NETWORKMANAGER_TEST_IPADDRESS>", prefix: "<NETWORKMANAGER_TEST_PREFIX>", gateway: "<NETWORKMANAGER_TEST_GATEWAY>", primarydns: "<NETWORKMANAGER_TEST_PRIMARY_DNS>", secondarydns: "<NETWORKMANAGER_TEST_SECONDARY_DNS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setipsettings_with_invalid_interface"></a>
### TestCase Name
NetworkManager_SetIPSettings_With_Invalid_Interface

### TestCase ID
NM_62

### TestCase Objective
Check if the SetIPSettings method returns an error when the interface parameter is invalid

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetIPSettings With Invalid Interface | Invoke SetIPSettings on org.rdk.NetworkManager with interface: "invalid", ipversion: "<NETWORKMANAGER_TEST_IPVERSION>", autoconfig: "<NETWORKMANAGER_TEST_AUTOCONFIG>", ipaddress: "<NETWORKMANAGER_TEST_IPADDRESS>", prefix: "<NETWORKMANAGER_TEST_PREFIX>", gateway: "<NETWORKMANAGER_TEST_GATEWAY>", primarydns: "<NETWORKMANAGER_TEST_PRIMARY_DNS>", secondarydns: "<NETWORKMANAGER_TEST_SECONDARY_DNS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "invalid", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setipsettings_with_empty_ipversion"></a>
### TestCase Name
NetworkManager_SetIPSettings_With_Empty_Ipversion

### TestCase ID
NM_63

### TestCase Objective
Check if the SetIPSettings method returns an error when the ipversion parameter is empty

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetIPSettings With Empty Ipversion | Invoke SetIPSettings on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_TEST_INTERFACE>", ipversion: "", autoconfig: "<NETWORKMANAGER_TEST_AUTOCONFIG>", ipaddress: "<NETWORKMANAGER_TEST_IPADDRESS>", prefix: "<NETWORKMANAGER_TEST_PREFIX>", gateway: "<NETWORKMANAGER_TEST_GATEWAY>", primarydns: "<NETWORKMANAGER_TEST_PRIMARY_DNS>", secondarydns: "<NETWORKMANAGER_TEST_SECONDARY_DNS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setipsettings_with_invalid_ipversion"></a>
### TestCase Name
NetworkManager_SetIPSettings_With_Invalid_Ipversion

### TestCase ID
NM_64

### TestCase Objective
Check if the SetIPSettings method returns an error when the ipversion parameter is invalid

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetIPSettings With Invalid Ipversion | Invoke SetIPSettings on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_TEST_INTERFACE>", ipversion: "invalid", autoconfig: "<NETWORKMANAGER_TEST_AUTOCONFIG>", ipaddress: "<NETWORKMANAGER_TEST_IPADDRESS>", prefix: "<NETWORKMANAGER_TEST_PREFIX>", gateway: "<NETWORKMANAGER_TEST_GATEWAY>", primarydns: "<NETWORKMANAGER_TEST_PRIMARY_DNS>", secondarydns: "<NETWORKMANAGER_TEST_SECONDARY_DNS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "invalid", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setipsettings_with_invalid_ipaddress"></a>
### TestCase Name
NetworkManager_SetIPSettings_With_Invalid_Ipaddress

### TestCase ID
NM_65

### TestCase Objective
Check if the SetIPSettings method returns an error when the ipaddress parameter is invalid

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetIPSettings With Invalid Ipaddress | Invoke SetIPSettings on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_TEST_INTERFACE>", ipversion: "<NETWORKMANAGER_TEST_IPVERSION>", autoconfig: "<NETWORKMANAGER_TEST_AUTOCONFIG>", ipaddress: "<NETWORKMANAGER_INVALID_ENDPOINT>", prefix: "<NETWORKMANAGER_TEST_PREFIX>", gateway: "<NETWORKMANAGER_TEST_GATEWAY>", primarydns: "<NETWORKMANAGER_TEST_PRIMARY_DNS>", secondarydns: "<NETWORKMANAGER_TEST_SECONDARY_DNS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_INVALID_ENDPOINT>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setipsettings_with_invalid_gateway"></a>
### TestCase Name
NetworkManager_SetIPSettings_With_Invalid_Gateway

### TestCase ID
NM_66

### TestCase Objective
Check if the SetIPSettings method returns an error when the gateway parameter is invalid

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetIPSettings With Invalid Gateway | Invoke SetIPSettings on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_TEST_INTERFACE>", ipversion: "<NETWORKMANAGER_TEST_IPVERSION>", autoconfig: "<NETWORKMANAGER_TEST_AUTOCONFIG>", ipaddress: "<NETWORKMANAGER_TEST_IPADDRESS>", prefix: "<NETWORKMANAGER_TEST_PREFIX>", gateway: "<NETWORKMANAGER_INVALID_ENDPOINT>", primarydns: "<NETWORKMANAGER_TEST_PRIMARY_DNS>", secondarydns: "<NETWORKMANAGER_TEST_SECONDARY_DNS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_INVALID_ENDPOINT>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setipsettings_with_invalid_primarydns"></a>
### TestCase Name
NetworkManager_SetIPSettings_With_Invalid_PrimaryDNS

### TestCase ID
NM_67

### TestCase Objective
Check if the SetIPSettings method returns an error when the primarydns parameter is invalid

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetIPSettings With Invalid PrimaryDNS | Invoke SetIPSettings on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_TEST_INTERFACE>", ipversion: "<NETWORKMANAGER_TEST_IPVERSION>", autoconfig: "<NETWORKMANAGER_TEST_AUTOCONFIG>", ipaddress: "<NETWORKMANAGER_TEST_IPADDRESS>", prefix: "<NETWORKMANAGER_TEST_PREFIX>", gateway: "<NETWORKMANAGER_TEST_GATEWAY>", primarydns: "<NETWORKMANAGER_INVALID_ENDPOINT>", secondarydns: "<NETWORKMANAGER_TEST_SECONDARY_DNS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_INVALID_ENDPOINT>", "secondarydns": "<NETWORKMANAGER_TEST_SECONDARY_DNS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_setipsettings_with_invalid_secondarydns"></a>
### TestCase Name
NetworkManager_SetIPSettings_With_Invalid_SecondaryDNS

### TestCase ID
NM_68

### TestCase Objective
Check if the SetIPSettings method returns an error when the secondarydns parameter is invalid

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | SetIPSettings With Invalid SecondaryDNS | Invoke SetIPSettings on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_TEST_INTERFACE>", ipversion: "<NETWORKMANAGER_TEST_IPVERSION>", autoconfig: "<NETWORKMANAGER_TEST_AUTOCONFIG>", ipaddress: "<NETWORKMANAGER_TEST_IPADDRESS>", prefix: "<NETWORKMANAGER_TEST_PREFIX>", gateway: "<NETWORKMANAGER_TEST_GATEWAY>", primarydns: "<NETWORKMANAGER_TEST_PRIMARY_DNS>", secondarydns: "<NETWORKMANAGER_INVALID_ENDPOINT>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetIPSettings", "params": {"interface": "<NETWORKMANAGER_TEST_INTERFACE>", "ipversion": "<NETWORKMANAGER_TEST_IPVERSION>", "autoconfig": "<NETWORKMANAGER_TEST_AUTOCONFIG>", "ipaddress": "<NETWORKMANAGER_TEST_IPADDRESS>", "prefix": "<NETWORKMANAGER_TEST_PREFIX>", "gateway": "<NETWORKMANAGER_TEST_GATEWAY>", "primarydns": "<NETWORKMANAGER_TEST_PRIMARY_DNS>", "secondarydns": "<NETWORKMANAGER_INVALID_ENDPOINT>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_check_getavailableinterfaces_error"></a>
### TestCase Name
NetworkManager_Check_GetAvailableInterfaces_Error

### TestCase ID
NM_69

### TestCase Objective
Check if the GetAvailableInterfaces method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check GetAvailableInterfaces API Response | Invoke GetAvailableInterfaces on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_getprimaryinterface_error"></a>
### TestCase Name
NetworkManager_Check_GetPrimaryInterface_Error

### TestCase ID
NM_70

### TestCase Objective
Check if the GetPrimaryInterface method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check GetPrimaryInterface API Response | Invoke GetPrimaryInterface on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPrimaryInterface"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_getpublicip_error"></a>
### TestCase Name
NetworkManager_Check_GetPublicIP_Error

### TestCase ID
NM_71

### TestCase Objective
Check if the GetPublicIP method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check GetPublicIP API Response | Invoke GetPublicIP on org.rdk.NetworkManager with ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPublicIP", "params": {"ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_ping_error"></a>
### TestCase Name
NetworkManager_Check_Ping_Error

### TestCase ID
NM_72

### TestCase Objective
Check if the Ping method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Ping API Response | Invoke Ping on org.rdk.NetworkManager with endpoint: "<PING_IP>", ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Ping", "params": {"endpoint": "<PING_IP>", "ipversion": "IPv4", "count": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_trace_error"></a>
### TestCase Name
NetworkManager_Check_Trace_Error

### TestCase ID
NM_73

### TestCase Objective
Check if the Trace method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Trace API Response | Invoke Trace on org.rdk.NetworkManager with endpoint: "<TRACE_IP>", ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Trace", "params": {"endpoint": "<TRACE_IP>", "ipversion": "IPv4", "count": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_isconnectedtointernet_error"></a>
### TestCase Name
NetworkManager_Check_IsConnectedToInternet_Error

### TestCase ID
NM_74

### TestCase Objective
Check if the IsConnectedToInternet method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check IsConnectedToInternet API Response | Invoke IsConnectedToInternet on org.rdk.NetworkManager with ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": {"ipversion": "IPv4"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_getinterfacestate_error"></a>
### TestCase Name
NetworkManager_Check_GetInterfaceState_Error

### TestCase ID
NM_75

### TestCase Objective
Check if the GetInterfaceState method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check GetInterfaceState API Response | Invoke GetInterfaceState on org.rdk.NetworkManager with interface: "eth0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "eth0"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_setinterfacestate_error"></a>
### TestCase Name
NetworkManager_Check_SetInterfaceState_Error

### TestCase ID
NM_76

### TestCase Objective
Check if the SetInterfaceState method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check SetInterfaceState API Response | Invoke SetInterfaceState on org.rdk.NetworkManager with interface: "eth0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "eth0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_stopwifiscan_error"></a>
### TestCase Name
NetworkManager_Check_StopWiFiScan_Error

### TestCase ID
NM_77

### TestCase Objective
Check if the StopWiFiScan method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check StopWiFiScan API Response | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_check_wifidisconnect_error"></a>
### TestCase Name
NetworkManager_Check_WiFiDisconnect_Error

### TestCase ID
NM_78

### TestCase Objective
Check if the WiFiDisconnect method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of NetworkManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check WiFiDisconnect API Response | Invoke WiFiDisconnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="networkmanager_ssid_frequency_checker_2-4ghz"></a>
### TestCase Name
NetworkManager_SSID_Frequency_Checker_2.4GHz

### TestCase ID
NM_79

### TestCase Objective
Scan for 2.4GHz SSIDs and verify that all SSIDs listed in the onAvailableSSIDs event are on the 2.4GHz band

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan", "params": {"frequency": 2.4}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received with `2.4` found in the scanned SSID list |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |

---

<a id="networkmanager_ssid_frequency_checker_5ghz"></a>
### TestCase Name
NetworkManager_SSID_Frequency_Checker_5GHz

### TestCase ID
NM_80

### TestCase Objective
Scan for 5GHz SSIDs and verify that all SSIDs listed in the onAvailableSSIDs event are on the 5GHz band

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan", "params": {"frequency": 5}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received with `5` found in the scanned SSID list |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |

---

<a id="networkmanager_scan_specific_ssid_2-4ghz"></a>
### TestCase Name
NetworkManager_Scan_Specific_SSID_2.4GHz

### TestCase ID
NM_81

### TestCase Objective
This test case checks if NetworkManager can scan for a specific SSID on the 2.4GHz band and confirm its presence

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager with ssids: "<WIFI_SSID_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan", "params": {"frequency": 2.4, "ssids": "<WIFI_SSID_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |

---

<a id="networkmanager_scan_specific_ssid_5ghz"></a>
### TestCase Name
NetworkManager_Scan_Specific_SSID_5GHz

### TestCase ID
NM_82

### TestCase Objective
This test case checks if NetworkManager can scan for a specific SSID on the 5GHz band and confirm its presence

### TestCase Pre-condition

#### TestCase Pre-condition 1: Enable_Wifi_Interface

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Interface State | Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 2 | Set Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Set Interface State on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.SetInterfaceState", "params": {"interface": "wlan0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Interface State set successfully  |
| 3 | Get Interface State | *(Conditional statement executed only if previous step condition is met)*<br>Get Interface State from NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "wlan0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` `enabled` state returned  |
| 4 | Wifi Disconnect | Wi Fi Disconnect on NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiDisconnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi disconnected successfully  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Wifi Scan | Invoke StartWiFiScan on org.rdk.NetworkManager with ssids: "<WIFI_SSID_NAME_5GHZ>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StartWiFiScan", "params": {"frequency": 5, "ssids": "<WIFI_SSID_NAME_5GHZ>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan started successfully  |
| 2 | Check On AvailableSSIDs Event | Listen for Event_On_AvailableSSIDs event (wait 5s) | Ensure the `onAvailableSSIDs` event is received and the SSID list is validated |
| 3 | Stop Wifi Scan | Invoke StopWiFiScan on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.StopWiFiScan"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` WiFi Scan stopped successfully  |

---

<a id="networkmanager_trace_empty_endpoint"></a>
### TestCase Name
NetworkManager_Trace_Empty_Endpoint

### TestCase ID
NM_83

### TestCase Objective
Traces the empty endpoint

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Trace Empty Endpoint | Invoke Trace on org.rdk.NetworkManager with endpoint: "", ipversion: "IPv4"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Trace", "params": {"endpoint": "", "ipversion": "IPv4", "packets": 10}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_trace_without_parameter"></a>
### TestCase Name
NetworkManager_Trace_Without_Parameter

### TestCase ID
NM_84

### TestCase Objective
Check if the Trace method returns an error when parameters are not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Trace Without Parameter | Invoke Trace on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.Trace"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_wifi_connect_without_parameter"></a>
### TestCase Name
NetworkManager_Wifi_Connect_Without_Parameter

### TestCase ID
NM_85

### TestCase Objective
Check if the WifiConnect method returns an error when parameter is not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Wifi Connect Without Parameter | Invoke WiFiConnect on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.WiFiConnect"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="networkmanager_get_public_ipv6_ip"></a>
### TestCase Name
NetworkManager_Get_Public_IPv6_IP

### TestCase ID
NM_86

### TestCase Objective
Validate public IPv6 IP address of the device

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Public IPv6 IP | Invoke GetPublicIP on org.rdk.NetworkManager with ipversion: "IPv6"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPublicIP", "params": {"ipversion": "IPv6"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` public IP address returned  |

---

<a id="networkmanager_check_internet_ipv6_connectivity"></a>
### TestCase Name
NetworkManager_Check_Internet_IPv6_Connectivity

### TestCase ID
NM_87

### TestCase Objective
Seeks whether the device has internet connectivity

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Internet IPv6 Connectivity | Invoke IsConnectedToInternet on org.rdk.NetworkManager with ipversion: "IPv6"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": {"ipversion": "IPv6"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API returns `true` as the expected result  |

---

<a id="networkmanager_get_ipsettings_ipv6"></a>
### TestCase Name
NetworkManager_Get_IPSettings_IPv6

### TestCase ID
NM_88

### TestCase Objective
Gets the IP setting for the given interface

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get IPSettings | Invoke GetIPSettings on org.rdk.NetworkManager with interface: "<NETWORKMANAGER_INTERFACE_DETAILS>", ipversion: "IPv6"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetIPSettings", "params": {"interface": "<NETWORKMANAGER_INTERFACE_DETAILS>", "ipversion": "IPv6"}}' http://127.0.0.1:9998/jsonrpc` | Verify that IP settings are returned successfully |

---

<a id="networkmanager_check_primary_interface_after_lightsleep"></a>
### TestCase Name
NetworkManager_Check_Primary_Interface_After_LightSleep

### TestCase ID
NM_89

### TestCase Objective
Checks the primary interface after the device has been put in sleep mode and then woken up

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_System_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check power state | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Set Power State | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setPowerState on org.rdk.System with standbyReason: "<value>", powerState: "ON"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the power state is set successfully |
| 3 | Get Device Interfaces | Invoke GetAvailableInterfaces on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetAvailableInterfaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that the available interfaces are returned successfully |
| 4 | Get Primary/Default Interface | Invoke GetPrimaryInterface on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPrimaryInterface"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` returned `interface` is one of the values retrieved in step 3  |
| 5 | Set Power State | Invoke setPowerState on org.rdk.System with standbyReason: "<value>", powerState: "STANDBY"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the power state is set successfully |
| 6 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned power state is `STANDBY` as expected  |
| 7 | Set Power State | Invoke setPowerState on org.rdk.System with standbyReason: "<value>", powerState: "ON"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the power state is set successfully |
| 8 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned power state is `ON` as expected  |
| 9 | Get Primary/Default Interface | Invoke GetPrimaryInterface on org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.GetPrimaryInterface"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` primary interface matches value from step 4  |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check power state | Get Power State from System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Set Power State | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the power state is set successfully |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onInterfaceStateChange event | Unregister the WebSocket event listener for `onInterfaceStateChange` to stop receiving `onInterfaceStateChange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.unregister", "params": {"event": "onInterfaceStateChange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the onAvailableSSIDs event | Unregister the WebSocket event listener for `onAvailableSSIDs` to stop receiving `onAvailableSSIDs` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.unregister", "params": {"event": "onAvailableSSIDs", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 3 | Unsubscribe from the onWiFiStateChange event | Unregister the WebSocket event listener for `onWiFiStateChange` to stop receiving `onWiFiStateChange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.NetworkManager.1.unregister", "params": {"event": "onWiFiStateChange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 4 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 20 mins

**Priority** : Medium

**Release Version** : M133

<div align="right"><a href="#testscript-name">Go to Top</a></div>
