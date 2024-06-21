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

import java.nio.file.Path;
import java.util.List;

import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.dto.DeviceCreateDTO;
import com.rdkm.tdkservice.dto.DeviceUpdateDTO;
import com.rdkm.tdkservice.dto.DeviceResponseDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsResponse;

public interface IDeviceService {
	/**
	 * This method is used to create a new Device.
	 *
	 * @param deviceDto This is the request object containing the details of the
	 *                  Device to be created.
	 * @return boolean This returns true if the Device was created successfully,
	 *         false otherwise.
	 */
	public boolean createDevice(DeviceCreateDTO deviceDto);

	/**
	 * This method is used to update a Device.
	 *
	 * @param deviceUpdateDTO This is the request object containing the updated
	 *                        details of the Device.
	 * @return Device This returns the updated Device.
	 */
	public DeviceUpdateDTO updateDevice(DeviceUpdateDTO deviceUpdateDTO);

	/**
	 * This method is used to retrieve all Devices.
	 *
	 * @return List<Device> This returns a list of all Devices.
	 */
	public List<DeviceResponseDTO> getAllDeviceDetails();

	/**
	 * This method is used to retrieve all Devices by Category.
	 *
	 * @return List<Device> This returns a list of all Devices.
	 */
	public List<DeviceResponseDTO> getAllDeviceDetailsByCategory(String category);

	/**
	 * This method is used to find a Device by its id.
	 *
	 * @param id This is the id of the Device to be found.
	 * @return Device This returns the found Device.
	 */
	public DeviceResponseDTO findDeviceById(Long id);

	/**
	 * This method is used to delete a Device by its id.
	 *
	 * @param id This is the id of the Device to be deleted.
	 */
	public void deleteDeviceById(Long id);

	/**
	 * This method is get all gateway devices.
	 * 
	 * 
	 * @return List<String> This returns a list of gateway devices.
	 */
	List<String> getGatewayDeviceList(String category);

	/**
	 * This method is used to retrieve all Devices by Category.
	 *
	 * @return List<Device> This returns a list of all Devices.
	 */
	public List<StreamingDetailsResponse> getStreamsForTheDevice(Long id);

	/**
	 * This method is used to parse the Device XML.
	 *
	 * @param file This is the file containing the Device XML.
	 */
	public void parseXMLForDevice(MultipartFile file);

	/**
	 * This method is used to download the Device XML.
	 *
	 * @param stbName This is the stbName of the Device to be downloaded.
	 * @return String This returns the Device XML.
	 */
	public String downloadDeviceXML(String stbName);

	/**
	 * This method is used to download all Devices by Category.
	 *
	 * @param category This is the category of the Devices to be downloaded.
	 * @return String This returns the Device XML.
	 */
	public Path downloadAllDevicesByCategory(String category) throws Exception;

}
