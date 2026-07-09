## TestCase ID
NATIVE_PLAYBACK_134

## TestCase Name
NPVS_Audio_Low_Volume_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate AAC audio stream playback at low volume. The test sets volume to 50% amplitude and verifies that audio quality is maintained during volume-constrained playback. Confirm volume control propagates correctly through the pipeline and playback continues smoothly with position advancing at the expected rate.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | AAC stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) at configured DASH manifest URL (test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd") | Verify DASH manifest accessible, AAC audio track parseable, and stream playable without timeout |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_aac` must be configured in `MediaValidationVariables.py` pointing to valid AAC DASH manifest with functioning HTTPS endpoint | Verify `video_src_url_aac` resolves to DASH_H264_AAC manifest accessible from DUT |
| 4 | Volume Control API Availability | GStreamer `GstStreamVolume` interface must be supported by playbin element on target platform; audio-sink element must expose "volume" property for verification | Verify playbin supports GstStreamVolume, audio-sink property accessible via  |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables, Wayland compositor active |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, audio library paths, and Wayland configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Initialize logging to `/opt/TDK/mediapipeline_test_step.log` | Verify environment variables load without errors, GStreamer plugin path includes audio elements, Wayland display active, logging ready |
| 2 | Configure Test Parameters and Load Media | Retrieve device configuration: `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default 10 seconds) flag. Build `mediapipelinetests` command with: test_name="test_audio_volume", stream_url=video_src_url_aac (DASH manifest), arguments:, timeout=N, volume_set=0.5 | Verify device config parameters retrieved successfully, command constructed with volume_set=0.5 parameter |
| 3 | Construct Pipeline and Configure Audio Path | Create `playbin` element via . Set `uri` property to AAC DASH manifest URL via . Trigger state transitions: `NULL→READY→PAUSED→PLAYING` via . Register bus message handler to detect errors and first-audio-frame signal | Verify playbin created, URI set to valid DASH manifest, state machine transitions execute, no GST_MESSAGE_ERROR detected |
| 4 | Verify Initial Playback State | Monitor GStreamer bus for  confirming PLAYING state achieved and `first-audio-frame-callback` signal indicating audio rendering started.  Validate return value in valid range [0.0, 1.0] representing linear cubic amplitude. Log result format: "Previous volume: %.0f%%" (multiply by 100 for percentage display) | Verify function returns without error, value in valid range [0.0, 1.0], typically near 1.0 (100%) for unmodified stream |
| 6 | Set Volume to Target Low Level (50% = 0.5 Cubic) | Call  to set audio volume to exactly 50% cubic amplitude. Log operation: "Setting volume to 0.500000". Monitor GStreamer bus for any GST_MESSAGE_WARNING or GST_MESSAGE_ERROR during volume change | Verify function executes without error return code, no warning/error messages on bus, volume state changed internally |
| 7 | Query Volume After Setting and Verify Propagation | Call  immediately after set operation to confirm volume change. Compare return value with set value (0.5) using exact equality `get_volume == set_volume`. Log result: "Volume: %.0f%%" (0.5 * 100 = 50%). Assert failure if values don't match exactly (tolerance 0.0) | Verify get returns exactly 0.5, no rounding or conversion errors, assertion passes confirming internal volume state updated |
| 8 | Retrieve and Validate Audio-Sink Volume Property | Execute  to retrieve audio-sink element reference. Check if audio-sink has "volume" property via . Query property via  | Verify audio-sink element retrieved non-null, "volume" property exists and is queryable, property value returned successfully |
| 9 | Verify Audio-Sink Volume Matches Set Value | Compare audio-sink reported volume (`sink_volume` from property query) with intended set value (0.5) using equality assertion. Expected: sink_volume == 0.5. Log comparison: "Volume from audiosink = %.0f" vs "Expected volume = %.0f". Assert failure if mismatch indicating volume setting didn't propagate to audio output layer | Verify audio-sink reports exactly 0.5 (50%), assertion passes confirming volume setting reached output layer, audio will play at specified amplitude |
| 10 | Monitor Continuous Playback During Low Volume Playback | Play AAC stream at low volume for minimum 10 seconds.  Verify position advances continuously at rate: 1 second elapsed per 1 second playback ±250ms tolerance. Detect any position stalls, backward jumps, or discontinuities indicating glitching during volume-constrained playback. Monitor bus for buffer underflow or error conditions | Verify position increments smoothly without stalls, playback rate matches real-time (±250ms tolerance), audio plays clearly without artifacts, no errors/underflow logged |
| 11 | Release Pipeline and Validate Test Completion | Set pipeline to  via . Call  and  to release all references. Verify test framework logs indicate completion: parse `/opt/TDK/mediapipeline_test_step.log` and confirm test execution summary shows `Failures: 0`, `Errors: 0` | Verify pipeline transitions to NULL state, all GStreamer objects unreferenced, test logs show zero failures/errors, test marked as PASSED |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
