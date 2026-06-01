# FNCS_Playback_CheckLatency_H264 Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_203

## TestCase Name
FNCS_Playback_CheckLatency_H264

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To check if latency observed during H264 playback is within the threshold limit, validating that the media pipeline's H264 codec latency performance meets acceptable requirements for real-time video delivery.

**VIDEO CODEC:** H264 Latency Validation

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | H264 stream must be available and referenced in MediaValidationVariables.video_src_url_dash_h264 (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd) |
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
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD config values, get H264 stream URL from MediaValidationVariables.video_src_url_dash_h264 (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd), construct tdk_mediapipelinetests command, and run test_playback_latency with stream | Configuration values retrieved, stream URL obtained, command executed: `tdk_mediapipelinetests test_playback_latency <DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd> checkavstatus=no timeout=<TIMEOUT>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for H264 latency testing, configure westeros-sink for video rendering with latency measurement capabilities, setup H264 decoder for codec-specific latency analysis | Playbin element created successfully with H264 latency monitoring support, westeros-sink configured with latency measurement enabled, H264 decoder initialized for codec performance analysis |
| 4 | Start H264 Playback | Begin playback with H264 stream and initiate latency measurement timer, monitor for proper H264 video decoding and AAC audio processing with codec-specific performance tracking | H264 playback starts successfully with proper H264 video codec decoding, AAC audio processing, and codec-specific latency measurement initiated |
| 5 | Monitor H264 Decoding | Track H264 decoder performance and measure time from encoded frame input to decoded frame output, validate H264 specific decoding efficiency and buffer management | H264 decoder processes frames efficiently, decoding latency measured from input to output, proper H264 frame handling and buffer optimization confirmed |
| 6 | Measure Codec Latency | Collect H264-specific latency measurements including decode time, frame processing delay, and rendering latency, track H264 codec performance characteristics | H264 codec latency measurements collected successfully, decode time and frame processing delays recorded, codec-specific performance metrics gathered |
| 7 | Validate H264 Performance | Monitor H264 playback for the configured timeout duration, ensure consistent H264 codec latency performance and stable decoding without frame drops | H264 playback proceeds stably for specified timeout duration, consistent codec latency performance maintained, no frame drops or decoding errors detected |
| 8 | Analyze H264 Metrics | Calculate average, minimum, and maximum H264 latency values observed during playback, compare against configured threshold limits for codec performance | H264 latency metrics calculated successfully, statistical analysis completed for codec latency distribution, threshold comparison values prepared |
| 9 | Validate Latency Threshold | Compare measured H264 latency values against FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD configuration, verify all measurements are within acceptable limits | H264 latency measurements compared against threshold (default 100ms), all values verified to be within acceptable limits for real-time H264 decoding |
| 10 | Parse H264 Latency Results | Extract H264-specific latency measurement data from test output using parseLatency function, validate that H264 codec latency values meet performance requirements | H264 latency data parsed successfully from test output, parseLatency function validates H264 measurements against threshold, results indicate acceptable codec performance |
| 11 | Monitor H264 Resource Usage | Track system resource usage during H264 latency testing to ensure efficient codec processing and optimal H264 decoder performance | System resources monitored efficiently, H264 processing optimized for minimal latency, CPU and memory usage within acceptable ranges for codec operations |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" and confirm H264 latency threshold compliance | Test output contains success strings indicating H264 latency test completed without errors and latency measurements within threshold |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release H264 stream resources, and clean up H264 latency measurement components | Pipeline transitions to NULL state successfully, all H264 streaming resources released, and codec latency measurement components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121