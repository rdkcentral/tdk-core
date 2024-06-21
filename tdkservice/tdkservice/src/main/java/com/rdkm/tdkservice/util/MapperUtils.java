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

import org.modelmapper.ModelMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.rdkm.tdkservice.dto.BoxManufacturerDTO;
import com.rdkm.tdkservice.dto.BoxManufacturerUpdateDTO;
import com.rdkm.tdkservice.dto.BoxTypeDTO;
import com.rdkm.tdkservice.dto.BoxTypeUpdateDTO;
import com.rdkm.tdkservice.dto.DeviceCreateDTO;
import com.rdkm.tdkservice.dto.DeviceUpdateDTO;
import com.rdkm.tdkservice.dto.SocVendorDTO;
import com.rdkm.tdkservice.dto.SocVendorUpdateDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsUpdateDTO;
import com.rdkm.tdkservice.dto.UserDTO;
import com.rdkm.tdkservice.dto.UserGroupDTO;
import com.rdkm.tdkservice.dto.UserRoleDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.BoxManufacturer;
import com.rdkm.tdkservice.model.BoxType;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.model.SocVendor;
import com.rdkm.tdkservice.model.StreamingDetails;
import com.rdkm.tdkservice.model.User;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.model.UserRole;
import com.rdkm.tdkservice.dto.DeviceResponseDTO;

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

}
