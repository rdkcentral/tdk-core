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

import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.rdkm.tdkservice.dto.ExecutionResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionTriggerDTO;
import com.rdkm.tdkservice.service.IExecutionService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;

/*
 * 	The ExecutionController class is used to handle the execution related operations
 */

@RestController
@RequestMapping("/execution")
public class ExecutionController {

	@Autowired
	private IExecutionService executionService;

	private static final Logger LOGGER = LoggerFactory.getLogger(ExecutionController.class);

	/**
	 * This method is used to trigger the execution.
	 * 
	 * @param executionTrigger
	 * 
	 * @return ResponseEntity<ExecutionResponseDTO>
	 */
	@Operation(summary = "Trigger the execution")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Execution triggered successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to trigger the execution") })
	@PostMapping("/trigger")
	public ResponseEntity<ExecutionResponseDTO> triggerExecution(@RequestBody ExecutionTriggerDTO executionTriggerDTO) {
		ExecutionResponseDTO responseBody = executionService.triggerExecution(executionTriggerDTO);
		return ResponseEntity.ok(responseBody);
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
		// How to avoid passing all these parameters in the URL
		boolean saved = executionService.saveExecutionResult(execId, resultData, execResult, expectedResult,
				resultStatus, testCaseName, execDevice);
		if (saved) {
			return ResponseEntity.ok("Result Details saved successfully");
		} else {
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

		// How to avoid passing all these parameters in the URL
		executionService.saveLoadModuleStatus(execId, statusData, execDevice, execResult);
		return ResponseEntity.ok("Load Module Status saved successfully");
	}

	/**
	 * This method is used to get the client port.
	 * 
	 * @param deviceIP
	 * @param agentPort
	 * 
	 * @return ResponseEntity<String>
	 */
	@Operation(summary = "Get client port")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Client port fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to fetch client port")

	})
	@GetMapping("/getClientPort")
	public ResponseEntity<String> getClientPort(@RequestParam String deviceIP, @RequestParam String agentPort) {
		try {
			JSONObject result = executionService.getClientPort(deviceIP, agentPort);
			return ResponseEntity.ok(result.toString());
		} catch (Exception e) {
			return ResponseEntity.status(500).body("Failed to fetch client port: " + e.getMessage());
		}
	}
}