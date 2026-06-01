# FNCS_Playback_Appsrc_Audio_Underflow_Playback_MP3 Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_259

## TestCase Name
FNCS_Playback_Appsrc_Audio_Underflow_Playback_MP3

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To verify playback recovery after pushing additional audio buffers from "appsrc" once underflow state is reached through 'playbin' and audio sink GStreamer elements. This test validates the media pipeline's capability to handle audio buffer underflow situations by detecting underflow signals, managing pipeline state transitions, and successfully resuming playback with additional buffer data using appsrc for controlled audio buffer feeding with comprehensive playback validation mechanisms including position monitoring and audio frame rendering validation.

**AUDIO CODEC:** MP3

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | TDK_Asset_Sunrise_MP3.mp3 must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_AUDIO_SINK configuration in Video_Accelerator.config specifies custom audio sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | audio_src_url_mp3 variable in MediaValidationVariables.py contains MP3 audio stream URL (TDK_Asset_Sunrise_MP3.mp3) for appsrc underflow testing |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS config value, get MP3 stream URL from MediaValidationVariables.audio_src_url_mp3, construct tdk_mediapipelinetests command with underflow threshold parameter (811071 bytes), and run test_appsrc_audio_underflow with MP3 stream | Configuration values retrieved, MP3 stream URL obtained, command executed: `tdk_mediapipelinetests test_appsrc_audio_underflow https://<server_hosting_stream>:<port_number>/TDK_Asset_Sunrise_MP3.mp3 checkavstatus=no validateFullPlayback underflow_threshold=811071`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline with Appsrc | Initialize playbin element and configure with force_appsrc flag for audio-only playback, set audio_underflow_test flag to enable underflow detection | Playbin element created successfully with appsrc integration and audio underflow testing capability enabled |
| 4 | Configure Audio Output | Create native audio sink element and link it to playbin with audio underflow signal connection | Audio sink element created and linked successfully to playbin with underflow callback configured |
| 5 | Setup Appsrc Element | Configure appsrc with size property set to underflow threshold (811071 bytes), set appropriate MP3 audio caps, and connect push-buffer signal for manual feeding | Appsrc element configured successfully with threshold size and MP3 audio capabilities |
| 6 | Start Pipeline and Feed Buffers | Set pipeline to PLAYING state and begin feeding audio data through appsrc up to threshold limit | Pipeline transitions to PLAYING state successfully and starts consuming audio buffers from appsrc |
| 7 | Reach Buffer Threshold | Continue feeding audio buffers via appsrc until threshold bytes (811071) are reached | Threshold limit reached successfully, pipeline consuming all provided audio buffer data |
| 8 | Trigger Buffer Underflow | Emit end-of-stream signal from appsrc to stop buffer feeding and trigger audio underflow condition | End-of-stream signal emitted successfully, causing pipeline to enter audio underflow state |
| 9 | Detect Underflow Signal | Monitor native audio sink buffer-underflow-callback signal to capture audio underflow event detection | Audio buffer underflow signal received successfully indicating proper underflow detection mechanism |
| 10 | Pause Pipeline | Set pipeline to PAUSED state after underflow signal detection to prepare for buffer refilling | Pipeline transitions to PAUSED state successfully, stopping audio playback temporarily |
| 11 | Update Buffer Threshold | Double the buffer threshold value to 1622142 bytes and prepare for additional audio buffer feeding | Buffer threshold updated successfully, ready for extended audio buffer feeding |
| 12 | Push Additional Buffers | Feed additional audio buffers through appsrc with updated threshold to resume playback | Additional audio buffers pushed successfully via appsrc element with increased threshold |
| 13 | Resume Pipeline Playback | Set pipeline back to PLAYING state to resume audio playback from current position | Pipeline transitions to PLAYING state successfully and resumes audio playback |
| 14 | Monitor Position Progression | Execute position monitoring validation checking playback position advancement each second | Audio playback progresses smoothly with position advancing at normal rate after underflow recovery |
| 15 | Validate Audio Frame Rendering | Use native audio sink stats property to monitor rendered and dropped audio frame counts each second | Audio frame drop rate remains below 1% threshold during playback indicating proper audio rendering recovery |
| 16 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating MP3 appsrc audio underflow recovery completed without errors |
| 17 | Cleanup Pipeline | Set playbin pipeline to NULL state and release resources | Pipeline transitions to NULL state successfully and resources cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 7 minutes  

**Priority:** High

**Release Version:** M123