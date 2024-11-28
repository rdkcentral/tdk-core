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

import org.json.JSONObject;
import org.springframework.http.ResponseEntity;

import com.rdkm.tdkservice.dto.ExecutionResponseDTO;
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
	 */
	void saveLoadModuleStatus(String execId, String statusData, String execDevice, String execResult);

	/**
	 * This method is used to get client port
	 * 
	 * @param deviceIP
	 * @param port
	 * 
	 * @return
	 */
	JSONObject getClientPort(String deviceIP, String port);
}
