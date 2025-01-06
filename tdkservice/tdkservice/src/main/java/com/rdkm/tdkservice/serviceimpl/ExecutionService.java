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
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
package com.rdkm.tdkservice.serviceimpl;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import org.apache.tomcat.util.http.fileupload.FileUtils;
import org.json.JSONException;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.rdkm.tdkservice.dto.ExecutionDetailsDTO;
import com.rdkm.tdkservice.dto.ExecutionDetailsResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionListDTO;
import com.rdkm.tdkservice.dto.ExecutionListResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionMethodResultResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionNameRequestDTO;
import com.rdkm.tdkservice.dto.ExecutionResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionResultDTO;
import com.rdkm.tdkservice.dto.ExecutionResultResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionSummaryResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionTriggerDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.enums.DeviceStatus;
import com.rdkm.tdkservice.enums.ExecutionMethodResultStatus;
import com.rdkm.tdkservice.enums.ExecutionOverallResultStatus;
import com.rdkm.tdkservice.enums.ExecutionProgressStatus;
import com.rdkm.tdkservice.enums.ExecutionResultStatus;
import com.rdkm.tdkservice.enums.ExecutionStatus;
import com.rdkm.tdkservice.enums.ExecutionTriggerStatus;
import com.rdkm.tdkservice.enums.ExecutionType;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.exception.TDKServiceException;
import com.rdkm.tdkservice.exception.UserInputException;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.model.DeviceType;
import com.rdkm.tdkservice.model.Execution;
import com.rdkm.tdkservice.model.ExecutionDevice;
import com.rdkm.tdkservice.model.ExecutionMethodResult;
import com.rdkm.tdkservice.model.ExecutionResult;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.model.Oem;
import com.rdkm.tdkservice.model.Script;
import com.rdkm.tdkservice.model.ScriptTestSuite;
import com.rdkm.tdkservice.model.Soc;
import com.rdkm.tdkservice.model.TestSuite;
import com.rdkm.tdkservice.model.User;
import com.rdkm.tdkservice.repository.DeviceRepositroy;
import com.rdkm.tdkservice.repository.ExecutionDeviceRepository;
import com.rdkm.tdkservice.repository.ExecutionMethodResultRepository;
import com.rdkm.tdkservice.repository.ExecutionRepository;
import com.rdkm.tdkservice.repository.ExecutionResultRepository;
import com.rdkm.tdkservice.repository.ScriptRepository;
import com.rdkm.tdkservice.repository.TestSuiteRepository;
import com.rdkm.tdkservice.repository.UserRepository;
import com.rdkm.tdkservice.service.IExecutionService;
import com.rdkm.tdkservice.service.IScriptService;
import com.rdkm.tdkservice.service.utilservices.CommonService;
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
	private CommonService commonService;

	@Autowired
	private DeviceStatusService deviceStatusService;

	@Autowired
	private ExecutionDeviceRepository executionDeviceRepository;

	@Autowired
	private FileTransferService fileTransferService;

	@Autowired
	private IScriptService scriptService;

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
		ExecutionResponseDTO response = this.startExecution(executionTriggerDTO);
		return response;
	}

	/**
	 * The execution part with out the validation to be used in scheduler as well as
	 * in triggered execution
	 * 
	 * @param executionTriggerDTO
	 * @return ExecutionResponseDTO
	 */
	public ExecutionResponseDTO startExecution(ExecutionTriggerDTO executionTriggerDTO) {
		// Prepare the response string
		StringBuilder responseLogs = new StringBuilder();

		// Get the devices from the request
		List<String> devicesFromRequest = executionTriggerDTO.getDeviceList();
		List<Device> deviceList = this.getValidDeviceList(devicesFromRequest, responseLogs);

		ExecutionResponseDTO response = null;

		ExecutionDetailsDTO executionDetailsDTO = null;
		List<String> scriptsListFromRequest = executionTriggerDTO.getScriptList();
		List<String> testSuiteListFromRequest = executionTriggerDTO.getTestSuite();

		// Check if the devices are available for execution
		List<Device> freeDevices = this.filterFreeDevices(deviceList, responseLogs);
		if (freeDevices.isEmpty()) {
			LOGGER.error("No valid devices found for execution");
			ExecutionResponseDTO executionResponseDTO = createExecutionResponseDTO(responseLogs.toString(),
					ExecutionTriggerStatus.NOTTRIGGERED);
			return executionResponseDTO;
		}

		// Script Execution - Single and Multiple
		if (null != scriptsListFromRequest && !scriptsListFromRequest.isEmpty()) {
			LOGGER.info("The request came for  script execution");
			List<Script> scriptsList = this.getValidScriptList(scriptsListFromRequest, responseLogs);
			executionDetailsDTO = this.convertTriggerDTOToExecutionDetailsDTO(executionTriggerDTO, freeDevices,
					scriptsList, null);
			if (scriptsList.size() > 1) {
				LOGGER.info("The request came for multiple script execution");
				response = multiScriptExcecution(executionDetailsDTO);
			} else if (scriptsList.size() == 1) {
				LOGGER.info("The request came for single script execution");
				response = singleScriptExecution(executionDetailsDTO);
			}
		}

		// Test suite Execution - Single and Multiple
		if (null != testSuiteListFromRequest && !testSuiteListFromRequest.isEmpty()) {
			LOGGER.info("The request came for  Test suite execution");
			List<TestSuite> testSuiteList = this.getValidTestSuiteList(testSuiteListFromRequest, responseLogs);
			executionDetailsDTO = this.convertTriggerDTOToExecutionDetailsDTO(executionTriggerDTO, deviceList, null,
					testSuiteList);
			if (testSuiteList.size() > 1) {
				LOGGER.info("The request came for multi testsuite execution");
				response = multiTestSuiteExecution(executionDetailsDTO);
			} else if (testSuiteList.size() == 1) {
				LOGGER.info("The request came for single testsuite execution");
				response = testSuiteExecution(executionDetailsDTO);

			}

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
					executionName, executionDetailsDTO.getRepeatCount(), executionDetailsDTO.isRerunOnFailure(),
					executionDetailsDTO.isDeviceLogsNeeded(), executionDetailsDTO.isPerformanceLogsNeeded(),
					executionDetailsDTO.isDiagnosticLogsNeeded());
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
		if (!Utils.isEmpty(executionName) && !executionName.contains(Constants.MULTIPLE_KEY_WORD)) {
			baseExecutionName = executionName;
		} else {
			baseExecutionName = this.getExecutionNameFromDeviceAndTestType(device, testType);
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
					executionDetailsDTO.getUser(), executionName, executionDetailsDTO.getCategory(), null,
					executionDetailsDTO.getRepeatCount(), executionDetailsDTO.isRerunOnFailure(),
					executionDetailsDTO.isDeviceLogsNeeded(), executionDetailsDTO.isDiagnosticLogsNeeded(),
					executionDetailsDTO.isPerformanceLogsNeeded());
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

	/**
	 * Executes the test suite based on the provided execution details.
	 *
	 * @param executionDetailsDTO the details of the execution including test suite,
	 *                            devices, user, etc.
	 * @return ExecutionResponseDTO containing the response logs and execution
	 *         status.
	 *
	 *         This method performs the following steps: 1. Logs the start of the
	 *         test suite execution. 2. Retrieves the list of scripts from the test
	 *         suite. 3. Iterates over each device in the execution details: a.
	 *         Checks if the device is available for execution. b. If the device is
	 *         not available, logs an error and appends a message to the response
	 *         logs. c. If the device is available, prepares and executes the
	 *         scripts asynchronously on the device. 4. Creates and returns an
	 *         ExecutionResponseDTO with the accumulated response logs and a
	 *         triggered status.
	 */
	private ExecutionResponseDTO testSuiteExecution(ExecutionDetailsDTO executionDetailsDTO) {
		LOGGER.info("Executing test suite: {}", executionDetailsDTO.getTestSuite().get(0).getName());
		// Get script list from Test suite
		TestSuite testSuite = executionDetailsDTO.getTestSuite().get(0);
		List<ScriptTestSuite> scriptList = testSuite.getScriptTestSuite();
		List<Script> scripts = new ArrayList<>();
		for (ScriptTestSuite scriptTestSuite : scriptList) {
			scripts.add(scriptTestSuite.getScript());
		}

		StringBuilder responseLogs = new StringBuilder();
		for (Device device : executionDetailsDTO.getDeviceList()) {
			if (!checkDeviceAvailabilityForExecution(device)) {
				LOGGER.error("Device: {} is not available for execution\n", device.getName());
				responseLogs.append("Device: " + device.getName()
						+ " is not available for execution, So not triggering excution in it\n");
				continue;
			}
			String executionName = getExecutionName(executionDetailsDTO.getExecutionName(), device,
					executionDetailsDTO.getTestType());
			responseLogs.append("TestSuite execution on device: ").append(device.getName()).append(".");
			executionAsyncService.prepareAndExecuteMultiScript(device, scripts, executionDetailsDTO.getUser(),
					executionName, executionDetailsDTO.getCategory(), testSuite.getName(),
					executionDetailsDTO.getRepeatCount(), executionDetailsDTO.isRerunOnFailure(),
					executionDetailsDTO.isDeviceLogsNeeded(), executionDetailsDTO.isDiagnosticLogsNeeded(),
					executionDetailsDTO.isDiagnosticLogsNeeded());

		}
		ExecutionResponseDTO executionResponseDTO = this.createExecutionResponseDTO(responseLogs.toString(),
				ExecutionTriggerStatus.TRIGGERED);

		return executionResponseDTO;

	}

	/**
	 * Executes multiple test suites on the provided devices.
	 * 
	 * @param executionDetailsDTO the details of the execution, including test
	 *                            suites, devices, user, and other parameters.
	 * @return an ExecutionResponseDTO containing the response logs and the status
	 *         of the execution trigger.
	 */
	private ExecutionResponseDTO multiTestSuiteExecution(ExecutionDetailsDTO executionDetailsDTO) {
		LOGGER.info("Starting multiTestSuite excecution");
		List<TestSuite> testSuiteList = executionDetailsDTO.getTestSuite();
		StringBuilder responseLogs = new StringBuilder();
		Set<Script> scriptSet = new HashSet<>();
		List<ScriptTestSuite> scriptList = new ArrayList<>();
		for (TestSuite testSuite : testSuiteList) {
			scriptList.addAll(testSuite.getScriptTestSuite());
		}
		for (ScriptTestSuite scriptTestSuite : scriptList) {
			scriptSet.add(scriptTestSuite.getScript());
		}
		List<Script> scripts = new ArrayList<>(scriptSet);

		for (Device device : executionDetailsDTO.getDeviceList()) {
			if (!checkDeviceAvailabilityForExecution(device)) {
				LOGGER.error("Device: {} is not available for execution\n", device.getName());
				responseLogs.append("Device: " + device.getName()
						+ " is not available for execution, So not triggering excution in it\n");
				break;
			}
			String executionName = getExecutionName(executionDetailsDTO.getExecutionName(), device,
					executionDetailsDTO.getTestType());
			responseLogs.append("Multitestsuite execution on device: ").append(device.getName()).append(".");
			executionAsyncService.prepareAndExecuteMultiScript(device, scripts, executionDetailsDTO.getUser(),
					executionName, executionDetailsDTO.getCategory(), Constants.MULTI_TEST_SUITE,
					executionDetailsDTO.getRepeatCount(), executionDetailsDTO.isRerunOnFailure(),
					executionDetailsDTO.isDeviceLogsNeeded(), executionDetailsDTO.isDiagnosticLogsNeeded(),
					executionDetailsDTO.isPerformanceLogsNeeded());
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
	private List<Device> getValidDevicesForScriptbasedOnCategory(List<Device> deviceList, Script script,
			StringBuilder responseString) {
		LOGGER.info("Getting valid devices for script based on category");
		List<Device> validDevices = new ArrayList<>();
		for (Device device : deviceList) {
			if (commonService.vaidateScriptDeviceCategory(device, script)) {
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
		LOGGER.info("Validating script and device type");
		List<DeviceType> deviceTypes = script.getDeviceTypes();
		if (deviceTypes.isEmpty()) {
			LOGGER.info("Script has no device types");
			return true;
		} else {
			for (DeviceType deviceType : deviceTypes) {
				if (deviceType.equals(device.getDeviceType())) {
					LOGGER.info("Device: {} and Script: {} combination is valid\n", device.getName(), script.getName());
					return true;
				}
			}
		}
		LOGGER.error("Device: {} and Script: {} combination is invalid and belongs to different devicetypes\n",
				device.getName(), script.getName());
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
			LOGGER.info("Script: {} is marked to be skipped\n", script.getName());
			return true;
		}
		LOGGER.info("Script: {} is not marked to be skipped\n", script.getName());
		return false;
	}

	/**
	 * Retrieves a list of valid scripts based on the provided script names.
	 * 
	 * @param scripts        A list of script names to be validated and retrieved.
	 * @param responseString A StringBuilder to append error messages if scripts are
	 *                       not found.
	 * @return A list of valid Script objects.
	 * @throws ResourceNotFoundException if no valid scripts are found in the
	 *                                   request.
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
	 * This method is used to convert the trigger DTO to execution details DTO
	 * 
	 * @param executionTriggerDTO - the execution trigger DTO
	 * @param deviceList          - the device list
	 * @param scriptList          - the script list
	 * @param testSuite           - the test suite
	 * @return ExecutionDetailsDTO - the execution details DTO
	 */
	private ExecutionDetailsDTO convertTriggerDTOToExecutionDetailsDTO(ExecutionTriggerDTO executionTriggerDTO,
			List<Device> deviceList, List<Script> scriptList, List<TestSuite> testSuite) {
		LOGGER.debug("Converting ExecutionTriggerDTO to ExecutionDetailsDTO");
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
		executionDetailsDTO.setDeviceLogsNeeded(executionTriggerDTO.isDeviceLogsNeeded());
		executionDetailsDTO.setPerformanceLogsNeeded(executionTriggerDTO.isPerformanceLogsNeeded());
		executionDetailsDTO.setDiagnosticLogsNeeded(executionTriggerDTO.isDiagnosticLogsNeeded());
		LOGGER.debug("Converted ExecutionTriggerDTO to ExecutionDetailsDTO");
		return executionDetailsDTO;

	}

	/**
	 * Retrieves a list of valid TestSuite objects based on the provided list of
	 * test suite names.
	 * 
	 * @param testSuiteListFromRequest A list of test suite names to be validated
	 *                                 and retrieved.
	 * @param responseLogs             A StringBuilder object to append logs for any
	 *                                 test suites that are not found.
	 * @return A list of valid TestSuite objects.
	 * @throws ResourceNotFoundException If no valid test suites are found in the
	 *                                   provided list.
	 */
	private List<TestSuite> getValidTestSuiteList(List<String> testSuiteListFromRequest, StringBuilder responseLogs) {
		LOGGER.info("Getting valid test suites from the request");
		List<TestSuite> testSuiteList = new ArrayList<>();
		for (String testSuiteName : testSuiteListFromRequest) {
			TestSuite testSuite = testSuiteRepository.findByName(testSuiteName);
			if (testSuite == null) {
				LOGGER.error("TestSuite not found with name: {}", testSuiteName);
				responseLogs.append("TestSuite: " + testSuiteName + " not found.");
			} else {
				testSuiteList.add(testSuite);
			}
		}
		if (testSuiteList.isEmpty()) {
			LOGGER.error("No valid/available Test Suites found in the request");
			throw new ResourceNotFoundException("Test Suites in the request", testSuiteListFromRequest.toString());
		}
		return testSuiteList;
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
		LOGGER.info("Getting valid devices from the request");
		List<Device> deviceList = new ArrayList<>();
		for (String deviceName : devices) {
			Device device = deviceRepository.findByName(deviceName);
			if (device == null) {
				LOGGER.error("Device not found with name: {}", deviceName);
				responseString.append("Device: " + deviceName + " not found.\n");
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
	 * This method is used to get the execution name based on the device
	 * 
	 * @param deviceList - the device list
	 * @return String - the execution name
	 */
	private List<Device> filterFreeDevices(List<Device> deviceList, StringBuilder responseString) {
		LOGGER.info("Filtering devices based on the availability");
		List<Device> availableDevices = new ArrayList<>();
		for (Device device : deviceList) {
			if (device.getDeviceStatus().equals(DeviceStatus.FREE)) {
				availableDevices.add(device);
			} else {
				responseString.append("Device: " + device.getName() + " is not available for execution\n");
			}
		}
		if (availableDevices.isEmpty()) {
			LOGGER.error("Device not available for execution");
			responseString.append("No devices available for execution\n");
			throw new ResourceNotFoundException("Device not available for execution", "");
		}
		return availableDevices;
	}

	/**
	 * Validates the execution trigger request.
	 *
	 * This method performs the following validations: 1. Ensures that either
	 * scripts or test suite is provided in the request. 2. Checks if the device
	 * list is not empty. 3. Ensures that both script list and test suite are not
	 * provided simultaneously. 4. Verifies that the execution name, if provided, is
	 * unique.
	 *
	 * @param executionTriggerDTO the execution trigger request data transfer object
	 * @throws UserInputException if any validation fails with appropriate error
	 *                            message
	 */
	public void checkValidTriggerRequest(ExecutionTriggerDTO executionTriggerDTO) {
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
		if (!executionTriggerDTO.getScriptList().isEmpty() && !executionTriggerDTO.getTestSuite().isEmpty()) {
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

			}
			executionResultRepository.save(executionResult);

		} else {
			// If the executionResult ID is not passed and executionID is passed, mark the
			// status as failed

			execution.setResult(ExecutionOverallResultStatus.FAILURE);
			executionRepository.save(execution);

		}
		return true;
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
	public boolean saveLoadModuleStatus(String execId, String statusData, String execDevice, String execResult) {
		Logger LOGGER = LoggerFactory.getLogger(ExecutionService.class);
		LOGGER.info("Finding execution with id: {}", execId);
		Execution execution = executionRepository.findById(UUID.fromString(execId))
				.orElseThrow(() -> new ResourceNotFoundException("Execution ID", execId));

		if (execution != null && !ExecutionOverallResultStatus.FAILURE.equals(execution.getResult())) {
			LOGGER.info("Updating execution result to: {}", statusData);
			execution.setResult(ExecutionOverallResultStatus.valueOf(statusData.toUpperCase().trim()));
			executionRepository.save(execution);
		}

		LOGGER.info("Finding execution result with id: {}", execResult);
		ExecutionResult executionResult = executionResultRepository.findById(UUID.fromString(execResult))
				.orElseThrow(() -> new ResourceNotFoundException("ExecutionResult  ID", execResult));

		if (executionResult != null && !ExecutionResultStatus.FAILURE.equals(executionResult.getResult())) {
			LOGGER.info("Updating execution result to: {}", statusData);
			executionResult.setResult(ExecutionResultStatus.valueOf(statusData.toUpperCase().trim()));
			executionResultRepository.save(executionResult);
		}
		return true;

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
		LOGGER.info("Getting client port for deviceIP: {} and port: {}", deviceIP, port);
		JSONObject resultNode = new JSONObject();
		if (deviceIP != null && port != null) {
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

	/**
	 * This method is used to get the executions by category
	 * 
	 * @param category - the category RDKV, B, C
	 * @param page     - the page number
	 * @param size     - size in page
	 * @param sortBy   - by default it is createdDate
	 * @param sortDir  - by default it is desc
	 * @return ExecutionListResponseDTO
	 */
	@Override
	public ExecutionListResponseDTO getExecutionsByCategory(String categoryName, int page, int size, String sortBy,
			String sortDir) {
		LOGGER.info("Fetching executions by category: {} for size{} and page number{} ", categoryName, size, page);
		Category category = Category.valueOf(categoryName);
		if (category == null) {
			throw new UserInputException("Invalid category name provided");
		}

		Pageable pageable = getPageable(page, size, sortBy, sortDir);
		Page<Execution> pageExecutions = executionRepository.findByCategory(category, pageable);
		ExecutionListResponseDTO executionListResponseDTO = getExecutionListResponseFromSearchResult(pageExecutions);

		return executionListResponseDTO;
	}

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
	 * @return ExecutionListResponseDTO
	 */
	@Override
	public ExecutionListResponseDTO getExecutionsByScriptTestsuite(String testSuiteName, String categoryName, int page,
			int size, String sortBy, String sortDir) {
		LOGGER.info("Searching executions by test suite or script  name: {} for size{} and page number{} ",
				testSuiteName, size, page);

		Category category = Category.valueOf(categoryName);
		if (category == null) {
			throw new UserInputException("Invalid category name provided");
		}

		Pageable pageable = getPageable(page, size, sortBy, sortDir);
		// Search the executions based on the test suite name or script
		Page<Execution> pageExecutions = executionRepository.findByscripttestSuiteNameContainingAndCategory(
				testSuiteName, Category.valueOf(categoryName), pageable);

		ExecutionListResponseDTO executionListResponseDTO = getExecutionListResponseFromSearchResult(pageExecutions);

		return executionListResponseDTO;
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
	 * @return response DTO
	 */
	@Override
	public ExecutionListResponseDTO getExecutionsByDeviceName(String deviceName, String categoryName, int page,
			int size, String sortBy, String sortDir) {
		LOGGER.info("Fetching executions by device name: {} for size{} and page number{} ", deviceName, size, page);
		Pageable pageable = getPageable(page, size, sortBy, sortDir);
		Page<Execution> pageExecutions = executionRepository.findByDeviceName(deviceName, pageable);
		ExecutionListResponseDTO executionListResponseDTO = getExecutionListResponseFromSearchResult(pageExecutions);
		return executionListResponseDTO;
	}

	/**
	 * This method is used to get the executions by execution name with pagination
	 * 
	 * @param executionName - the execution name
	 * @param categoryName  - RDKV, RDKB, RDKC
	 * @param page          - the page number
	 * @param size          - size in page
	 * @param sortBy        - by default it is date
	 * @param sortDir       - by default it is desc
	 * @return executionListResponseDTO
	 */
	@Override
	public ExecutionListResponseDTO getExecutionsByExecutionName(String executionName, String categoryName, int page,
			int size, String sortBy, String sortDir) {
		LOGGER.info("Fetching executions by execution name: {} for size{} and page number{} ", executionName, size,
				page);
		Category category = Category.valueOf(categoryName);
		if (category == null) {
			throw new UserInputException("Invalid category name provided");
		}
		Pageable pageable = getPageable(page, size, sortBy, sortDir);
		Page<Execution> pageExecutions = executionRepository.findByNameContainingAndCategory(executionName, category,
				pageable);
		ExecutionListResponseDTO executionListResponseDTO = getExecutionListResponseFromSearchResult(pageExecutions);
		return executionListResponseDTO;

	}

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
	@Override
	public ExecutionListResponseDTO getExecutionsByUser(String username, String categoryName, int page, int size,
			String sortBy, String sortDir) {
		LOGGER.info("Fetching executions by user: {} for size{} and page number{} ", username, size, page);
		User user = userRepository.findByUsername(username);
		if (user == null) {
			throw new ResourceNotFoundException("User", username);
		}

		Category category = Category.valueOf(categoryName);
		if (category == null) {
			throw new UserInputException("Invalid category name provided");
		}

		Pageable pageable = getPageable(page, size, sortBy, sortDir);
		Page<Execution> pageExecutions = executionRepository.findByUserAndCategory(user, category, pageable);
		ExecutionListResponseDTO executionListResponseDTO = getExecutionListResponseFromSearchResult(pageExecutions);
		return executionListResponseDTO;

	}

	/**
	 * This method is used to get the pageable object
	 * 
	 * @param page    - the page number
	 * @param size    - size in page
	 * @param sortBy  - by default it is createdDate
	 * @param sortDir - by default it is desc
	 * @return Pageable - the pageable object
	 */
	private Pageable getPageable(int page, int size, String sortBy, String sortDir) {
		Sort sort = sortDir.equalsIgnoreCase(Sort.Direction.ASC.name()) ? Sort.by(sortBy).ascending()
				: Sort.by(sortBy).descending();
		return PageRequest.of(page, size, sort);
	}

	/**
	 * This method is to convert the pagination based execution search data to
	 * response DTO
	 * 
	 * @param pageExecutions - Execution pagination data
	 * @return Final Execution list response
	 */
	private ExecutionListResponseDTO getExecutionListResponseFromSearchResult(Page<Execution> pageExecutions) {
		List<Execution> listOfExecutions = pageExecutions.getContent();
		List<ExecutionListDTO> executionListDTO = getExecutionDTOListFromExecutionList(listOfExecutions);
		if (executionListDTO.isEmpty()) {
			return null;
		}
		ExecutionListResponseDTO executionListResponseDTO = new ExecutionListResponseDTO();
		executionListResponseDTO.setExecutions(executionListDTO);
		executionListResponseDTO.setCurrentPage(pageExecutions.getNumber());
		executionListResponseDTO.setTotalItems(pageExecutions.getTotalElements());
		executionListResponseDTO.setTotalPages(pageExecutions.getTotalPages());
		return executionListResponseDTO;

	}

	/*
	 * This method is used to get the execution dto list from the execution list
	 * 
	 * @param executionList - the execution list
	 * 
	 * @return List<ExecutionListDTO> - the execution list DTO
	 */
	private List<ExecutionListDTO> getExecutionDTOListFromExecutionList(List<Execution> executionList) {
		List<ExecutionListDTO> executionListDTO = new ArrayList<>();
		for (Execution execution : executionList) {
			ExecutionListDTO executionDTO = new ExecutionListDTO();
			executionDTO.setExecutionName(execution.getName());
			executionDTO.setExecutionDate(Utils.convertInstantToWithoutMilliseconds(execution.getCreatedDate()));
			executionDTO.setStatus(this.getStatusFromExecution(execution));
			// Find ExecutionDevice for execution
			ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);
			if (executionDevice != null) {
				executionDTO.setDevice(executionDevice.getDevice().getName());
			}

			User user = execution.getUser();
			if (user != null) {
				executionDTO.setUser(user.getUsername());
			}
			executionDTO.setExecutionId(execution.getId().toString());
			ExecutionType executionType = execution.getExecutionType();
			String scriptTestSuite = null;
			if (executionType != null) {
				if ((executionType.equals(ExecutionType.SINGLESCRIPT))
						|| (executionType.equals(ExecutionType.TESTSUITE))) {
					scriptTestSuite = execution.getScripttestSuiteName();
				} else if (executionType.equals(ExecutionType.MULTISCRIPT)) {
					scriptTestSuite = "Multiple Scripts";
				} else if (executionType.equals(ExecutionType.MULTITESTSUITE)) {
					scriptTestSuite = "MultiTestSuite";
				}

			}
			if (scriptTestSuite == null) {
				scriptTestSuite = "N/A";
			}
			executionDTO.setScriptTestSuite(scriptTestSuite);

			executionListDTO.add(executionDTO);
		}

		return executionListDTO;

	}

	/**
	 * Retrieves the status from the given Execution object.
	 *
	 * This method checks the execution status and result of the provided Execution
	 * object and returns the corresponding status as a string. The possible
	 * statuses are: - INPROGRESS: If the execution status is INPROGRESS. - ABORTED:
	 * If the execution status is ABORTED. - SUCCESS: If the execution status is
	 * COMPLETED and the result is SUCCESS. - FAILURE: If the execution status is
	 * COMPLETED and the result is FAILURE, or if none of the above conditions are
	 * met.
	 *
	 * @param execution the Execution object from which to retrieve the status
	 * @return a string representing the status of the execution
	 */
	private String getStatusFromExecution(Execution execution) {
		if (execution.getExecutionStatus() == ExecutionProgressStatus.INPROGRESS) {
			return ExecutionProgressStatus.INPROGRESS.toString();
		} else if (execution.getExecutionStatus() == ExecutionProgressStatus.ABORTED) {
			return ExecutionProgressStatus.ABORTED.toString();
		} else if (execution.getExecutionStatus() == ExecutionProgressStatus.COMPLETED) {
			if (execution.getResult() == ExecutionOverallResultStatus.SUCCESS) {
				return ExecutionOverallResultStatus.SUCCESS.toString();
			} else if (execution.getResult() == ExecutionOverallResultStatus.FAILURE) {
				return ExecutionOverallResultStatus.FAILURE.toString();
			}
		}
		return ExecutionOverallResultStatus.FAILURE.toString();

	}

	/**
	 * Retrieves the execution logs for a given execution result ID.
	 *
	 * @param executionResultID the ID of the execution result for which logs are to
	 *                          be fetched
	 * @return a string containing the execution remarks followed by the content of
	 *         the execution log file
	 * @throws ResourceNotFoundException if the execution result ID is not found or
	 *                                   if the log file does not exist
	 */
	@Override
	public String getExecutionLogs(String executionResultID) {
		LOGGER.info("Fetching execution logs for exec with Id: {}", executionResultID);
		ExecutionResult executionResult = executionResultRepository.findById(UUID.fromString(executionResultID))
				.orElseThrow(() -> new ResourceNotFoundException("Execution Result ID ", executionResultID));
		String executionID = executionResult.getExecution().getId().toString();

		String executionLogfile = commonService.getExecutionLogFilePath(executionID,
				executionResult.getId().toString());
		String executionRemarks = executionResult.getExecutionRemarks() + "\n";
		File logFile = new File(executionLogfile);
		if (logFile.exists()) {
			StringBuilder logFileData = new StringBuilder(executionRemarks); // Start with execution remarks

			try (BufferedReader reader = new BufferedReader(new FileReader(logFile))) {
				String line;
				while ((line = reader.readLine()) != null) {
					logFileData.append("\n").append(line); // Add line with newline character
				}
				return logFileData.toString();
			} catch (IOException e) {
				LOGGER.error("Error reading log file: {}", executionLogfile, e);
				return executionRemarks;
			}
		} else {
			LOGGER.warn("Log file does not exist: {}", executionLogfile);
			return ("Log file for the execution doesnt't exist");

		}
	}

	/**
	 * Retrieves the execution name based on the provided ExecutionNameRequestDTO.
	 * 
	 * @param nameRequestDTO the DTO containing the list of device names and test
	 *                       type
	 * @return the generated execution name
	 * 
	 *         The method performs the following steps: 1. Logs the initiation of
	 *         the execution name retrieval process. 2. Extracts the list of device
	 *         names from the request DTO. 3. Initializes an empty string for the
	 *         execution name. 4. Checks if the list of devices is not empty: - If
	 *         there are multiple devices, logs the process and generates an
	 *         execution name for multiple devices. - If there is a single device,
	 *         logs the process, retrieves the device from the repository, and
	 *         generates an execution name based on the device and test type.
	 */
	@Override
	public String getExecutionName(ExecutionNameRequestDTO nameRequestDTO) {
		// Implementation logic to handle the list of devices
		LOGGER.info("Going to get the Execution Name");
		List<String> devices = nameRequestDTO.getDeviceNames();
		String executionName = "";

		if (!devices.isEmpty()) {
			if (devices.size() > 1) {
				LOGGER.info("Going to generate device name for multiple devices execution");
				executionName = Constants.MULTIPLE_KEY_WORD + Constants.UNDERSCORE
						+ Utils.getTimeStampInUTCForExecutionName();
			} else if (devices.size() == 1) {
				LOGGER.info("Going to generate device name for single devices execution");
				Device device = deviceRepository.findByName(devices.getFirst());
				executionName = this.getExecutionNameFromDeviceAndTestType(device, nameRequestDTO.getTestType());
			}
		}

		return executionName;

	}

	/**
	 * Generates an execution name based on the provided device and test type.
	 *
	 * @param device   the device object containing information about the OEM and
	 *                 SOC
	 * @param testType the type of test being executed
	 * @return a string representing the execution name, which includes the SOC
	 *         name, OEM name, test type, and a timestamp in UTC format. If the OEM
	 *         or SOC is null, the device name is used instead. If the test type is
	 *         empty, only the timestamp is appended.
	 */
	private String getExecutionNameFromDeviceAndTestType(Device device, String testType) {
		LOGGER.info("Generating execution name based on device and test type");
		String executionName;
		Oem oem = device.getOem();
		Soc soc = device.getSoc();
		if (oem != null && soc != null) {
			executionName = soc.getName() + Constants.UNDERSCORE + oem.getName() + Constants.UNDERSCORE;
		} else if (oem != null && soc == null) {
			executionName = oem.getName() + Constants.UNDERSCORE;
		} else if (soc != null && oem == null) {
			executionName = soc.getName() + Constants.UNDERSCORE;
		} else {
			executionName = device.getName() + Constants.UNDERSCORE;
		}
		if (!Utils.isEmpty(testType)) {
			executionName += testType + Constants.UNDERSCORE + Utils.getTimeStampInUTCForExecutionName();
		} else {
			executionName += Utils.getTimeStampInUTCForExecutionName();
		}
		LOGGER.info("Generated Execution Name: {}", executionName);
		return executionName;
	}

	/**
	 * This method is used to get the trend analysis
	 * 
	 * @param executionResultId - the execution result ID
	 * @return List of String - the trend analysis
	 */
	@Override
	public List<String> getTrendAnalysis(UUID executionResultId) {
		LOGGER.info("Fetching script trend for executionResultId: {}", executionResultId);
		ExecutionResult executionResult;
		try {
			executionResult = executionResultRepository.findById(executionResultId)
					.orElseThrow(() -> new ResourceNotFoundException("ExecutionResult", executionResultId.toString()));
		} catch (ResourceNotFoundException e) {
			LOGGER.error("ExecutionResult not found with id: {}", executionResultId);
			throw e;
		} catch (Exception e) {
			LOGGER.error("Error fetching ExecutionResult with id: {}", executionResultId, e);
			throw new TDKServiceException(e.getMessage());
		}
		String scriptName = executionResult.getScript();
		List<ExecutionResult> results;
		try {
			Pageable pageable = PageRequest.of(0, 5);
			results = executionResultRepository.findTop5ByScriptOrderByDateOfExecutionDesc(scriptName, pageable);
		} catch (Exception e) {
			LOGGER.error("Error fetching script trend for script: {}", scriptName, e);
			throw new TDKServiceException(e.getMessage());
		}
		List<String> trend = results.stream().map(ExecutionResult::getResult).map(Enum::name).toList();
		LOGGER.info("Successfully fetched script trend for executionResultId: {}", executionResultId);
		return trend;
	}

	/**
	 * This method is used to get the execution result
	 * 
	 * @param execResultId - the execution result ID
	 * @return ExecutionResultResponseDTO - the execution result response
	 * @throws ResourceNotFoundException - if the execution result is not found
	 */
	@Override
	public ExecutionResultResponseDTO getExecutionResult(UUID execResultId) {
		LOGGER.info("Fetching execution result for  execResultId: {}" + execResultId);
		ExecutionResult executionResult;
		try {
			executionResult = executionResultRepository.findById(execResultId)
					.orElseThrow(() -> new ResourceNotFoundException("ExecutionResult", execResultId.toString()));
		} catch (ResourceNotFoundException e) {
			LOGGER.error("ExecutionResult not found with id: {}", execResultId);
			throw e;

		} catch (Exception e) {
			LOGGER.error("Error fetching ExecutionResult with id: {}", execResultId, e);
			throw new TDKServiceException(e.getMessage());
		}
		ExecutionResultResponseDTO response = new ExecutionResultResponseDTO();
		response.setScript(executionResult.getScript());
		response.setTimeTaken(executionResult.getExecutionTime());
		response.setExecutionTrend(getTrendAnalysis(execResultId));
		String executionLogs = null;
		executionLogs = this.getExecutionLogs(execResultId.toString());

		if (!Utils.isEmpty(executionLogs)) {
			response.setLogs(executionLogs);
		} else if (executionResult.getExecutionRemarks() != null) {
			response.setLogs(executionResult.getExecutionRemarks().toString());
		} else {
			response.setLogs("No logs found for this execution");
		}

		List<ExecutionMethodResult> methodResults;
		try {
			methodResults = executionMethodResultRepository.findByExecutionResult(executionResult);
			int methodCount = methodResults.size();
			response.setTestCaseCount(methodCount);

		} catch (Exception e) {
			LOGGER.error("Error fetching ExecutionMethodResults for ExecutionResult with id: {}", execResultId, e);
			throw new TDKServiceException(e.getMessage());
		}

		if (methodResults != null) {
			List<ExecutionMethodResultResponseDTO> methodResponse = new ArrayList<>();
			for (ExecutionMethodResult result : methodResults) {
				ExecutionMethodResultResponseDTO method = new ExecutionMethodResultResponseDTO();
				method.setFunctionName(result.getFunctionName());
				method.setActualResult(result.getActualResult().name());
				method.setExpectedResult(result.getExpectedResult().name());
				method.setResultStatus(result.getMethodResult().name());
				methodResponse.add(method);
			}
			response.setExecutionMethodResult(methodResponse);
		}

		// Check if logs are available and set the status in the response
		response.setAgentLogsAbvailable(this.checkLogExists(Constants.AGENTLOGTYPE, executionResult));
		response.setDeviceLogsAvailable(this.checkLogExists(Constants.DEVICELOGTYPE, executionResult));
		response.setCrashLogsAvailable(this.checkLogExists(Constants.CRASHLOGTYPE, executionResult));

		LOGGER.info("Successfully fetched execution result for execId: {}, execResultId: {}", execResultId);
		return response;
	}

	/**
	 * This method is used to check the log exists or not
	 * 
	 * @param logtype         - Device, Crash, Agent
	 * @param executionResult - the execution result
	 * @return boolean - true if the log exists, false otherwise
	 */
	private boolean checkLogExists(String logtype, ExecutionResult executionResult) {
		LOGGER.info("Checking if the log exists for log type: {}", logtype);
		String executionID = executionResult.getExecution().getId().toString();
		String executionResultID = executionResult.getId().toString();
		if (logtype.equalsIgnoreCase(Constants.DEVICELOGTYPE)) {
			return checkDeviceLogsExists(executionID, executionResultID);
		} else if (logtype.equalsIgnoreCase(Constants.AGENTLOGTYPE)) {
			return checkAgentLogsExists(executionID, executionResultID);
		} else if (logtype.equalsIgnoreCase(Constants.CRASHLOGTYPE)) {
			return false;
		} else {
			return false;
		}

	}

	/**
	 * This method is used to check the device logs exists or not
	 * 
	 * @param executionID       - the execution ID
	 * @param executionResultID - the execution result ID
	 * @return boolean - true if the device logs exists, false otherwise
	 */
	private boolean checkDeviceLogsExists(String executionID, String executionResultID) {
		String baseLogPath = commonService.getBaseLogPath();
		String devicelogsDirectoryPath = commonService.getDeviceLogsPathForTheExecution(executionID, executionResultID,
				baseLogPath);
		return commonService.checkAFolderExists(devicelogsDirectoryPath);
	}

	/**
	 * This method is used to check the agent logs exists or not
	 * 
	 * @param executionID       - the execution ID
	 * @param executionResultID - the execution result ID
	 * @return boolean - true if the agent logs exists, false otherwise
	 */
	private boolean checkAgentLogsExists(String executionID, String executionResultID) {
		String baseLogPath = commonService.getBaseLogPath();
		String agentLogsDirectoryPath = commonService.getAgentLogPath(executionID, executionResultID, baseLogPath);
		return commonService.checkAFolderExists(agentLogsDirectoryPath);
	}

	/**
	 * This method is used to abort the execution
	 * 
	 * @param execId - the execution ID
	 */

	@Override
	public boolean abortExecution(UUID execId) {
		LOGGER.info("Aborting execution with id: {}", execId);
		Execution execution = executionRepository.findById(execId)
				.orElseThrow(() -> new ResourceNotFoundException("Execution", execId.toString()));
		if (execution.getExecutionStatus() == ExecutionProgressStatus.COMPLETED) {
			LOGGER.error("Execution with id: {} is already completed", execId);
			throw new UserInputException("Execution is already completed");
		}
		try {
			execution.setAbortRequested(true);
			executionRepository.save(execution);
		} catch (Exception e) {
			LOGGER.error("Error aborting execution with id: {}", execId, e);
			throw new TDKServiceException(e.getMessage());
		}
		return true;
	}

	/**
	 * Repeats the execution of a given execution ID.
	 *
	 * @param execId the UUID of the execution to be repeated
	 * @return true if the execution is successfully repeated
	 * @throws ResourceNotFoundException if the execution, execution device, or
	 *                                   scripts are not found
	 * @throws TDKServiceException       if there is an error during the execution
	 *                                   repetition process
	 */
	@Override
	public boolean repeatExecution(UUID execId, String user) {
		LOGGER.info("Repeating execution with id: {}", execId);
		Execution execution = executionRepository.findById(execId)
				.orElseThrow(() -> new ResourceNotFoundException("Execution", execId.toString()));
		ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);
		if (executionDevice == null) {
			LOGGER.error("Execution Device not found for execution with id: {}", execId);
			throw new ResourceNotFoundException("Execution Device", "Execution ID: " + execId.toString());
		}

		Device device = executionDevice.getDevice();
		if (device == null) {
			LOGGER.error("Device not found for execution with id: {}", execId);
			throw new ResourceNotFoundException("Device", "for Execution ID: " + execId.toString());
		}

		try {
			List<ExecutionResult> executionResult = executionResultRepository.findByExecution(execution);
			List<String> scriptNames = executionResult.stream().map(ExecutionResult::getScript).toList();

			List<String> executionNames = executionRepository.findAll().stream().map(Execution::getName)
					.collect(Collectors.toList());
			String execName = getNextRepeatExecutionName(execution.getName(), executionNames);
			List<String> deviceList = new ArrayList<>();
			deviceList.add(device.getName());
			List<String> testSuiteList = new ArrayList<>();
			if (execution.getExecutionType() == ExecutionType.TESTSUITE) {
				testSuiteList.add(execution.getScripttestSuiteName());

			}
			ExecutionTriggerDTO executionTriggerDTO = new ExecutionTriggerDTO();
			executionTriggerDTO.setDeviceList(deviceList);
			if (testSuiteList == null || testSuiteList.isEmpty()) {
				executionTriggerDTO.setScriptList(scriptNames);
			}
			if (null != testSuiteList && !testSuiteList.isEmpty()) {
				executionTriggerDTO.setTestSuite(testSuiteList);
			}
			if (null != execution.getTestType()) {
				executionTriggerDTO.setTestType(execution.getTestType());
			}
			if (Utils.isEmpty(user) && null != execution.getUser()) {
				executionTriggerDTO.setUser(execution.getUser().getUsername());
			} else {
				executionTriggerDTO.setUser(user);
			}
			executionTriggerDTO.setCategory(execution.getCategory().name());
			executionTriggerDTO.setExecutionName(execName);
			executionTriggerDTO.setRepeatCount(1);
			executionTriggerDTO.setRerunOnFailure(false);
			executionTriggerDTO.setDeviceLogsNeeded(true);
			executionTriggerDTO.setDiagnosticLogsNeeded(true);
			executionTriggerDTO.setPerformanceLogsNeeded(true);
			this.startExecution(executionTriggerDTO);
			LOGGER.info("Successfully repeated execution with id: {}", execId);
		} catch (Exception e) {
			LOGGER.error("Error repeating execution with id: {}", execId, e);
			throw new TDKServiceException("Error repeating execution with id: " + execId + e.getMessage());
		}
		return true;
	}

	/**
	 * Re-runs the failed scripts for a given execution ID.
	 *
	 * @param execId the UUID of the execution whose failed scripts need to be
	 *               re-run
	 * @return true if the failed scripts were successfully re-run
	 * @throws ResourceNotFoundException if the execution, execution device, or
	 *                                   failed scripts are not found
	 * @throws TDKServiceException       if there is an error during the re-run
	 *                                   process
	 */
	@Override
	public boolean reRunFailedScript(UUID execId, String user) {
		LOGGER.info("Re-running failed scripts for execution with id: {}", execId);
		Execution execution = executionRepository.findById(execId).orElseThrow(
				() -> new ResourceNotFoundException("Execution", "id: " + execId.toString() + " not found"));
		ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);
		if (executionDevice == null) {
			LOGGER.error("Execution Device not found for execution with id: {}", execId);
			throw new ResourceNotFoundException("Execution Device", "Execution ID: " + execId.toString());
		}

		Device device = executionDevice.getDevice();
		if (device == null) {
			LOGGER.error("Device not found for execution with id: {}", execId);
			throw new ResourceNotFoundException("Device", "for Execution ID: " + execId.toString());
		}

		if (!device.getDeviceStatus().equals(DeviceStatus.FREE)) {
			LOGGER.error("Device with name: {} is not available for execution", device.getName());
			throw new UserInputException("Device selected is not available for execution");
		}

		List<ExecutionResult> failedResults = executionResultRepository.findByExecutionAndResult(execution,
				ExecutionResultStatus.FAILURE);
		if (failedResults.isEmpty() || failedResults == null) {
			LOGGER.error("No failed scripts found for execution with id: {}", execId);
			throw new ResourceNotFoundException("Failed Scripts", "for Execution ID: " + execId.toString());
		}
		User triggerUser = null;
		if (Utils.isEmpty(user)) {
			LOGGER.error("User not found for execution with id: {}", execId);
			triggerUser = execution.getUser();

		} else {
			triggerUser = userRepository.findByUsername(user);
		}
		try {
			List<String> failedScripts = failedResults.stream().map(ExecutionResult::getScript).toList();
			List<Script> scripts = getValidScriptList(failedScripts, new StringBuilder());
			List<String> executionNames = executionRepository.findAll().stream().map(Execution::getName)
					.collect(Collectors.toList());
			String execName = getNextRerunExecutionName(execution.getName(), executionNames);
			executionAsyncService.prepareAndExecuteMultiScript(executionDevice.getDevice(), scripts, triggerUser,
					execName, execution.getCategory().name(), execution.getTestType(), 1, false,
					execution.isDeviceLogsNeeded(), execution.isDiagnosticLogsNeeded(),
					execution.isDiagnosticLogsNeeded());
			LOGGER.info("Successfully re-run failed scripts for execution with id: {}", execId);
		} catch (Exception e) {
			LOGGER.error("Error re-running failed scripts for execution with id: {}", execId, e);
			throw new TDKServiceException(
					"Error re-running failed scripts for execution with id: " + execId + e.getMessage());
		}
		return true;
	}

	/**
	 * This method is used to delete single the execution detail
	 * 
	 * @param id - the execution ID
	 * @return ExecutionDetailsResponse
	 * @throws ResourceNotFoundException - if the execution is not found
	 */

	@Override
	@Transactional
	public boolean deleteExecution(UUID id) {
		LOGGER.info("Deleting execution with id: {}", id);
		this.deleteAllFilesForTheExecution(id.toString());
		Execution execution = executionRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException("Execution", id.toString()));
		List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);
		for (ExecutionResult executionResult : executionResults) {
			List<ExecutionMethodResult> executionMethodResults = executionMethodResultRepository
					.findByExecutionResult(executionResult);
			if (executionMethodResults != null && !executionMethodResults.isEmpty()) {
				executionMethodResultRepository.deleteAll(executionMethodResults);
			}
		}
		// Delete execution results
		if (executionResults != null && !executionResults.isEmpty()) {
			executionResultRepository.deleteAll(executionResults);
		}

		ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);
		if (executionDevice != null) {
			executionDeviceRepository.delete(executionDevice);
		}
		try {
			executionRepository.delete(execution);

			LOGGER.info("Successfully deleted execution with id: {}", id);
			return true;
		} catch (Exception e) {
			LOGGER.error("Error deleting execution with id: {}", id, e);
			throw new TDKServiceException("Error deleting execution with id: " + id);
		}
	}

	/**
	 * This method is used to delete the execution related files for the given
	 * execution
	 * 
	 * @param executionId - the execution ID
	 */
	private void deleteAllFilesForTheExecution(String executionId) {
		LOGGER.info("Deleting all files for the execution with id: {}", executionId);
		String logBasePath = commonService.getBaseLogPath();
		String executionBasePath = logBasePath + Constants.FILE_PATH_SEPERATOR + Constants.EXECUTION_KEYWORD
				+ Constants.UNDERSCORE + executionId;
		// Delete the execution folder
		File executionFolder = new File(executionBasePath);
		if (executionFolder.exists()) {
			try {
				FileUtils.deleteDirectory(executionFolder);
			} catch (IOException e) {
				LOGGER.error("Error deleting execution folder: {}", executionBasePath, e);
			}
		}

	}

	/**
	 * This method is used to delete the execution details list
	 * 
	 * @param id - the execution ID
	 * @return ExecutionDetailsResponse
	 * @throws ResourceNotFoundException - if the execution is not found
	 */

	@Override
	@Transactional
	public boolean deleteExecutions(List<UUID> ids) {
		LOGGER.info("Deleting executions with ids: {}", ids);
		try {
			for (UUID id : ids) {
				deleteExecution(id);
			}
			LOGGER.info("Successfully deleted executions with ids: {}", ids);
			return true;
		} catch (Exception e) {
			LOGGER.error("Error deleting executions with ids: {}", ids, e);
			throw new TDKServiceException("Error deleting executions with ids: " + ids);
		}
	}

	/**
	 * Generates the next repeat execution name based on the current execution name
	 * and a list of existing execution names.
	 *
	 * @param currentExecutionName   the current execution name to base the new name
	 *                               on
	 * @param existingExecutionNames a list of existing execution names to check for
	 *                               repeat counts
	 * @return the next repeat execution name in the format
	 *         "baseName_R{nextRepeatNumber}"
	 */
	public String getNextRepeatExecutionName(String currentExecutionName, List<String> existingExecutionNames) {
		// Extract the base name before "_R"
		String baseName = currentExecutionName.split("_R")[0];

		// Initialize the maximum repeat count
		int maxRepeatCount = 0;

		// Iterate through existing execution names
		for (String existingName : existingExecutionNames) {
			if (existingName.startsWith(baseName + "_R")) {
				try {
					// Extract the number after "_R"
					String suffix = existingName.substring((baseName + "_R").length());
					int repeatNumber = Integer.parseInt(suffix);

					// Update the maximum repeat count
					if (repeatNumber > maxRepeatCount) {
						maxRepeatCount = repeatNumber;
					}
				} catch (NumberFormatException e) {
					// Ignore names that do not conform to the pattern
					continue;
				}
			}
		}

		// Generate the next execution name
		return baseName + "_R" + (maxRepeatCount + 1);
	}

	/**
	 * Generates the next rerun execution name based on the current execution name
	 * and a list of existing execution names.
	 * 
	 * @param currentExecutionName   The name of the current execution.
	 * @param existingExecutionNames A list of existing execution names.
	 * @return The next rerun execution name.
	 * 
	 *         This method checks if the current execution name already contains
	 *         "RERUN". If it does, it extracts the base name and the current rerun
	 *         count. If it does not, it initializes the base name with "_RERUN"
	 *         appended to the current execution name.
	 * 
	 *         It then iterates through the list of existing execution names to find
	 *         the maximum rerun count for the given base name. Finally, it
	 *         generates the next rerun execution name by incrementing the maximum
	 *         rerun count by 1.
	 */
	public String getNextRerunExecutionName(String currentExecutionName, List<String> existingExecutionNames) {
		// Initialize the base name for rerun
		String baseName;
		int currentRerunCount = 0;

		// Check if the current execution name already contains "RERUN"
		if (currentExecutionName.contains("RERUN")) {
			int rerunIndex = currentExecutionName.lastIndexOf("RERUN");
			baseName = currentExecutionName.substring(0, rerunIndex + 5); // Include "RERUN"
			String suffix = currentExecutionName.substring(rerunIndex + 5);
			if (suffix.matches("\\d+")) {
				currentRerunCount = Integer.parseInt(suffix);
			}
		} else {
			baseName = currentExecutionName + "_RERUN";
		}

		// Initialize the maximum rerun count
		int maxRerunCount = currentRerunCount;

		// Iterate through the existing execution names
		for (String existingName : existingExecutionNames) {
			if (existingName.startsWith(baseName)) {
				try {
					// Check if the name ends with a number (e.g., _RERUN2, _R1_RERUN3)
					String suffix = existingName.substring(baseName.length());
					if (suffix.matches("\\d+")) {
						int rerunNumber = Integer.parseInt(suffix);
						maxRerunCount = Math.max(maxRerunCount, rerunNumber);
					}
				} catch (NumberFormatException e) {
					// Ignore names that do not conform to the expected pattern
					continue;
				}
			}
		}

		// Generate the next rerun execution name
		String name = baseName + (maxRerunCount + 1);
		return name;
	}

	/**
	 * Retrieves the execution details for a given execution ID.
	 *
	 * @param id the UUID of the execution to retrieve details for
	 * @return an ExecutionDetailsResponseDTO containing the details of the
	 *         execution
	 * @throws ResourceNotFoundException if the execution or execution device is not
	 *                                   found
	 */
	@Override
	public ExecutionDetailsResponseDTO getExecutionDetails(UUID id) {
		LOGGER.info("Fetching execution details for id: {}", id);
		Execution execution = executionRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException("Execution", "id" + id));
		ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);
		if (executionDevice == null) {
			LOGGER.error("Execution Device not found for execution with id: {}", id);
			throw new ResourceNotFoundException("Execution Device", "Execution ID: " + id + " not found");
		}
		Device device = executionDevice.getDevice();
		ExecutionDetailsResponseDTO response = new ExecutionDetailsResponseDTO();
		response.setDeviceName(device.getName());
		response.setDeviceIP(device.getIp());
		response.setDeviceMac(device.getMacId());
		response.setDeviceDetails(fileTransferService.getDeviceDetailsFromVersionFile(id.toString()));
		response.setDeviceImageName(executionDevice.getBuildName());
		response.setRealExecutionTime(execution.getRealExecutionTime());
		response.setTotalExecutionTime(execution.getExecutionTime());
		response.setDateOfExecution(execution.getCreatedDate());
		response.setExecutionType(execution.getExecutionType().name());
		response.setScriptTestSuite(execution.getScripttestSuiteName());
		response.setExecutionStatus(execution.getExecutionStatus().name());
		response.setResult(execution.getResult().name());
		response.setSummary(getExecutionSummary(execution));
		response.setExecutionResults(getExecutionResults(execution));
		return response;
	}

	/**
	 * Converts a list of ExecutionResult objects to a list of ExecutionResultDTO
	 * objects.
	 *
	 * @param execution the Execution object containing the list of ExecutionResult
	 *                  objects
	 * @return a list of ExecutionResultDTO objects
	 */
	public List<ExecutionResultDTO> getExecutionResults(Execution execution) {
		List<ExecutionResult> results = execution.getExecutionResults();
		List<ExecutionResultDTO> resultDTO = new ArrayList<>();
		for (ExecutionResult result : results) {
			ExecutionResultDTO resultDTOObj = new ExecutionResultDTO();
			resultDTOObj.setExecutionResultID(result.getId());
			resultDTOObj.setName(result.getScript());
			if (null != result.getStatus() && result.getStatus() == ExecutionStatus.INPROGRESS) {
				resultDTOObj.setStatus(ExecutionResultStatus.INPROGRESS.name());
			} else {
				resultDTOObj.setStatus(result.getResult().name());
			}

			resultDTO.add(resultDTOObj);
		}
		return resultDTO;
	}

	/**
	 * Generates an execution summary for the given execution.
	 *
	 * @param execution the execution object containing details of the execution
	 * @return an ExecutionSummaryResponseDTO object containing the summary of the
	 *         execution
	 */
	public ExecutionSummaryResponseDTO getExecutionSummary(Execution execution) {

		ExecutionSummaryResponseDTO summary = new ExecutionSummaryResponseDTO();
		summary.setTotalScripts(execution.getScriptCount());
		summary.setExecuted(execution.getExecutedScriptCount());
		summary.setInProgressCount((int) execution.getExecutionResults().stream()
				.filter(r -> r.getResult() == ExecutionResultStatus.INPROGRESS).count());
		summary.setSuccess((int) execution.getExecutionResults().stream()
				.filter(r -> r.getResult() == ExecutionResultStatus.SUCCESS).count());
		summary.setFailure((int) execution.getExecutionResults().stream()
				.filter(r -> r.getResult() == ExecutionResultStatus.FAILURE).count());
		summary.setPending((int) execution.getExecutionResults().stream()
				.filter(r -> r.getResult() == ExecutionResultStatus.PENDING).count());
		summary.setNa((int) execution.getExecutionResults().stream()
				.filter(r -> r.getResult() == ExecutionResultStatus.NA).count());
		summary.setTimeout((int) execution.getExecutionResults().stream()
				.filter(r -> r.getResult() == ExecutionResultStatus.TIMEOUT).count());
		summary.setSkipped((int) execution.getExecutionResults().stream()
				.filter(r -> r.getResult() == ExecutionResultStatus.SKIPPED).count());
		summary.setAborted((int) execution.getExecutionResults().stream()
				.filter(r -> r.getResult() == ExecutionResultStatus.ABORTED).count());
		summary.setSuccessPercentage((double) summary.getSuccess() / summary.getTotalScripts() * 100);

		return summary;

	}

	/**
	 * This method is used to get the unique users.
	 * 
	 * @return List of String - the list of unique users
	 */

	@Override
	public List<String> getUniqueUsers() {
		LOGGER.info("Fetching unique users");
		List<Execution> executions = executionRepository.findAll();
		Set<User> users = new HashSet<>();
		for (Execution execution : executions) {
			if (execution.getUser() != null) {
				users.add(execution.getUser());
			}
		}
		List<String> uniqueUsers = users.stream().map(User::getUsername).toList();
		LOGGER.info("Successfully fetched unique users");
		return uniqueUsers;
	}

	/**
	 * 
	 * This method is to get the module wise summary
	 * 
	 * @param executionId - the execution id
	 * @return the module wise summary
	 */
	@Override
	public Map<String, ExecutionSummaryResponseDTO> getModulewiseExecutionSummary(UUID executionId) {
		LOGGER.info("Fetching execution summary for id: {}", executionId);

		Execution execution = executionRepository.findById(executionId)
				.orElseThrow(() -> new ResourceNotFoundException("Execution with id", executionId.toString()));

		List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);
		if (executionResults.isEmpty()) {
			LOGGER.error("No execution results found for execution with id: {}", executionId);
			return null;
		}

		// Map to store module-wise summary and the module name
		Map<String, ExecutionSummaryResponseDTO> moduleSummaryMap = new HashMap<>();

		for (ExecutionResult executionResult : executionResults) {
			String scriptName = executionResult.getScript();
			Module module = scriptService.getModuleByScriptName(scriptName);
			String moduleName = module.getName();

			ExecutionSummaryResponseDTO executionSummaryResponseDTO = null;
			if (moduleSummaryMap.containsKey(moduleName)) {
				executionSummaryResponseDTO = moduleSummaryMap.get(moduleName);

			} else {
				executionSummaryResponseDTO = new ExecutionSummaryResponseDTO();
			}
			executionSummaryResponseDTO.setTotalScripts(executionSummaryResponseDTO.getTotalScripts() + 1);
			this.setExecutionSummaryCount(executionSummaryResponseDTO, executionResult.getResult());

			moduleSummaryMap.put(moduleName, executionSummaryResponseDTO);
		}

		moduleSummaryMap.put(Constants.TOTAL_KEYWORD, this.getExecutionSummary(execution));
		if (moduleSummaryMap.isEmpty()) {
			LOGGER.error("No module-wise summary found for execution with id: {}", executionId);
			return null;
		} else {
			LOGGER.info("Successfully fetched module-wise summary for execution with id: {}", executionId);
			// loop through the map and calculate percentage and assign it to the object
			// executionSummaryResponseDTO
			for (Map.Entry<String, ExecutionSummaryResponseDTO> entry : moduleSummaryMap.entrySet()) {
				String moduleName = entry.getKey();
				ExecutionSummaryResponseDTO summaryDTO = entry.getValue();

				// Calculate total scripts (excluding "Total Execution" entry)
				int totalScripts = summaryDTO.getTotalScripts();

				// Calculate percentages (assuming all counters are non-zero)
				if (totalScripts > 0) {
					summaryDTO.setSuccessPercentage((double) summaryDTO.getSuccess() / totalScripts * 100);
				}

				// Update the map with the modified DTO
				moduleSummaryMap.put(moduleName, summaryDTO);
			}

		}
		LOGGER.info("Successfully fetched execution summary for id: {}", executionId);

		return moduleSummaryMap;

	}

	/**
	 * This method is used to get the execution summary count assigned to the
	 * ExecutionSummaryResponseDTO object based on the ExecutionResultStatus
	 * 
	 * @param executionSummaryResponseDTO - the execution summary response DTO
	 * @param status                      - the execution
	 */
	private void setExecutionSummaryCount(ExecutionSummaryResponseDTO executionSummaryResponseDTO,
			ExecutionResultStatus status) {
		switch (status) {
		case SUCCESS:
			executionSummaryResponseDTO.setSuccess(executionSummaryResponseDTO.getSuccess() + 1);
			executionSummaryResponseDTO.setExecuted(executionSummaryResponseDTO.getExecuted() + 1);
			break;
		case FAILURE:
			executionSummaryResponseDTO.setFailure(executionSummaryResponseDTO.getFailure() + 1);
			executionSummaryResponseDTO.setExecuted(executionSummaryResponseDTO.getExecuted() + 1);
			break;
		case INPROGRESS:
			executionSummaryResponseDTO.setInProgressCount(executionSummaryResponseDTO.getInProgressCount() + 1);
			break;
		case PENDING:
			executionSummaryResponseDTO.setPending(executionSummaryResponseDTO.getPending() + 1);
			break;
		case NA:
			executionSummaryResponseDTO.setNa(executionSummaryResponseDTO.getNa() + 1);
			break;
		case TIMEOUT:
			executionSummaryResponseDTO.setTimeout(executionSummaryResponseDTO.getTimeout() + 1);
			break;
		case SKIPPED:
			executionSummaryResponseDTO.setSkipped(executionSummaryResponseDTO.getSkipped() + 1);
			break;
		case ABORTED:
			executionSummaryResponseDTO.setAborted(executionSummaryResponseDTO.getAborted() + 1);
			break;

		default:
			// Do nothing
			break;
		}

	}

	/**
	 * This method is used to delete the executions by date range
	 * 
	 * @param fromDate the start date
	 * @param toDate   end date
	 * @return total executions
	 */
	@Override
	public int deleteExecutionsByDateRange(Instant fromDate, Instant toDate) {
		LOGGER.info("Deleting executions between dates: {} and {}", fromDate, toDate);
		List<Execution> executions = executionRepository.executionListInDateRange(fromDate, toDate);
		if (executions.isEmpty()) {
			LOGGER.info("No executions found between dates: {} and {}", fromDate, toDate);
			return 0;
		}
		try {
			for (Execution execution : executions) {
				deleteExecution(execution.getId());
			}
			LOGGER.info("Successfully deleted executions between dates: {} and {}", fromDate, toDate);
			return executions.size();
		} catch (Exception e) {
			LOGGER.error("Error deleting executions between dates: {} and {}", fromDate, toDate, e);
			throw new TDKServiceException("Error deleting executions between dates: " + fromDate + " and " + toDate);
		}
	}
}
