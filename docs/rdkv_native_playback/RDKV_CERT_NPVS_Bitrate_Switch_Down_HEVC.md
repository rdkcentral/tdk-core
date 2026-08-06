## TestCase ID
RDKV_NATIVE_PLAYBACK_273

## TestCase Name
RDKV_CERT_NPVS_Bitrate_Switch_Down_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify adaptive bitrate downgrade capability during DASH stream playback on HEVC (H.265) video. The test starts at the highest available bitrate/resolution and progressively lowers to lower resolutions by reducing bandwidth constraints on dashdemux element. Validate that each bitrate switch (downgrade) seamlessly changes video resolution without pipeline interruption, audio/video synchronization loss, or decoding errors. Specifically test using GStreamer dashdemux `max-bitrate` property and verify resolution adaptation through querying westerossink `video-height` property at each iteration to confirm successful downgrade from highest to lowest bitrate tier.

## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries (mediapipelinetests<br>binary implements GStreamer playbin pipeline with dashdemux DASH demultiplexer and westerossink video sink for adaptive bitrate switching) | Verify TDK_Package is installed, `tdk_mediapipelinetests` binary is executable, all GStreamer DASH demux and video plugin dependencies available |
| 2 | DASH Media Stream with Multiple Bitrate Tiers |  DASH manifest (MPD file))<br>must be accessible<br>via HTTP/HTTPS or local file system (`filesrc`))<br>containing multiple video representations with different bitrate and resolution combinations. Stream URL is configured<br>via MediaValidationVariables.py variable `video_src_url_bitrate_hevc` with external DASH manifest (external stream source). HEVC DASH manifest must contain minimum 3 resolution tiers with distinct bitrate and resolution combinations. MPD file must define `bandwidth` and `height` attributes for each representation  | Verify external DASH manifest file is accessible, parseable, contains multiple HEVC video representations with distinct bitrate and resolution values, MPD XML structure valid |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_bitrate_hevc` must be configured in `MediaValidationVariables.py` with valid DASH manifest URL containing HEVC codec<br>video stream with multiple bitrate/resolution tiers | Verify `video_src_url_bitrate_hevc` variable resolves to valid, accessible DASH manifest location with HEVC multi-bitrate stream |
| 4 | Device Configuration Parameters | Test execution parameters must be retrieved from device configuration file: , `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) for<br>playback duration per bitrate iteration | Verify all device config parameters are accessible and contain valid values |
| 5 | Platform-Specific Environment and GStreamer Configuration |  Platform-specific environment variables must be defined in `/opt/TDK/TDK.env`: `WAYLAND_DISPLAY` (Wayland display server),<br>`XDG_RUNTIME_DIR` (runtime directory for Wayland sockets),<br>`LD_PRELOAD` with vendor audio/video libraries, `GST_PLUGIN_PATH` (GStreamer plugin directory). GStreamer must have: playbin element, dashdemux DASH demultiplexer with `max-bitrate` property support, HEVC video decoder, and westerossink video sink  | Verify `/opt/TDK/TDK.env` exists with all environment variables, Wayland display functional, GStreamer 1.16+ installed with playbin, dashdemux, and westerossink with adaptive bitrate support in GST_PLUGIN_PATH |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Retrieve Configuration |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration (GST_PLUGIN_PATH, LD_PRELOAD, WAYLAND_DISPLAY, XDG_RUNTIME_DIR). Establish Wayland display session<br>via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log`. Retrieve device config: `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT`. Retrieve stream URL from `MediaValidationVariables.video_src_url_bitrate_hevc`  | Verify all environment variables load correctly, Wayland display created successfully, device config parameters retrieved, stream URL resolves to valid DASH manifest |
| 2 | Parse DASH Manifest (MPD) to Extract Bitrate and Resolution Tiers |  Download and parse MPD (MPEG-DASH manifest))<br>file from `video_src_url_bitrate_hevc` URL using CURL (for HTTP/HTTPS))<br>or local file read (for `file://` protocol). Parse XML structure: `<MPD><Period><AdaptationSet contentType="video"><Representation>` to extract `bandwidth` (bits/sec))<br>and `height` (pixels))<br>attributes from each HEVC representation. Filter representations to include only HEVC codec (check `mimeType="video/mp4"` and `codecs` attribute). Sort extracted resolutions and bandwidths in DESCENDING order (highest bitrate first for downgrade scenario). Verify minimum 1 resolution tier available, maximum up to 7 tiers supported  | Verify MPD file successfully parsed, multiple resolution tiers extracted (bandwidth and height values), sorted in descending order for downgrade (highest first), at least 3 resolution tiers available |
| 3 | Create Playbin Element and Configure DASH Stream | Create playbin element and configure DASH manifest URL as stream source<br> Set playback flags to enable video and audio<br> Set westerossink as video rendering sink | Verify playbin element created successfully, URI configured to DASH manifest, playback flags set for A/V, video-sink set to westerossink |
| 4 | Transition Pipeline to Playing State (Initial Highest Bitrate) | Set pipeline to PLAYING state to begin DASH stream playback at initial highest bitrate tier (no bandwidth constraint applied yet, so dashdemux selects highest available)<br> Play stream for initial 5 seconds at highest bitrate to establish stable playback and allow video decoder initialization | Verify pipeline transitions to PLAYING state, playback begins without errors, initial video frames rendered at highest bitrate/resolution |
| 5 | Query Initial Video Resolution Before Bitrate Downgrades | Query westerossink `video-height` property to capture initial resolution (should be highest resolution from MPD)<br> Query current playback position to record starting position | Verify initial video height obtained successfully, represents highest resolution from MPD, initial position recorded |
| 6 | Iterate Through Each Bitrate Tier (Downgrade Scenario) Loop | For each resolution tier starting from SECOND highest (skip first iteration already played): Extract bandwidth value from sorted resolution list (progressively lower values in each iteration)<br> Set bandwidth constraint on dashdemux element to force resolution downgrade<br> Query current playback position and perform seek operation with FLUSH flag to clear buffers and trigger bitrate adaptation<br> Wait 100ms for dashdemux adaptation | Verify max-bitrate constraint set successfully on dashdemux for each iteration, seek operation completes, pipeline flushes buffers |
| 7 | Validate Resolution Downgrade After Each Bitrate Switch | Query westerossink `video-height` property to obtain new resolution after adaptation<br> Compare new height with previous value: if decreased, confirm downgrade successful<br> Query playback position to verify position advances (playback continues despite bitrate switch)<br> Query westerossink stats to verify video frames rendering properly at new resolution | Verify video height decreased from previous iteration (resolution downgraded), playback position advanced, frame rendering statistics show frames being rendered without excessive drops |
| 8 | Monitor Playback During Bitrate Downgrade Iteration | Continuously poll playback position at 100ms intervals during current bitrate level playback<br> Record timestamps to verify position advances at expected rate (1 second playback per 1 second real-time +/-250ms tolerance)<br> Monitor for audio/video synchronization errors and pipeline error messages<br> Continue without stalls or backward position jumps | Verify playback position advances continuously at current bitrate level within timing tolerance, no stalls or backward jumps, A/V sync maintained, no pipeline errors |
| 9 | Repeat Bitrate Downgrade Loop Until Minimum Bitrate Reached | Repeat steps 6-8 for each remaining resolution tier until all bitrate iterations complete (maximum 7 tiers or until lowest bitrate reached)<br> Final iteration should result in lowest available bitrate/resolution with smallest `video-height` value | Verify all bitrate iterations completed successfully, final resolution is lowest available from MPD, each downgrade successful |
| 10 | Validate Test Success and Release Resources | Query final playback position to confirm playback continued through all bitrate transitions<br> Verify test framework output shows `Failures: 0` and `Errors: 0`<br> Confirm westerossink statistics show overall frame rendering success across all bitrate levels (total rendered frames > threshold, dropped frames minimal)<br> Set pipeline to NULL state to stop playback and terminate dashdemux element<br> Unreference GStreamer objects and free allocated memory | Verify final position advances beyond initial position, test shows no failures/errors, frame statistics confirm successful playback across all bitrate downgrades, pipeline reaches NULL state, all resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 7 mins

**Priority:** High

**Release Version:** M121







