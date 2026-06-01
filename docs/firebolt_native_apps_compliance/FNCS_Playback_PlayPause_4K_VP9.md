# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_291**

## TestCase Name
**FNCS_Playback_PlayPause_4K_VP9**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that WebM container format with VP9 video codec at 4K resolution supports stable play and pause operations through the GStreamer media pipeline, ensuring correct state transitions and robust pipeline management with high-resolution content rendering.

**VIDEO CODEC:** VP9

**AUDIO CODEC:** Opus

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | 4K VP9 WebM stream (TDK_Asset_4K_VP9_WebM_Stream.webm) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the timeout in seconds for video playback verification. Default value is "10" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Play-Pause Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve 4K VP9 WebM stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_play_pause_pipeline operation. Execute command: `tdk_mediapipelinetests_pipeline https://<server_hosting_stream>:<port_number>/TDK_Asset_4K_VP9_WebM_Stream.webm checkavstatus=<yes/no> timeout=<seconds>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Create GStreamer Pipeline with Playbin | Initialize GStreamer pipeline infrastructure and create playbin element for unified media handling. Configure playbin to auto-detect and initialize VP9 video decoder for 4K content handling and Opus audio decoder for WebM stream processing. Set westerossink as video rendering sink for 4K resolution output and native audio-sink for audio output | GStreamer pipeline must be created successfully. Playbin element must initialize with proper plugins for VP9 4K decoding and Opus audio decoding. Video and audio sink elements must be configured for 4K output without errors |
| 4 | Set Pipeline to PLAYING State | Transition the GStreamer pipeline from NULL state to READY state, then to PAUSED state, and finally to PLAYING state. During READY to PAUSED transition, establish connection to WebM stream and begin decoder initialization for 4K content. Verify that VP9 video decoder initializes for 4K resolution and Opus audio decoder begins rendering content | Pipeline state transitions must succeed at each stage. WebM stream connection must establish successfully. VP9 decoder must initialize for 4K frame sizes. Audio decoder must output audio samples |
| 5 | Monitor Playback in PLAYING State at 4K Resolution | Verify that 4K video frames render continuously using westerossink "stats" property to monitor frame rendering rate at high resolution. Monitor audio output quality using native audio-sink "stats" property. Verify that 4K video resolution is properly decoded and rendered without scaling artifacts. Maintain PLAYING state for configured timeout duration | 4K video frames must render continuously and smoothly at full resolution. Audio frames must render with quality. Frame drop rate must remain below 1% during high-resolution playback. Westerossink output must display 4K frames without artifacts |
| 6 | Transition Pipeline to PAUSED State | Issue explicit command to transition playbin from PLAYING to PAUSED state. Verify that video frame rendering and audio output stop cleanly while maintaining decoder state and current playback position. Confirm that 4K video decoding pauses without resource issues or buffer underflow | Pipeline must transition to PAUSED state successfully. 4K video and audio rendering must stop immediately. Current playback position must be maintained. Decoder resources must remain stable |
| 7 | Resume Playback from Paused State | Transition playbin from PAUSED state back to PLAYING state. Verify that 4K video rendering resumes from the paused position with correct frame sizes. Confirm that audio output resumes with synchronized timing relative to video playback. Maintain playback for configured timeout duration | Pipeline must transition from PAUSED to PLAYING state successfully. 4K video frames must resume rendering at full resolution. Audio must resume in synchronization with video position. Frame drop rate must remain below 1% |
| 8 | Transition Pipeline to PAUSED State Again | Perform second pause operation to ensure consistent pause behavior and state management under 4K playback conditions. Verify that the pipeline handles multiple pause operations correctly without degradation of 4K rendering quality | Second pause operation must succeed cleanly. Pipeline must remain stable and responsive to multiple state transitions. 4K playback resources must be properly managed |
| 9 | Monitor Overall Pipeline Quality and Validation at 4K | Throughout all state transitions, monitor westerossink "stats" property for video frame drop rates and rendering consistency at 4K resolution. Monitor audio quality through native audio-sink "stats". If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder activity during all state transitions at 4K loads | 4K video frame drop rate must remain below 1% across all states. Audio frame drop rate must remain below 1%. All state transitions must complete without errors or pipeline hangs. If AV status is enabled, video decoder must show continuous activity under 4K load |
| 10 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that all 4K play-pause pipeline operations completed successfully and pipeline was properly cleaned up | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". All play-pause pipeline operations at 4K must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M130
