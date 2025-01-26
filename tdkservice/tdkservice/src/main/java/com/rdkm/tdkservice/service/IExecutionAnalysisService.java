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
import com.rdkm.tdkservice.dto.JiraDescriptionDTO;
import com.rdkm.tdkservice.dto.TicketCreateDTO;
import com.rdkm.tdkservice.dto.TicketDetailsDTO;
import com.rdkm.tdkservice.dto.TicketUpdateDTO;

/**
 * Interface for execution analysis services. Provides methods to save analysis
 * results, retrieve analysis summaries, and interact with Jira for ticket
 * details and operations.
 */
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

	/**
	 * Retrieves details for populating ticket details in Jira.
	 *
	 * @param execResultID the unique identifier of the execution result
	 * @return the Jira description DTO
	 */
	JiraDescriptionDTO getDetailsForPopulatingTicketDetails(UUID execResultID);

	/**
	 * Retrieves a list of project IDs.
	 *
	 * @return a list of project IDs
	 */
	List<String> getListOfProjectIDs();

	/**
	 * Checks if the given project ID is a platform project ID.
	 *
	 * @param projectID the project ID to check
	 * @return true if the project ID is a platform project ID
	 */
	boolean isPlatformProjectID(String projectID);

	/**
	 * Retrieves a list of labels.
	 *
	 * @return a list of labels
	 */
	List<String> getListOfLabels();

	/**
	 * Retrieves a list of release versions.
	 *
	 * @return a list of release versions
	 */
	List<String> getReleaseVersions();

	/**
	 * Retrieves a list of hardware configurations.
	 *
	 * @return a list of hardware configurations
	 */
	List<String> getHardwareConfiguration();

	/**
	 * Retrieves a list of impacted platforms.
	 *
	 * @return a list of impacted platforms
	 */
	List<String> getImpactedPlatforms();

	/**
	 * Retrieves a list of severities.
	 *
	 * @return a list of severities
	 */
	List<String> getSeverities();

	/**
	 * Retrieves a list of versions in which issues are fixed.
	 *
	 * @return a list of fixed-in versions
	 */
	List<String> getFixedInVersions();

	/**
	 * Retrieves a list of impacted components.
	 *
	 * @return a list of impacted components
	 */
	List<String> getComponentsImpacted();

	/**
	 * Retrieves a list of defect types.
	 *
	 * @return a list of defect types
	 */
	List<String> getDefectTypes();

	/**
	 * Retrieves the steps to reproduce an issue based on the script name.
	 *
	 * @param scriptName the name of the script
	 * @return the steps to reproduce the issue
	 */
	String getStepsToReproduce(String scriptName);

	/**
	 * Retrieves a list of priorities.
	 *
	 * @return a list of priorities
	 */
	List<String> getPriorities();

	/**
	 * Creates a Jira ticket based on the provided ticket creation DTO.
	 *
	 * @param ticketCreateDTO the ticket creation DTO
	 * @return the ID of the created Jira ticket
	 */
	String createJiraTicket(TicketCreateDTO ticketCreateDTO);

	/**
	 * Updates a Jira ticket based on the provided ticket update DTO.
	 *
	 * @param ticketUpdateDTO the ticket update DTO
	 * @return the ID of the updated Jira ticket
	 */
	String updateJiraTicket(TicketUpdateDTO ticketUpdateDTO);

	/**
	 * Checks if Jira automation is implemented.
	 *
	 * @return true if Jira automation is implemented
	 */
	boolean isJiraAutomationImplemented();
	
	/**
	 * This method is used to get the analysis defect types.
	 *
	 * @return the list of analysis defect types
	 */
	List<String> getAnalysisDefectTypes();
}
