## TestCase ID
NATIVE_PLAYBACK_127

## TestCase Name
NPVS_Track_Switch_EAC3

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate dynamic audio track switching while maintaining video playback continuity on EAC3 codec streams. The test switches between different audio tracks in a multi-track stream and verifies seamless playback without interruption. Confirm audio rendering quality, position synchronization, and track switching timing accuracy during active playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | Multi-track EAC3 stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file path configured as `test_streams_base_path + "TDK_Asset_Sunrise_MultiTrack_EAC3.mp4"` in MediaValidationVariables.py (stream contains multiple EAC3 audio tracks for track switching validation) | Verify multi-track EAC3 stream file is accessible and readable, multiple EAC3 audio tracks are present in stream |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_multi_audio_eac3` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Sunrise_MultiTrack_EAC3.mp4` (stream must contain at least 2 EAC3 audio tracks with same codec) | Verify `video_src_url_multi_audio_eac3` resolves to valid, accessible multi-track EAC3 stream location with multiple tracks |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` configuration must be set to time duration (in seconds) for audio track switch validation. Typical value: 10 seconds playback per track configuration to ensure sufficient sampling
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Playbin Pipeline and Load Multi-Track EAC3 Stream | Create `playbin` element via  and configure `uri` property to multi-track stream path via . Set `video-sink` property to `westerossink` via  | Verify playbin element created successfully, `uri` property configured to multi-track EAC3 stream containing multiple EAC3 tracks, `video-sink` property is set |
| 3 | Retrieve Stream Properties and Verify Multiple Audio Tracks | Query playbin to determine number of audio streams via . Verify that stream contains at least 2 audio tracks (multiple EAC3 tracks). Query current audio stream index via  to identify starting audio track | Verify n-audio value is at least 2 (confirming multiple EAC3 track presence), current audio stream index successfully retrieved |
| 4 | Verify Default Audio Playback (First EAC3 Track) and Retrieve Audio-Tags | Set pipeline to  via . Transition pipeline to  via  to start playback with default (first) audio track (EAC3 codec, index 0). Emit "get-audio-tags" signal to retrieve codec metadata via . Parse tag list using  to identify codec name (EAC3). Log retrieved audio-tags including codec type, sample rate, channels for baseline verification | Verify pipeline state transitions to PLAYING with first EAC3 audio track, playback position advances linearly, audio-tags successfully retrieved and logged showing EAC3 codec information, default track playback verified |
| 5 | Monitor First Audio Track Playback Progress | g., 5-10 seconds). Verify position advances at expected rate (1 second position per 1 second real-time ±250ms tolerance). Monitor `pts-error-callback` signal to detect presentation timestamp errors during first EAC3 track playback. Check for audio underflow conditions via underflow callback monitoring. Confirm first EAC3 track is rendering smoothly without glitches or interruptions | Verify first EAC3 track playback position advances linearly, no backward jumps, no `pts-error-callback` signals detected, no audio underflow signals, first EAC3 track rendering confirmed stable and continuous |
| 6 | Switch to Second Audio Track using current-audio Signal and Flush Pipeline | Set `current-audio` property via  to switch from first EAC3 track (index 0) to second EAC3 track (index 1). Verify audio stream switches successfully by querying `current-audio` property via . Flush pipeline using  followed by  to clear buffered audio and synchronize with new track. Confirm `current-audio` query returns value 1 (second track index confirmed) | Verify `current-audio` property successfully set to index 1, pipeline flush-start and flush-stop events processed successfully, confirmation query returns value 1, audio switch ready for second track playback without stale buffers |
| 7 | Verify Second Audio Track Playback (Second EAC3 Track) and Retrieve Audio-Tags | After pipeline flush, playback continues automatically with second EAC3 track now active. Emit "get-audio-tags" signal to retrieve codec metadata for second audio track via . Parse tag list using  to identify codec name (EAC3). Log retrieved audio-tags including codec type, sample rate, channels to verify track switch from first to second EAC3 track. Compare logged audio-tags from Step 4 (first EAC3 track) with current audio-tags (second EAC3 track) to confirm track change | Verify second EAC3 track audio-tags successfully retrieved and logged showing EAC3 codec information, track change confirmed through audio-tags retrieval, second track playback verified active |
| 8 | Monitor Second Audio Track Playback Progress During Track Switch | g., 5-10 seconds) after track switch. Verify position advances at expected rate (1 second position per 1 second real-time ±250ms tolerance) with no backward jumps from pre-flush position. Monitor `pts-error-callback` signal to detect presentation timestamp errors during second EAC3 track playback. Check for audio underflow conditions via underflow callback monitoring. Confirm second EAC3 track is rendering smoothly after track change | Verify second EAC3 track playback position advances linearly from flush point, no backward jumps or position glitches, no `pts-error-callback` signals detected, no audio underflow signals, second EAC3 track rendering confirmed stable and continuous |
| 9 | Validate Multiple Audio Track Support using Audio-Tags Logs | Review logged audio-tags from Step 4 (first EAC3 track tags) and Step 7 (second EAC3 track tags). Verify codec names are both EAC3 but confirm track change occurred by comparing tag details (sample rate, channels may differ between tracks). Confirm both audio track tags were successfully retrieved, parsed, and logged. Verify test framework output shows `Failures: 0` and `Errors: 0`. Set pipeline to  via .  to release all codec decoders, audio sink, demultiplexer resources. Free allocated memory and close logging file | Verify audio-tags logs confirm both EAC3 tracks were active and properly identified, test execution completed successfully with multi-track validation via tags comparison, no failures or errors in test output, pipeline reaches , all GStreamer resources released, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
