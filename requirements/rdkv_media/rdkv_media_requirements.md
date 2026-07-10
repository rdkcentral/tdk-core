# Media Validation Suite (MVS) — Requirements

> **Suite:** Media Validation Suite (MVS) | **Req ID Prefix:** `MVS-REQ`
> **Source specs:** [tdk-core/docs/rdkv_media](https://github.com/rdkcentral/tdk-core/tree/main/docs/rdkv_media) (622 test cases)
> **Total requirements:** 23

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** across all player runtimes.
Test cases from Lightning Video Player (`Video_Play_*`, `Video_PlayPause_*`, etc.),
Lightning SHAKA Player (`Video_SHAKA_*`), HTML5 native player (`Video_HTML_*`),
HTML5 Shaka.js player (`Video_HTML_SHAKA_*`), and Animation app (`Animation_*`)
are all mapped to the same functional requirement where they validate the same capability.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| MVS-REQ-001 | Basic video and audio media playback | Functional Playback | 49 |
| MVS-REQ-002 | 4K UHD video playback | Functional Playback | 6 |
| MVS-REQ-003 | Live streaming playback — HLS and DASH | Functional Playback | 4 |
| MVS-REQ-004 | Audio-only stream playback | Functional Playback | 8 |
| MVS-REQ-005 | DASH segment addressing format compliance | Functional Playback | 4 |
| MVS-REQ-006 | Resolution-variant playback — 480i to 1080p | Quality | 10 |
| MVS-REQ-007 | Audio sound mode output selection — Atmos, Dolby Digital, Stereo | Functional Playback | 6 |
| MVS-REQ-008 | Full-duration content playback to natural end-of-stream | Lifecycle | 23 |
| MVS-REQ-009 | PlayPause operation | Trick Play | 87 |
| MVS-REQ-010 | PlayPause stress testing | Trick Play (Stress) | 25 |
| MVS-REQ-011 | Mute and unmute audio | Lifecycle | 44 |
| MVS-REQ-012 | Mute/unmute audio stress testing | Lifecycle (Stress) | 20 |
| MVS-REQ-013 | Fast-forward at 2×, 3×, and 4× rates | Trick Play | 94 |
| MVS-REQ-014 | Fast-forward stress testing | Trick Play (Stress) | 12 |
| MVS-REQ-015 | Seek operations — position seek, seek during FF, forward and backward seek | Seek | 88 |
| MVS-REQ-016 | Seek stress testing | Seek (Stress) | 24 |
| MVS-REQ-017 | Combined trick play sequence (FF, RW, pause) | Trick Play | 15 |
| MVS-REQ-018 | Loop play — continuous content looping | Lifecycle | 15 |
| MVS-REQ-019 | Audio volume control | Lifecycle | 12 |
| MVS-REQ-020 | Widevine DRM content protection — CTR, Clear Lead, Crypt-Skip, MultiKey | Security (DRM) | 34 |
| MVS-REQ-021 | Widevine CBCS content encryption | Security (DRM) | 8 |
| MVS-REQ-022 | PlayReady DRM content protection — CTR and CBCS modes | Security (DRM) | 23 |
| MVS-REQ-023 | Animation rendering performance | Platform (Performance) | 11 |
| | **Total** | | **622** |

### MVS-REQ-001 — Basic video and audio media playback (49 tests)

Lightning Video Player (17): RDKV_CERT_MVS_Video_Play_DASH_H264, RDKV_CERT_MVS_Video_Play_DASH_H264_Main, RDKV_CERT_MVS_Video_Play_DASH_H264_VP9, RDKV_CERT_MVS_Video_Play_HLS_H264, RDKV_CERT_MVS_Video_Play_HEVC, RDKV_CERT_MVS_Video_Play_HEVC_MKV, RDKV_CERT_MVS_Video_Play_HEVC_Main10, RDKV_CERT_MVS_Video_Play_MKV, RDKV_CERT_MVS_Video_Play_MP4, RDKV_CERT_MVS_Video_Play_MPEG, RDKV_CERT_MVS_Video_Play_MPEG_TS, RDKV_CERT_MVS_Video_Play_H263, RDKV_CERT_MVS_Video_Play_VP8, RDKV_CERT_MVS_Video_Play_VP9, RDKV_CERT_MVS_Video_Play_AV1, RDKV_CERT_MVS_Video_Play_EC3, RDKV_CERT_MVS_Video_Play_HDR

Lightning SHAKA Player (11): RDKV_CERT_MVS_Video_SHAKA_Play_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Play_DASH_H264_Main, RDKV_CERT_MVS_Video_SHAKA_Play_HEVC, RDKV_CERT_MVS_Video_SHAKA_Play_HEVC_Main10, RDKV_CERT_MVS_Video_SHAKA_Play_HLS_H264, RDKV_CERT_MVS_Video_SHAKA_Play_MKV, RDKV_CERT_MVS_Video_SHAKA_Play_MP4, RDKV_CERT_MVS_Video_SHAKA_Play_VP9, RDKV_CERT_MVS_Video_SHAKA_Play_HDR, RDKV_CERT_MVS_Video_SHAKA_Play_DASH_1080p, RDKV_CERT_MVS_Video_SHAKA_Play_HLS_1080p

HTML5 native player (19): RDKV_CERT_MVS_Video_HTML_Play_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_Play_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_Play_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_Play_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_Play_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_Play_DASH_H264, RDKV_CERT_MVS_Video_HTML_Play_DASH_HEVC, RDKV_CERT_MVS_Video_HTML_Play_DASH_VP9, RDKV_CERT_MVS_Video_HTML_Play_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_Play_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_Play_HEVC, RDKV_CERT_MVS_Video_HTML_Play_HLS_H264, RDKV_CERT_MVS_Video_HTML_Play_HLS_HEVC, RDKV_CERT_MVS_Video_HTML_Play_MP4, RDKV_CERT_MVS_Video_HTML_Play_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Play_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Play_VORBIS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_Play_Vorbis_Webm, RDKV_CERT_MVS_Video_HTML_Play_Webm

HTML5 Shaka.js player (2): RDKV_CERT_MVS_Video_HTML_SHAKA_Play_DASH_H264, RDKV_CERT_MVS_Video_HTML_SHAKA_Play_HLS_H264

### MVS-REQ-002 — 4K UHD video playback (6 tests)

Lightning Video Player (4): RDKV_CERT_MVS_Video_Play_4K_AV1, RDKV_CERT_MVS_Video_Play_4K_DASH, RDKV_CERT_MVS_Video_Play_4K_HLS, RDKV_CERT_MVS_Video_Play_4K_VP9

Lightning SHAKA Player (2): RDKV_CERT_MVS_Video_SHAKA_Play_4K_DASH, RDKV_CERT_MVS_Video_SHAKA_Play_4K_HLS

### MVS-REQ-003 — Live streaming playback (4 tests)

Lightning Video Player (2): RDKV_CERT_MVS_Video_Play_Live_DASH, RDKV_CERT_MVS_Video_Play_Live_HLS

Lightning SHAKA Player (2): RDKV_CERT_MVS_Video_SHAKA_Play_Live_DASH, RDKV_CERT_MVS_Video_SHAKA_Play_Live_HLS

### MVS-REQ-004 — Audio-only stream playback (8 tests)

Lightning Video Player (8): RDKV_CERT_MVS_Video_Play_AAC, RDKV_CERT_MVS_Video_Play_Audio_Only, RDKV_CERT_MVS_Video_Play_DTS_Audio, RDKV_CERT_MVS_Video_Play_M4A_Audio, RDKV_CERT_MVS_Video_Play_MP3_Audio, RDKV_CERT_MVS_Video_Play_OGG, RDKV_CERT_MVS_Video_Play_Opus, RDKV_CERT_MVS_Video_Play_WAV_PCM_Audio

### MVS-REQ-005 — DASH segment addressing format compliance (4 tests)

Lightning Video Player (4): RDKV_CERT_MVS_Video_Play_DASH_SegmentBase, RDKV_CERT_MVS_Video_Play_DASH_SegmentList, RDKV_CERT_MVS_Video_Play_DASH_SegmentTemplate, RDKV_CERT_MVS_Video_Play_DASH_SegmentTimeline

### MVS-REQ-006 — Resolution-variant playback 480i to 1080p (10 tests)

Lightning Video Player (10): RDKV_CERT_MVS_Video_Play_DASH_480i, RDKV_CERT_MVS_Video_Play_DASH_480p, RDKV_CERT_MVS_Video_Play_DASH_720p, RDKV_CERT_MVS_Video_Play_DASH_1080i, RDKV_CERT_MVS_Video_Play_DASH_1080p, RDKV_CERT_MVS_Video_Play_HLS_480i, RDKV_CERT_MVS_Video_Play_HLS_480p, RDKV_CERT_MVS_Video_Play_HLS_720p, RDKV_CERT_MVS_Video_Play_HLS_1080i, RDKV_CERT_MVS_Video_Play_HLS_1080p

### MVS-REQ-007 — Audio sound mode output selection (6 tests)

Lightning Video Player (3): RDKV_CERT_MVS_Video_Play_DASH_SoundMode_AtmosOutput, RDKV_CERT_MVS_Video_Play_DASH_SoundMode_DolbyDigital, RDKV_CERT_MVS_Video_Play_DASH_SoundMode_Stereo

Lightning SHAKA Player (3): RDKV_CERT_MVS_Video_SHAKA_Play_DASH_SoundMode_AtmosOutput, RDKV_CERT_MVS_Video_SHAKA_Play_DASH_SoundMode_DolbyDigital, RDKV_CERT_MVS_Video_SHAKA_Play_DASH_SoundMode_Stereo

### MVS-REQ-008 — Full-duration content playback to natural end-of-stream (23 tests)

Lightning Video Player (13): RDKV_CERT_MVS_Video_Play_Full_DASH_H264, RDKV_CERT_MVS_Video_Play_Full_HLS_H264, RDKV_CERT_MVS_Video_Play_Full_HEVC, RDKV_CERT_MVS_Video_Play_Full_HEVC_MKV, RDKV_CERT_MVS_Video_Play_Full_MKV, RDKV_CERT_MVS_Video_Play_Full_MP4, RDKV_CERT_MVS_Video_Play_Full_AV1, RDKV_CERT_MVS_Video_Play_Full_VP9, RDKV_CERT_MVS_Video_Play_Full_4K_DASH, RDKV_CERT_MVS_Video_Play_Full_4K_VP9, RDKV_CERT_MVS_Video_Play_Full_4K_AV1, RDKV_CERT_MVS_Video_Play_Full_EC3, RDKV_CERT_MVS_Video_Play_Full_Audio_Only

Lightning SHAKA Player (10): RDKV_CERT_MVS_Video_SHAKA_Play_Full_4K_AV1, RDKV_CERT_MVS_Video_SHAKA_Play_Full_AV1, RDKV_CERT_MVS_Video_SHAKA_Play_Full_Audio_Only, RDKV_CERT_MVS_Video_SHAKA_Play_Full_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Play_Full_EC3, RDKV_CERT_MVS_Video_SHAKA_Play_Full_HEVC, RDKV_CERT_MVS_Video_SHAKA_Play_Full_HLS_H264, RDKV_CERT_MVS_Video_SHAKA_Play_Full_MKV, RDKV_CERT_MVS_Video_SHAKA_Play_Full_MP4, RDKV_CERT_MVS_Video_SHAKA_Play_Full_VP9

### MVS-REQ-009 — PlayPause operation (87 tests)

Lightning Video Player (21): RDKV_CERT_MVS_Video_PlayPause_DASH_H264, RDKV_CERT_MVS_Video_PlayPause_DASH_H264_Main, RDKV_CERT_MVS_Video_PlayPause_HLS_H264, RDKV_CERT_MVS_Video_PlayPause_HEVC, RDKV_CERT_MVS_Video_PlayPause_HEVC_MKV, RDKV_CERT_MVS_Video_PlayPause_HEVC_Main10, RDKV_CERT_MVS_Video_PlayPause_MKV, RDKV_CERT_MVS_Video_PlayPause_MP4, RDKV_CERT_MVS_Video_PlayPause_AV1, RDKV_CERT_MVS_Video_PlayPause_VP9, RDKV_CERT_MVS_Video_PlayPause_EC3, RDKV_CERT_MVS_Video_PlayPause_AAC, RDKV_CERT_MVS_Video_PlayPause_HDR, RDKV_CERT_MVS_Video_PlayPause_4K_AV1, RDKV_CERT_MVS_Video_PlayPause_4K_DASH, RDKV_CERT_MVS_Video_PlayPause_4K_HLS, RDKV_CERT_MVS_Video_PlayPause_4K_VP9, RDKV_CERT_MVS_Video_PlayPause_Audio_Only, RDKV_CERT_MVS_Video_PlayPause_MPEG_TS, RDKV_CERT_MVS_Video_PlayPause_Opus, RDKV_CERT_MVS_Video_PlayPause_OGG

Lightning SHAKA Player (8): RDKV_CERT_MVS_Video_SHAKA_PlayPause_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_PlayPause_DASH_H264_Main, RDKV_CERT_MVS_Video_SHAKA_PlayPause_HEVC, RDKV_CERT_MVS_Video_SHAKA_PlayPause_HEVC_Main10, RDKV_CERT_MVS_Video_SHAKA_PlayPause_HLS_H264, RDKV_CERT_MVS_Video_SHAKA_PlayPause_MKV, RDKV_CERT_MVS_Video_SHAKA_PlayPause_MP4, RDKV_CERT_MVS_Video_SHAKA_PlayPause_VP9

HTML5 native player (56): RDKV_CERT_MVS_Video_HTML_PlayPause_AAC_H264_MP4, RDKV_CERT_MVS_Video_HTML_PlayPause_AAC_H264_MP4_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_AAC_H264_MP4_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_AAC_H264_MP4_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_PlayPause_AAC_H265_MP4_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_AAC_H265_MP4_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_AAC_H265_MP4_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_PlayPause_AC3_H265_MP4_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_AC3_H265_MP4_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_AC3_H265_MP4_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_AAC_MP4_1080p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_AAC_MP4_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_AAC_MP4_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_AAC_MP4_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_OPUS_WEBM_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_OPUS_WEBM_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_OPUS_WEBM_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_VORBIS_WEBM_1080p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_VORBIS_WEBM_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_AV1_VORBIS_WEBM_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_DASH_H264, RDKV_CERT_MVS_Video_HTML_PlayPause_DASH_HEVC, RDKV_CERT_MVS_Video_HTML_PlayPause_DASH_VP9, RDKV_CERT_MVS_Video_HTML_PlayPause_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_PlayPause_H264_AC3_MP4_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_H264_AC3_MP4_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_H264_AC3_MP4_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_PlayPause_H264_MP3_MP4_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_H264_MP3_MP4_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_H264_MP3_MP4_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_HEVC, RDKV_CERT_MVS_Video_HTML_PlayPause_HLS_H264, RDKV_CERT_MVS_Video_HTML_PlayPause_HLS_HEVC, RDKV_CERT_MVS_Video_HTML_PlayPause_MP4, RDKV_CERT_MVS_Video_HTML_PlayPause_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_PlayPause_OPUS_VP8_WEBM_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_OPUS_VP8_WEBM_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_OPUS_VP8_WEBM_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_OPUS_VP9_WEBM_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_OPUS_VP9_WEBM_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_OPUS_VP9_WEBM_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_PlayPause_VORBIS_VP8_WEBM_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_VORBIS_VP8_WEBM_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_VORBIS_VP8_WEBM_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_VORBIS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_PlayPause_VORBIS_VP9_WEBM_2160p, RDKV_CERT_MVS_Video_HTML_PlayPause_VORBIS_VP9_WEBM_480p, RDKV_CERT_MVS_Video_HTML_PlayPause_VORBIS_VP9_WEBM_720p, RDKV_CERT_MVS_Video_HTML_PlayPause_Vorbis_Webm, RDKV_CERT_MVS_Video_HTML_PlayPause_Webm

HTML5 Shaka.js player (2): RDKV_CERT_MVS_Video_HTML_SHAKA_PlayPause_DASH_H264, RDKV_CERT_MVS_Video_HTML_SHAKA_PlayPause_HLS_H264

### MVS-REQ-010 — PlayPause stress testing (25 tests)

Lightning Video Player (21): RDKV_CERT_MVS_Video_PlayPause_STRESS_DASH_H264, RDKV_CERT_MVS_Video_PlayPause_STRESS_DASH_H264_Main, RDKV_CERT_MVS_Video_PlayPause_STRESS_HLS_H264, RDKV_CERT_MVS_Video_PlayPause_STRESS_HEVC, RDKV_CERT_MVS_Video_PlayPause_STRESS_HEVC_MKV, RDKV_CERT_MVS_Video_PlayPause_STRESS_HEVC_Main10, RDKV_CERT_MVS_Video_PlayPause_STRESS_MKV, RDKV_CERT_MVS_Video_PlayPause_STRESS_MP4, RDKV_CERT_MVS_Video_PlayPause_STRESS_AV1, RDKV_CERT_MVS_Video_PlayPause_STRESS_VP9, RDKV_CERT_MVS_Video_PlayPause_STRESS_EC3, RDKV_CERT_MVS_Video_PlayPause_STRESS_AAC, RDKV_CERT_MVS_Video_PlayPause_STRESS_HDR, RDKV_CERT_MVS_Video_PlayPause_STRESS_4K_AV1, RDKV_CERT_MVS_Video_PlayPause_STRESS_4K_DASH, RDKV_CERT_MVS_Video_PlayPause_STRESS_4K_HLS, RDKV_CERT_MVS_Video_PlayPause_STRESS_4K_VP9, RDKV_CERT_MVS_Video_PlayPause_STRESS_Audio_Only, RDKV_CERT_MVS_Video_PlayPause_STRESS_MPEG_TS, RDKV_CERT_MVS_Video_PlayPause_STRESS_Opus, RDKV_CERT_MVS_Video_PlayPause_STRESS_OGG

Lightning SHAKA Player (4): RDKV_CERT_MVS_Video_SHAKA_PlayPause_STRESS_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_PlayPause_STRESS_DASH_H264_Main, RDKV_CERT_MVS_Video_SHAKA_PlayPause_STRESS_HEVC_Main10, RDKV_CERT_MVS_Video_SHAKA_PlayPause_STRESS_HLS_H264

### MVS-REQ-011 — Mute and unmute audio (44 tests)

Lightning Video Player (17): RDKV_CERT_MVS_Video_Mute_UnMute_DASH_H264, RDKV_CERT_MVS_Video_Mute_UnMute_DASH_H264_Main, RDKV_CERT_MVS_Video_Mute_UnMute_HLS_H264, RDKV_CERT_MVS_Video_Mute_UnMute_HEVC, RDKV_CERT_MVS_Video_Mute_UnMute_HEVC_MKV, RDKV_CERT_MVS_Video_Mute_UnMute_HEVC_Main10, RDKV_CERT_MVS_Video_Mute_UnMute_MKV, RDKV_CERT_MVS_Video_Mute_UnMute_MP4, RDKV_CERT_MVS_Video_Mute_UnMute_AV1, RDKV_CERT_MVS_Video_Mute_UnMute_VP9, RDKV_CERT_MVS_Video_Mute_UnMute_EC3, RDKV_CERT_MVS_Video_Mute_UnMute_HDR, RDKV_CERT_MVS_Video_Mute_UnMute_4K_AV1, RDKV_CERT_MVS_Video_Mute_UnMute_4K_DASH, RDKV_CERT_MVS_Video_Mute_UnMute_4K_HLS, RDKV_CERT_MVS_Video_Mute_UnMute_4K_VP9, RDKV_CERT_MVS_Video_Mute_UnMute_Audio_Only

Lightning SHAKA Player (8): RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_DASH_H264_Main, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_HEVC, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_HEVC_Main10, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_HLS_H264, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_MKV, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_MP4, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_VP9

HTML5 native player (17): RDKV_CERT_MVS_Video_HTML_Mute_Unmute_AAC_H264_MP4, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_DASH_H264, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_DASH_HEVC, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_DASH_VP9, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_HLS_H264, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_HLS_HEVC, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_OPUS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Mute_Unmute_VORBIS_VP9_WEBM

HTML5 Shaka.js player (2): RDKV_CERT_MVS_Video_HTML_SHAKA_Mute_Unmute_DASH_H264, RDKV_CERT_MVS_Video_HTML_SHAKA_Mute_Unmute_HLS_H264

### MVS-REQ-012 — Mute/unmute audio stress testing (20 tests)

Lightning Video Player (16): RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_DASH_H264, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_DASH_H264_Main, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_HLS_H264, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_HEVC, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_HEVC_Main10, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_MKV, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_MP4, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_AV1, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_VP9, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_EC3, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_HDR, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_4K_AV1, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_4K_DASH, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_4K_HLS, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_4K_VP9, RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_Audio_Only

Lightning SHAKA Player (4): RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_STRESS_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_STRESS_DASH_H264_Main, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_STRESS_HEVC_Main10, RDKV_CERT_MVS_Video_SHAKA_Mute_UnMute_STRESS_HLS_H264

### MVS-REQ-013 — Fast-forward at 2×, 3×, and 4× rates (94 tests)

Lightning Video Player FF2x (15): RDKV_CERT_MVS_Video_FF2X_Play_4K_AV1, RDKV_CERT_MVS_Video_FF2X_Play_4K_DASH, RDKV_CERT_MVS_Video_FF2X_Play_4K_HLS, RDKV_CERT_MVS_Video_FF2X_Play_4K_VP9, RDKV_CERT_MVS_Video_FF2X_Play_AV1, RDKV_CERT_MVS_Video_FF2X_Play_DASH_H264, RDKV_CERT_MVS_Video_FF2X_Play_DASH_H264_Main, RDKV_CERT_MVS_Video_FF2X_Play_EC3, RDKV_CERT_MVS_Video_FF2X_Play_HDR, RDKV_CERT_MVS_Video_FF2X_Play_HEVC, RDKV_CERT_MVS_Video_FF2X_Play_HEVC_MKV, RDKV_CERT_MVS_Video_FF2X_Play_HLS_H264, RDKV_CERT_MVS_Video_FF2X_Play_MKV, RDKV_CERT_MVS_Video_FF2X_Play_MP4, RDKV_CERT_MVS_Video_FF2X_Play_VP9

Lightning Video Player FF3x (15): RDKV_CERT_MVS_Video_FF3X_Play_4K_AV1, RDKV_CERT_MVS_Video_FF3X_Play_4K_DASH, RDKV_CERT_MVS_Video_FF3X_Play_4K_HLS, RDKV_CERT_MVS_Video_FF3X_Play_4K_VP9, RDKV_CERT_MVS_Video_FF3X_Play_AV1, RDKV_CERT_MVS_Video_FF3X_Play_DASH_H264, RDKV_CERT_MVS_Video_FF3X_Play_DASH_H264_Main, RDKV_CERT_MVS_Video_FF3X_Play_EC3, RDKV_CERT_MVS_Video_FF3X_Play_HDR, RDKV_CERT_MVS_Video_FF3X_Play_HEVC, RDKV_CERT_MVS_Video_FF3X_Play_HEVC_MKV, RDKV_CERT_MVS_Video_FF3X_Play_HLS_H264, RDKV_CERT_MVS_Video_FF3X_Play_MKV, RDKV_CERT_MVS_Video_FF3X_Play_MP4, RDKV_CERT_MVS_Video_FF3X_Play_VP9

Lightning Video Player FF4x (12): RDKV_CERT_MVS_Video_FF4X_Play_4K_DASH, RDKV_CERT_MVS_Video_FF4X_Play_4K_HLS, RDKV_CERT_MVS_Video_FF4X_Play_4K_VP9, RDKV_CERT_MVS_Video_FF4X_Play_AV1, RDKV_CERT_MVS_Video_FF4X_Play_DASH_H264, RDKV_CERT_MVS_Video_FF4X_Play_DASH_H264_Main, RDKV_CERT_MVS_Video_FF4X_Play_EC3, RDKV_CERT_MVS_Video_FF4X_Play_HEVC, RDKV_CERT_MVS_Video_FF4X_Play_HLS_H264, RDKV_CERT_MVS_Video_FF4X_Play_MKV, RDKV_CERT_MVS_Video_FF4X_Play_MP4, RDKV_CERT_MVS_Video_FF4X_Play_VP9

Lightning SHAKA Player FF2x (3): RDKV_CERT_MVS_Video_SHAKA_FF2X_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_FF2X_HLS_H264, RDKV_CERT_MVS_Video_SHAKA_FF2X_Play_DASH_H264_Main

Lightning SHAKA Player FF3x (3): RDKV_CERT_MVS_Video_SHAKA_FF3X_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_FF3X_HLS_H264, RDKV_CERT_MVS_Video_SHAKA_FF3X_Play_DASH_H264_Main

Lightning SHAKA Player FF4x (3): RDKV_CERT_MVS_Video_SHAKA_FF4X_Play_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_FF4X_Play_DASH_H264_Main, RDKV_CERT_MVS_Video_SHAKA_FF4X_Play_HLS_H264

HTML5 native player FF2x (17): RDKV_CERT_MVS_Video_HTML_FF2X_Play_AAC_H264_MP4, RDKV_CERT_MVS_Video_HTML_FF2X_Play_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_FF2X_Play_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_FF2X_Play_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_FF2X_Play_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_FF2X_Play_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_FF2X_Play_DASH_H264, RDKV_CERT_MVS_Video_HTML_FF2X_Play_DASH_HEVC, RDKV_CERT_MVS_Video_HTML_FF2X_Play_DASH_VP9, RDKV_CERT_MVS_Video_HTML_FF2X_Play_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_FF2X_Play_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_FF2X_Play_HLS_H264, RDKV_CERT_MVS_Video_HTML_FF2X_Play_HLS_HEVC, RDKV_CERT_MVS_Video_HTML_FF2X_Play_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_FF2X_Play_OPUS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_FF2X_Play_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_FF2X_Play_VORBIS_VP9_WEBM

HTML5 native player FF3x (12): RDKV_CERT_MVS_Video_HTML_FF3X_Play_AAC_H264_MP4, RDKV_CERT_MVS_Video_HTML_FF3X_Play_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_FF3X_Play_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_FF3X_Play_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_FF3X_Play_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_FF3X_Play_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_FF3X_Play_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_FF3X_Play_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_FF3X_Play_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_FF3X_Play_OPUS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_FF3X_Play_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_FF3X_Play_VORBIS_VP9_WEBM

HTML5 native player FF4x (12): RDKV_CERT_MVS_Video_HTML_FF4X_Play_AAC_H264_MP4, RDKV_CERT_MVS_Video_HTML_FF4X_Play_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_FF4X_Play_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_FF4X_Play_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_FF4X_Play_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_FF4X_Play_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_FF4X_Play_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_FF4X_Play_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_FF4X_Play_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_FF4X_Play_OPUS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_FF4X_Play_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_FF4X_Play_VORBIS_VP9_WEBM

HTML5 Shaka.js player FF2x (2): RDKV_CERT_MVS_Video_HTML_SHAKA_FF2X_Play_DASH_H264, RDKV_CERT_MVS_Video_HTML_SHAKA_FF2X_Play_HLS_H264

### MVS-REQ-014 — Fast-forward stress testing (12 tests)

Lightning Video Player (10): RDKV_CERT_MVS_Video_FF_STRESS_4K_DASH, RDKV_CERT_MVS_Video_FF_STRESS_4K_HLS, RDKV_CERT_MVS_Video_FF_STRESS_4K_VP9, RDKV_CERT_MVS_Video_FF_STRESS_AV1, RDKV_CERT_MVS_Video_FF_STRESS_DASH_H264, RDKV_CERT_MVS_Video_FF_STRESS_EC3, RDKV_CERT_MVS_Video_FF_STRESS_HEVC, RDKV_CERT_MVS_Video_FF_STRESS_HLS_H264, RDKV_CERT_MVS_Video_FF_STRESS_MKV, RDKV_CERT_MVS_Video_FF_STRESS_VP9

Lightning SHAKA Player (2): RDKV_CERT_MVS_Video_SHAKA_FF_STRESS_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_FF_STRESS_HLS_H264

### MVS-REQ-015 — Seek operations (88 tests)

Lightning Video Player — Seek to position (13): RDKV_CERT_MVS_Video_Seek_Pos_4K_AV1, RDKV_CERT_MVS_Video_Seek_Pos_4K_DASH, RDKV_CERT_MVS_Video_Seek_Pos_4K_HLS, RDKV_CERT_MVS_Video_Seek_Pos_4K_VP9, RDKV_CERT_MVS_Video_Seek_Pos_AV1, RDKV_CERT_MVS_Video_Seek_Pos_DASH_H264, RDKV_CERT_MVS_Video_Seek_Pos_DASH_H264_Main, RDKV_CERT_MVS_Video_Seek_Pos_EC3, RDKV_CERT_MVS_Video_Seek_Pos_HEVC, RDKV_CERT_MVS_Video_Seek_Pos_HEVC_MKV, RDKV_CERT_MVS_Video_Seek_Pos_HLS_H264, RDKV_CERT_MVS_Video_Seek_Pos_MKV, RDKV_CERT_MVS_Video_Seek_Pos_VP9

Lightning Video Player — Seek during FF (12): RDKV_CERT_MVS_Video_Seek_FF_4K_AV1, RDKV_CERT_MVS_Video_Seek_FF_4K_DASH, RDKV_CERT_MVS_Video_Seek_FF_4K_HLS, RDKV_CERT_MVS_Video_Seek_FF_4K_VP9, RDKV_CERT_MVS_Video_Seek_FF_AV1, RDKV_CERT_MVS_Video_Seek_FF_DASH_H264, RDKV_CERT_MVS_Video_Seek_FF_DASH_H264_Main, RDKV_CERT_MVS_Video_Seek_FF_EC3, RDKV_CERT_MVS_Video_Seek_FF_HEVC, RDKV_CERT_MVS_Video_Seek_FF_HLS_H264, RDKV_CERT_MVS_Video_Seek_FF_MKV, RDKV_CERT_MVS_Video_Seek_FF_VP9

Lightning SHAKA Player — Seek to position (3): RDKV_CERT_MVS_Video_SHAKA_Seek_Pos_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Seek_Pos_DASH_H264_Main, RDKV_CERT_MVS_Video_SHAKA_Seek_Pos_HLS_H264

Lightning SHAKA Player — Seek during FF (3): RDKV_CERT_MVS_Video_SHAKA_Seek_FF_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Seek_FF_DASH_H264_Main, RDKV_CERT_MVS_Video_SHAKA_Seek_FF_HLS_H264

HTML5 native player — Seek forward (17): RDKV_CERT_MVS_Video_HTML_Seek_FWD_AAC_H264_MP4, RDKV_CERT_MVS_Video_HTML_Seek_FWD_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_Seek_FWD_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_Seek_FWD_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_Seek_FWD_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_FWD_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_FWD_DASH_H264, RDKV_CERT_MVS_Video_HTML_Seek_FWD_DASH_HEVC, RDKV_CERT_MVS_Video_HTML_Seek_FWD_DASH_VP9, RDKV_CERT_MVS_Video_HTML_Seek_FWD_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_Seek_FWD_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_Seek_FWD_HLS_H264, RDKV_CERT_MVS_Video_HTML_Seek_FWD_HLS_HEVC, RDKV_CERT_MVS_Video_HTML_Seek_FWD_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_FWD_OPUS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_FWD_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_FWD_VORBIS_VP9_WEBM

HTML5 native player — Seek backward (17): RDKV_CERT_MVS_Video_HTML_Seek_BWD_AAC_H264_MP4, RDKV_CERT_MVS_Video_HTML_Seek_BWD_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_Seek_BWD_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_Seek_BWD_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_Seek_BWD_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_BWD_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_BWD_DASH_H264, RDKV_CERT_MVS_Video_HTML_Seek_BWD_DASH_HEVC, RDKV_CERT_MVS_Video_HTML_Seek_BWD_DASH_VP9, RDKV_CERT_MVS_Video_HTML_Seek_BWD_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_Seek_BWD_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_Seek_BWD_HLS_H264, RDKV_CERT_MVS_Video_HTML_Seek_BWD_HLS_HEVC, RDKV_CERT_MVS_Video_HTML_Seek_BWD_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_BWD_OPUS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_BWD_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_BWD_VORBIS_VP9_WEBM

HTML5 native player — Seek to position (17): RDKV_CERT_MVS_Video_HTML_Seek_Pos_AAC_H264_MP4, RDKV_CERT_MVS_Video_HTML_Seek_Pos_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_Seek_Pos_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_Seek_Pos_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_Seek_Pos_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_Pos_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_Pos_DASH_H264, RDKV_CERT_MVS_Video_HTML_Seek_Pos_DASH_HEVC, RDKV_CERT_MVS_Video_HTML_Seek_Pos_DASH_VP9, RDKV_CERT_MVS_Video_HTML_Seek_Pos_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_Seek_Pos_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_Seek_Pos_HLS_H264, RDKV_CERT_MVS_Video_HTML_Seek_Pos_HLS_HEVC, RDKV_CERT_MVS_Video_HTML_Seek_Pos_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_Pos_OPUS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_Pos_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Seek_Pos_VORBIS_VP9_WEBM

HTML5 Shaka.js player — Seek (6): RDKV_CERT_MVS_Video_HTML_SHAKA_Seek_BWD_DASH_H264, RDKV_CERT_MVS_Video_HTML_SHAKA_Seek_BWD_HLS_H264, RDKV_CERT_MVS_Video_HTML_SHAKA_Seek_FWD_DASH_H264, RDKV_CERT_MVS_Video_HTML_SHAKA_Seek_FWD_HLS_H264, RDKV_CERT_MVS_Video_HTML_SHAKA_Seek_Pos_DASH_H264, RDKV_CERT_MVS_Video_HTML_SHAKA_Seek_Pos_HLS_H264

### MVS-REQ-016 — Seek stress testing (24 tests)

Lightning Video Player — Forward seek stress (10): RDKV_CERT_MVS_Video_Seek_FWD_STRESS_4K_DASH, RDKV_CERT_MVS_Video_Seek_FWD_STRESS_4K_HLS, RDKV_CERT_MVS_Video_Seek_FWD_STRESS_4K_VP9, RDKV_CERT_MVS_Video_Seek_FWD_STRESS_AV1, RDKV_CERT_MVS_Video_Seek_FWD_STRESS_DASH_H264, RDKV_CERT_MVS_Video_Seek_FWD_STRESS_EC3, RDKV_CERT_MVS_Video_Seek_FWD_STRESS_HEVC, RDKV_CERT_MVS_Video_Seek_FWD_STRESS_HLS_H264, RDKV_CERT_MVS_Video_Seek_FWD_STRESS_MKV, RDKV_CERT_MVS_Video_Seek_FWD_STRESS_VP9

Lightning Video Player — Backward seek stress (10): RDKV_CERT_MVS_Video_Seek_BWD_STRESS_4K_DASH, RDKV_CERT_MVS_Video_Seek_BWD_STRESS_4K_HLS, RDKV_CERT_MVS_Video_Seek_BWD_STRESS_4K_VP9, RDKV_CERT_MVS_Video_Seek_BWD_STRESS_AV1, RDKV_CERT_MVS_Video_Seek_BWD_STRESS_DASH_H264, RDKV_CERT_MVS_Video_Seek_BWD_STRESS_EC3, RDKV_CERT_MVS_Video_Seek_BWD_STRESS_HEVC, RDKV_CERT_MVS_Video_Seek_BWD_STRESS_HLS_H264, RDKV_CERT_MVS_Video_Seek_BWD_STRESS_MKV, RDKV_CERT_MVS_Video_Seek_BWD_STRESS_VP9

Lightning SHAKA Player (4): RDKV_CERT_MVS_Video_SHAKA_Seek_FWD_STRESS_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Seek_FWD_STRESS_HLS_H264, RDKV_CERT_MVS_Video_SHAKA_Seek_BWD_STRESS_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Seek_BWD_STRESS_HLS_H264

### MVS-REQ-017 — Combined trick play sequence (15 tests)

Lightning Video Player (13): RDKV_CERT_MVS_Video_TrickPlay_4K_AV1, RDKV_CERT_MVS_Video_TrickPlay_4K_DASH, RDKV_CERT_MVS_Video_TrickPlay_4K_HLS, RDKV_CERT_MVS_Video_TrickPlay_4K_VP9, RDKV_CERT_MVS_Video_TrickPlay_AV1, RDKV_CERT_MVS_Video_TrickPlay_DASH_H264, RDKV_CERT_MVS_Video_TrickPlay_EC3, RDKV_CERT_MVS_Video_TrickPlay_HDR, RDKV_CERT_MVS_Video_TrickPlay_HEVC, RDKV_CERT_MVS_Video_TrickPlay_HEVC_MKV, RDKV_CERT_MVS_Video_TrickPlay_HLS_H264, RDKV_CERT_MVS_Video_TrickPlay_MKV, RDKV_CERT_MVS_Video_TrickPlay_VP9

Lightning SHAKA Player (2): RDKV_CERT_MVS_Video_SHAKA_TrickPlay_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_TrickPlay_HLS_H264

### MVS-REQ-018 — Loop play — continuous content looping (15 tests)

Lightning Video Player (13): RDKV_CERT_MVS_Video_Loop_Play_4K_AV1, RDKV_CERT_MVS_Video_Loop_Play_4K_DASH, RDKV_CERT_MVS_Video_Loop_Play_4K_VP9, RDKV_CERT_MVS_Video_Loop_Play_AV1, RDKV_CERT_MVS_Video_Loop_Play_Audio_Only, RDKV_CERT_MVS_Video_Loop_Play_DASH_H264, RDKV_CERT_MVS_Video_Loop_Play_EC3, RDKV_CERT_MVS_Video_Loop_Play_HEVC, RDKV_CERT_MVS_Video_Loop_Play_HEVC_MKV, RDKV_CERT_MVS_Video_Loop_Play_HLS_H264, RDKV_CERT_MVS_Video_Loop_Play_MKV, RDKV_CERT_MVS_Video_Loop_Play_MP4, RDKV_CERT_MVS_Video_Loop_Play_VP9

Lightning SHAKA Player (2): RDKV_CERT_MVS_Video_SHAKA_Loop_Play_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Loop_Play_HLS_H264

### MVS-REQ-019 — Audio volume control (12 tests)

HTML5 native player (12): RDKV_CERT_MVS_Video_HTML_Setvolume_AAC_H264_MP4, RDKV_CERT_MVS_Video_HTML_Setvolume_AAC_H265_MP4, RDKV_CERT_MVS_Video_HTML_Setvolume_AC3_H265_MP4, RDKV_CERT_MVS_Video_HTML_Setvolume_AV1_AAC_MP4, RDKV_CERT_MVS_Video_HTML_Setvolume_AV1_OPUS_WEBM, RDKV_CERT_MVS_Video_HTML_Setvolume_AV1_VORBIS_WEBM, RDKV_CERT_MVS_Video_HTML_Setvolume_H264_AC3_MP4, RDKV_CERT_MVS_Video_HTML_Setvolume_H264_MP3_MP4, RDKV_CERT_MVS_Video_HTML_Setvolume_OPUS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Setvolume_OPUS_VP9_WEBM, RDKV_CERT_MVS_Video_HTML_Setvolume_VORBIS_VP8_WEBM, RDKV_CERT_MVS_Video_HTML_Setvolume_VORBIS_VP9_WEBM

### MVS-REQ-020 — Widevine DRM content protection (34 tests)

Lightning Video Player — CTR, Clear Lead, Crypt-Skip, MultiKey (29): RDKV_CERT_MVS_Video_Play_Widevine_DASH_AAC, RDKV_CERT_MVS_Video_Play_Widevine_DASH_AV1, RDKV_CERT_MVS_Video_Play_Widevine_DASH_EC3, RDKV_CERT_MVS_Video_Play_Widevine_DASH_H264, RDKV_CERT_MVS_Video_Play_Widevine_DASH_HEVC, RDKV_CERT_MVS_Video_Play_Widevine_DASH_OPUS, RDKV_CERT_MVS_Video_Play_Widevine_DASH_VP8, RDKV_CERT_MVS_Video_Play_Widevine_DASH_VP9, RDKV_CERT_MVS_Video_Play_Widevine_HLS_AAC, RDKV_CERT_MVS_Video_Play_Widevine_HLS_H264, RDKV_CERT_MVS_Video_Play_Widevine_HLS_HEVC, RDKV_CERT_MVS_Video_Play_Widevine_MultiKey_DASH, RDKV_CERT_MVS_Video_Play_Widevine_MultiKey_HLS, RDKV_CERT_MVS_Video_Play_Widevine_Clear_Lead_DASH_AAC, RDKV_CERT_MVS_Video_Play_Widevine_Clear_Lead_DASH_AC3, RDKV_CERT_MVS_Video_Play_Widevine_Clear_Lead_DASH_AV1, RDKV_CERT_MVS_Video_Play_Widevine_Clear_Lead_DASH_EC3, RDKV_CERT_MVS_Video_Play_Widevine_Clear_Lead_DASH_HEVC_AAC, RDKV_CERT_MVS_Video_Play_Widevine_Clear_Lead_DASH_VP9, RDKV_CERT_MVS_Video_Play_Widevine_Clear_Lead_HLS_H264, RDKV_CERT_MVS_Video_Play_Widevine_Clear_Lead_HLS_HEVC, RDKV_CERT_MVS_Video_Play_Widevine_Cypt_Skip_Byte_Block_DASH_AAC, RDKV_CERT_MVS_Video_Play_Widevine_Cypt_Skip_Byte_Block_DASH_AC3, RDKV_CERT_MVS_Video_Play_Widevine_Cypt_Skip_Byte_Block_DASH_AV1, RDKV_CERT_MVS_Video_Play_Widevine_Cypt_Skip_Byte_Block_DASH_EC3, RDKV_CERT_MVS_Video_Play_Widevine_Cypt_Skip_Byte_Block_DASH_HEVC_AAC, RDKV_CERT_MVS_Video_Play_Widevine_Cypt_Skip_Byte_Block_DASH_VP9_OPUS, RDKV_CERT_MVS_Video_Play_Widevine_Cypt_Skip_Byte_Block_HLS_H264_AAC, RDKV_CERT_MVS_Video_Play_Widevine_Cypt_Skip_Byte_Block_HLS_HEVC_AAC

Lightning SHAKA Player (5): RDKV_CERT_MVS_Video_SHAKA_Play_Widevine_DASH_EC3, RDKV_CERT_MVS_Video_SHAKA_Play_Widevine_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Play_Widevine_HLS_AAC, RDKV_CERT_MVS_Video_SHAKA_Play_Widevine_HLS_H264, RDKV_CERT_MVS_Video_SHAKA_Play_Widevine_HLS_HEVC

### MVS-REQ-021 — Widevine CBCS content encryption (8 tests)

Lightning Video Player (8): RDKV_CERT_MVS_Video_Play_Widevine_CBCS_DASH, RDKV_CERT_MVS_Video_Play_Widevine_CBCS_DASH_AC3, RDKV_CERT_MVS_Video_Play_Widevine_CBCS_DASH_AV1, RDKV_CERT_MVS_Video_Play_Widevine_CBCS_DASH_EC3, RDKV_CERT_MVS_Video_Play_Widevine_CBCS_DASH_HEVC, RDKV_CERT_MVS_Video_Play_Widevine_CBCS_DASH_VP9, RDKV_CERT_MVS_Video_Play_Widevine_CBCS_HLS, RDKV_CERT_MVS_Video_Play_Widevine_CBCS_HLS_HEVC

### MVS-REQ-022 — PlayReady DRM content protection (23 tests)

Lightning Video Player (15): RDKV_CERT_MVS_Video_Play_PlayReady_CBCS_DASH, RDKV_CERT_MVS_Video_Play_PlayReady_CBCS_DASH_AV1, RDKV_CERT_MVS_Video_Play_PlayReady_CBCS_HLS, RDKV_CERT_MVS_Video_Play_PlayReady_DASH_AAC, RDKV_CERT_MVS_Video_Play_PlayReady_DASH_AV1, RDKV_CERT_MVS_Video_Play_PlayReady_DASH_EC3, RDKV_CERT_MVS_Video_Play_PlayReady_DASH_H264, RDKV_CERT_MVS_Video_Play_PlayReady_DASH_HEVC, RDKV_CERT_MVS_Video_Play_PlayReady_HLS_AAC, RDKV_CERT_MVS_Video_Play_PlayReady_HLS_H264, RDKV_CERT_MVS_Video_Play_PlayReady_HLS_HEVC, RDKV_CERT_MVS_Video_Play_PlayReady_MultiKey_DASH, RDKV_CERT_MVS_Video_Play_PlayReady_MultiKey_HLS, RDKV_CERT_MVS_Video_TrickPlay_PlayReady_DASH_H264, RDKV_CERT_MVS_Video_TrickPlay_PlayReady_HLS_H264

Lightning SHAKA Player (8): RDKV_CERT_MVS_Video_SHAKA_Play_PlayReady_CBCS_DASH, RDKV_CERT_MVS_Video_SHAKA_Play_PlayReady_DASH_AAC, RDKV_CERT_MVS_Video_SHAKA_Play_PlayReady_DASH_AV1, RDKV_CERT_MVS_Video_SHAKA_Play_PlayReady_DASH_EC3, RDKV_CERT_MVS_Video_SHAKA_Play_PlayReady_DASH_H264, RDKV_CERT_MVS_Video_SHAKA_Play_PlayReady_HLS_AAC, RDKV_CERT_MVS_Video_SHAKA_Play_PlayReady_HLS_H264, RDKV_CERT_MVS_Video_SHAKA_TrickPlay_PlayReady_HLS_H264

### MVS-REQ-023 — Animation rendering performance (11 tests)

Animation app (11): RDKV_CERT_MVS_Animation_Average_Device_CPULoad, RDKV_CERT_MVS_Animation_Average_FPS, RDKV_CERT_MVS_Animation_Check_Graphics_workload, RDKV_CERT_MVS_Animation_Complex_Average_FPS, RDKV_CERT_MVS_Animation_Object_Compare_ScreenShots, RDKV_CERT_MVS_Animation_Objects_Average_FPS, RDKV_CERT_MVS_Animation_Operations, RDKV_CERT_MVS_Animation_PlayPause_STRESS, RDKV_CERT_MVS_Animation_Simple_Average_FPS, RDKV_CERT_MVS_Animation_StartStop_STRESS, RDKV_CERT_MVS_Animation_Texts_Average_FPS

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `MVS-REQ-001` | SHALL decode and render video and audio content including H.264, HEVC (MKV/Main10), MKV, MP4, MPEG, MPEG-TS, H.263, VP8, VP9, AV1, EC3, HDR, Vorbis, OPUS, AC3, MP3, and WebM formats, emitting a playing event within the configured playback duration without playback error. |
| `MVS-REQ-002` | SHALL decode and render 4K UHD content — AV1, DASH, and HLS streams — without playback error. |
| `MVS-REQ-003` | SHALL establish and sustain live DASH and live HLS stream playback, emitting a playing event and maintaining continuous playback for the configured duration without buffering failure. |
| `MVS-REQ-004` | SHALL decode and render audio-only streams including AAC, DTS, M4A, MP3, OGG, Opus, and WAV PCM without playback error or audio discontinuity. |
| `MVS-REQ-005` | SHALL parse and play MPEG-DASH streams that use SegmentBase, SegmentList, SegmentTemplate, and SegmentTimeline segment addressing formats without segment retrieval error or playback failure. |
| `MVS-REQ-006` | SHALL decode and render DASH and HLS streams at 480i, 480p, 720p, 1080i, and 1080p resolution tiers without playback error. |
| `MVS-REQ-007` | SHALL select and output Atmos, Dolby Digital, and Stereo audio sound modes for DASH content without audio output error or incorrect mode application. |
| `MVS-REQ-008` | SHALL play DASH H.264, HLS H.264, HEVC (MKV), MKV, MP4, AV1, VP9, EC3, 4K, and audio-only content from start to natural end-of-stream, completing the full asset duration without playback error or premature termination. |
| `MVS-REQ-009` | SHALL pause playback and resume from the paused position for H.264, HEVC (MKV/Main10), MKV, MP4, AV1, VP9, EC3, AAC, HDR, 4K, MPEG-TS, Opus, OGG, DASH, HLS, WebM, Vorbis, AC3, and MP3 content across resolutions from 480p to 4K, resuming from the correct position without error. |
| `MVS-REQ-010` | SHOULD sustain repeated PlayPause cycles across all supported codec and container combinations under stress conditions without playback instability or resource exhaustion. |
| `MVS-REQ-011` | SHALL mute and unmute audio output during active playback of H.264, HEVC (MKV/Main10), MKV, MP4, AV1, VP9, EC3, HDR, 4K, DASH, HLS, WebM, Vorbis, OPUS, and AC3 content without playback error or residual audio after mute. |
| `MVS-REQ-012` | SHOULD sustain repeated mute and unmute audio operations under stress conditions without playback instability or resource exhaustion. |
| `MVS-REQ-013` | SHALL execute fast-forward at 2×, 3×, and 4× playback rates for H.264, HEVC (MKV), AV1, VP9, MKV, MP4, EC3, HDR, 4K, DASH, HLS, WebM, Vorbis, OPUS, and AC3 content without playback error or incorrect rate application. |
| `MVS-REQ-014` | SHOULD sustain repeated fast-forward trick play operations across DASH, HLS, HEVC, AV1, VP9, MKV, EC3, and 4K content under stress conditions without playback instability. |
| `MVS-REQ-015` | SHALL seek to an absolute position, seek while in fast-forward mode, and seek forward and backward for H.264, HEVC (MKV), AV1, VP9, MKV, EC3, 4K, DASH, HLS, WebM, Vorbis, OPUS, and AC3 content, resuming from the correct position without playback error. |
| `MVS-REQ-016` | SHOULD sustain repeated forward and backward seek operations under stress conditions for DASH, HLS, HEVC, AV1, VP9, MKV, EC3, and 4K content without playback instability or state corruption. |
| `MVS-REQ-017` | SHALL execute the complete trick play sequence — fast-forward, rewind, and pause-resume — for DASH H.264, HLS H.264, HEVC (MKV), AV1, VP9, MKV, EC3, HDR, and 4K content without playback error. |
| `MVS-REQ-018` | SHOULD play DASH H.264, HLS H.264, HEVC (MKV), AV1, VP9, MKV, MP4, EC3, 4K, and audio-only content in continuous loop mode without playback error or resource leak between iterations. |
| `MVS-REQ-019` | SHALL set audio volume to a specified level during active playback of H.264, HEVC, AV1, VP9, WebM, Vorbis, OPUS, AC3, and MP3 content without audio artefact or playback error. |
| `MVS-REQ-020` | SHALL decrypt and play Widevine CTR-encrypted DASH and HLS content covering AAC, AC3, EC3, AV1, HEVC, OPUS, VP8, VP9, and H.264 codecs, including clear-lead, crypt-skip-byte-block, and multi-key variants, without decryption failure or licence acquisition error. |
| `MVS-REQ-021` | SHALL decrypt and play Widevine CBCS-encrypted DASH and HLS content covering HEVC, VP9, AV1, AC3, EC3, and H.264 codecs without decryption failure. |
| `MVS-REQ-022` | SHALL decrypt and play PlayReady CTR and CBCS-encrypted DASH and HLS content covering AAC, EC3, AV1, HEVC, H.264 codecs and multi-key streams — including trick play over PlayReady-protected content — without decryption failure or licence acquisition error. |
| `MVS-REQ-023` | SHOULD render Lightning animation scenes including simple, text, object, and complex animation types and validate that average FPS, CPU load, graphics workload, and visual frame accuracy meet expected thresholds — including under PlayPause and start/stop stress conditions. |
