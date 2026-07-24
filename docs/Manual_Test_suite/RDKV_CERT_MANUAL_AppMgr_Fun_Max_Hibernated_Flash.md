## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_12
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Max_Hibernated_Flash

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the maximum flash storage available for hibernated applications as reported by the AppManager on the DUT. This test confirms that the flash usage limit is correctly retrieved and reflects the expected storage boundary, ensuring that storage resource management for hibernated applications meets certification requirements.

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
| 1 | Launch app from Recommended/My Apps | Select the App tile from the My Apps/Recommended Apps section/row of RDK UI Home screen and press Enter/OK on the remote | Selected App should be launched successfully  either as a cold launch or hot launch depending on the app's previous state.|
| 2 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content|
| 3 | Press Home key to suspend app | Press Home key from remote on the launched Apps | App should not terminate but goes to Hibernated state|
| 4 | Repeat steps for other apps up to max count | Repeat the steps 2 - 4 on other installed Apps upto the same count of maxHibernatedApps | Expected Response should be same as step 2 -4 for maxHibernatedApps|
| 5 | Query getMaxHibernatedFlashUsage via API | Execute the below curl command to gets the max size of flash to use for hibernated apps (in mebibytes) :<br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 22, "method": "org.rdk.AppManager.getMaxHibernatedFlashUsage"}' http://127.0.0.1:9998/jsonrpc` | The `getMaxHibernatedFlashUsage` API should return a successful response containing the `maxHibernatedFlashUsage` value, indicating the maximum flash storage (in mebibytes) available for hibernated apps.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
