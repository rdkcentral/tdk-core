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

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.json.JSONObject;

import com.rdkm.tdkservice.dto.ExecutionDetailsResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionListResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionNameRequestDTO;
import com.rdkm.tdkservice.dto.ExecutionResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionResultResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionSummaryResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionTriggerDTO;

public interface IExecutionService {

	/**
	 * This method is used to trigger the execution of the scripts or test suite
	 * 
	 * @param executionTriggerDTO
	 * @return
	 */
	public ExecutionResponseDTO triggerExecution(ExecutionTriggerDTO executionTriggerDTO);

	/**
	 * This method is used to save the execution result
	 * 
	 * @param execId
	 * @param resultData
	 * @param execResult
	 * @param expectedResult
	 * @param resultStatus
	 * @param testCaseName
	 * @param execDevice
	 * 
	 * @return
	 */
	public boolean saveExecutionResult(String execId, String resultData, String execResult, String expectedResult,
			String resultStatus, String testCaseName, String execDevice);

	/**
	 * This method is used to trigger the execution of the scripts or test suite
	 * based on the input provided.
	 *
	 * @param execId     - the execution trigger DTO
	 * @param statusData - the execution trigger DTO
	 * @param execDevice - the execution trigger DTO
	 * @param execResult - the execution trigger DTO
	 * @return
	 */
	boolean saveLoadModuleStatus(String execId, String statusData, String execDevice, String execResult);

	/**
	 * This method is used to get client port
	 * 
	 * @param deviceIP
	 * @param port
	 * 
	 * @return
	 */
	JSONObject getClientPort(String deviceIP, String port);

	/**
	 * Get executions by category with the pagination applied
	 * 
	 * @param categoryName
	 * @param page
	 * @param size
	 * @param sortBy
	 * @param sortDir
	 * @return List of executions in required data format in DTO
	 */
	ExecutionListResponseDTO getExecutionsByCategory(String categoryName, int page, int size, String sortBy,
			String sortDir);

	/**
	 * This method is used to get the execution logs
	 * 
	 * @param executionResultID
	 * @return returns the execution logs
	 */
	String getExecutionLogs(String executionResultID);

	/**
	 * This method is used to get the execution name
	 * 
	 * @param devices - the list
	 * @return the execution name
	 */
	String getExecutionName(ExecutionNameRequestDTO executionNameRequestDTO);

	/**
	 * This method is used to get the execution details
	 * 
	 * @param id
	 * @return
	 */
	ExecutionDetailsResponseDTO getExecutionDetails(UUID id);

	/**
	 * This method is used to get the execution result
	 * 
	 * @param execResultId
	 * @return
	 */
	ExecutionResultResponseDTO getExecutionResult(UUID execResultId);

	/**
	 * This method is used to get the trend analysis
	 * 
	 * @param execResultId
	 * @return
	 */
	List<String> getTrendAnalysis(UUID execResultId);

	/**
	 * This method is used to trigger abort the execution
	 * 
	 * @param execResultId
	 * @return
	 */
	boolean abortExecution(UUID execId);

	/**
	 * This method is used to repeat the failed script
	 * 
	 * @param execId
	 * @return
	 */
	boolean repeatExecution(UUID execId, String user);

	/**
	 * This method is used to rerun the failed script
	 * 
	 * @param execId
	 * @return
	 */
	public boolean reRunFailedScript(UUID execId, String user);

	/*
	 * This method is used to delete the execution
	 * 
	 * @param id
	 * 
	 */
	public boolean deleteExecution(UUID id);

	/**
	 * This method is used to delete the list of executions
	 * 
	 * @param ids
	 * 
	 */
	public boolean deleteExecutions(List<UUID> ids);

	/**
	 * This method is to search executions based on test suite name and script name
	 * 
	 * @param scriptTestSuiteName - full script name or testsuite name or partial
	 *                            name for search query
	 * @param categoryName        - RDKV, RDKB, RDKC
	 * @param page                - the page number
	 * @param size                - size in page
	 * @param sortBy              - by default it is createdDate
	 * @param sortDir             - by default it is desc
	 */
	public ExecutionListResponseDTO getExecutionsByDeviceName(String deviceName, String categoryName, int page,
			int size, String sortBy, String sortDir);

	/**
	 * This method is used to get the executions by device name with pagination
	 * 
	 * @param deviceName   - the device name
	 * @param categoryName - RDKV, RDKB, RDKC
	 * @param page         - the page number
	 * @param size         - size in page
	 * @param sortBy       - by default it is date
	 * @param sortDir      - by default it is desc
	 * @return response DTO
	 */
	public ExecutionListResponseDTO getExecutionsByScriptTestsuite(String testSuiteName, String categoryName, int page,
			int size, String sortBy, String sortDir);
	/**
	 * This method is used to get the executions by executionName with
	 * pagination
	 * 
	 * @param executionName - executionName
	 * @param categoryName        - RDKV, RDKB, RDKC
	 * @param page                - the page number
	 * @param size                - size in page
	 * @param sortBy              - by default it is date
	 * @param sortDir             - by default it is desc
	 * @return response DTO
	 */
	public ExecutionListResponseDTO getExecutionsByExecutionName(String executionName, String categoryName, int page,
			int size, String sortBy, String sortDir);
	
	/**
	 * This method is used to get the executions by user with pagination
	 * 
	 * @param username     - the username
	 * @param categoryName - RDKV, RDKB, RDKC
	 * @param page         - the page number
	 * @param size         - size in page
	 * @param sortBy       - by default it is date
	 * @param sortDir      - by default it is desc
	 * @return response DTO
	 */
	public ExecutionListResponseDTO getExecutionsByUser(String username, String category, int page, int size,
			String sortBy, String sortDir);

	/**
	 * This method is used to get the unique users.
	 * 
	 * @return List of String - the list of unique users
	 */
	public List<String> getUniqueUsers();

	/**
	 * 
	 * This method is to get the module wise summary
	 * 
	 * @param executionId - the execution id
	 * @return the module wise summary
	 */
	Map<String, ExecutionSummaryResponseDTO> getModulewiseExecutionSummary(UUID executionId);

	/**
	 * This method is used to delete the executions by date range
	 * 
	 * @param fromDate
	 * @param toDate
	 * @return
	 */
	public int deleteExecutionsByDateRange(Instant fromDate, Instant toDate);
}
