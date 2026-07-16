## TestCase ID
RDKV_MANUAL_BLUETOOTH_11
## TestCase Name
RDKV_CERT_MANUAL_BTRemote_RepairViaKeySequence

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a Bluetooth remote can be successfully re-paired with the DUT using the pairing key sequence after remote pairing has been intentionally removed via the Thunder (WPEFramework) API. This test exercises the RDK Bluetooth pairing stack, the remote-control key-mapping service, and the RDK UI to validate remote-control button behaviour. The test confirms that the remote should pair and connect back to the DUT automatically after a few seconds. All key presses should respond correctly, confirming successful re-pairing.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the DUT to an active network via Ethernet prior to the test. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 2 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 3 |  Conduct test in isolated environment  | Conduct the test in an isolated environment free of other VA/Bluetooth devices to prevent unintended Bluetooth interference. | The test environment should be free of Bluetooth interference from other devices.|
| 4 |  Ensure bluetooth remote already paired  | Ensure the Bluetooth remote is successfully paired with the DUT and all key presses are confirmed to be functioning correctly prior to the test. | The Bluetooth remote should be paired and all key presses should be functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Reboot DUT  | Reboot the DUT and wait for the RDK UI Home screen to appear. | The DUT should reboot successfully and the RDK UI Home screen should be displayed.|
| 2 |  Activate bluetooth plugin via API  | Execute the following curl command via the DUT serial console or SSH session to activate the org.rdk.Bluetooth plugin:<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be activated successfully.|
| 3 |  Retrieve connected device ID  | Retrieve the connected Bluetooth remote's device ID using the following curl command:<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The response should contain the connected remote's device ID.|
| 4 |  Unpair remote via API  | Unpair the remote using the device ID retrieved in Step 3 with the following curl command (replace <deviceID> with the actual device ID obtained):<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<deviceID>"}}' http://127.0.0.1:9998/jsonrpc` | The DUT should successfully unpair the remote with the specified device ID.|
| 5 |  Clear remote pairing information  | Clear the pairing information from the remote by pressing and holding the CH UP and VOL DOWN keys simultaneously for a few seconds. | The red LED on the remote should blink once and stop, indicating that the pairing information has been successfully cleared from the remote.|
| 6 |  Put remote into pairing mode  | Put the remote into pairing mode by pressing and holding the OK and CH UP keys simultaneously for a few seconds. | The red LED on the remote should blink continuously, indicating that the remote has entered pairing mode.|
| 7 |  Validate re-pairing and key presses  | Wait for the DUT to detect and pair with the remote, then perform key presses using the remote. | The remote should pair and connect back to the DUT automatically after a few seconds. All key presses should respond correctly, confirming successful re-pairing.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
