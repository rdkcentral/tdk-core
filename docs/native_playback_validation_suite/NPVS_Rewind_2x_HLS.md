## TestCase ID
NATIVE_PLAYBACK_97

## TestCase Name
NPVS_Rewind_2x_HLS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate reverse playback at 2x speed (playback rate = -2) on H.264 video with AAC audio via hlsdemux demuxer. Test executes seek operation to stream position (2*NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT + 30 seconds) via `gst_element_seek()` with GST_SEEK_FLAG_FLUSH, then applies negative playback rate via `gst_element_seek(playbin, -2, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, 0, GST_SEEK_TYPE_SET, currentPosition)`. Validate position decreases at expected rate during 2x reverse playback for NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT seconds with position tolerance Â±250ms, no GST_MESSAGE_ERROR, and continuous rendered frames

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary, GStreamer plugins (hlsdemux demuxer, necessary decoders), and westerossink element | Verify TDK_Package is installed, binary is executable, hlsdemux element available in GStreamer |
| 2 | Media Stream Provisioning | HLS H.264/AAC stream must be accessible via network (`souphttpsrc` element for streaming) or local file system (`filesrc`). Stream file path configured in MediaValidationVariables.py as `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` | Verify HLS_H264_AAC/master.m3u8 is accessible via HTTP or local storage with adequate duration (minimum 2*timeout + 30 seconds) |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_hls` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "HLS_H264_AAC/master.m3u8"`. hlsdemux capable of parsing stream and extracting audio/video representations | Verify `video_src_url_hls` resolves to valid, accessible HLS H.264/AAC stream location |
| 4 | Rewind Operation Parameters | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with timeout value (default: 10 seconds). Rewind operation configured with seek duration = 2*timeout + 30 seconds, then rewind rate = -2 applied for timeout seconds | Verify timeout is set, seek duration calculated correctly, rewind speed parameter 2x set in test runner |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required variables, westerossink available, Wayland display active |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, hlsdemux demuxer, decoders, westerossink, and Wayland display configuration. Establish Wayland display session via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify all environment variables load correctly, Wayland display session created successfully, logging initialized without errors |
| 2 | Configure Test Framework and Load Stream | Set test name to `test_trickplay`, Load HLS H.264/AAC stream via `video_src_url_hls` variable from MediaValidationVariables.py. Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and calculate seek duration = 2*timeout + 30 seconds | Verify test case name configured, HLS_H264_AAC/master.m3u8 stream URI resolved successfully, timeout retrieved and seek duration calculated |
| 3 | Create Playbin Pipeline and Configure Sinks | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Set `uri` property to stream URL via `g_object_set(playbin, "uri", stream_url, NULL)`. Set `video-sink` property to `westerossink` element (or `autoaudiosink` for audio-only) via `g_object_set(playbin, "video-sink", westerossink, NULL)` | Verify playbin element created successfully, URI property set to HLS_H264_AAC/master.m3u8, video-sink properly configured |
| 4 | Transition Pipeline to PLAYING and Initial Buffering | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`. Monitor `GST_MESSAGE_STREAM_START` on GStreamer bus. Wait for initial buffering to complete via `GST_MESSAGE_ASYNC_DONE` (2-second timeout). Query initial playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` | Verify pipeline transitions to PLAYING state without errors, stream start message detected, initial position queried successfully |
| 5 | Execute Forward Seek to Calculated Position | Calculate seek target: `seekPosition = (2 * NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT + 30) * GST_SECOND`. Execute `gst_element_seek(playbin, 1.0, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_SET, GST_CLOCK_TIME_NONE)` to advance stream to seek target position. Monitor `GST_MESSAGE_ASYNC_DONE` on bus (2-second timeout for seek completion). Query new position via `gst_element_query_position()` to verify seek accuracy within Â±250ms tolerance | Verify seek executed successfully, position advanced to target within tolerance, no GST_MESSAGE_ERROR on bus |
| 6 | Apply Negative Playback Rate for Rewind | Set `setRate = -2` (negative value for reverse playback). Execute `gst_element_seek(playbin, -2, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, 0, GST_SEEK_TYPE_SET, currentPosition)` to initiate 2x reverse playback (reference source: mediapipelinetests_trickplay.cpp lines 1115-1119). Monitor `GST_MESSAGE_ASYNC_DONE` on bus (2-second timeout). Query position to confirm reverse playback initiated | Verify rewind operation executed successfully, pipeline in reverse playback mode at rate -2, position query reflects reverse progression |
| 7 | Monitor Position During Rewind Playback | Execute `PlaybackValidation()` function which polls position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` at 100ms intervals. For each poll, verify position DECREASES from previous value (reverse playback verification). Calculate position delta per 100ms interval; expected rate â‰ˆ -2/3/4 seconds per second real-time depending on rewind speed. Verify position decrements stay within tolerance (Â±250ms per interval) | Verify position queries return valid, monotonically decreasing timestamps, position deltas consistent with 2x reverse rate, no backward-forward jitter |
| 8 | Validate Frame Rendering and Decode During Rewind | Query westerossink element properties via `g_object_get(westerossink, "rendered-frames", &rendered_frames, NULL)` and `g_object_get(westerossink, "dropped-frames", &dropped_frames, NULL)` at periodic intervals. Verify rendered_frames increments (frame decoding continues during rewind). Monitor for `GST_MESSAGE_ERROR`, `GST_MESSAGE_WARNING` on GStreamer bus during entire rewind operation. Verify no decoder underflows or buffer stalls during reverse playback | Verify rendered_frames count increments during rewind operation, dropped_frames remains at acceptable level, no error/warning messages detected |
| 9 | Validate Rewind Completion and Release Pipeline | Continue rewind playback for NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT seconds. Monitor until position reaches near stream beginning or timeout expires. Set pipeline state to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin and sink elements via `gst_object_unref()`. Verify test framework output shows "Failures: 0" and "Errors: 0" in mediapipelinetests console output | Verify rewind operation completed for full timeout duration, pipeline transitions to NULL state successfully, all resources released, test reports zero failures and errors |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
