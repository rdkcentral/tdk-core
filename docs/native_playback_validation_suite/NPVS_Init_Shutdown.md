## TestCase ID
NATIVE_PLAYBACK_10

## TestCase Name
NPVS_Init_Shutdown

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate the pipeline lifecycle management including proper initialization and graceful shutdown. The test verifies that all codec, decoder, and sink resources are correctly allocated during pipeline creation and properly released during shutdown without resource leaks.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | DASH Media Stream Provisioning | DASH stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) for playbin URI handling. Stream file: `DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd` configured in `MediaValidationVariables.py` as `video_src_url_dash` = `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify DASH stream is accessible via network and MPD manifest can be parsed by GStreamer demuxer |
| 3 | Stream Variable Configuration | Stream URL must be configured in `MediaValidationVariables.py` with variable `video_src_url_dash` = `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify stream URL resolves to valid, accessible DASH manifest location |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in device configuration file for initialization and cleanup validation | Verify timeout is set appropriately to allow complete pipeline initialization and shutdown |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required environment variables and Wayland display is active for rendering setup |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, GStreamer plugin paths are configured, Wayland display configuration is available |
| 2 | Create Playbin Element | Create `playbin` element via  to instantiate the GStreamer multimedia playback engine | Verify `playbin` element created successfully without errors, element is in NULL state by default |
| 3 | Configure Playbin with DASH Stream URI | Set playbin `uri` property via  to configure the media source from MediaValidationVariables.py | Verify URI property is set correctly, DASH manifest is recognized by playbin |
| 4 | Configure Playbin Flags for Audio/Video | Retrieve current flags via . Set flags to  via  to enable multimedia playback capabilities | Verify both video and audio playback flags are enabled in playbin element |
| 5 | Create and Configure Westeros Video Sink | Create `westerossink` element via . Link to playbin via  to establish video rendering pipeline | Verify `westerossink` element created successfully and properly linked to playbin video output |
| 6 | Perform Pipeline State Initialization | Transition pipeline through initialization sequence: `NULL→READY→PAUSED→PLAYING` via repeated  calls. Monitor state transitions to verify asynchronous state changes complete properly | Verify pipeline reaches initialized state without , all state transitions execute successfully |
| 7 | Validate Pipeline Ready State | Query pipeline state via  to verify current operational state. Verify pipeline state machine transitions occur correctly without deadlocks or unexpected states | Verify `cur_state` reflects expected pipeline state, no blocking or timeout during state query |
| 8 | Release All Pipeline Resources | Set pipeline state to  via  to uninitialize all elements. Unreference playbin element via  to deallocate memory and release codec, decoder, and sink resources | Verify pipeline reaches , all GStreamer resources are deallocated, system returns to pre-test state with no resource leaks |
| 9 | Validate Test Success Indicators | Parse test execution output and verify GCheck framework reports test execution completed successfully with expected result metrics | Verify test output contains completion status and no assertion failures detected |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
