# FNCS_Essos_Wayland_Client_Validation Test Case Documentation

## TestCase ID
FNCS_GRAPHICS_01

## TestCase Name
FNCS_Essos_Wayland_Client_Validation

## Objective
To execute the Essos_TDKTestApp as a Wayland client application and validate that the graphics rendering pipeline initializes correctly in Wayland client mode with all required APIs responding successfully and no validation errors occurring during the application execution.

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | TDK_FNCS_Package should be installed in DUT |
| 2 | Essos_TDKTestApp test binary should be available in the device |
| 3 | RunGraphicsTDKTest.sh script should be available in /opt/TDK directory on DUT |
| 4 | DUT must support Wayland client rendering with active Wayland compositor |
| 5 | Wayland client support must be present in the graphics stack and libwayland-egl library must be available |
| 6 | wpeframework should be stoppable if running to obtain client EGL display for Wayland rendering |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Graphics Test Environment | Setup environment for graphics validation using platform specific environment variables from TDK.env. Stop wpeframework if required to obtain EGL display. Ensure the display compositor or Wayland server is configured for Wayland client rendering backend. | All environment variables must be set successfully, wpeframework must be stopped if required, and the display environment must be ready for Wayland client application launch successfully. |
| 2 | Validate Test Environment Readiness | Confirm that Essos_TDKTestApp binary, RunGraphicsTDKTest.sh script, and libwayland-egl library are accessible on the DUT. | Essos_TDKTestApp binary, RunGraphicsTDKTest.sh, and Wayland EGL library must be present and accessible in expected DUT paths. |
| 3 | Execute Wayland Client Graphics Validation | Run the Wayland client graphics test command on DUT for 30 seconds to execute Essos_TDKTestApp in Wayland client mode using the command `cd /opt/TDK ; sh RunGraphicsTDKTest.sh Essos 30 USE_WAYLAND`. | Environment variables must be set successfully, the Essos application binary must be accessible, the command must be constructed properly with correct parameters, and test application must start execution without errors. |
| 4 | Initialize Wayland Client Graphics Context | Essos_TDKTestApp creates graphics context for Wayland client mode and initializes EGL surface with Wayland client configuration, establishing connection to Wayland compositor. | Wayland client context created successfully with Wayland compositor connection established and EGL surface configured for client mode. |
| 5 | Validate Wayland EGL API Calls | Verify all EGL initialization API calls for Wayland client mode execute successfully through the validation framework, checking Wayland-specific EGL setup functions. | All Wayland EGL APIs must return success status without errors during initialization and client mode setup. |
| 6 | Configure Wayland Client Display Output | Essos_TDKTestApp configures display output in Wayland client mode with triangle geometry and color rendering through Wayland EGL pipeline. | Wayland client display output must be configured with proper rendering pipeline for visual output to compositor. |
| 7 | Execute Wayland Client Rendering Loop | Essos_TDKTestApp runs the rendering loop for the specified timeout (30 seconds), continuously updating triangle position and rendering to Wayland compositor. | Graphics rendering to Wayland compositor must proceed for full 30-second duration with stable frame rendering. |
| 8 | Monitor Wayland Client Rendering Performance | Continuously monitor graphics rendering performance in Wayland client mode during the 30-second execution window to ensure stable animation and proper resource utilization. | Graphics must render smoothly in Wayland client mode without stuttering, frame skipping, or performance degradation. |
| 9 | Validate Wayland Graphics Output | Verify that Wayland client graphics application produces valid display output with no visual corruption or rendering artifacts during execution. | Wayland graphics output must display correctly on compositor with no visual artifacts, color corruption, or rendering errors. |
| 10 | Capture Application Output | Collect the complete output from Essos_TDKTestApp in Wayland client mode including all validation messages and status indicators. | Output must be captured and available for validation parsing. |
| 11 | Parse Graphics Validation Output | Parse captured output to verify absence of `VALIDATION ERROR` strings and confirm success indicators from graphics validation framework. | Output must not contain `VALIDATION ERROR` statements; validation success indicators must be present. |
| 12 | Determine Test Result | Based on command execution completion, graphics validation output, and absence of validation errors, determine overall test result for Wayland client mode. | Test result must be marked SUCCESS if command executed without errors, graphics output is valid, and no validation errors found; otherwise mark FAILURE. |

## Test Attributes

**Supported Models:** RPI-Client, Video_Accelerator

**Estimated Duration:** 10 seconds

**Priority:** High

**Release Version:** M121
