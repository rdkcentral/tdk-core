## Controller Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `CTRL‑REQ‑001` | SHALL successfully initiate a network discovery scan and return a list of discovered devices with valid locator, latency, model, and secure fields |
| `CTRL‑REQ‑002` | SHALL return a valid subsystems status array, framework process information (PID, path, memory, threads), active connections list, and all-plugins status list |
| `CTRL‑REQ‑003` | SHALL retrieve the current value of valid environment variables, and SHALL return an error response when queried with an invalid or non-existent environment variable name |
| `CTRL‑REQ‑004` | SHALL retrieve the DeviceInfo plugin configuration, successfully store an updated configuration, and successfully delete directory contents for a valid configured path; SHALL return an error response when deleteDirectoryContents is invoked with an empty path or when configuration is set with an empty value |
| `CTRL‑REQ‑005` | SHALL report the activation state of all plugins, confirm the WPEFramework process status, emit the statechange and all events during DeviceInfo plugin activate/deactivate transitions, and reflect the deactivated state after the DeviceInfo plugin is deactivated via an API call |
| `CTRL‑REQ‑006` | SHALL successfully set a plugin to the unavailable state from deactivated and from activated states, allow querying a plugin while it is in the unavailable state, and successfully re-activate a plugin that was previously set to unavailable; SHALL confirm that the Controller plugin itself can be set to unavailable |
| `CTRL‑REQ‑007` | SHALL successfully activate and deactivate the Controller plugin and confirm the resulting activation state after each transition |
| `CTRL‑REQ‑008` | SHALL return an error response when activate or deactivate is invoked with an invalid callsign or an empty callsign |
