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

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rdkm.tdkservice.config.AppConfig;
import com.rdkm.tdkservice.dto.AnalysisIssueTypewiseSummaryDTO;
import com.rdkm.tdkservice.dto.AnalysisResultDTO;
import com.rdkm.tdkservice.dto.IssueSearchRequestDTO;
import com.rdkm.tdkservice.dto.TicketDetailsDTO;
import com.rdkm.tdkservice.enums.AnalysisDefectType;
import com.rdkm.tdkservice.enums.ExecutionResultStatus;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.exception.TDKServiceException;
import com.rdkm.tdkservice.model.Execution;
import com.rdkm.tdkservice.model.ExecutionResult;
import com.rdkm.tdkservice.model.ExecutionResultAnalysis;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.repository.ExecutionRepository;
import com.rdkm.tdkservice.repository.ExecutionResultAnalysisRepository;
import com.rdkm.tdkservice.repository.ExecutionResultRepository;
import com.rdkm.tdkservice.service.IExecutionAnalysisService;
import com.rdkm.tdkservice.service.IScriptService;
import com.rdkm.tdkservice.service.utilservices.CommonService;
import com.rdkm.tdkservice.util.Constants;

/**
 * ExecutionAnalysisService is a service implementation class that provides
 * methods to fetch ticket details from Jira, save analysis results, and get
 * module-wise analysis status summary for execution results.
 * 
 */
@Service
public class ExecutionAnalysisService implements IExecutionAnalysisService {

	private static final Logger LOGGER = LoggerFactory.getLogger(ExecutionAnalysisService.class);

	@Autowired
	private ExecutionResultRepository executionResultRepository;

	@Autowired
	private ExecutionResultAnalysisRepository executionResultAnalysisRepository;

	@Autowired
	private ExecutionRepository executionRepository;

	@Autowired
	private HttpService httpService;

	@Autowired
	private IScriptService scriptService;

	@Autowired
	private CommonService commonService;

	/**
	 * Fetches ticket details from Jira based on the provided execution result ID
	 * and project name.
	 *
	 * @param executionResultID the unique identifier of the execution result
	 * @param projectName       the name of the project in Jira
	 * @return a list of TicketDetailsDTO containing the ticket details fetched from
	 *         Jira
	 * @throws ResourceNotFoundException if the execution result ID is not found in
	 *                                   the database
	 * @throws TDKServiceException       if there is an error while sending the POST
	 *                                   request to Jira or processing the response
	 */
	@Override
	public List<TicketDetailsDTO> getTicketDetailsFromJira(UUID executionResultID, String projectName) {
		LOGGER.info("Fetching ticket details from Jira for Execution Result Id: {}", executionResultID);
		ExecutionResult executionResult = executionResultRepository.findById(executionResultID).orElseThrow(() -> {
			LOGGER.error("Execution Result Id: {} not found in the database", executionResultID);
			return new ResourceNotFoundException("Execution Result Id", executionResultID.toString());
		});

		String scriptName = executionResult.getScript();
		String configFilePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
				+ Constants.ISSUE_ANALYSER_CONFIG;
		String baseUrl = commonService.getConfigProperty(new File(configFilePath), Constants.TICKET_HANDLER_URL);
		IssueSearchRequestDTO searchRequest = new IssueSearchRequestDTO();
		searchRequest.setSearchTitleOrDescription(scriptName);
		searchRequest.setProjectID(projectName);
		searchRequest.setIssueType(Constants.BUG_ISSUE_TYPE);

		ResponseEntity<String> response;
		try {
			response = httpService.sendPostRequest(baseUrl, searchRequest, null);
		} catch (Exception e) {
			LOGGER.error("Error occurred while sending POST request to {}: {}", baseUrl, e.getMessage());
			throw new TDKServiceException("Failed to fetch ticket details from Jira" + e.getMessage());
		}

		if (!response.getStatusCode().is2xxSuccessful()) {
			LOGGER.error("Failed to fetch ticket details from Jira, status code: {}", response.getStatusCode());
			throw new TDKServiceException(
					"Failed to fetch ticket details from Jira, status code: " + response.getStatusCode());
		}

		ObjectMapper objectMapper = new ObjectMapper();
		List<TicketDetailsDTO> ticketResponseList;
		try {
			ticketResponseList = objectMapper.readValue(response.getBody(),
					new TypeReference<List<TicketDetailsDTO>>() {
					});
		} catch (JsonMappingException e) {
			LOGGER.error("Error mapping JSON response to TicketDetailsDTO: {}", e.getMessage());
			throw new TDKServiceException("Error mapping JSON response to TicketDetailsDTO:" + e.getMessage());
		} catch (JsonProcessingException e) {
			LOGGER.error("Error processing JSON response: {}", e.getMessage());
			throw new TDKServiceException("Error processing JSON response:" + e.getMessage());
		}

		return ticketResponseList;
	}

	/**
	 * This method is used to save the analysis result
	 * 
	 * @param analysisResultRequest - the analysis result request DTO
	 * @return boolean - true if the analysis result is saved successfully
	 */
	@Override
	public boolean saveAnalysisResult(UUID executionResultID, AnalysisResultDTO analysisResultRequest) {
		LOGGER.info("Saving analysis result for execution result id: {}", executionResultID.toString());

		// Get the execution result based on the ID provided and save it after marking
		// the execution as analyzed
		ExecutionResult executionResult = executionResultRepository.findById(executionResultID).orElseThrow(
				() -> new ResourceNotFoundException("ExecutionResult with ID", executionResultID.toString()));

		// Save the ExecutionResultAnalysis based on the data given in DTO and save it
		ExecutionResultAnalysis executionResultAnalysis = new ExecutionResultAnalysis();
		executionResultAnalysis.setExecutionResult(executionResult);

		AnalysisDefectType defectType = AnalysisDefectType.valueOf(analysisResultRequest.getAnalysisDefectType());
		if (null != defectType) {
			executionResultAnalysis.setAnalysisDefectType(defectType);
		}
		executionResultAnalysis.setAnalysisUser(analysisResultRequest.getAnalysisUser());
		executionResultAnalysis.setAnalysisRemark(analysisResultRequest.getAnalysisRemark());
		executionResultAnalysis.setAnalysisTicketID(analysisResultRequest.getAnalysisTicketID());
		executionResultAnalysisRepository.save(executionResultAnalysis);

		LOGGER.info("Successfully saved analysis result for execution result id: {}", executionResultID.toString());
		return true;
	}

	/**
	 * 
	 * This method is to get the module wise anlysis status summary
	 * 
	 * @param executionId - the execution id
	 * @return the module wise anlysis status summary
	 */
	@Override
	public Map<String, AnalysisIssueTypewiseSummaryDTO> getModulewiseAnalysisSummary(UUID executionId) {
		LOGGER.info("Fetching analysis summary for id: {}", executionId);

		Execution execution = executionRepository.findById(executionId)
				.orElseThrow(() -> new ResourceNotFoundException("Execution with id", executionId.toString()));

		List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);
		if (executionResults.isEmpty()) {
			LOGGER.error("No execution results found for execution with id: {}", executionId);
			return null;
		}

		Map<String, AnalysisIssueTypewiseSummaryDTO> modulewiseAnalysisSummaryMap = new HashMap<>();

		for (ExecutionResult executionResult : executionResults) {
			if (executionResult.getResult() == ExecutionResultStatus.FAILURE) {

				// Get the module name of the script
				String scriptName = executionResult.getScript();
				Module module = scriptService.getModuleByScriptName(scriptName);
				String moduleName = module.getName();

				// If the module name is already there in the map , then the existing DTO is
				// updated
				// other wise a new DTO is created and added to the map
				AnalysisIssueTypewiseSummaryDTO analysisIssueTypewiseSummaryDTO = null;
				if (modulewiseAnalysisSummaryMap.containsKey(moduleName)) {
					analysisIssueTypewiseSummaryDTO = modulewiseAnalysisSummaryMap.get(moduleName);
				} else {
					analysisIssueTypewiseSummaryDTO = new AnalysisIssueTypewiseSummaryDTO();
				}

				// Get ExecutionResultAnalysis from the ExecutionResult
				ExecutionResultAnalysis executionResultAnalysis = executionResultAnalysisRepository
						.findByExecutionResult(executionResult);
				// Failure count is updated
				analysisIssueTypewiseSummaryDTO.setFailure(analysisIssueTypewiseSummaryDTO.getFailure() + 1);

				AnalysisDefectType analysisDefectType = null;
				if (null != executionResultAnalysis) {
					analysisIssueTypewiseSummaryDTO.setAnalysed(analysisIssueTypewiseSummaryDTO.getAnalysed() + 1);
					analysisDefectType = executionResultAnalysis.getAnalysisDefectType();
					if (null != analysisDefectType) {
						this.setAnalysisSummaryCount(analysisIssueTypewiseSummaryDTO, analysisDefectType);
					}
				}

				if (analysisIssueTypewiseSummaryDTO.getFailure() > 0) {
					analysisIssueTypewiseSummaryDTO.setNotAnalysed(analysisIssueTypewiseSummaryDTO.getFailure()
							- analysisIssueTypewiseSummaryDTO.getAnalysed());
				}

				modulewiseAnalysisSummaryMap.put(moduleName, analysisIssueTypewiseSummaryDTO);
			}
		}

		if (modulewiseAnalysisSummaryMap.isEmpty()) {
			LOGGER.error(
					"No module-wise analysis needed as there is no execution with failure status for the execution {}",
					executionId);
			return null;
		}

		try {
			// Update the analysis summary map with percentage
			this.updateAnalysisSummaryMapWithPercentageCount(modulewiseAnalysisSummaryMap);

			// Find the total analysis summary of all the failures in the execution
			this.updateTotalAnalysisSummary(modulewiseAnalysisSummaryMap);
		} catch (Exception e) {
			LOGGER.error("Error updating analysis summary map: {}", e.getMessage());
		}

		LOGGER.info("Successfully fetched analysis summary for id: {}", executionId);
		return modulewiseAnalysisSummaryMap;

	}

	/**
	 * This method is used to update the total analysis summary of all the failures
	 * in the execution
	 * 
	 * @param modulewiseAnalysisSummaryMap - map updated with total data
	 */
	private void updateTotalAnalysisSummary(Map<String, AnalysisIssueTypewiseSummaryDTO> modulewiseAnalysisSummaryMap) {
		AnalysisIssueTypewiseSummaryDTO totalAnalysisSummary = new AnalysisIssueTypewiseSummaryDTO();

		for (Map.Entry<String, AnalysisIssueTypewiseSummaryDTO> entry : modulewiseAnalysisSummaryMap.entrySet()) {
			AnalysisIssueTypewiseSummaryDTO analysisIssueTypewiseSummaryDTO = entry.getValue();
			totalAnalysisSummary
					.setFailure(totalAnalysisSummary.getFailure() + analysisIssueTypewiseSummaryDTO.getFailure());
			totalAnalysisSummary
					.setRdkIssue(totalAnalysisSummary.getRdkIssue() + analysisIssueTypewiseSummaryDTO.getRdkIssue());
			totalAnalysisSummary.setScriptIssue(
					totalAnalysisSummary.getScriptIssue() + analysisIssueTypewiseSummaryDTO.getScriptIssue());
			totalAnalysisSummary.setInterfaceChange(
					totalAnalysisSummary.getInterfaceChange() + analysisIssueTypewiseSummaryDTO.getInterfaceChange());
			totalAnalysisSummary
					.setEnvIssue(totalAnalysisSummary.getEnvIssue() + analysisIssueTypewiseSummaryDTO.getEnvIssue());
			totalAnalysisSummary.setOtherIssue(
					totalAnalysisSummary.getOtherIssue() + analysisIssueTypewiseSummaryDTO.getOtherIssue());
			totalAnalysisSummary
					.setAnalysed(totalAnalysisSummary.getAnalysed() + analysisIssueTypewiseSummaryDTO.getAnalysed());
			totalAnalysisSummary.setNotAnalysed(
					totalAnalysisSummary.getNotAnalysed() + analysisIssueTypewiseSummaryDTO.getNotAnalysed());
		}

		// Calculate the percentage based on Total analysed and Total Failure
		int totalAnalysed = totalAnalysisSummary.getEnvIssue() + totalAnalysisSummary.getInterfaceChange()
				+ totalAnalysisSummary.getOtherIssue() + totalAnalysisSummary.getRdkIssue()
				+ totalAnalysisSummary.getScriptIssue();
		int totalFailure = totalAnalysisSummary.getFailure();
		if (totalAnalysed > 0 && totalFailure > 0) {
			int percentage = (int) Math.round(((double) totalAnalysed / totalFailure) * 100);
			totalAnalysisSummary.setPercentageAnalysed(percentage);
		}

		modulewiseAnalysisSummaryMap.put(Constants.TOTAL_KEYWORD, totalAnalysisSummary);
	}

	/**
	 * This method is used to update the analysis summary map with the analysis
	 * percentage for each module
	 * 
	 * @param modulewiseAnalysisSummaryMap
	 */
	private void updateAnalysisSummaryMapWithPercentageCount(
			Map<String, AnalysisIssueTypewiseSummaryDTO> modulewiseAnalysisSummaryMap) {

		for (Map.Entry<String, AnalysisIssueTypewiseSummaryDTO> entry : modulewiseAnalysisSummaryMap.entrySet()) {
			String moduleName = entry.getKey();
			AnalysisIssueTypewiseSummaryDTO analysisIssueTypewiseSummaryDTO = entry.getValue();

			// Calculate total executions
			int totalAnalysed = analysisIssueTypewiseSummaryDTO.getAnalysed();
			int totalFailure = analysisIssueTypewiseSummaryDTO.getFailure();

			// Calculate the percentage based on Total analysed and Total Failure
			if (totalFailure > 0) {
				int percentage = (int) Math.round(((double) totalAnalysed / totalFailure) * 100);
				analysisIssueTypewiseSummaryDTO.setPercentageAnalysed(percentage);
			}

			// Update the map with the modified DTO
			modulewiseAnalysisSummaryMap.put(moduleName, analysisIssueTypewiseSummaryDTO);
		}
	}

	/**
	 * This method is used to get the analysis summary count based on different
	 * issue types
	 * 
	 * @param analysisIssueTypewiseSummaryDTO - the analysis issue type wise summary
	 * @param analysisDefectType              - Analysis Defect Type
	 */
	private void setAnalysisSummaryCount(AnalysisIssueTypewiseSummaryDTO analysisIssueTypewiseSummaryDTO,
			AnalysisDefectType analysisDefectType) {
		switch (analysisDefectType) {
		case RDK_ISSUE:
			analysisIssueTypewiseSummaryDTO.setRdkIssue(analysisIssueTypewiseSummaryDTO.getRdkIssue() + 1);
			break;
		case SCRIPT_ISSUE:
			analysisIssueTypewiseSummaryDTO.setScriptIssue(analysisIssueTypewiseSummaryDTO.getScriptIssue() + 1);
			break;
		case INTERFACE_CHANGE:
			analysisIssueTypewiseSummaryDTO
					.setInterfaceChange(analysisIssueTypewiseSummaryDTO.getInterfaceChange() + 1);
			break;
		case ENV_ISSUE:
			analysisIssueTypewiseSummaryDTO.setEnvIssue(analysisIssueTypewiseSummaryDTO.getEnvIssue() + 1);
			break;
		case OTHER_ISSUE:
			analysisIssueTypewiseSummaryDTO.setOtherIssue(analysisIssueTypewiseSummaryDTO.getOtherIssue() + 1);
			break;
		default:
			break;

		}

	}

	/**
	 * This method is used to get the analysis summary for the given execution ID.
	 * 
	 * @param executionResultID - the unique identifier of the execution result
	 * @return the analysis summary
	 */
	@Override
	public AnalysisResultDTO getAnalysisResult(UUID executionResultID) {
		LOGGER.info("Fetching analysis result for execution result id: {}", executionResultID.toString());
		ExecutionResult executionResult = executionResultRepository.findById(executionResultID).orElseThrow(
				() -> new ResourceNotFoundException("ExecutionResult with ID", executionResultID.toString()));
		ExecutionResultAnalysis executionResultAnalysis = executionResultAnalysisRepository
				.findByExecutionResult(executionResult);
		if (null == executionResultAnalysis) {
			LOGGER.error("Analysis result not found for execution result id: {}", executionResultID);
			return null;
		}
		AnalysisResultDTO analysisResultDTO = new AnalysisResultDTO();
		analysisResultDTO.setAnalysisDefectType(executionResultAnalysis.getAnalysisDefectType().name());
		analysisResultDTO.setAnalysisRemark(executionResultAnalysis.getAnalysisRemark());
		analysisResultDTO.setAnalysisTicketID(executionResultAnalysis.getAnalysisTicketID());
		analysisResultDTO.setAnalysisUser(executionResultAnalysis.getAnalysisUser());
		LOGGER.info("Successfully fetched analysis result for execution result id: {}", executionResultID.toString());

		return analysisResultDTO;
	}

}
