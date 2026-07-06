## TestCase ID
NATIVE_PLAYBACK_09

## TestCase Name
NPVS_Play_Live_HLS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate live H.264 streaming via HLS protocol with `test_generic_playback` function. Initialize playbin with `hlsdemux` for live stream adaptation, monitor manifest updates and segment fetching. Execute continuous playback without seeking, verify position advances at real-time 1x rate. Query video dimensions via `westerossink` properties, monitor frame rendering via `westerossinkâ†’stats`. Confirm adaptive bitrate switching and pipeline stability during live stream playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | External online HLS H.264 AAC live stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) element with `hlsdemux` capable of parsing HLS container for live stream adaptation | Verify external online HLS stream is accessible and contains valid H.264 and AAC representations for continuous live streaming |
| 3 | Stream Variable Configuration | `video_src_url_hls` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` | Verify `video_src_url_hls` resolves to valid external online HLS stream with correct codec support |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout configured for standard playback (10 seconds) | Verify `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` is set to 10 seconds in configuration file | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env`; Establish Wayland display session; Prepare for live stream handling | Verify environment loaded, display ready |
| 2 | Configure Live Stream Test | Retrieve stream URL from `video_src_url_hls` (live HLS); Configure for adaptive bitrate handling; Execute `mediapipelinetests test_generic_playback <URL>` | Verify live HLS stream configured |
| 3 | Construct Live H.264 Pipeline | Create `playbin` element; Configure `uri` to video_src_url_hls (live HLS manifest); Set `westerossink` as video sink; Transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING`, manifest fetched |
| 4 | Query Video Properties and Monitor Segments | Query `westerossinkâ†’video-height/width` to confirm stream resolution; Monitor segment fetching and manifest updates via GStreamer debug logging | Verify video dimensions detected; Verify segments fetching |
| 5 | Monitor Live Playback Position | Execute continuous playback monitoring position via `gst_element_query_position()` at 100ms intervals; Verify position advances at real-time 1x rate | Verify position advances at 1x rate matching live time |
| 6 | Validate Adaptive Bitrate Switching | Monitor HLS demuxer for bitrate adaptation events; Verify smooth bitrate transitions without playback interruptions | Verify bitrate changes detected; Verify smooth transitions |
| 7 | Monitor Frame Rendering During Live | Query `westerossinkâ†’stats` to track `rendered_frames` and `dropped_frames` during live adaptive streaming | Verify frames render consistently; Verify `dropped_frames` < 1% |
| 8 | Monitor GStreamer Bus | Monitor message bus via `gst_bus_pop()` for streaming errors or format issues; Verify live stream remains stable | Verify no streaming errors detected |
| 9 | Release Resources | Stop playback and release all resources via `terminatePipeline(playbin)`; Verify clean shutdown | Verify test output shows "Failures: 0" for live streaming |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
