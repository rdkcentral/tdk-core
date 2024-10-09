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
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.dto.TestSuiteCreateDTO;
import com.rdkm.tdkservice.dto.TestSuiteCustomDTO;
import com.rdkm.tdkservice.dto.TestSuiteDTO;
import com.rdkm.tdkservice.service.ITestSuiteService;
import com.rdkm.tdkservice.util.Constants;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/**
 * The TestSuiteController class is a REST controller that handles all the
 * requests related to the test suite.
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/testsuite")
public class TestSuiteController {

	private static final Logger LOGGER = LoggerFactory.getLogger(TestSuiteController.class);

	@Autowired
	ITestSuiteService testSuiteService;

	/**
	 * Create a test suite.
	 * 
	 * @param testSuiteCreateDTO
	 * @return
	 */
	@Operation(summary = "Create test suite", description = "Create test suite")
	@ApiResponse(responseCode = "201", description = "test suite created successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in creating test suite")
	@PostMapping("/create")
	public ResponseEntity<?> createTestSuite(@RequestBody @Valid TestSuiteCreateDTO testSuiteCreateDTO) {
		LOGGER.info("Received create test suite request: " + testSuiteCreateDTO.toString());
		boolean isTestSuiteCreated = testSuiteService.createTestSuite(testSuiteCreateDTO);
		if (isTestSuiteCreated) {
			LOGGER.info("Test suite created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Test suite created successfully");
		} else {
			LOGGER.error("Error in creating script");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in creating Test suite");
		}

	}

	/**
	 * Update the test suite.
	 * 
	 * @param testSuiteDTO - the test suite dto
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Update test suite", description = "Update test suite")
	@ApiResponse(responseCode = "200", description = "test suite updated successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in updating test suite")
	@PostMapping("/update")
	public ResponseEntity<?> updateTestSuite(@RequestBody @Valid TestSuiteDTO testSuiteDTO) {
		LOGGER.info("Received update test suite request: " + testSuiteDTO.toString());
		boolean isTestSuiteUpdated = testSuiteService.updateTestSuite(testSuiteDTO);
		if (isTestSuiteUpdated) {
			LOGGER.info("Test suite updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Test suite updated successfully");
		} else {
			LOGGER.error("Error in updating test suite");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in updating test suite");
		}

	}

	/**
	 * This method is used to get the test suite by id
	 * 
	 * @param testSuiteId - the test suite id
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Get TestSuite By Id", description = "Get test suite by id")
	@ApiResponse(responseCode = "200", description = "Scriptgroup fetched successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findbyid/{id}")
	public ResponseEntity<?> getTestSuiteById(@PathVariable UUID id) {
		LOGGER.info("Received get testSuite by id request: " + id);
		TestSuiteDTO testSuiteDTO = testSuiteService.findTestSuiteById(id);
		if (testSuiteDTO != null) {
			LOGGER.info("Test suite fetched successfully");
			return ResponseEntity.status(HttpStatus.OK).body(testSuiteDTO);
		} else {
			LOGGER.error("Error in fetching test suite");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in fetching test suite");
		}
	}

	/**
	 * This method is used to get All the test suite by category
	 * 
	 * @param category - the test suite category
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Get All TestSuite By Category", description = "Get All test suite by category")
	@ApiResponse(responseCode = "200", description = "Scriptgroup fetched successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findallbycategory")
	public ResponseEntity<?> getAllTestSuiteByCategory(@RequestParam String category) {
		LOGGER.info("Received get testSuite by category request: " + category);
		List<TestSuiteDTO> testSuiteDTOList = testSuiteService.findAllTestSuiteByCategory(category);
		if (testSuiteDTOList != null) {
			LOGGER.info("Test suite fetched successfully");
			return ResponseEntity.status(HttpStatus.OK).body(testSuiteDTOList);
		} else {
			LOGGER.error("Error in fetching test suite");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in fetching test suite by category");
		}
	}

	/**
	 * This method is used to delete the test suite
	 * 
	 * @param scriptId - the test suite id
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Delete TestSuite", description = "Delete test suite")
	@ApiResponse(responseCode = "200", description = "Scriptgroup deleted successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@DeleteMapping("/delete/{id}")
	public ResponseEntity<?> deleteScript(@PathVariable UUID id) {
		LOGGER.info("Received delete testSuite request: " + id);
		boolean isScriptDeleted = testSuiteService.deleteTestSuite(id);
		if (isScriptDeleted) {
			LOGGER.info("Test suite deleted successfully");
			return ResponseEntity.status(HttpStatus.OK).body("test suite deleted successfully");
		} else {
			LOGGER.error("Error in deleting test suite");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in deleting test suite");
		}
	}

	/**
	 * This method is used to download the test cases details for all the scripts in
	 * test suite as excel
	 * 
	 * @param testSuite - the test suite name
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Download TestCases", description = "Download TestCases")
	@ApiResponse(responseCode = "200", description = "TestCases downloaded successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in downloading test cases")
	@GetMapping("/downloadtestcases")
	public ResponseEntity<?> downloadTestCasesAsExcel(@RequestParam String testSuite) {
		LOGGER.info("Received download test cases details for all the scripts in test suite as excel request:");
		ByteArrayInputStream in = testSuiteService.getTestCasesInTestSuiteAsExcel(testSuite);
		if (in == null || in.available() == 0) {
			LOGGER.error("Error in downloading test cases details for all the scripts in test suite as excel");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in downloading test cases details for all the scripts in test suite as excel");
		}
		// Prepare response with the Excel file
		HttpHeaders headers = new HttpHeaders();
		headers.add("Content-Disposition",
				"attachment; filename=TestCase_" + testSuite + Constants.EXCEL_FILE_EXTENSION);
		LOGGER.info("Downloaded test case as excel by module");
		return ResponseEntity.status(HttpStatus.OK).headers(headers).contentType(MediaType.APPLICATION_OCTET_STREAM)
				.body(new InputStreamResource(in));
	}

	/**
	 * This method is used to create the custom test suite
	 * 
	 * @param testSuiteCustomDTO - the test suite custom dto
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Create Custom Test Suite", description = "Create Custom Test Suite")
	@ApiResponse(responseCode = "201", description = "Custom Test Suite created successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in creating Custom Test Suite")
	@PostMapping("/createCustomTestSuite")
	public ResponseEntity<?> createCustomTestSuite(@RequestBody @Valid TestSuiteCustomDTO testSuiteCustomDTO) {
		LOGGER.info("Received create custom test suite request: " + testSuiteCustomDTO.toString());
		boolean isTestSuiteCreated = testSuiteService.createCustomTestSuite(testSuiteCustomDTO);
		if (isTestSuiteCreated) {
			LOGGER.info("Custom Test Suite created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Custom Test Suite created successfully");
		} else {
			LOGGER.error("Error in creating Custom Test Suite");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in creating Custom Test Suite");
		}

	}

	/**
	 * This method is used to download the test suite as XML
	 * 
	 * @param testSuite - the test suite name
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Download test suite xml", description = "Download test suite xml")
	@ApiResponse(responseCode = "200", description = "test suite xml downloaded successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in downloading test suite xml")
	@GetMapping("/downloadtestsuitexml")
	public ResponseEntity<?> downloadTestSuiteXML(@RequestParam String testSuite) {
		LOGGER.info("Received download test suite XML request:");
		ByteArrayInputStream inputStream = testSuiteService.downloadTestSuiteAsXML(testSuite);
		if (inputStream == null || inputStream.available() == 0) {
			LOGGER.error("Error in downloading test suite as XML");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in downloading test suite as XML");
		}
		// Prepare response with the XML file
		HttpHeaders headers = new HttpHeaders();
		headers.add("Content-Disposition", "attachment; filename=" + testSuite + Constants.XML_EXTENSION);
		LOGGER.info("Downloaded test suite as XML");
		return ResponseEntity.status(HttpStatus.OK).headers(headers).contentType(MediaType.APPLICATION_OCTET_STREAM)
				.body(new InputStreamResource(inputStream));
	}

	/**
	 * This method is used to upload the test suite as XML
	 * 
	 * @param scriptFile - the test suite xml file
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Upload test suite xml", description = "Upload test suite xml")
	@ApiResponse(responseCode = "200", description = "test suite uploaded successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in uploading test suite")
	@PostMapping("/uploadtestsuitexml")
	public ResponseEntity<?> uploadTestSuiteXML(@RequestPart("testSuite") MultipartFile testSuite) {
		boolean isTestSuiteUploaded = testSuiteService.uploadTestSuiteAsXML(testSuite);
		if (isTestSuiteUploaded) {
			LOGGER.info("Script names uploaded successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Test suite uploaded successfully");
		} else {
			LOGGER.error("Error in uploading test suites");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in uploading test suites");
		}
	}

	/**
	 * This method is used to update the test suite by module name
	 *
	 * @param moduleName - the module name
	 * @return ResponseEntity - the response entity
	 */
	@Operation(summary = "Update TestSuite By Module Name", description = "Update TestSuite By Module Name")
	@ApiResponse(responseCode = "200", description = "Scriptgroup updated successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PutMapping("/updatetestsuite/{moduleName}/{category}")
	public ResponseEntity<String> updateTestSuiteByModuleNameAndCategory(@PathVariable String moduleName,
			@PathVariable String category) {
		LOGGER.info("Received request to update test suite for module: {} and category: {}", moduleName, category);
		String message = testSuiteService.updateTestSuiteByModuleNameAndCategory(moduleName, category);
		LOGGER.info("Successfully updated test suite for module: {} and category: {}", moduleName, category);
		return ResponseEntity.ok(message);
	}

	/**
	 * This method is used to download all the test suite as XML
	 * 
	 * @param category - the test suite category
	 * @return ResponseEntity - the response entity
	 * 
	 */
	@Operation(summary = "Download All TestSuite xml as zip by category", description = "Download All TestSuite As xml as zip by category")
	@ApiResponse(responseCode = "200", description = "All TestSuite downloaded successfully")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "500", description = "Issue in downloading All TestSuite")
	@GetMapping("/downloadalltestsuitexml")
	public ResponseEntity<?> downloadAllTestSuiteXML(@RequestParam String category) {
		LOGGER.info("Received download all test suite XML request:");
		ByteArrayInputStream inputStream = testSuiteService.downloadAllTestSuiteAsXML(category);
		if (inputStream == null || inputStream.available() == 0) {
			LOGGER.error("Error in downloading all test suite as XML");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in downloading all test suite as XML");
		}
		// Prepare response with the XML file
		HttpHeaders headers = new HttpHeaders();
		headers.add("Content-Disposition", "attachment; filename=" + category + Constants.ZIP_EXTENSION);
		LOGGER.info("Downloaded all test suite xml as zip");
		return ResponseEntity.status(HttpStatus.OK).headers(headers).contentType(MediaType.APPLICATION_OCTET_STREAM)
				.body(new InputStreamResource(inputStream));
	}

}
