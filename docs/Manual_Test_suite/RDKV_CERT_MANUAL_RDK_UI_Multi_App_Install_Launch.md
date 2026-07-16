## TestCase ID
RDKV_MANUAL_RDKUI_23
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Multi_App_Install_Launch

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that multiple apps can be downloaded and installed, that all installed apps are listed in the My Apps row, and that horizontal navigation within the My Apps row is supported. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that horizontal navigation should be possible.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Ensure stable network connection | Ensure a stable network connection is available on the DUT. | The DUT should have a stable network connection. |
| 3 | Ensure at least one app is installed | Ensure at least one app is already installed on the DUT. | At least one app should be installed and visible in the My Apps section. |
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Select and install app from Recommended Apps | In Recommended Apps row, select an app which is not currently installed | A buffering/loading indicator should be displayed on the app tile |
| 2 | Wait and verify installation completes with tick | Wait for sometime and check for the behavior on App tile | After sometime, buffering/loading icon will disappear and a green tick mark should appear on the tile for 2 to 3 seconds, indicating that the app is successfully installed |
| 3 | Verify My Apps row appears after installation | Check the change happened in RDK UI Home screen after successful installation of the App | The newly installed APP should be listed in My Apps row along with already installed Apps |
| 4 | Repeat install steps for another app | Perform steps 1 to 3 one more time | Expected results should be similar to steps 1 to 3 |
| 5 | Navigate to More Apps page | Click on More Apps button | Page should load with all available apps in App Catalogue |
| 6 | Select and install app from More Apps | Select an app which is not currently installed | A buffering/loading indicator should be displayed on the app tile |
| 7 | Wait and verify installation completes with tick | Wait for sometime and check for the behavior on App tile | After sometime, buffering/loading icon will disappear and a green tick mark should appear on the tile for 2 to 3 seconds, indicating that the app is successfully installed |
| 8 | Press Back button on remote | Press back button from Remote | RDK UI Home screen should load with My Apps row populated with the installed Apps |
| 9 | Verify horizontal navigation in My Apps | Try navigating horizontally among the installed apps in My Apps section | Horizontal navigation should be possible |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
