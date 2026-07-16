## TestCase ID
RDKV_MANUAL_APPS_27
## TestCase Name
RDKV_CERT_MANUAL_App_Clear_Cookies_App_Data

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that enabling the Clear Cookies and App Data option in the Privacy settings clears all application login sessions on the DUT. This test exercises the DAC App Manager service, the RDK UI Home screen Recommended Apps / More Apps tiles, and the App Info page to manage application installation and launch. The test confirms that in all the mentioned applications, login sessions should be cleared and the applications should prompt the user to sign in again.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT | Ensure the DUT is powered on prior to this test. | The DUT should be powered on successfully.|
| 2 | Connect display to DUT | Connect a display to the DUT and select the correct HDMI source. | The display should be connected to the DUT and the correct HDMI source should be selected.|
| 3 | Sign in to YouTube, Amazon Prime Video, and Netflix | Ensure YouTube, Amazon Prime Video, and Netflix are logged in with valid user credentials on the DUT (if these applications are available). | YouTube, Amazon Prime Video, and Netflix should be signed in with valid user credentials on the DUT.|
| 4 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Settings | In RDK UI, navigate to Settings → Other Settings → Privacy. | The Privacy screen should load and display the available options including: Local Device Discovery, USB Media Devices, Audio Input, Clear Cookies and App Data, Privacy Policy, and License.|
| 2 | Enable Clear Cookies and App Data option | Select and enable the Clear Cookies and App Data radio button. | The radio button should activate for a few seconds and then automatically deactivate. A success message should be displayed alongside the Clear Cookies and App Data option.|
| 3 | Verify login sessions cleared in all apps | Open YouTube, Amazon Prime Video, and Netflix and validate whether the login sessions have been cleared. | In all the mentioned applications, login sessions should be cleared and the applications should prompt the user to sign in again.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
