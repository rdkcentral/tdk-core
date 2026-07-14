## TestCase ID
NATIVE_PLAYBACK_130

## TestCase Name
NPVS_Track_Switch_with_Pause_EAC3

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate dynamic audio track switching during pause/resume transitions on EAC3 streams while maintaining position consistency. The test switches between different audio tracks during paused and active playback states. Confirm audio rendering quality, position synchronization during pause, and track switching timing accuracy without interruption or position discontinuities.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | Multi-track EAC3 stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file path configured as `test_streams_base_path + "TDK_Asset_Sunrise_MultiTrack_EAC3.mp4"` in MediaValidationVariables.py (stream contains multiple EAC3 audio tracks for track switching validation with pause operations) | Verify multi-track EAC3 stream file is accessible and readable, multiple EAC3 audio tracks are present in stream |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_multi_audio_eac3` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Sunrise_MultiTrack_EAC3.mp4` (stream must contain at least 2 EAC3 audio tracks with same codec) | Verify `video_src_url_multi_audio_eac3` resolves to valid, accessible multi-track EAC3 stream location with multiple tracks |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` configuration must be set to time duration (in seconds) for audio track switch validation with pause operations. Typical value: 20 seconds total (10 seconds per track with pause-resume cycles)
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Playbin Pipeline and Load Multi-Track EAC3 Stream | Create `playbin` element via  and configure `uri` property to multi-track stream path via . Set `video-sink` property to `westerossink` via  | Verify playbin element created successfully, `uri` property configured to multi-track EAC3 stream containing multiple EAC3 tracks, `video-sink` property is set |
| 3 | Retrieve Stream Properties and Verify Multiple Audio Tracks | Query playbin to determine number of audio streams via . Verify that stream contains at least 2 audio tracks (multiple EAC3 tracks). Query current audio stream index via  to identify starting audio track | Verify n-audio value is at least 2 (confirming multiple EAC3 track presence), current audio stream index successfully retrieved |
| 4 | Verify Default Audio Playback (First EAC3 Track) and Execute Pause-Resume Cycle | Set pipeline to  via . Transition pipeline to  via  to start playback with default (first) audio track (EAC3 codec, index 0). Record initial playback position via . Emit "get-audio-tags" signal to retrieve codec metadata via . Log audio-tags for baseline verification.  via  and verify position stops advancing. Query position during pause to confirm it remains at recorded value ±10ms | Verify pipeline state transitions to PLAYING with first EAC3 track, audio-tags successfully retrieved and logged, pipeline transitions to PAUSED, position stops advancing during pause |
| 5 | Monitor First Track Playback and Resume from Pause | Transition pipeline back to  via . Verify playback resumes from paused position without position jumps via . Poll playback position at 100ms intervals for 3-5 seconds. Verify position advances at expected rate (1 second position per 1 second real-time ±250ms tolerance) from resumed position. Monitor `pts-error-callback` signal to detect presentation timestamp errors. Confirm first EAC3 track continues rendering smoothly without glitches | Verify playback resumes without position jumps, position advances linearly from paused point, no `pts-error-callback` signals detected, first EAC3 track rendering stable after resume |
| 6 | Switch Audio Track During Paused State | Set pipeline to  via  while first EAC3 track is playing. Record position at pause point. Set `current-audio` property via  to switch from first EAC3 track (index 0) to second EAC3 track (index 1) during paused state. Verify audio stream switches successfully by querying `current-audio` property via . Flush pipeline using  followed by  to clear buffered audio and synchronize with new track | Verify `current-audio` property successfully set to index 1 during pause, pipeline flush events processed successfully, confirmation query returns value 1 |
| 7 | Verify Second Track Playback After Pause-Resume-Switch Cycle | Transition pipeline to  via  to resume playback with second EAC3 track now active. Emit "get-audio-tags" signal to retrieve codec metadata for second audio track via . Parse tag list and log audio-tags to verify track switch. Query playback position via  to confirm position advances from paused point. Compare logged audio-tags from Step 4 (first EAC3 track) with current audio-tags (second EAC3 track) to confirm track change | Verify second EAC3 track audio-tags successfully retrieved and logged, track change confirmed through audio-tags comparison, playback position advances from previous paused point |
| 8 | Monitor Second Track Playback and Execute Pause-Resume During Second Track |  Verify position advances at expected rate (1 second position per 1 second real-time ±250ms tolerance). Transition pipeline to  via . Record position during pause and verify it stops advancing (±10ms tolerance). Transition back to  via . Verify playback resumes without position jumps and continues advancing at expected rate. Monitor `pts-error-callback` signal throughout pause-resume cycle | Verify second EAC3 track position advances linearly, pause stops position advance, resume continues from paused point without jumps, no `pts-error-callback` signals detected, second track rendering stable through pause-resume cycle |
| 9 | Validate Multi-Track Support with Pause-Resume Cycling | Review logged audio-tags from Step 4 (first EAC3 track) and Step 7 (second EAC3 track). Verify both codec names are EAC3 and track change is confirmed. Confirm all position queries during pause/resume cycles show expected behavior (position halts during pause, resumes without jumps). Verify test framework output shows `Failures: 0` and `Errors: 0`. Set pipeline to  via .  to release all codec decoders, audio sink, demultiplexer resources. Free allocated memory and close logging file | Verify audio-tags logs confirm both EAC3 tracks were active, track switching during pause validated, position behavior during pause-resume cycles confirmed correct, test execution completed successfully, pipeline reaches , all GStreamer resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
