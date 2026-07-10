## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_14
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_PKG_LOCK_PREVENT_UPDATE

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that calling PackageManager.lock via the AppManager successfully prevents the locked package from being updated.

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
| 4 | Attempt to uninstall active app (expect failure) | Execute the below curl commands to Uninstall the Active App :<br>curl -d '{ "jsonrpc": 2.0, "id": 15, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": { "packageId": "<Package_name>" } }' http://127.0.0.1:9998/jsonrpc | App uninstallation should failed and Expected API response should be like below :<br>{"jsonrpc":"2.0","id":1002,"error":{"code":1,"message":"ERROR_GENERAL"}} |
| 5 | Verify active app functionality is unaffected | Validate that App playback or functionality got affected or not | Active App functionality shouldn't get affected and App shouldn't close unexpectedly or playback should not close |
| 6 | Close apps via Back key | Close/Exit the Apps by back key press on remote and Validate that App still available in MyApps | App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.. App should be available in MyApps Tab |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
