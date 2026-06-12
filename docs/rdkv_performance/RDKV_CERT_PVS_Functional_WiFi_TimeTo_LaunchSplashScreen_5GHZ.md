## TestCase ID
RDKV_PERFORMANCE_49
## TestCase Name
RDKV_CERT_PVS_Functional_WiFi_TimeTo_LaunchSplashScreen_5GHZ
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to display the splash screen during 5GHz WiFi-connected device boot is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|Device must be capable of rebooting and connecting via 5GHz WiFi.|
|2|`WIFI_5GHZ_SPLASH_SCREEN_THRESHOLD` must be configured in device config.|
|3|5GHz WiFi credentials must be configured in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Record Start Time | Record UTC timestamp when device reboot is initiated via `Controller.1.harakiri`. | Start time recorded. |
| 2 | Reboot Device via 5GHz WiFi | Reboot the device while connected via 5GHz WiFi. | Device begins rebooting. |
| 3 | Monitor for Splash Screen | Monitor the device display for the appearance of the splash screen. | Splash screen appears. |
| 4 | Record Splash Screen Time | Record UTC timestamp when the splash screen is first displayed. | End time recorded. |
| 5 | Validate Time | Calculate splash screen display time = end timestamp - start timestamp. Compare against threshold. | Time to launch splash screen during 5GHz WiFi-connected boot is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M89<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
