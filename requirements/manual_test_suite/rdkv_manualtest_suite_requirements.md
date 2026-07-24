# RDK-V Manual Test Suite — Specifications

## Normative Terminology

Requirement statements use the following normative terms:

| Term | Meaning | Certification implication |
|:-----|:--------|:--------------------------|
| **SHALL / MUST** | Mandatory requirement | Failure blocks certification unless a formal waiver is approved |
| **SHALL NOT / MUST NOT** | Mandatory prohibition | Violation blocks certification unless an exceptional waiver is approved |
| **SHOULD** | Strong recommendation | Deviation must be documented when applicable; does not automatically block certification unless tied to a mandatory test |
| **MAY** | Permitted option | No certification impact unless the option is declared as supported by the DUT |
| **OPTIONAL** | Capability not required for all devices | If claimed by vendor or profile, applicable tests may become mandatory |
| **CONDITIONAL** | Required when a defined condition is true | Applicability must be determined using the capability declaration |

## Normative-Term Classification Summary

The table below records requirements that are **not** `SHALL` and the rationale for their classification. All requirements not listed here are `SHALL` (mandatory core-platform behaviour applicable to every DUT).

| Req ID | Term | Rationale |
|:-------|:-----|:----------|
| `MANUAL-REQ-004` | SHOULD | AppManager resource limits for suspended and inactive application states are not applicable to all RDK platform versions (e.g., not supported in RDK8); classified as SHOULD to reflect platform-version-conditional applicability. |
| `MANUAL-REQ-008` | SHOULD | App suspension to background state via Home key and playback resume is a supplementary UX convenience behavior; no normative specification mandates this interaction pattern, and deviation does not automatically block certification. |
| `MANUAL-REQ-022` | SHOULD | Miracast screen mirroring is an optional secondary use case; Miracast is a Wi-Fi Alliance optional profile not universally mandated for streaming Video Accelerators, and deviation is documented rather than automatically blocking certification. |

## Requirement Grouping Criteria

The table below documents the criteria considered when grouping test cases into requirements.

| Criterion | Description and Example |
|:----------|:------------------------|
| **Same feature domain** | Test cases validating the same functional capability are grouped under one requirement. E.g., all AppManager data clear operations → `MANUAL-REQ-001`. |
| **Distinct operation type within a module** | Where a module tests clearly distinct operations, separate requirements are created. E.g., AppManager produces five separate requirements covering data clear, lifecycle, update, resource limits, and installation. |
| **Subsystem boundary** | Test cases from different platform subsystems are never merged. E.g., HDCP compliance and HDMI Hotplug are separate requirements despite both involving HDMI. |
| **Wake mechanism abstraction** | Multiple test cases exercising the same power state capability through different wake triggers are unified under one requirement. E.g., all Deep Sleep wake tests (BT remote, WoL, USB Ethernet) → `MANUAL-REQ-024`. |
| **App suspend/hibernate isolation** | Any test cases or requirement groups involving application suspension, hibernation, or inactive state resource management are isolated into dedicated `SHOULD` requirements and never grouped with mandatory `SHALL` requirements. |
| **Cross-aspect unification at interface boundaries** | Test cases covering multiple aspects of the same interface event (UI restoration, playback resilience, DRM, HDCP) are unified when all aspects relate to the same platform-level recovery capability. E.g., HDMI Hotplug recovery → `MANUAL-REQ-018`. |
| **Codec and format grouping by media type** | Audio codecs, video codecs, streaming protocols, and container formats each form a distinct requirement under the AV pipeline. Video codecs (H.264/AVC, H.265/HEVC, MPEG-4, AV1) and HDR display technology → `MANUAL-REQ-009`; streaming protocols (HLS, MPEG-DASH) and container format (MPEG2-TS) → `MANUAL-REQ-010`; audio codecs (AAC, MP3, AC-3, E-AC-3) → `MANUAL-REQ-011`. MPEG-2 Transport Stream (MPEG2-TS) is classified as a container format and grouped with streaming protocols in `MANUAL-REQ-010`, not with video codecs. |
| **Wi-Fi split by operational class** | Initial connectivity and SSID switching tests are separated from resilience, fallback, and persistence tests. E.g., connectivity → `MANUAL-REQ-035`, resilience → `MANUAL-REQ-036`. |

## Requirements

| Req ID | Test Scope | Open Issues |
|--------|------------|-------------|
| `MANUAL-REQ-001` | SHALL support complete and persistent user data clearance for installed applications — individually and in bulk — with the cleared state durably maintained across subsequent launches and device reboot. | |
| `MANUAL-REQ-002` | SHALL support multi-application lifecycle management — including concurrent launch, suspension, background operation, deeplink-based launch, reinstallation, and post-uninstall reboot recovery — with correct state retention across each lifecycle transition. | |
| `MANUAL-REQ-003` | SHALL support application version update management for installed applications — individually and concurrently — accessible from all available UI entry points, with updated version state persistently maintained after each update operation. | |
| `MANUAL-REQ-004` | SHOULD support Application Manager resource limit enforcement for suspended and inactive application states, including maximum concurrent suspended application count and the associated memory and storage capacity boundaries for those states. | |
| `MANUAL-REQ-005` | SHALL support Application Manager installation robustness and package integrity protection, encompassing background installation continuity without user interaction, deterministic error state management under storage exhaustion and application data-state failure conditions, and enforcement of package lock to prevent uninstallation of active applications. | |
| `MANUAL-REQ-006` | SHALL support RDK UI Home screen navigation — including application launch from available content sections, Settings screen accessibility, pane-based focus state restoration, and timezone-synchronized time display. | |
| `MANUAL-REQ-007` | SHALL support AV content playback with complete trick-play control and Back key-triggered session termination to the RDK UI Home screen for installed streaming applications. | |
| `MANUAL-REQ-008` | SHOULD support streaming application background state management, enabling applications to retain their playback state and resume from the last-known playback position upon subsequent foreground launch. | |
| `MANUAL-REQ-009` | SHALL decode and render H.264 (AVC), H.265/HEVC, MPEG-4 Part 2, and AV1 video codec formats, including HDR10 high dynamic range content, without playback error or AV artifact. | |
| `MANUAL-REQ-010` | SHALL parse and play HLS (.m3u8) and MPEG-DASH / DASH (.mpd) adaptive bitrate streams, and demux and play MPEG-2 Transport Stream (MPEG2-TS) container-encapsulated content, without playback error or AV artifact. | |
| `MANUAL-REQ-011` | SHALL decode and play AAC, MP3, AC-3 (Dolby Digital), and E-AC-3 (Dolby Digital Plus) audio codec formats without playback error or audio discontinuity. | |
| `MANUAL-REQ-012` | SHALL support Bluetooth remote pairing from all available entry points, pairing persistence across device reboot, re-pairing after factory reset, and automatic reconnection after power interruption. | |
| `MANUAL-REQ-013` | SHALL support standard Bluetooth remote key functionality, encompassing navigation, content selection, volume control, and display power state management. | |
| `MANUAL-REQ-014` | SHALL decrypt and play PlayReady and Widevine DRM-protected content without decryption failure or license acquisition error. | |
| `MANUAL-REQ-015` | SHALL support Bluetooth external audio device connectivity, encompassing pairing and disconnection management, audio stream routing, volume and mute control, device information retrieval, and automatic audio stream re-establishment after power interruption. | |
| `MANUAL-REQ-016` | SHALL maintain HDCP content protection compliance — including authentication initiation, authentication status reporting, protocol and version reporting, enabled-status reporting, and display connection status reporting — across all supported HDMI connection states. | |
| `MANUAL-REQ-017` | SHALL support HDMI CEC control, encompassing enable and disable management, TV power state control, RDK UI screen restoration on TV power-on, active session preservation during CEC command execution, and DUT wake-up from low-power states via CEC-triggered input selection. | |
| `MANUAL-REQ-018` | SHALL support complete platform state restoration — including RDK UI display restoration, application playback continuity, active streaming and casting session preservation, DRM-protected content resumption, and HDCP compliance maintenance — following an HDMI cable reconnect event. | |
| `MANUAL-REQ-019` | SHALL decode and render JPEG, PNG, SVG, and WebP image formats through the browser rendering subsystem. | |
| `MANUAL-REQ-020` | SHALL support XCONF-based firmware upgrade and downgrade capability — accessible via all supported initiation methods — with user settings, network connectivity, and peripheral pairing persistently maintained across firmware transitions. | |
| `MANUAL-REQ-021` | SHALL support IPv6 network connectivity encompassing connectivity status reporting, per-interface public address retrieval, internet access over IPv6, network diagnostic operations, and accurate per-interface address isolation across all active network interface configurations. | |
| `MANUAL-REQ-022` | SHOULD support Miracast screen mirroring capability, encompassing device discovery and connection, real-time screen and audio transmission, media playback controls, sustained long-duration operational continuity, cross-platform compatibility, fault-tolerant error state recovery, and session resilience across power state transitions and network changes. | |
| `MANUAL-REQ-023` | SHALL support Light Sleep power state management — including timer-based automatic entry, configurable sleep timer disable, and wake-up from all supported mechanisms — with complete platform service and network connectivity restoration upon exit. | |
| `MANUAL-REQ-024` | SHALL support Deep Sleep power state management — including timer-based automatic entry, configurable sleep timer disable, and wake-up from all supported mechanisms — with complete platform service and network connectivity restoration upon exit. | |
| `MANUAL-REQ-025` | SHALL support screen saver power state management — including inactivity-triggered activation, configurable screen saver disable, and deterministic timer sequencing when configured alongside sleep state timers — with complete RDK UI display restoration upon exit. | |
| `MANUAL-REQ-026` | SHALL support consistent RDK UI display rendering from boot — including valid first-boot and subsequent boot screen layout, absence of display rendering artifacts during navigation, and volume overlay rendering in response to volume key input. | |
| `MANUAL-REQ-027` | SHALL support RDK UI device settings and configuration management — including language localization and persistence, display and audio output configuration, device and peripheral information display, timezone management, privacy and license information access, privacy data clearance, and system reboot capability. | |
| `MANUAL-REQ-028` | SHALL support factory reset capability that restores all device settings and user-installed applications to factory defaults, with subsequent application reinstallation and launch fully functional after reset. | |
| `MANUAL-REQ-029` | SHALL support RDK UI app store navigation and installation — encompassing app catalogue browsing with defined loading and error state transitions, multi-entry-point application installation, background download continuity, sequential download queue management, and input event suppression during active installation operations. | |
| `MANUAL-REQ-030` | SHALL support application uninstallation capability — including individual and sequential multi-application removal — with state-consistent RDK UI Home screen adaptation to the installed application state and complete reinstallation capability after uninstall. | |
| `MANUAL-REQ-031` | SHALL support RDK UI error state management for application download and launch failures, with error notification overlays dismissible via any supported user interaction and the prior screen state restored upon dismissal. | |
| `MANUAL-REQ-032` | SHALL maintain core platform service operational status — including accessible serial console and SSH remote management interfaces, WPEFramework service availability, and a system log rotation mechanism. | |
| `MANUAL-REQ-033` | SHALL support Web Audio API capabilities — including audio context lifecycle management, audio playback and control, speech synthesis with multi-language and voice enumeration support, programmatic sound synthesis, and concurrent multimedia stream management. | |
| `MANUAL-REQ-034` | SHALL decode and play AAC, MP3, OGG Vorbis, and WAV PCM audio codec formats through the Web Audio API. | |
| `MANUAL-REQ-035` | SHALL support Wi-Fi network connectivity — including SSID connection and switching from all available UI entry points, dual-band network support, reconnection to previously connected networks, and connection failure status notification. | |
| `MANUAL-REQ-036` | SHALL support Wi-Fi network resilience — including automatic Ethernet failover, connection persistence across device reboot, mobile hotspot connectivity, automatic network fallback to available prior networks when target networks are inaccessible, and automatic reconnection after manual disconnect. | |
| `MANUAL-REQ-037` | SHALL support XDial device discovery and dynamic registration lifecycle — including configurable local discovery, application-installation-driven registration and de-registration, and registration state persistence across device reboot. | |
| `MANUAL-REQ-038` | SHALL support XDial casting session management and media playback control — including remote navigation and playback controls from the casting device, independent application volume control, content selection from all supported interaction points, voice search integration, session disconnect and reconnect capability, and concurrent casting attempt arbitration. | |
| `MANUAL-REQ-039` | SHALL support deterministic XDial casting session state management across network interface transitions and power state transitions — including session termination upon network interface change, and DUT wake-up from network standby in response to an incoming cast request. | |
