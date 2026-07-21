## TestCase ID
RDKV_MANUAL_RDKUI_22
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_App_Install_From_Recommended

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that selecting an uninstalled app tile from the Recommended Apps row correctly initiates the download and installation, and that the newly installed app appears in the My Apps row on the home screen. This test confirms that the My Apps row is created and the installed app is listed correctly, ensuring app installation from the Recommended Apps row meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Ensure stable network connection | Ensure a stable network connection is available on the DUT. | The DUT should have a stable network connection.|
| 3 | Ensure no apps installed on DUT | Ensure no apps are installed on the DUT prior to this test (fresh flash or factory reset state). | The DUT should have no installed apps.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Select and install app from Recommended Apps | In Recommended Apps row, select an app which is not currently installed | A buffering/loading indicator should be displayed on the app tile|
| 2 | Wait and verify installation completes with tick | Wait for sometime and check for the behavior on App tile | After sometime, buffering/loading icon will disappear and a green tick mark should appear on the tile for 2 to 3 seconds, indicating that the app is successfully installed|
| 3 | Verify My Apps row appears after installation | Check the change happened in RDK UI Home screen after successful installation of the App | A new row with Title 'My Apps' should be created as first row in RDK UI Home screen. The newly installed APP should be listed here|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
