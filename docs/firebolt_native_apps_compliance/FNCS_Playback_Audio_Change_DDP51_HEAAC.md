# FNCS_Playback_Audio_Change_DDP51_HEAAC Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_126

## TestCase Name
FNCS_Playback_Audio_Change_DDP51_HEAAC

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To verify the media pipeline's capability to switch between different audio codecs (DDP51 and HEAAC) present in the same stream without changing the video, ensuring seamless audio codec transitions during playback. This test validates dynamic audio codec switching functionality by monitoring playback continuity and verifying successful codec detection during runtime transitions.

**AUDIO CODECS:** DDP51 ⟷ HEAAC

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | Multi-codec stream with DDP51 and HEAAC audio tracks must be available and referenced in MediaValidationVariables.video_src_url_ddp51_heaac |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration in Video_Accelerator.config specifies playback duration per codec in seconds, default 10 seconds |
| 12 | FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD configuration in Video_Accelerator.config specifies acceptable playback latency threshold in milliseconds |
| 13 | video_src_url_ddp51_heaac variable in MediaValidationVariables.py contains multi-codec stream URL with both DDP51 and HEAAC audio tracks |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT config values, get multi-codec stream URL from MediaValidationVariables.video_src_url_ddp51_heaac, construct tdk_mediapipelinetests command with timeout parameter, and run test_audio_change with DDP51/HEAAC stream | Configuration values retrieved, multi-codec stream URL obtained, command executed: `tdk_mediapipelinetests test_audio_change <DDP51_HEAAC_STREAM_URL> checkavstatus=no timeout=10`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element and configure with multi-codec audio stream support, enable audio codec switching capability using current-audio property | Playbin element created successfully with multi-codec audio stream support and codec switching capability enabled |
| 4 | Configure Audio Output | Create and configure audio sink element for multi-codec audio playback, establish audio codec detection monitoring | Audio sink element configured successfully for multi-codec playback with codec detection monitoring enabled |
| 5 | Start Initial DDP51 Playback | Set pipeline to PLAYING state and begin playback with initial DDP51 audio codec, monitor audio frames and codec detection | Pipeline transitions to PLAYING state successfully, DDP51 audio playback starts, and codec detection confirms DDP51 audio stream |
| 6 | Validate DDP51 Playback | Monitor DDP51 audio playback for configured timeout duration (default 10 seconds), verify audio frames and codec stability | DDP51 audio playback proceeds successfully for full timeout duration with stable audio frames and confirmed DDP51 codec detection |
| 7 | Initiate Audio Codec Switch | Use playbin current-audio property to switch from DDP51 to HEAAC audio track while maintaining video playback continuity | Audio codec switch initiated successfully using current-audio property, video playback continues without interruption |
| 8 | Complete HEAAC Transition | Monitor transition from DDP51 to HEAAC audio codec, verify seamless audio changeover without audio dropouts or glitches | Transition from DDP51 to HEAAC completed successfully with seamless audio changeover and no audio artifacts |
| 9 | Validate HEAAC Playback | Monitor HEAAC audio playback for configured timeout duration (default 10 seconds), verify audio frames and codec stability | HEAAC audio playback proceeds successfully for full timeout duration with stable audio frames and confirmed HEAAC codec detection |
| 10 | Verify Codec Detection | Check output for AAC and EAC3 codec detection confirmations using checkifCodecPlayed validation for both audio codecs | Output contains successful codec detection for both "aac" and "e-ac-3" codecs indicating proper codec recognition |
| 11 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating DDP51 to HEAAC audio codec switching completed without errors |
| 12 | Cleanup Pipeline | Set playbin pipeline to NULL state, release multi-codec audio resources, and clean up codec switching components | Pipeline transitions to NULL state successfully, multi-codec audio resources released, and all components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121