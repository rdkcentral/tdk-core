# FNCS_Playback_CheckLatency_DASH Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_202

## TestCase Name
FNCS_Playback_CheckLatency_DASH

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To check if latency observed during DASH playback is within the threshold limit, validating that the media pipeline's DASH streaming latency performance meets acceptable requirements for real-time video delivery.

**VIDEO CODEC:** DASH Latency Validation

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | DASH stream must be available and referenced in MediaValidationVariables.video_src_url_dash (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd) |
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
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD config values, get DASH stream URL from MediaValidationVariables.video_src_url_dash (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd), construct tdk_mediapipelinetests command, and run test_playback_latency with stream | Configuration values retrieved, stream URL obtained, command executed: `tdk_mediapipelinetests test_playback_latency <DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd> checkavstatus=no timeout=<TIMEOUT>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for DASH latency testing, configure westeros-sink for video rendering with latency measurement capabilities, setup dash-demux element for DASH streaming | Playbin element created successfully with latency monitoring support, westeros-sink configured with latency measurement enabled, dash-demux initialized for DASH protocol processing |
| 4 | Start DASH Playback | Begin playback with DASH stream and initiate latency measurement timer, monitor for proper H264 video decoding and AAC audio processing with DASH manifest parsing | DASH playback starts successfully with proper H264 video codec decoding, AAC audio processing, and DASH manifest loaded with segment downloading initiated |
| 5 | Monitor Playback Initialization | Track pipeline state changes and measure time from playback start to first video frame rendering, validate DASH segment fetching and buffer management | Pipeline transitions through states correctly, first video frame rendered within expected timeframe, DASH segments downloaded and buffered appropriately |
| 6 | Measure Latency Performance | Collect latency measurements during DASH playback including segment fetch time, decoding latency, and rendering delay, track overall end-to-end latency | Latency measurements collected successfully, segment fetch times recorded, decoding and rendering delays monitored throughout playback duration |
| 7 | Validate Streaming Stability | Monitor DASH playback for the configured timeout duration, ensure consistent latency performance and stable streaming without buffering events | DASH streaming proceeds stably for specified timeout duration, consistent latency performance maintained, no buffering interruptions detected |
| 8 | Analyze Latency Metrics | Calculate average, minimum, and maximum latency values observed during playback, compare against configured threshold limits | Latency metrics calculated successfully, statistical analysis completed for latency distribution, threshold comparison values prepared |
| 9 | Validate Latency Threshold | Compare measured latency values against FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD configuration, verify all measurements are within acceptable limits | Latency measurements compared against threshold (default 100ms), all values verified to be within acceptable limits for real-time streaming |
| 10 | Parse Latency Results | Extract latency measurement data from test output using parseLatency function, validate that latency values meet performance requirements | Latency data parsed successfully from test output, parseLatency function validates measurements against threshold, results indicate acceptable performance |
| 11 | Monitor Resource Utilization | Track system resource usage during latency testing to ensure efficient DASH processing and optimal performance | System resources monitored efficiently, DASH processing optimized for minimal latency, CPU and memory usage within acceptable ranges |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" and confirm latency threshold compliance | Test output contains success strings indicating latency test completed without errors and latency measurements within threshold |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release DASH stream resources, and clean up latency measurement components | Pipeline transitions to NULL state successfully, all DASH streaming resources released, and latency measurement components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121