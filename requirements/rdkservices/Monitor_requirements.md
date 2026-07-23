## Monitor Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `MON‑REQ‑001` | SHALL successfully reset the memory and process statistics for the NetworkManager service via resetstats and return the observable name with restart limit and window values |
| `MON‑REQ‑002` | SHALL return the current service statistics for the NetworkManager service via the status API including observable name, restart limit, and restart window |
| `MON‑REQ‑003` | SHALL successfully set new restart limits (limit and window) for the NetworkManager service via restartlimits, and return an error response when restartlimits is invoked with invalid or missing parameters |
| `MON‑REQ‑004` | SHALL emit the statechange event with the correct plugin state when the Monitor plugin is activated and deactivated, and emit the all event for the same lifecycle transitions |
