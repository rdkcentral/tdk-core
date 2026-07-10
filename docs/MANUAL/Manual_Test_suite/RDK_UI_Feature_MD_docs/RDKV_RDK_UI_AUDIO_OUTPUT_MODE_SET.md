## TestCase ID
RDKV_MANUAL_RDKUI_09
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_AUDIO_OUTPUT_MODE_SET

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the available audio output modes can be set and applied via the RDK UI Settings.

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
| 1 | Launch Audio Settings screen | Launch Settings / Audio screen | Screen should launch and selected output mode should be seen |
| 2 | Open Audio Output Mode selection | Click on  Output Mode | The Output Mode screen should launch listing the supported audio output modes(Eg:Stereo, Passthru, Auto(Dolby Digital Plus)). The current mode should be indicated with a tick mark. |
| 3 | Select audio output mode | Select the first audio mode if its not the current one. Else select the next one | Tick mark will shift to the newly selected audio mode. |
| 4 | Press back button | Press Back button | Settings / Audio Screen should launch and selected audio mode will be displayed against Output Mode |
| 5 | Press Home button to go to Home screen | Press Home Button | RDK UI Home screen should launch |
| 6 | Launch app and verify audio output | Open any app which can play audio and play any content | App should launch and upon playing the content audio should be as expected / without errors heard |
| 7 | Repeat steps 3 to 6 for | Repeat steps 3 to 6 for all audio modes available in Settings/Audio/Output Mode screen | Expected results are similar to steps 3 to 6 |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
