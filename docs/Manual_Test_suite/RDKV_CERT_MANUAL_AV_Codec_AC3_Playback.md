## TestCase ID
RDKV_MANUAL_AV_11
## TestCase Name
RDKV_CERT_MANUAL_AV_Codec_AC3_Playback

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that AC3 audio codec playback is functional on the DUT using the RDK media pipeline. This test confirms that the audio plays back and completes gracefully without errors or crashes, ensuring AC3 codec support meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Ensure console access to DUT | Ensure that SSH or serial console access to the DUT is available. | SSH or serial console access should be available and functional on the DUT.|
| 2 | Set required environment variables | Set the required environment variables from /lib/systemd/system/wpeframework.service in the console session (e.g., `export LD_PRELOAD=/usr/lib/libwesteros_gl.so.0`). | The required environment variables should be set successfully in the console session.|
| 3 | Set WAYLAND_DISPLAY variable | Set the mandatory environment variable for the display.<br>Command: `export WAYLAND_DISPLAY=test` | The WAYLAND_DISPLAY variable should be set successfully.|
| 4 | Stop running video playback | Stop any currently running video playback on the DUT. | All running video playback on the DUT should be stopped.|
| 5 | Kill Ref UI via AppManager API | Kill the Ref UI using the AppManager API.<br>Command: `curl http://127.0.0.1:9998/jsonrpc --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method": "org.rdk.AppManager.killApp", "params":{"appId": "com.rdkcentral.refui"}}'` | The Ref UI should be killed successfully and the DUT should be ready for GStreamer playback.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Execute GStreamer command for AC3 | Execute the GStreamer command to play the AC3 stream.<br>Command: `gst-launch-1.0 playbin uri=<AC3_URL>` | The AC3 audio stream should play without any distortion or errors.|
| 2 | Wait for playback to end | Wait for the audio playback to end gracefully. | The audio playback should end gracefully without any errors or crashes.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
