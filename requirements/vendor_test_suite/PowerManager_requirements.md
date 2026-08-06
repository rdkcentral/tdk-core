# Power Manager — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑POWERMANAGER‑001` | SHALL successfully initialize the Power Manager HAL, successfully terminate it, and support re-initialization after a prior termination. |
| `VTS‑POWERMANAGER‑002` | SHALL preserve power state data integrity by setting the device power state for each power state defined in the device profile, retrieving the current power state, and, when a power state is set and subsequently retrieved, reporting a power state that matches the value that was set. |
| `VTS‑POWERMANAGER‑003` | SHALL preserve wakeup source data integrity by configuring each supported wakeup source to both enabled and disabled states, retrieving the current enable state, and, when a wakeup source enable state is set and subsequently retrieved, reporting an enable state that matches the value that was set. |
| `VTS‑POWERMANAGER‑004` | SHALL report an already-initialized error on repeated initialization, a not-initialized error for operations invoked before initialization or after termination, and an invalid-argument error for out-of-range parameter values or NULL output pointers. |
