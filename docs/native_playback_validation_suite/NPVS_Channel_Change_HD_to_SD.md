## TestCase ID
NATIVE_PLAYBACK_194

## TestCase Name
NPVS_Channel_Change_HD_to_SD

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate seamless resolution switching from HD (1080p) to SD (360p). The test pauses playback, switches to lower resolution, and resumes playback to verify smooth transition without interruption. Confirm playback position advances correctly and rendering quality remains consistent across different resolutions.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | First Stream (HD 1080p) Provisioning | HD 1080p H.264 MP4 stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_H264_1080p.mp4"` in MediaValidationVariables.py as variable `video_src_url_1080p`. Stream contains 1080p H.264 video | Verify HD 1080p stream is accessible and manifest parseable |
| 3 | Second Stream (SD 360p) Provisioning | SD 360p H.264 MP4 stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_H264_360p.mp4"` in MediaValidationVariables.py as variable `video_src_url_360p`. Stream contains 360p H.264 video | Verify SD 360p stream is accessible and manifest parseable |
| 4 | Stream Variable Configuration | Stream variables `video_src_url_1080p` = `test_streams_base_path + "TDK_Asset_Sunrise_H264_1080p.mp4"` and `video_src_url_360p` = `test_streams_base_path + "TDK_Asset_Sunrise_H264_360p.mp4"` must be configured in `MediaValidationVariables.py` | Verify both stream variables resolve to valid, accessible stream locations |
| 5 | Playback Timeout Configuration | Test execution parameters must be retrieved from device configuration file: `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds per stream) and `NATIVE_PLAYBACK_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT` (default: 10 seconds for second stream) | Verify all device config parameters are accessible and contain valid values |
| 6 | Platform-Specific Environment Variables | Platform-specific environment variables must be defined in `/opt/TDK/TDK.env`: `WAYLAND_DISPLAY` (Wayland display server), `XDG_RUNTIME_DIR` (runtime directory for Wayland sockets), `LD_PRELOAD` with vendor libraries,  (GStreamer plugin directory) | Verify `/opt/TDK/TDK.env` exists with all environment variables, Wayland display functional, GStreamer 1.16+ installed |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log`. Retrieve device config: `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and `NATIVE_PLAYBACK_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT`. Retrieve stream URLs from `MediaValidationVariables.video_src_url_1080p` and `MediaValidationVariables.video_src_url_360p` | Verify all environment variables load correctly, Wayland display created successfully, device config parameters retrieved, both stream URLs resolve to valid HD 1080p and SD 360p manifests |
| 2 | Create Playbin Element and Configure First Stream | Create playbin element and configure first HD 1080p stream URL as stream source via URI property. Set playback flags to enable video. Set westerossink as video rendering sink. Register first-video-frame-callback signal to detect initial frame rendering | Verify playbin element created successfully, HD 1080p stream URI configured, playback flags set for video, video-sink set to westerossink, first-frame callback registered |
| 3 | Transition Pipeline to Playing State (First Stream - HD 1080p) | Set pipeline to PLAYING state to begin HD 1080p stream playback. Wait for first-video-frame-callback signal to confirm frame rendering started | Verify pipeline transitions to PLAYING state, playback begins without errors, first video frame from HD 1080p stream rendered successfully |
| 4 | Monitor First Stream Playback | Continuously poll playback position at 100ms intervals for configured timeout duration (default 10 seconds) during HD 1080p playback. Record timestamps to verify position advances at expected rate (1 second playback per 1 second real-time ±250ms tolerance). Query westerossink stats to verify video frame rendering (rendered_frames incrementing, dropped_frames minimal). Monitor for any error messages or stalls | Verify playback position advances continuously at 1.0x rate within tolerance, frame statistics show frames being rendered without excessive drops, no errors or stalls detected |
| 5 | Stop First Stream Playback and Release Pipeline State | Set pipeline to NULL state to stop playback and halt HD 1080p stream processing. This flushes remaining buffered data and prepares pipeline for URI change | Verify pipeline transitions to NULL state successfully, no error messages from GStreamer bus |
| 6 | Update Stream URI to Second Stream (SD 360p) | While pipeline is in NULL state, update URI property to SD 360p stream URL (`MediaValidationVariables.video_src_url_360p`). This allows seamless stream switching without recreating pipeline elements | Verify URI property updated successfully to SD 360p stream path, new URI resolves to accessible SD manifest |
| 7 | Transition Pipeline to Playing State (Second Stream - SD 360p) | Set pipeline to PLAYING state to begin SD 360p stream playback. Wait for stream-start message or first-video-frame-callback signal to confirm second stream is rendering. Stream-start message should arrive within 2 seconds | Verify pipeline transitions to PLAYING state, stream-start message detected or first frame rendered, second stream begins playback without errors |
| 8 | Monitor Second Stream Playback | Continuously poll playback position at 100ms intervals for configured timeout duration (default 10 seconds) during SD 360p playback. Record timestamps to verify position advances at expected rate. Query westerossink stats to verify video frame rendering on second stream. Monitor for any error, EOS, or stall messages | Verify playback position advances continuously at 1.0x rate from start of second stream, frame statistics show frames rendering without excessive drops, no errors detected on second stream |
| 9 | Validate Stream Change Success | Compare playback metrics across both streams: position advancement rates should be similar, frame statistics should show consistent rendering quality. Verify test framework output shows `Failures: 0` and `Errors: 0` for entire stream change operation | Verify stream change operation completed successfully with matching quality metrics, test shows no failures/errors |
| 10 | Release Pipeline and Cleanup Resources | Set pipeline to NULL state to stop playback and terminate SD 360p stream. Unreference GStreamer objects and free allocated memory. Close logging file | Verify pipeline reaches NULL state, all resources released, logging closed, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3-4 minutes

**Priority:** High

**Release Version:** M121
