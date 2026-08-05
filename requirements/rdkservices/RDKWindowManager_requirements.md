## RDKWindowManager Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `RWM‑REQ‑001` | SHALL successfully add key intercepts with valid key codes and modifiers, and return an error response when addKeyIntercepts is invoked with empty modifiers or invalid keys |
| `RWM‑REQ‑002` | SHALL successfully create a display with valid parameters, and return an error response when createDisplay is invoked with empty or invalid display parameters |
| `RWM‑REQ‑003` | SHALL successfully enable and disable inactivity reporting, and return an error response when enableInactivityReporting is invoked with an invalid value |
| `RWM‑REQ‑004` | SHALL successfully generate a key event with a valid key code, and return an error response when generateKey is invoked with an invalid key code or without parameters |
| `RWM‑REQ‑005` | SHALL return the list of active application IDs |
| `RWM‑REQ‑006` | SHALL successfully remove a key intercept with valid parameters, and return an error response when removeKeyIntercept is invoked with invalid or empty parameters |
| `RWM‑REQ‑007` | SHALL successfully reset the inactivity time counter, set a valid positive inactivity interval, and return an error response when setInactivityInterval is invoked with a negative value |
| `RWM‑REQ‑008` | SHALL successfully set focus to a valid client, and return an error response when setFocus is invoked with an invalid or empty client |
| `RWM‑REQ‑009` | SHALL successfully set the visibility of a valid client to true and false, and return an error response when setVisible is invoked with an invalid client |
| `RWM‑REQ‑010` | SHALL successfully signal render-ready for a valid clientId, enable and disable display render for a valid clientId, and set and verify the Z-order for a valid clientId; return an error response when renderReady, enableDisplayRender, setZOrder, or getZOrder is invoked with invalid or empty clientId values |
| `RWM‑REQ‑011` | SHALL emit the onUserInactivity event after the configured inactivity interval expires, not emit the event when inactivity reporting is disabled, and confirm user-active status via the userActive API |
