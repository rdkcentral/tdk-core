## TestCase ID
NATIVE_PLAYBACK_272

## TestCase Name
NPVS_Bitrate_Switch_Up_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate adaptive bitrate upgrade on HEVC DASH streams. The test progressively increases bitrate and resolution from lowest to highest available tiers. Verify each bitrate switch happens seamlessly without pipeline interruption, audio/video synchronization loss, or decoding errors. Confirm video resolution adapts correctly during upgrade progression.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries (mediapipelinetests binary implements GStreamer playbin pipeline with dashdemux DASH demultiplexer and westerossink video sink for adaptive bitrate switching) | Verify TDK_Package is installed, `tdk_mediapipelinetests` binary is executable, all GStreamer DASH demux and video plugin dependencies available |
| 2 | DASH Media Stream with Multiple Bitrate Tiers | DASH manifest (MPD file) must be accessible via HTTP/HTTPS or local file system (`filesrc`) containing multiple video representations with different bitrate and resolution combinations. Stream URL is configured via MediaValidationVariables.py variable `video_src_url_bitrate_hevc` with external DASH manifest (external stream source). HEVC DASH manifest must contain minimum 3 resolution tiers (e.g., 720p@5Mbps, 1080p@8Mbps, 2160p@15Mbps). MPD file must define `bandwidth` and `height` attributes for each representation | Verify external DASH manifest file is accessible, parseable, contains multiple HEVC video representations with distinct bitrate and resolution values, MPD XML structure valid |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_bitrate_hevc` must be configured in `MediaValidationVariables.py` with valid DASH manifest URL containing HEVC codec video stream with multiple bitrate/resolution tiers | Verify `video_src_url_bitrate_hevc` variable resolves to valid, accessible DASH manifest location with HEVC multi-bitrate stream |
| 4 | Device Configuration Parameters | Test execution parameters must be retrieved from device configuration file: , `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) for playback duration per bitrate iteration | Verify all device config parameters are accessible and contain valid values |
| 5 | Platform-Specific Environment and GStreamer Configuration | Platform-specific environment variables must be defined in `/opt/TDK/TDK.env`: `WAYLAND_DISPLAY` (Wayland display server), `XDG_RUNTIME_DIR` (runtime directory for Wayland sockets), `LD_PRELOAD` with vendor audio/video libraries,  (GStreamer plugin directory). GStreamer must have: playbin element, dashdemux DASH demultiplexer with `max-bitrate` property support, HEVC video decoder, and westerossink video sink | Verify `/opt/TDK/TDK.env` exists with all environment variables, Wayland display functional, GStreamer 1.16+ installed with playbin, dashdemux, and westerossink with adaptive bitrate support in GST_PLUGIN_PATH |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Retrieve Configuration | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration (GST_PLUGIN_PATH, LD_PRELOAD, WAYLAND_DISPLAY, XDG_RUNTIME_DIR). Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log`. Retrieve device config: `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT`. Retrieve stream URL from `MediaValidationVariables.video_src_url_bitrate_hevc` | Verify all environment variables load correctly, Wayland display created successfully, device config parameters retrieved, stream URL resolves to valid DASH manifest |
| 2 | Parse DASH Manifest (MPD) to Extract Bitrate and Resolution Tiers | Download and parse MPD (MPEG-DASH manifest) file from `video_src_url_bitrate_hevc` URL using CURL (for HTTP/HTTPS) or local file read (for `file://` protocol). Parse XML structure: `<MPD><Period><AdaptationSet contentType="video"><Representation>` to extract `bandwidth` (bits/sec) and `height` (pixels) attributes from each HEVC representation. Filter representations to include only HEVC codec (check `mimeType="video/mp4"` and `codecs` attribute). Sort extracted resolutions and bandwidths in ASCENDING order (lowest bitrate first for upgrade scenario). Verify minimum 1 resolution tier available, maximum up to 7 tiers supported | Verify MPD file successfully parsed, multiple resolution tiers extracted (bandwidth and height values), sorted in ascending order for upgrade (lowest first), at least 3 resolution tiers available |
| 3 | Create Playbin Element and Configure DASH Stream | Create playbin element and configure DASH manifest URL as stream source. Set playback flags to enable video and audio. Set westerossink as video rendering sink | Verify playbin element created successfully, URI configured to DASH manifest, playback flags set for A/V, video-sink set to westerossink |
| 4 | Transition Pipeline to Playing State (Initial Lowest Bitrate) | Set pipeline to PLAYING state to begin DASH stream playback at initial lowest bitrate tier (bandwidth constraint set to lowest tier value from MPD to force initial selection of lowest resolution). Play stream for initial 5 seconds at lowest bitrate to establish stable playback and allow video decoder initialization | Verify pipeline transitions to PLAYING state, playback begins without errors, initial video frames rendered at lowest bitrate/resolution |
| 5 | Query Initial Video Resolution Before Bitrate Upgrades | Query westerossink `video-height` property to capture initial resolution (should be lowest resolution from MPD). Query current playback position to record starting position | Verify initial video height obtained successfully, represents lowest resolution from MPD, initial position recorded |
| 6 | Iterate Through Each Bitrate Tier (Upgrade Scenario) Loop | For each resolution tier starting from SECOND lowest (skip first iteration already played): Extract bandwidth value from sorted resolution list (progressively higher values in each iteration). Set bandwidth constraint on dashdemux element to allow resolution upgrade to higher tier. Query current playback position and perform seek operation with FLUSH flag to clear buffers and trigger bitrate adaptation. Wait 100ms for dashdemux adaptation | Verify max-bitrate constraint set successfully on dashdemux for each iteration, seek operation completes, pipeline flushes buffers |
| 7 | Validate Resolution Upgrade After Each Bitrate Switch | Query westerossink `video-height` property to obtain new resolution after adaptation. Compare new height with previous value: if increased, confirm upgrade successful. Query playback position to verify position advances (playback continues despite bitrate switch). Query westerossink stats to verify video frames rendering properly at new resolution | Verify video height increased from previous iteration (resolution upgraded), playback position advanced, frame rendering statistics show frames being rendered without excessive drops |
| 8 | Monitor Playback During Bitrate Upgrade Iteration | Continuously poll playback position at 100ms intervals during current bitrate level playback. Record timestamps to verify position advances at expected rate (1 second playback per 1 second real-time ±250ms tolerance). Monitor for audio/video synchronization errors and pipeline error messages. Continue without stalls or backward position jumps | Verify playback position advances continuously at current bitrate level within timing tolerance, no stalls or backward jumps, A/V sync maintained, no pipeline errors |
| 9 | Repeat Bitrate Upgrade Loop Until Maximum Bitrate Reached | Repeat steps 6-8 for each remaining resolution tier until all bitrate iterations complete (maximum 7 tiers or until highest bitrate reached). Final iteration should result in highest available bitrate/resolution with largest `video-height` value | Verify all bitrate iterations completed successfully, final resolution is highest available from MPD, each upgrade successful |
| 10 | Validate Test Success and Release Resources | Query final playback position to confirm playback continued through all bitrate transitions. Verify test framework output shows `Failures: 0` and `Errors: 0`. Confirm westerossink statistics show overall frame rendering success across all bitrate levels (total rendered frames > threshold, dropped frames minimal). Set pipeline to NULL state to stop playback and terminate dashdemux element. Unreference GStreamer objects and free allocated memory | Verify final position advances beyond initial position, test shows no failures/errors, frame statistics confirm successful playback across all bitrate upgrades, pipeline reaches NULL state, all resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 5-7 minutes (dependent on number of bitrate tiers in manifest, typically 3-7 iterations)

**Priority:** High

**Release Version:** M121
