# FNCS_Playback_FastForward_3x_VP9

## TestCase ID
FNCS_PLAYBACK_308

## TestCase Name
FNCS_Playback_FastForward_3x_VP9

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate the fast forward functionality of VP9 video streams at 3x playback rate, ensuring proper video frame progression and timing accuracy during trick play operations.

**VIDEO CODEC:** VP9

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | TDK_FNCS_Package should be installed in DUT |
| 2 | video_src_url_4k_vp9 must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://&lt;server_hosting_stream&gt;:&lt;port_number&gt;/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set as yes/no in Video_Accelerator.config file to control AV status checking during playback validation |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration should be set to time in seconds to wait before checking for AV playback in Video_Accelerator.config file |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Retrieve Configuration and Execute FastForward Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from device config, get video_src_url_4k_vp9 stream URL from MediaValidationVariables, construct trickplay command with 3x fast forward parameters, and execute command: `tdk_mediapipelinetests_trickplay https://&lt;server_hosting_stream&gt;:&lt;port_number&gt;/[VP9_STREAM_NAME] checkavstatus=no operations=fastforward3x:10` | Configuration values must be retrieved successfully, stream URL must be obtained correctly, command must be constructed properly with 3x fast forward parameters, and test application starts execution without errors |
| 3 | Initialize GStreamer Pipeline | Create GStreamer pipeline using playbin element and configure it for VP9 stream playback with httpsrc source element for network streaming | GStreamer pipeline must be created successfully with playbin configured for VP9 stream processing and httpsrc elements initialized properly |
| 4 | Configure Pipeline Elements | Set up pipeline elements including video sink (westerossink), audio sink, and configure pipeline properties for VP9 decoding with fast forward capabilities | All pipeline elements must be configured successfully with proper VP9 decoder selection and sink elements ready for fast forward operations |
| 5 | Start Pipeline and Begin FastForward | Set pipeline to PLAYING state and initiate fast forward operation at 3x playback rate immediately after playback starts | Pipeline must transition to PLAYING state successfully and fast forward operation must engage at 3x rate with proper video acceleration |
| 6 | Monitor FastForward Playback | Monitor playback position progression to verify 3x fast forward rate is maintained consistently throughout the test duration | Position must advance at 3x normal playback rate indicating successful fast forward operation with consistent speed |
| 7 | Validate Fast Forward Performance | Use pipeline bus messages to monitor for any errors, warnings, or state change notifications during fast forward operation | No error messages should be received and pipeline must maintain stable fast forward state at 3x rate without frame dropping issues |
| 8 | Stop Pipeline and Cleanup | Stop fast forward operation, set pipeline to NULL state, and release all allocated resources after test duration | Pipeline must stop gracefully, all resources must be freed properly, and system must return to stable state |

## Test Attributes
**Supported Models:** Video_Accelerator, Client  
**Estimated Duration:** 3 minutes  
**Priority:** High  
**Release Version:** M121
