# Device Settings Display — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DSDISPLAY‑001` | SHALL successfully initialize the Display sub-system, successfully terminate it, and return a valid display device handle for each supported video port. |
| `VTS‑DSDISPLAY‑002` | SHALL preserve data integrity across the display configuration controls — AVI content type, AVI scan information, and Auto Low Latency Mode (ALLM) enabled status — with each reported value matching the value that was set. |
| `VTS‑DSDISPLAY‑003` | SHALL retrieve the connected display's EDID information, its raw EDID byte buffer and length, and the display aspect ratio, each reporting a valid value with the default aspect ratio being 16x9. |
| `VTS‑DSDISPLAY‑004` | SHALL successfully register a display-event callback for a valid display. |
| `VTS‑DSDISPLAY‑005` | SHALL report an already-initialized error on repeated initialization, a not-initialized error for operations invoked before initialization or after termination, and an invalid-parameter error for invalid handles, NULL output pointers, or out-of-range parameter values. |
