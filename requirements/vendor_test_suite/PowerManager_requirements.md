# Power Manager — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑POWERMANAGER‑001` | SHALL successfully initialize the Power Manager HAL and successfully terminate it, supporting re-initialization after a prior termination. |
| `VTS‑POWERMANAGER‑002` | SHALL set the device power state for each power state defined in the device profile. |
| `VTS‑POWERMANAGER‑003` | SHALL retrieve the current device power state. |
| `VTS‑POWERMANAGER‑004` | SHALL, when a power state is set and subsequently retrieved, report a power state that matches the value that was set. |
| `VTS‑POWERMANAGER‑005` | SHALL configure each supported wakeup source to both enabled and disabled states. |
| `VTS‑POWERMANAGER‑006` | SHALL retrieve the current enable state of each supported wakeup source. |
| `VTS‑POWERMANAGER‑007` | SHALL, when a wakeup source enable state is set and subsequently retrieved, report an enable state that matches the value that was set. |
| `VTS‑POWERMANAGER‑008` | SHALL enforce the following error handling contracts across all Power Manager operations:<br>report an already-initialized error when initialization is attempted while the module is already initialized<br>report a not-initialized error when any operation is attempted without prior initialization or after the module has already been terminated<br>report an invalid-argument error when a power state or wakeup source set/get operation is called with an out-of-range parameter value or a NULL output pointer. |
