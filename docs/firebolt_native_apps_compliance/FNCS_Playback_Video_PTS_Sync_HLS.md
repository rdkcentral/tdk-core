# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_347**

## TestCase Name
**FNCS_Playback_Video_PTS_Sync_HLS**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To verify that HLS adaptive stream playback maintains synchronized Presentation Time Stamp (PTS) values using the westeros-sink element's 'last-sample' property, ensuring video timing accuracy throughout adaptive bitrate playback.

**VIDEO CODEC:** H264

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | HLS short duration stream (TDK_Asset_HLS_Short_Duration_Stream.m3u8) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for video playback and PTS monitoring. Default value is 15 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Video PTS Sync Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve HLS short duration stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_video_PTS_sync operation specifying PTS synchronization validation for adaptive streaming. Execute command: `tdk_mediapipelinetests_video_PTS_sync https://<server_hosting_stream>:<port_number>/TDK_Asset_HLS_Short_Duration_Stream.m3u8 checkavstatus=<yes/no>` with configured timeout | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with PTS sync operation. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins HLS stream playback using GStreamer playbin element with westeros-sink for rendering. Confirm that adaptive bitrate stream is detected and playback begins at appropriate bitrate | HLS stream playback must begin successfully without pipeline errors. Adaptive stream detection must be successful |
| 4 | Monitor Video PTS Synchronization During Adaptive Streaming | Continuously monitor the 'last-sample' property of the westeros-sink element throughout video playback. Extract PTS (Presentation Time Stamp) values from the video sample buffer at regular intervals (millisecond resolution). Verify that PTS values progress smoothly and continuously during bitrate transitions | PTS values must progress continuously and smoothly. Timing must remain synchronized during adaptive bitrate changes. No timing gaps during bitrate transitions permitted |
| 5 | Validate PTS Accuracy During Bitrate Transitions | Verify that PTS values maintain accuracy and consistency even when adaptive bitrate transitions occur. Compare extracted PTS values with expected timing and verify frame duration calculations remain valid. Ensure PTS progression is logical through bitrate adaptation without discontinuities | PTS must remain accurate during bitrate transitions. Frame duration calculations must remain valid. Timing must be continuous through adaptation events |
| 6 | Monitor Playback Quality During Adaptive Streaming | Monitor video frame rendering using westerossink "stats" property during PTS validation. Verify that video frame drop rate does not exceed 1% even during bitrate transitions. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active | Video frames must render with drop rate below 1%. Bitrate adaptation must not cause excessive frame drops. If AV status check is enabled, video decoder must remain operational |
| 7 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that PTS synchronization validation completed successfully through all bitrate transitions and no timing anomalies were detected | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". PTS synchronization validation must be confirmed as successful through adaptive streaming |

## Test Attributes

**Supported Models:** Video_Accelerator, RDKTV, RPI-Client

**Estimated Duration:** 1-2 minutes

**Priority:** High

**Release Version:** M135
