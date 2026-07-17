## TestCase ID
RDKV_MANUAL_GT_XCONF_01
## TestCase Name
RDKV_CERT_MANUAL_GT_Xconf_Fw_Upgrade_Via_Api

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT's XCONF-based firmware upgrade process can be triggered via the RDK system service API and that the device successfully downloads and applies the configured target firmware image. This test confirms the complete firmware upgrade workflow — from initiation through download and flash completion — is operational and correctly reported, meeting XCONF image upgrade certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`XCONF_imageUpgrade_Automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with the correct XCONF server URL, firmware image details, and API credentials specific to this test case prior to execution. | The files `XCONF_imageUpgrade_Automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all correct XCONF-specific values (`<xconf_server_url>`, `<xconf_imagefile_to_upgrade>`, `<xconf_firmware_dwld_location>`, `<xconf_API_key_token>`, etc.) prior to execution. |
| 2 | Verify DUT network connectivity | Ensure the DUT has active Ethernet network connectivity and can reach the XCONF server. The script validates this automatically via `check_server_connectivity "<xconf_server_url>"` before any test steps execute. | The DUT must have active network connectivity and the XCONF server at `<xconf_server_url>` must be reachable from the DUT prior to test execution. |
| 3 | Verify DUT platform is XCONF-supported | Confirm the DUT platform is one of the XCONF-supported models: RPI4, AH212, or REALTEKHANK. The script automatically identifies the platform via `platform_type_finder`. The BCM974116SFF platform does not support XCONF image upgrade and will cause the precondition to fail. | The DUT platform must be identified as RPI4, AH212, or REALTEKHANK. If the platform is BCM974116SFF or unidentified, the precondition will exit and the test will not execute. |
| 4 | Verify target firmware image available on download server | Ensure the target firmware image `<xconf_imagefile_to_upgrade>` is hosted and accessible at the configured firmware download location `<xconf_firmware_dwld_location>` prior to the test. | The target firmware image file must be present and accessible at `<xconf_firmware_dwld_location>` so that the DUT can successfully download and flash it during the upgrade process. |
| 5 | Retrieve DUT MAC and query XCONF firmware config | The script automatically retrieves the DUT Ethernet MAC address via `get_iface_info "eth0" "mac"`, then queries the XCONF server at `<xconf_config_check_url><MAC>` to verify that valid firmware rules exist for the DUT. The response is checked to confirm that `firmwareFilename` matches `<xconf_imagefile_to_upgrade>` and `firmwareLocation` matches `<xconf_firmware_dwld_location>` from `device.conf`. | The XCONF server must return a valid firmware config for the DUT MAC address. The `firmwareFilename` and `firmwareLocation` in the XCONF response must match the expected values configured in `device.conf`. |
| 6 | Update XCONF firmware config if mismatch detected | If the XCONF config does not match the expected values, the script prompts: *"Do you want to update the firmware config in XCONF with build `<xconf_imagefile_to_upgrade>`? [yes/no]:"* — responding `yes` triggers an automatic PUT request to `<xconf_restApi_firmware_config>` using `<xconf_API_key_token>` to update the firmware configuration with the correct filename, version, and supported model IDs. | If a mismatch is detected and the tester responds `yes`, the XCONF PUT API must return a response confirming the firmware config has been updated with `<xconf_imagefile_to_upgrade>` and `<xconf_imagefile_version>` before the test steps execute. If the tester responds `no`, the precondition exits without updating. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Capture current firmware version | Execute the following command on the DUT to record the current firmware version as the baseline before initiating the upgrade:<br>`cat /version.txt` | The current firmware version (imagename) should be displayed from `/version.txt` and recorded as the baseline firmware version prior to the XCONF upgrade. |
| 2 | Trigger XCONF firmware upgrade via RDK service API | Execute the following curl command to trigger the XCONF firmware upgrade via the `org.rdk.System.1.firmwareUpdate` RDK service API:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.firmwareUpdate"}' http://127.0.0.1:9998/jsonrpc` | The `org.rdk.System.1.firmwareUpdate` API should return `"success":true` confirming that the XCONF firmware upgrade process has been initiated on the DUT. The DUT will begin contacting the XCONF server and downloading the target firmware in the background. |
| 3 | Monitor swupdate.log for firmware upgrade success | The script polls `/opt/logs/swupdate.log` at regular intervals for a maximum of 10 minutes, checking for the presence of either of the following upgrade success strings using `check_log_for_string`:<br>- `"doCDL success"`<br>- `"image flashing success"`<br><br>Once a success string is found the firmware flash is complete and the DUT will reboot automatically. The shell script terminates at this point — no further steps execute after the reboot. If neither string is found within 10 minutes the upgrade is considered failed. | The string `"doCDL success"` or `"image flashing success"` must be found in `/opt/logs/swupdate.log` within the 10-minute polling window, confirming that the firmware image `<xconf_imagefile_to_upgrade>` was successfully downloaded and flashed on the DUT. The step is marked PASS when the success string is detected. If neither string appears within 10 minutes the step is marked FAIL. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
