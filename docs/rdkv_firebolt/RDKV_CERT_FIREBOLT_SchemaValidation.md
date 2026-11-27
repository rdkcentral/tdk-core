## TestCase ID
RDKV_CERT_FIREBOLT_01
## TestCase Name
RDKV_CERT_FIREBOLT_SchemaValidation

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Coverage](#head.Coverage)
  - [Accessibility](#head.Module.Accessibility)
  - [Actions](#head.Module.Actions)
  - [Advertising](#head.Module.Advertising)
  - [Device](#head.Module.Device)
  - [Discovery](#head.Module.Discovery)
  - [Display](#head.Module.Display)
  - [Lifecycle2](#head.Module.Lifecycle2)
  - [Localization](#head.Module.Localization)
  - [Metrics](#head.Module.Metrics)
  - [Network](#head.Module.Network)
  - [SpeechSynthesis](#head.Module.SpeechSynthesis)
  - [Stats](#head.Module.Stats)
  - [TextToSpeech](#head.Module.TextToSpeech)
  - [VideoOutput](#head.Module.VideoOutput)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Firebolt APIs and events on the device conform to the Firebolt OpenRPC schema. The Firebolt certification application is installed and launched on the device, and it invokes each API and event in the Firebolt spec. Every API response is validated against its schema for required fields, data types, allowed values and undocumented fields. Every event subscription and unsubscription must be acknowledged successfully. The results are published as JSON, HTML and Excel reports and collected by the TDK framework.

<a name="head.Coverage"></a>
## Coverage
The test covers 67 APIs and 24 events across 14 Firebolt modules, listed below by module in the order they are executed. `Lifecycle2.close` is excluded by default because it would close the certification application. The status, parameters, expected response format, actual response and failure reason of every API and event are recorded in the reports.
### Modules

<a name="head.Module.Accessibility"></a>
#### Accessibility

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Accessibility.audioDescription`|API|Returns the audio description setting of the device|None|Result must be a boolean|
|2|`Accessibility.onAudioDescriptionChanged`|Event|Notifies when the audio description setting changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|3|`Accessibility.closedCaptionsSettings`|API|Returns closed captions settings: enabled, and a list of zero or more preferred languages in decreasing order of preference|None|Result must be an object with `enabled` (boolean), `preferredLanguages` (array of string (pattern `^[a-z]{3}$`)). No other properties allowed|
|4|`Accessibility.onClosedCaptionsSettingsChanged`|Event|Notifies when closed captions settings change|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|5|`Accessibility.highContrastUI`|API|Returns the high contrast UI device setting|None|Result must be a boolean|
|6|`Accessibility.onHighContrastUIChanged`|Event|Notifies when the high contrast UI setting changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|7|`Accessibility.voiceGuidanceSettings`|API|Returns voice guidance settings: enabled, rate, and navigationHints|None|Result must be an object with `enabled` (boolean), `rate` (number (0.1 to 10)), `navigationHints` (boolean). No other properties allowed|
|8|`Accessibility.onVoiceGuidanceSettingsChanged`|Event|Notifies when voice guidance settings change|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|

<a name="head.Module.Actions"></a>
#### Actions

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Actions.start`|API|Send an intent to the platform. Argument is a JSON document|`{"intent": {"action": "search", "data": {"query": "tdk-test"}, "context": {"source": "voice"}}}`|Result must be `null`|
|2|`Actions.intent`|API|Returns the intent that was most recently received from the platform, as a JSON document. Typically called after transitioning to the active lifecycle state|None|Result must be an object with `intentId` (integer (>= 0)), `intent` (JSON object). No other properties allowed|
|3|`Actions.onIntent`|Event|Notifies when a new intent is received from the platform|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|

<a name="head.Module.Advertising"></a>
#### Advertising

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Advertising.advertisingId`|API|Returns the IFA (Identifier for Advertising)|None|Result must be an object with `ifa` (string (pattern-validated)), `ifa_type` (one of `dpid`, `sspid`, `sessionid`), `lmt` (one of `0`, `1`). No other properties allowed|

<a name="head.Module.Device"></a>
#### Device

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Device.uid`|API|Returns a persistent unique UUID for the current app and device. Reset when the app or device is reset|None|Result must be a string (pattern-validated)|
|2|`Device.deviceClass`|API|Returns the class of the device|None|Result must be one of `ott`, `stb`, `tv`|
|3|`Device.uptime`|API|Returns the number of seconds since most recent device boot, including any time spent during deep sleep|None|Result must be an integer (>= 0)|
|4|`Device.timeInActiveState`|API|Returns the number of seconds since the device transitioned to the ON power state|None|Result must be an integer (>= 0)|
|5|`Device.chipsetId`|API|Returns chipset ID as a printable string, e.g. 'BCM72180'|None|Result must be a string|
|6|`Device.hdr`|API|Returns the HDR standards supported by the attached TV or the integral display|None|Result must be an object with `hdr10` (boolean), `hdr10Plus` (boolean), `dolbyVision` (boolean), `hlg` (boolean). No other properties allowed|
|7|`Device.onHdrChanged`|Event|Notifies when supported HDR standards change|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|8|`Device.dolbyAtmosExperienceAvailable`|API|Returns whether the user would get a Dolby Atmos experience if a Dolby Atmos track were played now|None|Result must be a boolean|
|9|`Device.onDolbyAtmosExperienceAvailableChanged`|Event|Notifies when Dolby Atmos experience availability changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|10|`Device.osName`|API|Returns the operating system name as defined by the operator|None|Result must be a string|
|11|`Device.osVersion`|API|Returns the operating system version as defined by the operator|None|Result must be a string|
|12|`Device.firmware`|API|Returns a string that identifies the firmware image of the device|None|Result must be a string|
|13|`Device.name`|API|Returns the device friendly name, used by network services (DIAL, Miracast, AirPlay) for device discovery|None|Result must be a string|
|14|`Device.onNameChanged`|Event|Notifies when the device friendly name changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|

<a name="head.Module.Discovery"></a>
#### Discovery

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Discovery.watched`|API|Notify the platform that content has been partially or completely watched|`{"entityId": "entity-xyz-123", "progress": 0.95, "completed": true, "watchedOn": "2026-10-28T06:00:00.000Z", "agePolicy": "app:adult"}`|Result must be `null`|

<a name="head.Module.Display"></a>
#### Display

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Display.size`|API|Returns the physical dimensions of the connected or integral display, in centimeters|None|Result must be an object with `width` (integer (>= 0)), `height` (integer (>= 0)). No other properties allowed|
|2|`Display.maxResolution`|API|Returns the physical/native resolution of the connected or integral display, in pixels|None|Result must be an object with `width` (integer (>= 0)), `height` (integer (>= 0)). No other properties allowed|
|3|`Display.edid`|API|Returns the EDID (and extensions) of the connected or integral display, as a Base64 encoded string|None|Result must be a string (pattern-validated)|
|4|`Display.colorimetry`|API|Returns an unordered list of colorimetry values supported by the attached TV or integral display|None|Result must be an array of one of `bt709`, `bt2020`|
|5|`Display.videoResolutions`|API|Returns an unordered list of HD video resolutions and frame rates supported by the attached TV or integral display|None|Result must be an array of one of `720p50`, `720p60`, `1080p50`, `1080p60`, `2160p50`, `2160p60`|

<a name="head.Module.Lifecycle2"></a>
#### Lifecycle2

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Lifecycle2.close`|API|Request the platform to deactivate the app, and possibly take further action|`{"type": "deactivate"}`|Not executed. Excluded by default (`EXCLUDED_METHODS`) because it would close the certification application|
|2|`Lifecycle2.state`|API|Returns the current lifecycle state of the app|None|Result must be one of `initializing`, `active`, `paused`, `suspended`, `hibernated`, `terminating`|
|3|`Lifecycle2.onStateChanged`|Event|Notifies on lifecycle state changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|

<a name="head.Module.Localization"></a>
#### Localization

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Localization.country`|API|Returns the country, e.g. US, CA, GB, BE|None|Result must be a string (pattern `^([A-Z]{2})?$`)|
|2|`Localization.onCountryChanged`|Event|Notifies when the device country changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|3|`Localization.preferredAudioLanguages`|API|A list of zero or more languages in order of decreasing preference|None|Result must be an array of string (pattern `^[a-z]{3}$`)|
|4|`Localization.onPreferredAudioLanguagesChanged`|Event|Notifies when preferred audio languages change|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|5|`Localization.presentationLanguage`|API|The presentation language of the device, e.g. en-US|None|Result must be a string (pattern `^([A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*)?$`)|
|6|`Localization.onPresentationLanguageChanged`|Event|Notifies when the presentation language changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|7|`Localization.timeZone`|API|Returns the current time zone in IANA format, e.g. America/New_York|None|Result must be a string (pattern-validated)|
|8|`Localization.onTimeZoneChanged`|Event|Notifies when the time zone changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|

<a name="head.Module.Metrics"></a>
#### Metrics

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Metrics.ready`|API|Inform the platform that the app is minimally usable|None|Result must be `null`|
|2|`Metrics.signIn`|API|Log a sign in event|None|Result must be `null`|
|3|`Metrics.signOut`|API|Log a sign out event|None|Result must be `null`|
|4|`Metrics.startContent`|API|Inform the platform that your user has started content|`{"entityId": "content-1", "agePolicy": "app:adult"}`|Result must be `null`|
|5|`Metrics.stopContent`|API|Inform the platform that your user has stopped content|`{"entityId": "content-1", "agePolicy": "app:adult"}`|Result must be `null`|
|6|`Metrics.page`|API|Inform the platform that your user has navigated to a page or view|`{"pageId": "home"}`|Result must be `null`|
|7|`Metrics.error`|API|Inform the platform of an error that has occurred in your app|`{"type": "other", "code": "ERR_0", "description": "Unspecified error", "visible": false, "parameters": {"retryCount": 0, "source": "player"}}`|Result must be `null`|
|8|`Metrics.mediaLoadStart`|API|Called when setting the URL of a media asset to play, in order to infer load time|`{"entityId": "content-1"}`|Result must be `null`|
|9|`Metrics.mediaPlay`|API|Called when media playback should start due to autoplay, user-initiated play, or unpausing|`{"entityId": "content-1"}`|Result must be `null`|
|10|`Metrics.mediaPlaying`|API|Called when media playback actually starts due to autoplay, user-initiated play, unpausing, or recovering from a buffering interruption|`{"entityId": "content-1"}`|Result must be `null`|
|11|`Metrics.mediaPause`|API|Called when media playback will pause due to an intentional pause operation|`{"entityId": "content-1"}`|Result must be `null`|
|12|`Metrics.mediaWaiting`|API|Called when media playback will halt due to a network, buffer, or other unintentional constraint|`{"entityId": "content-1"}`|Result must be `null`|
|13|`Metrics.mediaSeeking`|API|Called when a seek is initiated during media playback|`{"entityId": "content-1", "target": 0}`|Result must be `null`|
|14|`Metrics.mediaSeeked`|API|Called when a seek is completed during media playback|`{"entityId": "content-1", "position": 0}`|Result must be `null`|
|15|`Metrics.mediaRateChanged`|API|Called when the playback rate of media is changed|`{"entityId": "content-1", "rate": 1}`|Result must be `null`|
|16|`Metrics.mediaRenditionChanged`|API|Called when the playback rendition (e.g. bitrate, dimensions, profile) is changed|`{"entityId": "content-1", "bitrate": 5000, "width": 1920, "height": 1080, "profile": "HDR10"}`|Result must be `null`|
|17|`Metrics.mediaEnded`|API|Called when playback has stopped because the end of the media was reached|`{"entityId": "content-1"}`|Result must be `null`|
|18|`Metrics.event`|API|Inform the platform of 1st party distributor metrics data|`{"schema": "xrn:firebolt:metrics", "data": "{}"}`|Result must be `null`|
|19|`Metrics.appInfo`|API|Inform the platform about an app's build info|`{"build": "1.0.0"}`|Result must be `null`|

<a name="head.Module.Network"></a>
#### Network

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Network.connected`|API|Returns whether the device has a usable network connection|None|Result must be a boolean|
|2|`Network.onConnectedChanged`|Event|Notifies when network connectivity changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|

<a name="head.Module.SpeechSynthesis"></a>
#### SpeechSynthesis

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`SpeechSynthesis.voices`|API|Returns a list of available voices|None|Result must be an array of objects, each: `name` (string), `lang` (string (pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$`)), `default` (boolean). No other properties allowed|
|2|`SpeechSynthesis.onVoicesChanged`|Event|Notifies when the available voices change|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|3|`SpeechSynthesis.speak`|API|Requests the system to speak an utterance. Returns an utteranceId if accepted|`{"text": "Hello", "lang": "en-US"}`|Result must be an integer (>= 0)|
|4|`SpeechSynthesis.cancel`|API|Stop the utterance|`{"utteranceId": 1}`|Result must be `null`|
|5|`SpeechSynthesis.pause`|API|Pause the utterance|`{"utteranceId": 1}`|Result must be `null`|
|6|`SpeechSynthesis.resume`|API|Resume a paused or synthesizing utterance|`{"utteranceId": 1}`|Result must be `null`|
|7|`SpeechSynthesis.onUtteranceEvent`|Event|Notifies events related to an utterance|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|

<a name="head.Module.Stats"></a>
#### Stats

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`Stats.memoryUsage`|API|Returns information about container memory usage, in bytes|None|Result must be an object with `userMemoryUsed` (integer (>= 0)), `userMemoryLimit` (integer (>= 0)), `gpuMemoryUsed` (integer (>= 0)), `gpuMemoryLimit` (integer (>= 0)). No other properties allowed|

<a name="head.Module.TextToSpeech"></a>
#### TextToSpeech

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`TextToSpeech.speak`|API (deprecated)|Speak the utterance immediately. Any ongoing speech is interrupted|`{"text": "Hello"}`|Result must be an object with `speechid` (integer (>= 0)), `TTS_Status` (one of `0`, `1`, `2`, `3`), `success` (boolean). No other properties allowed|
|2|`TextToSpeech.cancel`|API (deprecated)|Stop speaking if an utterance is currently being spoken. Raises onSpeechInterrupted if speaking was interrupted|`{"speechid": 1}`|Result must be an object with `TTS_Status` (one of `0`, `1`, `2`, `3`), `success` (boolean). No other properties allowed|
|3|`TextToSpeech.onSpeechComplete`|Event (deprecated)|Speech completed successfully|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|4|`TextToSpeech.onSpeechInterrupted`|Event (deprecated)|Speech was stopped, due to another call to speak or cancel|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|5|`TextToSpeech.onNetworkError`|Event (deprecated)|Utterance failed due to network|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|6|`TextToSpeech.onPlaybackError`|Event (deprecated)|Utterance failed during playback|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|

<a name="head.Module.VideoOutput"></a>
#### VideoOutput

|#|API / Event|Type|What it does|Parameters passed|Expected result|
|-|-----------|----|------------|-----------------|---------------|
|1|`VideoOutput.resolution`|API|Returns the width and height of the video signal on the video output, in pixels|None|Result must be an object with `width` (integer (>= 0)), `height` (integer (>= 0)). No other properties allowed|
|2|`VideoOutput.onResolutionChanged`|Event|Notifies when the video output resolution changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|3|`VideoOutput.hdcp`|API|Returns the current state of output protection on the video output|None|Result must be one of `hdcp1.4`, `hdcp2.2`, `none`, `direct`|
|4|`VideoOutput.onHdcpChanged`|Event|Notifies when HDCP state changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|5|`VideoOutput.cecState`|API|Returns whether the output of the OTT/STB device is actively being displayed on the TV|None|Result must be one of `active`, `inactive`, `unsupported`|
|6|`VideoOutput.onCecStateChanged`|Event|Notifies when HDMI CEC state changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|7|`VideoOutput.refreshRate`|API|Returns the refresh rate of the video signal on the video output, in Hz|None|Result must be one of `0`, `23.976`, `24`, `25`, `29.97`, `30`, `50`, `59.94`, `60`, given as a string or a number|
|8|`VideoOutput.onRefreshRateChanged`|Event|Notifies when the video output refresh rate changes|`{"listen": true}` (subscribe), then `{"listen": false}` (unsubscribe)|Subscribe reply must be `null` and unsubscribe reply must be `null`|
|9|`VideoOutput.colorDepth`|API|Returns the video color depth being used on the video output, in bits|None|Result must be one of `0`, `8`, `10`, `12`, given as a string or a number|
|10|`VideoOutput.colorFormat`|API|Returns the current color format of the video signal on the active video output port or integrated display|None|Result must be one of `ycbcr420`, `ycbcr422`, `ycbcr444`, `rgb444`, `none`|
|11|`VideoOutput.colorimetry`|API|Returns the current colorimetry value of the video signal on the active video output port or integrated display|None|Result must be one of `bt2020rgb`, `bt2020ycc`, `bt709`, `oprgb`, `none`|
|12|`VideoOutput.dynamicRange`|API|Returns the current dynamic range format of the video signal on the video output|None|Result must be one of `hdr10`, `hdr10plus`, `dolbyVision`, `hlg`, `sdr`, `none`|
|13|`VideoOutput.quantizationRange`|API|Returns the quantization range used on the video output|None|Result must be one of `limited`, `full`, `none`|

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework and Firebolt gateway are running | WPEFramework must be running on the device. The plugins org.rdk.DownloadManager, org.rdk.AppPackageManager and org.rdk.AppManager must be available, and the Firebolt gateway must be listening on `ws://127.0.0.1:3473`. | WPEFramework, the required plugins and the Firebolt gateway should be available on the device. |
| 2 | Configure the report publish URL in the Firebolt application | In `Firebolt_Certification/src/config/runtime.ts`, set `DEFAULT_REPORT_PUBLISH_URL` to the report server URL, for example `http://<report-host>:8090/`. The URL must end with `/` and must be the same as `report_server_url` in `FireboltTestVariables.py`. To skip more methods, add them to `EXCLUDED_METHODS` in the same file, or pass them in the `excludeMethods` launch parameter. | The application should be configured to publish its reports to the TDK report server. |
| 3 | Create the Firebolt certification bolt package | Create a bolt package of the Firebolt certification application with the entry point URL:<br>`https://<host>:<port>/?standalone=true&autoRun=true`<br>- `standalone=true`: runs the application as a standalone validation app<br>- `autoRun=true`: runs all modules on launch and publishes the reports<br><br>Use `firebolt_app_id` as the package ID and host the package at `<app_download_url>/<firebolt_bundle>`. | The bolt package should be downloadable by the device. |
| 4 | Configure FireboltTestVariables | In `fileStore/FireboltTestVariables.py`, set:<br>`firebolt_bundle`: file name of the bolt package<br>`firebolt_app_id`: package ID used in the package configuration<br>`app_download_url`: base URL where the bolt package is hosted<br>`report_server_url`: report server URL. It must be the same as the report publish URL of the application and must end with `/`<br>`reports_directory`: folder where the report server stores the reports, relative to fileStore or an absolute path (default `Firebolt_Certification/firebolt_certification_report/reports`) | The Firebolt test variables should be configured with valid values. |
| 5 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the path on the device where downloaded packages are stored, in the device or device-type configuration file. | The file locator path should be correctly configured in the device-specific config file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Load the rdkv_firebolt module | Load the `rdkv_firebolt` test module and connect to the device. | The module should load successfully. |
| 2 | Verify and activate required plugins | Query the state of org.rdk.DownloadManager, org.rdk.AppPackageManager and org.rdk.AppManager, activate the plugins that are not activated, and wait for 10 seconds. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin>"}}` | All three plugins should be in the activated state. |
| 3 | Register the TDK execution with the report server | Primitive test `firebolt_execute`: send the device IP, the reporting ID `tdk_<execution id>` and a timeout of 4500 seconds to the report server. <br>`POST <report_server_url>automation/runs` <br>`{"deviceIp": "<DUT IP>", "reportingId": "tdk_<execution id>", "timeout": 4500}` | The report server should respond with HTTP 201 and the reporting ID. |
| 4 | Check if the application is already installed | Query the installed packages to check whether `firebolt_app_id` is already installed. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppPackageManager.1.listPackages"}` | The installed packages list should be returned successfully. If the application is already installed, steps 5 and 6 are skipped. |
| 5 | Download the bolt package | Download the bolt package through the DownloadManager and wait for 10 seconds. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<firebolt_bundle>"}}` | The download should succeed and the downloaded file details should be returned. |
| 6 | Install the application | Build the file locator from `PACKAGEMANAGER_FILE_LOCATOR` and the downloaded file details, install the package, and verify that it is listed in the installed packages. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppPackageManager.install", "params": {"packageId": "<firebolt_app_id>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR><download details>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppPackageManager.1.listPackages"}` | The installation should succeed and `firebolt_app_id` should be listed in the installed packages. |
| 7 | Launch the application | Launch the application and wait for 10 seconds. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<firebolt_app_id>", "intent": "", "launchArgs": ""}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | The application should launch and be listed in the loaded apps. |
| 8 | Run the Firebolt schema validation | The application starts automatically because `autoRun=true` is set in its entry point. It fetches the reporting ID for the device IP from the report server, runs all modules listed in [Coverage](#head.Coverage), and publishes the JSON, HTML and Excel reports to the report server. <br>`GET <report_server_url>automation/context?deviceIp=<DUT IP>` | The application should receive the reporting ID `tdk_<execution id>`, complete the run and publish the reports. |
| 9 | Search for the generated reports | Wait for 10 seconds, then search `reports_directory` (json, html and xlsx sub folders) for files whose names start with `tdk_<execution id>`. The search is retried up to 10 times with a 3 second wait. | At least one report starting with `tdk_<execution id>` should be found. Otherwise the test is marked as failed. |
| 10 | Copy the HTML and Excel reports to the execution logs | Copy each `.html` and `.xlsx` report to `<log path><execution id>_<device id>_<result id>_<report file name>`. | The HTML and Excel reports should be available in the execution logs. |
| 11 | Terminate the application | Terminate the application. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<firebolt_app_id>"}}` | The application should be terminated successfully. |
| 12 | Unload the rdkv_firebolt module | Unload the test module. | The module should be unloaded successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M155<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
