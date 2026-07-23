# Deep Sleep Manager — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DEEPSLEEP‑001` | SHALL successfully initialize the Deep Sleep Management module, successfully terminate it, and support re-initialization after a prior termination without error. |
| `VTS‑DEEPSLEEP‑002` | SHALL place the DUT into deep sleep for a valid timeout duration with network standby both disabled and enabled, and after a timed deep sleep cycle report the last wakeup reason as a timer-triggered wakeup. |
| `VTS‑DEEPSLEEP‑003` | SHALL successfully complete post-wakeup platform processing following a deep sleep cycle. |
| `VTS‑DEEPSLEEP‑004` | SHALL retrieve the last wakeup reason and report a valid wakeup reason value. |
| `VTS‑DEEPSLEEP‑005` | SHALL retrieve the last wakeup key code and report a valid wakeup key code value. |
| `VTS‑DEEPSLEEP‑006` | SHALL report an already-initialized error on repeated initialization, a not-initialized error for operations invoked before initialization or after termination, and an invalid-argument error for NULL output pointers or out-of-range parameter values. |
