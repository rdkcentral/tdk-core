# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_345**

## TestCase Name
**FNCS_Playback_Video_PTS_Sync_AV1**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To verify that AV1 video stream playback maintains synchronized Presentation Time Stamp (PTS) values using the westeros-sink element's 'last-sample' property during frame-drop scenarios, ensuring video timing accuracy throughout playback under stress conditions.

**VIDEO CODEC:** AV1

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | AV1 frame-drop MP4 stream (TDK_Asset_AV1_FrameDrop_MP4_Stream.mp4) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for video playback and PTS monitoring. Default value is 30 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Video PTS Sync Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve AV1 frame-drop MP4 stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_video_PTS_sync operation specifying PTS synchronization validation under frame-drop stress conditions. Execute command: `tdk_mediapipelinetests_video_PTS_sync https://<server_hosting_stream>:<port_number>/TDK_Asset_AV1_FrameDrop_MP4_Stream.mp4 checkavstatus=<yes/no>` with configured timeout | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with PTS sync operation. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins AV1 frame-drop MP4 stream playback using GStreamer playbin element with westeros-sink for rendering. Confirm that frame drops will be introduced during playback for stress testing | AV1 MP4 stream playback must begin successfully without pipeline errors. Frame drop conditions must be active |
| 4 | Monitor Video PTS Synchronization During Frame Drops | Continuously monitor the 'last-sample' property of the westeros-sink element throughout video playback including frame-drop scenarios. Extract PTS (Presentation Time Stamp) values from the video sample buffer at regular intervals (millisecond resolution) during both normal and dropped frame periods | PTS values must continue to progress during frame drops. Timing must remain synchronized despite frame loss. No unintended timing regressions permitted |
| 5 | Validate PTS Accuracy Under Stress | Verify that PTS values maintain accuracy and consistency even when video frames are dropped. Compare extracted PTS values with expected timing and verify frame duration calculations remain valid. Ensure PTS compensates appropriately for skipped frames without introducing discontinuities | PTS must remain accurate despite frame drops. Frame duration from PTS must maintain codec specification alignment. PTS progression must be logical and continuous |
| 6 | Monitor Playback Quality During Frame Drops | Monitor video frame rendering using westerossink "stats" property during PTS validation with frame drops. Track frame drop rate and verify it aligns with stress test conditions. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active | Video frame drops must be within acceptable range for stress test. Statistics must be accurate. If AV status check is enabled, video decoder must remain operational |
| 7 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that PTS synchronization validation completed successfully despite frame-drop stress conditions and no unrecoverable timing anomalies were detected | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". PTS synchronization validation must be confirmed as successful under frame-drop stress |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 1-2 minutes

**Priority:** High

**Release Version:** M135
