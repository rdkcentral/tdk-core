# Device Settings Display — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DSDISPLAY‑001` | SHALL successfully initialize the Display sub-system and successfully terminate it. |
| `VTS‑DSDISPLAY‑002` | SHALL return a valid display device handle for each supported video port. |
| `VTS‑DSDISPLAY‑003` | SHALL retrieve the connected display's EDID information and report valid EDID data. |
| `VTS‑DSDISPLAY‑004` | SHALL retrieve the connected display's raw EDID byte buffer and its length. |
| `VTS‑DSDISPLAY‑005` | SHALL retrieve the display aspect ratio of a valid display, with the default reported aspect ratio being 16x9. |
| `VTS‑DSDISPLAY‑006` | SHALL register a display-event callback for a valid display. |
| `VTS‑DSDISPLAY‑007` | SHALL, for each valid AVI content type, set the value, with the reported value matching the value that was set. |
| `VTS‑DSDISPLAY‑008` | SHALL set the AVI scan information of a valid display and retrieve it reporting a valid value. |
| `VTS‑DSDISPLAY‑009` | SHALL set the Auto Low Latency Mode (ALLM) enabled status of a valid display and retrieve it reporting a valid value. |
| `VTS‑DSDISPLAY‑010` | SHALL report an already-initialized error on repeated initialization, a not-initialized error for operations invoked before initialization or after termination, and an invalid-parameter error for invalid handles, NULL output pointers, or out-of-range parameter values. |
