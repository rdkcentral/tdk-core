# FNCS_Playback_Bitrate_Switch_Up_HEVC Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_272

## TestCase Name
FNCS_Playback_Bitrate_Switch_Up_HEVC

## Table Of Contents
- [FNCS\_Playback\_Bitrate\_Switch\_Up\_HEVC Test Case Documentation](#fncs_playback_bitrate_switch_up_hevc-test-case-documentation)
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To restrict network bandwidth to certain levels and verify adaptive bitrate streaming by switching from the lowest possible resolution to the highest resolution in the manifest for HEVC video streams, validating the media pipeline's capability to handle dynamic bitrate adaptation and resolution switching based on improving network conditions with high-efficiency video compression.

**VIDEO CODEC:** HEVC

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | HEVC adaptive bitrate stream must be available and referenced in MediaValidationVariables.video_src_url_bitrate_hevc (currently empty - requires configuration) |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration in Video_Accelerator.config specifies playback duration in seconds for each bitrate level |
| 12 | video_src_url_bitrate_hevc variable in MediaValidationVariables.py contains HEVC adaptive bitrate stream URL (currently empty - requires configuration) for bitrate switching testing |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT config values, get HEVC bitrate stream URL from MediaValidationVariables.video_src_url_bitrate_hevc, construct tdk_mediapipelinetests command, and run test_bitrate_switching with HEVC stream | Configuration values retrieved, HEVC bitrate stream URL obtained, command executed: `tdk_mediapipelinetests test_bitrate_switching <HEVC_BITRATE_STREAM_URL> checkavstatus=no timeout=<TIMEOUT>`, and test application starts execution without errors |
| 3 | Parse Manifest File | Parse the HEVC stream manifest file to extract available resolutions and corresponding bandwidth levels, identify lowest and highest quality variants for HEVC content | Manifest file parsed successfully, all available HEVC resolutions and bandwidth levels identified, lowest and highest quality variants determined |
| 4 | Create GStreamer Pipeline | Initialize playbin element with dash-demux for adaptive streaming, configure HEVC video stream support with bitrate switching capabilities and hardware decoding | Playbin element created successfully with dash-demux, HEVC adaptive streaming support configured, and bitrate switching with hardware decoding enabled |
| 5 | Configure Adaptive Streaming | Set up dash-demux instance for dynamic bitrate adaptation, enable bandwidth monitoring and resolution switching based on network conditions for HEVC content | Dash-demux configured successfully for HEVC adaptive streaming with bandwidth monitoring and resolution switching capabilities |
| 6 | Start Lowest Bitrate Playback | Set initial bitrate to lowest resolution available in manifest, begin HEVC video playback at minimum quality level with efficient compression | Pipeline starts successfully with lowest bitrate/resolution, HEVC video playback begins at minimum quality with efficient compression |
| 7 | Monitor Low Quality Playback | Play HEVC video at lowest bitrate for configured timeout duration, verify stable playback and quality maintenance with efficient decoding | Low quality HEVC playback proceeds successfully for full timeout duration with stable video quality and efficient decoding |
| 8 | Switch to Higher Bitrate | Dynamically switch to next highest bandwidth level available in manifest, verify resolution change occurs as expected for HEVC content | Bitrate switching executed successfully, HEVC resolution changed to next higher level as defined in manifest |
| 9 | Validate Resolution Upgrade | Verify that HEVC video resolution matches expected quality level for selected bandwidth, confirm smooth transition without artifacts | HEVC video resolution matches expected level for selected bandwidth, smooth transition completed without visual artifacts |
| 10 | Continue Bitrate Escalation | Repeat bitrate switching process through all available quality levels up to highest resolution in manifest for HEVC stream | All HEVC bitrate levels tested successfully, progressive quality improvement from lowest to highest resolution completed |
| 11 | Monitor Highest Quality Playback | Play HEVC video at highest bitrate for configured timeout duration, verify stable playback at maximum quality level with maintained efficiency | Highest quality HEVC playback proceeds successfully for full timeout duration with stable video at maximum resolution and maintained efficiency |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating HEVC bitrate switching completed without errors |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release HEVC adaptive streaming resources, and clean up bitrate switching components | Pipeline transitions to NULL state successfully, HEVC adaptive streaming resources released, and bitrate switching components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M129