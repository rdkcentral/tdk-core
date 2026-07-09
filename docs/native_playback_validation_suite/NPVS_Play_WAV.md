## TestCase ID
NATIVE_PLAYBACK_226

## TestCase Name
NPVS_Play_WAV

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate PCM audio codec playback  with WAV audio stream. Initialize audio-only pipeline with wavparse element, configure `autoaudiosink` for audio output. Execute continuous playback for 10 seconds via  polling. Verify audio stream present via 
-audio` property, monitor audio rendering statistics, and validate clean pipeline state transitions without errors.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | WAV WAV PCM stream (`TDK_Asset_Sunrise_WAV_Audio.wav`) must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`) element with `wavparse` capable of parsing WAV container  | Verify WAV stream is accessible and contains valid WAV and PCM representations |
| 3 | Stream Variable Configuration | `audio_src_url_wav_pcm` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "TDK_Asset_Sunrise_WAV_Audio.wav"` | Verify `audio_src_url_wav_pcm` resolves to valid WAV location with correct codec support |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout configured for standard playback (10 seconds) | Verify `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` is set to 10 seconds in configuration file
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins and audio configuration. Establish Wayland display session via RDKWindowManager (audio-only playback). Set up logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify environment variables load correctly, logging initialized |
| 2 | Configure and Execute Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` configuration; Retrieve stream URL from `audio_src_url_wav_pcm` variable; Execute `mediapipelinetests test_generic_playback <URL> timeout=<seconds>` with audio stream | Verify mediapipelinetests initializes with WAV audio stream |
| 3 | Construct Audio Pipeline | Create `playbin` element via ; Set `uri` property to WAV audio file via ; Configure `autoaudiosink` for audio output via ; Set state to  via  | Verify playbin reaches , audio sink active |
| 4 | Query Audio Stream Properties | Query audio stream presence via ; Verify n-audio >= 1 confirming PCM stream; Query audio pad capabilities for PCM format information | Verify n-audio >= 1; Verify PCM stream properties queried successfully |
| 5 | Play Audio Stream | Execute continuous playback via internal play mechanism for configured timeout (10 seconds); Monitor playback position via  at 100ms intervals | Verify position advances at 1x rate (±1 second), no stalls |
| 6 | Validate Audio Rendering | Monitor audio output on device; Verify continuous audio playback without glitches or interruptions during timeout window | Verify audio renders clearly throughout playback window |
| 7 | Monitor GStreamer Bus | Monitor GStreamer message bus via  for , , or  messages; Verify no audio decoder errors | Verify no errors/warnings; Verify clean audio decoding |
| 8 | Release Pipeline Resources | Call `terminatePipeline(playbin)` to set state to  and release audio decoder and sink resources | Verify pipeline reaches ; Verify test output shows "Failures: 0" |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
