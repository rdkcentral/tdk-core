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

import com.rdkm.tdkservice.dto.*;
import com.rdkm.tdkservice.enums.TestGroup;
import com.rdkm.tdkservice.model.*;
import com.rdkm.tdkservice.model.Module;
import org.modelmapper.ModelMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.BoxManufacturer;
import com.rdkm.tdkservice.model.BoxType;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.model.RdkVersion;
import com.rdkm.tdkservice.model.ScriptTag;
import com.rdkm.tdkservice.model.SocVendor;
import com.rdkm.tdkservice.model.StreamingDetails;
import com.rdkm.tdkservice.model.User;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.model.UserRole;
import com.rdkm.tdkservice.dto.DeviceResponseDTO;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

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
		return userDTO;
	}

	/**
	 * This method is used to convert the BoxType object to BoxTypeDTO object.
	 * 
	 * @param boxType This is the BoxType object.
	 * @return BoxTypeDTO This returns the BoxTypeDTO object converted from the
	 *         BoxType object.
	 */
	public static BoxTypeDTO convertToBoxTypeDTO(BoxType boxType) {
		modelMapper.typeMap(BoxType.class, BoxTypeDTO.class).addMappings(mapper -> {
			mapper.map(src -> src.getType(), BoxTypeDTO::setType);
			mapper.map(src -> src.getName(), BoxTypeDTO::setBoxTypeName);
			mapper.map(src -> src.getUserGroup().getName(), BoxTypeDTO::setBoxUserGroup);
		});
		BoxTypeDTO boxTypeDTO = modelMapper.map(boxType, BoxTypeDTO.class);
		LOGGER.info("Box Type DTO: {}", boxTypeDTO);
		return boxTypeDTO;
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
	 * This method is used to convert the BoxManufacturer object to
	 * BoxManufacturerDTO object.
	 * 
	 * @param boxManufacturer This is the BoxManufacturer object.
	 * @return BoxManufacturerDTO This returns the BoxManufacturerDTO object
	 *         converted from the BoxManufacturer object.
	 */
	public static BoxManufacturerDTO convertToBoxManufacturerDTO(BoxManufacturer boxManufacturer) {
		modelMapper.typeMap(BoxManufacturer.class, BoxManufacturerDTO.class).addMappings(mapper -> {
			mapper.map(src -> src.getUserGroup().getName(), BoxManufacturerDTO::setBoxManufacturerUserGroup);
		});
		BoxManufacturerDTO boxManufacturerDTO = modelMapper.map(boxManufacturer, BoxManufacturerDTO.class);

		LOGGER.info("Box Manufacturer DTO: {}", boxManufacturerDTO);
		return boxManufacturerDTO;
	}

	/**
	 * This method is used to convert the SocVendor object to SocVendorDTO object.
	 * 
	 * @param socVendor This is the SocVendor object.
	 * @return SocVendorDTO This returns the SocVendorDTO object converted from the
	 *         SocVendor object.
	 */

	public static SocVendorDTO convertToSocVendorDTO(SocVendor socVendor) {
		modelMapper.typeMap(SocVendor.class, SocVendorDTO.class).addMappings(mapper -> {
			mapper.map(src -> src.getUserGroup().getName(), SocVendorDTO::setSocVendorUserGroup);
		});
		SocVendorDTO socVendorDTO = modelMapper.map(socVendor, SocVendorDTO.class);
		LOGGER.info("Soc Vendor DTO: {}", socVendorDTO);
		return socVendorDTO;
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
	 * This method is used to convert the StreamingDetails object to
	 * StreamingDetailsDTO object.
	 * 
	 * @param streamingDetails This is the StreamingDetails object.
	 * @return StreamingDetailsDTO This returns the StreamingDetailsDTO object
	 *         converted from the StreamingDetails object.
	 */
	public static StreamingDetailsDTO convertToStreamingDetailsDTO(StreamingDetails streamingDetails) {
		StreamingDetailsDTO streamingDetailsDTO = new StreamingDetailsDTO();
		streamingDetailsDTO.setStreamId(streamingDetails.getId());
		streamingDetailsDTO.setStreamingDetailsId(streamingDetails.getStreamId());
		streamingDetailsDTO.setStreamType(streamingDetails.getStreamType().toString());
		streamingDetailsDTO.setChannelType(
				streamingDetails.getChannelType() != null ? streamingDetails.getChannelType().getName() : null);
		streamingDetailsDTO.setVideoType(
				streamingDetails.getVideoType() != null ? streamingDetails.getVideoType().getName() : null);
		streamingDetailsDTO.setAudioType(
				streamingDetails.getAudioType() != null ? streamingDetails.getAudioType().getName() : null);
		LOGGER.info("Streaming Details DTO: {}", streamingDetails);
		return streamingDetailsDTO;
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
		device.setStbIp(deviceCreateDTO.getStbIp());
		device.setStbName(deviceCreateDTO.getStbName());
		device.setStbPort(deviceCreateDTO.getStbPort());
		device.setStatusPort(deviceCreateDTO.getStatusPort());
		device.setAgentMonitorPort(deviceCreateDTO.getAgentMonitorPort());
		device.setLogTransferPort(deviceCreateDTO.getLogTransferPort());
		device.setMacId(deviceCreateDTO.getMacId());
		// device.setDeviceStatus(deviceCreateDTO.getDevicestatus());
		device.setRecorderId(deviceCreateDTO.getRecorderId());
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
		if (!Utils.isEmpty(deviceUpdateDTO.getStbIp()))
			device.setStbIp(deviceUpdateDTO.getStbIp());
		if (!Utils.isEmpty(deviceUpdateDTO.getStbName()))
			device.setStbName(deviceUpdateDTO.getStbName());
		if (!Utils.isEmpty(deviceUpdateDTO.getStbPort()))
			device.setStbPort(deviceUpdateDTO.getStbPort());
		if (!Utils.isEmpty(deviceUpdateDTO.getStatusPort()))
			device.setStatusPort(deviceUpdateDTO.getStatusPort());
		if (!Utils.isEmpty(deviceUpdateDTO.getAgentMonitorPort()))
			device.setAgentMonitorPort(deviceUpdateDTO.getAgentMonitorPort());
		if (!Utils.isEmpty(deviceUpdateDTO.getLogTransferPort()))
			device.setLogTransferPort(deviceUpdateDTO.getLogTransferPort());
		if (!Utils.isEmpty(deviceUpdateDTO.getMacId()))
			device.setMacId(deviceUpdateDTO.getMacId());
		if (!Utils.isEmpty(deviceUpdateDTO.getRecorderId()))
			device.setRecorderId(deviceUpdateDTO.getRecorderId());
		if (!Utils.isEmpty(deviceUpdateDTO.getGatewayDeviceName()))
			device.setGatewayIp(deviceUpdateDTO.getGatewayDeviceName());
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
		// set box type for update case

	}

	/**
	 * This method is used to convert the BoxType object to BoxTypeDTO object.
	 * 
	 * @param boxType This is the BoxType object.
	 * @return BoxTypeDTO This returns the BoxTypeDTO object converted from the
	 *         BoxType object.
	 */
	public static BoxTypeUpdateDTO convertToBoxTypeUpdateDTO(BoxType boxType) {
		BoxTypeUpdateDTO boxTypeUpdateDTO = new BoxTypeUpdateDTO();
		boxTypeUpdateDTO.setBoxTypeName(boxType.getName());
		boxTypeUpdateDTO.setBoxType(boxType.getType().getName());
		boxTypeUpdateDTO.setBoxTypeCategory(boxType.getCategory().name());
		LOGGER.info("Box type Update DTO: {}", boxTypeUpdateDTO);
		return boxTypeUpdateDTO;
	}

	/**
	 * This method is used to convert the BoxManufacturer object to
	 * BoxManufacturerUpdateDTO object.
	 * 
	 * @param boxManufacturer This is the BoxManufacturer object.
	 * @return BoxManufacturerUpdateDTO This returns the BoxManufacturerDTO object
	 *         converted from the BoxManufacturer object.
	 */
	public static BoxManufacturerUpdateDTO convertToBoxManufacturerUpdateDTO(BoxManufacturer boxManufacturer) {
		BoxManufacturerUpdateDTO boxManufacturerUpdateDTO = new BoxManufacturerUpdateDTO();
		boxManufacturerUpdateDTO.setBoxManufacturerName(boxManufacturer.getName());
		boxManufacturerUpdateDTO.setBoxManufacturerCategory(boxManufacturer.getCategory().name());
		LOGGER.info("Box Manufacturer Update DTO: {}", boxManufacturer);
		return boxManufacturerUpdateDTO;
	}

	// update the socvendorUpdate
	/**
	 * This method is used to convert the SocVendor object to SocVendorDTO object.
	 * 
	 * @param socVendor This is the SocVendor object.
	 * @return SocVendorDTO This returns the SocVendorDTO object converted from the
	 *         SocVendor object.
	 */
	public static SocVendorUpdateDTO convertToSocVendorUpdateDTO(SocVendor socVendor) {
		SocVendorUpdateDTO socVendorUpdateDTO = new SocVendorUpdateDTO();
		socVendorUpdateDTO.setSocVendorName(socVendor.getName());
		socVendorUpdateDTO.setSocVendorCategory(socVendor.getCategory().name());
		LOGGER.info("Soc Vendor Update DTO: {}", socVendor);
		return socVendorUpdateDTO;

	}

	/**
	 * This method is used to convert the Device object to DeviceDTO object.
	 *
	 * @param device This is the Device object.
	 * @return DeviceDTO This returns the DeviceDTO object converted from the Device
	 *         object.
	 */
	public static DeviceResponseDTO convertToDeviceDTO(Device device) {
		ModelMapper modelMapper = new ModelMapper();
		DeviceResponseDTO deviceDTO = modelMapper.map(device, DeviceResponseDTO.class);
		return deviceDTO;
	}

	/**
	 * This method is used to convert the StreamingDetails object to
	 * StreamingDetailsUpdateDTO object.
	 * 
	 * @param streamingDetails This is the StreamingDetails object.
	 * @return StreamingDetailsUpdateDTO This returns the StreamingDetailsUpdateDTO
	 *         object converted from the StreamingDetails object.
	 */

	public static StreamingDetailsUpdateDTO streamingDetailsUpdate(StreamingDetails streamingDetails) {
		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamId(streamingDetails.getStreamId());
		streamingDetailsUpdateDTO.setChannelType(
				streamingDetails.getChannelType() != null ? streamingDetails.getChannelType().getName() : null);
		streamingDetailsUpdateDTO.setVideoType(
				streamingDetails.getVideoType() != null ? streamingDetails.getVideoType().getName() : null);
		streamingDetailsUpdateDTO.setAudioType(
				streamingDetails.getAudioType() != null ? streamingDetails.getAudioType().getName() : null);
		LOGGER.info("Streaming Details Update DTO: {}", streamingDetailsUpdateDTO);
		return streamingDetailsUpdateDTO;

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
		module.setAdvanced(dto.isModuleAdvanced());
		module.setThunderEnabled(dto.isModuleThunderEnabled());
		return module;
	}

	/**
	 * This method is used to convert the ScriptTag object to ScriptTagDTO object.
	 * 
	 * @param scriptTag This is the ScriptTag object.
	 * @return ScriptTagDTO This returns the ScriptTagDTO object converted from the
	 *         ScriptTag object.
	 */
	public static ScriptTagDTO convertToScriptTagDTO(ScriptTag scriptTag) {
		ScriptTagDTO scriptTagDTO = new ScriptTagDTO();
		scriptTagDTO.setScriptTagId(scriptTag.getId());
		scriptTagDTO.setScriptTagName(scriptTag.getName());
		scriptTagDTO.setScriptTagCategory(scriptTag.getCategory().name());
		scriptTagDTO
				.setScriptTagUserGroup(scriptTag.getUserGroup() != null ? scriptTag.getUserGroup().getName() : null);
		LOGGER.info("Script Tag DTO: {}", scriptTagDTO);
		return scriptTagDTO;
	}

	/**
	 * This method is used to convert the RdkVersion object to RdkVersionDTO object.
	 * 
	 * @param rdkVersion This is the RdkVersion object.
	 * @return RdkVersionDTO This returns the RdkVersionDTO object converted from
	 *         the RdkVersion object.
	 */
	public static RdkVersionDTO convertToRdkVersionDTO(RdkVersion rdkVersion) {
		RdkVersionDTO rdkVersionDTO = new RdkVersionDTO();
		rdkVersionDTO.setRdkVersionId(rdkVersion.getId());
		rdkVersionDTO.setBuildVersionName(rdkVersion.getName());
		rdkVersionDTO.setRdkVersionCategory(rdkVersion.getCategory().name());
		rdkVersionDTO
				.setRdkVersionUserGroup(rdkVersion.getUserGroup() != null ? rdkVersion.getUserGroup().getName() : null);
		LOGGER.info("Rdk Version DTO: {}", rdkVersionDTO);
		return rdkVersionDTO;
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
		if (moduleDTO.getModuleCategory() != null && !moduleDTO.getModuleCategory().isEmpty()) {
			Category category = Category.valueOf(moduleDTO.getModuleCategory());
			module.setCategory(category);
		}
		module.setThunderEnabled(moduleDTO.isModuleThunderEnabled());
		module.setAdvanced(moduleDTO.isModuleAdvanced());
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
		moduleDTO.setModuleThunderEnabled(module.isThunderEnabled());
		moduleDTO.setModuleAdvanced(module.isAdvanced());
		moduleDTO.setModuleCategory(module.getCategory() != null ? module.getCategory().name() : null);
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
	 * @param function This is the Function object.
	 * @return FunctionDTO This returns the FunctionDTO object converted from the
	 *         Function object.
	 */

	public static List<PrimitiveTestParameterDTO> convertPrimitiveTestParameterToDTO(
			List<PrimitiveTestParameter> primitiveTestParameters) {
		LOGGER.info("Converting primitive test parameters to DTO");
		List<PrimitiveTestParameterDTO> primitiveTestParameterDTOs = new ArrayList<>();
		for (PrimitiveTestParameter primitiveTestParameter : primitiveTestParameters) {
			PrimitiveTestParameterDTO primitiveTestParameterDTO = new PrimitiveTestParameterDTO();
			primitiveTestParameterDTO.setParameterName(primitiveTestParameter.getParameter().getName());
			primitiveTestParameterDTO.setParameterValue(primitiveTestParameter.getValue());
			primitiveTestParameterDTO.setParameterrangevalue(primitiveTestParameter.getParameter().getRangeVal());
			primitiveTestParameterDTO
					.setParameterType(primitiveTestParameter.getParameter().getParameterDataType().toString());
			primitiveTestParameterDTOs.add(primitiveTestParameterDTO);
		}
		LOGGER.info("Primitive test parameters converted to DTO:" + primitiveTestParameterDTOs.toString());
		return primitiveTestParameterDTOs;
	}
}
