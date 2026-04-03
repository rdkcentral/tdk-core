# FNCS_Playback_CheckLatency_MKV Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_317

## TestCase Name
FNCS_Playback_CheckLatency_MKV

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To check if latency observed during MKV playback is within the threshold limit, validating that the media pipeline's MKV container latency performance meets acceptable requirements for real-time video delivery with AV1 codec.

**VIDEO CODEC:** MKV Latency Validation

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | MKV stream must be available and referenced in MediaValidationVariables.video_src_url_4k_av1_mkv (TDK_Asset_Sunrise_AV1_MKV.mkv) |
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
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD config values, get MKV stream URL from MediaValidationVariables.video_src_url_4k_av1_mkv (TDK_Asset_Sunrise_AV1_MKV.mkv), construct tdk_mediapipelinetests command, and run test_playback_latency with stream | Configuration values retrieved, stream URL obtained, command executed: `tdk_mediapipelinetests test_playback_latency <TDK_Asset_Sunrise_AV1_MKV.mkv> checkavstatus=no timeout=<TIMEOUT>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for MKV latency testing, configure westeros-sink for video rendering with latency measurement capabilities, setup matroskademux element for MKV container processing | Playbin element created successfully with MKV latency monitoring support, westeros-sink configured with latency measurement enabled, matroskademux initialized for MKV container parsing |
| 4 | Start MKV Playback | Begin playback with MKV stream and initiate latency measurement timer, monitor for proper AV1 video decoding with MKV container demuxing | MKV playback starts successfully with proper AV1 video codec decoding, MKV container parsed and demuxed correctly, latency measurement initiated |
| 5 | Monitor MKV Container Processing | Track MKV container demuxing performance and measure time from container parsing to frame extraction, validate MKV specific processing efficiency | MKV container processing optimized, demuxing latency measured from container input to frame output, proper MKV handling and buffer management confirmed |
| 6 | Measure Container Latency | Collect MKV-specific latency measurements including container parsing time, frame extraction delay, and AV1 decoding latency, track container performance characteristics | MKV container latency measurements collected successfully, parsing time and frame extraction delays recorded, container-specific performance metrics gathered |
| 7 | Validate MKV Performance | Monitor MKV playback for the configured timeout duration, ensure consistent container latency performance and stable AV1 decoding without frame drops | MKV playback proceeds stably for specified timeout duration, consistent container latency performance maintained, no frame drops or container parsing errors detected |
| 8 | Analyze MKV Metrics | Calculate average, minimum, and maximum MKV latency values observed during playback, compare against configured threshold limits for container performance | MKV latency metrics calculated successfully, statistical analysis completed for container latency distribution, threshold comparison values prepared |
| 9 | Validate Latency Threshold | Compare measured MKV latency values against FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD configuration, verify all measurements are within acceptable limits | MKV latency measurements compared against threshold (default 100ms), all values verified to be within acceptable limits for real-time MKV container processing |
| 10 | Parse MKV Latency Results | Extract MKV-specific latency measurement data from test output using parseLatency function, validate that container latency values meet performance requirements | MKV latency data parsed successfully from test output, parseLatency function validates container measurements against threshold, results indicate acceptable performance |
| 11 | Monitor MKV Resource Usage | Track system resource usage during MKV latency testing to ensure efficient container processing and optimal demuxer performance | System resources monitored efficiently, MKV processing optimized for minimal latency, CPU and memory usage within acceptable ranges for container operations |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" and confirm MKV latency threshold compliance | Test output contains success strings indicating MKV latency test completed without errors and latency measurements within threshold |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release MKV stream resources, and clean up container latency measurement components | Pipeline transitions to NULL state successfully, all MKV container resources released, and latency measurement components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M132