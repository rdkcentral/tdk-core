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
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import com.jayway.jsonpath.internal.Utils;
import com.rdkm.tdkservice.config.AppConfig;
import com.rdkm.tdkservice.dto.CIComponentLevelDTO;
import com.rdkm.tdkservice.dto.CIDeviceDTO;
import com.rdkm.tdkservice.dto.CIRequestDTO;
import com.rdkm.tdkservice.dto.CIResultDTO;
import com.rdkm.tdkservice.dto.CIScriptDetailsDTO;
import com.rdkm.tdkservice.dto.CITestInfoDTO;
import com.rdkm.tdkservice.enums.DeviceStatus;
import com.rdkm.tdkservice.enums.ExecutionOverallResultStatus;
import com.rdkm.tdkservice.enums.ExecutionProgressStatus;
import com.rdkm.tdkservice.enums.ExecutionResultStatus;
import com.rdkm.tdkservice.enums.ExecutionStatus;
import com.rdkm.tdkservice.enums.ExecutionType;
import com.rdkm.tdkservice.exception.TDKServiceException;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.model.Execution;
import com.rdkm.tdkservice.model.ExecutionDevice;
import com.rdkm.tdkservice.model.ExecutionEntities;
import com.rdkm.tdkservice.model.ExecutionMethodResult;
import com.rdkm.tdkservice.model.ExecutionResult;
import com.rdkm.tdkservice.model.Script;
import com.rdkm.tdkservice.model.User;
import com.rdkm.tdkservice.repository.ExecutionDeviceRepository;
import com.rdkm.tdkservice.repository.ExecutionMethodResultRepository;
import com.rdkm.tdkservice.repository.ExecutionRepository;
import com.rdkm.tdkservice.repository.ExecutionResultRepository;
import com.rdkm.tdkservice.repository.ScriptRepository;
import com.rdkm.tdkservice.service.utilservices.CommonService;
import com.rdkm.tdkservice.service.utilservices.PythonLibraryScriptExecutorService;
import com.rdkm.tdkservice.service.utilservices.ScriptExecutorService;
import com.rdkm.tdkservice.util.Constants;

/**
 * This class is used to execute the scripts asynchronously.
 */
@Service
public class ExecutionAsyncService {

	@Autowired
	private ScriptExecutorService scriptExecutorService;

	@Autowired
	private ExecutionRepository executionRepository;

	@Autowired
	private ExecutionResultRepository executionResultRepository;

	@Autowired
	private ExecutionMethodResultRepository executionMethodResultRepository;

	@Autowired
	private ExecutionDeviceRepository executionDeviceRepository;

	@Autowired
	private ScriptRepository scriptRepository;

	@Autowired
	private CommonService commonService;

	@Autowired
	private HttpService httpService;

	@Autowired
	private AppConfig appConfig;

	@Autowired
	private DeviceStatusService deviceStatusService;

	@Autowired
	private FileTransferService fileTransferService;

	@Autowired
	private PythonLibraryScriptExecutorService pythonLibraryScriptExecutorService;

	private static final Logger LOGGER = LoggerFactory.getLogger(ExecutionService.class);

	/**
	 * This method is used to execute a single script on a device asynchronously.
	 * 
	 * @param device           This is the device on which the script should be
	 *                         executed.
	 * @param script           This is the script that should be executed.
	 * @param user             This is the user who triggered the execution.
	 * @param executionName    This is the name of the execution.
	 * @param category         This is the category of the device.
	 * @param repeatCount      This is the number of times the script should be
	 *                         repeated.
	 * @param isRerunOnFailure This is a boolean flag to indicate if the script
	 *                         should be rerun on failure.
	 */
	@Async
	public void prepareAndExecuteSingleScript(Device device, Script script, User user, String executionName,
			int repeatCount, boolean isRerunOnFailure, boolean isDeviceLogsNeeded, boolean isPerformanceLogsNeeded,
			boolean isDiagnosticLogsNeeded, String testType, String callBackUrl, String imageVersion) {
		LOGGER.info("Going to execute script: {} on device: {}", script.getName(), device.getName());
		// Busy lock in the database device entity before execution
		deviceStatusService.setDeviceStatus(DeviceStatus.IN_USE, device);
		try {
			String realExecutionName = "";

			// repeatCount means how many times the execution needs to be done
			// If 0 is added by the user , then the execution won't happen
			// So if the repeatcount is 0, then it is defaulted to 1
			if (repeatCount == 0) {
				repeatCount = 1;
			}
			for (int i = 0; i < repeatCount; i++) {
				if (i == 0) {
					realExecutionName = executionName;
				} else {
					// For repeat of the base execution, add a suffix R1, R2, R3 etc
					realExecutionName = executionName + "_R" + i;
				}
				// Start time is stored
				double executionStartTime = System.currentTimeMillis();

				// The set of objects required for the executing the script are added here.
				// for concise code
				ExecutionEntities executionEntities = this.getExecutionEntitiesForExecution(device, script, user,
						realExecutionName, isRerunOnFailure, isDeviceLogsNeeded, isPerformanceLogsNeeded,
						isDiagnosticLogsNeeded, testType);
				// Transfer the version File
				this.transferVersionFileOfTheDevice(executionEntities.getExecution().getId().toString(), device,
						executionEntities.getExecutionDevice().getId().toString());

				boolean executionStatus = executeScriptinDevice(script, executionEntities.getExecution(),
						executionEntities.getExecutionResult().get(0), executionEntities.getExecutionDevice());
				double executionEndTime = System.currentTimeMillis();
				double executionTime = this
						.roundOfToThreeDecimals(this.computeTimeDifference(executionStartTime, executionEndTime));

				double realExecutionTime = this.getRealExcecutionTime(executionEntities.getExecutionResult());
				this.setExecutionTime(executionEntities.getExecution(), executionTime, realExecutionTime);
				Execution finalExecutionStatus = this.setFinalStatusOfExecution(executionEntities.getExecution());
				this.callCiRequest(finalExecutionStatus, callBackUrl, imageVersion);

				// TODO : Execution Status logic cross check once again
				if (isRerunOnFailure && !executionStatus) {
					// For the rerun on Failure, add _RERUN in the execution name
					realExecutionName = realExecutionName + Constants.RERUN_APPENDER;
					executionStartTime = System.currentTimeMillis();
					ExecutionEntities executionEntitiesForFailureRerun = this.getExecutionEntitiesForExecution(device,
							script, user, realExecutionName, isRerunOnFailure, isDeviceLogsNeeded,
							isPerformanceLogsNeeded, isDiagnosticLogsNeeded, testType);

					executeScriptinDevice(script, executionEntitiesForFailureRerun.getExecution(),
							executionEntitiesForFailureRerun.getExecutionResult().get(0),
							executionEntitiesForFailureRerun.getExecutionDevice());

					this.transferVersionFileOfTheDevice(
							executionEntitiesForFailureRerun.getExecution().getId().toString(), device,
							executionEntities.getExecutionDevice().getId().toString());

					executionEndTime = System.currentTimeMillis();
					executionTime = this
							.roundOfToThreeDecimals(this.computeTimeDifference(executionStartTime, executionEndTime));
					realExecutionTime = this
							.getRealExcecutionTime(executionEntitiesForFailureRerun.getExecutionResult());
					this.setExecutionTime(executionEntities.getExecution(), executionTime, realExecutionTime);
					Execution execData = this
							.setFinalStatusOfExecution(executionEntitiesForFailureRerun.getExecution());
					this.callCiRequest(execData, callBackUrl, imageVersion);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			// Unlock the device with the current status
			deviceStatusService.fetchAndUpdateDeviceStatus(device);
			LOGGER.error("Error in executing script: {} on device: {} , due to the exception", script.getName(),
					device.getName(), e);
		}
		// Unlock the device with the current status
		deviceStatusService.fetchAndUpdateDeviceStatus(device);

	}

	/**
	 * This method is used to call ci request
	 * 
	 * @param finalExecutionStatus - the final execution status
	 * @param callBackUrl          - the call back url
	 * @param imageVersion         - the image
	 * 
	 */
	private void callCiRequest(Execution finalExecutionStatus, String callBackUrl, String imageVersion) {
		if (!finalExecutionStatus.getTestType().contains("CI")) {
			return;
		}

		CIRequestDTO request = getCIRequestForRDKPortal(finalExecutionStatus.getId().toString(), imageVersion);
		LOGGER.info("CI Jsonobject: {}", request);

		if (callBackUrl == null || callBackUrl.isEmpty()) {
			callBackUrl = getCallBackUrlFromConfig();
		}

		if (callBackUrl == null) {
			LOGGER.error("CallBack url not found in tm.config file");
			throw new TDKServiceException("CallBack url not found in tm.config file");
		}

		try {
			httpService.sendPostRequest(callBackUrl, request, null);
		} catch (Exception e) {
			LOGGER.error("Error occurred while sending the request to the CI server", e.getMessage());
		}
	}

	/*
	 * This method is used to get the call back url from the config file
	 * 
	 * @return String - the call back url
	 */
	private String getCallBackUrlFromConfig() {
		String configFilePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + Constants.TM_CONFIG_FILE;
		return commonService.getConfigProperty(new File(configFilePath), Constants.CI_CALLBACK_URL);
	}

	/**
	 * This method is used to set the execution time
	 * 
	 * @param executionObject   - the execution object
	 * @param executionTime     - the execution time
	 * @param executionRealTime - the real time for script execution
	 */
	private void setExecutionTime(Execution executionObject, double executionTime, double executionRealTime) {
		Execution execution = executionRepository.findById(executionObject.getId()).orElse(null);
		execution.setExecutionTime(executionTime);
		execution.setRealExecutionTime(executionRealTime);
		executionRepository.save(execution);

	}

	/**
	 * This method is used to execute multiple scripts on a device asynchronously.
	 * 
	 * @param device        This is the device on which the scripts should be
	 *                      executed.
	 * @param scriptList    This is the list of scripts that should be executed
	 * @param user          This is the user who triggered the execution.
	 * @param executionName This is the name
	 * @param category      This is the category of the device.
	 * @param testSuiteName This is the name of the test suite.
	 * 
	 */
	@Async
	public void prepareAndExecuteMultiScript(Device device, List<Script> scriptList, User user, String executionName,
			String category, String testSuiteName, int repeatCount, boolean isRerunOnFailure,
			boolean isDeviceLogsNeeded, boolean isDiagnosticsLogsNeeded, boolean isPerformanceNeeded,
			boolean isIndividualRepeatExecution, String testType, String callBackUrl, String imageVersion) {
		LOGGER.info("Executing multiple scripts execution in device:" + device.getName());
		deviceStatusService.setDeviceStatus(DeviceStatus.IN_USE, device);
		try {
			if (repeatCount == 0) {
				repeatCount = 1;
			}
			for (int repeatIndex = 0; repeatIndex < repeatCount; repeatIndex++) {
				String currentExecutionName = executionName;

				// Use the provided execution name for the first execution
				if (repeatIndex == 0) {
					currentExecutionName = executionName;
				} else {
					// Append _R<i> for subsequent executions, starting from _R1
					currentExecutionName = executionName + "_R" + repeatIndex;
				}

				List<Script> applicableScripts = new ArrayList<>();
				List<Script> invalidScripts = new ArrayList<>();
				int scriptCount = scriptList.size();

				for (Script script : scriptList) {
					if ((commonService.validateScriptDeviceDeviceType(device, script))
							&& (commonService.vaidateScriptDeviceCategory(device, script))
							&& !commonService.isScriptMarkedToBeSkipped(script)) {
						applicableScripts.add(script);
					} else {
						invalidScripts.add(script);
					}
				}

				double executionStartTime = System.currentTimeMillis();

				// Create and save Execution for the device
				Execution execution = new Execution();
				execution.setCategory(device.getCategory());
				if (testSuiteName == null) {
					execution.setExecutionType(ExecutionType.MULTISCRIPT);
					execution.setScripttestSuiteName("Multiple Scripts");
				} else if (Constants.MULTI_TEST_SUITE.equals(testSuiteName)) {
					execution.setExecutionType(ExecutionType.MULTITESTSUITE);
					execution.setScripttestSuiteName(testSuiteName);
				} else {
					execution.setExecutionType(ExecutionType.TESTSUITE);
					execution.setScripttestSuiteName(testSuiteName);
				}
				execution.setName(currentExecutionName);
				execution.setResult(ExecutionOverallResultStatus.INPROGRESS);
				execution.setExecutionStatus(ExecutionProgressStatus.INPROGRESS);
				execution.setScriptCount(scriptCount);
				execution.setTestType(testType);
				execution.setDeviceLogsNeeded(isDeviceLogsNeeded);
				execution.setDiagnosticLogsNeeded(isDiagnosticsLogsNeeded);
				execution.setPerformanceLogsNeeded(isPerformanceNeeded);
				execution.setUser(user);
				Execution savedExecution = executionRepository.save(execution);

				// Create and save ExecutionDevice
				ExecutionDevice executionDevice = new ExecutionDevice();
				executionDevice.setDevice(device);
				executionDevice.setExecution(execution);

				String executionID = savedExecution.getId().toString();

				ExecutionDevice savedExecutionDevice = executionDeviceRepository.save(executionDevice);

				List<ExecutionResult> execResultList = new ArrayList<>();
				List<ExecutionResult> inValidExecutionResults = new ArrayList<>();
				if (!invalidScripts.isEmpty()) {
					inValidExecutionResults = handleInvalidScripts(invalidScripts, execution, device);
				}

				List<ExecutionResult> executableResultList = new ArrayList<>();
				if (!applicableScripts.isEmpty()) {
					executableResultList = handleApplicableScripts(applicableScripts, device, execution,
							executionDevice, isIndividualRepeatExecution, repeatCount);
				}

				execResultList.addAll(inValidExecutionResults);
				execResultList.addAll(executableResultList);
				execution.setExecutionResults(execResultList);
				executionRepository.save(execution);

				UUID executionId = execution.getId();
				this.transferVersionFileOfTheDevice(executionID, device, savedExecutionDevice.getId().toString());
				int executedScript = 0;

				for (ExecutionResult execRes : executableResultList) {
					if (this.isExecutionAborted(executionId)) {
						for (ExecutionResult execResults : executableResultList) {
							if (execResults.getResult() == ExecutionResultStatus.INPROGRESS
									|| execResults.getResult() == ExecutionResultStatus.PENDING) {
								execResults.setResult(ExecutionResultStatus.ABORTED);
								execResults.setExecutionRemarks("Execution aborted by user");
								executionResultRepository.save(execResults);
							}
						}
						Execution executionAborted = executionRepository.findById(executionId).orElse(null);
						executionAborted.setExecutionStatus(ExecutionProgressStatus.ABORTED);
						executionAborted.setResult(ExecutionOverallResultStatus.ABORTED);
						executionRepository.save(executionAborted);
						LOGGER.info("Execution aborted for device: {}", device.getName());
						break;
					}
					execRes.setExecutionRemarks(
							"Executing script: " + execRes.getScript() + " on device: " + device.getName());
					executionResultRepository.save(execRes);
					Script script = scriptRepository.findByName(execRes.getScript());
					boolean executionResult = executeScriptinDevice(script, execution, execRes, executionDevice);

					if (executionResult) {
						LOGGER.info("Execution result success for {} on device: {}", script.getName(),
								device.getName());
					} else {
						LOGGER.info("Execution result failed for {} on device: {}", script.getName(), device.getName());
					}

					executedScript++;
					Execution executionCompleted = executionRepository.findById(executionId).orElse(null);
					double currentExecTime = System.currentTimeMillis();
					double executionTime = this.computeTimeDifference(executionStartTime, currentExecTime);
					executionCompleted.setExecutedScriptCount(executedScript);
					executionCompleted.setExecutionTime(executionTime);
					executionRepository.save(executionCompleted);

				}

				Execution finalExecution = executionRepository.findById(executionId).orElse(null);

				if (executableResultList != null) {
					double realExecTime = this.getRealExcecutionTime(executableResultList);
					double roundOfValue = this.roundOfToThreeDecimals(realExecTime);
					finalExecution.setRealExecutionTime(roundOfValue);
				}

				double executionEndTime = System.currentTimeMillis();
				double executionTime = this.computeTimeDifference(executionStartTime, executionEndTime);
				finalExecution.setExecutionTime(executionTime);
				executionRepository.save(finalExecution);
				Execution finalExecutionStatus = this.setFinalStatusOfExecution(finalExecution);
				this.callCiRequest(finalExecutionStatus, callBackUrl, imageVersion);

				if (isRerunOnFailure && (finalExecutionStatus.getResult() == ExecutionOverallResultStatus.FAILURE)) {
					List<String> failedScriptName = executableResultList.stream()
							.filter(result -> result.getResult() == ExecutionResultStatus.FAILURE)
							.map(ExecutionResult::getScript).toList();
					List<Script> failedScripts = failedScriptName.stream().map(scriptRepository::findByName).toList();
					if (!failedScripts.isEmpty()) {
						String rerunExecutionName = currentExecutionName + "_RERUN";
						LOGGER.info("Starting Rerun due to failure: execution name: {}", rerunExecutionName);
						prepareAndExecuteMultiScript(device, failedScripts, user, rerunExecutionName, category,
								testSuiteName, 1, false, isDeviceLogsNeeded, isDiagnosticsLogsNeeded,
								isPerformanceNeeded, isIndividualRepeatExecution, testType, callBackUrl, imageVersion);
					}
				}

				if (isIndividualRepeatExecution) {
					break;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			// Unlock the device with the current status
			deviceStatusService.fetchAndUpdateDeviceStatus(device);
			LOGGER.error("Error in executing scripts: {} on device: {}", device.getName());
			throw new TDKServiceException("Error in executing scripts: " + " on device: " + device.getName());
		}
		// Unlock the device with the current status
		deviceStatusService.fetchAndUpdateDeviceStatus(device);

	}

	/**
	 * Method to transfer version file from the device, get the image name and store
	 * in the Execution Device object
	 * 
	 * @param executionID       - ID of the Execution ID object
	 * @param device            - Device object
	 * @param executionDeviceID - ID of the Execution ID object
	 */
	private void transferVersionFileOfTheDevice(String executionID, Device device, String executionDeviceID) {
		boolean isVersionFileTransfered = fileTransferService.getVersionFileForTheDevice(executionID, device);
		if (!isVersionFileTransfered) {
			LOGGER.warn("Version file is not transferred for the device: {}", device.getName());
		}
		String buildName = fileTransferService.getImageName(executionID);
		if (Utils.isEmpty(buildName)) {
			buildName = Constants.BUILD_NAME_FAILED;
		}
		ExecutionDevice executionDevice = executionDeviceRepository.findById(UUID.fromString(executionDeviceID)).get();

		executionDevice.setBuildName(buildName);
		executionDeviceRepository.save(executionDevice);

	}

	/**
	 * Generates a CIRequestDTO for the RDK Portal based on the provided execution
	 * ID.
	 *
	 * @param executionId the ID of the execution to retrieve the CI request for
	 * @return a CIRequestDTO containing details about the execution, including
	 *         device and component level details
	 *
	 */
	private CIRequestDTO getCIRequestForRDKPortal(String executionId, String imageVersion) {
		LOGGER.info("Getting CI request for RDK Portal");
		Execution execution = executionRepository.findById(UUID.fromString(executionId)).orElse(null);
		String baseUrl = appConfig.getBaseURL() + "/execution/getExecutionLogs?executionResultID=";
		CIRequestDTO ciRequestDTO = new CIRequestDTO();
		ciRequestDTO.setService(Constants.TDK_PORTAL_SERVICE);
		ciRequestDTO.setStarted_at(getEpochTime(execution.getCreatedDate()));
		ciRequestDTO.setStarted_by("RDKPortal/Jenkins");
		ciRequestDTO.setStatus(execution.getResult().name());
		ciRequestDTO.setDuration(getExecutionDurationInEpoch(execution.getExecutionTime()));

		ArrayList<CIResultDTO> ciRequestDTOList = new ArrayList<>();
		CIResultDTO ciResultDTO = new CIResultDTO();
		ciResultDTO.setExecutionName(execution.getName());

		ArrayList<CIDeviceDTO> cIDeviceDTOList = new ArrayList<>();
		ArrayList<Object> systemInfoList = new ArrayList<>();
		ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);
		if (executionDevice != null) {
			CIDeviceDTO ciDeviceDTO = new CIDeviceDTO();
			ciDeviceDTO.setDevice(getDeviceNameFromConfigFile(imageVersion));
			ciDeviceDTO.setDeviceType(executionDevice.getDevice().getDeviceType().getName());
			ciDeviceDTO.setImageName(imageVersion);

			ArrayList<CIComponentLevelDTO> componentLevelDTOList = new ArrayList<>();
			List<ExecutionResult> executionResults = execution.getExecutionResults();

			Map<String, List<ExecutionResult>> moduleScriptMap = new HashMap<>();
			for (ExecutionResult result : executionResults) {
				String moduleName = scriptRepository.findByName(result.getScript()).getModule().getName();
				moduleScriptMap.computeIfAbsent(moduleName, k -> new ArrayList<>()).add(result);
			}

			for (Map.Entry<String, List<ExecutionResult>> entry : moduleScriptMap.entrySet()) {
				String moduleName = entry.getKey();
				List<ExecutionResult> scriptResults = entry.getValue();

				CIComponentLevelDTO ciComponentLevelDTO = new CIComponentLevelDTO();
				ciComponentLevelDTO.setModuleName(moduleName);
				boolean moduleStatus = true;
				ArrayList<CIScriptDetailsDTO> ciScriptDetailsDTOList = new ArrayList<>();
				for (ExecutionResult result : scriptResults) {
					CIScriptDetailsDTO ciScriptDetailsDTO = new CIScriptDetailsDTO();
					ciScriptDetailsDTO.setScriptName(result.getScript());
					ciScriptDetailsDTO.setScriptStatus(result.getResult().name());
					ciScriptDetailsDTO.setLogUrl(baseUrl + result.getId().toString());
					if (result.getResult().name().equals(ExecutionResultStatus.FAILURE.name())) {
						moduleStatus = false;
					}

					ArrayList<CITestInfoDTO> ciTestInfoDTOList = new ArrayList<>();
					if (moduleName.equals("rdkservices")) {
						List<ExecutionMethodResult> executionMethodResults = executionMethodResultRepository
								.findByExecutionResult(result);
						for (ExecutionMethodResult methodResult : executionMethodResults) {
							CITestInfoDTO ciTestInfoDTO = new CITestInfoDTO();
							ciTestInfoDTO.setTestCaseName(methodResult.getFunctionName());
							ciTestInfoDTO.setTestCaseStatus(methodResult.getActualResult().name());
							ciTestInfoDTOList.add(ciTestInfoDTO);
						}
					}
					ciScriptDetailsDTO.setTestInfo(ciTestInfoDTOList.isEmpty() ? new ArrayList<>() : ciTestInfoDTOList);

					ciScriptDetailsDTOList.add(ciScriptDetailsDTO);
				}

				if (moduleStatus) {
					ciComponentLevelDTO.setModuleStatus(ExecutionResultStatus.SUCCESS.name());
				} else {
					ciComponentLevelDTO.setModuleStatus(ExecutionResultStatus.FAILURE.name());
				}
				ciComponentLevelDTO.setScriptDetails(ciScriptDetailsDTOList);
				componentLevelDTOList.add(ciComponentLevelDTO);
			}
			ciDeviceDTO.setComponentLevelDetails(componentLevelDTOList);
			ciDeviceDTO.setSystemLevelDetails(systemInfoList);
			cIDeviceDTOList.add(ciDeviceDTO);
		}

		ciResultDTO.setDeviceDetails(cIDeviceDTOList.isEmpty() ? new ArrayList<>() : cIDeviceDTOList);
		ciRequestDTOList.add(ciResultDTO);
		ciRequestDTO.setResult(ciRequestDTOList.isEmpty() ? new ArrayList<>() : ciRequestDTOList);

		return ciRequestDTO;
	}

	/*
	 * The method is used to get the Device corresponding to the image version from
	 * config file
	 * 
	 * @param imageVersion - the image version
	 * 
	 * @return - the device
	 */
	private String getDeviceNameFromConfigFile(String imageVersion) {
		String configFilePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
				+ Constants.CI_IMAGE_BOXTYPE_CONFIG_FILE;
		List<Map<String, String>> boxTypeMap = parseConfigFile(configFilePath);

		for (Map<String, String> boxType : boxTypeMap) {
			for (Map.Entry<String, String> entry : boxType.entrySet()) {
				if (entry.getValue() != null && entry.getValue().contains(imageVersion)) {
					return entry.getKey();
				}
			}
		}
		throw new TDKServiceException("Device name not found for image version: " + imageVersion);
	}

	/**
	 * This method is used to create a map of Device and Corresponding Image Version
	 * keyWord From Config file
	 * 
	 * @param filePath - the file path
	 * @return - the list of map of device and image version keyword
	 */
	public static List<Map<String, String>> parseConfigFile(String filePath) {
		List<Map<String, String>> configMaps = new ArrayList<>();
		Map<String, String> configMap = new HashMap<>();

		try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
			String line;
			while ((line = reader.readLine()) != null) {
				// Trim and skip empty or comment lines
				line = line.trim();
				if (line.isEmpty() || line.startsWith("#")) {
					continue;
				}

				// Split the line by ':'
				String[] parts = line.split("=", 2);
				if (parts.length == 2) {
					String key = parts[0].trim();
					String value = parts[1].trim();
					configMap.put(key, value);
				}
			}

			// Add the map to the list if it's not empty
			if (!configMap.isEmpty()) {
				configMaps.add(configMap);
			}

		} catch (Exception e) {
			LOGGER.error("Error reading config file: {}", filePath, e);
			throw new TDKServiceException("Error reading config file: " + filePath);
		}

		return configMaps;
	}

	/**
	 * Converts the given execution time in minutes to epoch time in seconds.
	 *
	 * @param executionTime the execution time in minutes
	 * @return the execution time in epoch seconds as a String
	 */
	private String getExecutionDurationInEpoch(double executionTime) {
		// convert double to epoch time
		long epochTime = (long) (executionTime * 60);
		return String.valueOf(epochTime);

	}

	/**
	 * Converts the given Instant to its epoch time in milliseconds as a String.
	 *
	 * @param createdDate the Instant to be converted
	 * @return the epoch time in milliseconds as a String
	 */
	private String getEpochTime(Instant createdDate) {
		return String.valueOf(createdDate.toEpochMilli());

	}

	/**
	 * Checks if the execution with the given ID has been aborted.
	 *
	 * @param executionId the unique identifier of the execution
	 * @return {@code true} if the execution has an abort request, {@code false}
	 *         otherwise
	 */
	private boolean isExecutionAborted(UUID executionId) {
		Execution execution = executionRepository.findById(executionId).orElse(null);
		if (execution == null) {
			return false;
		}
		return execution.isAbortRequested();
	}

	/**
	 * The method is used to execute the script in the device
	 * 
	 * @param script          - the script to be executed
	 * @param execution       - the execution object
	 * @param executionResult - the execution result object
	 * @param executionDevice - the execution device object
	 * @return boolean - true if the script is executed successfully, false
	 *         otherwise
	 */
	private boolean executeScriptinDevice(Script script, Execution execution, ExecutionResult executionResult,
			ExecutionDevice executionDevice) {
		String output = "";
		LOGGER.info("Executing script: {} on device: {}", script.getName(), executionDevice.getDevice().getName());
		Device device = executionDevice.getDevice();
		StringBuilder remarksString = new StringBuilder();
		remarksString.append("Execution started in device: ").append(device.getName()).append(" for script: ")
				.append(script.getName()).append("\n");
		executionResult.setExecutionRemarks(remarksString.toString());
		executionResult.setResult(ExecutionResultStatus.INPROGRESS);
		executionResult.setStatus(ExecutionStatus.INPROGRESS);
		executionResultRepository.save(executionResult);
		ExecutionResultStatus finalExecutionResultStatus = ExecutionResultStatus.FAILURE;
		try {
			String basePathForFileStore = AppConfig.getBaselocation();
			String scriptPath = script.getScriptLocation();
			String absoluteScriptFilePath = basePathForFileStore + Constants.FILE_PATH_SEPERATOR + scriptPath
					+ Constants.FILE_PATH_SEPERATOR + script.getName() + Constants.PYTHON_FILE_EXTENSION;
			String temporaryScriptPath = basePathForFileStore + Constants.FILE_PATH_SEPERATOR
					+ Constants.TEMP_SCRIPT_FILE_KEYWORD + Constants.UNDERSCORE + script.getName()
					+ Constants.UNDERSCORE + System.currentTimeMillis() + Constants.PYTHON_FILE_EXTENSION;

			// Read the content of the original python script
			String content = null;
			content = readFile(absoluteScriptFilePath);
			if (content == null || content.isEmpty()) {
				remarksString
						.append("There is something wrong with the script, Please check the script is there or not\n");
				executionResult.setExecutionRemarks(remarksString.toString());
				executionResult.setResult(ExecutionResultStatus.FAILURE);
				executionResult.setStatus(ExecutionStatus.COMPLETED);
				executionResultRepository.save(executionResult);
				return false;
			}

			// Prepare replacements and modify content
			Map<String, String> replacements = new HashMap<>();
			replacements.put(Constants.PORT_REPLACE_TOKEN, device.getPort());
			replacements.put(Constants.IP_REPLACE_TOKEN, "\"" + device.getIp() + "\"");
			replacements.put(Constants.CONFIGURE_TESTCASE_REPLACE_TOKEN,
					prepareReplacementString(device, execution, executionDevice, executionResult, script));
			String modifiedContent = modifyContent(content, replacements);

			// Append the script end token to the modified content, to identify the
			// end of the script execution
			modifiedContent += Constants.SCRIPT_END_PY_CODE;
			// Write the modified content to a temporary file
			writeFile(temporaryScriptPath, modifiedContent);

			// If the script is marked as long duration, then there is no timeout
			// for the scripts execution
			int waittime = 0;
			if (!script.isLongDuration()) {
				waittime = script.getExecutionTimeOut();
			}
			// A standardized path for storing the logs
			String executionLogfile = commonService.getExecutionLogFilePath(execution.getId().toString(),
					executionResult.getId().toString());

			LOGGER.info("Execution log file path: " + executionLogfile);

			String[] commands = { commonService.getPythonCommandFromConfig(), temporaryScriptPath };

			double currentTimeMillisBeforeExecution = System.currentTimeMillis();

			output = scriptExecutorService.executeTestScript(commands, waittime, executionLogfile);

			double currentTimeMillisAfterExecution = System.currentTimeMillis();

			// Finding the execution time and converts to minutes
			double executiontime = this.computeTimeDifference(currentTimeMillisBeforeExecution,
					currentTimeMillisAfterExecution);
			executionResult.setExecutionTime(executiontime);

			LOGGER.debug("Execution output: " + output);

			// Update the execution result based on the output

			// If there is a TDK_error string , add it as failure
			if (output.contains(Constants.ERROR_TAG_PY_COMMENT)) {
				LOGGER.info(
						"There is TDK error string in the log, So it can be an exception or error from the python framework");
				executionResult.setResult(ExecutionResultStatus.FAILURE);
				executionResultRepository.save(executionResult);
				if (!device.isThunderEnabled()) {
					LOGGER.info("The device is TDK enabled, So after the error, the TDK agent needs to be reset");
					pythonLibraryScriptExecutorService.resetAgentForTDKDevices(device.getIp(), device.getPort(),
							Constants.TRUE);
				}
			} else if (output.contains("Pre-Condition not met")) {
				LOGGER.info("Precondition failure happened");
				executionResult.setResult(ExecutionResultStatus.FAILURE);
				executionResultRepository.save(executionResult);
			} else {

				if (output.contains(Constants.END_TAG_PY_COMMENT)) {
					// The execution result is parallely set from the python framework via APIS
					// that is added here
					ExecutionResult finalExecutionResult = executionResultRepository.findById(executionResult.getId())
							.get();
					finalExecutionResultStatus = finalExecutionResult.getResult();
					executionResult.setResult(finalExecutionResultStatus);
					executionResultRepository.save(executionResult);

				} else {
					// If the script output does not contain the script end token,
					// then the script execution is considered as interrupted in between due
					// to timeout or either any abrupt failure
					if ((executiontime >= waittime) && (waittime != 0)) {
						LOGGER.info("The script execution is interrupted due to timeout");
						executionResult.setResult(ExecutionResultStatus.TIMEOUT);
						if (!device.isThunderEnabled()) {
							LOGGER.info(
									"The device is TDK enabled, the TDK agent needs to be reset, other wise the device status will be in busy state");
							pythonLibraryScriptExecutorService.resetAgentForTDKDevices(device.getIp(), device.getPort(),
									Constants.TRUE);
						}
					} else {
						executionResult.setResult(ExecutionResultStatus.FAILURE);
						if (!device.isThunderEnabled()) {
							LOGGER.info(
									"The device is TDK enabled, the TDK agent needs to be reset, other wise the device status will be in busy state");
							pythonLibraryScriptExecutorService.resetAgentForTDKDevices(device.getIp(), device.getPort(),
									Constants.FALSE);
						}
					}
					executionResultRepository.save(executionResult);

				}

			}

			// Delete the temporary script file after execution
			deleteTemporaryFile(temporaryScriptPath);
			// remove the unwanted comments in the console log like TDK_ERROR which were
			// added for the result status reading
			this.removeFWRequiredTextsFromLogs(executionLogfile);

			if (execution.isDeviceLogsNeeded()) {
				fileTransferService.transferDeviceLogs(execution, executionResult, device);
			}

			if (execution.isDiagnosticLogsNeeded() && device.isThunderEnabled()) {
				fileTransferService.transferDiagnosisLogs(execution, executionResult, device);
			}

			// transfer crash logs
			fileTransferService.transferCrashLogs(execution, executionResult, device);

			ExecutionResult finalExecutionResult = executionResultRepository.findById(executionResult.getId()).get();
			finalExecutionResult.setStatus(ExecutionStatus.COMPLETED);
			executionResultRepository.save(finalExecutionResult);

		} catch (Exception e) {
			finalExecutionResultStatus = ExecutionResultStatus.FAILURE;
			executionResult.setResult(ExecutionResultStatus.FAILURE);
			executionResult.setStatus(ExecutionStatus.COMPLETED);
			executionResult.setExecutionRemarks("Execution failed due to some issue in TM");
			executionResultRepository.save(executionResult);
			LOGGER.error("Error in executing script: {} on device: {} due to ", script.getName(), device.getName(), e);
		}

		// boolean returned with execution result status
		return finalExecutionResultStatus == ExecutionResultStatus.SUCCESS;
	}

	/**
	 * This method is to remove unwanted texts that was added for the python script
	 * execution status checks. SCRIPTEND#!@~ for checking python script was
	 * executed till end. "#TDK_@error" for adding the status as Failure when
	 * exception is thrown from the python script
	 * 
	 * @param logFilePath
	 */
	private void removeFWRequiredTextsFromLogs(String logFilePath) {
		File logFile = new File(logFilePath);
		if (!logFile.exists()) {
			LOGGER.error("Log file does not exist at path: " + logFilePath);
			return;
		}
		StringBuilder contentBuilder = new StringBuilder();
		try (BufferedReader br = new BufferedReader(new FileReader(logFilePath))) {
			String line;
			while ((line = br.readLine()) != null) {
				line = line.replace(Constants.END_TAG_PY_COMMENT, "").replace(Constants.ERROR_TAG_PY_COMMENT, "");
				contentBuilder.append(line).append("\n");
			}
		} catch (IOException e) {
			LOGGER.error("Error reading log file: " + logFilePath, e);
			return;
		}

		try (BufferedWriter bw = new BufferedWriter(new FileWriter(logFilePath))) {
			bw.write(contentBuilder.toString());
		} catch (IOException e) {
			LOGGER.error("Error writing to log file: " + logFilePath, e);
		}

	}

	/**
	 * Sets the final status of the given execution object based on the results of
	 * its execution.
	 *
	 * This method retrieves the execution object from the repository using its ID.
	 * If the execution status is INPROGRESS, it updates the status to COMPLETED. It
	 * then retrieves the list of execution results associated with the execution
	 * and calculates the counts of different result statuses (FAILURE, NA, TIMEOUT,
	 * SUCCESS, SKIPPED).
	 *
	 * Based on the counts of these result statuses, the method sets the overall
	 * result status of the execution: - If there are any FAILURE results, the
	 * overall result is set to FAILURE. - If there are any TIMEOUT results, the
	 * overall result is set to FAILURE. - If all results are either NA or SKIPPED,
	 * the overall result is set to FAILURE. - If there are any SUCCESS results, the
	 * overall result is set to SUCCESS.
	 *
	 * Finally, the method saves the updated execution object back to the
	 * repository.
	 *
	 * @param executionObject the execution object whose final status needs to be
	 *                        set
	 * @return the updated execution object with the final status set
	 */
	private Execution setFinalStatusOfExecution(Execution executionObject) {

		Execution execution = executionRepository.findById(executionObject.getId()).orElse(null);

		if (execution.getExecutionStatus() == ExecutionProgressStatus.INPROGRESS) {
			execution.setExecutionStatus(ExecutionProgressStatus.COMPLETED);
		}

		if (execution.getExecutionStatus() == ExecutionProgressStatus.ABORTED) {
			return execution;
		}

		List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);
		int totalExecuted = 0;
		int failureCount = 0;
		int naCount = 0;
		int skipped = 0;
		int success = 0;
		int scriptTimeoutCount = 0;

		if (executionResults == null || executionResults.isEmpty()) {
			execution.setResult(ExecutionOverallResultStatus.FAILURE);
			execution.setExecutionStatus(ExecutionProgressStatus.COMPLETED);
			executionRepository.save(execution);
			return execution;
		}

		for (ExecutionResult result : executionResults) {
			ExecutionResultStatus status = result.getResult();
			totalExecuted++;
			if (status == ExecutionResultStatus.FAILURE) {
				failureCount++;
			} else if (status == ExecutionResultStatus.NA) {
				naCount++;
			} else if (status == ExecutionResultStatus.TIMEOUT) {
				scriptTimeoutCount++;
			} else if (status == ExecutionResultStatus.SUCCESS) {
				success++;
			} else if (status == ExecutionResultStatus.SKIPPED) {
				skipped++;
			}
		}

		if (failureCount > 0) {
			execution.setResult(ExecutionOverallResultStatus.FAILURE);
		} else if (scriptTimeoutCount > 0) {
			execution.setResult(ExecutionOverallResultStatus.FAILURE);
		} else if (naCount + skipped == totalExecuted) {
			execution.setResult(ExecutionOverallResultStatus.FAILURE);
		} else if (success > 0) {
			execution.setResult(ExecutionOverallResultStatus.SUCCESS);
		}

		executionRepository.save(execution);
		return execution;

	}

	/**
	 * 
	 * This method is used to get execution entities for the execution as a code
	 * optimisaation for Single script execution
	 * 
	 * @param device
	 * @param script
	 * @param user
	 * @param executionName
	 * @param category
	 * @param isRerunOnFailure
	 * @return ExecutionEntities
	 * 
	 */
	private ExecutionEntities getExecutionEntitiesForExecution(Device device, Script script, User user,
			String executionName, boolean isRerunOnFailure, boolean isDeviceLogsNeeded, boolean isPerformanceLogsNeeded,
			boolean isDiagnosticLogsNeeded,String testType) {
		Execution execution = new Execution();
		execution.setName(executionName);
		execution.setCategory(device.getCategory());
		execution.setExecutionType(ExecutionType.SINGLESCRIPT);
		execution.setScripttestSuiteName(script.getName());
		execution.setRerunOnFailure(isRerunOnFailure);
		execution.setResult(ExecutionOverallResultStatus.INPROGRESS);
		execution.setExecutionStatus(ExecutionProgressStatus.INPROGRESS);
		execution.setScriptCount(1);
		execution.setUser(user);
		execution.setTestType(testType);
		execution.setDeviceLogsNeeded(isDeviceLogsNeeded);
		execution.setPerformanceLogsNeeded(isPerformanceLogsNeeded);
		execution.setDiagnosticLogsNeeded(isDiagnosticLogsNeeded);
		Execution savedExecution = executionRepository.save(execution);

		// Create and save ExecutionDevice
		ExecutionDevice executionDevice = new ExecutionDevice();
		executionDevice.setDevice(device);
		executionDevice.setExecution(savedExecution);
		// Before saving the execution device, get the latest build name from the device
		executionDeviceRepository.save(executionDevice);

		ExecutionResult executionResult = new ExecutionResult();
		executionResult.setDateOfExecution(Instant.now());
		executionResult.setExecution(execution);
		executionResult.setScript(script.getName());
		executionResult.setResult(ExecutionResultStatus.INPROGRESS);
		executionResultRepository.save(executionResult);

		ExecutionEntities executionEntites = new ExecutionEntities();
		executionEntites.setExecution(execution);
		executionEntites.setExecutionDevice(executionDevice);
		List<ExecutionResult> executionResultList = new ArrayList<ExecutionResult>();
		executionResultList.add(executionResult);
		executionEntites.setExecutionResult(executionResultList);

		return executionEntites;

	}

	/**
	 * This method is used to get real execution time
	 * 
	 * @param executableResultList
	 * @return double
	 */
	private double getRealExcecutionTime(List<ExecutionResult> executableResultList) {
		double realExecutionTime = 0L;
		for (ExecutionResult executionResult : executableResultList) {
			realExecutionTime += executionResult.getExecutionTime();
		}
		return realExecutionTime;
	}

	/**
	 * Handles invalid scripts by generating execution results for each script.
	 * 
	 * @param invalidScripts the list of invalid scripts to be processed
	 * @param execution      the execution context associated with the scripts
	 * @param device         the device associated with the execution
	 * @return a list of execution results for the invalid scripts
	 */
	private List<ExecutionResult> handleInvalidScripts(List<Script> invalidScripts, Execution execution,
			Device device) {
		List<ExecutionResult> execResultList = new ArrayList<>();
		for (Script script : invalidScripts) {
			StringBuilder remarks = new StringBuilder();
			ExecutionResult executionResult = new ExecutionResult();
			executionResult.setDateOfExecution(Instant.now());
			executionResult.setExecution(execution);
			executionResult.setScript(script.getName());

			if (script.isSkipExecution()) {
				remarks.append("Script: ").append(script.getName())
						.append(" is marked as skipTest, so not triggering execution.\n");
				executionResult.setResult(ExecutionResultStatus.SKIPPED);
			} else if (!commonService.validateScriptDeviceDeviceType(device, script)) {
				remarks.append("Device: ").append(device.getName()).append(" and Script: ").append(script.getName())
						.append(" combination is invalid due to different device types, so not triggering execution.\n");
				executionResult.setResult(ExecutionResultStatus.NA);
			} else if (!commonService.vaidateScriptDeviceCategory(device, script)) {
				remarks.append("Device: ").append(device.getName()).append(" and Script: ").append(script.getName())
						.append(" combination is invalid and belongs to different category, so not triggering execution.\n");
				executionResult.setResult(ExecutionResultStatus.NA);
			}

			executionResult.setExecutionRemarks(remarks.toString());
			executionResultRepository.save(executionResult);
			execResultList.add(executionResult);
		}
		return execResultList;
	}

	/*
	 * This method is to handle the applicable scripts and create the execution
	 * result for the same and save it
	 * 
	 * @param applicableScripts
	 * 
	 * @param device
	 * 
	 * @param execution
	 * 
	 * @param executionDevice
	 * 
	 * @return List<ExecutionResult>
	 */

	private List<ExecutionResult> handleApplicableScripts(List<Script> applicableScripts, Device device,
			Execution execution, ExecutionDevice executionDevice, boolean isIndividualRepeatExecution,
			int repeatCount) {
		if (!isIndividualRepeatExecution) {
			repeatCount = 1;
		}
		List<ExecutionResult> executableResultList = new ArrayList<>();
		for (Script script : applicableScripts) {
			for (int i = 0; i < repeatCount; i++) {
				LOGGER.info("Executing script: {} on device: {}", script.getName(), device.getName());
				ExecutionResult executionResult = new ExecutionResult();
				executionResult.setDateOfExecution(Instant.now());
				executionResult.setExecution(execution);
				executionResult.setScript(script.getName());
				executionResult.setResult(ExecutionResultStatus.PENDING);
				executionResultRepository.save(executionResult);
				executableResultList.add(executionResult);
			}
		}
		return executableResultList;
	}

	/**
	 * This method is used to create the replacement string for the script the
	 * params that should be passed to the ConfigureTestCase method in the python
	 * script
	 * 
	 * @param device
	 * @param execution
	 * @param executionDevice
	 * @param executionResult
	 * @param script
	 * @return the modified ConfigureTestCase method string with required parameters
	 */
	private String prepareReplacementString(Device device, Execution execution, ExecutionDevice executionDevice,
			ExecutionResult executionResult, Script script) {
		return Constants.METHOD_TOKEN + Constants.LEFT_PARANTHESIS + Constants.SINGLE_QUOTES
				+ commonService.getTMUrlFromConfigFile() + Constants.SINGLE_QUOTES + Constants.COMMA_SEPERATOR
				+ Constants.SINGLE_QUOTES + AppConfig.getRealPath() + Constants.SINGLE_QUOTES
				+ Constants.COMMA_SEPERATOR + Constants.SINGLE_QUOTES + commonService.getBaseLogPath()
				+ Constants.SINGLE_QUOTES + Constants.COMMA_SEPERATOR + Constants.SINGLE_QUOTES + execution.getId()
				+ Constants.SINGLE_QUOTES + Constants.COMMA_SEPERATOR + Constants.SINGLE_QUOTES
				+ executionDevice.getId() + Constants.SINGLE_QUOTES + Constants.COMMA_SEPERATOR
				+ Constants.SINGLE_QUOTES + executionResult.getId() + Constants.SINGLE_QUOTES
				+ Constants.REPLACE_BY_TOKEN + device.getAgentMonitorPort() + Constants.COMMA_SEPERATOR
				+ device.getStatusPort() + Constants.COMMA_SEPERATOR + Constants.SINGLE_QUOTES + script.getId()
				+ Constants.SINGLE_QUOTES + Constants.COMMA_SEPERATOR + Constants.SINGLE_QUOTES + device.getId()
				+ Constants.SINGLE_QUOTES + Constants.COMMA_SEPERATOR + Constants.SINGLE_QUOTES + false
				+ Constants.SINGLE_QUOTES + Constants.COMMA_SEPERATOR + Constants.SINGLE_QUOTES + false
				+ Constants.SINGLE_QUOTES + Constants.COMMA_SEPERATOR + Constants.SINGLE_QUOTES + false
				+ Constants.SINGLE_QUOTES + Constants.COMMA_SEPERATOR;
	}

	/**
	 * This method is used to delete the temporary file
	 * 
	 * @param deleteFilePath
	 */
	private void deleteTemporaryFile(String deleteFilePath) {
		LOGGER.info("Deleting temporary file: " + deleteFilePath);
		boolean isDeleted = commonService.deleteFile(deleteFilePath);
		if (!isDeleted) {
			LOGGER.error("Failed to delete  temporaryfile: " + deleteFilePath);
		} else {
			LOGGER.info("Temporary file deleted successfully: " + deleteFilePath);

		}
	}

	/**
	 * This method is used to modify the content of the file by replacing the
	 * placeholders with the actual values
	 * 
	 * @param content
	 * @param replacements
	 * @return String
	 */
	private String modifyContent(String content, Map<String, String> replacements) {
		for (Map.Entry<String, String> entry : replacements.entrySet()) {
			content = content.replace(entry.getKey(), entry.getValue());
		}
		return content;
	}

	/**
	 * This method is used to read the content of a file
	 * 
	 * @param filePath
	 * @return String
	 * @throws IOException
	 */
	private String readFile(String filePath) throws IOException {
		// Check if the file exists
		File file = new File(filePath);
		if (!file.exists()) {
			LOGGER.error("File does not exist at path: " + filePath);
		}
		StringBuilder contentBuilder = new StringBuilder();

		BufferedReader br = new BufferedReader(new FileReader(filePath));
		String line;
		while ((line = br.readLine()) != null) {
			contentBuilder.append(line).append("\n");
		}

		return contentBuilder.toString();
	}

	/**
	 * This method is used to write content to a file
	 * 
	 * @param filePath
	 * @param content
	 * @throws IOException
	 */
	private void writeFile(String filePath, String content) throws IOException {
		try (BufferedWriter bw = new BufferedWriter(new FileWriter(filePath))) {
			bw.write(content);
		}

	}

	/**
	 * This method is used to compute the time difference between two time stamps
	 * 
	 * @param currentTimeMillisBeforeExecution
	 * @param currentTimeMillisAfterExecution
	 * @return double
	 */
	private double computeTimeDifference(double currentTimeMillisBeforeExecution,
			double currentTimeMillisAfterExecution) {
		double differenceInMinutes = (currentTimeMillisAfterExecution - currentTimeMillisBeforeExecution) / (1000 * 60);
		return Math.round(differenceInMinutes * 1000.0) / 1000.0;
	}

	/**
	 * This method is used to round off the time to three decimal places
	 * 
	 * @param time
	 * @return double
	 */
	private double roundOfToThreeDecimals(double time) {
		return Math.round(time * 1000.0) / 1000.0;
	}

}
