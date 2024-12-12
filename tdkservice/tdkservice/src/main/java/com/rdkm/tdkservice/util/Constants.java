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

	public static final String LINE_STRING = "======";
	// Default user role for the user if not provided
	public static final String DEFAULT_USER_ROLE = "tester";

	// Default user group for the user if not provided
	public static final String DEFAULT_THEME_NAME = "DARK";

	// Default user group for the user if not provided
	public static final String HMACSHA256 = "HmacSHA256";

	// File store location
	public static final String FILESTORE_LOCATION = "classpath:/filestore/";

	// Default device config file name in filestore
	public static final String DEFAULT_DEVICE_CONFIG_FILE = "sampleDevice.config";

	// Config file extension
	public static final String CONFIG_FILE_EXTENSION = ".config";

	// Base filestore directory
	public static final String BASE_FILESTORE_DIR = "fileStore";

	// Slash as file path seperator
	public static final String FILE_PATH_SEPERATOR = "/";

	// TDKV device config directory inside filestore
	public static final String TDKV_DEVICE_CONFIG_DIR = "tdkvDeviceConfig";

	// Empty string
	public static final String EMPTY_STRING = "";

	// Category
	public static final String CATEGORY = "Category";

	// Oem Id
	public static final String OEM_ID = "oem Id";

	// Oem Name
	public static final String OEM_NAME = "oem Name";

	// Soc Id
	public static final String SOC_ID = "Soc Id";

	// Soc name
	public static final String SOC_NAME = "Soc";

	// User group
	public static final String USER_GROUP = "User Group";
	// User group id
	public static final String USER_GROUP_ID = "User Group Id";
	// User Role
	public static final String USER_ROLE = "User Role";

	// User Role Id
	public static final String USER_ROLE_ID = "User Role Id";

	// Device type
	public static final String DEVICE_TYPE = "Device type";

	// device type id
	public static final String DEVICE_TYPE_ID = "Device type id";
	// device type type
	public static final String DEVICE_TYPE_TYPE = "DeviceType type";
	// user name
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
	public static final String XML_TAG_DEVICE_NAME = "device_name";
	// gatewayname
	public static final String XML_TAG_GATEWAY_NAME = "gateway_name";
	// cameraname
	public static final String XML_TAG_CAMERA_NAME = "camera_name";
	// device ip
	public static final String XML_TAG_DEVICE_IP = "device_ip";
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
	// xml device type
	public static final String XML_TAG_Device_TYPE = "device_type";
	// xml oem
	public static final String XML_TAG_OEM = "oem";
	// xml soc
	public static final String XML_TAG_SOC = "soc";
	// xml category
	public static final String XML_TAG_CATEGORY = "category";

	// Db file name
	public static final String DB_FILE_NAME = "classpath:data.sql";
	// script tag name
	public static final String SCRIPT_TAG_NAME = "Script tag name";

	// script tag is
	public static final String SCRIPT_TAG_ID = "Script tag id";

	// build version
	public static final String RDK_VERSION_NAME = "Build version";

	// build version id
	public static final String RDK_VERSION_ID = "Build version id";

	// Module name
	public static final String MODULE_NAME = "Module name";

	// function name
	public static final String FUNCTION_NAME = "Function name";

	// ParameterType name
	public static final String PARAMETER_NAME = "Parameter name";

	// Primitive test name
	public static final String PRIMITIVE_TEST_NAME = "Primitive test name";

	// Primitive test id
	public static final String PRIMITIVE_TEST_ID = "Primitive test id";

	// Primitive test with module name
	public static final String PRIMITIVE_TEST_WITH_MODULE_NAME = "Primitive test with module name";

	// xml extension
	public static final String XML_EXTENSION = ".xml";

	// xml module tag
	public static final String XML_MODULE_TAG = "module";

	// xml module element
	public static final String XML_MODULE_ELEMENT = "moduleName";

	// xml execution time out
	public static final String XML_TAG_EXECUTION_TIME_OUT = "executionTimeOut";

	// xml test group
	public static final String XML_TAG_TEST_GROUP = "testGroup";

	// xml log file names
	public static final String XML_TAG_LOG_FILE_NAMES = "logFileNames";

	// xml crash file names
	public static final String XML_TAG_CRASH_FILE_NAMES = "crashFileNames";

	// xml functions
	public static final String XML_FUNCTIONS = "functions";

	// xml function
	public static final String XML_FUNCTION = "function";

	// name
	public static final String NAME = "name";

	// xml parameter name
	public static final String XML_PARAMETER_NAME = "parameterName";

	// xml parameter
	public static final String XML_PARAMETER = "parameter";

	// xml function name of of parameter
	public static final String XML_PARAMETER_FUN_NAME = "funName";

	// xml parameter type
	public static final String XML_PARAMETER_TYPE = "parameterType";

	// xml range value
	public static final String XML_PARAMETER_RANGE = "range";

	// xml
	public static final String XML = "xml";
	// xml parameters
	public static final String XML_PARAMETERS = "parameters";

	// comma separator
	public static final String COMMA_SEPARATOR = ",";

	// yes value
	public static final String YES = "yes";

	// Script name
	public static final String SCRIPT_NAME = "Script name";

	// Script location for RDKV
	public static final String RDKV_FOLDER_NAME = "testscriptsRDKV";

	// Script location for RDKB
	public static final String RDKB_FOLDER_NAME = "testscriptsRDKB";

	// Script location for RDKC
	public static final String RDKC_FOLDER_NAME = "testscriptsRDKC";

	// Python file extension
	public static final String PYTHON_FILE_EXTENSION = ".py";

	// Script ID
	public static final String SCRIPT_ID = "Script id";

	// Script
	public static final String SCRIPT = "Script";

	// Module name
	public static final String MODULE = "Module";

	// Excel file extension
	public static final String EXCEL_FILE_EXTENSION = ".xlsx";

	// Script group name
	public static final String TEST_SUITE = "Test suite";

	// Script group id
	public static final String TEST_SUITE_ID = "Test suite id";

	public static final String NO = "no";

	public static final String XML_FILE_EXTENSION = ".xml";

	public static final String PYTHON_CONTENT = "text/x-python";

	public static final String USER_DIRECTORY = "user.dir";

	public static final String BASE_FILESTORE_FOLDER = "src/main/webapp/filestore";

	public static final String ZIP_EXTENSION = ".zip";

	// config file extension
	public static final String CONFIG_FILE = ".config";
	// config file path
	public static final String RDK_CERTIFICATION_CONFIG_PATH = "rdkCertificationConfigs";
	// Header finder to add HEader template
	public static final String HEADER_FINDER = "If not stated otherwise in this file or this component's Licenses.txt";
	// Header template
	public static final String HEADER_TEMPLATE = "##########################################################################\r\n"
			+ "# If not stated otherwise in this file or this component's Licenses.txt\r\n"
			+ "# file the following copyright and licenses apply:\r\n" + "#\r\n"
			+ "# Copyright CURRENT_YEAR RDK Management\r\n" + "#\r\n"
			+ "# Licensed under the Apache License, Version 2.0 (the \"License\");\r\n"
			+ "# you may not use this file except in compliance with the License.\r\n"
			+ "# You may obtain a copy of the License at\r\n" + "#\r\n"
			+ "# http://www.apache.org/licenses/LICENSE-2.0\r\n" + "#\r\n"
			+ "# Unless required by applicable law or agreed to in writing, software\r\n"
			+ "# distributed under the License is distributed on an \"AS IS\" BASIS,\r\n"
			+ "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\n"
			+ "# See the License for the specific language governing permissions and\r\n"
			+ "# limitations under the License.\r\n"
			+ "##########################################################################\r\n" + "";

	public static final String USER_THEME = "User Theme";

	public static final String TDK_UTIL_FILE_LOCATION = "/tdkUtilFiles/HeaderFile.txt";

	public static final String NEW_LINE = "\n";

	// Python default command
	public static final String PYTHON = "python";

	// Busy status
	public static final String BUSY = "BUSY";

	// Free status
	public static final String FREE = "FREE";

	// Not found status
	public static final String NOT_FOUND = "NOT_FOUND";

	// HANG status
	public static final String HANG = "HANG";

	// TDK_DISABLED status
	public static final String TDK_DISABLED = "TDK_DISABLED";

	// IPV6_INTERFACE
	public static final String IPV6 = "IPV6";

	// IPV4_INTERFACE
	public static final String IPV4 = "IPV4";

	// PERCENTAGE
	public static final String PERCENTAGE = "%";

	public static final String COLON = ":";

	public static final String KEY_LASTDAY = "L";
	public static final String KEY_ENTERNEW_LINE = "\r\n";
	public static final String GREATERTHAN = ">";
	public static final String LESSTHAN = "<";
	public static final String HTML_GREATERTHAN = "&gt;";
	public static final String HTML_LESSTHAN = "&lt;";
	public static final String HTML_REPLACEBR = "</?br\\b[^>]*>";
	public static final String HTML_PATTERN = "<span(.*?)</span>";
	public static final String HTML_PATTERN_AFTERSPAN = "</?span\\b[^>]*>";
	// CURLY_BRACKET_OPEN
	public static final String CURLY_BRACKET_OPEN = "{";

	public static final String STATUS_NONE = "none";

	public static final String CONFIGURE_TESTCASE_REPLACE_TOKEN = "configureTestCase(ip,port,";
	public static final String REPLACE_BY_TOKEN = ",ip,port,";
	public static final String LEFT_PARANTHESIS = "(";
	public static final String RIGHT_PARANTHESIS = ")";
	public static final String CURLY_BRACKET_CLOSE = "}";
	public static final String SQUARE_BRACKET_OPEN = "[";
	public static final String SQUARE_BRACKET_CLOSE = "]";

	public static final String COMMA_SEPERATOR = ",";
	public static final String SINGLE_QUOTES = "'";
	public static final String UNDERSCORE = "_";

	public static final String METHOD_TOKEN = "configureTestCase";

	public static final String LOGS = "logs";

	public static final String TEMP_SCRIPT_FILE_KEYWORD = "tempScript";

	public static final String PORT_REPLACE_TOKEN = "<port>";

	public static final String IP_REPLACE_TOKEN = "<ipaddress>";

	public static final String EXECUTION_KEYWORD = "execution";

	public static final String RESULT = "result";

	public static final String EXECUTION_LOGS = "executionLogs";

	public static final String RERUN_APPENDER = "_RERUN";

	public static final String SCRIPT_END_PY_CODE = "\nprint(\"SCRIPTEND#!@~\");";

	public static final String ERROR_TAG_PY_COMMENT = "#TDK_@error";

	public static final String END_TAG_PY_COMMENT = "SCRIPTEND#!@~";

	public static final String IPV6_INTERFACE = "ipv6.interface";
	public static final String IPV4_INTERFACE = "ipv4.interface";
	public static final String PYTHON_COMMAND = "python_command";
	public static final String CONSOLE_FILE_UPLOAD_SCRIPT = "//filestore//callConsoleLogUpload.py";

	public static final String LOG_UPLOAD_IPV4 = "log.upload.ipv4";
	public static final String LOG_UPLOAD_IPV6 = "log.upload.ipv6";
	public static final String REST_MECHANISM = "REST";
	public static final String TM_URL = "tmURL";
	public static final String FILE_TRANSFER_SCRIPT_RDKSERVICE = "transfer_thunderdevice_logs.py"; // Update path
	public static final String SLASH_VERSION_TXT_FILE = "/version.txt"; // Update as necessary
	public static final String ROOT_STRING = "root"; // Example path, change as necessary
	public static final String NONE_STRING = "none";
	public static final String TM_CONFIG_FILE = "tm.config";
	// AgentConsoleLog.txt
	public static final String AGENT_CONSOLE_LOG_FILE = "AgentConsoleLog.log";
	// logs.path
	public static final String LOGS_PATH = "logs.path";
	public static final String HTML_BR = "<br/>";

	public static final String MULTI_TEST_SUITE = "MultiTestSuite";
	public static final String DEVICE_LOGS = "deviceLogs";
	public static final String AGENT_LOGS = "agentLogs";
	public static final String DEVICE_INFO_LOGS = "deviceinfo";

	public static final String THUNDER_DEFAULT_PORT = "9998";
	public static final String FILE_UPLOAD_SCRIPT = "fileupload.py";
	public static final String PYTHON3 = "python3";

	public static final String BUILD_NAME_FAILED = "Build name fetching failed";
	public static final String DEFAULT_IPV4_INTERFACE = "eth0";
	public static final String DEFAULT_IPV6_INTERFACE = "sit1";

	// The total keyword to be used in DTO
	public static final String TOTAL_KEYWORD = "Total";
}
