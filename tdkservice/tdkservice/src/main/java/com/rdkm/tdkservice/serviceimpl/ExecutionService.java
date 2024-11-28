/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
package com.rdkm.tdkservice.serviceimpl;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import org.json.JSONException;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.rdkm.tdkservice.dto.ExecutionDetailsDTO;
import com.rdkm.tdkservice.dto.ExecutionResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionTriggerDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.enums.DeviceStatus;
import com.rdkm.tdkservice.enums.ExecutionMethodResultStatus;
import com.rdkm.tdkservice.enums.ExecutionOverallResultStatus;
import com.rdkm.tdkservice.enums.ExecutionResultStatus;
import com.rdkm.tdkservice.enums.ExecutionTriggerStatus;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.exception.UserInputException;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.model.DeviceType;
import com.rdkm.tdkservice.model.Execution;
import com.rdkm.tdkservice.model.ExecutionMethodResult;
import com.rdkm.tdkservice.model.ExecutionResult;
import com.rdkm.tdkservice.model.Script;
import com.rdkm.tdkservice.model.ScriptTestSuite;
import com.rdkm.tdkservice.model.TestSuite;
import com.rdkm.tdkservice.model.User;
import com.rdkm.tdkservice.repository.DeviceRepositroy;
import com.rdkm.tdkservice.repository.ExecutionMethodResultRepository;
import com.rdkm.tdkservice.repository.ExecutionRepository;
import com.rdkm.tdkservice.repository.ExecutionResultRepository;
import com.rdkm.tdkservice.repository.ScriptRepository;
import com.rdkm.tdkservice.repository.TestSuiteRepository;
import com.rdkm.tdkservice.repository.UserRepository;
import com.rdkm.tdkservice.service.IExecutionService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.Utils;

/*
 * The ExecutionService class is used to handle the execution related operations
 */

@Service
public class ExecutionService implements IExecutionService {

	private static final Logger LOGGER = LoggerFactory.getLogger(ExecutionService.class);

	@Autowired
	private DeviceRepositroy deviceRepository;

	@Autowired
	private ExecutionRepository executionRepository;

	@Autowired
	private ScriptRepository scriptRepository;

	@Autowired
	private ExecutionResultRepository executionResultRepository;

	@Autowired
	private ExecutionMethodResultRepository executionMethodResultRepository;

	@Autowired
	private ExecutionAsyncService executionAsyncService;

	@Autowired
	private TestSuiteRepository testSuiteRepository;

	@Autowired
	private UserRepository userRepository;

	@Autowired
	private DeviceStatusService deviceStatusService;

	/**
	 * This method is used to trigger the execution of the scripts or test suite
	 * based on the input provided.
	 *
	 * @param executionTriggerDTO - the execution trigger DTO
	 * @return ExecutionResponseDTO - the execution response
	 */
	@Override
	public ExecutionResponseDTO triggerExecution(ExecutionTriggerDTO executionTriggerDTO) {
		LOGGER.info("Triggering execution with details: {}", executionTriggerDTO);

		// Checks if the trigger request is valid
		this.checkValidTriggerRequest(executionTriggerDTO);

		// Prepare the response string
		StringBuilder responseLogs = new StringBuilder();

		// Get the devices from the request
		List<String> devicesFromRequest = executionTriggerDTO.getDeviceList();
		List<Device> deviceList = this.getValidDeviceList(devicesFromRequest, responseLogs);

		ExecutionResponseDTO response = null;

		ExecutionDetailsDTO executionDetailsDTO = null;
		List<String> scriptsListFromRequest = executionTriggerDTO.getScriptList();

		// Script Execution - Single and Multiple
		if (null != scriptsListFromRequest && !scriptsListFromRequest.isEmpty()) {
			LOGGER.info("The request came for  script execution");
			List<Script> scriptsList = this.getValidScriptList(scriptsListFromRequest, responseLogs);
			executionDetailsDTO = this.convertTriggerDTOToExecutionDetailsDTO(executionTriggerDTO, deviceList,
					scriptsList, null);
			if (scriptsList.size() > 1) {
				LOGGER.info("The request came for multiple script execution");
				response = multiScriptExcecution(executionDetailsDTO);
			} else if (scriptsList.size() == 1) {
				LOGGER.info("The request came for single script execution");
				response = singleScriptExecution(executionDetailsDTO);

			}
		}

		// Suite Execution
		if (!Utils.isEmpty(executionTriggerDTO.getTestSuite())) {
			LOGGER.info("The request came for Test Suite execution");
			String testSuiteName = executionTriggerDTO.getTestSuite();
			TestSuite testSuite = this.getValidTestSuite(testSuiteName, responseLogs);
			executionDetailsDTO = this.convertTriggerDTOToExecutionDetailsDTO(executionTriggerDTO, deviceList, null,
					testSuite);
			response = testSuiteExecution(executionDetailsDTO);
		}

		response = this.appendResponseLogs(response, responseLogs);

		return response;

	}

	/**
	 * This method is used to trigger the execution of a single script
	 * 
	 * @param executionDetailsDTO - the execution details DTO
	 * @return ExecutionResponseDTO - the execution response
	 */
	private ExecutionResponseDTO singleScriptExecution(ExecutionDetailsDTO executionDetailsDTO) {
		LOGGER.info("Executing single script: {}", executionDetailsDTO.getScriptList().get(0).getName());
		StringBuilder responseLogs = new StringBuilder();

		Script script = executionDetailsDTO.getScriptList().get(0);

		List<Device> deviceList = executionDetailsDTO.getDeviceList();
		List<Device> validDevices = getValidDevicesForScriptbasedOnCategory(deviceList, script, responseLogs);

		if (validDevices.isEmpty()) {
			responseLogs.append("No valid devices found for the script as categories are different: ")
					.append(script.getName()).append(". So not triggering execution").append("\n");
			ExecutionResponseDTO executionResponseDTO = createExecutionResponseDTO(responseLogs.toString(),
					ExecutionTriggerStatus.NOTTRIGGERED);
			return executionResponseDTO;
		}

		if (isScriptMarkedToBeSkipped(script)) {
			responseLogs.append("Script: ").append(script.getName())
					.append(" is marked to be skipped as it is obsolete. So execution is not triggered\n");
			ExecutionResponseDTO executionResponseDTO = createExecutionResponseDTO(responseLogs.toString(),
					ExecutionTriggerStatus.NOTTRIGGERED);
			return executionResponseDTO;
		}

		boolean isScriptExecutionTriggered = false;
		for (Device device : deviceList) {
			if (!validateScriptDeviceDeviceType(device, script)) {
				LOGGER.error("Device: {} and Script: {} combination is invalid\n", device.getName(), script.getName());
				responseLogs.append("Device: " + device.getName() + " and Script: " + script.getName()
						+ " combination is invalid due to different devicetypes, So not triggering execution in the device\n");
				continue;
			}

			if (!checkDeviceAvailabilityForExecution(device)) {
				LOGGER.error("Device: {} is not available for execution in it\n", device.getName());
				responseLogs.append("Device: " + device.getName() + " is not available for execution\n");
				continue;
			}

			isScriptExecutionTriggered = true;
			responseLogs.append("Executing script: ").append(script.getName()).append(" on device: ")
					.append(device.getName()).append(".");
			String executionName = getExecutionName(executionDetailsDTO.getExecutionName(), device,
					executionDetailsDTO.getTestType());
			LOGGER.info("Execution script on " + script.getName() + "the device" + device.getName());
			executionAsyncService.prepareAndExecuteSingleScript(device, script, executionDetailsDTO.getUser(),
					executionName, executionDetailsDTO.getCategory(), executionDetailsDTO.getRepeatCount(),
					executionDetailsDTO.isRerunOnFailure());
			LOGGER.info(" Asynchronous Execution of script on " + script.getName() + "the device" + device.getName()
					+ " triggered");

		}
		// If atleast one script execution is triggered in one box, then return the
		// response as triggered
		if (isScriptExecutionTriggered) {
			LOGGER.info("Script execution is triggered");
			ExecutionResponseDTO executionResponseDTO = this.createExecutionResponseDTO(responseLogs.toString(),
					ExecutionTriggerStatus.TRIGGERED);
			return executionResponseDTO;
		} else {
			LOGGER.info("Script execution is not triggered");
			ExecutionResponseDTO executionResponseDTO = this.createExecutionResponseDTO(responseLogs.toString(),
					ExecutionTriggerStatus.NOTTRIGGERED);
			return executionResponseDTO;
		}

	}

	/**
	 * This method is used to get the execution name based on the device and the
	 * execution name provided in the request
	 * 
	 * @param executionName - the execution name
	 * @param device        - the device
	 * @param testType      - the test type
	 * @return String - the execution name
	 */
	private String getExecutionName(String executionName, Device device, String testType) {
		String baseExecutionName = executionName;
		// TODO: Advanced use cases later - For CI API triggere, SOC , OEM etc
		if (!Utils.isEmpty(executionName)) {
			baseExecutionName = executionName + "_" + device.getName();
		} else {
			baseExecutionName = device.getName() + "_" + LocalDate.now();
		}
		return baseExecutionName;
	}

	/**
	 * This method is used to trigger the execution of multiple scripts
	 * 
	 * @param executionDetailsDTO - the execution details DTO
	 * @return ExecutionResponseDTO - the execution response
	 */
	private ExecutionResponseDTO multiScriptExcecution(ExecutionDetailsDTO executionDetailsDTO) {
		LOGGER.info("Starting multiScript excecution");

		StringBuilder responseLogs = new StringBuilder();
		boolean isExecutionTriggered = false;
		for (Device device : executionDetailsDTO.getDeviceList()) {

			if (!checkDeviceAvailabilityForExecution(device)) {
				LOGGER.error("Device: {} is not available for execution\n", device.getName());
				responseLogs.append("Device: " + device.getName()
						+ " is not available for execution, So not triggering excution in it\n");
				break;
			}
			String executionName = getExecutionName(executionDetailsDTO.getExecutionName(), device,
					executionDetailsDTO.getTestType());
			isExecutionTriggered = true;
			responseLogs.append("MultiScript execution on device triggered: ").append(device.getName())
					.append("triggered .\n");
			executionAsyncService.prepareAndExecuteMultiScript(device, executionDetailsDTO.getScriptList(),
					executionDetailsDTO.getUser(), executionName, executionDetailsDTO.getCategory(), null);
		}

		// If atleast one script execution is triggered in one box, then return the
		// response as triggered
		if (isExecutionTriggered) {
			LOGGER.info("Execution is triggered");
			ExecutionResponseDTO executionResponseDTO = this.createExecutionResponseDTO(responseLogs.toString(),
					ExecutionTriggerStatus.TRIGGERED);
			return executionResponseDTO;
		} else {
			LOGGER.info("Execution is  not triggered");
			ExecutionResponseDTO executionResponseDTO = this.createExecutionResponseDTO(responseLogs.toString(),
					ExecutionTriggerStatus.NOTTRIGGERED);
			return executionResponseDTO;
		}

	}

	private ExecutionResponseDTO testSuiteExecution(ExecutionDetailsDTO executionDetailsDTO) {
		LOGGER.info("Executing test suite: {}", executionDetailsDTO.getTestSuite().getName());
		// Get script list from Test suite
		TestSuite testSuite = executionDetailsDTO.getTestSuite();
		List<ScriptTestSuite> scriptList = testSuite.getScriptTestSuite();
		List<Script> scripts = new ArrayList<>();
		for (ScriptTestSuite scriptTestSuite : scriptList) {
			scripts.add(scriptTestSuite.getScript());
		}

		StringBuilder responseLogs = new StringBuilder();
		for (Device device : executionDetailsDTO.getDeviceList()) {
			String executionName = getExecutionName(executionDetailsDTO.getExecutionName(), device,
					executionDetailsDTO.getTestType());
			responseLogs.append("TestSuite execution on device: ").append(device.getName()).append(".");
			executionAsyncService.prepareAndExecuteMultiScript(device, scripts, executionDetailsDTO.getUser(),
					executionName, executionDetailsDTO.getCategory(), testSuite.getName());
		}

		ExecutionResponseDTO executionResponseDTO = this.createExecutionResponseDTO(responseLogs.toString(),
				ExecutionTriggerStatus.TRIGGERED);

		return executionResponseDTO;

	}

	/**
	 * This method is used to check if the device is available for execution
	 * 
	 * @param device - the device
	 * @return boolean - true if the device is available for execution, false
	 *         otherwise
	 */
	private boolean checkDeviceAvailabilityForExecution(Device device) {
		// Check if the device is available for execution
		// If the device is not available, then return false
		// If the device is available, then return true
		DeviceStatus deviceStatus = deviceStatusService.fetchDeviceStatus(device);
		if (DeviceStatus.FREE.equals(deviceStatus)) {
			return true;
		}
		return false;
	}

	/**
	 * This method is used to get the valid test suite, if the test suite is not
	 * found then it will append the response string with the test suite name not
	 * found and if no test suite found then it will throw ResourceNotFoundException
	 * 
	 * @param testSuiteName - the test suite name
	 * @param responseLogs  - the response logs
	 * @return TestSuite - the test suite
	 */
	private TestSuite getValidTestSuite(String testSuiteName, StringBuilder responseLogs) {
		TestSuite testSuite = null;
		if (!Utils.isEmpty(testSuiteName)) {
			testSuite = testSuiteRepository.findByName(testSuiteName);
			if (testSuite == null) {
				LOGGER.error("TestSuite not found with name: {}", testSuiteName);
				responseLogs.append("TestSuite: " + testSuiteName + " not found.");
				throw new ResourceNotFoundException("TestSuite", testSuiteName);
			}
		}
		return testSuite;

	}

	/**
	 * This method is used to append the response logs to the execution response DTO
	 * 
	 * @param response       - the execution response DTO
	 * @param responseString - the response string
	 * @return ExecutionResponseDTO - the execution response DTO
	 */

	private ExecutionResponseDTO appendResponseLogs(ExecutionResponseDTO response, StringBuilder responseLogs) {

		ExecutionResponseDTO executionResponseDTO = response;
		if (!Utils.isEmpty(responseLogs.toString())) {
			String executionResponseLog = executionResponseDTO.getMessage();
			String executionResponseAndOtherResponseLog = responseLogs + executionResponseLog;
			executionResponseDTO.setMessage(executionResponseAndOtherResponseLog);
		}
		return executionResponseDTO;

	}

	/**
	 * This method is used to create the execution response DTO
	 * 
	 * @param message                - the message
	 * @param executionTriggerStatus - the execution trigger status
	 * @return ExecutionResponseDTO - the execution response DTO
	 */

	private ExecutionResponseDTO createExecutionResponseDTO(String message,
			ExecutionTriggerStatus executionTriggerStatus) {
		ExecutionResponseDTO executionResponseDTO = new ExecutionResponseDTO();
		executionResponseDTO.setMessage(message);
		executionResponseDTO.setExecutionTriggerStatus(executionTriggerStatus);
		return executionResponseDTO;
	}

	/**
	 * This method is used to get the valid devices for the script based on the
	 * category
	 * 
	 * @param deviceList     - the device list
	 * @param script         - the script
	 * @param responseString - the response string
	 * @return List<Device> - the valid devices
	 */

	private boolean vaidateScriptDeviceCategory(Device device, Script script) {
		boolean isCategoryMatch = false;

		// TODO: Revisit this logic for RDKVRDKService
		if (device.isThunderEnabled()) {
			isCategoryMatch = script.getModule().getCategory().equals(Category.RDKV);
		} else {
			isCategoryMatch = script.getModule().getCategory().equals(device.getCategory());
		}
		return isCategoryMatch;
	}

	/**
	 * This method is used to get the valid devices for the script based on the
	 * category
	 * 
	 * @param deviceList     - the device list
	 * @param script         - the script
	 * @param responseString - the response string
	 * @return List<Device> - the valid devices
	 */
	private List<Device> getValidDevicesForScriptbasedOnCategory(List<Device> deviceList, Script script,
			StringBuilder responseString) {
		List<Device> validDevices = new ArrayList<>();
		for (Device device : deviceList) {
			if (vaidateScriptDeviceCategory(device, script)) {
				validDevices.add(device);
			} else {
				LOGGER.error("Device: {} and Script: {} combination is invalid and belongs to different category\n",
						device.getName(), script.getName());
			}
		}
		return validDevices;
	}

	/**
	 * This method is used to validate the script and device type
	 * 
	 * @param device - the device
	 * @param script - the script
	 * @return boolean - true if the script and device type is valid, false
	 *         otherwise
	 */

	private boolean validateScriptDeviceDeviceType(Device device, Script script) {
		List<DeviceType> deviceTypes = script.getDeviceTypes();
		if (deviceTypes.isEmpty()) {
			return true;
		} else {
			for (DeviceType deviceType : deviceTypes) {
				if (deviceType.equals(device.getDeviceType())) {
					return true;
				}
			}
		}
		return false;

	}

	/**
	 * This method is used to check if the script is marked to be skipped
	 * 
	 * @param script - the script
	 * @return boolean - true if the script is marked to be skipped, false otherwise
	 */

	private boolean isScriptMarkedToBeSkipped(Script script) {
		if (script.isSkipExecution()) {
			return true;
		}
		return false;
	}

	/**
	 * This method is used to convert the trigger DTO to execution details DTO
	 * 
	 * @param executionTriggerDTO - the execution trigger DTO
	 * @param deviceList          - the device list
	 * @param scriptList          - the script list
	 * @param testSuite           - the test suite
	 * @return ExecutionDetailsDTO - the execution details DTO
	 */

	private ExecutionDetailsDTO convertTriggerDTOToExecutionDetailsDTO(ExecutionTriggerDTO executionTriggerDTO,
			List<Device> deviceList, List<Script> scriptList, TestSuite testSuite) {

		ExecutionDetailsDTO executionDetailsDTO = new ExecutionDetailsDTO();
		executionDetailsDTO.setCategory(executionTriggerDTO.getCategory());
		executionDetailsDTO.setDeviceList(deviceList);
		executionDetailsDTO.setExecutionName(executionTriggerDTO.getExecutionName());
		executionDetailsDTO.setTestType(executionTriggerDTO.getTestType());
		executionDetailsDTO.setScriptList(scriptList);

		executionDetailsDTO.setTestSuite(testSuite);
		executionDetailsDTO.setRepeatCount(executionTriggerDTO.getRepeatCount());
		executionDetailsDTO.setRerunOnFailure(executionTriggerDTO.isRerunOnFailure());
		if (executionTriggerDTO.getUser() != null) {
			User user = userRepository.findByUsername(executionTriggerDTO.getUser());
			if (null != user) {
				executionDetailsDTO.setUser(user);
			}

		}
		return executionDetailsDTO;

	}

	/**
	 * This method is used to get the valid script list, if the script is not found
	 * then it will append the response string with the script name not found and if
	 * no scripts found then it will throw ResourceNotFoundException
	 * 
	 * @param scripts
	 * @return
	 */
	private List<Script> getValidScriptList(List<String> scripts, StringBuilder responseString) {
		List<Script> scriptList = new ArrayList<>();
		for (String scriptName : scripts) {
			Script script = scriptRepository.findByName(scriptName);
			// TODO : Check if file exists using a scriptService method
			if (script == null) {
				LOGGER.error("Script not found with name: {}", scriptName);
				responseString.append("Script: " + scriptName + " not found.)");
			} else {
				scriptList.add(script);
			}
		}
		if (scriptList.isEmpty()) {
			LOGGER.error("No valid/available scripts found in the request");
			throw new ResourceNotFoundException("Script/s in the request", scripts.toString());
		}
		return scriptList;

	}

	/**
	 * This method is used to get the valid device list, if the device is not found
	 * then it will append the response string with the device name not found and if
	 * no devices found then it will throw ResourceNotFoundException
	 * 
	 * @param devices        List of devices from the request
	 * @param responseString StringBuilder to append the response
	 * @return List of valid devices
	 */
	private List<Device> getValidDeviceList(List<String> devices, StringBuilder responseString) {
		List<Device> deviceList = new ArrayList<>();
		for (String deviceName : devices) {
			Device device = deviceRepository.findByName(deviceName);
			if (device == null) {
				LOGGER.error("Device not found with name: {}", deviceName);
				responseString.append("Device: " + deviceName + " not found.");
			} else {
				deviceList.add(device);
			}
		}
		if (deviceList.isEmpty()) {
			throw new ResourceNotFoundException("Device/s in the request", devices.toString());
		}
		return deviceList;
	}

	/**
	 * This method is used to check the request is Valid or not
	 * 
	 * @param executionTriggerDTO
	 * @return
	 */
	private void checkValidTriggerRequest(ExecutionTriggerDTO executionTriggerDTO) {
		// Checking for scripts or test suite is null or empty
		if ((executionTriggerDTO.getScriptList() == null || executionTriggerDTO.getScriptList().isEmpty())
				&& (executionTriggerDTO.getTestSuite() == null || executionTriggerDTO.getTestSuite().isEmpty())) {
			LOGGER.error("Either scripts or test suite must be provided in the request");
			throw new UserInputException("Either scripts or test suite must be provided in the request");
		}

		// Checking for devices
		if (!executionTriggerDTO.getDeviceList().isEmpty() && executionTriggerDTO.getDeviceList().size() > 0) {
		} else {
			LOGGER.error("No devices found in the request");
			throw new UserInputException("Devices not found in the request");
		}

		// Both script list and test suite cannot be non empty
		if (!executionTriggerDTO.getScriptList().isEmpty() && !Utils.isEmpty(executionTriggerDTO.getTestSuite())) {
			LOGGER.error("Both scripts and test suite cannot be provided in the  same request");
			throw new UserInputException("Both scripts and test suite cannot be provided in the  same request");
		}

		// Execution name provided should not be already available
		if (!Utils.isEmpty(executionTriggerDTO.getExecutionName())) {
			boolean isExecutionNameExists = executionRepository.existsByName(executionTriggerDTO.getExecutionName());
			if (isExecutionNameExists) {
				LOGGER.error("The Execution name already exists, execution name should be unique");
				throw new UserInputException("The Execution name already exists, execution name should be unique");
			}
		}
	}

	/**
	 * This method is used to save the execution result
	 * 
	 * @param execId         - the execution ID
	 * @param resultData     - the result data
	 * @param execResult     - the execution result
	 * @param expectedResult - the expected result
	 * @param resultStatus   - the result status
	 * @param testCaseName   - the test case name
	 * @param execDevice     - the execution device
	 * @return boolean - true if the execution result is saved, false otherwise
	 */
	@Override
	@Transactional
	public boolean saveExecutionResult(String execId, String resultData, String execResult, String expectedResult,
			String resultStatus, String testCaseName, String execDevice) {
		LOGGER.info(
				"Saving execution result for execId: {}, resultData: {}, execResultID: {}, expectedResult: {}, resultStatus: {}, testCaseName: {}, execDevice: {}",
				execId, resultData, execResult, expectedResult, resultStatus, testCaseName, execDevice);

		// Check if the execution ID is empty and throw an exception
		if (Utils.isEmpty(execId)) {
			LOGGER.error("Execution ID is empty");
			throw new UserInputException("Execution ID is empty");
		}

		// Check if the execution data exists and get the data from DB
		Execution execution = executionRepository.findById(UUID.fromString(execId)).orElseThrow(() -> {
			LOGGER.error("Execution not found with id: {}", execId);
			return new ResourceNotFoundException("Execution ID ", execId);
		});
		String executionResultID = execResult;

		if (!Utils.isEmpty(executionResultID)) {

			// Check if the executionResult ID is empty and throw an exception
			ExecutionResult executionResult = executionResultRepository.findById(UUID.fromString(executionResultID))
					.orElseThrow(() -> {
						LOGGER.error("Execution not found with id: {}", execResult);
						return new ResourceNotFoundException("Execution ID ", execResult);
					});

			// Save the execution method result or test case result
			ExecutionMethodResult executionMethodResult = new ExecutionMethodResult();
			String actualResult = resultData;
			if (resultStatus.equals(Constants.STATUS_NONE) || Utils.isEmpty(resultStatus)) {
				executionMethodResult.setMethodResult(ExecutionMethodResultStatus.valueOf(actualResult));
			} else {
				executionMethodResult.setExecutionResult(executionResult);
				executionMethodResult.setExpectedResult(ExecutionMethodResultStatus.valueOf(expectedResult));
				executionMethodResult.setActualResult(ExecutionMethodResultStatus.valueOf(actualResult));
				executionMethodResult.setMethodResult(ExecutionMethodResultStatus.valueOf(resultStatus));
			}
			executionMethodResult.setFunctionName(testCaseName);
			executionMethodResultRepository.save(executionMethodResult);

			// If the result in Execution and ExecutionResult is already failure from
			// anyone of the test case, then don't update the status. Because the status is
			// already failed
			if ((null == executionResult.getResult())
					|| (!executionResult.getResult().equals(ExecutionResultStatus.FAILURE))) {
				executionResult.setResult(ExecutionResultStatus.valueOf(resultStatus));
				executionResultRepository.save(executionResult);
				if ((null == execution.getResult())
						|| !(execution.getResult().equals(ExecutionOverallResultStatus.FAILURE))) {
					execution.setResult(ExecutionOverallResultStatus.valueOf(resultStatus));
					executionRepository.save(execution);
				}

				// TO DO: Status of the execution device need to decide
			}
			executionResultRepository.save(executionResult);

		} else {
			// If the executionResult ID is not passed and executionID is passed, mark the
			// status as failed

			execution.setResult(ExecutionOverallResultStatus.FAILURE);
			executionRepository.save(execution);

		}
		return true;

		// Convert execID to UUID

	}

	/**
	 * This method is used to trigger the execution of the scripts or test suite
	 * based on the input provided.
	 *
	 * @param execId     - the execution trigger DTO
	 * @param statusData - the execution trigger DTO
	 * @param execDevice - the execution trigger DTO
	 * @param execResult - the execution trigger DTO
	 */
	@Override
	@Transactional
	public void saveLoadModuleStatus(String execId, String statusData, String execDevice, String execResult) {
		Logger LOGGER = LoggerFactory.getLogger(ExecutionService.class);
		try {
			LOGGER.info("Finding execution with id: {}", execId);
			Execution execution = executionRepository.findById(UUID.fromString(execId))
					.orElseThrow(() -> new RuntimeException("Execution not found with id: " + execId));

			if (execution != null && !ExecutionOverallResultStatus.FAILURE.equals(execution.getResult())) {
				LOGGER.info("Updating execution result to: {}", statusData);
				execution.setResult(ExecutionOverallResultStatus.valueOf(statusData.toUpperCase().trim()));
				executionRepository.save(execution);
			}

			LOGGER.info("Finding execution result with id: {}", execResult);
			ExecutionResult executionResult = executionResultRepository.findById(UUID.fromString(execResult))
					.orElseThrow(() -> new RuntimeException("ExecutionResult not found with id: " + execResult));

			if (executionResult != null && !ExecutionResultStatus.FAILURE.equals(executionResult.getResult())) {
				LOGGER.info("Updating execution result to: {}", statusData);
				executionResult.setResult(ExecutionResultStatus.valueOf(statusData.toUpperCase().trim()));
				executionResultRepository.save(executionResult);
			}

//			if (execution != null && Result.FAILURE.equals(execution.getResult())) {
//				LOGGER.info("Execution result is FAILURE, retrieving all execution results");
//				List<ExecutionResult> allExecutionResults = executionResultRepository.findAllByExecution(execution);
//				List<ExecutionResult> naExecutionResults = executionResultRepository
//						.findAllByExecutionAndResult(execution, Result.NOT_APPLICABLE);
//				List<ExecutionResult> successExecutionResults = executionResultRepository
//						.findAllByExecutionAndResult(execution, Result.SUCCESS);
//				List<ExecutionResult> skippedExecutionResults = executionResultRepository
//						.findAllByExecutionAndResult(execution, Result.SKIPPED);
//
//				int totalScriptsCount = allExecutionResults.size();
//				int naScriptsCount = naExecutionResults.size();
//				int successScriptsCount = successExecutionResults.size();
//				int skippedScriptsCount = skippedExecutionResults.size();
//				int naAndSkippedAndSuccessSum = naScriptsCount + skippedScriptsCount + successScriptsCount;
//
//				LOGGER.info("Total scripts count: {}", totalScriptsCount);
//				LOGGER.info("NA scripts count: {}", naScriptsCount);
//				LOGGER.info("Success scripts count: {}", successScriptsCount);
//				LOGGER.info("Skipped scripts count: {}", skippedScriptsCount);
//				LOGGER.info("NA, Skipped, and Success sum: {}", naAndSkippedAndSuccessSum);
//
//				boolean setAsSuccess = false;
//				if (successScriptsCount > 0 && totalScriptsCount == naAndSkippedAndSuccessSum) {
//					setAsSuccess = true;
//				}
//
//				if (setAsSuccess) {
//					LOGGER.info("Setting execution result to SUCCESS");
//					execution.setResult(Result.SUCCESS);
//					executionRepository.save(execution);
//				}
//			}
		} catch (Exception e) {
			LOGGER.error("Exception occurred while saving load module status", e);
		}
	}

	/**
	 * This method is used to get the client port
	 * 
	 * @param deviceIP - the device IP
	 * @param port     - the port
	 * @return JSONObject - the client port
	 */
	@Override
	public JSONObject getClientPort(String deviceIP, String port) {
		JSONObject resultNode = new JSONObject();

		if (deviceIP != null && port != null) {
			// Assuming DeviceRepository is a Spring Data JPA repository
			Device device = deviceRepository.findByIpAndPort(deviceIP, port);

			if (device != null) {
				// Adding properties to the JsonObject
				try {
					resultNode.put("logTransferPort", device.getAgentMonitorPort());
					resultNode.put("statusPort", device.getStatusPort());
				} catch (JSONException e) {
					throw new RuntimeException(e);
				}
			}
		}

		// Return the JSON response
		return resultNode;
	}
}