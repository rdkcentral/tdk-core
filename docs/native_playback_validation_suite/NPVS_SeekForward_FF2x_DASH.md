**TestCase ID**
NATIVE_PLAYBACK_211

**TestCase Name**
NPVS_SeekForward_FF2x_DASH

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates forward seeking capability on DASH streaming media by invoking `gst_element_seek()` to jump playback ahead to a position later in the media presentation. The test verifies that the seek target position is reached correctly using position queries every 100ms with tolerance of ±1 second, handling DASH playlist/segment updates. Validates playback resumes normally from the forward-seeked position with continuous video frame rendering and no PTS errors detected.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (DASH container format for forward fast-forward testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_dash` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify `video_src_url_dash` resolves to valid DASH manifest URL, manifest contains valid MPD structure with Period, AdaptationSet, Representation elements |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec, DASH streaming libraries. Establish Wayland display. Setup logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Environment variables load, Wayland created, DASH plugins available |
| 2 | Create Playbin and Configure Video | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure URI via `g_object_set(playbin, "uri", dash_stream_url, NULL)` with DASH manifest. Set `westerossink` as video sink | Playbin created, DASH URI configured, westerossink set |
| 3 | Register Callbacks and Setup Monitoring | Register `first-video-frame-callback` signal via `g_signal_connect()`. Set playbin flags (VIDEO, AUDIO, BUFFERING). Register bus message handler for ERROR, EOS, STATE_CHANGED | Signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing | Set state `GST_STATE_PAUSED` via `gst_element_set_state()`. Query initial position via `gst_element_query_position()`. Transition `GST_STATE_PLAYING`. Monitor first-frame signal | Pipeline PLAYING, first frame detected, baseline position recorded |
| 5 | Execute Forward Seek on DASH Stream | Query current position via `gst_element_query_position()`. Calculate forward seek target. Invoke `gst_element_seek(playbin, 1.0, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` handling manifest updates | Seek completes, DASH demux updates manifest, playback continues |
| 6 | Validate Forward Seek Accuracy on Streaming | Monitor bus for `GST_MESSAGE_ASYNC_DONE`. Poll `gst_element_query_position()` every 100ms verifying position within ±1000ms of target. Handle segment boundaries in manifest | Position matches target within ±1000ms, seek confirmed on DASH stream |
| 7 | Monitor Video Rendering on Streaming | Every 1 second poll westerossink stats. Extract rendered_frames and dropped_frames. Verify rendered frames increment, dropped < 1%. Query video-pts for monotonicity | Rendered frames increase per second, dropped < 1%, PTS continuous |
| 8 | Monitor EOS and Validate Stream Integrity | Continue until `GST_MESSAGE_EOS` or timeout. Verify no `GST_MESSAGE_ERROR` during streaming and seeking operations | EOS or timeout detected, no errors on DASH stream |
| 9 | Release Pipeline Resources | Set state `GST_STATE_NULL`. Unreference playbin via `gst_object_unref()`. Close logging, free memory | Pipeline NULL, resources released |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
