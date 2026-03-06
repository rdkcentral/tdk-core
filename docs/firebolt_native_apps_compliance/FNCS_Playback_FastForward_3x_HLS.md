# FNCS_PLAYBACK_40 - 4K HLS FastForward 3x Playback Test

## TestCase ID

FNCS_PLAYBACK_40

## TestCase Name

FNCS_Playback_FastForward_3x_HLS

## Table Of Contents

1. [TestCase ID](#testcase-id)
2. [TestCase Name](#testcase-name)
3. [Objective](#objective)
4. [Preconditions](#preconditions)
5. [Test Steps](#test-steps)
6. [Test Attributes](#test-attributes)

## Objective

Validate the FastForward 3x trick play operation on 4K HLS adaptive streaming content to ensure proper segment-based acceleration control and adaptive bitrate handling during high-speed playback.

### VIDEO CODEC

H264/HEVC (HLS Adaptive)

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package should be installed in DUT |
| 2 | tdk_mediapipelinetests_trickplay application must be installed in DUT |
| 3 | Test stream for 4K HLS format must be available through video_src_url_4k_hls_test configuration in MediaValidationVariables.py - stream must be installed in the server hosting streams or installed inside the device if using filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://\<server_hosting_stream\>:\<port_number\>/) based on their setup preference |
| 4 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set in device config file - specifies whether SOC level AV playback verification should be done (yes/no), default is no |
| 5 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration should be set in device config file - specifies timeout in seconds for media playback duration, default is 10 seconds |
| 6 | FIREBOLT_COMPLIANCE_FASTFORWARD_3x_4x_ENABLED configuration should be set to yes in device config file - enables 3x FastForward trick play support on the device |

## Test Steps

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Verify FastForward 3x Support | Check FIREBOLT_COMPLIANCE_FASTFORWARD_3x_4x_ENABLED configuration value from device config to confirm 3x trick play is supported | FastForward 3x feature must be enabled (configuration value should be yes) |
| 3 | Execute MediaPipeline FastForward Test | Retrieve configuration values (FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT), get 4K HLS stream URL from MediaValidationVariables.video_src_url_4k_hls_test, construct trickplay command with fastforward3x operation parameters, and execute tdk_mediapipelinetests_trickplay command | Configuration values must be retrieved successfully, 4K HLS stream URL must be obtained correctly, fastforward3x command must be constructed properly as `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/[STREAM_NAME] checkavstatus=no operations=fastforward3x:10`, and test application starts execution without errors |
| 4 | Setup GStreamer Pipeline | Create GStreamer pipeline with playbin element configured for 4K HLS adaptive streaming playback using westeros-sink for video rendering with HLS demuxer support | GStreamer pipeline must be created successfully with proper HLS adaptive streaming capabilities and 4K video decoding support |
| 5 | Configure Trick Play Operation | Set pipeline to PLAYING state and configure fastforward3x operation with specified timeout duration for accelerated HLS segment processing | Pipeline must transition to PLAYING state successfully and fastforward3x operation must be configured with 3x playback rate for HLS adaptive content |
| 6 | Execute FastForward 3x Operation | Start fastforward3x playbook operation and monitor 4K HLS adaptive streaming processing for specified timeout duration while managing segment transitions | FastForward 3x operation must execute successfully, 4K HLS stream must play at 3x speed with proper adaptive bitrate segment handling during acceleration |
| 7 | Monitor Playback and Position Validation | Track playback position progression and verify that position advances at 3x normal playback rate throughout the operation duration while handling HLS segment boundaries | Playback position must advance consistently at 3x rate, indicating proper fastforward operation with seamless HLS segment transitions |
| 8 | Validate Output and Cleanup | Check command execution output for success indicators ("Failures: 0", "Errors: 0", or "failed: 0") and properly cleanup pipeline resources | mediapipelinetests execution must return success status with zero failures and errors, pipeline resources must be released properly |

## Test Attributes

**Supported Models:** Video_Accelerator  
**Estimated Duration:** 3 minutes  
**Priority:** High  
**Release Version:** M131