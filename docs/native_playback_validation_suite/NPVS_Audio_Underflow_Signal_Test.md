## TestCase ID
NATIVE_PLAYBACK_145

## TestCase Name
NPVS_Audio_Underflow_Signal_Test

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify audio stream underflow signal detection capability on audio decoder and audio sink elements without recovery validation. Monitor buffer-underflow-callback and underrun-callback signals when audio buffer depletes during continuous playback, then validate signals were properly emitted. Specifically test underflow signal generation on AAC audio stream using GStreamer audio element callback mechanism and verify signals propagate correctly when buffer starvation occurs.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries (mediapipelinetests binary implements GStreamer playbin pipeline with audio decoder and audio sink elements for underflow signal detection) | Verify TDK_Package is installed, `tdk_mediapipelinetests` binary is executable, all GStreamer audio plugin dependencies available |
| 2 | Media Stream Provisioning | Audio underflow test stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream URL is configured via MediaValidationVariables.py variable `video_src_url_audio_underflow` = `test_streams_base_path + "TDK_Asset_Audio_underflow_v2.mp4"`. This specialized stream contains intentional audio buffer starvation points for underflow signal generation | Verify audio underflow stream file is accessible and readable from filesystem |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_audio_underflow` must be configured in `MediaValidationVariables.py`. Path: `TDK_Asset_Audio_underflow_v2.mp4` containing embedded underflow trigger points | Verify `video_src_url_audio_underflow` variable resolves to valid, accessible audio underflow stream location |
| 4 | Device Configuration Parameters | Test execution parameters must be retrieved from device configuration file: , `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) for playback duration, `NATIVE_PLAYBACK_UNDERFLOW_AUDIO_END_POINT` (playback duration before expected underflow signal) | Verify all device config parameters are accessible and contain valid values |
| 5 | Platform-Specific Environment and GStreamer Configuration | Platform-specific environment variables must be defined in `/opt/TDK/TDK.env`: `WAYLAND_DISPLAY` (Wayland display server), `XDG_RUNTIME_DIR` (runtime directory for Wayland sockets), `LD_PRELOAD` with vendor audio/video libraries, `GST_PLUGIN_PATH` (GStreamer plugin directory). GStreamer must have: playbin element, audio decoder elements (brcmaudiodecoder, amlhalasink, rtkaudiosink), and buffer-underflow-callback/underrun-callback support | Verify `/opt/TDK/TDK.env` exists with all environment variables, Wayland display functional, GStreamer 1.16+ installed with playbin and audio elements supporting underflow signals in GST_PLUGIN_PATH |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration (GST_PLUGIN_PATH, LD_PRELOAD, WAYLAND_DISPLAY, XDG_RUNTIME_DIR). Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Verify GStreamer library version and confirm playbin and audio element availability | Verify all environment variables load correctly from TDK.env, Wayland display is created successfully, logging initialized without errors, GStreamer 1.16+ with playbin and audio elements confirmed |
| 2 | Retrieve Device Configuration and Stream Parameters | Retrieve configuration parameters from device config file:`NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (playback duration before underflow check), `NATIVE_PLAYBACK_UNDERFLOW_AUDIO_END_POINT` (playback duration before expected underflow signal). Retrieve stream URL from `MediaValidationVariables.video_src_url_audio_underflow` | Verify all configuration values retrieved successfully, stream URL resolves to valid audio underflow test file path |
| 3 | Create Playbin Element and Configure Audio Underflow Stream | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure `uri` property to audio underflow stream via `g_object_set(playbin, "uri", stream_url, NULL)` where stream_url = `test_streams_base_path + "TDK_Asset_Audio_underflow_v2.mp4"`. Register `element-setup` signal via `g_signal_connect()` to discover audio decoder (brcmaudiodecoder, amlhalasink, rtkaudiosink) and audio sink elements during pipeline construction | Verify playbin element created successfully, `uri` property configured to audio underflow stream path, `element-setup` signal will enable audio element discovery |
| 4 | Register Audio Element Underflow Callbacks for Signal Detection | During `element-setup` signal callback, identify audio decoder and audio sink elements and register underflow detection callbacks: `g_signal_connect(audio_decoder_element, "buffer-underflow-callback", G_CALLBACK(callback_func), &audio_underflow_received)` and `g_signal_connect(audio_sink_element, "underrun-callback", G_CALLBACK(callback_func), &audio_underflow_received)`. Callback sets `audio_underflow_received = true` when signal is received | Verify audio element callbacks are registered successfully on correct elements (decoder and sink) |
| 5 | Transition Pipeline to Playing and Monitor for Underflow Signal | Set pipeline to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)` to begin audio stream playback. Continuously poll playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` every 100ms. Play stream for duration specified in `NATIVE_PLAYBACK_UNDERFLOW_AUDIO_END_POINT` seconds while monitoring for `buffer-underflow-callback` or `underrun-callback` signals | Verify pipeline transitions to PLAYING state, playback begins without errors, `audio_underflow_received` flag becomes true when audio buffer starves (underflow signal received) |
| 6 | Verify Audio Underflow Signal Reception and Cleanup | Validate that `audio_underflow_received == true` indicating audio element properly emitted buffer-underflow-callback or underrun-callback signal when audio buffer depleted. Verify test framework output shows `Failures: 0` and `Errors: 0`. Set pipeline to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)` to stop playback. Unreference GStreamer objects via `gst_object_unref()` | Verify underflow signal was properly detected and flag set to true, test shows no failures/errors, pipeline reaches GST_STATE_NULL, all resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
