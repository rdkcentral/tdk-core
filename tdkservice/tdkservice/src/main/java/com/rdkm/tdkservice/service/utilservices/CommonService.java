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
package com.rdkm.tdkservice.service.utilservices;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Year;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.Font;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.config.AppConfig;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.enums.TestGroup;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.exception.TDKServiceException;
import com.rdkm.tdkservice.exception.UserInputException;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.model.DeviceType;
import com.rdkm.tdkservice.model.Script;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.ScriptRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.Utils;

/**
 * This class is used to provide common services.
 */
@Service
public class CommonService {

	public static final Logger LOGGER = LoggerFactory.getLogger(CommonService.class);

	@Autowired
	UserGroupRepository userGroupRepository;

	@Autowired
	ScriptRepository scriptRepository;

	/**
	 * This method is used to get the folder name based on the module type.
	 * 
	 * @param testGroup
	 * @return
	 */
	public String getFolderBasedOnModuleType(TestGroup testGroup) {
		LOGGER.info("Inside getFolderBasedOnModuleType method with testGroup: {}", testGroup);
		String folderName = "";
		switch (testGroup) {
		case COMPONENT:
			folderName = "component";
			break;
		case CERTIFICATION:
			folderName = "certification";
			break;
		case E2E:
			folderName = "integration";
			break;
		default:
			LOGGER.error("Invalid test type: " + testGroup.getName());
		}
		return folderName;

	}

	/**
	 * This method is used to get the folder name based on the category.
	 * 
	 * @param category - RDKV, RDKB, RDKC
	 * @return folder name based on the category - RDKV, RDKB, RDKC
	 */
	public String getFolderBasedOnCategory(Category category) {
		String folderName = "";
		switch (category) {
		case RDKV:
			folderName = Constants.RDKV_FOLDER_NAME;
			break;
		case RDKV_RDKSERVICE:
			folderName = Constants.RDKV_FOLDER_NAME;
			break;
		case RDKB:
			folderName = Constants.RDKB_FOLDER_NAME;
			break;
		case RDKC:
			folderName = Constants.RDKC_FOLDER_NAME;
			break;
		default:
			LOGGER.error("Invalid category: " + category.getName());
		}
		return folderName;
	}

	/**
	 * This method is used to validate the category and return the Catgory enum.
	 * 
	 * @param category string- RDKV, RDKB, RDKC
	 * @return category enum - RDKV, RDKB, RDKC
	 */
	public Category validateCategory(String category) {
		Category categoryEnum = Category.valueOf(category.toUpperCase());
		if (categoryEnum != null) {
			return categoryEnum;
		} else {
			LOGGER.error("Category not found: " + category);
			throw new ResourceNotFoundException("Category not found", category);
		}
	}

	/**
	 * This method is used to validate the user group.
	 * 
	 * @param userGroupName - user group name
	 * @return - user group
	 */
	public UserGroup validateUserGroup(String userGroupName) {
		// Validates user group name and gets the user group
		if (userGroupName != null) {
			UserGroup userGroup = userGroupRepository.findByName(userGroupName);
			if (userGroup != null) {
				return userGroup;
			}
		} else {
			return null;
		}
		return null;

	}

	/**
	 * Create excel from test cases information in script.
	 *
	 * @param scripts   the test cases
	 * @param sheetName the sheet name
	 * @return the byte array input stream
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	public ByteArrayInputStream createExcelFromTestCasesDetailsInScript(List<Script> scripts, String sheetName) {
		LOGGER.info("Creating excel from test cases for sheet");
		String[] headers = { "Test Script", "Test Case ID", "Test Objective", "Test Type", "Supported device Type",
				"Test Prerequisites", "RDK Interface", "Input Parameters", "Automation Approach", "Expected Output",
				"Priority", "Test Stub Interface", "Skipped", "Skip remarks", "Update Release Version", "Remarks" };
		try {
			Workbook workBook = new XSSFWorkbook();
			ByteArrayOutputStream out = new ByteArrayOutputStream();

			Sheet sheet = workBook.createSheet(sheetName);

			// Create header row
			Row headerRow = sheet.createRow(0);
			CellStyle boldStyle = workBook.createCellStyle();
			Font boldFont = workBook.createFont();
			boldFont.setFontName("Arial");
			boldFont.setFontHeightInPoints((short) 10);
			boldFont.setBold(true);
			boldStyle.setFont(boldFont);

			for (int col = 0; col < headers.length; col++) {
				Cell cell = headerRow.createCell(col);
				cell.setCellValue(headers[col]);
				cell.setCellStyle(boldStyle);
			}

			// Set the data row with Arial font size 10
			CellStyle dataStyle = workBook.createCellStyle();
			Font dataFont = workBook.createFont();
			dataFont.setFontName("Arial");
			dataFont.setFontHeightInPoints((short) 10);
			dataStyle.setFont(dataFont);

			int rowNum = 1; // Start after the header row
			for (Script script : scripts) {
				Row dataRow = sheet.createRow(rowNum++);

				dataRow.createCell(0).setCellValue(script.getName());
				dataRow.createCell(1).setCellValue(script.getTestId());
				dataRow.createCell(2).setCellValue(script.getObjective());
				dataRow.createCell(3).setCellValue(script.getTestType().toString());
				if (script.getDeviceTypes() == null) {
					dataRow.createCell(4).setCellValue("");
				} else {
					dataRow.createCell(4).setCellValue(Utils.convertListToCommaSeparatedString(
							this.getDeviceTypesAsStringList(script.getDeviceTypes())));
				}
				dataRow.createCell(5).setCellValue(script.getPrerequisites());
				dataRow.createCell(6).setCellValue(script.getApiOrInterfaceUsed());
				dataRow.createCell(7).setCellValue(script.getInputParameters());
				dataRow.createCell(8).setCellValue(script.getAutomationApproach());
				dataRow.createCell(9).setCellValue(script.getExpectedOutput());
				dataRow.createCell(10).setCellValue(script.getPriority());
				dataRow.createCell(11).setCellValue(script.getTestStubInterface());
				if (script.isSkipExecution()) {
					dataRow.createCell(12).setCellValue("Yes");
					dataRow.createCell(13).setCellValue(script.getSkipRemarks());
				} else {
					dataRow.createCell(12).setCellValue("No");
					dataRow.createCell(13).setCellValue("N/A");

				}
				dataRow.createCell(14).setCellValue(script.getReleaseVersion());
				dataRow.createCell(15).setCellValue(script.getRemarks());
				// Apply the data style (Arial, size 10) to each cell in the row
				for (int i = 0; i < headers.length; i++) {
					dataRow.getCell(i).setCellStyle(dataStyle);
				}
			}

			// Auto size the columns to fit the content
			for (int i = 0; i < headers.length; i++) {
				sheet.autoSizeColumn(i);
			}

			workBook.write(out);
			workBook.close();

			return new ByteArrayInputStream(out.toByteArray());
		} catch (Exception e) {
			LOGGER.error("Error creating excel from test cases: " + e.getMessage());
			throw new TDKServiceException("Error creating excel from test cases: " + e.getMessage());
		}
	}

	/**
	 * Get the list of deviceTypes as list of Stringbased on the deviceTypes name
	 * 
	 * @param deviceTypes
	 * @return
	 */
	public List<String> getDeviceTypesAsStringList(List<DeviceType> deviceTypes) {
		List<String> deviceTypeList = new ArrayList<>();
		for (DeviceType deviceType : deviceTypes) {
			deviceTypeList.add(deviceType.getName());
		}
		return deviceTypeList;
	}

	public List<DeviceType> getDeviceType(String scriptName) {
		Script script = scriptRepository.findByName(scriptName);
		if (script == null) {
			LOGGER.error("Script not found with the name: " + scriptName);
			throw new ResourceNotFoundException(Constants.SCRIPT_NAME, scriptName);
		}
		return script.getDeviceTypes();
	}

	/*
	 * /* The method to add license header in the python files and config files
	 * 
	 * @param scriptFile
	 * 
	 * @return
	 */
	public MultipartFile addHeader(MultipartFile file) throws IOException {
		if (file == null || file.isEmpty()) {
			LOGGER.error("Script file is null or empty");
			throw new UserInputException("Script file is null or empty");
		}

		String fileContent = new String(file.getBytes(), StandardCharsets.UTF_8);
		if (fileContent.contains(Constants.HEADER_FINDER)) {
			LOGGER.info("Header already exists in the file");
			return file;
		}

		String headerFileLocation = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
				+ Constants.TDK_UTIL_FILE_LOCATION;
		Path path = Paths.get(headerFileLocation);
		if (!Files.exists(path)) {
			LOGGER.error("Header file not found at location: " + headerFileLocation);
			throw new IOException("Header file not found at location: " + headerFileLocation);
		}

		String headerContent = Files.readString(path, StandardCharsets.UTF_8);
		String currentYear = Year.now().toString();
		String header = headerContent.replace("CURRENT_YEAR", currentYear);

		// Prepend the header to the file content
		String updatedContent = header + fileContent;
		return new MockMultipartFile(file.getName(), file.getOriginalFilename(), file.getContentType(),
				updatedContent.getBytes(StandardCharsets.UTF_8));
	}

	/**
	 * Validate the python file
	 * 
	 * @param configFile
	 */
	public void validatePythonFile(MultipartFile configFile) {
		if (configFile.isEmpty()) {
			LOGGER.error("Python file is empty");
			throw new UserInputException("Python file is empty");
		}
		if (!configFile.getOriginalFilename().endsWith(Constants.PYTHON_FILE_EXTENSION)) {
			LOGGER.error("Invalid file extension: " + configFile.getOriginalFilename());
			throw new UserInputException(
					"Invalid file extension: " + configFile.getOriginalFilename() + " The File must be .py file");
		}
	}

	/**
	 * Retrieves the host IP address based on the specified IP type.
	 *
	 * @param ipType the type of IP address (e.g., "IPv4" or "IPv6")
	 * @return the host IP address as a String
	 */
	public String getHostIpAddress(String ipType) {
		String nwInterfaceName = "";
		if (ipType.equals(Constants.IPV4)) {

			nwInterfaceName = this.getInterfaceFromConfigFile(Constants.IPV4);
		} else if (ipType.equals(Constants.IPV6)) {
			nwInterfaceName = this.getInterfaceFromConfigFile(Constants.IPV6);
		}
		String hostIPAddress = InetUtilityService.getIPAddress(ipType, nwInterfaceName);
		return hostIPAddress;

	}

	/**
	 * This method is used to get the base log path. If it is available in the
	 * config file , then that path is taken, other wise the base log path in
	 * fileStore/logs directory is taken
	 * 
	 * @return - base log path
	 */
	public String getBaseLogPath() {
		LOGGER.info("Getting base log path");
		String defaultLogBasePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + Constants.LOGS;
		String configFilePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + Constants.TM_CONFIG_FILE;
		String logsPath = getConfigProperty(new File(configFilePath), Constants.LOGS_PATH_KEY_CONFIG_FILE);

		// Check if the value from the config is null or empty
		if (Utils.isEmpty(logsPath)) {
			// Provide a default logpath - fileStore/logs
			logsPath = defaultLogBasePath;
		}
		return defaultLogBasePath;

	}

	/**
	 * This method is used to delete the file.
	 * 
	 * @param deleteFilePath
	 * @return
	 */
	public boolean deleteFile(String deleteFilePath) {
		boolean isFileDeleted = false;

		Path tempScriptPath = Paths.get(deleteFilePath);
		try {
			if (Files.exists(tempScriptPath)) {
				Files.delete(tempScriptPath);
				if (!Files.exists(tempScriptPath)) {
					isFileDeleted = true;

				}
				LOGGER.info("File deleted: " + deleteFilePath);
			}
		} catch (IOException e) {
			LOGGER.error("Failed to delete file: " + deleteFilePath, e);
		}
		return isFileDeleted;

	}

	/**
	 * This method is used to validate the script device device type.
	 * 
	 * @param device
	 * @param script
	 * @return
	 */
	public boolean validateScriptDeviceDeviceType(Device device, Script script) {

		List<DeviceType> deviceTypes = this.getDeviceType(script.getName());
		if (null == deviceTypes) {
			return true;
		} else {
			for (DeviceType deviceType : deviceTypes) {
				if (deviceType.equals(device.getDeviceType())) {
					return true;
				}
			}
		}
		return false;

	}

	/**
	 * This method is used to check if the script is marked to be skipped.
	 * 
	 * @param script
	 * @return
	 */
	public boolean isScriptMarkedToBeSkipped(Script script) {
		if (script.isSkipExecution()) {
			return true;
		}
		return false;
	}

	/**
	 * This method is used to validate the script device category.
	 * 
	 * @param device
	 * @param script
	 * @return
	 */
	public boolean vaidateScriptDeviceCategory(Device device, Script script) {
		boolean isCategoryMatch = false;
		if (device.isThunderEnabled()) {
			isCategoryMatch = script.getModule().getCategory().equals(Category.RDKV_RDKSERVICE);
		} else {
			isCategoryMatch = script.getModule().getCategory().equals(device.getCategory());
		}
		return isCategoryMatch;
	}

	/**
	 * This method is used to get the execution log file path.
	 * 
	 * @param executionID
	 * @param executionResultID
	 * @return
	 */
	public String getExecutionLogFilePath(String executionID, String executionResultID) {
		String logBasePath = this.getBaseLogPath();
		return logBasePath + Constants.FILE_PATH_SEPERATOR + Constants.EXECUTION_KEYWORD + Constants.UNDERSCORE
				+ executionID + Constants.FILE_PATH_SEPERATOR + Constants.RESULT + Constants.UNDERSCORE
				+ executionResultID + Constants.FILE_PATH_SEPERATOR + Constants.EXECUTION_LOGS
				+ Constants.FILE_PATH_SEPERATOR + executionResultID + "_executionlogs.log";
	}

	/**
	 * Method to load properties from a file
	 * 
	 * @param filePath The path to the configuration file
	 * @return The loaded properties, or null if the file does not exist or an error
	 *         occurs
	 */
	private Properties loadPropertiesFromFile(String filePath) {
		LOGGER.debug("Loading properties from file: {}", filePath);
		File configFile = new File(filePath);
		if (!configFile.exists() || !Files.exists(configFile.toPath())) {
			LOGGER.error("No Config File !!! ");
			return null;
		}
		try (InputStream is = new FileInputStream(configFile)) {
			Properties prop = new Properties();
			prop.load(is);
			return prop;
		} catch (IOException e) {
			LOGGER.error("Error reading config file: {}", configFile, e);
		}
		return null;
	}

	/**
	 * Method to get the configuration property from the specified file
	 *
	 * @param configFile The configuration file
	 * @param key        The key to search for in the configuration file
	 * @return The value of the configuration property
	 */
	public String getConfigProperty(File configFile, String key) {
		Properties prop = loadPropertiesFromFile(configFile.getPath());
		if (prop != null) {
			LOGGER.info(" properties key for getting the property from config file" + prop.getProperty(key));
			return prop.getProperty(key);
		}
		return null;
	}

	/**
	 * Method to get the TM URL from the configuration file
	 * 
	 * @return The TM URL
	 */
	public String getTMUrlFromConfigFile() {
		String tmUrl = Constants.TM_URL;
		try {
			// get tm.config file using base location
			String configFilePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
					+ Constants.TM_CONFIG_FILE;
			LOGGER.debug("configFilePath: {}", configFilePath);
			// get the TM URL from the config file
			tmUrl = getConfigProperty(new File(configFilePath), Constants.TM_URL);
			LOGGER.debug("TM URL from config file: {}", tmUrl);
		} catch (Exception e) {
			LOGGER.error("Error getting TM URL from config file: " + e.getMessage());
		}
		return tmUrl;
	}

	/**
	 * Method to get the TM URL from configuration file for test execution The URL
	 * to be accessed from the python frameworks like tdklib while test execution
	 * TODO: Change to auto detected from the request
	 */
	public String getTMUrlFromConfigFileForTestExecution() {
		String tmUrl = "";
		try {
			// get tm.config file using base location
			String configFilePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
					+ Constants.TM_CONFIG_FILE;
			LOGGER.debug("configFilePath: {}", configFilePath);
			// get the TM URL from the config file
			tmUrl = getConfigProperty(new File(configFilePath), Constants.TM_URL_EXEC_KEY_CONFIG_FILE);
			LOGGER.debug("TM URL from config file: {}", tmUrl);
		} catch (Exception e) {
			LOGGER.error("Error getting TM URL from config file: " + e.getMessage());
		}
		return tmUrl;
	}

	/**
	 * Method to get the interface from the configuration file
	 * 
	 * @param ipType The IP type (e.g., "IPv4" or "IPv6")
	 * @return The interface
	 */
	public String getInterfaceFromConfigFile(String ipType) {
		LOGGER.debug("Getting interface from config file for IP type: {}", ipType);
		String key = "";
		String defaultInterface = "";
		if (ipType.equals(Constants.IPV4)) {
			key = Constants.IPV4_INTERFACE;
			defaultInterface = Constants.DEFAULT_IPV4_INTERFACE;
		} else if (ipType.equals(Constants.IPV6)) {
			key = Constants.IPV6_INTERFACE;
			defaultInterface = Constants.DEFAULT_IPV6_INTERFACE;

		} else {
			return null;
		}
		String value = "";
		try {
			// get tm.config file using base location
			String configFilePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
					+ Constants.TM_CONFIG_FILE;
			LOGGER.debug("configFilePath: {}", configFilePath);
			// get the TM URL from the config file
			value = getConfigProperty(new File(configFilePath), key);
			if (Utils.isEmpty(value)) {
				value = defaultInterface;
			}

			LOGGER.debug("Interface from congs is", value);
		} catch (Exception e) {
			LOGGER.error("Error getting TM URLinterface from config file: " + e.getMessage());
		}
		return value;

	}

	/**
	 * Get the device log file path for the given execution result
	 *
	 * @param executionId       the execution ID
	 * @param executionResultId the execution result ID
	 * @param baseLogPath       the base log path
	 */
	public String getDeviceLogsPathForTheExecution(String executionId, String executionResultId, String baseLogPath) {
		String deviceLogsPath = baseLogPath + Constants.FILE_PATH_SEPERATOR + Constants.EXECUTION_KEYWORD
				+ Constants.UNDERSCORE + executionId + Constants.FILE_PATH_SEPERATOR + Constants.RESULT
				+ Constants.UNDERSCORE + executionResultId + Constants.FILE_PATH_SEPERATOR + Constants.DEVICE_LOGS
				+ Constants.FILE_PATH_SEPERATOR;
		return deviceLogsPath;
	}

	/**
	 * Constructs the crash logs path for a given execution.
	 *
	 * @param executionId       the unique identifier for the execution
	 * @param executionResultId the unique identifier for the execution result
	 * @param baseLogPath       the base path where logs are stored
	 * @return the constructed crash logs path for the specified execution and
	 *         result
	 */
	public String getCrashLogsPathForTheExecution(String executionId, String executionResultId, String baseLogPath) {
		String crashLogsPath = baseLogPath + Constants.FILE_PATH_SEPERATOR + Constants.EXECUTION_KEYWORD
				+ Constants.UNDERSCORE + executionId + Constants.FILE_PATH_SEPERATOR + Constants.RESULT
				+ Constants.UNDERSCORE + executionResultId + Constants.FILE_PATH_SEPERATOR + Constants.CRASH_LOGS
				+ Constants.FILE_PATH_SEPERATOR;
		return crashLogsPath;
	}

	/**
	 * Get file names from directory
	 *
	 * @param directoryPath
	 * @param executionId
	 * @return fileNames
	 */
	public List<String> getFilenamesFromDirectory(String directoryPath, String executionId) {
		List<String> fileNames = new ArrayList<>();
		File directory = new File(directoryPath);

		if (directory.exists() && directory.isDirectory()) {
			File[] files = directory.listFiles();
			if (files != null) {
				for (File file : files) {
					if (file.isFile()) {
						fileNames.add(file.getName());
					}
				}
			}
		} else {
			LOGGER.warn("Directory does not exist or is not a directory: {}", directoryPath);
		}

		return fileNames;
	}

	/**
	 * Get the base file path for the upload log API
	 *
	 * @return String
	 */
	public String getBaseFilePathForUploadLogAPI() {
		String baseLogFilePath = this.getBaseLogPath();
		String logsPath = baseLogFilePath + Constants.FILE_PATH_SEPERATOR + "uploadedlogs";
		return logsPath;
	}

	/**
	 * Get the agent log path for the given execution result
	 * 
	 * @param executionId
	 * @param executionResultId
	 * @param baseLogPath
	 * @return agentLogsPath
	 */
	public String getAgentLogPath(String executionId, String executionResultId, String baseLogPath) {
		String agentLogsPath = baseLogPath + Constants.FILE_PATH_SEPERATOR + Constants.EXECUTION_KEYWORD
				+ Constants.UNDERSCORE + executionId + Constants.FILE_PATH_SEPERATOR + Constants.RESULT
				+ Constants.UNDERSCORE + executionResultId + Constants.FILE_PATH_SEPERATOR + Constants.AGENT_LOGS
				+ Constants.FILE_PATH_SEPERATOR;
		return agentLogsPath;

	}

	/**
	 * Get the version log file path for the given execution
	 * 
	 * @param executionId
	 * @return versionLogsPath
	 */
	public String getVersionLogFilePathForTheExecution(String executionId) {
		String baseLogPath = this.getBaseLogPath();
		String versionLogsPath = baseLogPath + Constants.FILE_PATH_SEPERATOR + Constants.EXECUTION_KEYWORD
				+ Constants.UNDERSCORE + executionId + Constants.FILE_PATH_SEPERATOR + Constants.DEVICE_INFO_LOGS
				+ Constants.FILE_PATH_SEPERATOR;
		return versionLogsPath;
	}

	/**
	 * Get the python command from the config file
	 * 
	 * @return Python command , if not found return the default python
	 */
	public String getPythonCommandFromConfig() {
		String configFilePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + Constants.TM_CONFIG_FILE;
		String pythonCommand = getConfigProperty(new File(configFilePath), Constants.PYTHON_COMMAND);

		// Check if the value from the config is null or empty
		if (pythonCommand == null || pythonCommand.isEmpty()) {
			// Provide a default Python 3 command
			pythonCommand = Constants.PYTHON3;
		}

		return pythonCommand;
	}

	/**
	 * This method checks if the given directory exists and is not empty
	 * 
	 * @param directoryPath - the directory path
	 * @return boolean - true if the directory exists and is not empty, false
	 *         otherwise
	 */
	public boolean checkAFolderExists(String directoryPath) {
		File directory = new File(directoryPath);
		// Check if the directory exists
		LOGGER.info("Checking if the directory exists: {}", directoryPath);
		if (!directory.exists()) {
			LOGGER.error("Directory does not exist: {}", directoryPath);
			return false; // Directory doesn't exist
		}
		// Check if the directory is empty
		if (directory.listFiles().length == 0) {
			LOGGER.error("Directory is empty: {}", directoryPath);
			return false; // Directory exists but is empty
		}
		return true;
	}

}
