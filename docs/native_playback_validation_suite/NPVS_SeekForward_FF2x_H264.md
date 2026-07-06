**TestCase ID**
NATIVE_PLAYBACK_208

**TestCase Name**
NPVS_SeekForward_FF2x_H264

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate forward seek operation to future position beyond current playback location. The test invokes `gst_element_seek()` with target position ahead of current timestamp, simulating user fast-skip behavior. Verify seek operation repositions pipeline to the forward target without stalling or buffer underflow exceptions. Confirm position queries return values matching the forward seek target, and for DASH streams verify dashdemux correctly repositions to the appropriate segment boundary; for HLS verify hlsdemux skips to correct playlist segment. Resume playback from seeked position and validate continuous rendering without glitches.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (DASH container format for forward fast-forward testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_dash_h264` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify `video_src_url_dash_h264` resolves to valid DASH manifest URL, manifest contains valid MPD structure with Period, AdaptationSet, Representation elements |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec libraries, and Wayland display configuration. Establish Wayland display session. Set up logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Verify all environment variables load correctly, Wayland display created, H.264 plugins available, logging initialized |
| 2 | Create Playbin and Configure Video Sink | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure URI via `g_object_set(playbin, "uri", stream_url, NULL)` with H.264 stream path. Create and set `westerossink` as video sink via `g_object_set(playbin, "video-sink", westerossink, NULL)` | Playbin created successfully, URI configured, westerossink set as video sink |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via `g_signal_connect()` for frame detection. Set playbin flags (VIDEO, AUDIO, BUFFERING) via `g_object_set(playbin, "flags", flags, NULL)`. Register bus message handler for ERROR, EOS, STATE_CHANGED | All signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set pipeline state `GST_STATE_PAUSED` via `gst_element_set_state()`. Transition to `GST_STATE_PLAYING` via `gst_element_set_state()`. Query initial position via `gst_element_query_position()`. Monitor first-frame signal for rendering confirmation | Pipeline state changed to PLAYING, first frame signal detected, baseline position recorded |
| 5 | Execute Forward Seek Operation | Query current playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)`. Calculate seek target later in stream (e.g., +30 seconds from current). Invoke `gst_element_seek(playbin, 1.0, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` | Seek operation completes without errors, pipeline continues playing |
| 6 | Validate Seek Target Accuracy | Monitor bus via `gst_bus_pop_filtered()` for `GST_MESSAGE_ASYNC_DONE` confirming seek completion. Poll `gst_element_query_position()` every 100ms to verify position matches seek target within ±GST_SECOND (±1000ms). Confirm position stabilizes at target | Position queries show currentPosition ≈ seekPosition ±1000ms, seek confirmed successful |
| 7 | Monitor Playback Continuation and Frame Statistics | Continue polling position every 100ms. Every 1 second, poll westerossink stats via `g_object_get(westerossink, "stats", &structure)`. Extract rendered_frames and dropped_frames via `gst_structure_get_uint64()`. Verify rendered frames increment, dropped frames < 1%. Query video-pts via `g_object_get(westerossink, "video-pts", &pts)` | Rendered frame count increases per second, dropped < 1%, PTS advances without gaps |
| 8 | Monitor EOS and Validate Playback Quality | Continue monitoring until `GST_MESSAGE_EOS` detected on bus via `gst_bus_pop_filtered()`. Verify no `GST_MESSAGE_ERROR` messages detected. Confirm PTS monotonicity maintained - no backward jumps | EOS detected or timeout reached, no errors, PTS strictly increasing |
| 9 | Release Pipeline Resources | Set pipeline state `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin via `gst_object_unref(playbin)`. Close logging, free memory, verify system ready | Pipeline state becomes NULL, all resources released, logging closed |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
