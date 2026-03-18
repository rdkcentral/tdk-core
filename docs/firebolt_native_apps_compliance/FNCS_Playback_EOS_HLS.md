# FNCS_Playback_EOS_HLS Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_150

## TestCase Name
FNCS_Playback_EOS_HLS

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test the End Of Stream (EOS) detection scenario for an HLS stream through 'playbin' and 'westerossink' GStreamer elements, validating the media pipeline's capability to properly detect stream completion and handle EOS events for HLS adaptive streaming content.

**STREAM FORMAT:** HLS

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | HLS stream must be available and referenced in MediaValidationVariables.video_src_url_short_duration_hls (HLS_H264_AAC_15Sec/master.m3u8) |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | FIREBOLT_COMPLIANCE_EOS_TIMEOUT configuration in Video_Accelerator.config specifies EOS detection timeout in seconds (default 6 minutes for test application) |
| 12 | video_src_url_short_duration_hls variable in MediaValidationVariables.py contains short-duration HLS stream URL (HLS_H264_AAC_15Sec/master.m3u8) for EOS testing |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_EOS_TIMEOUT config values, get HLS stream URL from MediaValidationVariables.video_src_url_short_duration_hls, construct tdk_mediapipelinetests command, and run test_EOS with HLS stream | Configuration values retrieved, HLS stream URL obtained, command executed: `tdk_mediapipelinetests test_EOS <HLS_STREAM_URL> checkavstatus=no timeout=<EOS_TIMEOUT>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element and configure for HLS adaptive streaming playback, enable HLS manifest parsing and segment handling with westerossink | Playbin element created successfully with HLS adaptive streaming support and manifest parsing enabled |
| 4 | Configure HLS Adaptive Output | Create and configure video and audio sink elements for HLS playback, establish adaptive bitrate streaming and segment buffering | Video and audio sink elements configured successfully for HLS adaptive streaming with proper buffering |
| 5 | Enable EOS Detection | Configure pipeline to monitor for End-of-Stream events from HLS stream parser, set up EOS message handling and timeout mechanism for adaptive content | EOS detection enabled successfully with proper message handling and timeout configuration for HLS content |
| 6 | Start HLS Adaptive Playback | Set pipeline to PLAYING state and begin playback with HLS adaptive streaming, monitor for video/audio frames and EOS events | Pipeline transitions to PLAYING state successfully, HLS adaptive playback starts, and EOS monitoring activated |
| 7 | Monitor Stream Completion | Continuously monitor HLS adaptive playback until natural stream completion or EOS timeout, verify segment processing and stream position | HLS adaptive playback proceeds successfully with continuous segment processing and proper stream position tracking |
| 8 | Detect EOS Event | Wait for End-of-Stream message from HLS stream parser when all segments are processed and stream reaches natural completion, verify EOS signal reception within configured timeout | EOS message received successfully from HLS parser when all segments complete naturally within timeout period |
| 9 | Validate EOS Handling | Verify proper EOS event processing and pipeline state transition after HLS stream completion, ensure clean shutdown of adaptive streaming components | EOS event processed correctly with proper pipeline state transitions and clean adaptive streaming component shutdown |
| 10 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating HLS EOS detection completed without errors |
| 11 | Cleanup Pipeline | Set playbin pipeline to NULL state, release HLS streaming resources, and clean up adaptive playback components | Pipeline transitions to NULL state successfully, HLS resources released, and adaptive streaming components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121