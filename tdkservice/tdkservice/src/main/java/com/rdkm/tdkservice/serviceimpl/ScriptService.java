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
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;

import com.rdkm.tdkservice.model.*;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.repository.*;
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
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.config.AppConfig;
import com.rdkm.tdkservice.dto.ScriptCreateDTO;
import com.rdkm.tdkservice.dto.ScriptDTO;
import com.rdkm.tdkservice.dto.ScriptListDTO;
import com.rdkm.tdkservice.dto.ScriptModuleDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.exception.TDKServiceException;
import com.rdkm.tdkservice.exception.UserInputException;
import com.rdkm.tdkservice.service.IScriptService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;

/**
 * Service for scripts. This class is used to provide the service to save the
 * script file and the script details. The script file will be saved in the
 * location based on the module and category. The script details will be saved
 * in the database.
 */
@Service
public class ScriptService implements IScriptService {

	public static final Logger LOGGER = LoggerFactory.getLogger(ScriptService.class);

	@Autowired
	ScriptRepository scriptRepository;

	@Autowired
	DeviceTypeRepository deviceTypeRepository;

	@Autowired
	PrimitiveTestRepository primitiveTestRepository;

	@Autowired
	private UserGroupRepository userGroupRepository;

	@Autowired
	private ModuleRepository moduleRepository;

	@Autowired
	CommonService commonService;

	/**
	 * Save the script file and the script details. The script file will be saved in
	 * the location based on the module and category. The script details will be
	 * saved in the database.
	 * 
	 */
	@Override
	public boolean saveScript(MultipartFile scriptFile, ScriptCreateDTO scriptCreateDTO) {
		LOGGER.info("Saving script file: " + scriptFile.getOriginalFilename() + " for scriptdetails: "
				+ scriptCreateDTO.toString());
		// Check if the script already exists with the same name or not in the database
		this.checkIfScriptExists(scriptCreateDTO);

		// Convert DTO to Entity, this is a custom method
		Script script = MapperUtils.convertToScriptEntity(scriptCreateDTO);

		// Get the primitive test based on the primitive test name
		PrimitiveTest primitiveTest = primitiveTestRepository.findByName(scriptCreateDTO.getPrimitiveTestName());
		if (null != primitiveTest) {
			script.setPrimitiveTest(primitiveTest);
		} else {
			LOGGER.error("Primitive test not found with the name: " + scriptCreateDTO.getPrimitiveTestName());
			throw new ResourceNotFoundException(Constants.PRIMITIVE_TEST_NAME, scriptCreateDTO.getPrimitiveTestName());
		}

		// Set user group in the script
		UserGroup userGroup = userGroupRepository.findByName(scriptCreateDTO.getUserGroup());
		if (userGroup != null) {
			script.setUserGroup(userGroup);
		}

		// Get the module based on the primitive test
		Module module = primitiveTest.getModule();
		if (module == null) {
			LOGGER.error("Module not found for the primitive test: " + primitiveTest.getName());
			throw new TDKServiceException("Module not found for the primitive test: " + primitiveTest.getName());
		}
		script.setModule(module);

		// Set the category based on the module
		Category category = this.getCategoryBasedOnModule(module);
		script.setCategory(category);

		// Get script location based on the module and category
		String scriptLocation = this.getScriptLocation(module, category);

		// Validate the script file before saving
		this.validateScriptFile(scriptFile, scriptCreateDTO.getName(), scriptLocation);

		// Save the script file
		this.saveScriptFile(scriptFile, scriptLocation);

		// Save the script details in the database after the python file is saved
		script.setScriptLocation(scriptLocation);

		// If the file is saved successfully, save the script details
		Script savedScriptWithDevicetypes = null;
		try {

			script.setScriptLocation(scriptLocation);
			Script savedScript = scriptRepository.save(script);
			List<DeviceType> deviceTypes = this.getScriptDevicetypes(scriptCreateDTO.getDeviceTypes());
			script.setDeviceTypes(deviceTypes);
			savedScriptWithDevicetypes = scriptRepository.save(script);
			if (null == savedScriptWithDevicetypes) {
				LOGGER.error("Error saving script with Device types");
				scriptRepository.delete(savedScript);
			}
		} catch (Exception e) {
			LOGGER.error("Error saving script with device types: " + e.getMessage());
			e.printStackTrace();
			throw new TDKServiceException("Error saving script with device types: " + e.getMessage());
		}
		return null != savedScriptWithDevicetypes;

	}

	/**
	 * This method is used to update the script.
	 * 
	 * @param scriptFile      - the script file
	 * @param scriptUpdateDTO - the script update dto
	 * @return - true if the script is updated successfully, false otherwise
	 */
	@Override
	public boolean updateScript(MultipartFile scriptFile, ScriptDTO scriptUpdateDTO) {

		LOGGER.info("Updating script : " + scriptUpdateDTO.toString());

		// Check if the script ID is present in the database or not
		Script script = scriptRepository.findById(scriptUpdateDTO.getId()).orElseThrow(
				() -> new ResourceNotFoundException(Constants.SCRIPT_ID, scriptUpdateDTO.getId().toString()));

		// Updating the script entity with the updated script details
		script = MapperUtils.updateScript(script, scriptUpdateDTO);

		if (!(Utils.isEmpty(scriptUpdateDTO.getName())) && !(scriptUpdateDTO.getName().equals(script.getName()))) {
			LOGGER.error("Script name should not be changed for the existing script: " + script.getName());
			throw new UserInputException(
					"Script name should not be changed for the existing script. Please create a new script with the new name if needed.");
		}

		// Primitive test and thus the module is not editable or changable. So there
		// won't be any change in scriptlocation, primitive test and thus module. If the
		// script file is changed, then the script is saved in the same location
		if (!scriptFile.isEmpty()) {
			this.validateScriptFile(scriptFile, script.getName(), script.getScriptLocation());
			// This will replave the existing file with the new file
			this.saveScriptFile(scriptFile, script.getScriptLocation());
		}

		// Set devicetypes in the script entity if the devicetypes are updated
		if (null != scriptUpdateDTO.getDeviceTypes() || !scriptUpdateDTO.getDeviceTypes().isEmpty()) {
			List<DeviceType> deviceType = this.getScriptDevicetypes(scriptUpdateDTO.getDeviceTypes());
			script.setDeviceTypes(deviceType);
		}

		Script updatedScript = scriptRepository.save(script);
		return (null != updatedScript);
	}

	/**
	 * This method is used to delete the script.
	 * 
	 * @param scriptId - the script
	 * @return - true if the script is deleted successfully, false otherwise
	 */
	@Override
	public boolean deleteScript(Integer scriptId) {
		LOGGER.info("Deleting script: " + scriptId.toString());
		Script script = scriptRepository.findById(scriptId)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.SCRIPT_ID, scriptId.toString()));
		try {
			scriptRepository.delete(script);
			this.deleteScriptFile(script.getName() + Constants.PYTHON_FILE_EXTENSION, script.getScriptLocation());
			LOGGER.info("Script deleted successfully: " + scriptId.toString());
			return true;
		} catch (Exception e) {
			LOGGER.error("Error deleting script: " + e.getMessage());
		}
		return false;
	}

	/**
	 * This method is used to get the list of scripts based on the module.
	 * 
	 * @param moduleName - the module name
	 * @return - the list of scripts based on the module
	 */
	@Override
	public List<ScriptListDTO> findAllScriptsByModule(String moduleName) {
		LOGGER.info("Getting all scripts based on the module: " + moduleName);
		Module module = moduleRepository.findByName(moduleName);
		if (module == null) {
			LOGGER.error("Module not found with the name: " + moduleName);
			throw new ResourceNotFoundException(Constants.MODULE, moduleName);
		}

		List<Script> scripts = scriptRepository.findAllByModule(module);
		List<ScriptListDTO> scriptListDTO = new ArrayList<>();
		for (Script script : scripts) {
			ScriptListDTO scriptDTO = MapperUtils.convertToScriptListDTO(script);
			scriptListDTO.add(scriptDTO);
			LOGGER.info("Script: " + script.getName() + " added to the list");
		}

		return scriptListDTO;
	}

	/**
	 * This method is used to get all the scripts based on the module with the
	 * category
	 * 
	 * @param category - the category
	 * @return - the list of scripts based on the module with the category
	 */
	@Override
	public List<ScriptModuleDTO> findAllScriptByModuleWithCategory(String category) {
		LOGGER.info("Getting all scripts based on the module");

		// Get the category based on the category name
		Category categoryValue = Category.valueOf(category);
		if (categoryValue == null) {
			LOGGER.error("Category not found with the name: " + category);
			throw new ResourceNotFoundException(Constants.CATEGORY, category);
		}

		// Get all the modules based on the category
		List<Module> modules = moduleRepository.findAllByCategory(categoryValue);

		List<ScriptModuleDTO> scriptModuleDTOList = new ArrayList<>();
		// If no modules are found for the category, then throw an exception
		if (modules.isEmpty()) {
			LOGGER.error("No modules found for the category: " + category);
			throw new TDKServiceException("No modules found for the category: " + category);
		}

		for (Module module : modules) {
			List<ScriptListDTO> scripts = this.findAllScriptsByModule(module.getName());
			ScriptModuleDTO moduleDTO = new ScriptModuleDTO();
			moduleDTO.setModuleId(module.getId());
			moduleDTO.setModuleName(module.getName());
			moduleDTO.setScripts(scripts);
			moduleDTO.setTestGroupName(module.getTestGroup().getName());
			scriptModuleDTOList.add(moduleDTO);
			LOGGER.info("Module: " + module.getName() + " added to the list");
		}
		return scriptModuleDTOList;
	}

	/**
	 * This method is used to get the script details by testscriptId.
	 * 
	 * @param scriptId - the script id
	 * @return - the script
	 */
	public ScriptDTO findScriptById(Integer scriptId) {
		LOGGER.info("Getting script details by scriptId: " + scriptId);
		Script script = scriptRepository.findById(scriptId)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.SCRIPT_ID, scriptId.toString()));
		ScriptDTO scriptDTO = MapperUtils.convertToScriptDTO(script);
		if (null != script.getDeviceTypes()) {
			scriptDTO.setDeviceTypes(this.getDeviceTypesAsStringList(script.getDeviceTypes()));

		}
		LOGGER.info("Script details: " + scriptDTO.toString());
		return scriptDTO;
	}

	/**
	 * This method is used to get the script details by testScriptName.
	 * 
	 * @param testScriptName - the module name
	 * @return - the script
	 */

	@Override
	public ByteArrayInputStream testCaseToExcel(String testScriptName) {
		LOGGER.info("Received request to download test case as excel for test script: " + testScriptName);
		Script script = scriptRepository.findByName(testScriptName);
		if (script == null) {
			LOGGER.error("Test script not found with the name: " + testScriptName);
			throw new ResourceNotFoundException(Constants.SCRIPT_NAME, testScriptName);
		}
		List<Script> scripts = new ArrayList<>();
		scripts.add(script);
		return createExcelFromTestCasesDetailsInScript(scripts, "TEST_CASE_" + testScriptName);
	}

	/**
	 * This method is used to get the script details by module.
	 * 
	 * @param moduleName - the module name
	 * @return - the script
	 */

	@Override
	public ByteArrayInputStream testCaseToExcelByModule(String moduleName) {
		LOGGER.info("Received request to download test case as excel for module: " + moduleName);

		Module module = moduleRepository.findByName(moduleName);
		if (module == null) {
			LOGGER.error("Module not found with the name: " + moduleName);
			throw new ResourceNotFoundException(Constants.MODULE, moduleName);
		}
		List<Script> script = scriptRepository.findAllByModule(module);
		return createExcelFromTestCasesDetailsInScript(script, "TEST_CASE_" + moduleName);
	}

	/**
	 * Check if the script already exists with the same name or not in the database
	 * 
	 * @param scriptCreateDTO - the script details
	 */
	private void checkIfScriptExists(ScriptCreateDTO scriptCreateDTO) {
		if (scriptRepository.existsByName(scriptCreateDTO.getName())) {
			LOGGER.error("Script already exists with the same name: " + scriptCreateDTO.getName());
			throw new ResourceAlreadyExistsException(Constants.SCRIPT_NAME, scriptCreateDTO.getName());
		}
	}

	/**
	 * Get the list of deviceTypes as list of Stringbased on the deviceTypes name
	 * 
	 * @param deviceTypes
	 * @return
	 */
	private List<String> getDeviceTypesAsStringList(List<DeviceType> deviceTypes) {
		List<String> deviceTypeList = new ArrayList<>();
		for (DeviceType deviceType : deviceTypes) {
			deviceTypeList.add(deviceType.getName());
		}
		return deviceTypeList;
	}

	/**
	 * Save the script file in the location based on the module and category
	 * 
	 * @param scriptFile     - the script file
	 * @param scriptLocation - the script location
	 */
	private void saveScriptFile(MultipartFile scriptFile, String scriptLocation) {
		try {
			Path uploadPath = Paths.get(AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + scriptLocation
					+ Constants.FILE_PATH_SEPERATOR);
			if (!Files.exists(uploadPath)) {
				Files.createDirectories(uploadPath);
			}
			Path filePath = uploadPath.resolve(scriptFile.getOriginalFilename());
			Files.copy(scriptFile.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
			LOGGER.info("File uploaded successfully: {}", scriptFile.getOriginalFilename());
		} catch (IOException e) {
			e.printStackTrace();
			LOGGER.error("Error saving file: " + e.getMessage());
			throw new TDKServiceException("Error saving file: " + e.getMessage());
		} catch (Exception ex) {
			ex.printStackTrace();
			LOGGER.error("Error saving file: ", ex.getMessage());
			throw new TDKServiceException("Error saving file: " + ex.getMessage());

		}
	}

	/**
	 * Delete the script file from the location
	 * 
	 * @param scriptName     - the script name
	 * @param scriptLocation - the script location
	 */
	private void deleteScriptFile(String scriptName, String scriptLocation) {
		try {
			Path uploadPath = Paths.get(AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + scriptLocation
					+ Constants.FILE_PATH_SEPERATOR);
			if (!Files.exists(uploadPath)) {
				Files.createDirectories(uploadPath);
			}
			Path filePath = uploadPath.resolve(scriptName);
			System.out.println("Deleting file: " + filePath.toString());
			Files.delete(filePath);
			LOGGER.info("File deleted successfully: {}", scriptName);
		} catch (IOException e) {
			e.printStackTrace();
			LOGGER.error("Error deleting file: " + e.getMessage());
			throw new TDKServiceException("Error deleting file: " + e.getMessage());
		} catch (Exception ex) {
			ex.printStackTrace();
			LOGGER.error("Error deleting file: ", ex.getMessage());
			throw new TDKServiceException("Error deleting file: " + ex.getMessage());

		}
	}

	/**
	 * Validate the script file before saving it in the location
	 * 
	 * @param scriptFile      - the script file
	 * @param scriptName - the script details
	 * @param scriptLocation  - the script location
	 */
	private void validateScriptFile(MultipartFile scriptFile, String scriptName, String scriptLocation) {
		if (scriptFile.isEmpty()) {
			LOGGER.error("Script file is empty");
			throw new UserInputException("Script file is empty");
		}
		if (!(scriptName + Constants.PYTHON_FILE_EXTENSION).equals(scriptFile.getOriginalFilename())) {
			LOGGER.error("Script name and file name are not same");
			throw new UserInputException("Script name and Script file name are not the same");
		}
		if (!scriptFile.getOriginalFilename().endsWith(Constants.PYTHON_FILE_EXTENSION)) {
			LOGGER.error("Invalid file extension: " + scriptFile.getOriginalFilename());
			throw new UserInputException("Invalid file extension: " + scriptFile.getOriginalFilename());
		}
	}

	/**
	 * Get the list of deviceType based on the deviceType name
	 * 
	 * @param deviceTypes - list of deviceType names
	 * @return deviceTypes - list of deviceTypes
	 */
	private List<DeviceType> getScriptDevicetypes(List<String> deviceTypes) {
		List<DeviceType> deviceTypeList = new ArrayList<>();
		for (String deviceTypeName : deviceTypes) {
			DeviceType deviceType = deviceTypeRepository.findByName(deviceTypeName);
			if (null != deviceType) {
				deviceTypeList.add(deviceType);
			} else {
				LOGGER.error("deviceType not found with the name: " + deviceTypeName);
				throw new ResourceNotFoundException(Constants.DEVICE_TYPE, deviceTypeName);
			}
		}
		return deviceTypeList;
	}

	/**
	 * Get the script location path without base location based on the module and
	 * category
	 * 
	 * @param module   the module
	 * @param category the category
	 * @return filePath - script location path without t
	 */
	private String getScriptLocation(Module module, Category category) {
		LOGGER.info("Getting script location based on module and category: " + module.getName() + " - "
				+ category.getName());
		String filePath = "";
		String categoryFolderName = commonService.getFolderBasedOnCategory(category);
		String moduleFolderName = module.getName();
		String testGroupFolderName = commonService.getFolderBasedOnModuleType(module.getTestGroup());
		if (!Utils.isEmpty(categoryFolderName) && !Utils.isEmpty(moduleFolderName)
				&& !Utils.isEmpty(testGroupFolderName)) {
			filePath = String.format("%s/%s/%s", categoryFolderName, moduleFolderName, testGroupFolderName);
		} else {
			LOGGER.error("Invalid folder names: categoryFolderName: " + categoryFolderName + " moduleFolderName: "
					+ moduleFolderName + " testGroupFolderName: " + testGroupFolderName);
			throw new TDKServiceException("Invalid folder names: categoryFolderName: " + categoryFolderName
					+ " moduleFolderName: " + moduleFolderName + " testGroupFolderName: " + testGroupFolderName);
		}
		return filePath;

	}

	/**
	 * Get the category based on the module
	 * 
	 * @param module the primitive test
	 * @return category - RDKV, RDKB, RDKC, RDKV_RDKSERVICE
	 */
	private Category getCategoryBasedOnModule(Module module) {
		LOGGER.info("Getting category based on module: " + module.getName());
		if (module.getCategory().equals(Category.RDKV_RDKSERVICE)) {
			return Category.RDKV_RDKSERVICE;
		} else if (module.getCategory().equals(Category.RDKV)) {
			return Category.RDKV;
		} else if (module.getCategory().equals(Category.RDKB)) {
			return Category.RDKB;
		} else if (module.getCategory().equals(Category.RDKC)) {
			return Category.RDKC;
		} else {
			throw new TDKServiceException("Category is not found for the module: " + module.getName());
		}
	}

	/**
	 * Create excel from test cases information in script.
	 *
	 * @param scripts the test cases
	 * @param sheetName the sheet name
	 * @return the byte array input stream
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	private ByteArrayInputStream createExcelFromTestCasesDetailsInScript(List<Script> scripts, String sheetName) {
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
					dataRow.createCell(4).setCellValue(Utils
							.convertListToCommaSeparatedString(this.getDeviceTypesAsStringList(script.getDeviceTypes())));
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

}
