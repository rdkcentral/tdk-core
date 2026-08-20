## TestCase ID
RDKV_MANUAL_GT_IMAGEFORMATS_04
## TestCase Name
RDKV_CERT_MANUAL_GT_Image_Format_Webp_Support

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Preconditions](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the WebP (`.webp`) image format is correctly decoded and rendered by the WebKit browser engine on the DUT. This test confirms the DUT's browser correctly handles WebP image content, ensuring WebP format support meets RDK certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`Image_formats.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `Image_formats.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Verify DUT network connectivity | Ensure the DUT is connected to an active network (WiFi or Ethernet) prior to test execution. | The DUT must have active network connectivity so that the Browser Test application and hosted image resources can be accessed from the configured test server during test execution. |
| 3 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen prior to test execution. |
| 4 | Install Browser Test app | Install the Browser Test application on the DUT using the configured app bundle (`<browser_test_app_bundle>`) downloaded from the configured server (`<app_download_server>`). | The Browser Test application should be installed successfully on the DUT. |
| 5 | Kill active Browser Test instance | Terminate any active running instance of the Browser Test application on the DUT. | No active Browser Test app instance should be running before test execution begins. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch Browser Test app | Launch the Browser Test HTML application on the DUT. | The Browser Test HTML application should launch successfully and the app UI should be displayed on the TV. |
| 2 | Activate WEBP image format link | Set focus on the Browser Test application via `org.rdk.RDKWindowManager.setFocus`, then send the following key sequence via `org.rdk.RDKWindowManager.generateKey` to navigate and activate the WebP image format link:<br>— Press the **Tab** key **4 times** to navigate to the `.webp` image format link<br>— Press the **Enter** key **once** to activate the link and load the WebP image on screen | The `.webp` image format link should be activated by the script and the image should load within the Browser Test HTML application on the TV display. |
| 3 | Respond to script confirmation prompt | The script prompts: *"Is webp image format loaded in Browser_test App and Visible on TV [yes/no]:"* — look at the TV display and respond with `yes` if the `.webp` image is visible, or `no` if it is not. | The tester should confirm `yes`, indicating the `.webp` image format is correctly loaded and visible on the TV display connected to the DUT. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
