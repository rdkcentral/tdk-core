## HDCP_Profile Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `HDCP‑REQ‑001` | SHALL return the HDCP status information including HDCP version and authentication state for the connected display via getHDCPStatus |
| `HDCP‑REQ‑002` | SHALL return the HDCP version supported by the STB via getSettopHDCPSupport |
| `HDCP‑REQ‑003` | SHALL emit the statechange event with the correct plugin state when the HdcpProfile plugin is activated and deactivated, and emit the all event for the same lifecycle transitions |
