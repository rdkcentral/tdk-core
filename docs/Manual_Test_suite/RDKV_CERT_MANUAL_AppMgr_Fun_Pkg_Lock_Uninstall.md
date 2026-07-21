## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_14
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Pkg_Lock_Uninstall

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the package lock mechanism on the DUT prevents an active or locked application from being uninstalled while it is in use. This test confirms that the uninstall operation is correctly rejected and the application remains fully functional and accessible, ensuring that package protection controls work as intended for operational compliance.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 4 | Install required apps if not present | If the required App is not already installed, select the App tile from the Recommended Apps row (or the More Apps tab if not visible on Recommended row) of the RDK UI Home screen and press Enter/OK to install it. Skip this step if the required App is already available in the My Apps section. | The required App should be installed and available in the My Apps section/row of the RDK UI Home screen, ready to launch. If already installed, this step may be skipped.|
| 5 | Sign in to premium apps if applicable | This step is applicable only if the required App is a Premium App (such as YouTube, Amazon Prime, or Netflix). If applicable, sign in with valid user credentials and verify AV playback prior to test execution. | If the required App is a Premium App, it should be signed in with valid user credentials and AV playback should be verified successfully prior to test execution.|
| 6 | Verify app launch and AV playback | Verify that all required Apps are launching successfully from the RDK UI Home screen. For Apps that support A/V playback (regardless of whether the App is a Premium App or not), verify that audio and video playback is working correctly prior to test execution. | All required Apps should launch successfully from the RDK UI Home screen. For Apps supporting A/V playback, audio and video playback should be verified as working correctly prior to test execution.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch app from Recommended/My Apps | Select the App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should be launched successfully  (Either cold launch /hot launch based on the app's previous state)|
| 2 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content|
| 3 | Attempt to uninstall active app (expect failure) | Execute the below curl commands to Uninstall the Active App :<br>`curl -d '{ "jsonrpc": 2.0, "id": 15, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": { "packageId": "<Package_name>" } }' http://127.0.0.1:9998/jsonrpc` | The uninstall API should return an error response, confirming that active or locked packages cannot be uninstalled while in use.|
| 4 | Verify active app functionality is unaffected | Validate that App playback or functionality got affected or not | Active App functionality shouldn't get affected and App shouldn't close unexpectedly or playback should not close|
| 5 | Close apps via Back key | Close/Exit the Apps by back key press on remote and Validate that App still available in MyApps | App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. App should be available in MyApps Tab|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
