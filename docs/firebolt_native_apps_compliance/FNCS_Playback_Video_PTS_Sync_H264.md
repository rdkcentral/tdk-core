# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_343**

## TestCase Name
**FNCS_Playback_Video_PTS_Sync_H264**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To verify that H264 video stream playback maintains synchronized Presentation Time Stamp (PTS) values using the westeros-sink element's 'last-sample' property, ensuring video timing accuracy throughout playback.

**VIDEO CODEC:** H264

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | H264 short duration MP4 stream (TDK_Asset_H264_Short_Duration_Stream.mp4) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for video playback and PTS monitoring. Default value is 30 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Video PTS Sync Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve H264 short duration MP4 stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_video_PTS_sync operation specifying PTS synchronization validation. Execute command: `tdk_mediapipelinetests_video_PTS_sync https://<server_hosting_stream>:<port_number>/TDK_Asset_H264_Short_Duration_Stream.mp4 checkavstatus=<yes/no>` with configured timeout | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with PTS sync operation. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins H264 short duration MP4 stream playback using GStreamer playbin element with westeros-sink for rendering | H264 MP4 stream playback must begin successfully without pipeline errors |
| 4 | Monitor Video PTS Synchronization | Continuously monitor the 'last-sample' property of the westeros-sink element throughout video playback. Extract PTS (Presentation Time Stamp) values from the video sample buffer at regular intervals (millisecond resolution). Verify that PTS values progress smoothly and continuously without gaps or discontinuities | PTS values must progress continuously and smoothly. No timing gaps or discontinuities must be detected. PTS progression must align with actual playback rate |
| 5 | Validate PTS Alignment with Playback | Compare extracted PTS values with the actual playback position and elapsed time. Verify that the difference between consecutive PTS samples is consistent and matches the expected frame duration for the codec. Ensure PTS values do not regress or show timing anomalies | PTS timing must be accurate and consistent. Frame duration calculations from PTS must match codec specifications. No timing regressions or anomalies permitted |
| 6 | Monitor Playback Quality During PTS Validation | Monitor video frame rendering using westerossink "stats" property during PTS validation. Verify that video frame drop rate does not exceed 1%. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active | Video frames must render with drop rate below 1%. If AV status check is enabled, video decoder must show continuous activity |
| 7 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that PTS synchronization validation completed successfully and no timing anomalies were detected | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". PTS synchronization validation must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator, RDKTV, RPI-Client

**Estimated Duration:** 1-2 minutes

**Priority:** High

**Release Version:** M135
