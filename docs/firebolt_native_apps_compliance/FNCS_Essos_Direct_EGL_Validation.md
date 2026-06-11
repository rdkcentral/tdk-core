# FNCS_Essos_Direct_EGL_Validation Test Case Documentation

## TestCase ID
FNCS_GRAPHICS_02

## TestCase Name
FNCS_Essos_Direct_EGL_Validation

## Objective
To execute the Essos_TDKTestApp as a direct EGL application and validate that the graphics rendering pipeline initializes correctly with all required APIs responding successfully and no validation errors occurring during the application execution.

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | TDK_FNCS_Package should be installed in DUT |
| 2 | Essos_TDKTestApp test binary should be available in the device |
| 3 | RunGraphicsTDKTest.sh script should be available in /opt/TDK directory on DUT |
| 4 | DUT must support direct EGL rendering with accessible EGL display |
| 5 | wpeframework should be stoppable if running to obtain EGL display for direct rendering |
| 6 | DUT must have proper permissions to execute shell commands from /opt/TDK directory |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Graphics Test Environment | Setup environment for graphics validation using platform specific environment variables from TDK.env. Stop wpeframework if required to obtain EGL display. Ensure the display compositor is configured for direct EGL rendering backend. | All environment variables must be set successfully, wpeframework must be stopped if required, and the display environment must be ready for direct EGL application launch successfully. |
| 2 | Validate Test Environment Readiness | Confirm that Essos_TDKTestApp binary and RunGraphicsTDKTest.sh are accessible and executable on the DUT. | Essos_TDKTestApp binary and RunGraphicsTDKTest.sh must be present and executable in expected DUT paths. |
| 3 | Execute Direct EGL Graphics Validation | Run the direct EGL graphics test command on DUT for 30 seconds to execute Essos_TDKTestApp with direct EGL rendering using the command `cd /opt/TDK ; sh RunGraphicsTDKTest.sh Essos 30`. | Environment variables must be set successfully, the Essos application binary must be accessible, the command must be constructed properly with correct parameters, and test application must start execution without errors. |
| 4 | Initialize Essos Graphics Context | Essos_TDKTestApp creates graphics context and initializes EGL surface with direct rendering configuration. | EGL context created successfully with direct rendering mode initialized. |
| 5 | Validate EGL API Calls | Verify all EGL initialization API calls execute successfully through the validation framework, checking EGL setup functions. | All EGL APIs must return success status without errors during initialization. |
| 6 | Configure Graphics Display Output | Essos_TDKTestApp configures display output with triangle geometry and color rendering through direct EGL pipeline. | Display output must be configured with proper rendering pipeline for visual output. |
| 7 | Execute Graphics Rendering Loop | Essos_TDKTestApp runs the rendering loop for the specified timeout (30 seconds), continuously updating triangle position and rendering to display. | Graphics rendering must proceed for full 30-second duration with stable frame rendering. |
| 8 | Monitor Rendering Performance | Continuously monitor graphics rendering performance during the 30-second execution window to ensure stable animation and proper resource utilization. | Graphics must render smoothly without stuttering, frame skipping, or performance degradation. |
| 9 | Validate Graphics Output | Verify that graphics application produces valid display output with no visual corruption or rendering artifacts during execution. | Graphics output must display correctly with no visual artifacts, color corruption, or rendering errors. |
| 10 | Capture Application Output | Collect the complete output from Essos_TDKTestApp including all validation messages and status indicators. | Output must be captured and available for validation parsing. |
| 11 | Parse Graphics Validation Output | Parse captured output to verify absence of `VALIDATION ERROR` strings and confirm success indicators from graphics validation framework. | Output must not contain `VALIDATION ERROR` statements; validation success indicators must be present. |
| 12 | Determine Test Result | Based on command execution completion, graphics validation output, and absence of validation errors, determine overall test result. | Test result must be marked SUCCESS if command executed without errors, graphics output is valid, and no validation errors found; otherwise mark FAILURE. |

## Test Attributes

**Supported Models:** RPI-Client, Video_Accelerator

**Estimated Duration:** 10 seconds

**Priority:** High

**Release Version:** M121
