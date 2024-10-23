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
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.Year;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.zip.ZipEntry;
import java.util.zip.ZipException;
import java.util.zip.ZipFile;
import java.util.zip.ZipOutputStream;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import com.rdkm.tdkservice.config.AppConfig;
import com.rdkm.tdkservice.dto.ScriptCreateDTO;
import com.rdkm.tdkservice.dto.ScriptDTO;
import com.rdkm.tdkservice.dto.ScriptListDTO;
import com.rdkm.tdkservice.dto.ScriptModuleDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.enums.TestType;
import com.rdkm.tdkservice.exception.MandatoryFieldException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.exception.TDKServiceException;
import com.rdkm.tdkservice.exception.UserInputException;
import com.rdkm.tdkservice.model.DeviceType;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.model.PrimitiveTest;
import com.rdkm.tdkservice.model.Script;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.DeviceTypeRepository;
import com.rdkm.tdkservice.repository.ModuleRepository;
import com.rdkm.tdkservice.repository.PrimitiveTestRepository;
import com.rdkm.tdkservice.repository.ScriptRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.service.IScriptService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;

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
		Script savedScript = null;
		try {
			script.setScriptLocation(scriptLocation);
			// Set the device types in the script entity
			List<DeviceType> deviceTypes = this.getScriptDevicetypes(scriptCreateDTO.getDeviceTypes());
			script.setDeviceTypes(deviceTypes);
			savedScript = scriptRepository.save(script);
		} catch (ResourceNotFoundException e) {
			// Let ResourceNotFoundException propagate to the global exception handler
			LOGGER.error("Device type doesnt exist " + e.getMessage());
			throw e;
		} catch (Exception e) {
			LOGGER.error("Error saving script with device types: " + e.getMessage());
			e.printStackTrace();
		}
		return null != savedScript;

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

		if (!Utils.isEmpty(scriptUpdateDTO.getName())) {
			if (scriptRepository.existsByName(scriptUpdateDTO.getName())
					&& !(scriptUpdateDTO.getName().equals(script.getName()))) {
				LOGGER.info("Script already exists with the same name: " + scriptUpdateDTO.getName());
				throw new ResourceAlreadyExistsException(Constants.SCRIPT, scriptUpdateDTO.getName());
			} else {
				script.setName(scriptUpdateDTO.getName());
			}
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
	public boolean deleteScript(UUID scriptId) {
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
	 * This method is used to get the list of scripts based on the category.
	 * 
	 */
	@Override
	public List<ScriptListDTO> findAllScriptsByCategory(String categoryName) {
		LOGGER.info("Getting all scripts based on the category: " + categoryName);
		Category category = commonService.validateCategory(categoryName);
		List<Script> scripts = scriptRepository.findAllByCategory(category);
		List<ScriptListDTO> scriptListDTO = new ArrayList<>();
		for (Script script : scripts) {
			ScriptListDTO scriptDTO = MapperUtils.convertToScriptListDTO(script);
			scriptListDTO.add(scriptDTO);
			LOGGER.info("Script: " + script.getName() + " added to the list");
		}
		LOGGER.info("Returning all scripts based on the category: " + categoryName);
		return scriptListDTO;

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
		Category categoryValue = commonService.validateCategory(category);

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
	public ScriptDTO findScriptById(UUID scriptId) {
		LOGGER.info("Getting script details by scriptId: " + scriptId);
		Script script = scriptRepository.findById(scriptId)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.SCRIPT_ID, scriptId.toString()));
		ScriptDTO scriptDTO = MapperUtils.convertToScriptDTO(script);
		if (null != script.getDeviceTypes()) {
			scriptDTO.setDeviceTypes(commonService.getDeviceTypesAsStringList(script.getDeviceTypes()));
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
		return commonService.createExcelFromTestCasesDetailsInScript(scripts, "TEST_CASE_" + testScriptName);
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
		return commonService.createExcelFromTestCasesDetailsInScript(script, "TEST_CASE_" + moduleName);
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
	 * Save the script file in the location based on the module and category
	 * 
	 * @param scriptFile     - the script file
	 * @param scriptLocation - the script location
	 */
	private void saveScriptFile(MultipartFile scriptFile, String scriptLocation) {
		try {
			MultipartFile fileWithHeader = addHeader(scriptFile);
			Path uploadPath = Paths.get(AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + scriptLocation
					+ Constants.FILE_PATH_SEPERATOR);
			if (!Files.exists(uploadPath)) {
				Files.createDirectories(uploadPath);
			}
			Path filePath = uploadPath.resolve(fileWithHeader.getOriginalFilename());
			Files.copy(fileWithHeader.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
			LOGGER.info("File uploaded successfully: {}", fileWithHeader.getOriginalFilename());
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

	/*
	 * The method to add header to script python file
	 */
	private MultipartFile addHeader(MultipartFile scriptFile) throws IOException {

		String fileContent = new String(scriptFile.getBytes());
		String currentYear = Year.now().toString();

		String header = Constants.HEADER_TEMPLATE.replace("CURRENT_YEAR", currentYear);

		// Prepend the header to the file content
		String updatedContent = header + fileContent;
		return new MockMultipartFile(scriptFile.getName(), // Name of the file
				scriptFile.getOriginalFilename(), // Original filename
				scriptFile.getContentType(), // Content type (e.g., text/plain)
				updatedContent.getBytes() // Updated content as bytes
		);

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
	 * @param scriptFile     - the script file
	 * @param scriptName     - the script details
	 * @param scriptLocation - the script location
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
		commonService.validatePythonFile(scriptFile);
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
	 * Generate a ZIP file containing a Python script and an XML file with the test
	 * case details
	 * 
	 * @param scriptName - the script name
	 * @return - the ZIP file as a byte array
	 * @throws IOException - the IO exception
	 */

	@Override
	public byte[] generateScriptZip(String scriptName) {
		String xmlContent;
		File getPythonScriptFile;
		try {
			xmlContent = generateTestCaseXml(scriptName);
			getPythonScriptFile = getPythonFile(scriptName);
		} catch (ResourceNotFoundException e) {
			LOGGER.error("Test script not found: " + e.getMessage());
			throw e;
		}

		ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
		try (ZipOutputStream zipOutputStream = new ZipOutputStream(byteArrayOutputStream)) {
			ZipEntry xmlEntry = new ZipEntry(scriptName + Constants.XML_FILE_EXTENSION);
			zipOutputStream.putNextEntry(xmlEntry);
			zipOutputStream.write(xmlContent.getBytes());
			zipOutputStream.closeEntry();

			ZipEntry scriptEntry = new ZipEntry(getPythonScriptFile.getName());
			zipOutputStream.putNextEntry(scriptEntry);
			Files.copy(getPythonScriptFile.toPath(), zipOutputStream);
			zipOutputStream.closeEntry();
		} catch (FileNotFoundException e) {
			LOGGER.error("File not found: " + e.getMessage());
			throw new TDKServiceException("File not found: " + e.getMessage());
		} catch (ZipException e) {
			LOGGER.error("Error processing zip file: " + e.getMessage());
			throw new TDKServiceException("Error processing zip file: " + e.getMessage());
		} catch (IOException e) {
			LOGGER.error("IO error: " + e.getMessage());
			throw new TDKServiceException("IO error: " + e.getMessage());
		}

		return byteArrayOutputStream.toByteArray();
	}

	/**
	 * Get the python file based on the script name
	 * 
	 * @param scriptName - the script name
	 * @return - the python file
	 */

	public File getPythonFile(String scriptName) {
		Script testCase = scriptRepository.findByName(scriptName);
		if (testCase == null) {
			LOGGER.error("Test script not found with the name: " + scriptName);
			throw new ResourceNotFoundException(Constants.SCRIPT_NAME, scriptName);
		}
		String baseDir = System.getProperty(Constants.USER_DIRECTORY); // Get the current working directory
		Path scriptFilePath = Paths.get(baseDir, Constants.BASE_FILESTORE_FOLDER, testCase.getScriptLocation(),
				scriptName + Constants.PYTHON_FILE_EXTENSION); // Combine base directory and relative path
		File scriptFile = scriptFilePath.toFile();
		if (!scriptFile.exists()) {
			throw new ResourceNotFoundException("Script file not found at location: ", testCase.getScriptLocation());
		}
		return scriptFile;

	}

	/**
	 * Generate test case XML based on the test script name
	 * 
	 * @param scriptName - the script name
	 * @return - the test case XML
	 */

	public String generateTestCaseXml(String scriptName) {

		Script testCase = scriptRepository.findByName(scriptName);
		if (testCase == null) {
			LOGGER.error("Test script not found with the name: " + scriptName);
			throw new ResourceNotFoundException(Constants.SCRIPT_NAME, scriptName);
		}
		try {
			DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder docBuilder = docFactory.newDocumentBuilder();

			var doc = docBuilder.newDocument();
			var rootElement = doc.createElement(Constants.XML);
			doc.appendChild(rootElement);

			createElement(doc, rootElement, "name", testCase.getName());

			createElement(doc, rootElement, "primitive_test_name", testCase.getPrimitiveTest().getName());

			createElement(doc, rootElement, "synopsis", testCase.getSynopsis());

			String executionTime = String.valueOf(testCase.getExecutionTimeOut());
			if (executionTime != null && !executionTime.isEmpty()) {
				createElement(doc, rootElement, "execution_time", executionTime);
			}
			String longDuration = String.valueOf(testCase.isLongDuration());
			if (longDuration != null && !longDuration.isEmpty()) {
				createElement(doc, rootElement, "long_duration", longDuration);
			}
			String skip = String.valueOf(testCase.isSkipExecution());
			if (skip != null && !skip.isEmpty()) {
				createElement(doc, rootElement, "skip", skip);
			}
			if (testCase.isSkipExecution()) {
				createElement(doc, rootElement, "skip_remarks", testCase.getSkipRemarks());
			}
			createElement(doc, rootElement, "test_case_id", testCase.getTestId());
			createElement(doc, rootElement, "test_objective", testCase.getObjective());
			createElement(doc, rootElement, "test_type", testCase.getTestType().toString());

			// Create <box_types> element and add <box_type> child elements
			Element deviceTypesElement = doc.createElement("device_types");
			rootElement.appendChild(deviceTypesElement);

			// Loop through the list of box types and create <box_type> elements
			for (DeviceType deviceType : testCase.getDeviceTypes()) {
				createElement(doc, deviceTypesElement, "device_type", deviceType.getName());
			}
			createElement(doc, rootElement, "pre_requisite", testCase.getPrerequisites());
			createElement(doc, rootElement, "api_or_interface_used", testCase.getApiOrInterfaceUsed());
			createElement(doc, rootElement, "input_parameters", testCase.getInputParameters());
			createElement(doc, rootElement, "automation_approach", testCase.getAutomationApproach());
			createElement(doc, rootElement, "expected_output", testCase.getExpectedOutput());
			createElement(doc, rootElement, "priority", testCase.getPriority());
			createElement(doc, rootElement, "test_stub_interface", testCase.getTestStubInterface());
			createElement(doc, rootElement, "release_version", testCase.getReleaseVersion());
			createElement(doc, rootElement, "remarks", testCase.getRemarks());

			// Convert the document to a String
			TransformerFactory transformerFactory = TransformerFactory.newInstance();
			Transformer transformer = transformerFactory.newTransformer();
			transformer.setOutputProperty(OutputKeys.INDENT, Constants.YES);
			transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, Constants.NO);
			transformer.setOutputProperty(OutputKeys.METHOD, Constants.XML);

			DOMSource domSource = new DOMSource(doc);
			ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
			StreamResult result = new StreamResult(outputStream);
			transformer.transform(domSource, result);
			return outputStream.toString();
		} catch (Exception e) {
			LOGGER.error("Error generating test case XML: " + e.getMessage());
			throw new TDKServiceException("Error generating test case XML: " + e.getMessage());
		}

	}

	/**
	 * Upload a ZIP file containing a Python script and an XML file with the script
	 * details
	 * 
	 * @param file - the ZIP file
	 * @return true if the ZIP file is uploaded successfully, false otherwise
	 */

	@Override
	public boolean uploadZipFile(MultipartFile file) {
		LOGGER.info("Uploading zip file: " + file.getOriginalFilename());

		// Validate file is a zip
		if (!file.getContentType().equals("application/zip")
				&& !file.getOriginalFilename().endsWith(Constants.ZIP_EXTENSION)) {
			LOGGER.error("Only ZIP files are allowed");
			throw new UserInputException("Only ZIP files are allowed");
		}

		try {
			// Create a temporary file to store the uploaded zip
			File tempZipFile = File.createTempFile("uploaded-", Constants.ZIP_EXTENSION);
			file.transferTo(tempZipFile);

			try (ZipFile zip = new ZipFile(tempZipFile)) {
				Enumeration<? extends ZipEntry> entries = zip.entries();
				boolean pythonFileExists = false;
				boolean xmlFileExists = false;
				MultipartFile pythonFile = null;
				ScriptCreateDTO scriptCreateDTO = null;

				// First pass to check if both Python (.py) and XML (.xml) files exist
				while (entries.hasMoreElements()) {
					ZipEntry entry = entries.nextElement();
					// Check for Python file
					if (entry.getName().endsWith(Constants.PYTHON_FILE_EXTENSION)) {
						pythonFileExists = true;
					}
					// Check for XML file
					if (entry.getName().endsWith(Constants.XML_FILE_EXTENSION)) {
						xmlFileExists = true;
					}
				}
				// If either Python or XML file is missing, throw a UserInputException
				if (!pythonFileExists || !xmlFileExists) {
					LOGGER.error("Both Python and XML files are required in the ZIP file.");
					throw new UserInputException("Both Python and XML files are required in the ZIP file.");
				}

				// Reset entries to process the files now that we know both exist
				entries = zip.entries();
				// Process the Python and XML files
				while (entries.hasMoreElements()) {
					ZipEntry entry = entries.nextElement();
					// Handle Python file
					if (entry.getName().endsWith(Constants.PYTHON_FILE_EXTENSION)) {
						try (InputStream pyInputStream = zip.getInputStream(entry)) {
							// Convert Python file to MultipartFile
							pythonFile = convertScriptFileToMultipartFile(pyInputStream, entry.getName());
						}
					}
					// Handle XML file
					else if (entry.getName().endsWith(Constants.XML_FILE_EXTENSION)) {
						try (InputStream xmlInputStream = zip.getInputStream(entry)) {
							// Convert XML file to ScriptCreateDTO
							scriptCreateDTO = convertXmlToScriptCreateDTO(xmlInputStream);
						}
					}
				}

				// Validate that both files were processed
				if (pythonFile != null && scriptCreateDTO != null) {
					boolean savedScript = saveScript(pythonFile, scriptCreateDTO);
					tempZipFile.delete();
					LOGGER.info("Script XML saved successfully");
					return savedScript;
				} else {
					LOGGER.error(
							"Error processing the zip file, either the XML or Python file was not processed correctly.");
					throw new TDKServiceException(
							"Error processing the zip file: XML or Python file processing failed.");
				}
			}

		} catch (UserInputException e) {
			// Let UserInputException propagate to the global exception handler
			LOGGER.error("Error uploading zip file: " + e.getMessage());
			throw e;
		} catch (ResourceNotFoundException e) {
			LOGGER.error("Error uploading zip file: " + e.getMessage());
			throw e;
		} catch (ResourceAlreadyExistsException e) {
			LOGGER.error("Error uploading zip file: " + e.getMessage());
			throw e;
		} catch (Exception e) {
			LOGGER.error("Error uploading zip file: " + e.getMessage());
			throw new TDKServiceException("Error uploading zip file: " + e.getMessage());
		}
	}

	/**
	 * Convert the XML file to ScriptCreateDTO
	 * 
	 * @param xmlInputStream - the XML input stream
	 * @return - the ScriptCreateDTO
	 */
	private ScriptCreateDTO convertXmlToScriptCreateDTO(InputStream xmlInputStream) {

		ScriptCreateDTO testCase = null;
		// Parse XML
		try {
			DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
			DocumentBuilder builder = factory.newDocumentBuilder();
			Document document = builder.parse(xmlInputStream);
			ValidatorFactory validatorFactory = Validation.buildDefaultValidatorFactory();
			Validator validator = validatorFactory.getValidator();

			// Normalize XML structure
			document.getDocumentElement().normalize();

			// Extract fields from XML
			NodeList nodeList = document.getElementsByTagName(Constants.XML);
			for (int i = 0; i < nodeList.getLength(); i++) {
				Node node = nodeList.item(i);

				if (node.getNodeType() == Node.ELEMENT_NODE) {
					Element element = (Element) node;

					testCase = new ScriptCreateDTO();
					testCase.setName(getElementValue(element, "name"));
					testCase.setPrimitiveTestName(getElementValue(element, "primitive_test_name"));
					testCase.setExecutionTimeOut(Integer.parseInt(getElementValue(element, "execution_time")));
					testCase.setLongDuration(Boolean.parseBoolean(getElementValue(element, "long_duration")));
					testCase.setSkipExecution(Boolean.parseBoolean(getElementValue(element, "skip")));
					testCase.setSynopsis(getElementValue(element, "synopsis"));
					testCase.setTestId(getElementValue(element, "test_case_id"));
					testCase.setObjective(getElementValue(element, "test_objective"));
					TestType testType = TestType.valueOf(getElementValue(element, "test_type"));
					testCase.setTestType(testType.toString());
					testCase.setPrerequisites(getElementValue(element, "pre_requisite"));
					testCase.setApiOrInterfaceUsed(getElementValue(element, "api_or_interface_used"));
					testCase.setInputParameters(getElementValue(element, "input_parameters"));
					testCase.setAutomationApproach(getElementValue(element, "automation_approach"));
					testCase.setExpectedOutput(getElementValue(element, "expected_output"));
					testCase.setPriority(getElementValue(element, "priority"));
					testCase.setTestStubInterface(getElementValue(element, "test_stub_interface"));
					testCase.setReleaseVersion(getElementValue(element, "release_version"));
					testCase.setRemarks(getElementValue(element, "remarks"));

					// Handle box_types
					List<String> deviceType = new ArrayList<>();
					NodeList deviceTypeNodes = element.getElementsByTagName("device_type");
					for (int j = 0; j < deviceTypeNodes.getLength(); j++) {
						deviceType.add(deviceTypeNodes.item(j).getTextContent());
					}
					testCase.setDeviceTypes(deviceType);
					validateAndCreateScript(testCase, validator);
				}
			}
		} catch (Exception e) {
			LOGGER.error("Error parsing XML and saving to database: " + e.getMessage());
			throw new UserInputException(e.getMessage());

		}
		return testCase;

	}

	/**
	 * Validate the script details before saving
	 * 
	 * @param scriptCreateDTO - the script details
	 * @param validator       - the validator
	 */
	private void validateAndCreateScript(ScriptCreateDTO scriptCreateDTO, Validator validator) {
		Set<ConstraintViolation<ScriptCreateDTO>> violations = validator.validate(scriptCreateDTO);
		if (!violations.isEmpty()) {
			StringBuilder sb = new StringBuilder();
			for (ConstraintViolation<ScriptCreateDTO> violation : violations) {
				sb.append(violation.getMessage()).append(",");
			}
			LOGGER.error("Validation errors: \n" + sb.toString());
			throw new IllegalArgumentException("Validation errors: " + sb.toString());
		}

	}

	/**
	 * Convert the script file to MultipartFile
	 * 
	 * @param inputStream - the input stream
	 * @param fileName    - the file name
	 * @return - the MultipartFile
	 * @throws IOException
	 */
	private MultipartFile convertScriptFileToMultipartFile(InputStream inputStream, String fileName) {
		try {
			LOGGER.info("Converting script file to MultipartFile: " + fileName);
			// Read the input stream and store the content in a byte array
			byte[] fileContent = inputStream.readAllBytes();

			// Create a new MultipartFile (MockMultipartFile in this case)
			return new MockMultipartFile(fileName, fileName, Constants.PYTHON_CONTENT, fileContent);
		} catch (Exception e) {
			LOGGER.error("Error converting script file to MultipartFile: " + e.getMessage());
			throw new TDKServiceException("Error converting script file to MultipartFile: " + e.getMessage());
		}
	}

	/**
	 * Create an element with the tag name and text content
	 * 
	 * @param doc         - the document
	 * @param parent      - the parent element
	 * @param tagName     - the tag name
	 * @param textContent - the text content
	 */
	private void createElement(Document doc, Element parent, String tagName, String textContent) {
		Element element = doc.createElement(tagName);
		element.setTextContent(textContent);
		parent.appendChild(element);
	}

	/**
	 * Get the element value based on the tag name
	 * 
	 * @param parent  - the parent element
	 * @param tagName - the tag name
	 * @return - the element value
	 */
	private String getElementValue(Element parent, String tagName) {
		NodeList nodeList = parent.getElementsByTagName(tagName);
		if (nodeList.getLength() > 0) {
			return nodeList.item(0).getTextContent();
		}
		return null;
	}

	/**
	 * This method is used to get the script template details by primitiveTestName.
	 *
	 * @param primitiveTestName - the primitive test name
	 * @return - the script
	 */
	@Override
	public String scriptTemplate(String primitiveTestName) {

		StringBuilder scriptBuilder = new StringBuilder();

		if (primitiveTestName == null || primitiveTestName.isEmpty()) {
			throw new MandatoryFieldException("Primitive test name cannot be null or empty");
		}

		PrimitiveTest primitiveTest = primitiveTestRepository.findByName(primitiveTestName);
		if (primitiveTest == null) {
			throw new ResourceNotFoundException("Primitive test name: ", primitiveTestName);
		}

		scriptBuilder.append("# use tdklib library,which provides a wrapper for tdk testcase script \r\n")
				.append("import tdklib; \r\n\r\n").append("#Test component to be tested\r\n")
				.append("obj = tdklib.TDKScriptingLibrary(\"").append(primitiveTest.getModule().getName())
				.append("\",\"1\");\r\n\r\n").append("#IP and Port of device type, No need to change,\r\n")
				.append("#This will be replaced with corresponding DUT Ip and port while executing script\r\n")
				.append("ip = <ipaddress>\r\n").append("port = <port>\r\n")
				.append("obj.configureTestCase(ip,port,'');\r\n\r\n")
				.append("#Get the result of connection with test component and DUT\r\n")
				.append("result = obj.getLoadModuleResult();\r\n")
				.append("print(\"[LIB LOAD STATUS]  :  %s\" %result);\r\n\r\n")
				.append("#Prmitive test case which associated to this Script\r\n")
				.append("tdkTestObj = obj.createTestStep('").append(primitiveTestName).append("');\r\n\r\n")
				.append("#Execute the test case in DUT\r\n").append("tdkTestObj.executeTestCase(\"\");\r\n\r\n")
				.append("#Get the result of execution\r\n").append("result = tdkTestObj.getResult();\r\n")
				.append("print(\"[TEST EXECUTION RESULT] : %s\" %result);\r\n\r\n")
				.append("#Set the result status of execution\r\n")
				.append("tdkTestObj.setResultStatus(\"none\");\r\n\r\n").append("obj.unloadModule(\"")
				.append(primitiveTest.getModule().getName()).append("\");");

		return scriptBuilder.toString();
	}

	/**
	 * This method is used to get the Excel of scripts by module based on the
	 * category.
	 * 
	 * @param categoryName - the category name
	 */
	@Override
	public ByteArrayInputStream testCaseToExcelByCategory(String category) {
		LOGGER.info("Received request to download test case as excel for module and category: " + category);
		// Validate the category
		Category categoryValue = commonService.validateCategory(category);
		// Get all the modules based on the category
		List<Module> modules = moduleRepository.findAllByCategory(categoryValue);
		if (modules.isEmpty() || modules == null) {
			LOGGER.error("No modules found for the category: " + category);
			throw new ResourceNotFoundException("Modules for", category);
		}

		try {
			ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
			ZipOutputStream zipOutputStream = new ZipOutputStream(byteArrayOutputStream);
			for (Module module : modules) {
				try {
					ByteArrayInputStream byteArrayInputStream = testCaseToExcelByModule(module.getName());
					ZipEntry zipEntry = new ZipEntry(module.getName() + Constants.EXCEL_FILE_EXTENSION);
					zipOutputStream.putNextEntry(zipEntry);
					byte[] bytes = byteArrayInputStream.readAllBytes();
					zipOutputStream.write(bytes);
					zipOutputStream.closeEntry();
				} catch (Exception e) {
					LOGGER.error("Error creating ZIP entry for module: " + module.getName(), e);
					throw new TDKServiceException("Error creating ZIP entry for module: " + e.getMessage());
				}
			}

			zipOutputStream.finish();
			return new ByteArrayInputStream(byteArrayOutputStream.toByteArray());

		} catch (Exception e) {
			LOGGER.error("Error creating ZIP file: " + e.getMessage(), e);
			throw new TDKServiceException("Error creating ZIP file: " + e.getMessage());
		}
	}

}
