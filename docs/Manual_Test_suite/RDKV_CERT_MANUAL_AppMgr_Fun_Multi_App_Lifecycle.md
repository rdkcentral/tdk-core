## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_08
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Multi_App_Lifecycle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the lifecycle management behavior of multiple applications launched and suspended via the RDK UI on the DUT. This test confirms that all applications resume from their last closed state upon relaunch with playback intact, ensuring correct multi-app lifecycle handling for certification.

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
| 1 | Verify YouTube app is installed | Validate that YouTube App is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If YouTube is not installed follow the instructions of Precondition 4 | YouTube App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage.|
| 2 | Verify Amazon Prime app is installed | Validate that Amazon Prime App is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If Amazon Prime is not installed follow the instructions of Precondition 4 | Amazon Prime App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage.|
| 3 | Verify other apps are installed | Validate that other Apps is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If Other Apps are not installed follow the instructions of Precondition 4 | Other App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage.|
| 4 | Launch any installed app from home screen | Select any installed Apps from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Installed Apps should be launched successfully (cold launch)|
| 5 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content|
| 6 | Press Home key to suspend app | Press Home key from remote on the launched Apps | App should not terminate but goes to a suspended or hibernated state|
| 7 | Repeat launch/suspend steps for multiple apps | Repeat the steps 4 - 6 on multiple Apps | Expected Response should be same as step 4 -6|
| 8 | Relaunch all installed apps and verify state | Launch all the installed Apps again one by one and verify the App state | All the apps should resume from the last closed state when its relaunched and playback should be fine|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
