## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_10
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Max_Running_Apps

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate and retrieve the maximum number of applications that can be maintained in the running or suspended state using the GetMaxRunningApps property. This test exercises the `org.rdk.AppManager` plugin (including APIs such as `clearAppData`, `launchApp`, and `getAppStatus`) and the RDK UI Home screen navigation to drive the application lifecycle. The test confirms that maxRunningApps should be in running or suspended state. No Apps should terminate or relaunched.

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
| 1 | Query getMaxRunningApps via API | Execute the below curl command to gets the maximum number of apps to maintain in the running or suspended state : <br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 24, "method": "org.rdk.AppManager.getMaxRunningApps"}' http://127.0.0.1:9998/jsonrpc` | The `getMaxRunningApps` API should return a successful response containing the `maxRunningApps` value, indicating the maximum number of apps the AppManager plugin can maintain in the running or suspended state.|
| 2 | Launch app from Recommended/My Apps | Select the App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should be launched successfully  (Either cold launch /hot launch based on the app's previous state)|
| 3 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content|
| 4 | Press Home key to suspend app | Press Home key from remote on the launched Apps | App should not terminate but goes to a suspended state|
| 5 | Repeat launch/suspend steps up to maxRunningApps | Repeat the steps 3 - 5 on other installed Apps upto the same count of maxRunningApps in step 2 | Expected Response should be same as step 3 -5 for maxRunningApps|
| 6 | Verify maxRunningApps maintained in running/suspended state | Validate that upto maxRunningApps is maintained in the running or suspended state | maxRunningApps should be in running or suspended state. No Apps should terminate or relaunched|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
