# FNCS_Playback_Channel_Change_HLS_to_DASH Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_198

## TestCase Name
FNCS_Playback_Channel_Change_HLS_to_DASH

## Table Of Contents
- [FNCS\_Playback\_Channel\_Change\_HLS\_to\_DASH Test Case Documentation](#fncs_playback_channel_change_hls_to_dash-test-case-documentation)
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test channel change functionality from a HLS stream to DASH stream through playbin gst element and westerossink, validating the media pipeline's capability to seamlessly switch between different streaming protocols during channel change operations.

**VIDEO CODEC:** HLS to DASH

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | HLS stream must be available and referenced in MediaValidationVariables.video_src_url_hls (HLS_H264_AAC/master.m3u8) |
| 3 | DASH stream must be available and referenced in MediaValidationVariables.video_src_url_dash (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd) |
| 4 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 5 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 7 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 8 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 10 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 11 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 12 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration in Video_Accelerator.config specifies playback duration in seconds for first channel |
| 13 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT configuration in Video_Accelerator.config specifies playback duration in seconds for second channel after channel change |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT config values, get HLS stream URL from MediaValidationVariables.video_src_url_hls (HLS_H264_AAC/master.m3u8) and DASH stream URL from MediaValidationVariables.video_src_url_dash (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd), construct tdk_mediapipelinetests command, and run test_channel_change_playback with both streams | Configuration values retrieved, stream URLs obtained, command executed: `tdk_mediapipelinetests test_channel_change_playback <HLS_H264_AAC/master.m3u8> <DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd> checkavstatus=no timeout=<TIMEOUT1>,<TIMEOUT2>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for multi-protocol channel change playback, configure westeros-sink for video rendering with protocol switching capabilities | Playbin element created successfully with channel change support, westeros-sink configured with adaptive protocol processing enabled |
| 4 | Start HLS Playback | Begin playback with HLS stream as first channel, monitor for proper HLS protocol handling and H264/AAC decoding | HLS playback starts successfully with proper HLS protocol parsing, H264 video decoding, and AAC audio processing |
| 5 | Monitor First Channel | Continue monitoring HLS stream playback for the configured first channel timeout duration, validate HLS protocol performance and streaming stability | First channel playback proceeds normally for specified timeout duration, HLS segments processed correctly with stable streaming |
| 6 | Initiate Channel Change | Execute channel change operation from HLS stream to DASH stream, monitor pipeline state transition during protocol switching | Channel change operation initiated successfully, pipeline transitions smoothly from HLS to DASH protocol without demuxer errors |
| 7 | Validate Protocol Transition | Verify seamless transition from HLS protocol to DASH protocol, confirm demuxer adaptation and protocol switching without playback interruption | Protocol transition completed successfully, pipeline switches from HLS demuxer to DASH demuxer with proper protocol adaptation |
| 8 | Start DASH Playback | Begin playback with DASH stream as second channel, monitor for proper DASH protocol handling and streaming performance | DASH playback starts successfully after channel change with proper DASH protocol parsing and streaming functionality |
| 9 | Monitor Second Channel | Continue monitoring DASH stream playback for the configured second channel timeout duration, validate DASH protocol performance and streaming stability | Second channel playback proceeds normally for specified timeout duration, DASH segments processed correctly with stable streaming |
| 10 | Validate Channel Change Performance | Verify that channel change operation completed within acceptable time limits and maintained audio/video synchronization throughout protocol transition | Channel change performance meets expected timing requirements, audio/video synchronization maintained during protocol transition |
| 11 | Monitor Protocol Resources | Track system resource utilization during channel change operation to ensure efficient protocol switching and demuxer management | System resources managed efficiently during protocol change, demuxer resources optimized for HLS to DASH transition |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating channel change test completed without errors |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release both HLS and DASH stream resources, and clean up protocol switching components | Pipeline transitions to NULL state successfully, all protocol resources released, and channel change components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121