## SystemAudioPlayer Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `SAP‑REQ‑001` | SHALL successfully open a System Audio Player session for PCM, MP3, and WAV audio types with HTTPSRC source type in both System and App play modes, returning a valid player ID |
| `SAP‑REQ‑002` | SHALL successfully configure a PCM player session with valid parameters in both System and App play modes |
| `SAP‑REQ‑003` | SHALL return a valid player session ID for WAV and MP3 audio sources in both System and App play modes |
| `SAP‑REQ‑004` | SHALL correctly report the isSpeaking status as true during active audio playback for MP3 and WAV sources in both System and App play modes |
| `SAP‑REQ‑005` | SHALL successfully play, pause, and stop audio for MP3 and WAV sources in System and App play modes, and successfully play, pause, resume, and stop audio for MP3 and WAV sources in System and App play modes |
| `SAP‑REQ‑006` | SHALL successfully set mixer levels (primary volume and player volume) during MP3 and WAV audio playback in both System and App play modes |
| `SAP‑REQ‑007` | SHALL successfully enable smart volume control for PCM, MP3, and WAV audio sources in both System and App play modes, with the primary audio volume automatically reduced accordingly |
| `SAP‑REQ‑008` | SHALL return an error response when openPlayer is invoked with an empty audio type, an invalid audio type, an invalid source type, or an invalid play mode |
| `SAP‑REQ‑009` | SHALL return an error response when closePlayer, playAudio, pauseAudio, resumeAudio, or stopAudio is invoked with an invalid player ID, when playAudio is invoked with an empty URL, and when playAudio is attempted on a closed (error state) player |
| `SAP‑REQ‑010` | SHALL return an error response when setMixerLevels is invoked with an out-of-range primary volume or player volume, and accept mixer level values at both the minimum and maximum boundary values |
| `SAP‑REQ‑011` | SHALL return an error response when getPlayerSessionId is invoked with an empty URL, when configPlayer is invoked with an invalid player ID, and when setSmartVolControl is invoked with an out-of-range threshold value |
| `SAP‑REQ‑012` | SHALL correctly manage the smart volume control lifecycle (enable, play, disable), successfully operate two simultaneous players in System and App modes, and correctly replay audio after a play/stop cycle |
