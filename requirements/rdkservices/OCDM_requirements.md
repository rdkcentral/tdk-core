## OCDM Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `OCDM‑REQ‑001` | SHALL enumerate all supported DRM systems and successfully resolve the corresponding key system identifiers for each reported DRM, with the returned DRM list matching the expected value and each key system query returning a successful response |
| `OCDM‑REQ‑002` | SHALL emit a state change event when the OCDM plugin is activated and deactivated via the platform controller, with the event payload identifying the correct plugin callsign and target state value, and confirm the updated activation state after each transition |
