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
package com.rdkm.tdkservice.serviceimpl;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Year;
import java.util.ArrayList;
import java.util.List;

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
import com.rdkm.tdkservice.model.DeviceType;
import com.rdkm.tdkservice.model.Script;
import com.rdkm.tdkservice.model.UserGroup;
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

	/*
	 * The method to add license header in the python files and config files
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

}
