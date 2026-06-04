# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_374**

## TestCase Name
**FNCS_Playback_PlayPause_VP9_HDR**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that DASH adaptive streaming with VP9 video codec in HDR format supports stable play and pause operations through the GStreamer media pipeline, ensuring correct state transitions and robust pipeline management with HDR content rendering.

**VIDEO CODEC:** VP9

**AUDIO CODEC:** Opus

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | VP9 HDR DASH stream (TDK_Asset_VP9_HDR_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the timeout in seconds for video playback verification. Default value is "10" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Play-Pause Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve VP9 HDR DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_play_pause_pipeline operation. Execute command: `tdk_mediapipelinetests_pipeline https://<server_hosting_stream>:<port_number>/TDK_Asset_VP9_HDR_DASH_Stream.mpd checkavstatus=<yes/no> timeout=<seconds>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Create GStreamer Pipeline with Playbin | Initialize GStreamer pipeline infrastructure and create playbin element for unified media handling. Configure playbin to auto-detect and initialize VP9 video decoder and Opus audio decoder for HDR stream processing. Set westerossink as video rendering sink for HDR content and native audio-sink for audio output | GStreamer pipeline must be created successfully. Playbin element must initialize with proper plugins for VP9 and Opus decoding. Video and audio sink elements must be configured without errors |
| 4 | Set Pipeline to PLAYING State | Transition the GStreamer pipeline from NULL state to READY state, then to PAUSED state, and finally to PLAYING state. During READY to PAUSED transition, establish connection to DASH stream and begin decoder initialization. Verify that VP9 video decoder and Opus audio decoder initialize and begin rendering HDR video frames and audio | Pipeline state transitions must succeed at each stage. DASH stream connection must establish successfully. Video decoder must begin rendering HDR frames and audio decoder must output audio samples |
| 5 | Monitor Playback in PLAYING State | Verify that video frames render continuously using westerossink "stats" property to monitor frame rendering rate. Monitor audio output quality using native audio-sink "stats" property. Verify that HDR metadata is properly processed for correct color mapping and rendering. Maintain PLAYING state for configured timeout duration | Video and audio frames must render continuously and smoothly. HDR color information must be correctly applied to rendered frames. Frame drop rate must remain below 1% during playback |
| 6 | Transition Pipeline to PAUSED State | Issue explicit command to transition playbin from PLAYING to PAUSED state. Verify that video frame rendering and audio output stop cleanly while maintaining decoder state and current playback position. Confirm that pipeline remains in valid PAUSED state without errors or deadlocks | Pipeline must transition to PAUSED state successfully. Video and audio rendering must stop immediately. Current playback position must be maintained without loss |
| 7 | Resume Playback from Paused State | Transition playbin from PAUSED state back to PLAYING state. Verify that video rendering resumes from the paused position with HDR frames rendered correctly. Confirm that audio output resumes with synchronized timing relative to video playback. Maintain playback for configured timeout duration | Pipeline must transition from PAUSED to PLAYING state successfully. Video frames must resume rendering with correct HDR processing. Audio must resume in synchronization with video position. Frame drop rate must remain below 1% |
| 8 | Transition Pipeline to PAUSED State Again | Perform second pause operation to ensure consistent pause behavior and state management. Verify that the pipeline handles multiple pause operations correctly without degradation or resource issues | Second pause operation must succeed cleanly. Pipeline must remain stable and responsive after multiple state transitions |
| 9 | Monitor Overall Pipeline Quality and Validation | Throughout all state transitions, monitor westerossink "stats" property for video frame drop rates and rendering consistency. Monitor audio quality through native audio-sink "stats". If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder activity during all state transitions. Verify that HDR processing remains consistent throughout pipeline operations | Video frame drop rate must remain below 1% across all states. Audio frame drop rate must remain below 1%. All state transitions must complete without errors or pipeline hangs. If AV status is enabled, video decoder must show continuous activity |
| 10 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that all play-pause pipeline operations completed successfully and pipeline was properly cleaned up | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". All play-pause pipeline operations must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M136
