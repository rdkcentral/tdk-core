## TestCase ID
RDKV_MANUAL_IMG_UPGRADE_01
## TestCase Name
RDKV_CERT_MANUAL_Img_Upgrade_Xconf_Fw_Via_Api

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the XCONF firmware upgrade workflow from the current test image to a target image using the RDKServices Thunder API on the DUT. This test confirms that the firmware version is correctly updated to the upgraded image version as configured in XCONF, ensuring API-triggered firmware upgrade meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect Ethernet cable | Connect the Ethernet cable to the DUT and ensure a valid IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 3 | Ensure SSH or console access | Ensure that serial console or SSH access to the DUT is available from the PC/laptop. | Serial console or SSH access should be available and functional on the DUT.|
| 4 | Flash DUT with test firmware image | Flash the DUT with the test firmware image prior to the test. | The DUT should be successfully flashed with the test firmware image and booted up.|
| 5 | Configure DUT in XCONF with target firmware | Configure the DUT in the XCONF application with the target firmware image details as per the XCONF configuration guide available at <XCONF_Configuration_Guide_URL>. | The DUT should be correctly configured in XCONF with the target firmware image details.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify XCONF firmware update response | Execute the following command to verify the DUT can retrieve the XCONF firmware update response (replace <DUT_MAC> with the actual DUT MAC address).<br>Command: `curl <XCONF_Server_URL>/xconf/swu/stb?eStbMac=<DUT_MAC>` | The XCONF server should return a valid firmware update response payload containing firmwareFilename, firmwareVersion, firmwareLocation, and rebootImmediately fields.|
| 2 | Set XconfUrl RFC parameter | Set the XconfUrl RFC parameter to point to the required XCONF server instance.<br>Command: `tr181 -s -t string -v <XCONF_Server_URL> Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Bootstrap.XconfUrl` | The XconfUrl RFC should be set successfully. Verify using: `tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Bootstrap.XconfUrl` — the output should return <XCONF_Server_URL>.|
| 3 | Activate org.rdk.System plugin | Execute the following curl command to activate the org.rdk.System plugin.<br>Command: `curl -X POST http://0.0.0.0:9998/jsonrpc -d '}'` | The org.rdk.System plugin should be activated successfully.|
| 4 | Trigger XCONF firmware upgrade | Execute the following curl command to trigger the XCONF firmware upgrade.<br>Command: `curl -X POST http://127.0.0.1:9998/jsonrpc -d '}'` | The XCONF firmware upgrade should initiate successfully.|
| 5 | Monitor software update logs | Monitor the software update logs for upgrade progress and completion.<br>Command: `tail -f /opt/logs/swupdate.log` | No errors or abnormalities should be observed during the upgrade. The following success log entries should appear upon completion:<br>[mod=FWUPG, lvl=INFO] doCDL success.<br>[mod=FWUPG, lvl=INFO] Image Flashing is success|
| 6 | Reboot DUT if needed | If the rebootImmediately flag was not set to true in XCONF, reboot the DUT manually using the following command.<br>Command: `curl -X POST http://127.0.0.1:9998/jsonrpc -d '}'` | The DUT should reboot successfully. The RDK UI Home screen should be visible after the reboot.|
| 7 | Verify upgraded firmware version | Once the DUT is up after reboot, execute the following command to verify the updated firmware version.<br>Command: `cat /version.txt` | The firmware version in /version.txt should reflect the upgraded image version as configured in XCONF (e.g., imagename:<upgraded_image_name>).|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
