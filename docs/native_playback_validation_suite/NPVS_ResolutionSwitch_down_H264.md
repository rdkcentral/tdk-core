## TestCase ID
NATIVE_PLAYBACK_115

## TestCase Name
NPVS_ResolutionSwitch_down_H264

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate dynamic video resolution switching during playback through `playbin` element monitoring westerossink video pad properties. Test verifies stream contains exactly 7 unique resolutions (2160p, 1080p, 720p, 480p, 360p, 240p, 144p (descending)) and detects each resolution change via  at 100ms intervals combined with video-height/video-width property queries. Confirm pipeline transitions through all resolutions without decoding failures, GST_MESSAGE_ERROR, or frame drops during switching by polling rendered_frames/dropped_frames from westerossink sink statistics.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary, GStreamer plugins (qtdemux, x-h264 decoder), and westerossink element | Verify TDK_Package is installed, binary is executable, qtdemux element available, H.264 decoder registered in GStreamer |
| 2 | Media Stream Provisioning | H.264 video stream with multiple resolutions (high (4K) to low (144p) resolution) must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file path configured in MediaValidationVariables.py as `test_streams_base_path + "TDK_Asset_Sunrise_H264_resolution_down.mp4"`  | Verify TDK_Asset_Sunrise_H264_resolution_down.mp4 is accessible and readable from filesystem with multiple embedded resolution representations |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_resolution_down_h264` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "TDK_Asset_Sunrise_H264_resolution_down.mp4"` (local file access, not DASH/HLS streams) | Verify `video_src_url_resolution_down_h264` resolves to valid, accessible H.264 MP4 file location with resolution switching capability |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env`. Westerossink must be available and configured for video rendering | Verify `/opt/TDK/TDK.env` exists with all required environment variables, westerossink element registered in GStreamer |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, westerossink element, and Wayland display configuration. Establish Wayland display session via RDKWindowManager. Create logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify all environment variables load correctly, Wayland display session created successfully, logging initialized without errors |
| 2 | Configure Test Framework and Load Stream | Set test name to `test_resolution_down`, configure `ResolutionSwitchTest = true` flag in test framework. Load H.264 stream via `video_src_url_resolution_down_h264` variable from MediaValidationVariables.py. Set test timeout to 70 seconds for complete resolution traversal | Verify test case name and flags configured, TDK_Asset_Sunrise_H264_resolution_down.mp4 stream URI resolved successfully, timeout set to 70 seconds |
| 3 | Create Playbin Pipeline and Configure Westerossink | Create `playbin` element via . Set `uri` property to local file path via . Set `video-sink` property to `westerossink` element via  | Verify playbin element created successfully, URI property set to TDK_Asset_Sunrise_H264_resolution_down.mp4 file path, video-sink property configured with westerossink element |
| 4 | Transition Pipeline to PLAYING State and Detect First Resolution | Set pipeline state to  via . Monitor  on GStreamer bus. Query initial video-height and video-width from westerossink via  and . Initialize `ResolutionCount = 1` when first resolution (144p for UP, 2160p for DOWN) detected | Verify pipeline transitions to PLAYING state without errors, first resolution identified and ResolutionCount initialized to 1 |
| 5 | Monitor Resolution Changes During Playback | Execute `PlaybackValidation()` function which  For each position poll, query current video-height and video-width from westerossink. Compare new height with previous height to detect resolution changes. Maintain array `resolutionSeen[]` to track unique resolutions encountered (reference source: MediaPipelineSuite.cpp lines 1100-1160) | Verify position queries return valid, incrementing timestamps at 100ms poll intervals. New height/width queries detect each resolution transition. No duplicate resolution entries recorded |
| 6 | Validate Detected Resolutions Against Expected Sequence | When new_height differs from previous height, verify it matches one of the expected values (144, 240, 360, 480, 720, 1080, 2160) with ±5 pixel tolerance (RESOLUTION_OFFSET). Increment `ResolutionCount` for each unique, previously unseen resolution. Verify resolutions appear in correct sequence: 2160p, 1080p, 720p, 480p, 360p, 240p, 144p (descending) | Verify each resolution change matches expected value within tolerance. ResolutionCount increments only for new resolutions. Sequence follows down progression without gaps or out-of-order resolutions |
| 7 | Monitor Rendered Frames and Frame Drop Statistics | Query westerossink element properties via  and  at periodic intervals during playback. Verify rendered_frames continuously increments at ~30 FPS (consistent with video encoding). Monitor for GST_MESSAGE_ERROR or GST_MESSAGE_WARNING on GStreamer bus during resolution switches | Verify rendered_frames count increments continuously (~30 frames per second), dropped_frames remains at 0 or acceptable level (<1% of rendered_frames), no error/warning messages on bus |
| 8 | Validate All Resolutions Traversed Successfully | Continue PlaybackValidation until `ResolutionCount == TOTAL_RESOLUTIONS_COUNT (7)` or playback timeout reached. Verify `resolutionSeen[]` array shows all 7 expected resolutions were encountered during playback. Pipeline reaches  from GStreamer bus or test timeout expires after complete resolution traversal | Verify ResolutionCount equals 7, all 7 resolutions detected and recorded in resolutionSeen[], pipeline completed full sequence without stalls or decoder failures |
| 9 |  Free allocated memory, close logging file. Verify test framework output shows "Failures: 0" and "Errors: 0" in mediapipelinetests console output | Verify pipeline reaches GST_STATE_NULL state successfully, all GStreamer resources released without segmentation faults, mediapipelinetests reports successful test completion with zero failures and errors |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
