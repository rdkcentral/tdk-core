# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_348**

## TestCase Name
**FNCS_Playback_Video_PTS_Sync_HEVC_MKV**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To verify that HEVC video stream in MKV container format maintains synchronized Presentation Time Stamp (PTS) values using the westeros-sink element's 'last-sample' property, ensuring video timing accuracy throughout playback of extended duration content.

**VIDEO CODEC:** HEVC

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | HEVC 30-second duration MKV stream (TDK_Asset_HEVC_30Sec_Stream.mkv) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for video playback and PTS monitoring. Default value is 30 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Video PTS Sync Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve HEVC 30-second duration MKV stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_video_PTS_sync operation specifying PTS synchronization validation for extended duration content. Execute command: `tdk_mediapipelinetests_video_PTS_sync https://<server_hosting_stream>:<port_number>/TDK_Asset_HEVC_30Sec_Stream.mkv checkavstatus=<yes/no>` with configured timeout | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with PTS sync operation. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins HEVC MKV stream playback using GStreamer playbin element with westeros-sink for rendering. Confirm that extended duration stream is properly recognized and playback begins successfully | HEVC MKV stream playback must begin successfully without pipeline errors. 30-second duration stream must be properly detected |
| 4 | Monitor Video PTS Synchronization Over Extended Duration | Continuously monitor the 'last-sample' property of the westeros-sink element throughout the entire 30-second video playback. Extract PTS (Presentation Time Stamp) values from the video sample buffer at regular intervals (millisecond resolution) across the entire playback duration | PTS values must progress continuously and smoothly over 30 seconds. Timing must remain synchronized throughout extended playback. No timing gaps or discontinuities permitted |
| 5 | Validate PTS Consistency Throughout Playback | Verify that PTS values maintain accuracy and consistency across the entire 30-second stream. Compare extracted PTS values with expected timing and verify frame duration calculations remain valid and consistent. Ensure no timing drift or degradation occurs over the extended playback period | PTS must remain accurate throughout full 30-second duration. Frame duration calculations must remain consistent. No timing drift or progressive deviation permitted |
| 6 | Monitor Playback Quality Over Extended Duration | Monitor video frame rendering using westerossink "stats" property during the entire PTS validation period. Verify that video frame drop rate does not exceed 1% throughout the 30-second playback. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active | Video frames must render with drop rate below 1% over entire duration. Decoder must remain operational throughout. Quality metrics must remain consistent |
| 7 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that PTS synchronization validation completed successfully over the entire 30-second stream and no timing anomalies were detected | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". PTS synchronization validation must be confirmed as successful over entire extended duration |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 1-2 minutes

**Priority:** High

**Release Version:** M135
