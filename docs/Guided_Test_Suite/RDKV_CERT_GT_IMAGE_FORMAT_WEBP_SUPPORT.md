## TestCase ID
RDKV_MANUAL_IMAGEFORMATS_04
## TestCase Name
RDKV_CERT_GT_IMAGE_FORMAT_WEBP_SUPPORT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the WEBP image format is correctly loaded and rendered by the Browser Test application on the DUT.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Install Browser Test app | Install the Browser Test application on the DUT using the configured app bundle (`<browser_test_app_bundle>`) downloaded from the configured server (`<app_download_server>`). | The Browser Test application should be installed successfully on the DUT. |
| 2 | Kill active Browser Test instance | Terminate any active running instance of the Browser Test application on the DUT. | No active Browser Test app instance should be running before test execution begins. |
| 3 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen prior to test execution. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch Browser Test app | Launch the Browser Test HTML application on the DUT. | The Browser Test HTML application should launch successfully and the app UI should be displayed on the TV. |
| 2 | Activate WEBP image format link | The script automatically activates the `.webp` image format link within the Browser Test HTML application on the DUT. The corresponding image is loaded on screen without any manual selection. | The `.webp` image format link should be activated by the script and the image should load within the Browser Test HTML application on the TV display. |
| 3 | Respond to script confirmation prompt | The script prompts: *"Is webp image format loaded in Browser_test App and Visible on TV [yes/no]:"* — look at the TV display and respond with `yes` if the `.webp` image is visible, or `no` if it is not. | The tester should confirm `yes`, indicating the `.webp` image format is correctly loaded and visible on the TV display connected to the DUT. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
