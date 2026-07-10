# RDK Services — NetworkManager Plugin Requirements

> **Module:** NetworkManager (`org.rdk.NetworkManager.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_NetworkManager.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_NetworkManager.md)
> **Total requirements:** 9 | **Total test cases:** 52

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | Functional Capability | Classification | # Tests | Test Cases |
|--------|----------------------|----------------|---------|------------|
| RDKSVC-REQ-001 | Network interface listing and state management | Interface API | 13 | NetworkManager_Get_Device_Interfaces, NetworkManager_Get_Primary/Default_Interface, NetworkManager_GetAvailableInterfaces_With_Enabled/Disabled_Interface, NetworkManager_Get_Interface_State, NetworkManager_SetandGet_Interface_State, NetworkManager_SetInterfaceState_Without_Enable_Parameter, NetworkManager_SetInterfaceState_Without_Parameter, NetworkManager_GetInterfaceState_With_Invalid_Parameter, NetworkManager_Set_Invalid_Interface_State, NetworkManager_GetInterfaceState_With_Empty_Parameter, NetworkManager_GetInterfaceState_Without_Parameter, NetworkManager_SetInterfaceState_Without_Interface_Parameter, NetworkManager_SetInterfaceState_With_Invalid_Parameters |
| RDKSVC-REQ-002 | IP address validation, ping, traceroute, and internet connectivity | Connectivity API | 7 | NetworkManager_Validate_Public_IPv4_IP, NetworkManager_Ping_IPv4_Endpoint, NetworkManager_Trace_IPv4_Endpoint, NetworkManager_Check_Internet_IPv4_Connectivity, NetworkManager_Ping_Invalid_Endpoint, NetworkManager_Ping_Endpoint_With_Invalid_IPVersion, NetworkManager_GetIPSettings_With_Invalid_Parameter |
| RDKSVC-REQ-003 | Wi-Fi network scan and SSID discovery | WiFi Scan API | 4 | NetworkManager_Wifi_Start_Stop_Scan, NetworkManager_Check_On_AvailableSSIDs_Event, NetworkManager_Check_On_AvailableSSIDs_Event_Not_Triggered, NetworkManager_Start_Scan_And_Check_Wifi_State |
| RDKSVC-REQ-004 | Wi-Fi connection and disconnection management | WiFi Connection API | 7 | NetworkManager_Wifi_Connect_Disconnect, NetworkManager_Check_Get_Connected_SSID, NetworkManager_Get_Supported_Security_Modes, NetworkManager_Check_WifiConnect_With_Invalid_SSID_Passphrase, NetworkManager_5GHz_Wifi_Connect_Disconnect, NetworkManager_Check_5GHz_Get_Connected_SSID, NetworkManager_Verify_Wifi_Connect_Error |
| RDKSVC-REQ-005 | Wi-Fi connection state monitoring and events | WiFi State API | 6 | NetworkManager_Check_On_WifiStateChange_Event, NetworkManager_Check_Wifi_State, NetworkManager_Connect_Wifi_And_Check_Wifi_State, NetworkManager_Check_Wifi_State_After_Connecting_To_Wifi, NetworkManager_Check_Wifi_State_On_Connecting_To_Invalid_Wifi_SSID, NetworkManager_Check_WiFi_StateChange_Event_On_Connecting_To_Wifi |
| RDKSVC-REQ-006 | Known Wi-Fi network list management | SSID Management API | 4 | NetworkManager_Add_and_Remove_SSID, NetworkManager_Check_Get_Known_SSID, NetworkManager_Remove_Invalid_SSID, NetworkManager_Remove_Empty_SSID |
| RDKSVC-REQ-007 | STUN endpoint and connectivity test endpoint configuration | Endpoint Configuration API | 5 | NetworkManager_SetandGet_Stun_Endpoint, NetworkManager_SetStunEndpoint_With_Invalid_Endpoint, NetworkManager_Set_Single_Connectivity_Test_Endpoints, NetworkManager_Set_Five_Connectivity_Test_Endpoints, NetworkManager_SetandGet_Connectivity_Test_Endpoints |
| RDKSVC-REQ-008 | Diagnostic log verbosity control | Logging API | 4 | NetworkManager_Check_Logging_Level, NetworkManager_Set_Lowest_Logging_Level, NetworkManager_Set_Mid-range_Logging_Level, NetworkManager_Set_Highest_Logging_Level |
| RDKSVC-REQ-009 | Interface state change and plugin lifecycle event notifications | Event API | 2 | NetworkManager_Check_On_Interface_StateChange_Event, NetworkManager_ActivateDeactivate_Event_Test |
| | **Total** | | **52** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL report all available network interfaces with their type and enabled state, identify the primary interface, and return correct error responses for interface state change requests with missing enable parameter, missing parameters, invalid state values, empty parameter, missing interface identifier, and invalid parameter combinations. |
| `RDKSVC-REQ-002` | SHALL confirm the device's public IPv4 address is reachable, send and receive ping and traceroute responses to a valid IPv4 endpoint, verify internet connectivity, and return correct error responses for ping requests with an invalid endpoint, unsupported IP version, and for IP settings queries with invalid parameters. |
| `RDKSVC-REQ-003` | SHALL start and stop a Wi-Fi network scan, notify of discovered SSIDs on scan completion, suppress the notification when no new networks are detected, and correctly report the Wi-Fi operational state during an active scan. |
| `RDKSVC-REQ-004` | SHALL connect and disconnect the device from 2.4 GHz and 5 GHz Wi-Fi networks, report the currently connected SSID after a successful connection, list the supported Wi-Fi security modes, and return correct error responses for connection attempts with an invalid SSID or passphrase and for general connection failures. |
| `RDKSVC-REQ-005` | SHALL report the current Wi-Fi connection state, reflect correct state transitions when connecting to a valid network, attempting to connect to an invalid network, and after a connection is established, and fire a state change notification with correct payload when the Wi-Fi connection state changes. |
| `RDKSVC-REQ-006` | SHALL add and remove networks from the device's known Wi-Fi network list, retrieve the current list of known networks, and return correct error responses for remove requests with an invalid and an empty network identifier. |
| `RDKSVC-REQ-007` | SHALL configure STUN endpoint settings and retrieve the configured value, set single and multiple (up to five) connectivity test endpoint addresses, retrieve configured connectivity test endpoints, and return a correct error response for STUN configuration requests with an invalid endpoint value. |
| `RDKSVC-REQ-008` | SHALL control the network manager diagnostic log verbosity, supporting lowest, mid-range, and highest log levels, and retrieve the currently active log level with a correct response. |
| `RDKSVC-REQ-009` | SHALL fire a network interface state change notification with the correct interface identifier and updated state when a network interface changes state, and fire a plugin state change notification with correct state during network manager activation and deactivation. |
