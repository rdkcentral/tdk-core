## TestCase ID
RDKV_MANUAL_WIFI_01
## TestCase Name
RDKV_CERT_MANUAL_Wifi_Startup_SSID_Connect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a user can successfully connect to an available Wi-Fi SSID from the startup network selection screen. This test exercises the RDK UI Network Configuration settings, the Wi-Fi connection manager (`wpa_supplicant`), and the network interface stack to validate the targeted Wi-Fi connectivity behaviour. The test confirms that the application should install and launch successfully. Video playback should start with proper audio and video output.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Flash DUT or factory reset | Flash the DUT freshly prior to the test. If Wi-Fi is being tested after other tests have already been conducted, perform a factory reset via Settings > Other Settings > Advanced Settings > Device to restore the startup screens on the next boot. | The DUT should be freshly flashed or factory reset, and the startup screens should be restored on the next boot. |
| 3 | Connect Ethernet cable | Connect the Ethernet cable to the DUT and ensure a valid Ethernet IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT. |
| 4 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. Refer to the Bluetooth Remote test module for pairing instructions. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 5 | Complete language selection | Complete language selection from the startup screen and navigate to the Network Configuration screen. | The language selection should be completed and the Network Configuration screen should be displayed. |
| 6 | Ensure same network | Ensure the DUT and the PC/laptop used for SSH are on the same network. | The DUT and the PC/laptop should be on the same network. |
| 7 | Connect serial cable | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized. |
| 8 | Configure serial terminal | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT. |
| 9 | Install SSH client | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Select WiFi interface | Select "WiFi" on the Network Configuration screen. | The Wi-Fi network selection screen should be displayed, listing all available SSIDs (both 2.4 GHz and 5 GHz bands). |
| 2 | Select available SSID | Select any available SSID from the list. | The password entry screen should launch with an on-screen keyboard and Connect/Cancel buttons. |
| 3 | Enter password and connect | Enter the correct password using the on-screen keyboard and press the Connect button. | The DUT should connect to the selected SSID. The Wi-Fi network selection screen should briefly display with the connected SSID in a ticked state, followed by the RDK UI Home screen launching automatically. |
| 4 | Verify IP via SSH ifconfig | SSH to the DUT via its Ethernet IP address and execute the ifconfig command.<br>Command: `ifconfig` | The SSH connection should be established. The command output should list both eth0 and wlan0 interfaces, each with their respective IP addresses. |
| 5 | Disconnect Ethernet and check ifconfig | Disconnect the Ethernet cable from the DUT and execute the ifconfig command in the DUT serial console.<br>Command: `ifconfig` | The ifconfig output should display a valid IP address for the wlan0 interface. The eth0 interface should not display an IP address. |
| 6 | SSH via wlan0 IP | SSH to the DUT using the wlan0 IP address obtained in Step 5. | The SSH connection should be established successfully using the wlan0 IP address. |
| 7 | Verify internet via ping | In the SSH console, execute the ping command.<br>Command: `ping google.com` | Ping packets should be transmitted and received successfully, confirming internet connectivity via Wi-Fi. |
| 8 | Launch video app and play | On the RDK UI Home screen, install a video application (such as YouTube), launch it, and attempt to play any video. | The application should install and launch successfully. Video playback should start with proper audio and video output. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
