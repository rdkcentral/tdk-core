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

package com.rdkm.tdkservice.controller;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.util.List;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.dto.ScriptCreateDTO;
import com.rdkm.tdkservice.dto.ScriptDTO;
import com.rdkm.tdkservice.dto.ScriptListDTO;
import com.rdkm.tdkservice.dto.ScriptModuleDTO;
import com.rdkm.tdkservice.service.IScriptService;
import com.rdkm.tdkservice.util.Constants;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/**
 * The ScriptController class is used to handle script related operations. It
 * contains the APIs to create, update, delete and get the script.
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/script")
public class ScriptController {

	private static final Logger LOGGER = LoggerFactory.getLogger(ScriptController.class);

	@Autowired
	IScriptService scriptService;

	/**
	 * This method is used to create the script. The script is created by uploading
	 * the script file and providing the script details.
	 * 
	 * @param scriptCreateDTO - the script create dto
	 * @param file            - the script file
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Create Script", description = "Create Script")
	@ApiResponse(responseCode = "201", description = "Script created successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in creating script")
	@PostMapping("/create")
	public ResponseEntity<?> createScript(@Valid @RequestPart("scriptCreateData") ScriptCreateDTO scriptCreateDTO,
			@RequestPart("scriptFile") MultipartFile scriptFile) {
		LOGGER.info("Received create script request: " + scriptCreateDTO.toString());
		boolean isScriptCreated = scriptService.saveScript(scriptFile, scriptCreateDTO);
		if (isScriptCreated) {
			LOGGER.info("Script created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Script created successfully");
		} else {
			LOGGER.error("Error in creating script");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in creating script");
		}
	}

	/**
	 * This method is used to update the script. The script is updated by uploading
	 * 
	 * @param scriptUpdateDTO - the script update dto
	 * @param scriptFile      - the script
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Update Script", description = "Update Script")
	@ApiResponse(responseCode = "200", description = "Script updated successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in updating script")
	@PutMapping("/update")
	public ResponseEntity<?> updateScript(@Valid @RequestPart("scriptUpdateData") ScriptDTO scriptUpdateDTO,
			@RequestPart("scriptFile") MultipartFile scriptFile) {
		LOGGER.info("Received update script request: " + scriptUpdateDTO.toString());
		boolean isScriptUpdated = scriptService.updateScript(scriptFile, scriptUpdateDTO);
		if (isScriptUpdated) {
			LOGGER.info("Script updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Script updated successfully");
		} else {
			LOGGER.error("Error in updating script");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in updating script");
		}
	}

	/**
	 * This method is used to delete the script
	 * 
	 * @param scriptId - the script id
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Delete Script", description = "Delete Script")
	@ApiResponse(responseCode = "200", description = "Script deleted successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@DeleteMapping("/delete/{id}")
	public ResponseEntity<?> deleteScript(@PathVariable UUID id) {
		LOGGER.info("Received delete script request: " + id);
		boolean isScriptDeleted = scriptService.deleteScript(id);
		if (isScriptDeleted) {
			LOGGER.info("Script deleted successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Script deleted successfully");
		} else {
			LOGGER.error("Error in deleting script");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in deleting script");
		}
	}

	/**
	 * This method is used to get all the scripts list by module. This will return
	 * the list of scripts for the given module as script id and script name.
	 * 
	 * @param module - the module
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Get all scripts by module", description = "Get all scripts by module")
	@ApiResponse(responseCode = "200", description = "Scripts fetched successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findlistbymodule")
	public ResponseEntity<?> findAllScriptsByModule(@RequestParam String module) {
		LOGGER.info("Received get all scripts request for module: " + module);
		List<ScriptListDTO> scripts = scriptService.findAllScriptsByModule(module);
		if (scripts != null) {
			LOGGER.info("Scripts fetched successfully  for module: " + module);
			return ResponseEntity.status(HttpStatus.OK).body(scripts);
		} else {
			LOGGER.error("Error in fetching scripts");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in fetching scripts for module: " + module);
		}
	}

	/**
	 * This method is used to get the script details by script id.
	 * 
	 * @param scriptId - the script id
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Get Script by Id", description = "Get Script by Id")
	@ApiResponse(responseCode = "200", description = "Script fetched successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findbyid/{id}")
	public ResponseEntity<?> findScriptById(@PathVariable UUID id) {
		LOGGER.info("Received get script by id request for script id: " + id);
		ScriptDTO script = scriptService.findScriptById(id);
		if (script != null) {
			LOGGER.info("Script fetched successfully for script id: " + id);
			return ResponseEntity.status(HttpStatus.OK).body(script);
		} else {
			LOGGER.error("Error in fetching script");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in fetching script for script id: " + id);
		}
	}

	/**
	 * This method is used to get all the scripts by module with category. This will
	 * return the list of scripts for all the modules by the given category.
	 * 
	 * @param category - the category
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Get all scripts by module with category", description = "Get all scripts by module with category")
	@ApiResponse(responseCode = "200", description = "Scripts fetched successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findallbymodulewithcategory")
	public ResponseEntity<?> findAllScriptByModuleWithCategory(@RequestParam String category) {
		LOGGER.info("Received get all scripts request for category: " + category);
		List<ScriptModuleDTO> scripts = scriptService.findAllScriptByModuleWithCategory(category);
		if (scripts != null) {
			LOGGER.info("Scripts fetched successfully for category: " + category);
			return ResponseEntity.status(HttpStatus.OK).body(scripts);
		} else {
			LOGGER.error("Error in fetching scripts");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in fetching scripts for category: " + category);
		}
	}

	/**
	 * This method is used to download the test case as excel
	 * 
	 * @param testScriptName - the test script name
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Download Test Case as Excel", description = "Download Test Case as Excel")
	@ApiResponse(responseCode = "200", description = "Test case downloaded successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/downloadtestcaseasexcel")
	public ResponseEntity<?> downloadTestCaseToExcel(@RequestParam String testScriptName) {
		ByteArrayInputStream in = scriptService.testCaseToExcel(testScriptName);
		// Prepare response with the Excel file
		if (in == null || in.available() == 0) {
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in downloading test case as excel");
		}
		HttpHeaders headers = new HttpHeaders();
		headers.add("Content-Disposition",
				"attachment; filename=TestCase_" + testScriptName + Constants.EXCEL_FILE_EXTENSION);
		LOGGER.info("Test case downloaded successfully");
		return ResponseEntity.status(HttpStatus.OK).headers(headers).contentType(MediaType.APPLICATION_OCTET_STREAM)
				.body(new InputStreamResource(in));
	}

	/**
	 * This method is used to download the test case as excel by module
	 * 
	 * @param moduleName - the module name
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Download Test Case as Excel by Module", description = "Download Test Case as Excel by Module")
	@ApiResponse(responseCode = "200", description = "Test case downloaded successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/downloadtestcaseasexcelbymodule")
	public ResponseEntity<?> downloadTestCaseToExcelByModule(@RequestParam String moduleName) {
		ByteArrayInputStream in = scriptService.testCaseToExcelByModule(moduleName);
		if (in == null || in.available() == 0) {
			LOGGER.error("Error in downloading test case as excel by module");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in downloading test case as excel by module");
		}
		// Prepare response with the Excel file
		HttpHeaders headers = new HttpHeaders();
		headers.add("Content-Disposition",
				"attachment; filename=TestCase_" + moduleName + Constants.EXCEL_FILE_EXTENSION);
		LOGGER.info("Downloaded test case as excel by module");
		return ResponseEntity.status(HttpStatus.OK).headers(headers).contentType(MediaType.APPLICATION_OCTET_STREAM)
				.body(new InputStreamResource(in));
	}

	/**
	 * This method is used to get all the scripts by category. This will return the
	 * list of scripts for the given category.
	 * 
	 * @param category - the category
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Get all scripts by  category", description = "Get all scripts by category")
	@ApiResponse(responseCode = "200", description = "Scripts fetched successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findlistbycategory")
	public ResponseEntity<?> findAllScriptByCategory(@RequestParam String category) {
		LOGGER.info("Received get all scripts request for category: " + category);
		List<ScriptListDTO> scripts = scriptService.findAllScriptsByCategory(category);
		if (scripts != null) {
			LOGGER.info("Scripts fetched successfully for category: " + category);
			return ResponseEntity.status(HttpStatus.OK).body(scripts);
		} else {
			LOGGER.error("Error in fetching scripts");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in fetching scripts for category: " + category);
		}
	}

	/**
	 * This method is used to download the script
	 * 
	 * @param scriptName - the script name
	 * @return ResponseEntity - the response entity
	 * @throws IOException
	 */
	@Operation(summary = "Download Script", description = "Download Script")
	@ApiResponse(responseCode = "200", description = "Script downloaded successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/downloadscriptdatazip")
	public ResponseEntity<?> downloadScript(@RequestParam String scriptName) {
		byte[] zipBytes = scriptService.generateScriptZip(scriptName);
		if (zipBytes == null) {
			LOGGER.error("Error in downloading script ");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in downloading script");
		}
		HttpHeaders headers = new HttpHeaders();
		headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + scriptName + ".zip");
		LOGGER.info("Script downloaded successfully");
		return ResponseEntity.status(HttpStatus.OK).headers(headers).contentType(MediaType.APPLICATION_OCTET_STREAM)
				.body(zipBytes);
	}

	/**
	 * This method is used to upload the ZIP file
	 * 
	 * @param file - the ZIP file
	 * @return ResponseEntity - the response entity
	 */

	@Operation(summary = "Upload ZIP file", description = "Upload ZIP file")
	@ApiResponse(responseCode = "200", description = "ZIP file has been successfully processed")
	@ApiResponse(responseCode = "500", description = "Error in processing ZIP file")
	@PostMapping("/uploadscriptdatazip")
	public ResponseEntity<String> uploadScript(@RequestParam("file") MultipartFile file) {
		LOGGER.info("Received upload ZIP file request: " + file.getOriginalFilename());
		boolean scriptUpload = scriptService.uploadZipFile(file);
		if (scriptUpload) {
			LOGGER.info("ZIP file has been successfully processed");
			return ResponseEntity.status(HttpStatus.OK).body("ZIP file has been successfully processed");
		} else {
			LOGGER.error("Error in processing ZIP file");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in processing ZIP file");
		}

	}

	/**
	 * This method is used to get the script template details by primitive test
	 * name.
	 *
	 * @param primitiveTestName - the primitive test name
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Get Script Template", description = "Get Script Template")
	@ApiResponse(responseCode = "200", description = "Script template fetched successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in fetching script template")
	@GetMapping("/template/{primitiveTestName}")
	public ResponseEntity<String> getScriptTemplate(@PathVariable String primitiveTestName) {
		String scriptTemplate = scriptService.scriptTemplate(primitiveTestName);
		return ResponseEntity.ok(scriptTemplate);
	}

	
	/**
	 * This method is used to download all the test cases as Excel by Module ZIP by
	 * Category
	 * 
	 * @param category - the category
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Download all Test Case as Module Excel  zip by Category", description = "Download all Test Case as Excel by Module ZIP by Category")
	@ApiResponse(responseCode = "200", description = "Test case downloaded successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/downloadalltestcasezipbycategory")
	public ResponseEntity<?> downloadAllTestCaseAsZipByCategory(@RequestParam String category) {
		LOGGER.info("Received download all test case as excel as zip  by category : " + category);
		ByteArrayInputStream in = scriptService.testCaseToExcelByCategory(category);
		if (in == null || in.available() == 0) {
			LOGGER.error("Error in downloading all test case as excel by module ZIP by category");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in downloading all test case as excel by module ZIP by category");
		}
		// Prepare response with the Excel file
		HttpHeaders headers = new HttpHeaders();
		headers.add(HttpHeaders.CONTENT_DISPOSITION,
				"attachment; filename=TestCase_" + category + Constants.ZIP_EXTENSION);
		LOGGER.info("Downloaded all test case as excel by module ZIP by category");
		return ResponseEntity.status(HttpStatus.OK).headers(headers).contentType(MediaType.APPLICATION_OCTET_STREAM)
				.body(new InputStreamResource(in));
	}
}
