/*
* If not stated otherwise in this file or this component's Licenses.txt file the
* following copyright and licenses apply:
*
* Copyright 2024 RDK Management
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*
http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/
package com.rdkm.tdkservice.util;

/*
 * 	This class is used to store the constants used in the application
 */
public class Constants {

	// Default user role for the user if not provided
	public static final String DEFAULT_USER_ROLE = "tester";

	// Default user group for the user if not provided
	public static final String DEFAULT_THEME_NAME = "DARK";

	// Default user group for the user if not provided
	public static final String HMACSHA256 = "HmacSHA256";

	// File store location
	public static final String FILESTORE_LOCATION = "classpath:/filestore/";

	// Default device config file name in filestore
	public static final String DEFAULT_DEVICE_CONFIG_FILE = "device.config";

	// Config file extension
	public static final String CONFIG_FILE_EXTENSION = ".config";

	// Base filestore directory
	public static final String BASE_FILESTORE_DIR = "src/main/resources/filestore/";

	// radio stream type
	public static final String RADIO_STREAM_TYPE = "RADIO";

	// video stream type
	public static final String VIDEO_STREAM_TYPE = "VIDEO";

	// Empty string
	public static final String EMPTY_STRING = "";
	// Starting with R
	public static final String STARTING_WITH_R = "R";

	// streaming Details template
	public static final String STREAMING_TEMPLATE_DETAILS = "StreamingDetailsTemplate";

	// Stream ID
	public static final String STREAMING_DETAILS_ID = "Stream Id";

	// Audio type
	public static final String AUDIO_TYPE = "Audio Type";

	// Video type
	public static final String VIDEO_TYPE = "Video Type";

	// ChannelType
	public static final String CHANNEL_TYPE = "Channel Type";

	// Category
	public static final String CATEGORY = "Category";

	// BoxManufacturer Id
	public static final String BOXMANUFACTURER_ID = "BoxManufacturer Id";

	// BoxManufacturer Name
	public static final String BOXMANUFACTURER_NAME = "BoxManufacturer Name";

	// SocVendor Id
	public static final String SOCVENDOR_ID = "SocVendor Id";

	// Soc Vendor name
	public static final String SOCVENDOR_NAME = "SocVendor";

	// User group
	public static final String USER_GROUP = "User Group";
	// User group id
	public static final String USER_GROUP_ID = "User Group Id";
	// User Role
	public static final String USER_ROLE = "User Role";

	// User Role Id
	public static final String USER_ROLE_ID = "User Role Id";

	// Box type
	public static final String BOX_TYPE = "Box type";

	// box type id
	public static final String BOX_TYPE_ID = "Box type id";
	// box type type
	public static final String BOX_TYPE_TYPE = "BoxType type";
	// User name
	public static final String USER_NAME = "User Name";
	// User id
	public static final String USER_ID = "User Id";

	// Email
	public static final String EMAIL = "Email";

	public static final String DEVICE_XML_FILE_EXTENSION = ".xml";
	// Device file extension
	public static final String DEVICE_FILE_EXTENSION_ZIP = ".zip";
	// XML tag
	public static final String XML_TAG_ROOT = "xml";
	// device
	public static final String XML_TAG_DEVICE = "device";
	public static final String XML_TAG_STB_NAME = "stb_name";
	// gatewayname
	public static final String XML_TAG_GATEWAY_NAME = "gateway_name";
	// cameraname
	public static final String XML_TAG_CAMERA_NAME = "camera_name";
	// stb ip
	public static final String XML_TAG_STB_IP = "stb_ip";
	// gatewayip
	public static final String XML_TAG_GATEWAY_IP = "gateway_ip";
	// cameraip
	public static final String XML_TAG_CAMERA_IP = "camera_ip";
	// mac address
	public static final String XML_TAG_MAC_ADDR = "mac_addr";
	// is thunder enabled
	public static final String XML_TAG_IS_THUNDER_ENABLED = "isThunderEnabled";
	// thunder port
	public static final String XML_TAG_THUNDER_PORT = "thunderPort";
	// xml box type
	public static final String XML_TAG_BOX_TYPE = "box_type";
	// xml box manufacturer
	public static final String XML_TAG_BOX_MANUFACTURER = "box_manufacturer";
	// xml soc vendor
	public static final String XML_TAG_SOC_VENDOR = "soc_vendor";
	// xml category
	public static final String XML_TAG_CATEGORY = "category";
	// xml recorder id
	public static final String XML_TAG_RECORDER_ID = "recorder_id";
	// xml gateway name
	public static final String XML_TAG_GATEWAY_IP_device = "gateway_name";
	// xml streams
	public static final String XML_TAG_STREAMS = "streams";
	// xml stream
	public static final String XML_TAG_STREAM = "stream";
	// xml stream id
	public static final String XML_TAG_ID = "id";

	// Db file name
	public static final String DB_FILE_NAME = "classpath:data.sql";

}
