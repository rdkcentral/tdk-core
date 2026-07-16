## TestCase ID
RDKV_MANUAL_IMG_UPGRADE_05
## TestCase Name
RDKV_CERT_MANUAL_Img_Upgrade_Xconf_User_Settings_Persist

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a XCONF firmware upgrade does not affect user-specific settings, application sign-in states, network connections, and Bluetooth remote pairing. This test exercises the RDK CDL (Code Download) service and the firmware upgrade stack (`XCONF` server configuration, SNMP triggers, or local USB/HTTP methods) to validate the firmware upgrade workflow. The test confirms that the following should persist after the firmware upgrade: YouTube, Prime Video, and Netflix sign-in states should remain active; the Wi-Fi connection should remain connected; the Bluetooth remote should remain paired and all key presses should….

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect Ethernet cable | Connect the Ethernet cable to the DUT and ensure a valid IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 3 | Pair Bluetooth remote and verify key presses | Pair and connect the Bluetooth remote to the DUT, and confirm that all key presses are functional. | The Bluetooth remote should be paired, connected, and all key presses should respond correctly on the DUT.|
| 4 | Sign in to streaming applications | Sign in to the YouTube, Prime Video, and Netflix applications with valid user credentials prior to the test. | Sign-in should succeed for all three applications and the accounts should remain active on the DUT.|
| 5 | Change display and audio settings to non-default | Change the display resolution and audio mode to non-default values prior to the test. | The display resolution and audio mode should be changed to the specified non-default values on the DUT.|
| 6 | Connect DUT to Wi-Fi SSID | Connect the DUT to a Wi-Fi SSID prior to the test. | The DUT should be connected to the Wi-Fi SSID with a valid IP address assigned.|
| 7 | Flash DUT with test firmware image | Flash the DUT with the test firmware image prior to the test. | The DUT should be successfully flashed with the test firmware image and booted up.|
| 8 | Configure DUT in XCONF with target firmware | Configure the DUT in the XCONF application with the target firmware image details as per the XCONF configuration guide at <XCONF_Configuration_Guide_URL>. | The DUT should be correctly configured in XCONF with the target firmware image details.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify XCONF firmware update response | Execute the following command to verify the DUT can retrieve the XCONF firmware update response (replace <DUT_MAC> with the actual DUT MAC address).<br>Command: `curl <XCONF_Server_URL>/xconf/swu/stb?eStbMac=<DUT_MAC>` | The XCONF server should return a valid firmware update response payload containing firmwareFilename, firmwareVersion, firmwareLocation, and rebootImmediately fields.|
| 2 | Set XconfUrl RFC parameter | Set the XconfUrl RFC parameter to point to the required XCONF server instance.<br>Command: `tr181 -s -t string -v <XCONF_Server_URL> Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Bootstrap.XconfUrl` | The XconfUrl RFC should be set successfully. Verify using: `tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Bootstrap.XconfUrl` — the output should return <XCONF_Server_URL>.|
| 3 | Navigate to firmware upgrade screen | Navigate to Settings > Other Settings > Advanced Settings > Device > Check for Firmware Upgrade and select it. | The Firmware Update screen should launch with all upgrade-related options and fields visible.|
| 4 | Initiate firmware upgrade via RDK UI | Select the "Check for Update" button. | The XCONF firmware upgrade should initiate.|
| 5 | Monitor software update logs | Monitor the software update logs for upgrade progress and completion.<br>Command: `tail -f /opt/logs/swupdate.log` | No errors or abnormalities should be observed during the upgrade. The following success log entries should appear upon completion:<br>[mod=FWUPG, lvl=INFO] doCDL success.<br>[mod=FWUPG, lvl=INFO] Image Flashing is success|
| 6 | Reboot DUT if needed | If rebootImmediately was not set to true, reboot the DUT manually.<br>Command: `curl -X POST http://127.0.0.1:9998/jsonrpc -d '}'` | The DUT should reboot successfully. The RDK UI should be displayed after reboot.|
| 7 | Verify upgraded firmware version | Verify the upgraded firmware version via RDK UI or console.<br>Command: `cat /version.txt` | The firmware version should reflect the upgraded image version.|
| 8 | Verify user settings persist after upgrade | Verify that all user-specific settings configured in the preconditions are preserved after the firmware upgrade. | The following should persist after the firmware upgrade: YouTube, Prime Video, and Netflix sign-in states should remain active; the Wi-Fi connection should remain connected; the Bluetooth remote should remain paired and all key presses should respond correctly; user-specific RDK UI settings (e.g., resolution, audio mode) should be retained.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
