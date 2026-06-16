# FNCS_Playback_Same_Asset_Twice_DASH Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_13

## TestCase Name
FNCS_Playback_Same_Asset_Twice_DASH

## Objective
Test to verify that the pipeline can initialise and shutdown correctly without doing av playback

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | video_src_url_dash variable must be configured with DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd in MediaValidationVariables.py as URL or file path for the test stream |
| 4 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set to no (default) in Video_Accelerator.config / RPI-Client.config |
| 5 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration should be set to 10 (default) in Video_Accelerator.config / RPI-Client.config |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If present create display using RDKWindowManager otherwise use RDKShell plugin or westeros --renderer command | All environment variables must be set and display created successfully using RDKWindowManager or RDKShell/westeros |
| 2 | Prepare and Execute Test | Retrieve required configuration values and stream URL, construct the mediapipeline command and start the media pipeline test application | Configuration values retrieved successfully, stream URL obtained and test application starts execution without errors |
| 3 | Monitor Playback | Observe playback for configured timeout and monitor video/audio playback health, position progression and frame rendering | Playback proceeds for configured duration without critical errors and frame drop rates are acceptable |
| 4 | Validate Results | Parse test application output for success indicators and validate playback metrics | Output contains success indicators such as "Failures: 0" or "failed: 0" |
| 5 | Cleanup | Stop pipeline, release playback resources and remove any created displays | Pipeline stopped cleanly and resources released |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
