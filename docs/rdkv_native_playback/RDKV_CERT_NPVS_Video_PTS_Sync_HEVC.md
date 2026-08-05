## TestCase ID
RDKV_NATIVE_PLAYBACK_344

## TestCase Name
RDKV_CERT_NPVS_Video_PTS_Sync_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate HEVC video Presentation Time Stamp (PTS) synchronization and frame rendering accuracy by continuously polling the property from at 100ms intervals and comparing against playback position obtained. Verify video-pts values remain strictly monotonically increasing without backward jumps or discontinuities that would indicate sync errors, and validate that rendered frame count increments consistently property while dropped frame count remains minimal. Confirm PTS progression aligns with expected frame duration (3003 ticks per frame for 30fps video) and that pipeline maintains smooth video playback without rendering stalls or position jumps exceeding +/-250ms tolerance.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration | HEVC stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`)<br> Stream file path: `test_streams_base_path + "TDK_Asset_Sunrise_HEVC_30fps_v2.mp4"` configured in MediaValidationVariables.py Stream variable `video_src_url_hevc_30fps` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Sunrise_HEVC_30fps_v2.mp4` (30fps HEVC video for accurate PTS increment validation) | Verify HEVC stream file is accessible, readable, and GStreamer HEVC decoder plugin is loaded Verify `video_src_url_hevc_30fps` resolves to valid, accessible HEVC MP4 file location with 30fps encoding |
| 3 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, HEVC codec library paths, and Wayland display configuration. Establish Wayland display session<br>via RDKWindowManager or westeros compositor. Create logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace  | Verify `/opt/TDK/TDK.env` loads successfully, GST_PLUGIN_PATH includes HEVC plugin, Wayland display is active, logging file created without errors |
| 2 | Configure Playbin and Load HEVC Stream |  Create `playbin` element<br>via `gst_element_factory_make("playbin", NULL)`. Configure `uri` property to HEVC stream URL from MediaValidationVariables.video_src_url_hevc_30fps<br>via `g_object_set(playbin, "uri", url, NULL)`. Set `video-sink` property to `westerossink`<br>via `g_object_set(playbin, "video-sink", westerossink_element, NULL)`  | Verify playbin element created successfully, `uri` property set to HEVC stream path, `video-sink` configured to westerossink element |
| 3 | Register Sink Signals and Setup Callbacks |  Register `first-video-frame-callback` signal<br>via `g_signal_connect()` to detect when first frame is rendered. Register `pts-error-callback` signal to detect presentation timestamp errors. Connect to GStreamer bus<br>via `gst_element_get_bus()` to monitor `GST_MESSAGE_ERROR`, `GST_MESSAGE_EOS`, and `GST_MESSAGE_STATE_CHANGED` messages  | Verify all signals registered successfully and bus message handler is active |
| 4 | Transition Pipeline to Playing State and Confirm Rendering | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`<br> Monitor `first-video-frame-callback` signal to confirm first frame rendering started<br> Verify state change to PLAYING completed within 5 seconds timeout | Verify pipeline transitions to PLAYING state, first frame signal is detected, no `GST_MESSAGE_ERROR` on bus |
| 5 | Poll Video-PTS Property and Validate Continuous Progression | Starting from pipeline PLAYING state, poll `video-pts` property from westerossink every 100ms via `g_object_get(westerossink, "video-pts", &pts, NULL)`<br> Store previous PTS value and compare: verify pts > old_pts (strictly monotonically increasing)<br> If pts == 0 or pts <= old_pts during PLAYING state, record PTS validation failure<br> Continue polling for entire playback duration | Verify `video-pts` values increment continuously without backward jumps or discontinuities. If any backward jump detected, test fails with PTS sync error |
| 6 | Query Playback Position and Validate Smooth Progression | Every 100ms (synchronized with PTS polling), query playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` in nanosecond units<br> Calculate position increment: (current_position - previous_position) / GST_SECOND<br> Verify position increment is ~0.1 seconds +/-0.025 seconds (+/-25% tolerance)<br> Log any position jumps > 0.9 seconds as playback stalls | Verify position increments consistently without stalls, backward jumps, or excessive forward jumps |
| 7 | Validate Frame Rendering Statistics |  Every 100ms, poll `g_object_get(westerossink, "stats")` property<br>via `g_object_get(westerossink, "stats", &structure, NULL)`. Extract `rendered` count<br>via `gst_structure_get_uint64(structure, "rendered", &rendered_frames)` and `dropped` count<br>via `gst_structure_get_uint64(structure, "dropped", &dropped_frames)`. Verify rendered_frames value is non-zero and increments at expected rate (3 frames per second for 30fps video). Calculate dropped_frame_percentage = dropped_frames / (rendered_frames + dropped_frames). Verify dropped frame percentage < 1%  | Verify rendered frame count increments consistently, dropped frames remain minimal (< 1%), no rendering stalls detected |
| 8 | Monitor Pipeline EOS and Validate Completion | Monitor GStreamer bus via `gst_bus_pop_filtered()` to detect `GST_MESSAGE_EOS` message indicating stream end<br> When EOS detected or playback timeout reached, verify test metrics are captured<br> Check for any `GST_MESSAGE_ERROR` messages indicating pipeline failures | Verify `GST_MESSAGE_EOS` detected when stream ends, no error messages recorded |
| 9 | Release Pipeline and Cleanup Resources |  Set pipeline state to `GST_STATE_NULL`<br>via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin element<br>via `gst_object_unref(playbin)`. Close logging file. Deallocate all GStreamer structures and callback references  | Verify pipeline reaches `GST_STATE_NULL`, all GStreamer objects unreferenced, logging closed, system ready for subsequent tests |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121









