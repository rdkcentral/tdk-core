## TestCase ID
RDKV_MANUAL_IMAGEUPGRADE_04
## TestCase Name
RDKV_CERT_MANUAL_IMG_UPGRADE_XCONF_VIA_RDK_UI

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the XCONF firmware upgrade behavior when initiated directly from the RDK UI Settings menu.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Connect Ethernet cable | Connect the Ethernet cable to the DUT and ensure a valid IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT. |
| 3 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 4 | Flash DUT with test firmware image | Flash the DUT with the test firmware image prior to the test. | The DUT should be successfully flashed with the test firmware image and booted up. |
| 5 | Configure DUT in XCONF with target firmware | Configure the DUT in the XCONF application with the target firmware image details as per the XCONF configuration guide at <XCONF_Configuration_Guide_URL>. | The DUT should be correctly configured in XCONF with the target firmware image details. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify XCONF firmware update response | Execute the following command to verify the DUT can retrieve the XCONF firmware update response (replace <DUT_MAC> with the actual DUT MAC address).<br>Command: `curl <XCONF_Server_URL>/xconf/swu/stb?eStbMac=<DUT_MAC>` | The XCONF server should return a valid firmware update response payload containing firmwareFilename, firmwareVersion, firmwareLocation, and rebootImmediately fields. |
| 2 | Set XconfUrl RFC parameter | Set the XconfUrl RFC parameter to point to the required XCONF server instance.<br>Command: `tr181 -s -t string -v <XCONF_Server_URL> Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Bootstrap.XconfUrl` | The XconfUrl RFC should be set successfully. Verify using: `tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Bootstrap.XconfUrl` — the output should return <XCONF_Server_URL>. |
| 3 | Navigate to firmware upgrade screen | Navigate to Settings > Other Settings > Advanced Settings > Device > Check for Firmware Upgrade and select it. | The Firmware Update screen should launch, displaying the "Check for Update" button, current Firmware State, Firmware Versions, and Downloaded Firmware Version fields. |
| 4 | Initiate firmware upgrade via RDK UI | Select the "Check for Update" button. | The XCONF firmware upgrade should initiate. |
| 5 | Observe upgrade progress on RDK UI | Observe the XCONF image upgrade progress and status on the RDK UI. | The RDK UI should sequentially display the upgrade status: Requesting → Preparing to download → Downloading (with percentage) → Flashing in progress. Upon successful download, the Downloaded Firmware Version field should display the new image name. |
| 6 | Reboot DUT if needed | If rebootImmediately was not set to true in XCONF, reboot the DUT manually from the RDK UI or via the Thunder API.<br>Command: `curl -X POST http://127.0.0.1:9998/jsonrpc -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.reboot","params":{"rebootReason":"FW Update Test"}}'` | The DUT should reboot successfully. The RDK UI should be displayed after reboot. |
| 7 | Verify upgraded firmware version via RDK UI | After reboot, navigate to Settings > Other Settings > Advanced Settings > Device > Check for Firmware Upgrade and verify the firmware version. | The Firmware Update screen should show the upgraded firmware image version in the Firmware Versions field. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
