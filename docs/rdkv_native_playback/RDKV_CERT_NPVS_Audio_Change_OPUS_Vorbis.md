## TestCase ID
RDKV_NATIVE_PLAYBACK_122

## TestCase Name
RDKV_CERT_NPVS_Audio_Change_OPUS_Vorbis

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify if dynamic audio codec switching (OPUS to Vorbis) is possible while maintaining video playback continuity. Validate that audio track can be switched between different codec types (OPUS and Vorbis) present in the same multi-codec stream without interrupting video playback. Specifically validate audio rendering quality, position synchronization, and codec switching timing accuracy during active playback. Verify codec identity is confirmed through tag comparison.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  Multi-codec stream containing both OPUS and Vorbis audio tracks must be accessible via HTTPS (`souphttpsrc`))<br>or local file system (`filesrc`))<br>with DASH manifest. Stream configured as `test_streams_base_path + "MultiCodecStreams/stream_with_opus_vorbis.mpd"` in MediaValidationVariables.py Stream variable `video_src_url_opus_vorbis` configured in `MediaValidationVariables.py` with DASH manifest containing OPUS and Vorbis audio tracks  | Verify multi-codec DASH stream accessible, both OPUS and Vorbis audio tracks present and parseable Verify `video_src_url_opus_vorbis` resolves to valid multi-codec stream with dual audio tracks |
| 3 | Device Configuration Parameters | Configuration parameters `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default 10 seconds per codec) must be retrievable from device configuration | Verify device config returns valid timeout  |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables, Wayland display active |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland configuration. Establish Wayland display session<br>via RDKWindowManager. Initialize logging to `/opt/TDK/mediapipeline_test_step.log`  | Verify environment variables load without errors, Wayland display active, logging initialized |
| 2 | Configure Test Parameters and Load Multi-Codec Stream | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device<br> Build `mediapipelinetests` command with test_name="test_playback_audio_change", stream_url=video_src_url_opus_vorbis, timeout=N | Verify device config retrieved successfully, command constructed with correct parameters |
| 3 | Create Playbin Pipeline and Load Multi-Codec Stream |  Create `playbin` element<br>via `gst_element_factory_make()`. Set `uri` property to multi-codec DASH stream URL<br>via `g_object_set(playbin, "uri", stream_url, NULL)`. Trigger state transitions to `GST_STATE_PLAYING`<br>via `gst_element_set_state()`  | Verify playbin created, URI configured to multi-codec DASH stream, pipeline transitions to PLAYING |
| 4 | Retrieve and Verify Multiple Audio Tracks |  Query playbin to determine number of audio streams<br>via `g_object_get(playbin, "n-audio", &n_audio, NULL)`. Verify n-audio >= 2 (confirming OPUS and Vorbis tracks present). Query current audio index<br>via `g_object_get(playbin, "current-audio", &current_audio, NULL)` to identify default (OPUS))<br>track  | Verify n-audio returns at least 2, current-audio successfully retrieved (typically 0 for first codec) |
| 5 | Verify Initial OPUS Audio Playback and Retrieve Audio-Tags | Emit "get-audio-tags" signal for default audio track via `g_signal_emit_by_name(playbin, "get-audio-tags", 0, &tags)`<br> Parse tag list using `gst_tag_list_foreach()` to identify codec name (OPUS)<br> Log audio-tags including codec type, sample rate, channels as baseline<br> Poll playback position for 5-10 seconds to verify OPUS audio plays without interruption | Verify audio-tags successfully retrieved showing OPUS codec (e.g., audio/x-opus), playback position advances linearly, no audio glitches or stalls |
| 6 | Switch to Vorbis Codec using current-audio and Flush Pipeline |  Set `current-audio` property<br>via `g_object_set(playbin, "current-audio", 1, NULL)` to switch to Vorbis track (index 1). Verify switch succeeded<br>via `g_object_get(playbin, "current-audio", &current_audio, NULL)` confirming value equals 1. Query current position<br>via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)`. Flush pipeline<br>via `gst_element_seek(playbin, NORMAL_PLAYBACK_RATE, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, currentPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` to clear buffered OPUS data. Wait 2 seconds for buffer refill with Vorbis. Reset audio underflow flag  | Verify current-audio property set to 1, position query succeeds, seek-flush executes successfully, 2-second wait completes, underflow flag reset |
| 7 | Verify Second Vorbis Audio Playback and Retrieve Audio-Tags | After seek-flush completes, playback continues with Vorbis codec now active<br> Emit "get-audio-tags" signal for Vorbis track via `g_signal_emit_by_name(playbin, "get-audio-tags", 1, &tags)`<br> Parse tag list using `gst_tag_list_foreach()` to identify codec name (Vorbis)<br> Log audio-tags including codec type, sample rate, channels<br> Compare logged tags from Step 5 (OPUS) with current tags (Vorbis) to confirm different codec | Verify audio-tags successfully retrieved showing Vorbis codec (e.g., audio/x-vorbis, different from OPUS), codec change confirmed through tag comparison |
| 8 | Monitor Vorbis Playback Progress and Validate Continuity | Poll playback position for 5-10 seconds after codec switch via `gst_element_query_position()` at 100ms intervals<br> Verify position advances linearly from seek-flush point with no backward jumps<br> Monitor bus for `pts-error-callback` signals (should be none)<br> Check for audio underflow conditions (should be none)<br> Verify video playback continues uninterrupted during audio codec switch | Verify Vorbis position advances smoothly, no pts-error or underflow signals, video continues playing, audio output clear and artifact-free |
| 9 | Validate Dual Audio Codec Support and Release Resources |  Review logged audio-tags from both codec playbacks. Verify codec identity confirmed<br>via tags: Step 5 shows OPUS, Step 7 shows Vorbis (distinctly different). Verify test framework output shows `Failures: 0`, `Errors: 0`. Set pipeline to `GST_STATE_NULL`<br>via `gst_element_set_state()`. Call `gst_object_unref(playbin)` to release all resources. Free allocated memory and close logging file  | Verify audio-tags logs confirm both codecs properly identified, test completed successfully with zero failures/errors, pipeline reaches NULL state, all GStreamer resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121





