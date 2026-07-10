# Performance Validation Suite (PERF) — Requirements

> **Suite:** Performance Validation Suite (PERF) | **Req ID Prefix:** `PERF-REQ`
> **Source specs:** [tdk-core/docs/rdkv_performance](https://github.com/rdkcentral/tdk-core/tree/main/docs/rdkv_performance) (100 test cases)
> **Total requirements:** 20

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | Functional Capability | Classification | # Tests | Test Cases |
|--------|-----------------------|----------------|---------|------------|
| PERF-REQ-001 | AppManager — App launch time latency | Timing (AppManager) | 7 | RDKV_CERT_PVS_AppManager_TimeTo_Launch_App, RDKV_CERT_PVS_AppManager_TimeTo_LaunchAfterReboot, RDKV_CERT_PVS_AppManager_TimeTo_LaunchApp_LifeCycle, RDKV_CERT_PVS_AppManager_TimeTo_LoadApp, RDKV_CERT_PVS_AppManager_TimeToRelaunchApp, RDKV_CERT_PVS_AppManager_TimeToRepeatedLaunch, RDKV_CERT_PVS_AppManager_TimeToRunApplication |
| PERF-REQ-002 | AppManager — App termination, close, and kill time latency | Timing (AppManager) | 6 | RDKV_CERT_PVS_AppManager_TimeTo_CloseApp, RDKV_CERT_PVS_AppManager_TimeTo_Terminate_App, RDKV_CERT_PVS_AppManager_TimeTo_TerminateApp_LifeCycle, RDKV_CERT_PVS_AppManager_TimeTo_Kill_App, RDKV_CERT_PVS_AppManager_TimeTo_KillApp_LifeCycle, RDKV_CERT_PVS_AppManager_TimeToTerminateFromBackground |
| PERF-REQ-003 | AppManager — App state transition time latency | Timing (AppManager) | 5 | RDKV_CERT_PVS_AppManager_TimeTo_ResumeApp, RDKV_CERT_PVS_AppManager_TimeTo_SetFocus, RDKV_CERT_PVS_AppManager_TimeTo_SetVisible_App, RDKV_CERT_PVS_AppManager_TimeTo_onHidden_App, RDKV_CERT_PVS_AppManager_TimeToSwitchBetweenApps |
| PERF-REQ-004 | AppManager — App package management time | Timing (AppManager) | 3 | RDKV_CERT_PVS_AppManager_TimeTo_Download_AppBundle, RDKV_CERT_PVS_AppManager_TimeTo_Install_App, RDKV_CERT_PVS_AppManager_TimeTo_Uninstall_App |
| PERF-REQ-005 | AppManager — Resource usage during app lifecycle operations | Resource Usage (AppManager) | 14 | RDKV_CERT_PVS_AppManager_ResourceUsage_Launch_App, RDKV_CERT_PVS_AppManager_ResourceUsage_Relaunch, RDKV_CERT_PVS_AppManager_ResourceUsage_Runtime_App, RDKV_CERT_PVS_AppManager_ResourceUsage_SteadyState, RDKV_CERT_PVS_AppManager_ResourceUsage_Kill_Relaunch_App, RDKV_CERT_PVS_AppManager_ResourceUsage_AppStartupVsIdle, RDKV_CERT_PVS_AppManager_ResourceUsage_ClearAppData, RDKV_CERT_PVS_AppManager_ResourceUsage_CloseApp, RDKV_CERT_PVS_AppManager_ResourceUsage_Kill_App, RDKV_CERT_PVS_AppManager_ResourceUsage_Terminate_App, RDKV_CERT_PVS_AppManager_ResourceUsage_SwitchApp, RDKV_CERT_PVS_AppManager_ResourceUsage_Download_AppBundle, RDKV_CERT_PVS_AppManager_ResourceUsage_Install_App, RDKV_CERT_PVS_AppManager_ResourceUsage_Uninstall_App |
| PERF-REQ-006 | AppManager — App lifecycle state validation | Lifecycle (AppManager) | 3 | RDKV_CERT_PVS_AppManager_LaunchApp_LifeCycle, RDKV_CERT_PVS_AppManager_CloseApp_LifeCycle, RDKV_CERT_PVS_AppManager_TerminateApp_LifeCycle |
| PERF-REQ-007 | AppManager — Stability under repeated install, uninstall, and launch operations | Stability (AppManager) | 4 | RDKV_CERT_PVS_AppManager_MultipleLaunchRequests_StressTest, RDKV_CERT_PVS_AppManager_InstallAppTwice_Stability, RDKV_CERT_PVS_AppManager_UninstallApp_StabilityCheck, RDKV_CERT_PVS_AppManager_UninstallLaunchedApp_Stability |
| PERF-REQ-008 | Apps — Resource usage during launch and video playback | Resource Usage (Apps) | 4 | RDKV_CERT_PVS_Apps_ResourceUsage_Launch, RDKV_CERT_PVS_Apps_ResourceUsage_Video_4K_DASH, RDKV_CERT_PVS_Apps_ResourceUsage_Video_4K_HLS, RDKV_CERT_PVS_Apps_ResourceUsage_Video_MP4 |
| PERF-REQ-009 | Apps — App launch time | Timing (Apps) | 2 | RDKV_CERT_PVS_Apps_TimeTo_Launch, RDKV_CERT_PVS_Apps_WiFi_TimeTo_Launch |
| PERF-REQ-010 | Apps — Video PlayPause response time across codecs | Timing (Apps) | 18 | RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_4K_AV1, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_4K_DASH, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_4K_HLS, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_4K_MKV, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_4K_VP9, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_AAC, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_AC3, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_AV1, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_Dash_H264, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_Direct_Vorbis, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_Direct_WEBM, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_EC3, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_HDR, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_HEVC, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_HLS_H264, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_MP4, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_VP9, RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_Vorbis |
| PERF-REQ-011 | Browser — JavaScript engine and rendering performance benchmarks | Performance Benchmark | 6 | RDKV_CERT_PVS_Browser_Animation_FPS, RDKV_CERT_PVS_Browser_CSS3, RDKV_CERT_PVS_Browser_Kraken, RDKV_CERT_PVS_Browser_MotionMark, RDKV_CERT_PVS_Browser_Octane, RDKV_CERT_PVS_Browser_Speedometer |
| PERF-REQ-012 | Platform — Boot and standby transition timing | Timing (Platform) | 3 | RDKV_CERT_PVS_Functional_TimeTo_ColdBoot, RDKV_CERT_PVS_Functional_TimeTo_StandbyToOn, RDKV_CERT_PVS_Functional_TimeTo_OnToStandby |
| PERF-REQ-013 | Platform — Functional operation timing (channel change, resolution, key response, factory reset) | Timing (Platform) | 4 | RDKV_CERT_PVS_Functional_TimeTo_ChannelChange, RDKV_CERT_PVS_Functional_TimeTo_ChangeResolution, RDKV_CERT_PVS_Functional_TimeTo_GetKeys, RDKV_CERT_PVS_Functional_TimeTo_UserFactory_ResetDevice |
| PERF-REQ-014 | Bluetooth — scan timing and resource usage | Timing / Resource Usage (Bluetooth) | 2 | RDKV_CERT_PVS_Functional_TimeTo_Scan_Bluetooth, RDKV_CERT_PVS_Functional_ResourceUsage_BluetoothConnection |
| PERF-REQ-015 | WiFi — scan timing and resource usage (2.4 GHz and 5 GHz) | Timing / Resource Usage (WiFi) | 4 | RDKV_CERT_PVS_Functional_TimeTo_Scan_WiFi, RDKV_CERT_PVS_Functional_ResourceUsage_WiFiConnection, RDKV_CERT_PVS_Functional_ResourceUsage_WiFiConnection_5GHZ, RDKV_CERT_PVS_Apps_WiFi_ResourceUsage_Launch |
| PERF-REQ-016 | Platform — system resource usage during monitoring and browser launch | Resource Usage (Platform) | 2 | RDKV_CERT_PVS_Functional_ResourceUsage_TopCommand, RDKV_CERT_PVS_Functional_ResourceUsage_WebkitBrowser_Launch_StandbyToOn |
| PERF-REQ-017 | Platform — Network performance validation | Network (Platform) | 2 | RDKV_CERT_PVS_Functional_Ping_Performance, RDKV_CERT_PVS_Functional_ValidateIPAddress |
| PERF-REQ-018 | Platform — WiFi persistence and channel change performance | Network (Platform) | 2 | RDKV_CERT_PVS_Functional_WiFi_PersistenceOnBoot, RDKV_CERT_PVS_Functional_WiFi_TimeTo_ChannelChange |
| PERF-REQ-019 | Platform — System health validation | System Health | 6 | RDKV_CERT_PVS_Functional_Check_FailedServices, RDKV_CERT_PVS_Functional_Device_MaxResponseTime, RDKV_CERT_PVS_Functional_DiskUsage, RDKV_CERT_PVS_Functional_IOWait_Time, RDKV_CERT_PVS_Functional_Zombie_Processes, RDKV_CERT_PVS_LogSize_Validation |
| PERF-REQ-020 | WebKitBrowser — Memory usage and stability during video playback | Resource Usage / Stability | 3 | RDKV_CERT_PVS_WebKitBrowser_Video_Playback_MemoryUsage_WithWebinspect, RDKV_CERT_PVS_WebKitBrowser_Video_Playback_Without_Crash_WithWebinspect, RDKV_CERT_PVS_Functional_WebKitBrowser_Reboot_OnLoadURL |
| | **Total** | | **100** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `PERF-REQ-001` | SHALL complete app launch from request to ready state within the defined time-to-launch threshold, covering cold launch, warm relaunch, launch after reboot, load-to-run sequence, and repeated launch operations. |
| `PERF-REQ-002` | SHALL complete app close, terminate, and kill operations within the defined time thresholds across all lifecycle states, including termination from the background state. |
| `PERF-REQ-003` | SHALL complete app state transitions — resume from suspended state, set focus, set visible, set hidden, and switch between apps — within the defined time thresholds. |
| `PERF-REQ-004` | SHALL complete app bundle download, install, and uninstall operations within the defined time thresholds. |
| `PERF-REQ-005` | SHALL maintain CPU and memory resource usage within defined bounds during all AppManager lifecycle operations — including launch, relaunch, steady-state runtime, kill-relaunch, switch, close, terminate, kill, install, uninstall, clear data, and startup-versus-idle comparison. |
| `PERF-REQ-006` | SHALL validate that app lifecycle state transitions for launch, close, and terminate complete without error and reach the expected final state as reported by AppManager. |
| `PERF-REQ-007` | SHOULD complete repeated install, uninstall, and multiple simultaneous launch request operations without failure or resource exhaustion across the defined iteration count. |
| `PERF-REQ-008` | SHALL maintain CPU and memory resource usage within defined bounds during app launch and during 4K DASH, 4K HLS, and MP4 video playback sessions. |
| `PERF-REQ-009` | SHALL complete app launch within the defined time-to-launch threshold on both a local network and a WiFi connection. |
| `PERF-REQ-010` | SHALL complete PlayPause operations within the defined response time threshold across H.264 (DASH/HLS), HEVC, AV1, VP9, HDR, EC3, AC3, AAC, MP4, Vorbis, WebM, and 4K (AV1/DASH/HLS/MKV/VP9) content. |
| `PERF-REQ-011` | SHOULD meet defined performance benchmark scores for JavaScript engine throughput (Octane, Kraken, Speedometer 2.0), CSS3 animation, rendering throughput (MotionMark), and animation frame rate in the WPEWebkit browser. |
| `PERF-REQ-012` | SHALL complete platform cold boot, standby-to-on wake, and on-to-standby entry within the defined time thresholds. |
| `PERF-REQ-013` | SHALL complete channel change, display resolution change, key press response delivery, and factory reset operations within the defined time thresholds. |
| `PERF-REQ-014` | SHALL complete a Bluetooth device scan within the defined time threshold and maintain CPU and memory resource usage within defined bounds during a Bluetooth connection. |
| `PERF-REQ-015` | SHALL complete a Wi-Fi network scan within the defined time threshold, maintain CPU and memory resource usage within defined bounds during 2.4 GHz and 5 GHz Wi-Fi connections, and maintain resource usage within bounds during app launch over WiFi. |
| `PERF-REQ-016` | SHALL maintain CPU and memory resource usage within defined bounds during system process monitoring and during a WPEWebkit browser launch triggered by a standby-to-on transition. |
| `PERF-REQ-017` | SHALL achieve network round-trip time within the defined ping latency threshold and confirm a valid IP address is assigned within the defined time after network attach. |
| `PERF-REQ-018` | SHALL persist WiFi connection configuration across a device reboot and complete a WiFi channel change within the defined time threshold. |
| `PERF-REQ-019` | SHALL report no failed services beyond the defined threshold, respond to device queries within the maximum response time limit, maintain disk usage within limits, sustain I/O wait below the defined threshold, produce zero zombie processes, and keep log file sizes within defined limits. |
| `PERF-REQ-020` | SHALL sustain WPEWebkit browser video playback within the defined memory footprint limit, complete playback without crash under WebInspector monitoring, and complete a browser URL-load following a reboot without error. |
