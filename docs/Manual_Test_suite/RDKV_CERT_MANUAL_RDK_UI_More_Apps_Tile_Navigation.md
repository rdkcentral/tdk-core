## TestCase ID
RDKV_MANUAL_RDKUI_20
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_More_Apps_Tile_Navigation

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that selecting the "More Apps" tile at the end of the Recommended Apps row opens a dedicated page listing all available applications in the DAC App Catalogue. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that the apps listed in more Apps should match with the apps in App catalogue. In 'More Apps' page, apps should be listed in alphabetical order, arranged in a row-column (n x 5) grid layout.

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
| 1 | Click More Apps tile from Home screen | From RDK UI Home screen, click on the 'More Apps' tile at the end of the 'Recommended Apps' row | A dedicated page should open which lists all applications available in DAC App Catalogue|
| 2 | Verify all apps listed in alphabetical order in More Apps | Verify that all apps available in App catalogue are listed in More Apps and its arrangement | The apps listed in more Apps should match with the apps in App catalogue. <br>In 'More Apps' page, apps should be listed in alphabetical order,<br>arranged in a row-column (n x 5) grid layout.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
