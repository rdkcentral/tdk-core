# Deep Sleep Manager — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DEEPSLEEP‑001` | SHALL successfully initialize the Deep Sleep Management module, successfully terminate it, and support re-initialization after a prior termination without error. |
| `VTS‑DEEPSLEEP‑002` | SHALL place the DUT into deep sleep for a valid timeout duration with network standby both disabled and enabled, and after a timed deep sleep cycle report the last wakeup reason as a timer-triggered wakeup. |
| `VTS‑DEEPSLEEP‑003` | SHALL successfully complete post-wakeup platform processing following a deep sleep cycle. |
| `VTS‑DEEPSLEEP‑004` | SHALL retrieve the last wakeup reason and report a valid wakeup reason value. |
| `VTS‑DEEPSLEEP‑005` | SHALL retrieve the last wakeup key code and report a valid wakeup key code value. |
| `VTS‑DEEPSLEEP‑006` | SHALL enforce the following error handling contracts across all Deep Sleep Management operations:<br>report an already-initialized error when initialization is attempted while the module is already initialized<br>report a not-initialized error when any operation is attempted without prior initialization or after the module has already been terminated<br>report an invalid-argument error when a deep sleep, last wakeup reason, or last wakeup key code operation is invoked with a NULL output pointer or an out-of-range parameter value. |
