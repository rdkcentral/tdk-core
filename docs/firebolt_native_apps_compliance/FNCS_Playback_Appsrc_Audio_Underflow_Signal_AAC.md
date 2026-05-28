# FNCS_Playback_Appsrc_Audio_Underflow_Signal_AAC Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_253

## TestCase Name
FNCS_Playback_Appsrc_Audio_Underflow_Signal_AAC

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To verify if underflow signal is captured by audio sink after reaching the amount of buffers pushed by "appsrc" element to pipeline created via "playbin" and audio sink GStreamer elements. This test validates the media pipeline's capability to detect audio buffer underflow conditions by monitoring underflow signals without attempting playback recovery, focusing specifically on signal detection and validation using appsrc for controlled audio buffer feeding with deliberate buffer starvation to trigger underflow events.

**AUDIO CODEC:** AAC

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4 must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_AUDIO_SINK configuration in Video_Accelerator.config specifies custom audio sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | audio_src_url_mp4_aac variable in MediaValidationVariables.py contains AAC audio stream URL (atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4) for appsrc underflow signal testing |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS config value, get AAC stream URL from MediaValidationVariables.audio_src_url_mp4_aac, construct tdk_mediapipelinetests command with underflow threshold parameter (548409 bytes), and run test_appsrc_audio_underflow_signal with AAC stream | Configuration values retrieved, AAC stream URL obtained, command executed: `tdk_mediapipelinetests test_appsrc_audio_underflow_signal https://<server_hosting_stream>:<port_number>/DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4 checkavstatus=no validateFullPlayback underflow_threshold=548409`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline with Appsrc | Initialize playbin element and configure with force_appsrc flag for audio-only playback, set audio_underflow_test and checkSignalTest flags to enable underflow signal detection | Playbin element created successfully with appsrc integration and audio underflow signal testing capability enabled |
| 4 | Configure Audio Output | Create native audio sink element and link it to playbin with audio underflow signal connection | Audio sink element created and linked successfully to playbin with underflow callback configured |
| 5 | Setup Appsrc Element | Configure appsrc with size property set to underflow threshold (548409 bytes), set appropriate AAC audio caps, and connect push-buffer signal for manual feeding | Appsrc element configured successfully with threshold size and AAC audio capabilities |
| 6 | Start Pipeline and Feed Buffers | Set pipeline to PLAYING state and begin feeding audio data through appsrc up to threshold limit | Pipeline transitions to PLAYING state successfully and starts consuming audio buffers from appsrc |
| 7 | Reach Buffer Threshold | Continue feeding audio buffers via appsrc until threshold bytes (548409) are reached | Threshold limit reached successfully, pipeline consuming all provided audio buffer data |
| 8 | Trigger Buffer Underflow | Emit end-of-stream signal from appsrc to stop buffer feeding and trigger audio underflow condition | End-of-stream signal emitted successfully, causing pipeline to enter audio underflow state |
| 9 | Detect Underflow Signal | Monitor native audio sink buffer-underflow-callback signal to capture audio underflow event detection | Audio buffer underflow signal received successfully indicating proper underflow detection mechanism |
| 10 | Complete Signal Test | Exit test immediately after underflow signal detection without attempting playback recovery since checkSignalTest flag is enabled | Test completes successfully after confirming underflow signal detection |
| 11 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating AAC appsrc audio underflow signal detection completed without errors |
| 12 | Cleanup Pipeline | Set playbin pipeline to NULL state and release resources | Pipeline transitions to NULL state successfully and resources cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M123