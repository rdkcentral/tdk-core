**TestCase ID**
NATIVE_PLAYBACK_151

**TestCase Name**
NPVS_FrameDrop_Test_H264

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates frame rendering performance and frame drop metrics during H264 video playback on `westerossink`. The test polls `westerossink→stats.rendered_frames` and `dropped_frames` properties continuously via `g_object_get()` to monitor frame rendering statistics. Verify `rendered_frames` counter increments at expected rate matching stream fps (30fps for this stream) and playback position advances at 1x rate via `gst_element_query_position()`. Confirm `dropped_frames` remains within acceptable baseline (< MIN_FRAMES_DROP threshold) throughout playback, validating that video codec and rendering pipeline maintain frame delivery performance without excessive frame loss during normal 1x playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent GStreamer libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | H264 video stream must be accessible via local file system (`filesrc` element) or HTTPS (`souphttpsrc` element); stream file path: `TDK_Asset_Sunrise_30fps_30secs.mp4` | Verify stream file is accessible and has 30fps frame rate with 30-second duration |
| 3 | Stream Variable Configuration | Stream URL must be configured in `MediaValidationVariables.py` as `video_src_url_mp4_frameDrop_h264 = test_streams_base_path + "TDK_Asset_Sunrise_30fps_30secs.mp4"` | Verify stream URL resolves to valid H264 MP4 file location |
| 4 | Frame Drop Test Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with timeout value (minimum 32 seconds for 30-second stream) and `NATIVE_PLAYBACK_CHECK_AV_STATUS` must be configured (yes/no) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to ≥32 seconds and CHECK_AV_STATUS configuration exists |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables for GStreamer 1.16+ H264 codec support |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve `NATIVE_PLAYBACK_CHECK_AV_STATUS` and `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` configuration values from device config file, construct `tdk_mediapipelinetests test_frameDrop` command with stream URL and timeout arguments | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes successfully |
| 3 | Create Playbin Pipeline and Set Stream URI | Create `playbin` element via `gst_element_factory_make()`, set stream URI to H264 file path via `g_object_set(pipeline, "uri", ...)`, attach `westerossink` as video sink via `g_object_set(pipeline, "video-sink", westerossink, NULL)` | Verify `playbin` element is created and configured with correct stream URI and video sink |
| 4 | Register First Frame Callback and Transition to PLAYING | Register `first-video-frame-callback` signal handler to detect first rendered frame, transition pipeline from `GST_STATE_NULL→GST_STATE_PLAYING` via `gst_element_set_state()` | Verify pipeline reaches `GST_STATE_PLAYING` and `first-video-frame-callback` signal is received within expected time |
| 5 | Poll Frame Statistics and Validate Increments | Poll `westerossink→stats.rendered_frames` and `dropped_frames` via `g_object_get(westerossink, "stats", &structure, NULL)` at 1ms intervals using `Sleep(1)` and `gst_structure_get_uint64()` to extract frame counts | Verify `rendered_frames` increments each polling cycle and `dropped_frames` remains minimal (< MIN_FRAMES_DROP baseline) |
| 6 | Monitor Playback Position and Frame Rate | Query playback position via `gst_element_query_position(pipeline, GST_FORMAT_TIME, &currentPosition)` to track playback progress at 1x rate; validate frame rendering rate matches stream fps (30fps for this H264 stream) | Verify position advances at 1x rate without stalls or backward jumps; frame increments match expected rendering rate |
| 7 | Continue Monitoring Until EOS or Target Frames Reached | Loop frame polling and position queries until either `gst_bus_pop_filtered(bus, GST_MESSAGE_EOS)` returns EOS message or rendered_frames reaches expected total (totalFrames parameter); validate `rendered_frames > previous_rendered_frames` on each iteration | Verify playback completes normally with expected frame count and no rendering stalls detected during playback loop |
| 8 | Transition to PAUSED, Validate Frame Drop Metrics, and Cleanup | Set pipeline state to `GST_STATE_PAUSED` via `gst_element_set_state()`, calculate expected_rendered_frames based on fps and duration, validate actual rendered_frames matches expected (with <MIN_FRAMES_DROP tolerance), release pipeline via `terminatePipeline()` to transition to `GST_STATE_NULL` | Verify dropped_frames is within acceptable baseline, pipeline transitions to NULL, GCheck reports `Failures: 0` and `Errors: 0` |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
