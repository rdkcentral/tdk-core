## MaintenanceManager Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `MM‑REQ‑001` | SHALL return the current maintenance activity status and maintenance start time via the respective API methods |
| `MM‑REQ‑002` | SHALL return the current maintenance mode and opt-out mode configuration via getMaintenanceMode |
| `MM‑REQ‑003` | SHALL successfully start and stop a maintenance task, emit the onMaintenanceStatusChange event during the operation, and handle starting maintenance when a session is already active |
| `MM‑REQ‑004` | SHALL emit the statechange event with the correct plugin state when the MaintenanceManager plugin is activated and deactivated |
| `MM‑REQ‑005` | SHALL return the correct maintenance activity status by polling the status during an active maintenance session |
| `MM‑REQ‑006` | SHALL successfully set the maintenance mode with BACKGROUND and FOREGROUND modes combined with valid opt-out values (BYPASS_OPTOUT, ENFORCE_OPTOUT, NONE), setting mode-only or opt-out-only parameters, and return an error for invalid, empty, special-character, or numeric mode or opt-out combinations |
| `MM‑REQ‑007` | SHALL return an error when getMaintenanceActivityStatus or getMaintenanceStartTime is called while maintenance is not running, and return an error when stopMaintenance is called while no maintenance is active |
| `MM‑REQ‑008` | SHALL return an error response when setMaintenanceMode is invoked with missing required parameters, an empty maintenanceMode, an empty optOut mode, an invalid optout mode, or an invalid maintenanceMode value |
