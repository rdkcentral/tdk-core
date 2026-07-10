## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_07
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_CLEAR_ALL_APPS_DATA

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that user account logins for all installed applications (YouTube, Amazon Prime Video, Netflix, etc.) are cleared after the clearAllAppData API call.

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
| 1 | Verify YouTube app is installed | Validate that YouTube App is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If YouTube is not installed follow the instructions of Pre condition 4 | YouTube App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage. |
| 2 | Verify Amazon Prime app is installed | Validate that Amazon Prime App is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If Amazon Prime is not installed follow the instructions of Pre condition 4 | Amazon Prime App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage. |
| 3 | Verify other user-login apps are installed | Validate that other Apps (User login required Apps) is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If Other Apps are not installed follow the instructions of Pre condition 4 | Other App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage. |
| 4 | Clear all installed app data via clearAllAppData API | Clear all the installed App data using the clearAllAppData API by executing below curl command  :<br>curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 0, "method": "org.rdk.AppManager.clearAllAppData"}' http://127.0.0.1:9998/jsonrpc | Expected response should be like below :<br>{"jsonrpc":"2.0","id":1,"result":null} |
| 5 | Launch all installed apps one by one | Launch all the installed Apps one by one from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | All the installed Apps should be launched succesfully (cold launch) |
| 6 | Validate all apps show sign in page | Validate that All the Apps have Sign in page is loaded or not | All installed Apps sign in page should be loaded indicating successful clear data on all apps |
| 7 | Sign in to all apps and verify A/V playback | Sign in with a valid user credentials and Check the AV playback of all tha Apps | Sign in should be successful and App AV playback should happen as expected / without errors on all the Apps |
| 8 | Close apps via Back key | Close/Exit the Apps by back key press on remote. | All Apps should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
