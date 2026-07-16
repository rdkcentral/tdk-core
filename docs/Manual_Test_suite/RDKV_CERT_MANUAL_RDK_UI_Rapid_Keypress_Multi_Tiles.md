## TestCase ID
RDKV_MANUAL_RDKUI_30
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Rapid_Keypress_Multi_Tiles

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that multiple rapid key presses on different app tiles in the More Apps page queue the downloads sequentially without errors. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that the other apps downloads should be queued only. Once the previous downloads, completed, subsequent downloads should start.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to More Apps page | Click on More Apps button | More Apps page should load where all apps available in App catalogue are visible|
| 2 | Select app to start download | Press on an App which is not installed yet | A buffering/loading indicator should be displayed on the app tile.|
| 3 | Rapidly press multiple uninstalled app tiles | Rapidly press on other app tiles which are not installed yet | The other apps downloads should be queued only. Once the previous downloads, completed, subsequent downloads should start|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
