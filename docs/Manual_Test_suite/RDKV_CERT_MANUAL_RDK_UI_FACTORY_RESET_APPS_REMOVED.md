## TestCase ID
RDKV_MANUAL_RDKUI_34
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Factory_Reset_Apps_Removed

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that after a Factory Reset is performed from the RDK UI Settings, all user-installed apps are removed from the RDK UI Home screen. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that the user should return to the previous screen.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Ensure multiple apps are installed | Ensure multiple apps are already installed on the DUT and listed under My Apps. | Multiple apps should be installed and visible in the My Apps section. |
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Initiate Factory Reset from Settings | From RDK UI Home screen, navigate to Settings / Other Settings / Advanced Settings / Device / Factory Reset and press on Factory Reset | Confirmation message should ask if we want to do the action |
| 2 | Click OK/Confirm button | Click on OK button | The DUT should perform a Factory Reset and reboot. |
| 3 | Verify My Apps row removed after Factory Reset | Once the UI is up, observe the RDK UI Home page | All the user installed apps should be deleted and the My Apps row should no longer be visible. The home page of the UI should have only two rows - Recommended Apps and Video on Demand. |
| 4 | Open App Info page to verify no apps | Click on the App Info button in the left pane of RDK UI Home screen | An informational message stating "No Apps Installed" should be displayed. |
| 5 | Press on ok button in the | Press on OK button in the message | The user should return to the previous screen. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
