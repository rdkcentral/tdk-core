## TestCase ID
RDKV_MANUAL_MEMCR_04
## TestCase Name
RDKV_CERT_MANUAL_Memcr_Youtube_Checkpoint_Restore_Verify

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the YouTube application state is serialized to disk upon hibernation (Home key press) and correctly deserialized and resumed from the same playback position upon relaunch. This test exercises the `memcr` memory checkpoint and restore service together with the application lifecycle manager to validate suspend-and-resume behaviour of DAC applications. The test confirms that the directory should be empty — confirming that the state has been deserialized and the app fully restored.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned. |
| 3 | Reboot DUT prior to test | Reboot the DUT prior to the test. | The DUT should reboot successfully and the RDK UI Home screen should be displayed. |
| 4 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 5 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT. |
| 6 | Verify MEMCR App on home screen | Verify that the MEMCR App is available in the My Apps section/row of the RDK UI Home screen. If the MEMCR App is already present, skip the remaining installation steps. | The MEMCR App should be visible in the My Apps section of the RDK UI Home screen or be available for installation. |
| 7 | Install MEMCR App | Select the MEMCR App tile on the Recommended Apps row and press Enter/OK on the remote. Verify that a loading indicator appears on the tile. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The MEMCR App should be installed successfully on the DUT. |
| 8 | Verify MEMCR App listed on home screen | Verify that the installed MEMCR App is listed under the My Apps section/row of the RDK UI Home screen, ready to launch. | The MEMCR App should be visible in the My Apps section of the RDK UI Home screen and ready to launch. |
| 9 | Verify MEMCR App package in /opt/CDL/ | Verify that the MEMCR App package is downloaded and available in the /opt/CDL/ directory of the DUT.<br>Command: `ls -lh /opt/CDL/` | The MEMCR App package should be listed in the /opt/CDL/ directory of the DUT. |
| 10 | Sign in to apps and verify A/V playback | After installing and launching the YouTube or Amazon Prime application, sign in with valid user credentials and verify A/V playback is functional prior to the Memcr test execution. | Sign-in should succeed and A/V playback should be functional in the installed application. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch YouTube app | Select the YouTube App tile from the My Apps / Recommended Apps section and press Enter/OK on the remote. | The YouTube App should launch successfully. |
| 2 | Select content and initiate YouTube playback | Select any video content and initiate playback on YouTube. | A/V playback on YouTube should start successfully. |
| 3 | Verify Memcr directory is empty before hibernation | Navigate to the Memcr working directory and list its contents.<br>Command: `ls /media/apps/memcr/ or ls /tmp/data/memcr/` | The directory should be empty — no serialized state files should be present at this point. |
| 4 | Note playback position and press Home key | Note the current video playback time position and press the Home key on the remote. | The RDK UI Home screen should be launched. |
| 5 | Verify serialized state file in Memcr directory | Navigate to the Memcr working directory and list its contents.<br>Command: `ls /media/apps/memcr/ or ls /tmp/data/memcr/` | A serialized state file with .img extension should be listed (e.g., screens-1738.img), confirming that the Cobalt process state has been serialized. |
| 6 | Relaunch YouTube and verify resume | Select the YouTube App tile from the My Apps / Recommended Apps section and press Enter/OK on the remote. | YouTube should relaunch and video should resume playback from the exact position at which the Home key was pressed in Step 4. |
| 7 | Verify Memcr directory is empty after restore | Navigate to the Memcr working directory and list its contents.<br>Command: `ls /media/apps/memcr/ or ls /tmp/data/memcr/` | The directory should be empty — confirming that the state has been deserialized and the app fully restored. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
