# FNCS_Playback_CheckLatency_HLS Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_204

## TestCase Name
FNCS_Playback_CheckLatency_HLS

## Table Of Contents
- [FNCS\_Playback\_CheckLatency\_HLS Test Case Documentation](#fncs_playback_checklatency_hls-test-case-documentation)
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To check if latency observed during HLS playback is within the threshold limit, validating that the media pipeline's HLS streaming latency performance meets acceptable requirements for real-time video delivery.

**VIDEO CODEC:** HLS Latency Validation

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | HLS stream must be available and referenced in MediaValidationVariables.video_src_url_hls (HLS_H264_AAC/master.m3u8) |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD configuration in Video_Accelerator.config specifies latency threshold in milliseconds, default set to 100ms |
| 5 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 7 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 8 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 10 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 11 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 12 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration in Video_Accelerator.config specifies playback duration in seconds before latency measurement |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD config values, get HLS stream URL from MediaValidationVariables.video_src_url_hls (HLS_H264_AAC/master.m3u8), construct tdk_mediapipelinetests command, and run test_playback_latency with stream | Configuration values retrieved, stream URL obtained, command executed: `tdk_mediapipelinetests test_playback_latency <HLS_H264_AAC/master.m3u8> checkavstatus=no timeout=<TIMEOUT>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for HLS latency testing, configure westeros-sink for video rendering with latency measurement capabilities, setup hlsdemux element for HLS streaming | Playbin element created successfully with HLS latency monitoring support, westeros-sink configured with latency measurement enabled, hlsdemux initialized for HLS protocol processing |
| 4 | Start HLS Playback | Begin playback with HLS stream and initiate latency measurement timer, monitor for proper H264 video decoding and AAC audio processing with HLS manifest parsing | HLS playback starts successfully with proper H264 video codec decoding, AAC audio processing, and HLS manifest loaded with segment downloading initiated |
| 5 | Monitor Playback Initialization | Track pipeline state changes and measure time from playback start to first video frame rendering, validate HLS segment fetching and buffer management | Pipeline transitions through states correctly, first video frame rendered within expected timeframe, HLS segments downloaded and buffered appropriately |
| 6 | Measure HLS Latency Performance | Collect latency measurements during HLS playback including segment fetch time, decoding latency, and rendering delay, track overall end-to-end HLS streaming latency | Latency measurements collected successfully, HLS segment fetch times recorded, decoding and rendering delays monitored throughout playback duration |
| 7 | Validate HLS Streaming Stability | Monitor HLS playback for the configured timeout duration, ensure consistent latency performance and stable streaming without buffering events | HLS streaming proceeds stably for specified timeout duration, consistent latency performance maintained, no buffering interruptions detected |
| 8 | Analyze HLS Latency Metrics | Calculate average, minimum, and maximum latency values observed during HLS playback, compare against configured threshold limits | HLS latency metrics calculated successfully, statistical analysis completed for latency distribution, threshold comparison values prepared |
| 9 | Validate Latency Threshold | Compare measured HLS latency values against FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD configuration, verify all measurements are within acceptable limits | HLS latency measurements compared against threshold (default 100ms), all values verified to be within acceptable limits for real-time HLS streaming |
| 10 | Parse HLS Latency Results | Extract HLS-specific latency measurement data from test output using parseLatency function, validate that latency values meet performance requirements | HLS latency data parsed successfully from test output, parseLatency function validates measurements against threshold, results indicate acceptable streaming performance |
| 11 | Monitor HLS Resource Utilization | Track system resource utilization during HLS latency testing to ensure efficient streaming processing and optimal performance | System resources monitored efficiently, HLS processing optimized for minimal latency, CPU and memory usage within acceptable ranges |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" and confirm HLS latency threshold compliance | Test output contains success strings indicating HLS latency test completed without errors and latency measurements within threshold |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release HLS stream resources, and clean up HLS latency measurement components | Pipeline transitions to NULL state successfully, all HLS streaming resources released, and latency measurement components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121