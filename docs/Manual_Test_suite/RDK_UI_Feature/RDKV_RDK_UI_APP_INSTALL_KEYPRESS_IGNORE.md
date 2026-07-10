## TestCase ID
RDKV_MANUAL_RDKUI_27
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_APP_INSTALL_KEYPRESS_IGNORE

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that any user key presses on an app tile while the application is in the download/installation state are ignored without causing errors.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | In recommended apps, press on an | In Recommended Apps, press on an app tile which is not yet installed | It should start downloading the app and a buffering/loading icon should be displayed on the app tile |
| 2 | Press downloading app tile again (expect ignore) | Before download completes, press on the same app tile again | The key press should be ignored and no error should come |
| 3 | Open More Apps page | Press on More Apps | Page should load with all available apps in App Catalogue |
| 4 | In recommended apps, press on an | In Recommended Apps, press on an app tile which is not yet installed | It should start downloading the app and a buffering/loading icon should be displayed on the app tile |
| 5 | Press downloading app tile again (expect ignore) | Before download completes, press on the same app tile again | The key press should be ignored and no error should come |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
