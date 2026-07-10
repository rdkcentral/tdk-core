# Device Settings Audio Port — Requirements

> **Module:** Device Settings Audio Port HAL (`dsAudio`) | **Req ID Prefix:** `VTS-DSAUDIO`
> **Total requirements:** 8 | **Total test cases:** 158 (134 L1 + 24 L2)

> **Note — Classification corrections applied:** `dsIsAudioMSDecode_pos`, `dsIsAudioMS12Decode_pos`, and L2 tests `GetAudioCapabilities`, `CheckMS12DecodeSupport`, `CheckMS11DecodeSupport` are classified as **Profile Compliance** (not Functional) because their L2 tests explicitly compare returned values against the device profile.

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** of the `dsAudio` HAL interface.
The module provides initialization/termination lifecycle, read-only port and capability queries,
paired Set/Get APIs for MS12 audio enhancement settings, port state/level/stereo control,
audio mixing and language configuration, capability compliance against the device profile,
and ARC/eARC plus MS12 profile management.

Positive L1 tests validate individual API correctness in isolation. L2 tests validate
end-to-end workflows. For requirements where L2 tests perform Set→Get→verify sequences,
the classification is **Data Integrity**. For requirements covering only read-only APIs or
registration calls, the classification is **Functional** or **Profile Compliance**.
All negative L1 tests are consolidated into a single **Error Handling** requirement.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| VTS-DSAUDIO-001 | dsAudio sub-system initialization and termination lifecycle | Lifecycle | 2 |
| VTS-DSAUDIO-002 | Audio port handle retrieval, format and connection queries, and event callback registration | Functional | 7 |
| VTS-DSAUDIO-003 | MS12 audio enhancement settings — compression, dialog, Dolby, IEQ, volume leveller, bass, surround, DRC, surround virtualizer, MI steering, graphic EQ, and LE config | Data Integrity | 36 |
| VTS-DSAUDIO-004 | Port enable/disable, audio mute, gain, level, delay, ATMOS output mode, and stereo configuration | Data Integrity | 20 |
| VTS-DSAUDIO-005 | Associated audio mixing, fader control, audio mixer levels, and AC4 language configuration | Data Integrity | 12 |
| VTS-DSAUDIO-006 | Audio and MS12 capabilities, and MS11/MS12 decode support compliance against device profile | Profile Compliance | 8 |
| VTS-DSAUDIO-007 | ARC/eARC management, Short Audio Descriptor configuration, and MS12 audio profile selection | Functional | 6 |
| VTS-DSAUDIO-008 | API error handling — not-initialized, already-initialized, and invalid-argument conditions | Error Handling | 67 |
| | **Total** | | **158** |

---

### VTS-DSAUDIO-001 — dsAudio sub-system initialization and termination lifecycle (2 tests)

L1 positive (2): dsAudioPortInit_pos, dsAudioPortTerm_pos

---

### VTS-DSAUDIO-002 — Audio port handle retrieval, format and connection queries, and event callback registration (7 tests)

L1 positive (7): dsGetAudioPort_pos, dsGetAudioFormat_pos, dsGetSinkDeviceAtmosCap_pos, dsAudioOutIsConn_pos, dsAudioOutRegConnCB_pos, dsAudioFmtUpdateRegCB_pos, dsAudioAtmosCapsRegCB_pos

> **Note:** `dsIsAudioMSDecode_pos`, `dsIsAudioMS12Decode_pos` and the `GetAudioCapabilities` L2 test moved to VTS-DSAUDIO-006 (Profile Compliance) because their L2 tests compare returned values against the device profile.

---

### VTS-DSAUDIO-003 — MS12 audio enhancement settings (36 tests)

L1 positive (24): dsGetAudioCompression_pos, dsSetAudioCompression_pos, dsGetDialogEnhance_pos, dsSetDialogEnhance_pos, dsGetDolbyVolumeMode_pos, dsSetDolbyVolumeMode_pos, dsGetIntelliEqMode_pos, dsSetIntelliEqMode_pos, dsGetVolumeLeveller_pos, dsSetVolumeLeveller_pos, dsGetBassEnhancer_pos, dsSetBassEnhancer_pos, dsIsSurroundDecoderEnabled_pos, dsEnableSurroundDecoder_pos, dsGetDRCMode_pos, dsSetDRCMode_pos, dsGetSurroundVirt_pos, dsSetSurroundVirt_pos, dsGetMISteering_pos, dsSetMISteering_pos, dsGetGraphicEqMode_pos, dsSetGraphicEqMode_pos, dsEnableLEConfig_pos, dsGetLEConfig_pos

L2 (12): SetAndGetAudioCompression, SetAndGetDialogEnhancement, SetAndGetDolbyVolumeMode, SetAndGetIntelligentEqualizerMode, SetAndGetVolumeLeveller, SetAndGetBassEnhancer, EnableAndVerifySurroundDecoder, SetAndGetDRCMode, SetAndGetSurroundVirtualizer, SetAndGetMISteering, SetAndGetGraphicEqualizerMode, EnableDisableAndRetrieveLEConfig

---

### VTS-DSAUDIO-004 — Port enable/disable, audio mute, gain, level, delay, ATMOS output mode, and stereo configuration (20 tests)

L1 positive (15): dsIsAudioPortEnabled_pos, dsEnableAudioPort_pos, dsIsAudioMute_pos, dsSetAudioMute_pos, dsGetAudioGain_pos, dsSetAudioGain_pos, dsGetAudioLevel_pos, dsSetAudioLevel_pos, dsGetAudioDelay_pos, dsSetAudioDelay_pos, dsSetAudioAtmosOutMode_pos, dsGetStereoMode_pos, dsSetStereoMode_pos, dsGetStereoAuto_pos, dsSetStereoAuto_pos

L2 (5): EnableDisableVerifyPortStatus, AudioMuteVerification, SetAndGetAudioDelay, SetAndGetStereoMode, AudioPortControl

---

### VTS-DSAUDIO-005 — Associated audio mixing, fader control, audio mixer levels, and AC4 language configuration (12 tests)

L1 positive (9): dsSetAssocAudioMixing_pos, dsGetAssocAudioMixing_pos, dsSetFaderControl_pos, dsGetFaderControl_pos, dsSetAudioMixLevels_pos, dsSetPrimaryLang_pos, dsGetPrimaryLang_pos, dsSetSecondaryLang_pos, dsGetSecondaryLang_pos

L2 (3): EnableDisableRetrieveAudioMixing, SetAndGetPrimaryLanguage, SetAndGetSecondaryLanguage

---

### VTS-DSAUDIO-006 — Audio and MS12 capabilities, and MS11/MS12 decode support compliance against device profile (8 tests)

L1 positive (4): dsGetAudioCaps_pos, dsGetMS12Caps_pos, dsIsAudioMSDecode_pos, dsIsAudioMS12Decode_pos

L2 (4): GetAndVerifyMS12Capabilities, GetAudioCapabilities, CheckMS12DecodeSupport, CheckMS11DecodeSupport

---

### VTS-DSAUDIO-007 — ARC/eARC management, Short Audio Descriptor configuration, and MS12 audio profile selection (6 tests)

L1 positive (6): dsGetMS12AudioProfList_pos, dsGetMS12AudioProf_pos, dsSetMS12AudioProf_pos, dsGetSupportedARCTypes_pos, dsAudioSetSAD_pos, dsAudioEnableARC_pos

> **Note:** `CheckMS12DecodeSupport` and `CheckMS11DecodeSupport` L2 tests moved to VTS-DSAUDIO-006 (Profile Compliance) because they compare against the device profile.

---

### VTS-DSAUDIO-008 — API error handling (67 tests)

L1 negative (67): dsAudioPortInit_neg, dsAudioPortTerm_neg, dsGetAudioPort_neg, dsGetAudioFormat_neg, dsGetAudioCompression_neg, dsSetAudioCompression_neg, dsGetDialogEnhance_neg, dsSetDialogEnhance_neg, dsGetDolbyVolumeMode_neg, dsSetDolbyVolumeMode_neg, dsGetIntelliEqMode_neg, dsSetIntelliEqMode_neg, dsGetVolumeLeveller_neg, dsSetVolumeLeveller_neg, dsGetBassEnhancer_neg, dsSetBassEnhancer_neg, dsIsSurroundDecoderEnabled_neg, dsEnableSurroundDecoder_neg, dsGetDRCMode_neg, dsSetDRCMode_neg, dsGetSurroundVirt_neg, dsSetSurroundVirt_neg, dsGetMISteering_neg, dsSetMISteering_neg, dsGetGraphicEqMode_neg, dsSetGraphicEqMode_neg, dsGetMS12AudioProfList_neg, dsGetMS12AudioProf_neg, dsGetStereoMode_neg, dsSetStereoMode_neg, dsGetStereoAuto_neg, dsSetStereoAuto_neg, dsGetAudioGain_neg, dsSetAudioGain_neg, dsGetAudioLevel_neg, dsSetAudioLevel_neg, dsGetAudioDelay_neg, dsSetAudioDelay_neg, dsSetAudioAtmosOutMode_neg, dsGetSinkDeviceAtmosCap_neg, dsIsAudioMute_neg, dsIsAudioPortEnabled_neg, dsEnableAudioPort_neg, dsEnableLEConfig_neg, dsGetLEConfig_neg, dsSetMS12AudioProf_neg, dsSetAudioMute_neg, dsIsAudioMSDecode_neg, dsIsAudioMS12Decode_neg, dsAudioOutIsConn_neg, dsAudioOutRegConnCB_neg, dsAudioFmtUpdateRegCB_neg, dsGetAudioCaps_neg, dsGetMS12Caps_neg, dsSetAssocAudioMixing_neg, dsGetAssocAudioMixing_neg, dsSetFaderControl_neg, dsGetFaderControl_neg, dsSetPrimaryLang_neg, dsGetPrimaryLang_neg, dsSetSecondaryLang_neg, dsGetSecondaryLang_neg, dsSetAudioMixLevels_neg, dsAudioAtmosCapsRegCB_neg, dsGetSupportedARCTypes_neg, dsAudioSetSAD_neg, dsAudioEnableARC_neg

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `VTS-DSAUDIO-001` | SHALL initialize the Device Settings Audio Port sub-system via `dsAudioPortInit()` returning `dsERR_NONE` and SHALL terminate it via `dsAudioPortTerm()` returning `dsERR_NONE`. The module SHALL support re-initialization after a prior termination without error. |
| `VTS-DSAUDIO-002` | SHALL return a valid audio port handle for each supported port type and index via `dsGetAudioPort()` returning `dsERR_NONE`, with repeated calls for the same port returning an equal handle. SHALL retrieve the current audio stream format via `dsGetAudioFormat()`, the ATMOS capability of the connected sink device via `dsGetSinkDeviceAtmosCapability()`, and the audio output port connection status via `dsAudioOutIsConnected()`, each returning `dsERR_NONE`. SHALL successfully register event callbacks for audio output connection changes, audio format updates, and ATMOS capability changes via `dsAudioOutRegisterConnectCB()`, `dsAudioFormatUpdateRegisterCB()`, and `dsAudioAtmosCapsChangeRegisterCB()`, each returning `dsERR_NONE`. |
| `VTS-DSAUDIO-003` | SHALL get and set audio compression level, dialog enhancement level, Dolby volume mode, intelligent equalizer mode, volume leveller settings, bass enhancer level, surround decoder enable state, DRC mode, surround virtualizer settings, MI steering enable state, graphic equalizer mode, and loudness equivalence (LE) configuration via their respective `dsGet*` and `dsSet*` / `dsEnable*` APIs, each returning `dsERR_NONE` for valid parameters on supported audio ports. The value retrieved via the Get API after a Set operation SHALL match the value that was configured for each supported audio port in both enabled and disabled conditions. |
| `VTS-DSAUDIO-004` | SHALL enable and disable audio ports via `dsEnableAudioPort()` and confirm the enable state via `dsIsAudioPortEnabled()` returning `dsERR_NONE`. SHALL mute and unmute audio output via `dsSetAudioMute()` and confirm the mute state via `dsIsAudioMute()` returning `dsERR_NONE`. SHALL set and retrieve audio gain via `dsSetAudioGain()` and `dsGetAudioGain()`, audio volume level via `dsSetAudioLevel()` and `dsGetAudioLevel()`, and audio delay via `dsSetAudioDelay()` and `dsGetAudioDelay()`, each returning `dsERR_NONE` for valid values on supported port types. SHALL configure the Dolby ATMOS output mode via `dsSetAudioAtmosOutputMode()` returning `dsERR_NONE`. SHALL set the stereo mode via `dsSetStereoMode()` and retrieve it via `dsGetStereoMode()`, and configure stereo auto mode via `dsSetStereoAuto()` and retrieve it via `dsGetStereoAuto()`. The port enable state, mute state, audio delay, and stereo mode retrieved after configuration SHALL match the value that was set. |
| `VTS-DSAUDIO-005` | SHALL enable and disable associated audio mixing via `dsSetAssociatedAudioMixing()` and confirm the state via `dsGetAssociatedAudioMixing()` returning `dsERR_NONE`. SHALL set and retrieve the fader control mixer balance in the range [-32, +32] via `dsSetFaderControl()` and `dsGetFaderControl()` returning `dsERR_NONE`. SHALL configure audio input mixer levels via `dsSetAudioMixerLevels()` returning `dsERR_NONE` for each supported audio input type. SHALL set and retrieve the AC4 primary language code via `dsSetPrimaryLanguage()` and `dsGetPrimaryLanguage()`, and the AC4 secondary language code via `dsSetSecondaryLanguage()` and `dsGetSecondaryLanguage()`, each returning `dsERR_NONE` for valid 3-letter language codes. The configured audio mixing state and language codes retrieved after a Set operation SHALL match the values that were set. |
| `VTS-DSAUDIO-006` | SHALL retrieve the bitwise-OR-ed audio capabilities of each audio port via `dsGetAudioCapabilities()` returning `dsERR_NONE`, with the returned value matching the `AudioCapabilities` declared in the device profile. SHALL retrieve the bitwise-OR-ed MS12 capabilities of each port via `dsGetMS12Capabilities()` returning `dsERR_NONE`, with the returned value matching the `MS12Capabilities` in the device profile. SHALL report MS11 multistream decode support via `dsIsAudioMSDecode()` returning `dsERR_NONE`, with the result matching the `MS11Decode` field in the device profile. SHALL report MS12 multistream decode support via `dsIsAudioMS12Decode()` returning `dsERR_NONE`, with the result matching the `MS12Decode` field in the device profile. |
| `VTS-DSAUDIO-007` | SHALL retrieve the supported ARC types of the connected ARC/eARC device via `dsGetSupportedARCTypes()` returning `dsERR_NONE` for HDMI ARC-type ports. SHALL configure Short Audio Descriptor (SAD) data received from CEC via `dsAudioSetSAD()` returning `dsERR_NONE` for valid SAD lists on HDMI ARC ports. SHALL enable and disable ARC/eARC audio routing via `dsAudioEnableARC()` returning `dsERR_NONE`. SHALL retrieve the list of supported MS12 audio profiles via `dsGetMS12AudioProfileList()` returning `dsERR_NONE`, retrieve the currently active MS12 audio profile string via `dsGetMS12AudioProfile()`, and set an MS12 audio profile via `dsSetMS12AudioProfile()` returning `dsERR_NONE` for valid profile names on supported ports. (Note: MS11 and MS12 decode support queries are covered under VTS-DSAUDIO-006 as they require profile compliance verification.) |
| `VTS-DSAUDIO-008` | SHALL enforce the following error code contracts across all `dsAudio` APIs: `dsAudioPortInit()` SHALL return `dsERR_ALREADY_INITIALIZED` when called while already initialized; `dsAudioPortTerm()` SHALL return `dsERR_NOT_INITIALIZED` when called without prior initialization or after the module has already been terminated; all remaining `dsAudio` APIs SHALL return `dsERR_NOT_INITIALIZED` when invoked before initialization or after termination, and SHALL return `dsERR_INVALID_PARAM` when called with an invalid or null port handle, a NULL output pointer, or an out-of-range parameter value. |
