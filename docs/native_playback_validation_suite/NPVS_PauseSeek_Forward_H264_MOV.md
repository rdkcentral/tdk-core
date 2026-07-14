## TestCase ID
NATIVE_PLAYBACK_365

## TestCase Name
NPVS_PauseSeek_Forward_H264_MOV

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and forward seek operation on H.264 MOV container video streams. The test executes controlled seek operations to a forward position while paused, then resumes playback to verify smooth transition and correct rendering at the seeked location. Confirm playback position advances correctly after seek and frame rendering shows no discontinuities.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | MOV container with H.264 video stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_H264_MOV.MOV"` in MediaValidationVariables.py. Stream contains H.264 video in MOV container format (QuickTime container for video playback testing) | Verify MOV file is accessible and readable from configured path, moovrelocator and H.264 decoder plugins available for playback |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_h264_mov` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Sunrise_H264_MOV.MOV"` | Verify `video_src_url_h264_mov` resolves to valid MOV container file with H.264 video and audio data |
| 4 | Playback Timeout Configuration | Invoke  with GST_SEEK_FLAG_FLUSH to seek forward from current position
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments. Load H264 MOV container configuration from MediaValidationVariables.py | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline for MOV container |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with H264 MOV stream URI, set `westerossink` as video sink, trigger `NULL→READY→PAUSED→PLAYING` state transition, verify `first-video-frame-callback` signal for MOV container | Verify `playbin` reaches  with first frame rendered from MOV container, no  |
| 4 | Perform Initial Playback | Transition pipeline to  state. Monitor playback for initial buffering and verify first frame rendered successfully | Verify pipeline transitions to PLAYING, first frame renders successfully, no GST_MESSAGE_ERROR detected |
| 5 | Pause Pipeline Before Forward Seek |  after reaching intermediate playback position. Monitor state transition to verify pipeline halts without  | Verify pipeline successfully pauses, position query returns valid paused position |
| 6 | Execute Forward Seek Operation | Query current position via . Invoke  to seek to `NATIVE_PLAYBACK_SEEK_POSITION` (forward position timestamp). Verify seek completion via `ASYNC_DONE` message | Verify seek position achieved within 1 second tolerance of target position, seek moves forward from current position, no seek errors detected |
| 7 | Resume Playback After Seek |  state.  Monitor `westerossink→stats` to verify `rendered_frames` increments smoothly | Verify playback resumes from seeked position without stalls, position advances at expected rate without backward jumps |
| 8 | Validate Frame Rendering Continuity | Query `westerossink→stats` structure via . Extract `rendered_frames` and `dropped_frames` via . Verify frame increments are consistent and dropped frames remain below acceptable threshold | Verify no frame drops at seek boundary, frame rendering continues smoothly post-seek from MOV container |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Priority:** High

**Release Version:** M121
