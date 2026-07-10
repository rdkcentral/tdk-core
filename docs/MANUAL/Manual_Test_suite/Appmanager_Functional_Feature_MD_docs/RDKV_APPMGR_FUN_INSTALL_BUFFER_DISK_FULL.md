## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_20
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_INSTALL_BUFFER_DISK_FULL

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the system behavior when the DUT disk space is full, validating that app download, installation, and launch operations fail gracefully with appropriate error handling when insufficient disk space is available.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Fill disk space using fallocate command | Navigate to /opt directory and execute fallocate command to use full memory :<br>cd /opt<br>fallocate -l <size to fillup> test.img | while checking the disk space using df -h it should show 100% usage for /opt |
| 2 | Navigate to More Apps page | Select More Apps button from Recommended Apps section and press enter/Ok button on remote | More Apps page should load where all apps available in App catalogue are visible |
| 3 | Select required app tile and press | Select required App tile and press enter/Ok button on remote | Selected App should not start installing since disk space is full instead an error message should be displayed based on disk space full |
| 4 | Select the installed app tile from | Select the Installed App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App shouldn't launch |
| 5 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | AV playback shouldn't start |
| 6 | Repeat disk-full failure steps for multiple apps | Perform steps 2 - 5 on multiple apps available in more Apps tab | Expected response should be same as step 2 - 5 |
| 7 | Close launched apps via Back key | Close/Exit the launched Apps by back key press on remote. | Launched App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
