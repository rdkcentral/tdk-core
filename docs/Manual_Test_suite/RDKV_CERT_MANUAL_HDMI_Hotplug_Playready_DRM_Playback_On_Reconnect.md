## TestCase ID
RDKV_MANUAL_HDMIHOTPLUG_12
## TestCase Name
RDKV_CERT_MANUAL_HDMI_Hotplug_Playready_DRM_Playback_On_Reconnect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that PlayReady DRM encrypted stream playback continues without interruption after an HDMI cable reconnect on the DUT. This test confirms that DRM-protected playback resumes correctly after HDMI reconnection and the session concludes cleanly, ensuring hotplug resilience for DRM-protected content meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned.|
| 2 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 3 | Connect HDMI cable and select source | Connect the HDMI cable between the DUT and the TV/display, with the correct input source selected. | The HDMI cable should be connected and the correct input source should be selected on the TV/display.|
| 4 | Enable OCDM plugin on DUT | Ensure the OCDM plugin is enabled on the DUT. | The OCDM plugin should be enabled and active on the DUT.|
| 5 | Set required environment variables | Identify and export the required environment variables from /lib/systemd/system/wpeframework.service (e.g., `export LD_PRELOAD=/usr/lib/libwesteros_gl.so.0`) in the serial console or SSH console prior to running aamp-cli commands. | The required environment variables should be set successfully in the console session.|
| 6 | Stop running video playback | Ensure any currently running video playback is stopped prior to the test. | All video playback on the DUT should be stopped.|
| 7 | Configure /opt/aamp.cfg for PlayReady | Configure /opt/aamp.cfg with the following keys (replace <Playready License server URL> with the actual URL):<br>`licenseServerUrl=<Playready License server URL>`<br>`FORCE_SVP=TRUE`<br>`preferredDrm=2`<br>`useWesterosSink=1` | The /opt/aamp.cfg file should be configured correctly with the PlayReady DRM settings.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Execute aamp-cli for PlayReady playback | On the DUT terminal, execute the aamp-cli command to initiate PlayReady DRM stream playback.<br>Command: `aamp-cli <Playready URL>` | Playback should start with proper audio and video output using the PlayReady DRM encrypted stream.|
| 2 | Disconnect and reconnect HDMI cable | Disconnect the HDMI cable from the DUT. Wait approximately 10 seconds, then reconnect the HDMI cable to the DUT. | Playback should continue with proper audio and video output after HDMI reconnection without requiring a restart.|
| 3 | Exit aamp-cli playback session | Press Enter in the DUT terminal and type exit to terminate the playback session.<br>Command: `exit` | Playback should terminate and the aamp-cli session should exit cleanly.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
