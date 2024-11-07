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
package com.rdkm.tdkservice.util;

import java.util.ArrayList;
import java.util.List;

import org.modelmapper.ModelMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.rdkm.tdkservice.dto.DeviceCreateDTO;
import com.rdkm.tdkservice.dto.DeviceResponseDTO;
import com.rdkm.tdkservice.dto.DeviceTypeDTO;
import com.rdkm.tdkservice.dto.DeviceUpdateDTO;
import com.rdkm.tdkservice.dto.FunctionCreateDTO;
import com.rdkm.tdkservice.dto.FunctionDTO;
import com.rdkm.tdkservice.dto.ModuleCreateDTO;
import com.rdkm.tdkservice.dto.ModuleDTO;
import com.rdkm.tdkservice.dto.OemDTO;
import com.rdkm.tdkservice.dto.ParameterCreateDTO;
import com.rdkm.tdkservice.dto.ParameterDTO;
import com.rdkm.tdkservice.dto.PrimitiveTestParameterDTO;
import com.rdkm.tdkservice.dto.ScriptCreateDTO;
import com.rdkm.tdkservice.dto.ScriptDTO;
import com.rdkm.tdkservice.dto.ScriptListDTO;
import com.rdkm.tdkservice.dto.SocDTO;
import com.rdkm.tdkservice.dto.TestSuiteDTO;
import com.rdkm.tdkservice.dto.UserDTO;
import com.rdkm.tdkservice.dto.UserGroupDTO;
import com.rdkm.tdkservice.dto.UserRoleDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.enums.TestGroup;
import com.rdkm.tdkservice.enums.TestType;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.model.DeviceType;
import com.rdkm.tdkservice.model.Function;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.model.Oem;
import com.rdkm.tdkservice.model.Parameter;
import com.rdkm.tdkservice.model.PrimitiveTestParameter;
import com.rdkm.tdkservice.model.Script;
import com.rdkm.tdkservice.model.ScriptTestSuite;
import com.rdkm.tdkservice.model.Soc;
import com.rdkm.tdkservice.model.TestSuite;
import com.rdkm.tdkservice.model.User;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.model.UserRole;

/**
 * This class is used to populate the DTO objects from the model objects.
 */
public class MapperUtils {

	private static ModelMapper modelMapper = new ModelMapper();

	private static final Logger LOGGER = LoggerFactory.getLogger(MapperUtils.class);

	/**
	 * This method is used to populate the UserDTO object from the User object.
	 * 
	 * @param user This is the User object.
	 * @return UserDTO This returns the UserDTO object populated from the User
	 *         object.
	 */
	public static UserDTO populateUserDTO(User user) {
		if (user == null) {
			return null;
		}
		UserDTO userDTO = new UserDTO();
		userDTO.setUserId(user.getId());
		userDTO.setUserName(user.getUsername());
		userDTO.setPassword(user.getPassword());
		userDTO.setUserEmail(user.getEmail());
		userDTO.setUserDisplayName(user.getDisplayName());
		userDTO.setUserThemeName(user.getTheme() != null ? user.getTheme().name() : null);
		userDTO.setUserGroupName(user.getUserGroup() != null ? user.getUserGroup().getName() : null);
		userDTO.setUserRoleName(user.getUserRole() != null ? user.getUserRole().getName() : null);
		userDTO.setUserStatus(user.getStatus());
		userDTO.setUserCategory(user.getCategory().name());
		return userDTO;
	}

	/**
	 * This method is used to convert the deviceType object to deviceTypeDTO object.
	 * 
	 * @param deviceType This is the deviceType object.
	 * @return deviceType This returns the deviceTypeDTO object converted from the
	 *         deviceType object.
	 */
	public static DeviceTypeDTO convertToDeviceTypeDTO(DeviceType deviceType) {
		DeviceTypeDTO deviceTypeDTO = new DeviceTypeDTO();
		deviceTypeDTO.setDeviceTypeId(deviceType.getId());
		deviceTypeDTO.setDeviceTypeName(deviceType.getName());
		deviceTypeDTO.setDeviceType(deviceType.getType().name());
		deviceTypeDTO.setDeviceTypeCategory(deviceType.getCategory().name());
		LOGGER.info("Device Type DTO: {}", deviceTypeDTO);
		return deviceTypeDTO;
	}

	/**
	 * This method is used to convert the UserGroup object to UserGroupDTO object.
	 * 
	 * @param userGroup This is the UserGroup object.
	 * @return UserGroupDTO This returns the UserGroupDTO object converted from the
	 *         UserGroup object.
	 */
	public static UserGroupDTO convertToUserGroupDTO(UserGroup userGroup) {
		UserGroupDTO userGroupDTO = modelMapper.map(userGroup, UserGroupDTO.class);
		LOGGER.info("User Group DTO: {}", userGroupDTO);
		return userGroupDTO;
	}

	/**
	 * This method is used to convert the oem object to oemDTO object.
	 * 
	 * @param oem This is the oem object.
	 * @return oemDTO This returns the oemDTO object converted from the oem object.
	 */
	public static OemDTO convertToOemDTO(Oem oem) {
		OemDTO oemDTO = modelMapper.map(oem, OemDTO.class);

		LOGGER.info("oem DTO: {}", oemDTO);
		return oemDTO;
	}

	/**
	 * This method is used to convert the SocVendor object to SocVendorDTO object.
	 * 
	 * @param soc This is the SocVendor object.
	 * @return SocVendorDTO This returns the SocVendorDTO object converted from the
	 *         SocVendor object.
	 */

	public static SocDTO convertToSocDTO(Soc soc) {
		SocDTO socDTO = modelMapper.map(soc, SocDTO.class);
		LOGGER.info("Soc DTO: {}", socDTO);
		return socDTO;
	}

	/**
	 * This method is used to convert the UserRole object to UserRoleDTO object.
	 * 
	 * @param userRole This is the UserRole object.
	 * @return UserRoleDTO This returns the UserRoleDTO object converted from the
	 *         UserRole object.
	 */
	public static UserRoleDTO convertToUserRoleDTO(UserRole userRole) {
		UserRoleDTO userRoleDTO = modelMapper.map(userRole, UserRoleDTO.class);
		LOGGER.info("User Role DTO: {}", userRoleDTO);
		return userRoleDTO;
	}

	/**
	 * This method is used to convert the Device object to DeviceDTO object.
	 *
	 * @param deviceCreateDTO This is the Device object.
	 * @return DeviceDTO This returns the DeviceDTO object converted from the Device
	 *         object.
	 */

	public static Device populateDeviceDTO(DeviceCreateDTO deviceCreateDTO) {

		Device device = new Device();
		device.setIp(deviceCreateDTO.getDeviceIp());
		device.setName(deviceCreateDTO.getDeviceName());
		device.setPort(deviceCreateDTO.getDevicePort());
		device.setStatusPort(deviceCreateDTO.getStatusPort());
		device.setAgentMonitorPort(deviceCreateDTO.getAgentMonitorPort());
		device.setLogTransferPort(deviceCreateDTO.getLogTransferPort());
		device.setMacId(deviceCreateDTO.getMacId());
		// device.setDeviceStatus(deviceCreateDTO.getDevicestatus());
		device.setThunderPort(deviceCreateDTO.getThunderPort());
		device.setThunderEnabled(deviceCreateDTO.isThunderEnabled());
		// isDevicePortsConfigured
		device.setDevicePortsConfigured(deviceCreateDTO.isDevicePortsConfigured());

		return device;
	}

	/**
	 * This method is used to convert the Device object to UpdateDeviceDTO object.
	 *
	 * @param device This is the Device object.
	 * @return DeviceDTO This returns the DeviceDTO object converted from the Device
	 *         object.
	 */
	public static void updateDeviceProperties(Device device, DeviceUpdateDTO deviceUpdateDTO) {
		if (!Utils.isEmpty(deviceUpdateDTO.getDevicePort()))
			device.setPort(deviceUpdateDTO.getDevicePort());
		if (!Utils.isEmpty(deviceUpdateDTO.getStatusPort()))
			device.setStatusPort(deviceUpdateDTO.getStatusPort());
		if (!Utils.isEmpty(deviceUpdateDTO.getAgentMonitorPort()))
			device.setAgentMonitorPort(deviceUpdateDTO.getAgentMonitorPort());
		if (!Utils.isEmpty(deviceUpdateDTO.getLogTransferPort()))
			device.setLogTransferPort(deviceUpdateDTO.getLogTransferPort());
		if (!Utils.isEmpty(deviceUpdateDTO.getThunderPort()))
			device.setThunderPort(deviceUpdateDTO.getThunderPort());
		device.setThunderEnabled(deviceUpdateDTO.isThunderEnabled());
		// isDevicePortsConfigured
		device.setDevicePortsConfigured(deviceUpdateDTO.isDevicePortsConfigured());

		if (!Utils.isEmpty(deviceUpdateDTO.getCategory())) {
			Category category = Category.valueOf(deviceUpdateDTO.getCategory().toUpperCase());
			if (category != null) {
				device.setCategory(category);
			} else {
				throw new ResourceNotFoundException("Category not found", deviceUpdateDTO.getCategory());
			}
		}
		// set device type for update case

	}

	/**
	 * This method is used to convert the deviceType object to deviceTypeUpdateDTO
	 * object.
	 * 
	 * @param deviceType This is the deviceType object.
	 * @return DeviceTypeUpdateDTO This returns the DeviceTypeUpdateDTO object
	 *         converted from the deviceType object.
	 */
	public static DeviceTypeDTO convertToDeviceTypeUpdateDTO(DeviceType deviceType) {
		DeviceTypeDTO deviceTypeUpdateDTO = new DeviceTypeDTO();
		deviceTypeUpdateDTO.setDeviceTypeName(deviceType.getName());
		deviceTypeUpdateDTO.setDeviceType(deviceType.getType().getName());
		deviceTypeUpdateDTO.setDeviceTypeCategory(deviceType.getCategory().name());
		LOGGER.info("device type Update DTO: {}", deviceTypeUpdateDTO);
		return deviceTypeUpdateDTO;
	}

	/**
	 * This method is used to convert the oem object to OemUpdateDTO object.
	 * 
	 * @param oem This is the oem object.
	 * @return OemUpdateDTO This returns the OemDTO object converted from the oem
	 *         object.
	 */
	public static OemDTO convertToOemUpdateDTO(Oem oem) {
		OemDTO oemUpdateDTO = new OemDTO();
		oemUpdateDTO.setOemName(oem.getName());
		oemUpdateDTO.setOemCategory(oem.getCategory().name());
		LOGGER.info("oem Update DTO: {}", oem);
		return oemUpdateDTO;
	}

	/**
	 * This method is used to convert the Soc object to socUpdateDTO object.
	 * 
	 * @param soc This is the SocVendor object.
	 * @return soc This returns the soc object converted from the soc object.
	 */
	public static SocDTO convertToSocUpdateDTO(Soc soc) {
		SocDTO socUpdateDTO = new SocDTO();
		socUpdateDTO.setSocName(soc.getName());
		socUpdateDTO.setSocCategory(soc.getCategory().name());
		LOGGER.info("Soc  Update DTO: {}", soc);
		return socUpdateDTO;

	}

	/**
	 * This method is used to convert the Device object to DeviceDTO object.
	 *
	 * @param device This is the Device object.
	 * @return DeviceDTO This returns the DeviceDTO object converted from the Device
	 *         object.
	 */

	public static DeviceResponseDTO convertToDeviceDTO(Device device) {
		modelMapper.typeMap(Device.class, DeviceResponseDTO.class).addMappings(mapper -> {
			mapper.map(src -> src.getName(), DeviceResponseDTO::setDeviceName);
		});
		return modelMapper.map(device, DeviceResponseDTO.class);
	}

	/**
	 * Converts a ModuleCreateDTO object to a Module entity.
	 *
	 * @param dto       the data transfer object containing the module details
	 * @param userGroup the user group associated with the module
	 * @return the Module entity populated with the details from the DTO
	 */
	public static Module toModuleEntity(ModuleCreateDTO dto, UserGroup userGroup) {
		Module module = new Module();
		module.setName(dto.getModuleName());
		TestGroup testGroup = TestGroup.valueOf(dto.getTestGroup());
		module.setTestGroup(testGroup);
		module.setUserGroup(userGroup);
		module.setExecutionTime(dto.getExecutionTime());
		module.setLogFileNames(dto.getModuleLogFileNames());
		module.setCrashLogFiles(dto.getModuleCrashLogFiles());
		return module;
	}

	/**
	 * This method is used to convert the Module object to ModuleDTO object.
	 *
	 * @param module This is the Module object.
	 * @return ModuleDTO This returns the ModuleDTO object converted from the Module
	 *         object.
	 */
	public static void updateModuleProperties(Module module, ModuleDTO moduleDTO) {
		if (moduleDTO.getExecutionTime() != null)
			module.setExecutionTime(moduleDTO.getExecutionTime());
		if (moduleDTO.getModuleLogFileNames() != null)
			module.setLogFileNames(moduleDTO.getModuleLogFileNames());
		if (moduleDTO.getModuleCrashLogFiles() != null)
			module.setCrashLogFiles(moduleDTO.getModuleCrashLogFiles());
		if (moduleDTO.getTestGroup() != null && !moduleDTO.getTestGroup().isEmpty()) {
			TestGroup testGroup = TestGroup.valueOf(moduleDTO.getTestGroup());
			module.setTestGroup(testGroup);
		}
	}

	/**
	 * Converts a Module entity to a ModuleDTO object.
	 *
	 * @param module the Module entity to be converted
	 * @return the ModuleDTO object populated with the details from the Module
	 *         entity
	 */
	public static ModuleDTO convertToModuleDTO(Module module) {

		ModuleDTO moduleDTO = new ModuleDTO();
		moduleDTO.setId(module.getId());
		moduleDTO.setModuleName(module.getName());
		moduleDTO.setTestGroup(module.getTestGroup() != null ? module.getTestGroup().name() : null);
		moduleDTO.setExecutionTime(module.getExecutionTime());
		moduleDTO.setModuleLogFileNames(module.getLogFileNames());
		moduleDTO.setModuleCrashLogFiles(module.getCrashLogFiles());
		moduleDTO.setModuleCategory(module.getCategory().name());
		return moduleDTO;
	}

	/**
	 * Converts a Function entity to a FunctionDTO object.
	 *
	 * @param function the Function entity to be converted
	 * @return the FunctionDTO object populated with the details from the Function
	 *         entity
	 */
	public static FunctionDTO convertToFunctionDTO(Function function) {
		FunctionDTO functionDTO = new FunctionDTO();
		functionDTO.setId(function.getId());
		functionDTO.setFunctionName(function.getName());
		functionDTO.setModuleName(function.getModule() != null ? function.getModule().getName() : null);
		functionDTO.setFunctionCategory(function.getCategory().name());
		return functionDTO;
	}

	/**
	 * Converts a ParameterType entity to a ParameterTypeDTO object.
	 *
	 * @param parameter the ParameterType entity to be converted
	 * @return the ParameterTypeDTO object populated with the details from the
	 *         ParameterType entity
	 */
	public static ParameterDTO convertToParameterTypeDTO(Parameter parameter) {
		ParameterDTO parameterDTO = new ParameterDTO();
		parameterDTO.setId(parameter.getId());
		parameterDTO.setParameterName(parameter.getName());
		parameterDTO.setParameterDataType(parameter.getParameterDataType());
		parameterDTO.setParameterRangeVal(parameter.getRangeVal());
		parameterDTO.setFunction(parameter.getFunction() != null ? parameter.getFunction().getName() : null);
		return parameterDTO;
	}

	/**
	 * Maps the data from FunctionCreateDTO to Function entity.
	 *
	 * @param function          the function entity to be updated
	 * @param functionCreateDTO the data transfer object containing the function
	 *                          details
	 * @param module            the module entity associated with the function
	 */
	public static void mapCreateDTOToEntity(Function function, FunctionCreateDTO functionCreateDTO, Module module) {
		function.setName(functionCreateDTO.getFunctionName());
		function.setModule(module);
		function.setCategory(Category.valueOf(functionCreateDTO.getFunctionCategory()));
	}

	/**
	 * Maps the data from ParameterTypeCreateDTO to ParameterType entity.
	 *
	 * @param parameter          the parameter type entity to be updated
	 * @param parameterCreateDTO the data transfer object containing the parameter
	 *                           type details
	 * @param function           the function entity associated with the parameter
	 *                           type
	 */
	public static void mapDTOCreateParameterTypeToEntity(Parameter parameter, ParameterCreateDTO parameterCreateDTO,
			Function function) {
		parameter.setName(parameterCreateDTO.getParameterName());
		parameter.setParameterDataType(parameterCreateDTO.getParameterDataType());
		parameter.setRangeVal(parameterCreateDTO.getParameterRangeVal());
		parameter.setFunction(function);
	}

	/**
	 * Maps the data from ParameterTypeDTO to ParameterType entity.
	 *
	 * @param parameter    the parameter type entity to be updated
	 * @param parameterDTO the data transfer object containing the parameter type
	 *                     details
	 */
	public static void mapDTOToEntity(Parameter parameter, ParameterDTO parameterDTO) {
		parameter.setName(parameterDTO.getParameterName());
		parameter.setParameterDataType(parameterDTO.getParameterDataType());
		parameter.setRangeVal(parameterDTO.getParameterRangeVal());
	}

	/**
	 * This method is used to convert the Function object to FunctionDTO object.
	 *
	 * @param primitiveTestParameters This is the Function object.
	 * @return FunctionDTO This returns the FunctionDTO object converted from the
	 *         Function object.
	 */

	public static List<PrimitiveTestParameterDTO> convertPrimitiveTestParameterToDTO(
			List<PrimitiveTestParameter> primitiveTestParameters) {
		LOGGER.info("Converting primitive test parameters to DTO");
		List<PrimitiveTestParameterDTO> primitiveTestParameterDTOs = new ArrayList<>();
		for (PrimitiveTestParameter primitiveTestParameter : primitiveTestParameters) {
			PrimitiveTestParameterDTO primitiveTestParameterDTO = new PrimitiveTestParameterDTO();
			primitiveTestParameterDTO.setParameterName(primitiveTestParameter.getParameterName());
			primitiveTestParameterDTO.setParameterValue(primitiveTestParameter.getParameterValue());
			primitiveTestParameterDTO.setParameterrangevalue(primitiveTestParameter.getParameterRange());
			primitiveTestParameterDTO.setParameterType(primitiveTestParameter.getParameterType().toString());
			primitiveTestParameterDTOs.add(primitiveTestParameterDTO);
		}
		LOGGER.info("Primitive test parameters converted to DTO:" + primitiveTestParameterDTOs.toString());
		return primitiveTestParameterDTOs;
	}

	/**
	 * This method is used to convert the ScriptCreateDTO to Script entity
	 * 
	 * @param scriptCreateDTO ScriptCreateDTO
	 * @return script Script
	 */
	public static Script convertToScriptEntity(ScriptCreateDTO scriptCreateDTO) {
		Script script = new Script();
		LOGGER.info("Converting ScriptDTO to ScriptEntity");
		script.setName(scriptCreateDTO.getName());
		script.setSynopsis(scriptCreateDTO.getSynopsis());
		script.setExecutionTimeOut(scriptCreateDTO.getExecutionTimeOut());
		script.setLongDuration(scriptCreateDTO.isLongDuration());
		script.setSkipExecution(scriptCreateDTO.isSkipExecution());
		if (scriptCreateDTO.isSkipExecution()) {
			script.setSkipRemarks(scriptCreateDTO.getSkipRemarks());
		}

		script.setTestId(scriptCreateDTO.getTestId());
		script.setObjective(scriptCreateDTO.getObjective());
		script.setTestType(TestType.valueOf(scriptCreateDTO.getTestType()));
		script.setApiOrInterfaceUsed(scriptCreateDTO.getApiOrInterfaceUsed());
		script.setInputParameters(scriptCreateDTO.getInputParameters());
		script.setAutomationApproach(scriptCreateDTO.getAutomationApproach());
		script.setExpectedOutput(scriptCreateDTO.getExpectedOutput());
		script.setPriority(scriptCreateDTO.getPriority());
		script.setTestStubInterface(scriptCreateDTO.getTestStubInterface());
		script.setReleaseVersion(scriptCreateDTO.getReleaseVersion());
		script.setPrerequisites(scriptCreateDTO.getPrerequisites());
		script.setRemarks(scriptCreateDTO.getRemarks());
		LOGGER.info("Converting ScriptDTO to ScriptEntity:" + script.toString());
		return script;
	}

	public static Script updateScript(Script script, ScriptDTO scriptUpdateDTO) {
		LOGGER.info("Updating the script entity with the properties available in the script update DTO");

		if (!Utils.isEmpty(scriptUpdateDTO.getSynopsis())) {
			script.setSynopsis(scriptUpdateDTO.getSynopsis());
		}

		script.setExecutionTimeOut(scriptUpdateDTO.getExecutionTimeOut());
		script.setLongDuration(scriptUpdateDTO.isLongDuration());
		script.setSkipExecution(scriptUpdateDTO.isSkipExecution());
		if (scriptUpdateDTO.isSkipExecution()) {
			if (!Utils.isEmpty(scriptUpdateDTO.getSkipRemarks())) {
				script.setSkipRemarks(scriptUpdateDTO.getSkipRemarks());
			}
		}

		// Update the test case documentation details
		if (!Utils.isEmpty(scriptUpdateDTO.getTestId())) {
			script.setTestId(scriptUpdateDTO.getTestId());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getObjective())) {
			script.setObjective(scriptUpdateDTO.getObjective());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getTestType())) {
			script.setTestType(TestType.valueOf(scriptUpdateDTO.getTestType()));
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getApiOrInterfaceUsed())) {
			script.setApiOrInterfaceUsed(scriptUpdateDTO.getApiOrInterfaceUsed());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getInputParameters())) {
			script.setInputParameters(scriptUpdateDTO.getInputParameters());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getPrerequisites())) {
			script.setPrerequisites(scriptUpdateDTO.getPrerequisites());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getAutomationApproach())) {
			script.setAutomationApproach(scriptUpdateDTO.getAutomationApproach());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getExpectedOutput())) {
			script.setExpectedOutput(scriptUpdateDTO.getExpectedOutput());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getPriority())) {
			script.setPriority(scriptUpdateDTO.getPriority());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getTestStubInterface())) {
			script.setTestStubInterface(scriptUpdateDTO.getTestStubInterface());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getRemarks())) {
			script.setRemarks(scriptUpdateDTO.getRemarks());
		}
		if (!Utils.isEmpty(scriptUpdateDTO.getReleaseVersion())) {
			script.setReleaseVersion(scriptUpdateDTO.getReleaseVersion());
		}

		LOGGER.info("Updated the script entity with the properties available in the script update DTO");
		return script;

	}

	/**
	 * This method is used to convert the Script entity to ScriptListDTO
	 * 
	 * @param script Script entity
	 * @return scriptListDTO ScriptListDTO
	 */
	public static ScriptListDTO convertToScriptListDTO(Script script) {
		LOGGER.info("Converting the script entity to script list DTO");
		ScriptListDTO scriptListDTO = new ScriptListDTO();
		scriptListDTO.setId(script.getId());
		scriptListDTO.setName(script.getName());
		LOGGER.info("Converted the script entity to script list DTO:" + scriptListDTO.toString());
		return scriptListDTO;
	}

	/**
	 * This method is used to convert the Script entity to ScriptDTO
	 * 
	 * @param script Script entity
	 * @return scriptDTO ScriptDTO
	 */
	public static ScriptDTO convertToScriptDTO(Script script) {
		LOGGER.info("Converting the script entity to script DTO");
		ScriptDTO scriptDTO = new ScriptDTO();
		scriptDTO.setId(script.getId());

		if (script.getPrimitiveTest() != null) {
			scriptDTO.setPrimitiveTestName(script.getPrimitiveTest().getName());
		}

		scriptDTO.setName(script.getName());
		scriptDTO.setSynopsis(script.getSynopsis());
		scriptDTO.setModuleName(script.getModule().getName());
		scriptDTO.setExecutionTimeOut(script.getExecutionTimeOut());
		scriptDTO.setLongDuration(script.isLongDuration());
		scriptDTO.setSkipExecution(script.isSkipExecution());
		scriptDTO.setSkipRemarks(script.getSkipRemarks());
		scriptDTO.setTestId(script.getTestId());
		scriptDTO.setObjective(script.getObjective());
		scriptDTO.setTestType(script.getTestType().name());
		scriptDTO.setApiOrInterfaceUsed(script.getApiOrInterfaceUsed());
		scriptDTO.setInputParameters(script.getInputParameters());
		scriptDTO.setAutomationApproach(script.getAutomationApproach());
		scriptDTO.setExpectedOutput(script.getExpectedOutput());
		scriptDTO.setPriority(script.getPriority());
		scriptDTO.setTestStubInterface(script.getTestStubInterface());
		scriptDTO.setReleaseVersion(script.getReleaseVersion());
		scriptDTO.setPrerequisites(script.getPrerequisites());
		scriptDTO.setRemarks(script.getRemarks());
		LOGGER.info("Converted the script entity to script DTO:" + scriptDTO.toString());
		return scriptDTO;

	}

	/**
	 * This method is used to convert the ScriptTestSuite map list to ScriptListDTO
	 * list
	 * 
	 * @param testSuiteCreateDTO
	 * @return scriptListDTOList ScriptListDTO list
	 */
	public static List<ScriptListDTO> getScriptList(List<ScriptTestSuite> scriptTestSuiteList) {
		List<ScriptListDTO> scriptList = new ArrayList<>();
		for (ScriptTestSuite scriptTestSuite : scriptTestSuiteList) {
			ScriptListDTO scriptListDTO = new ScriptListDTO();
			scriptListDTO.setId(scriptTestSuite.getScript().getId());
			scriptListDTO.setName(scriptTestSuite.getScript().getName());
			scriptList.add(scriptListDTO);
		}
		return scriptList;
	}

	/**
	 * This method is used to convert the TestSuite entity to TestSuiteDTO
	 * 
	 * @param testSuite TestSuite entity
	 * @return testSuite TestSuiteDTO
	 */
	public static TestSuiteDTO convertToTestSuiteDTO(TestSuite testSuite) {
		TestSuiteDTO testSuiteDTO = new TestSuiteDTO();
		testSuiteDTO.setId(testSuite.getId());
		testSuiteDTO.setName(testSuite.getName());
		testSuiteDTO.setDescription(testSuite.getDescription());
		testSuiteDTO.setCategory(testSuite.getCategory().toString());
		return testSuiteDTO;
	}

	/**
	 * This method is used to convert the Script entity to ScriptListDTO
	 * 
	 * @param script Script entity
	 * @return scriptListDTO ScriptListDTO
	 */
	public static List<ScriptListDTO> getScriptListDTOFromScriptList(List<Script> script) {
		LOGGER.info("Converting the script entity to script list DTO");
		List<ScriptListDTO> scriptListDTOList = new ArrayList<>();
		for (Script scriptObj : script) {
			ScriptListDTO scriptListDTO = new ScriptListDTO();
			scriptListDTO.setId(scriptObj.getId());
			scriptListDTO.setName(scriptObj.getName());
			scriptListDTOList.add(scriptListDTO);
		}
		return scriptListDTOList;

	}
}
