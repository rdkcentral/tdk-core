## TestCase ID
RDKV_NATIVE_PLAYBACK_347

## TestCase Name
RDKV_CERT_NPVS_Video_PTS_Sync_HLS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate video Presentation Time Stamp (PTS) synchronization and frame rendering accuracy for HTTP Live Streaming (HLS) adaptive bitrate streaming by continuously polling the property from at 100ms intervals and comparing against playback position obtained. Verify video-pts values remain strictly monotonically increasing without backward jumps or discontinuities that would indicate sync errors despite adaptive bitrate switches, and validate that rendered frame count increments consistently property while dropped frame count remains minimal. Confirm HLS demuxer correctly parses M3U8 playlists and media segments, and PTS progression remains synchronized during bitrate transitions.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration | HLS media stream with `.m3u8` playlist and media segments must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`)<br> Stream playlist URL: `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` configured in MediaValidationVariables.py Stream variable `video_src_url_hls` configured in `MediaValidationVariables.py` with URL: `HLS_H264_AAC/master.m3u8` (HLS adaptive bitrate stream for PTS sync validation during bitrate transitions) | Verify HLS `.m3u8` playlist URL is reachable, all media segments are accessible, and GStreamer `hlsdemux` plugin can parse the playlist Verify `video_src_url_hls` resolves to valid, accessible HLS master playlist containing H.264 video and AAC audio segments |
| 3 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, HLS demuxer, H.264 codec library paths, and Wayland display configuration. Establish Wayland display session<br>via RDKWindowManager or westeros compositor. Create logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace  | Verify `/opt/TDK/TDK.env` loads successfully, GST_PLUGIN_PATH includes HLS demux plugin, Wayland display is active, logging file created without errors |
| 2 | Configure Playbin and Load HLS Stream |  Create `playbin` element<br>via `gst_element_factory_make("playbin", NULL)`. Configure `uri` property to HLS master playlist URL from MediaValidationVariables.video_src_url_hls<br>via `g_object_set(playbin, "uri", url, NULL)`. Set `video-sink` property to `westerossink`<br>via `g_object_set(playbin, "video-sink", westerossink_element, NULL)`  | Verify playbin element created successfully, `uri` property set to HLS M3U8 playlist URL, `video-sink` configured to westerossink element |
| 3 | Register Sink Signals and Setup Callbacks |  Register `first-video-frame-callback` signal<br>via `g_signal_connect()` to detect when first frame is rendered. Register `pts-error-callback` signal to detect presentation timestamp errors. Connect to GStreamer bus<br>via `gst_element_get_bus()` to monitor `GST_MESSAGE_ERROR`, `GST_MESSAGE_EOS`, `GST_MESSAGE_STATE_CHANGED`, and `GST_MESSAGE_ELEMENT` (for bitrate switches))<br>messages  | Verify all signals registered successfully, bus message handler is active, bitrate change monitoring enabled |
| 4 | Transition Pipeline to Playing State and Confirm Rendering | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`<br> Monitor `first-video-frame-callback` signal to confirm first frame rendering started<br> Verify `hlsdemux` successfully downloads and parses master M3U8 playlist and fetches first media segment<br> Verify state change to PLAYING completed within 5 seconds timeout | Verify pipeline transitions to PLAYING state, first frame signal is detected, HLS playlist downloaded and parsed, media segments fetched, no `GST_MESSAGE_ERROR` on bus |
| 5 | Poll Video-PTS Property and Validate Continuous Progression | Starting from pipeline PLAYING state, poll `video-pts` property from westerossink every 100ms via `g_object_get(westerossink, "video-pts", &pts, NULL)`<br> Store previous PTS value and compare: verify pts > old_pts (strictly monotonically increasing)<br> If pts == 0 or pts <= old_pts during PLAYING state, record PTS validation failure<br> Monitor for bitrate switches and verify PTS remains continuous across segment boundaries | Verify `video-pts` values increment continuously without backward jumps, even during bitrate switches or segment transitions. If any backward jump detected, test fails with PTS sync error |
| 6 | Query Playback Position and Validate Smooth Progression | Every 100ms (synchronized with PTS polling), query playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` in nanosecond units<br> Calculate position increment: (current_position - previous_position) / GST_SECOND<br> Verify position increment is ~0.1 seconds +/-0.025 seconds (+/-25% tolerance)<br> Monitor for segment fetches and verify position advances smoothly during HLS segment transitions | Verify position increments consistently without stalls, backward jumps, or excessive forward jumps, including during segment fetches |
| 7 | Validate Frame Rendering Statistics |  Every 100ms, poll `g_object_get(westerossink, "stats")` property<br>via `g_object_get(westerossink, "stats", &structure, NULL)`. Extract `rendered` count<br>via `gst_structure_get_uint64(structure, "rendered", &rendered_frames)` and `dropped` count<br>via `gst_structure_get_uint64(structure, "dropped", &dropped_frames)`. Verify rendered_frames value is non-zero and increments consistently even during bitrate switches. Calculate dropped_frame_percentage = dropped_frames / (rendered_frames + dropped_frames). Verify dropped frame percentage < 1%  | Verify rendered frame count increments consistently, dropped frames remain minimal (< 1%), rendering continues smoothly during bitrate transitions |
| 8 | Monitor Pipeline EOS and Validate Completion | Monitor GStreamer bus via `gst_bus_pop_filtered()` to detect `GST_MESSAGE_EOS` message indicating stream end<br> When EOS detected or playback timeout reached, verify test metrics are captured<br> Check for any `GST_MESSAGE_ERROR` messages indicating pipeline, HLS demuxing, or segment fetch failures | Verify `GST_MESSAGE_EOS` detected when stream ends, no error messages recorded, all media segments successfully fetched and processed |
| 9 | Release Pipeline and Cleanup Resources |  Set pipeline state to `GST_STATE_NULL`<br>via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin element<br>via `gst_object_unref(playbin)`. Close logging file. Deallocate all GStreamer structures and callback references  | Verify pipeline reaches `GST_STATE_NULL`, all GStreamer objects unreferenced, logging closed, system ready for subsequent tests |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121









