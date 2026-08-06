## TestCase ID
RDKV_NATIVE_PLAYBACK_07

## TestCase Name
RDKV_CERT_NPVS_Play_VP9

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate VP9 video codec with OPUS audio using DASH streaming. Initialize playbin with dashdemux element, configure westerossink as video sink and alsasink for audio output. Query video dimensions and audio stream count via 'current-video' and 'current-audio' properties. Execute 10-second playback monitoring position advancement and frame rendering via westerossink stats.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  DASH VP9 OPUS stream (`master.mpd`))<br>must be accessible via HTTPS (`souphttpsrc`))<br>or local file system (`filesrc`))<br>element with `dashdemux` capable of parsing DASH container `video_src_url_vp9` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "DASH_VP9_OPUS_WebM/master.mpd"`  | Verify DASH stream is accessible and contains valid VP9 and OPUS representations Verify `video_src_url_vp9` resolves to valid DASH location with correct codec support |
|  3  |  Playback Timeout Configuration  |  `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config  | Verify timeout configured for standard playback (10 seconds); Verify timeout configured for standard playback (10 seconds); Verify `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` is set to 10 seconds in configuration file; Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session<br>via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log`  | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure and Execute Test Application | Retrieve configuration values for `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device config; Retrieve stream URL from `video_src_url_vp9` variable;<br>Execute `mediapipelinetests test_generic_playback <DASH_URL> timeout=<seconds>` | Verify mediapipelinetests initializes with VP9 DASH stream and timeout parameters |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element via `gst_element_factory_make()` with video_src_url_vp9 URI;<br>Configure `uri` property to video_src_url_vp9 manifest/file via `g_object_set()`; Set `video-sink` property to `westerossink` via `g_object_set()`;<br>Configure `autoaudiosink` for OPUS audio; Trigger state transition from `GST_STATE_NULL` to `GST_STATE_PLAYING` via `gst_element_set_state()`;<br>Monitor for `first-video-frame-callback` signal | Verify playbin reaches `GST_STATE_PLAYING` with first frame decoded, DASH manifest/file parsed successfully, no `GST_MESSAGE_ERROR` |
| 4 | Query Video and Audio Stream Properties | Query video dimensions via `g_object_get(westerossink, "video-height", &height, NULL)` and `g_object_get(westerossink, "video-width")`;<br>Query audio stream count via `g_object_get(playbin, "n-audio", &n_audio, NULL)` to verify OPUS stream presence; Log extracted properties | Verify video dimensions valid; Verify n-audio >= 1 confirming OPUS stream present |
| 5 | Play Stream for Configured Timeout | Execute continuous playback via PlaySeconds(playbin, play_timeout) or equivalent for configured timeout (default 10 seconds);<br>Monitor playback position via `gst_element_query_position()` at 100ms intervals to verify position advances at 1x rate | Verify playback position advances consistently at 1x rate (+/-1 second tolerance), no stalls or backward jumps detected |
| 6 | Validate Frame Rendering and Statistics | Poll `g_object_get(westerossink, "stats")` to verify `rendered_frames` increments indicating continuous video rendering;<br>Verify `dropped_frames` < 1% of rendered_frames throughout playback; Log frame statistics | Verify frame statistics indicate proper video rendering at VP9; Verify dropped frame rate acceptable |
| 7 | Monitor GStreamer Bus and Detect EOS | Monitor GStreamer message bus via `gst_bus_pop()` to detect `GST_MESSAGE_ERROR`, `GST_MESSAGE_WARNING`, or `GST_MESSAGE_EOS` messages;<br>Verify no error messages indicating codec decoding failures or stream parsing issues | Verify no decoder errors or format errors on bus; Verify clean playback without glitches or interruptions |
| 8 | Release Pipeline Resources | Call `terminatePipeline(playbin)` to set state to `GST_STATE_NULL` via `gst_element_set_state()` and release all GStreamer objects (playbin, DASH demuxer, westerossink, audio sink, bus);<br>Verify cleanup completes successfully without resource leaks | Verify pipeline reaches `GST_STATE_NULL`; Verify all resources released; Verify test output contains "Failures: 0" and "Errors: 0" or "failed: 0" |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121









