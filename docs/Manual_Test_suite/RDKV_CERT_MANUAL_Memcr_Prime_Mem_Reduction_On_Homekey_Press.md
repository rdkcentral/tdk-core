## TestCase ID
RDKV_MANUAL_MEMCR_09
## TestCase Name
RDKV_CERT_MANUAL_Memcr_Prime_Mem_Reduction_On_Homekey_Press

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the memory consumption of the Amazon Prime Video application process is significantly reduced after pressing the Home key, confirming successful Memcr hibernation. This test exercises the `memcr` memory checkpoint and restore service together with the application lifecycle manager to validate suspend-and-resume behaviour of DAC applications. The test confirms that awk '{print $2$3}'`.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned.|
| 3 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 4 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|
| 5 | Verify MEMCR App on home screen | Verify that the MEMCR App is available in the My Apps section/row of the RDK UI Home screen. If the MEMCR App is already present, skip the remaining installation steps. | The MEMCR App should be visible in the My Apps section of the RDK UI Home screen or be available for installation.|
| 6 | Install MEMCR App | Select the MEMCR App tile on the Recommended Apps row and press Enter/OK on the remote. Verify that a loading indicator appears on the tile. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The MEMCR App should be installed successfully on the DUT.|
| 7 | Verify MEMCR App listed on home screen | Verify that the installed MEMCR App is listed under the My Apps section/row of the RDK UI Home screen, ready to launch. | The MEMCR App should be visible in the My Apps section of the RDK UI Home screen and ready to launch.|
| 8 | Verify MEMCR App package in /opt/CDL/ | Verify that the MEMCR App package is downloaded and available in the /opt/CDL/ directory of the DUT.<br>Command: `ls -lh /opt/CDL/` | The MEMCR App package should be listed in the /opt/CDL/ directory of the DUT.|
| 9 | Sign in to apps and verify A/V playback | After installing and launching the YouTube or Amazon Prime application, sign in with valid user credentials and verify A/V playback is functional prior to the Memcr test execution. | Sign-in should succeed and A/V playback should be functional in the installed application.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch Amazon Prime Video app | Select the Amazon Prime Video App tile from the My Apps / Recommended Apps section and press Enter/OK on the remote. | The Amazon Prime Video App should launch successfully.|
| 2 | Select 4K content and initiate Amazon Prime playback | Select any 4K video content and initiate playback on Amazon Prime Video. | A/V playback on Amazon Prime Video should start successfully.|
| 3 | Identify Amazon process IDs | Execute the following command in the DUT serial console or SSH terminal to identify the Amazon process IDs.<br>Command: `ps -aux \| grep Amazon` | The output should list the running Amazon process entries including both the DobbyInit PID and the WPEProcess (Amazon) application PID.|
| 4 | Navigate to Amazon process /proc directory | From the output of Step 3, identify the WPEProcess (Amazon) application PID (not the DobbyInit PID) and navigate to its /proc directory.<br>Command: `cd /proc/<pid>` | The current directory should change to /proc/<pid>.|
| 5 | Read Amazon process RSS memory before hibernation | Execute the following command to read the current RSS memory usage of the Amazon process.<br>Command: `grep -i 'VmRSS' status \| awk '{print $2$3}'` | The command should output the current RSS memory consumption of the Amazon process (e.g., 216624kB). Record this value.|
| 6 | Press Home key and wait | Press the Home key on the remote and wait a few seconds. | The RDK UI Home screen should be displayed.|
| 7 | Read Amazon process RSS memory after hibernation | Execute the following command again to read the RSS memory usage after hibernation.<br>Command: `grep -i 'VmRSS' status \| awk '{print $2$3}'` | The RSS memory consumption should be significantly lower than the value recorded in Step 5, confirming that Memcr hibernation has reduced memory usage.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
