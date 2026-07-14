## TestCase ID
NATIVE_PLAYBACK_34

## TestCase Name
NPVS_PlayPause_96kHz_OPUS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate play-pause-resume state transitions during MP4 OPUS 96kHz playback  with audio sink at 96kHz sampling rate. Test creates `playbin` with , configures stream via , transitions pipeline between  and  states via , and validates audio sampling rate remains at 96kHz during playback via `stats` property on audio sink. Confirm position remains stationary during pause with 0ms drift tolerance while verifying position advances 1x rate during play via ±100ms tolerance. Verify audio rendered frames increment only during PLAYING state and remain static during PAUSED state, no GST_MESSAGE_ERROR on bus, and "Failures: 0" output for all state transitions.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary, GStreamer plugins (qtdemux demuxer, necessary decoders for 96kHz audio), and audio sink element | Verify TDK_Package is installed, binary is executable, qtdemux element available in GStreamer, audio decoder supports 96kHz |
| 2 | Media Stream Provisioning | MP4 OPUS 96kHz stream with 96kHz sampling rate must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file path configured in MediaValidationVariables.py as `test_streams_base_path + "TDK_Asset_Sunrise_OPUS_96kHz.mp4"`  | Verify stream file is accessible and contains valid 96kHz audio |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_96khz_opus` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "TDK_Asset_Sunrise_OPUS_96kHz.mp4"` | Verify `video_src_url_96khz_opus` resolves to valid, accessible stream with 96kHz audio |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device config to allow complete play-pause cycles with audio sampling rate verification | Verify timeout configured for minimum 3 play-pause cycles with audio sampling verification |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required variables, audio sink available, environment properly configured |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, qtdemux demuxer, audio decoders for 96kHz support, and audio sink configuration. Establish display session via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify all environment variables load correctly, display session created successfully, logging initialized without errors |
| 2 | Configure Test Framework and Load Stream | Set test name to `test_play_pause_pipeline`, Enable audio sampling rate validation flag. Load MP4 OPUS 96kHz stream via `video_src_url_96khz_opus` variable from MediaValidationVariables.py. Set timeout to NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT | Verify test case name configured, audio sampling rate flag enabled, stream URI resolved correctly, timeout set for minimum 3 play-pause cycles |
| 3 | Create Playbin Pipeline and Configure Audio Sink | Create `playbin` element via . Set `uri` property to stream URL via . Configure audio-sink via  for 96kHz playback | Verify playbin element created successfully, URI property set to stream, audio sink properly configured |
| 4 | Transition Pipeline to PLAYING State | Set pipeline state to  via . Monitor  on GStreamer bus via . Wait for state change completion via  polling until  | Verify pipeline transitions to PLAYING state without errors, qtdemux active, first audio frame detected |
| 5 | Validate Initial Audio Sampling Rate and Frame Rendering | Query audio sink `stats` property via  to retrieve audio rendered_frames and dropped_frames counters. Execute position query via  to establish baseline. Verify rendered_frames > 0 and audio sampling rate = 96kHz via internal buffer analysis | Verify audio rendered_frames counter increments during PLAYING state at 96kHz rate, dropped_frames < 1% of rendered_frames, initial position obtained |
| 6 | Transition Pipeline to PAUSED State | Set pipeline state to  via . Monitor state change completion via   Verify position remains constant (±0 movement, 0ms drift tolerance). Query audio sink `stats` property to verify rendered_frames counter remains static (no increment). Verify no audio samples processed | Verify position does NOT advance during PAUSED state with ±0 tolerance, audio rendered_frames counter unchanged, audio processing halted |
| 8 | Transition Pipeline Back to PLAYING State | Set pipeline state to  via . Monitor state change completion via  polling until  | Verify pipeline successfully resumes to PLAYING state without errors, state change completes synchronously |
| 9 | Validate Resumed Playback with Audio Sampling Rate Verification | Execute position query via  at 1-second intervals for NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT seconds. Verify position advances at 1x rate (1 second per 1 second real-time ±100ms tolerance). Query audio sink `stats` property at each 1-second interval to verify: (1) audio rendered_frames increment at expected rate for 96kHz, (2) sampling rate difference from expected rate within ±5% threshold. Verify no GST_MESSAGE_ERROR on bus | Verify position advances smoothly at 1x rate, audio rendered_frames increment at 96kHz rate with ±5% tolerance, no errors detected |
| 10 | Repeat Play-Pause Cycles Minimum 3 Times with Continuous Audio Sampling Verification | Repeat steps 6-9 (PAUSED -> PLAYING transitions) minimum 3 times total. For each cycle, continuously verify audio sampling rate remains 96kHz ±5% threshold during PLAYING periods. Verify audio sampling rate validation passes for all cycles | Verify all 3+ play-pause cycles complete successfully with consistent 96kHz audio sampling, sampling rate validation passes for each cycle, no performance degradation |
| 11 |  Free allocated memory and close logging file. Verify test framework output shows "Failures: 0" and "Errors: 0" | Verify pipeline reaches , all GStreamer resources released without segmentation faults, test reports zero failures and errors for all play-pause cycles with 96kHz sampling rate validation |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
