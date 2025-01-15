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

import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.rdkm.tdkservice.dto.AnalysisIssueTypewiseSummaryDTO;
import com.rdkm.tdkservice.dto.AnalysisResultDTO;
import com.rdkm.tdkservice.dto.TicketDetailsDTO;
import com.rdkm.tdkservice.service.IExecutionAnalysisService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;

/**
 * This controller class is used to handle the execution analysis related
 * requests.
 *
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/analysis")
public class ExecutionAnalysisController {

	private static final Logger LOGGER = LoggerFactory.getLogger(ExecutionAnalysisController.class);

	@Autowired
	private IExecutionAnalysisService executionAnalysisService;

	/**
	 * Endpoint to save the analysis result for an execution result.
	 *
	 * @param analysisResultRequest the request body containing analysis result
	 *                              details
	 * @return ResponseEntity<String> indicating the result of the save operation
	 */
	@Operation(summary = "Save analysis result for an execution result")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Analysis result saved successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to save analysis result"),
			@ApiResponse(responseCode = "400", description = "Bad request, invalid parameters") })
	@PostMapping("/saveAnalysisResult")
	public ResponseEntity<?> saveAnalysisResult(
			@RequestParam(value = "executionResultID", required = true) UUID executionResultID,
			@RequestBody AnalysisResultDTO analysisResultRequest) {
		LOGGER.info("Going to save analysis result");
		boolean saved = executionAnalysisService.saveAnalysisResult(executionResultID, analysisResultRequest);
		if (saved) {
			return ResponseEntity.ok("Analysis result saved successfully");
		} else {
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to save analysis result");
		}
	}

	/**
	 * Endpoint to get the analysis result for an execution result.
	 *
	 * @param executionResultID the UUID of the execution result
	 * @return ResponseEntity<?> containing the analysis result details
	 */
	@Operation(summary = "Get analysis result for an execution result")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Analysis result fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to get analysis result") })
	@GetMapping("/getAnalysisResult")
	public ResponseEntity<?> getAnalysisResult(@RequestParam UUID executionResultID) {
		LOGGER.info("Going to get analysis result");
		AnalysisResultDTO analysisResult = executionAnalysisService.getAnalysisResult(executionResultID);
		if (analysisResult != null) {
			return ResponseEntity.ok(analysisResult);
		} else {
			return ResponseEntity.status(HttpStatus.NO_CONTENT)
					.body("Analysis result for this execution result not available");
		}
	}

	/**
	 * Endpoint to get the module-wise analysis summary for an execution .
	 *
	 * @param executionID the UUID of the execution
	 * @return ResponseEntity<?> containing the module-wise analysis summary details
	 */
	@Operation(summary = "Get module-wise analysis summary for an execution")
	@ApiResponses(value = {
			@ApiResponse(responseCode = "200", description = "Module-wise analysis summary fetched successfully"),
			@ApiResponse(responseCode = "500", description = "Failed to get module-wise analysis summary"),
			@ApiResponse(responseCode = "201", description = "Module-wise analysis summary for this execution not available") })
	@GetMapping("/getModulewiseAnalysisSummary")
	public ResponseEntity<?> getModulewiseAnalysisSummary(@RequestParam UUID executionID) {
		LOGGER.info("Going to get module-wise analysis summary");
		Map<String, AnalysisIssueTypewiseSummaryDTO> analysisSummary = executionAnalysisService
				.getModulewiseAnalysisSummary(executionID);
		if (analysisSummary != null) {
			return ResponseEntity.ok(analysisSummary);
		} else {
			return ResponseEntity.status(HttpStatus.NO_CONTENT)
					.body("Module-wise analysis summary for this execution not available");
		}
	}

	/**
	 * Retrieves the ticket details from Jira for the specified execution script.
	 *
	 * @param executionResultID the unique identifier of the execution result
	 * @param projectName       the name of the project
	 * @return a ResponseEntity containing the ticket details if available, or a
	 *         message indicating no data is available
	 *
	 */
	@Operation(summary = "Get the ticket details from jira for the particular execution script")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Ticket details fetched successfully"),
			@ApiResponse(responseCode = "204", description = "Ticket details not available") })
	@GetMapping("/getTicketDetaisFromJira")
	public ResponseEntity<?> getTicketDetailsFromJira(@RequestParam UUID executionResultID,
			@RequestParam String projectName) {
		LOGGER.info("Going to get ticket details from Jira");
		List<TicketDetailsDTO> ticketDetails = executionAnalysisService.getTicketDetailsFromJira(executionResultID,
				projectName);
		if (ticketDetails != null && !ticketDetails.isEmpty()) {
			LOGGER.info("Ticket details fetched successfully");
			return ResponseEntity.status(HttpStatus.OK).body(ticketDetails);
		} else {
			LOGGER.error("Ticket details for this ticket not available");
			return ResponseEntity.status(HttpStatus.NO_CONTENT).body("No Jira data available");
		}
	}
}
