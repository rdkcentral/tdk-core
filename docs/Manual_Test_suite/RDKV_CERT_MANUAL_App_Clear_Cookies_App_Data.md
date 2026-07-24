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
To validate that enabling the Clear Cookies and App Data option in the Privacy settings clears all application login sessions on the DUT. This test confirms that all affected applications prompt the user to sign in again after the data is cleared, ensuring that privacy controls function correctly for certification.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT | Ensure the DUT is powered on prior to this test. | The DUT should be powered on successfully.|
| 2 | Connect display and network to DUT | Connect a display to the DUT and select the correct HDMI source. Connect the DUT to Ethernet or Wi-Fi with active internet access. | The display should be connected to the DUT and the correct HDMI source should be selected. The DUT should be connected to the network with active internet access.|
| 3 | Install YouTube and Amazon Prime apps | If YouTube or Amazon Prime Video is not already installed, select their tile from the Recommended Apps row of the RDK UI Home screen and press Enter/OK to install. Skip this step if they are already available in the My Apps section. | YouTube and Amazon Prime Video should be installed and available in the My Apps section/row of the RDK UI Home screen. If already installed, this step may be skipped.|
| 4 | Sign in to YouTube and Amazon Prime Video | Ensure YouTube and Amazon Prime Video are logged in with valid user credentials on the DUT. | YouTube and Amazon Prime Video should be signed in with valid user credentials on the DUT.|
| 5 | Verify playback in YouTube and Amazon Prime Video | Launch YouTube and Amazon Prime Video from the RDK UI Home screen and verify that audio and video playback is working correctly in each app prior to test execution. | YouTube and Amazon Prime Video should launch successfully and AV playback should be verified as working correctly prior to test execution.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Settings | In RDK UI, navigate to Settings → Other Settings → Privacy. | The Privacy screen should load and display the available options including: Local Device Discovery, USB Media Devices, Audio Input, Clear Cookies and App Data, Privacy Policy, and License.|
| 2 | Enable Clear Cookies and App Data option | Select and enable the Clear Cookies and App Data radio button. | The radio button should activate for a few seconds and then automatically deactivate. A success message should be displayed alongside the Clear Cookies and App Data option.|
| 3 | Verify login sessions cleared in all apps | Open YouTube, Amazon Prime Video, and Netflix and validate whether the login sessions have been cleared. | In all the mentioned applications, login sessions should be cleared and the applications should prompt the user to sign in again.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
