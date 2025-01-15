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
package com.rdkm.tdkservice.service;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import com.rdkm.tdkservice.dto.AnalysisIssueTypewiseSummaryDTO;
import com.rdkm.tdkservice.dto.AnalysisResultDTO;
import com.rdkm.tdkservice.dto.TicketDetailsDTO;

public interface IExecutionAnalysisService {

	/**
	 * This method is used to save the analysis result
	 * 
	 * @param analysisResultRequest - the analysis result request DTO
	 * @return boolean - true if the analysis result is saved successfully
	 */
	boolean saveAnalysisResult(UUID executionResultID, AnalysisResultDTO analysisResultRequest);

	/**
	 * This method is used to get the analysis summary for the given execution ID.
	 * 
	 * @param executionResultID - the unique identifier of the execution result
	 * @return the analysis summary
	 */
	AnalysisResultDTO getAnalysisResult(UUID executionResultID);

	/**
	 * 
	 * This method is to get the module wise anlysis status summary
	 * 
	 * @param executionId - the execution id
	 * @return the module wise anlysis status summary
	 */
	Map<String, AnalysisIssueTypewiseSummaryDTO> getModulewiseAnalysisSummary(UUID executionId);

	/**
	 * Retrieves ticket details from Jira based on the provided execution result ID
	 * and project name.
	 *
	 * @param executionResultID the unique identifier of the execution result
	 * @param projectName       the name of the project in Jira
	 * @return a list of TicketDetailsDTO objects containing the details of the
	 *         tickets
	 */
	List<TicketDetailsDTO> getTicketDetailsFromJira(UUID executionResultID, String projectName);
}
