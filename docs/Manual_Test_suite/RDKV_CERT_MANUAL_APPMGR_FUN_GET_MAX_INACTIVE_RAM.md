## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_13
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_GET_MAX_INACTIVE_RAM

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate and retrieve the maximum RAM available for inactive applications (in mebibytes) using the maxInactiveRamUsage property.

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
| 1 | Verify required apps are installed | Validate that required Apps is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If required Apps are not installed follow the instructions of Pre condition 4 | Required Apps should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage. |
| 2 | Launch app from Recommended/My Apps | Select the App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should be launched succesfully  (Either cold launch /hot launch based on the app's previous state) |
| 3 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content |
| 4 | Press Home key to suspend app | Press Home key from remote on the launched Apps | App should not terminate but goes to Hibernated state or puts the app in background as inactive |
| 5 | Repeat launch/suspend steps for other apps | Repeat the steps 2 - 4 on other installed Apps | Expected Response should be same as step 2 -4 |
| 6 | Query getMaxInactiveRamUsage via API | Execute the below curl command to gets max amount of ram available for inactive apps (in mebibytes) :<br>curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 23, "method": "org.rdk.AppManager.getMaxInactiveRamUsage"}' http://127.0.0.1:9998/jsonrpc | Expected API Response should be like below :<br>{ "jsonrpc": 2.0, "id": 24, "result": {"maxInactiveRamUsage": 0 } } , Which indicates max ram available for inactive apps (in mebibytes) |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
