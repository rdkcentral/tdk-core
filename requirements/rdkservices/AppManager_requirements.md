## AppManager Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `AM‑REQ‑001` | SHALL return the list of installed applications via getInstalledApps with a valid response payload |
| `AM‑REQ‑002` | SHALL return true when isInstalled is invoked with a valid installed appId, and SHALL return false or an appropriate response for invalid, empty, non-existent, numeric, special-character, whitespace, long-string, and alphanumeric-mixed appId values |
| `AM‑REQ‑003` | SHALL return the list of currently loaded applications via getLoadedApps with a valid response payload |
| `AM‑REQ‑004` | SHALL successfully launch an application with valid appId, intent, and launchArgs parameters, and SHALL return an error response when launchApp is invoked with invalid, empty, or missing appId, intent, launchArgs, or all parameters, including long-string edge cases |
| `AM‑REQ‑005` | SHALL successfully preload an application with valid parameters, accept numeric and alphanumeric appId and launchArgs variations, handle empty and special-character inputs gracefully, and return an appropriate response when the appId is already preloaded |
| `AM‑REQ‑006` | SHALL successfully close a loaded application with a valid appId, and SHALL return an error response when closeApp is invoked with an invalid, empty, or special-character appId, or when the specified valid appId is not currently loaded |
| `AM‑REQ‑007` | SHALL successfully terminate an application with a valid appId, and SHALL return an error response when terminateApp is invoked with an invalid, empty, numeric, or special-character appId |
| `AM‑REQ‑008` | SHALL successfully start a system application with a valid appId, and SHALL return an error response when startSystemApp is invoked with an invalid, empty, numeric, or special-character appId |
| `AM‑REQ‑009` | SHALL successfully stop a running system application with a valid appId, handle the case where the application is already stopped, and SHALL return an error response when stopSystemApp is invoked with invalid, empty, numeric, special-character, or alphanumeric appId values |
| `AM‑REQ‑010` | SHALL successfully terminate (kill) an application with a valid appId, and SHALL return an error response when killApp is invoked with an invalid, empty, numeric, or special-character appId |
| `AM‑REQ‑011` | SHALL successfully send an intent to an application with valid appId and intent parameters, and SHALL return an error response when sendIntent is invoked with an empty intent, empty appId, empty parameters, or an invalid appId |
| `AM‑REQ‑012` | SHALL successfully clear data for a valid appId, SHALL successfully clear all app data, and SHALL return an error response when clearAppData is invoked with invalid, empty, numeric, special-character, long, or alphanumeric appId values |
| `AM‑REQ‑013` | SHALL successfully set an application property with a valid appId, key, and value (including a configurable delay), return correct property values for valid key queries, and SHALL return an error response when setAppProperty or getAppProperty is invoked with invalid, empty, or mismatched appId, key, or value parameters, including special-character and numeric variants; SHALL also return valid property values for pinlock and inactive priority keys |
| `AM‑REQ‑014` | SHALL enforce a maximum concurrent running application limit and SHALL enforce an inactive application RAM usage ceiling |
| `AM‑REQ‑015` | SHALL successfully activate a system application with a valid appId, and SHALL return an error response when activateSystemApp is invoked with invalid, empty, special-character, or numeric appId values, or without any parameter |
| `AM‑REQ‑016` | SHALL successfully deactivate a system application with a valid appId, and SHALL return an error response when deactivateSystemApp is invoked with invalid, empty, special-character, or numeric appId values, or without any parameter |
| `AM‑REQ‑017` | SHALL successfully hibernate a system application with a valid appId, and SHALL return an error response when hibernateSystemApp is invoked with invalid, empty, special-character, or numeric appId values, or without any parameter |
| `AM‑REQ‑018` | SHALL correctly execute combined app lock, launch, terminate, kill, close, and unlock operation sequences in the correct order and reflect the expected application state after each operation |
| `AM‑REQ‑019` | SHALL emit the onAppLifecycleStateChanged event with the correct payload when an application is closed, killed, or terminated |
| `AM‑REQ‑020` | SHALL reflect the correct loaded applications list after a launch, after a second launch of the same app, and after close, kill, and terminate operations, confirming accurate getLoadedApps state tracking throughout the application lifecycle |
