**TestCase ID**
NATIVE_PLAYBACK_197

**TestCase Name**
NPVS_Channel_Change_H264_to_4K

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate seamless video stream switching capability via playbin pipeline. Execute channel change operation from H.264 DASH stream (HD resolution) to 4K HLS stream by setting pipeline to NULL state, updating stream URI, and resuming playback. Confirm that URI modification during NULL state enables successful second stream playback without pipeline interruption, position query errors, or frame rendering degradation. Verify playback position advancement and frame rendering quality remain consistent across both streams.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | First Stream (H.264 DASH) Provisioning | DASH stream with H.264 video must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py as variable `video_src_url_dash_h264`. Stream contains H.264 video and AAC audio | Verify H.264 DASH stream is accessible and DASH manifest parseable with dashdemux |
| 3 | Second Stream (4K HLS) Provisioning | HLS stream with 4K video must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "HLS_4K/master.m3u8"` in MediaValidationVariables.py as variable `video_src_url_4k_hls`. Stream contains 4K H.264 video and AAC audio | Verify 4K HLS stream is accessible and HLS manifest parseable with hlsdemux |
| 4 | Stream Variable Configuration | Stream variables `video_src_url_dash_h264` = `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` and `video_src_url_4k_hls` = `test_streams_base_path + "HLS_4K/master.m3u8"` must be configured in `MediaValidationVariables.py` | Verify both stream variables resolve to valid, accessible stream locations with correct codec support |
| 5 | Playback Timeout Configuration | Test execution parameters must be retrieved from device configuration file: `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds per stream) and `NATIVE_PLAYBACK_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT` (default: 10 seconds for second stream) | Verify all device config parameters are accessible and contain valid values |
| 6 | Platform-Specific Environment Variables | Platform-specific environment variables must be defined in `/opt/TDK/TDK.env`: `WAYLAND_DISPLAY` (Wayland display server), `XDG_RUNTIME_DIR` (runtime directory for Wayland sockets), `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH` (GStreamer plugin directory) | Verify `/opt/TDK/TDK.env` exists with all environment variables, Wayland display functional, GStreamer 1.16+ installed |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log`. Retrieve device config: `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and `NATIVE_PLAYBACK_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT`. Retrieve stream URLs from `MediaValidationVariables.video_src_url_dash_h264` and `MediaValidationVariables.video_src_url_4k_hls` | Verify all environment variables load correctly, Wayland display created successfully, device config parameters retrieved, both stream URLs resolve to valid DASH and HLS manifests |
| 2 | Create Playbin Element and Configure First Stream | Create playbin element and configure first H.264 DASH stream URL as stream source via URI property. Set playback flags to enable video. Set westerossink as video rendering sink. Register first-video-frame-callback signal to detect initial frame rendering | Verify playbin element created successfully, H.264 DASH stream URI configured, playback flags set for video, video-sink set to westerossink, first-frame callback registered |
| 3 | Transition Pipeline to Playing State (First Stream - H.264 DASH) | Set pipeline to PLAYING state to begin H.264 DASH stream playback. Wait for first-video-frame-callback signal to confirm frame rendering started | Verify pipeline transitions to PLAYING state, playback begins without errors, first video frame from H.264 DASH stream rendered successfully |
| 4 | Monitor First Stream Playback | Continuously poll playback position at 100ms intervals for configured timeout duration (default 10 seconds) during H.264 DASH playback. Record timestamps to verify position advances at expected rate (1 second playback per 1 second real-time ±250ms tolerance). Query westerossink stats to verify video frame rendering (rendered_frames incrementing, dropped_frames minimal). Monitor for any error messages or stalls | Verify playback position advances continuously at 1.0x rate within tolerance, frame statistics show frames being rendered without excessive drops, no errors or stalls detected |
| 5 | Stop First Stream Playback and Release Pipeline State | Set pipeline to NULL state to stop playback and halt H.264 DASH stream processing. This flushes remaining buffered data and prepares pipeline for URI change | Verify pipeline transitions to NULL state successfully, no error messages from GStreamer bus |
| 6 | Update Stream URI to Second Stream (4K HLS) | While pipeline is in NULL state, update URI property to 4K HLS stream URL (`MediaValidationVariables.video_src_url_4k_hls`). This allows seamless stream switching without recreating pipeline elements | Verify URI property updated successfully to 4K HLS stream path, new URI resolves to accessible HLS manifest |
| 7 | Transition Pipeline to Playing State (Second Stream - 4K HLS) | Set pipeline to PLAYING state to begin 4K HLS stream playback. Wait for stream-start message or first-video-frame-callback signal to confirm second stream is rendering. Stream-start message should arrive within 2 seconds | Verify pipeline transitions to PLAYING state, stream-start message detected or first frame rendered, second stream begins playback without errors |
| 8 | Monitor Second Stream Playback | Continuously poll playback position at 100ms intervals for configured timeout duration (default 10 seconds) during 4K HLS playback. Record timestamps to verify position advances at expected rate. Query westerossink stats to verify video frame rendering on second stream. Monitor for any error, EOS, or stall messages | Verify playback position advances continuously at 1.0x rate from start of second stream, frame statistics show frames rendering without excessive drops, no errors detected on second stream |
| 9 | Validate Stream Change Success | Compare playback metrics across both streams: position advancement rates should be similar, frame statistics should show consistent rendering quality. Verify test framework output shows `Failures: 0` and `Errors: 0` for entire stream change operation | Verify stream change operation completed successfully with matching quality metrics, test shows no failures/errors |
| 10 | Release Pipeline and Cleanup Resources | Set pipeline to NULL state to stop playback and terminate 4K HLS stream. Unreference GStreamer objects and free allocated memory. Close logging file | Verify pipeline reaches NULL state, all resources released, logging closed, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3-4 minutes

**Priority:** High

**Release Version:** M121
