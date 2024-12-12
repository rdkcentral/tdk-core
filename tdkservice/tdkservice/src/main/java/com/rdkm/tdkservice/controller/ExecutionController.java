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

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.dto.ExecutionDetailsResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionListResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionNameRequestDTO;
import com.rdkm.tdkservice.dto.ExecutionResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionResultResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionSummaryResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionTriggerDTO;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.service.IExecutionService;
import com.rdkm.tdkservice.service.IFileService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;

/**
 * This class is used to handle the execution related operations.
 *
 */
@RestController
@RequestMapping("/execution")
public class ExecutionController {

	private static final Logger LOGGER = LoggerFactory.getLogger(ExecutionController.class);

	@Autowired
	private IExecutionService executionService;

	@Autowired
	private IFileService fileService;

	/**
	 * This method is used to trigger the execution.
	 * 
	 * @param executionTrigger - the execution trigger
	 * @return ResponseEntity<ExecutionResponseDTO>
	 */
	@Operation(summary = "Trigger the execution")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Execution triggered successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to trigger the execution"),
			@ApiResponse(responseCode = "400", description = "Execution trigger request is invalid") })
	@PostMapping("/trigger")
	public ResponseEntity<?> triggerExecution(@RequestBody ExecutionTriggerDTO executionTriggerDTO) {
		LOGGER.info("Trigger execution called");
		ExecutionResponseDTO responseBody = executionService.triggerExecution(executionTriggerDTO);
		if (null != responseBody) {
			LOGGER.info("Execution triggered successfully");
			return ResponseEntity.status(HttpStatus.OK).body(responseBody);
		} else {
			LOGGER.error("Failed to trigger the execution");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to trigger the execution");
		}
	}

	/**
	 * This method is used to save the execution result details.
	 * 
	 * @param execId
	 * @param resultData
	 * @param execResult
	 * @param expectedResult
	 * @param resultStatus
	 * @param testCaseName
	 * @param execDevice
	 * 
	 * @return ResponseEntity<String>
	 */
	@Operation(summary = "Save the execution result details")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Result Details saved successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to save Result Details") })
	@GetMapping("/saveResultDetails")
	public ResponseEntity<String> getExecutionResult(@RequestParam String execId, @RequestParam String resultData,
			@RequestParam String execResult, @RequestParam String expectedResult, @RequestParam String resultStatus,
			@RequestParam String testCaseName, @RequestParam String execDevice) {
		LOGGER.info("Save result Details ids called");
		boolean saved = executionService.saveExecutionResult(execId, resultData, execResult, expectedResult,
				resultStatus, testCaseName, execDevice);
		if (saved) {
			return ResponseEntity.status(HttpStatus.OK).body("Result Details saved successfully");
		} else {
			LOGGER.error("Failed to save Result Details");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to save Result Details");
		}
	}

	/**
	 * This method is used to save the execution status details.
	 * 
	 * @param execId
	 * @param statusData
	 * @param execDevice
	 * @param execResult
	 * 
	 * @return ResponseEntity<String>
	 */
	@Operation(summary = "Save the execution status details")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Status Details saved successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to save Status Details") })
	@GetMapping("/saveLoadModuleStatus")
	public ResponseEntity<String> saveLoadModuleStatus(@RequestParam String execId, @RequestParam String statusData,
			@RequestParam String execDevice, @RequestParam String execResult) {

		LOGGER.info("Save result Details ids called");
		boolean isModuleStatusSaved = executionService.saveLoadModuleStatus(execId, statusData, execDevice, execResult);
		if (isModuleStatusSaved) {
			return ResponseEntity.status(HttpStatus.OK).body("Load Module Status saved successfully");
		} else {
			LOGGER.error("Failed to save Load Module Status");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to save Load Module Status");
		}
	}

	/**
	 * This method is used to get the client port from the python scripts.
	 * 
	 * @param deviceIP
	 * @param agentPort
	 * @return ResponseEntity<String>
	 */
	@Operation(summary = "Get client port")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Client port fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to fetch client port") })
	@GetMapping("/getClientPort")
	public ResponseEntity<String> getClientPort(@RequestParam String deviceIP, @RequestParam String agentPort) {
		try {
			JSONObject result = executionService.getClientPort(deviceIP, agentPort);
			return ResponseEntity.status(HttpStatus.OK).body(result.toString());
		} catch (Exception e) {
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to fetch client port: " + e.getMessage());
		}
	}

	/**
	 * This method is used to get the executions by category. with pagination added
	 * 
	 * @param category - the category RDKV, B, C
	 * @param page     - the page number
	 * @param size     - size in page
	 * @param sortBy   - by default it is date
	 * @param sortDir  - by default it is desc
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Get executions by category")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Executions fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to fetch executions") })
	@GetMapping("/getExecutionsByCategory")
	public ResponseEntity<?> getExecutionsByCategory(@RequestParam String category,
			@RequestParam(defaultValue = "0") int page, @RequestParam(defaultValue = "10") int size,
			@RequestParam(defaultValue = "createdDate") String sortBy,
			@RequestParam(defaultValue = "desc") String sortDir) {
		LOGGER.info("Fetching executions for category: " + category);
		ExecutionListResponseDTO result = executionService.getExecutionsByCategory(category, page, size, sortBy,
				sortDir);
		LOGGER.info("Executions fetched successfully");
		return result != null ? ResponseEntity.ok(result)
				: ResponseEntity.status(HttpStatus.NOT_FOUND).body("Execution data with this condition is not found");
	}

	/**
	 * This method is to search executions based on test suite name and script name
	 * 
	 * @param scriptTestSuiteName - full script name or testsuite name or partial
	 *                            name for search query
	 * @param categoryName        - RDKV, RDKB, RDKC
	 * @param page                - the page number
	 * @param size                - size in page
	 * @param sortBy              - by default it is date
	 * @param sortDir             - by default it is desc
	 * @return ExecutionListResponseDTO
	 */
	@Operation(summary = "Search executions based on  test suite and script name")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Execution details fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to fetch execution details"),
			@ApiResponse(responseCode = "400", description = "Execution data with this condition is not found") })
	@GetMapping("/getExecutionsByScriptTestsuite/{scriptTestSuiteName}")
	public ResponseEntity<?> getExecutionsByTestsuite(@PathVariable String scriptTestSuiteName,
			@RequestParam String categoryName, @RequestParam(defaultValue = "0") int page,
			@RequestParam(defaultValue = "10") int size, @RequestParam(defaultValue = "createdDate") String sortBy,
			@RequestParam(defaultValue = "desc") String sortDir) {
		LOGGER.info("Fetching executions for test suite or script: " + scriptTestSuiteName);
		ExecutionListResponseDTO executionListResponseDTO = executionService
				.getExecutionsByScriptTestsuite(scriptTestSuiteName, categoryName, page, size, sortBy, sortDir);
		return executionListResponseDTO != null ? ResponseEntity.ok(executionListResponseDTO)
				: ResponseEntity.status(HttpStatus.NOT_FOUND).body("Execution data with this condition is not found");
	}

	/**
	 * This method is used to get the executions by device name with pagination
	 * 
	 * @param deviceName   - the device name
	 * @param categoryName - RDKV, RDKB, RDKC
	 * @param page         - the page number
	 * @param size         - size in page
	 * @param sortBy       - by default it is date
	 * @param sortDir      - by default it is desc
	 * @return response
	 */
	@Operation(summary = "Get executions by device name")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Execution details fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to fetch execution details") })
	@GetMapping("/getExecutionsByDevice/{deviceName}")
	public ResponseEntity<?> getExecutionsByDeviceName(@PathVariable String deviceName,
			@RequestParam String categoryName, @RequestParam(defaultValue = "0") int page,
			@RequestParam(defaultValue = "10") int size, @RequestParam(defaultValue = "createdDate") String sortBy,
			@RequestParam(defaultValue = "desc") String sortDir) {
		LOGGER.info("Fetching executions for deviceName " + deviceName);
		ExecutionListResponseDTO executionListResponseDTO = executionService.getExecutionsByDeviceName(deviceName,
				categoryName, page, size, sortBy, sortDir);
		return executionListResponseDTO != null ? ResponseEntity.ok(executionListResponseDTO)
				: ResponseEntity.status(HttpStatus.NOT_FOUND).body("Execution data with this condition is not found");
	}

	/**
	 *
	 * This method is used to get the executions by user name with pagination
	 * 
	 * @param deviceName   - the device name
	 * @param categoryName - RDKV, RDKB, RDKC
	 * @param page         - the page number
	 * @param size         - size in page
	 * @param sortBy       - by default it is date
	 * @param sortDir      - by default it is desc
	 * @return
	 */
	@Operation(summary = "Get executions by user")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Execution details fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to fetch execution details") })
	@GetMapping("/getExecutionsByUsername/{username}")
	public ResponseEntity<?> getExecutionsByUser(@PathVariable String username, @RequestParam String categoryName,
			@RequestParam(defaultValue = "0") int page, @RequestParam(defaultValue = "10") int size,
			@RequestParam(defaultValue = "createdDate") String sortBy,
			@RequestParam(defaultValue = "desc") String sortDir) {
		LOGGER.info("Fetching executions for user " + username);
		ExecutionListResponseDTO executionListResponseDTO = executionService.getExecutionsByUser(username, categoryName,
				page, size, sortBy, sortDir);
		return executionListResponseDTO != null ? ResponseEntity.ok(executionListResponseDTO)
				: ResponseEntity.status(HttpStatus.NOT_FOUND).body("Execution data with this condition is not found");
	}

	/**
	 * This method is used to get the execution logs.
	 * 
	 * @param executionResultID - executionResultID
	 * @return the response of the execution logs
	 */
	@Operation(summary = "Get the execution logs")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Execution logs fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to fetch execution logs") })
	@GetMapping("/getExecutionLogs")
	public ResponseEntity<?> getExecutionLogs(@RequestParam String executionResultID) {
		LOGGER.info("Fetching execution logs for exec with Id: " + executionResultID);
		String result = executionService.getExecutionLogs(executionResultID);
		return result != null ? ResponseEntity.ok(result)
				: ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to fetch execution logs");
	}

	/**
	 * This method is used to get the execution name.
	 * 
	 * @param nameRequest - the name request
	 * @return The execution name generated
	 */
	@Operation(summary = "Get the execution name")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Execution Name fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to get Execution Name") })
	@PostMapping("/getExecutionName")
	public ResponseEntity<String> getExecutionName(@RequestBody ExecutionNameRequestDTO nameRequest) {
		LOGGER.info("Get execution name called");
		try {
			String result = executionService.getExecutionName(nameRequest);
			return ResponseEntity.ok(result);
		} catch (Exception e) {
			LOGGER.error("Failed to get Execution Name: {}", e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to get Execution Name");
		}
	}

	/**
	 * This method is used to get the execution result details.
	 * 
	 * @param execResultId
	 * 
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Get the execution result details")
	@ApiResponse(responseCode = "200", description = "Execution Result fetched successfully")
	@ApiResponse(responseCode = "500", description = "Failed to get Execution Result")
	@GetMapping("/getExecutionResult")
	public ResponseEntity<?> getExecutionResult(@RequestParam UUID execResultId) {
		LOGGER.info("Get execution result details called");
		ExecutionResultResponseDTO executinResultResponse = executionService.getExecutionResult(execResultId);
		if (null != executinResultResponse) {
			LOGGER.info("Execution results obtained");
			return ResponseEntity.status(HttpStatus.OK).body(executinResultResponse);
		} else {
			LOGGER.error("Execution results not  found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Execution results not  found");
		}
	}

	/**
	 * This method is used to get the trend analysis.
	 * 
	 * @param execResultId
	 * 
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Get the trend analysis")
	@ApiResponse(responseCode = "200", description = "Trend Analysis fetched successfully")
	@ApiResponse(responseCode = "500", description = "Failed to get Trend Analysis")
	@GetMapping("/getTrendAnalysis")
	public ResponseEntity<?> getTrendAnalysis(@RequestParam UUID execResultId) {
		LOGGER.info("Get trend analysis called");
		List<String> trendAnalysis = executionService.getTrendAnalysis(execResultId);
		if (null != trendAnalysis && !trendAnalysis.isEmpty()) {
			LOGGER.info("Trend Analysis of last 5 script found");
			return ResponseEntity.status(HttpStatus.OK).body(trendAnalysis);
		} else {
			LOGGER.error("Trend Analysis Not  found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Trend Analysis Not  found");
		}
	}

	/**
	 * This method is used to abort the execution.
	 * 
	 * @param execId
	 * 
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Abort the execution")
	@ApiResponse(responseCode = "200", description = "Execution aborted successfully")
	@ApiResponse(responseCode = "500", description = "Failed to abort the execution")
	@PostMapping("/abortexecution")
	public ResponseEntity<?> abortExecution(@RequestParam UUID execId) {
		LOGGER.info("Abort execution called");
		boolean isAborted = executionService.abortExecution(execId);
		if (isAborted) {
			LOGGER.info("Execution aborted successfully");
			return ResponseEntity.status(HttpStatus.OK)
					.body("The execution will be aborted after the current script execution is completed");
		} else {
			LOGGER.error("Failed to abort the execution");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to abort the execution");

		}
	}

	/*
	 * This method is used to repeat the execution
	 * 
	 * @param execId
	 * 
	 * @return ResponseEntity
	 */
	@Operation(summary = "Repeat the execution")
	@ApiResponse(responseCode = "200", description = "Execution repeated successfully")
	@ApiResponse(responseCode = "500", description = "Failed to repeat the execution")
	@PostMapping("/repeatExecution")
	public ResponseEntity<?> repeatExecution(@RequestParam UUID execId) {
		LOGGER.info("Repeat execution called");
		boolean isRepeated = executionService.repeatExecution(execId);
		if (isRepeated) {
			LOGGER.info("Execution repeated successfully");
			return ResponseEntity.status(HttpStatus.OK).body("The execution will be repeated");
		} else {
			LOGGER.error("Failed to repeat the execution");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to repeat the execution");
		}
	}

	/**
	 * This method is used to rerun the failed script.
	 * 
	 * @param execId
	 * 
	 * @return ResponseEntity
	 * 
	 */
	@Operation(summary = "Rerun the failed script")
	@ApiResponse(responseCode = "200", description = "Execution rerun successfully")
	@ApiResponse(responseCode = "500", description = "Failed to rerun the failed script")
	@PostMapping("/rerunFailedScript")
	public ResponseEntity<?> reRunFailedScript(@RequestParam UUID execId) {
		LOGGER.info("Rerun failed script called");
		boolean isRerun = executionService.reRunFailedScript(execId);
		if (isRerun) {
			LOGGER.info("Execution rerun successfully");
			return ResponseEntity.status(HttpStatus.OK).body("The failed script will be rerun");
		} else {
			LOGGER.error("Failed to rerun the failed script");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to rerun the failed script");
		}
	}

	/**
	 * This method is used to get the execution details.
	 * 
	 * @param id
	 * 
	 * @return ResponseEntity<ExecutionDetailsResponseDTO>
	 */
	@Operation(summary = "Get the execution details")
	@ApiResponse(responseCode = "200", description = "Execution details fetched successfully")
	@ApiResponse(responseCode = "500", description = "Failed to get Execution details")
	@GetMapping("/getExecutionDetails/{id}")
	public ResponseEntity<?> getExecutionDetails(@PathVariable UUID id) {
		LOGGER.info("Fetching execution details for ID: {}", id);
		ExecutionDetailsResponseDTO response = executionService.getExecutionDetails(id);
		if (null != response) {
			LOGGER.info("Execution details fetched successfully for ID: {}", id);
			return ResponseEntity.status(HttpStatus.OK).body(response);
		} else {
			LOGGER.error("Failed to get Execution details for ID: {}", id);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to get Execution details");
		}
	}

	/**
	 * This method is used to delete the executions.
	 * 
	 * @param ids
	 * 
	 * @return ResponseEntity
	 */
	@Operation(summary = "Delete the execution")
	@ApiResponse(responseCode = "201", description = "Execution deleted successfully")
	@ApiResponse(responseCode = "404", description = "Execution not found")
	@DeleteMapping("/delete/{id}")
	public ResponseEntity<String> deleteExecution(@PathVariable UUID id) {
		LOGGER.info("Deleting execution by ID: {}", id);
		boolean isDeleted = executionService.deleteExecution(id);
		if (isDeleted) {
			LOGGER.info("Execution deleted successfully: {}", id);
			return ResponseEntity.status(HttpStatus.CREATED).body("Execution deleted successfully");
		} else {
			LOGGER.error("Execution not found with ID: {}", id);
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Execution not found");
		}
	}

	/**
	 * This method is used to delete the executions by IDs.
	 * 
	 * @param ids
	 * 
	 * @return ResponseEntity
	 */

	@Operation(summary = "Delete the executions by IDs")
	@ApiResponse(responseCode = "201", description = "Executions deleted successfully")
	@ApiResponse(responseCode = "404", description = "Executions not found")
	@PostMapping("/deletelistofexecutions")
	public ResponseEntity<String> deleteExecutions(@RequestBody List<UUID> ids) {
		LOGGER.info("Deleting executions by IDs: {}", ids);
		boolean isDeleted = executionService.deleteExecutions(ids);
		if (isDeleted) {
			LOGGER.info("Executions deleted successfully: {}", ids);
			return ResponseEntity.status(HttpStatus.CREATED).body("Executions deleted successfully");
		} else {
			LOGGER.error("Executions not found with IDs: {}", ids);
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Executions not found");
		}
	}

	/**
	 * This method is used to get the execution users.
	 * 
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Get the execution users")
	@ApiResponse(responseCode = "200", description = "Unique users fetched successfully")
	@ApiResponse(responseCode = "500", description = "Failed to get unique users")
	@GetMapping("/getusers")
	public ResponseEntity<?> getUniqueUsers() {
		LOGGER.info("Fetching unique users");
		List<String> users = executionService.getUniqueUsers();
		if (null != users) {
			LOGGER.info("Unique users fetched successfully");
			return ResponseEntity.status(HttpStatus.OK).body(users);
		} else {
			LOGGER.error("Failed to get unique users");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Failed to get users users");
		}
	}

	/**
	 * This method is used to get the execution result details.
	 *
	 * @param execResultId
	 *
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Upload Logs")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Logs uploaded successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to upload logs") })
	@PostMapping("/uploadLogs")
	public ResponseEntity<String> uploadLogs(@RequestParam MultipartFile logFile, @RequestParam String fileName) {
		try {
			LOGGER.info("Fetching upload logs");
			String uploaded = fileService.uploadLogs(logFile, fileName);
			return ResponseEntity.ok(uploaded);
		} catch (Exception e) {
			LOGGER.error("Failed to upload logs: {}", e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to upload logs: " + e.getMessage());
		}
	}

	/**
	 * This method is used to get the image name or current firmware version based
	 * on execution ID.
	 * 
	 * @param executionId
	 * @return
	 */
	@Operation(summary = "Fetches the image name or current firmware version based on execution ID.")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Successfully retrieved the image name"),
			@ApiResponse(responseCode = "400", description = "Bad request, invalid parameters"),
			@ApiResponse(responseCode = "500", description = "Internal server error") })
	@GetMapping("/getDeviceImageName")
	public ResponseEntity<String> getImageName(@RequestParam String executionId) {
		try {
			LOGGER.info("Going to get image name");
			String imageName = fileService.getImageName(executionId);
			if (imageName.isEmpty()) {
				return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Image name or firmware version not found.");
			}
			return ResponseEntity.ok(imageName);
		} catch (Exception e) {
			// Log the error (optional, depending on logging setup)
			LOGGER.error("Error fetching image name for executionId: {}", executionId, e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("An error occurred while processing the request.");
		}
	}

	/**
	 * Endpoint to download a device log file.
	 *
	 * @param executionId    The execution ID
	 * @param executionResId The execution resource ID
	 * @param fileName       The name of the log file to download
	 * @return ResponseEntity with the file resource or error message
	 */

	@Operation(summary = "Download a specific log file", description = "Fetches and returns a specific log file based on execution ID, executionResId, and file name.")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Successfully retrieved the log file"),
			@ApiResponse(responseCode = "404", description = "Log file not found"),
			@ApiResponse(responseCode = "500", description = "Internal server error") })
	@GetMapping("/downloadDeviceLogFile")
	public ResponseEntity<?> downloadDeviceLogFile(@RequestParam String executionResId, @RequestParam String fileName) {

		LOGGER.info("Inside downloadLogFile controller with fileName: {}", fileName);
		Resource resource = null;
		try {
			// Call service method to retrieve the log file resource
			resource = fileService.downloadDeviceLogFile(executionResId, fileName);
		} catch (ResourceNotFoundException ex) {
			// Log and return not found error if the file doesn't exist
			LOGGER.error("Log file not found: {}", fileName);
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Log file not found: " + fileName);
		} catch (Exception e) {
			// Log and return internal server error for other exceptions
			LOGGER.error("Error in downloading log file: {}", e.getMessage(), e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in downloading log file");
		}

		if (resource != null && resource.exists()) {
			LOGGER.info("Log file downloaded successfully");
			return ResponseEntity.status(HttpStatus.OK)
					.header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + resource.getFilename() + "\"")
					.header("Access-Control-Expose-Headers", "content-disposition").body(resource);
		} else {
			LOGGER.error("Error in downloading log file: {}", fileName);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in downloading log file");
		}
	}

	/**
	 * Endpoint to download all device log files as a zip.
	 *
	 * @param executionResultId The execution result ID.
	 * @return A ResponseEntity containing the zip file.
	 * @throws IOException If there is an error during file reading or zip creation.
	 */
	@Operation(summary = "Download all device log files as a zip", description = "Fetches and returns all log files for the specified execution ID and execution result ID as a zip file.")
	@ApiResponses(value = {
			@ApiResponse(responseCode = "200", description = "Successfully retrieved the log files as a zip"),
			@ApiResponse(responseCode = "500", description = "Internal server error") })
	@GetMapping("/downloadAllDeviceLogFiles")
	public ResponseEntity<byte[]> downloadDeviceLogs(@RequestParam("executionResultId") String executionResultId)
			throws IOException, IOException {
		LOGGER.info("Inside download all device log files as a zip");
		byte[] zipFile = fileService.downloadAllDeviceLogFiles(executionResultId);

		// Set headers for downloading the zip file
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
		headers.setContentDispositionFormData("attachment", "device_logs.zip");

		return new ResponseEntity<>(zipFile, headers, HttpStatus.OK);
	}

	/**
	 * Endpoint to get the log file names for a given executionId and
	 * executionResId.
	 * 
	 * @param executionResultId The execution result ID.
	 * @return A ResponseEntity containing the list of log file names.
	 */
	@Operation(summary = "Get the log file names", description = "Fetches the list of log file names for the specified execution ID and execution result ID.")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Successfully retrieved log file names"),
			@ApiResponse(responseCode = "204", description = "No log files found"),
			@ApiResponse(responseCode = "500", description = "Internal server error") })
	@GetMapping("/getDeviceLogFileNames")
	public ResponseEntity<List<String>> getDeviceLogFileNames(
			@RequestParam("executionResultId") String executionResultId) {
		List<String> logFileNames = fileService.getDeviceLogFileNames(executionResultId);
		if (logFileNames.isEmpty()) {
			return ResponseEntity.status(HttpStatus.NO_CONTENT).body(logFileNames); // Return 204 NO CONTENT if no files
																					// found
		}
		return ResponseEntity.ok(logFileNames);
	}

	/**
	 * Endpoint to get the content of the agent log file for a given execution ID
	 * and execution result ID.
	 *
	 * @param executionId    The execution ID.
	 * @param executionResId The execution result ID.
	 * @param baseLogPath    The base log path.
	 * @return The content of the log file as a String.
	 */
	@GetMapping("/getAgentLogContent")
	public ResponseEntity<String> getAgentLogContent(@RequestParam("executionResId") String executionResId) {
		String logContent = fileService.getAgentLogContent(executionResId);

		if (logContent.equals("Log file not found")) {
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body(logContent); // 404 if file not found
		} else if (logContent.equals("Error reading log file")) {
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(logContent); // 500 on error
		}
		return ResponseEntity.ok(logContent); // Return the log content with 200 OK
	}

	/**
	 * Endpoint to download an agent log file for a specific execution ID and result
	 * ID.
	 *
	 * @param executionResId The result ID associated with the log file.
	 * @return ResponseEntity with the file resource or an error message if the file
	 *         is not found or an error occurs.
	 */
	@Operation(summary = "Download an agent log file for a specific execution ID and result ID")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Agent log file downloaded successfully"),
			@ApiResponse(responseCode = "404", description = "Agent log file not found"),
			@ApiResponse(responseCode = "500", description = "Error downloading agent log file") })
	@GetMapping("/downloadAgentLog")
	public ResponseEntity<?> downloadAgentLogFile(@RequestParam String executionResId) {

		LOGGER.info("Inside downloadAgentLogFile controller with fileName");

		try {
			// Call the service method to download the agent log file
			Resource resource = fileService.downloadAgentLogFile(executionResId);

			// Prepare the response headers for file download
			return ResponseEntity.ok()
					.header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + resource.getFilename() + "\"")
					.header("Access-Control-Expose-Headers", "content-disposition")
					.contentType(MediaType.APPLICATION_OCTET_STREAM).body(resource);
		} catch (ResourceNotFoundException ex) {
			// Log and return not found response
			LOGGER.error("Agent log file not found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Agent log file not found ");
		} catch (Exception e) {
			// Log and return internal server error response
			LOGGER.error("Error downloading agent log file: {}", e.getMessage(), e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error downloading agent log file: " + e.getMessage());
		}
	}

	/**
	 * This method is used to get the module wise execution summary.
	 * 
	 * @param executionId - ID of the execution entity
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Get the module wise execution summary")
	@ApiResponse(responseCode = "200", description = "Module wise summary fetched successfully")
	@ApiResponse(responseCode = "404", description = "Execution data with this condition is not found")
	@GetMapping("/getModulewiseExecutionSummary")
	public ResponseEntity<?> getModulewiseExecutionSummary(@RequestParam UUID executionId) {
		LOGGER.info("Get module wise summary called for the executionId {}", executionId.toString());
		Map<String, ExecutionSummaryResponseDTO> executionSummaryMap = executionService
				.getModulewiseExecutionSummary(executionId);
		return executionSummaryMap != null ? ResponseEntity.ok(executionSummaryMap)
				: ResponseEntity.status(HttpStatus.NOT_FOUND).body("Execution data with this condition is not found");

	}

}
