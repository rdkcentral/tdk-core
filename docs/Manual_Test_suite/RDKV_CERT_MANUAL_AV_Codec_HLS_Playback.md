## TestCase ID
RDKV_MANUAL_AV_05
## TestCase Name
RDKV_CERT_MANUAL_AV_Codec_HLS_Playback

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that HLS (.m3u8) adaptive streaming playback is functional on the DUT using the RDK media pipeline. This test confirms that the HLS asset plays with proper audio and video output without artifacts or errors, ensuring HLS streaming support meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Ensure TDK Test Manager accessibility | Ensure the TDK Test Manager tool is accessible on the PC/Laptop. | The TDK Test Manager tool should be accessible and ready to use on the PC/Laptop. |
| 2 | Log in to TDK Test Manager | Log in to the TDK Test Manager with valid credentials. | Login should be successful and the TDK Test Manager dashboard should be visible. |
| 3 | Add DUT to TDK Test Manager | Add the DUT details to the TDK Test Manager Tool. | The DUT should be added successfully and visible in the TDK Test Manager. |
| 4 | Verify DUT SSH connectivity | Ensure the DUT is SSH-accessible and shows as active in the TDK Test Manager. | The DUT should be sshable and displayed as active in the TDK Test Manager. |
| 5 | Connect HDMI display to DUT | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 6 | Verify WPEFramework process | Verify that the WPEFramework process is running on the device. | The WPEFramework process should be active and running on the device. |
| 7 | Configure BOLT package host path | Configure `MediaValidationVariables.bolt_packages_base_path` with the BOLT packages hosting server URL (e.g., `http://<TM_IP>:<port>/images/signed-packages/`). | The BOLT package host path should be configured and accessible. |
| 8 | Verify BOLT app download URL | Verify that `MediaValidationVariables.unified_player_app_download_url` resolves correctly to the BOLT app package URL. | The BOLT app package URL should be valid and accessible for download. |
| 9 | Configure HLS live stream URL | Configure the stream variable `video_src_url_live_hls` in `MediaValidationVariables.py` with a valid, accessible HLS live stream URL (this variable is environment-specific and must be set before running the test). | The `video_src_url_live_hls` variable should be configured with a valid, accessible HLS live stream URL in `MediaValidationVariables.py`. |
| 10 | Check app installation status | Query the installed package list to check whether the player app is already installed on the device. | The installed app package list should be retrievable and the app installation status should be confirmed. |
| 11 | Download app package if not installed | If the app is not already installed, download the app package from the configured download URL using the DownloadManager API. | The app package should be downloaded successfully if it was not already installed. |
| 12 | Install app via PackageManager | Install the downloaded app package using the PackageManagerRDKEMS.install API with the appropriate `packageId` and file locator. | The app package should be installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Select DUT from TDK left pane | Select the DUT from the left pane of TDK Test Manager. | Popup should launch where scripts can be selected for execution. |
| 2 | Execute HLS test script | Select the script `RDKV_CERT_MVS_Video_Play_Live_HLS` and click on 'Execute Now' button. | The script should start execution. |
| 3 | Verify video playback on TV | Verify if the video started playing on the TV and monitor it. | The HLS (.m3u8) asset should play with proper audio and video without any artifacts or errors. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
