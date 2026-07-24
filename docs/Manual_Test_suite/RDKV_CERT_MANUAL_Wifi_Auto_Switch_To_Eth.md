## TestCase ID
RDKV_MANUAL_WIFI_05
## TestCase Name
RDKV_CERT_MANUAL_Wifi_Auto_Switch_To_Eth

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT automatically switches to the Ethernet interface when an Ethernet cable is reconnected while the device is connected to a Wi-Fi network. This test confirms that internet connectivity is restored via Ethernet and content playback resumes successfully, ensuring automatic Wi-Fi to Ethernet failover meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 |  Ensure DUT connected to Wi-Fi  | Ensure that the DUT is already connected to a Wi-Fi network prior to the test. | The DUT should have an active Wi-Fi connection with a valid IP address.|
| 3 |  Disconnect Ethernet cable  | Disconnect the Ethernet cable from the DUT. | The Ethernet cable should be disconnected from the DUT.|
| 4 |  Pair bluetooth remote  | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 5 |  Ensure DUT and PC on same network  | Ensure that the DUT and the PC/laptop used for SSH are connected to the same network. | The DUT and PC/laptop should be on the same network and reachable from each other.|
| 6 |  Connect serial cable  | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized.|
| 7 |  Configure serial terminal  | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT.|
| 8 |  Install SSH client  | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Open network configuration  | Navigate to Settings > Network Configuration from the RDK UI Home screen. | The Network Configuration screen should load with the Network Interface value displayed as WiFi.|
| 2 |  Verify Wi-Fi network info  | Select "Network Info" and press OK. | The Network Info screen should load displaying the connected Wi-Fi SSID details and the wlan0 IP address with all fields correctly populated.|
| 3 |  Navigate Back to network config  | Press Back to return to the Network Configuration screen. | The Network Configuration screen should reload with the Network Interface value displayed as WiFi.|
| 4 |  Reconnect Ethernet cable  | Reconnect the Ethernet cable to the DUT. | The Network Interface value on the Network Configuration screen should automatically change from WiFi to ETHERNET.|
| 5 |  Verify Ethernet network info  | Navigate to "Network Info" and press OK. | The Network Info screen should load displaying Ethernet interface details. Wi-Fi details should no longer be displayed as the active interface.|
| 6 |  SSH via Ethernet IP  | SSH to the DUT using the Ethernet IP address shown on the Network Info screen. | The SSH connection should be established successfully using the Ethernet IP address.|
| 7 |  Verify both interfaces via ifconfig  | In the SSH console, execute the ifconfig command.<br>Command: `ifconfig` | The output should display both eth0 and wlan0 interfaces, each with their respective IP addresses.|
| 8 |  Verify internet via ping  | In the SSH console, execute the ping command.<br>Command: `ping google.com` | Ping packets should be transmitted and received successfully, confirming internet connectivity via Ethernet.|
| 9 |  Validate content playback  | On the RDK UI Home screen, open any application that requires internet and play any content. | The application should open successfully and content playback should start with proper audio and video output.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
