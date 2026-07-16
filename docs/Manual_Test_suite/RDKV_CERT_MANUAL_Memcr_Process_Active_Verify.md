## TestCase ID
RDKV_MANUAL_MEMCR_01
## TestCase Name
RDKV_CERT_MANUAL_Memcr_Process_Active_Verify

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Memcr (checkpoint/restore) process is active and running on the DUT after a hardware reboot. This test exercises the `memcr` memory checkpoint and restore service together with the application lifecycle manager to validate suspend-and-resume behaviour of DAC applications. The test confirms that the Memcr service status should show Active: active (running). Example output: memcr.service - Memcr checkpoint restore service ... Active: active (running) with Main PID and CGroup entries populated.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned.|
| 3 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|
| 4 | Power-cycle DUT | Perform an AC power cycle (power OFF then power ON) on the DUT prior to the test. | The DUT should complete the power cycle and be ready for testing.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Perform AC power cycle on DUT | Perform an AC power cycle (power OFF then power ON) on the DUT to execute a hard reboot. | The DUT should reboot successfully without any unexpected behavior.|
| 2 | Verify Memcr service status | Once the DUT is up, execute the following command in the DUT serial console or SSH terminal to check the Memcr service status.<br>Command: `systemctl status memcr` | The Memcr service status should show Active: active (running). Example output: memcr.service - Memcr checkpoint restore service . Active: active (running) with Main PID and CGroup entries populated.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
