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
package com.rdkm.tdkservice.controller;

import static com.rdkm.tdkservice.util.Constants.DEVICE_FILE_EXTENSION_ZIP;
import static com.rdkm.tdkservice.util.Constants.DEVICE_XML_FILE_EXTENSION;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.dto.DeviceCreateDTO;
import com.rdkm.tdkservice.dto.DeviceUpdateDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsResponse;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.service.IDeviceConfigService;
import com.rdkm.tdkservice.service.IDeviceService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;

/**
 * The DeviceController class is a REST controller that handles device-related
 * requests. It provides endpoints for creating, updating, and deleting devices,
 * as well as for fetching device details and streams. This class uses the
 * IDeviceService and IDeviceConfigService to perform the actual business logic.
 *
 */

@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/device")
public class DeviceController {

	@Autowired
	private IDeviceService deviceService;

	@Autowired
	private IDeviceConfigService deviceConfigService;

	private static final Logger LOGGER = LoggerFactory.getLogger(DeviceController.class);

	/**
	 * This method is used to create a new device.
	 *
	 * @param deviceDTO This is the request object containing the details of the
	 *                  device to be created.
	 * @return ResponseEntity<String> This returns the response message.
	 */
	@Operation(summary = "Create a new device details", description = "Creates a new device details in the system.")
	@ApiResponse(responseCode = "201", description = "device details created successfully")
	@ApiResponse(responseCode = "500", description = "Error in saving device details data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping("/create")
	public ResponseEntity<String> createDevice(@RequestBody @Valid DeviceCreateDTO deviceDTO) {
		LOGGER.info("Received create device request: " + deviceDTO.toString());
		boolean isDeviceCreated = deviceService.createDevice(deviceDTO);
		if (isDeviceCreated) {
			LOGGER.info("Device created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Device created successfully");
		} else {
			LOGGER.error("Failed to create device data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to create device");
		}
	}

	/**
	 * This method is used to update a device.
	 *
	 * @param deviceUpdateDTO This is the request object containing the updated
	 *                        details of the device.
	 * @return ResponseEntity<String> This returns the response message.
	 */
	@Operation(summary = "Update device details", description = "Updates the device details in the system.")
	@ApiResponse(responseCode = "200", description = "device details updated successfully")
	@ApiResponse(responseCode = "500", description = "Error in updating device details data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PutMapping("/update")
	public ResponseEntity<String> updateDevice(@RequestBody @Valid DeviceUpdateDTO deviceUpdateDTO) {
		LOGGER.info("Received update device request: " + deviceUpdateDTO.toString());
		try {
			deviceService.updateDevice(deviceUpdateDTO);
			LOGGER.info("Device updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Device updated successfully");
		} catch (Exception e) {
			LOGGER.error("Error in updating device details data", e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to update device: " + e.getMessage());
		}
	}

	/**
	 * This method is used to get all devices.
	 *
	 * @return ResponseEntity<?> This returns the response entity.
	 */
	@Operation(summary = "Get All device details", description = "Get the device details in the system.")
	@ApiResponse(responseCode = "200", description = "device details fetched successfully")
	@ApiResponse(responseCode = "500", description = "Error in fetching device details data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findall")
	public ResponseEntity<?> getAllDevices() {
		LOGGER.info("Received find all devices request");
		try {
			return ResponseEntity.status(HttpStatus.OK).body(deviceService.getAllDeviceDetails());
		} catch (Exception e) {
			LOGGER.error("Error in fetching device details data", e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to fetch device: " + e.getMessage());
		}
	}

	/**
	 * This method is used to get all devices by category.
	 *
	 * @param category This is the category of the devices to be fetched.
	 * @return ResponseEntity<?> This returns the response entity.
	 */
	@Operation(summary = "Get All device details", description = "Get the device details in the system.")
	@ApiResponse(responseCode = "200", description = "device details fetched successfully")
	@ApiResponse(responseCode = "500", description = "Error in fetching device details data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findallbycategory")
	public ResponseEntity<?> getAllDevicesByCategory(@RequestParam String category) {
		LOGGER.info("Received find all devices by category request: " + category);
		try {
			return ResponseEntity.status(HttpStatus.OK)
					.body(deviceService.getAllDeviceDetailsByCategory(category));
		} catch (Exception e) {
			LOGGER.error("Error in fetching device details data:", e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to fetch device: " + e.getMessage());
		}
	}

	/**
	 * This method is used to get device details by id.
	 *
	 * @param id This is the id of the device to be fetched.
	 * @return ResponseEntity<?> This returns the response entity.
	 */
	@Operation(summary = "Get device details by id", description = "Get the device details by id in the system.")
	@ApiResponse(responseCode = "200", description = "device details fetched successfully")
	@ApiResponse(responseCode = "500", description = "Error in fetching device details data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findbyid/{id}")
	public ResponseEntity<?> getDeviceById(@PathVariable Integer id) {
		LOGGER.info("Received find device by id request: " + id);
		try {
			return ResponseEntity.status(HttpStatus.OK).body(deviceService.findDeviceById(id));
		} catch (Exception e) {
			LOGGER.error("Error in fetching device details data", e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to fetch device: " + e.getMessage());
		}
	}

	/**
	 * This method is used to delete a device by its id.
	 *
	 * @param id This is the id of the device to be deleted.
	 * @return ResponseEntity<String> This returns the response message.
	 */
	@Operation(summary = "Delete device details by id", description = "Delete the device details by id in the system.")
	@ApiResponse(responseCode = "200", description = "device details deleted successfully")
	@ApiResponse(responseCode = "500", description = "Error in deleting device details data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@DeleteMapping("/deleteDeviceById/{id}")
	public ResponseEntity<String> deleteDeviceById(@PathVariable Integer id) {
		LOGGER.info("Received delete device request for id: " + id);
		try {
			deviceService.deleteDeviceById(id);
			LOGGER.info("Device deleted successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Device deleted successfully");
		} catch (Exception e) {
			LOGGER.error("Error in deleting device details data", e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to delete device: " + e.getMessage());
		}
	}

	/**
	 * Retrieves all gateway devices in the system.
	 *
	 * @return a ResponseEntity containing the list of gateway devices if found, or
	 *         a ResponseEntity with status NOT_FOUND and a message if no gateway
	 *         devices are found.
	 */
	@Operation(summary = "Get list of gateway devices", description = "Retrieves all gateway devices in the system.")
	@ApiResponse(responseCode = "200", description = "Gateway devices retrieved successfully")
	@ApiResponse(responseCode = "404", description = "No gateway devices found")
	@GetMapping("/getlistofgatewaydevices")
	public ResponseEntity<?> getListOfGateWayDevices(@RequestParam String category) {
		LOGGER.info("Received find box type by category request");
		List<String> gateWayDevice = deviceService.getGatewayDeviceList(category);
		if (null != gateWayDevice && !gateWayDevice.isEmpty()) {
			return ResponseEntity.status(HttpStatus.OK).body(gateWayDevice);
		} else {
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No gateway devices found");
		}
	}

	/**
	 * This method is used to get the streams for a device.
	 *
	 * @param id This is the id of the device for which the streams are to be
	 *           fetched.
	 * @return ResponseEntity<?> This returns the response entity.
	 */
	@Operation(summary = "Get streams for a device", description = "Get the streams for a specific device in the system.")
	@ApiResponse(responseCode = "200", description = "Streams fetched successfully")
	@ApiResponse(responseCode = "500", description = "Error in fetching streams")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/getStreamsForDevice/{id}")
	public ResponseEntity<?> getStreamsForDevice(@PathVariable Integer id) {
		LOGGER.info("Received get streams for device request: " + id);
		try {
			List<StreamingDetailsResponse> streams = deviceService.getStreamsForTheDevice(id);
			LOGGER.info("Streams fetched successfully for device: " + id);
			return ResponseEntity.status(HttpStatus.OK).body(streams);
		} catch (ResourceNotFoundException e) {
			LOGGER.error("No streams found for device: " + id);
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body(e.getMessage());
		} catch (Exception e) {
			LOGGER.error("Error in fetching streams", e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to fetch streams: " + e.getMessage());
		}
	}

	/**
	 * This method is used to upload the XML file for a device.
	 *
	 * @param file This is the XML file to be uploaded.
	 * @return ResponseEntity<String> This returns the response message.
	 */
	@Operation(summary = "Upload device XML File", description = "Upload device XML File.")
	@ApiResponse(responseCode = "200", description = "Device created successfully from XML data")
	@ApiResponse(responseCode = "500", description = "Failed to create device from XML data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping(value = "/uploadDeviceXML")
	public ResponseEntity<String> createDeviceFromXML(@Valid @RequestParam("file") MultipartFile file) {
		LOGGER.info("Received upload device XML request: " + file.getOriginalFilename());
		try {
			deviceService.parseXMLForDevice(file);
			LOGGER.info("Device created successfully from XML data");
			return ResponseEntity.status(HttpStatus.CREATED).body("Device created successfully from XML data");
		} catch (Exception e) {
			LOGGER.error("Failed to create device from XML data", e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to create device from XML data: " + e.getMessage());
		}
	}

	/**
	 * This method is used to download the XML file for a device.
	 *
	 * @param deviceName This is the name of the device for which the XML file is to
	 *                   be downloaded.
	 * @return ResponseEntity<String> This returns the XML content as a response.
	 */

	@Operation(summary = "Download device XML File", description = "Generate device XML File.")
	@ApiResponse(responseCode = "200", description = "Downloaded  Device XMl successfully")
	@ApiResponse(responseCode = "500", description = "Failed to create device from XML data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/downloadXML/{deviceName}")
	public ResponseEntity<String> downloadXML(@PathVariable String deviceName) {
		LOGGER.info("Received download device XML request: " + deviceName);
		String xmlContent = deviceService.downloadDeviceXML(deviceName);
		HttpHeaders headers = new HttpHeaders();
		headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + deviceName + DEVICE_XML_FILE_EXTENSION);
		LOGGER.info("Downloaded  Device XMl successfully");
		return ResponseEntity.ok().headers(headers).body(xmlContent);
	}

	/**
	 * This method is used to download the device configuration file exclusively
	 * for RDKV devices and the related usecases
	 *
	 * @param boxName - the box name
	 * @param boxType - the box type
	 * @return ResponseEntity<Resource> - the response entity - HttpStatus.OK - if
	 *         the file download is successful - HttpStatus.NOT_FOUND - if the file
	 *         is not found
	 *
	 */
	@Operation(summary = "Download device configuration file", description = "Download the device configuration file for a specific device in the system.")
	@ApiResponse(responseCode = "200", description = "Device configuration file downloaded successfully")
	@ApiResponse(responseCode = "500", description = "Internal server error in downloading device configuration file")
	@ApiResponse(responseCode = "400", description = "There is no file associated with the box or boxtype and no default file found.")
	@GetMapping("/downloadDeviceConfigFile")
	public ResponseEntity<Resource> downloadDeviceConfigFile(@RequestParam String boxName,
			@RequestParam String boxType) {
		LOGGER.info("Going to get the device config file " + boxName + " " + boxType);
		Resource resource = deviceConfigService.getDeviceConfigFile(boxName, boxType);
		if (resource == null) {
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
		} else {
			return ResponseEntity.status(HttpStatus.OK)
					.header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + resource.getFilename() + "\"")
					.header("Access-Control-Expose-Headers", "content-disposition").body(resource);
		}

	}

	/**
	 * This method is used to upload the device configuration file exclusively for
	 * RDKV devices and the related usecases
	 * 
	 * @param file - the device configuration file
	 * @return ResponseEntity<String> - the response entity - HttpStatus.OK - if the
	 *         file upload is successful - HttpStatus.BAD_REQUEST - if the file is
	 *         empty - HttpStatus.INTERNAL_SERVER_ERROR - if the file upload is not
	 *         successful
	 * 
	 */
	@Operation(summary = "Upload device configuration file", description = "Upload the device configuration file for a specific device in the system.")
	@ApiResponse(responseCode = "200", description = "Device configuration file uploaded successfully")
	@ApiResponse(responseCode = "500", description = "Internal server error in uploading device configuration file")
	@ApiResponse(responseCode = "400", description = "When the file is empty")
	@PostMapping("/uploadDeviceConfigFile")
	public ResponseEntity<String> uploadFile(@RequestParam("uploadFile") MultipartFile file) {
		LOGGER.info("Received upload device config file request: " + file.getOriginalFilename());
		if (file.isEmpty()) {
			LOGGER.error("Please select a file to upload.");
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Please select a file to upload.");
		}
		boolean isfileUploaded = deviceConfigService.uploadDeviceConfigFile(file);
		if (isfileUploaded) {
			LOGGER.info("File upload is succesful");
			return ResponseEntity.status(HttpStatus.OK).body("File upload is succesful");
		} else {
			LOGGER.error("Could not upload the device config file");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Could not upload the device config file");
		}
	}

	/**
	 * This method is used to delete the device configuration file exclusively for
	 * RDKV devices and the related usecases
	 *
	 * @param deviceConfigFileName - the device configuration file name
	 * @return ResponseEntity<String> - the response entity - HttpStatus.OK - if the
	 *         file deletion is successful - HttpStatus.INTERNAL_SERVER_ERROR - if
	 *         the file deletion is not successful
	 *
	 */
	@Operation(summary = "Delete device configuration file", description = "Delete the device configuration file for a specific device in the system.")
	@ApiResponse(responseCode = "200", description = "Device configuration file deleted successfully")
	@ApiResponse(responseCode = "400", description = "No such file exists")
	@ApiResponse(responseCode = "500", description = "Internal server error in deleting device configuration file")
	@DeleteMapping("/deleteDeviceConfigFile")
	public ResponseEntity<String> deleteDeviceConfigFile(@RequestParam String deviceConfigFileName) {
		LOGGER.info("Received delete device config file request: " + deviceConfigFileName);
		boolean isFileDeleted = deviceConfigService.deleteDeviceConfigFile(deviceConfigFileName);
		if (isFileDeleted) {
			return ResponseEntity.status(HttpStatus.OK).body("File deleted successfully");
		} else {
			LOGGER.error("Could not delete the device config file");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Could not delete the device config file");
		}
	}

	/**
	 * This method is used to download all Devices by Category.
	 *
	 * @param category This is the category of the Devices to be downloaded.
	 * @return ResponseEntity<Resource> This returns the Device XML.
	 */
	@Operation(summary = "Download all devices by category", description = "Download all devices by category to the system")
	@ApiResponse(responseCode = "200", description = "Downloaded successfully.")
	@ApiResponse(responseCode = "500", description = "Internal server error while downloading.")
	@GetMapping("/downloadDevicesByCategory/{category}")
	public ResponseEntity<?> downloadAllDevicesByCategory(@PathVariable String category, HttpServletResponse response) {
		try {
			LOGGER.info("Received download all devices by category request: " + category);
			Path file = deviceService.downloadAllDevicesByCategory(category);

			byte[] fileContent = Files.readAllBytes(file);

			HttpHeaders headers = new HttpHeaders();
			headers.add(HttpHeaders.CONTENT_DISPOSITION,
					"attachment; filename=devices_" + category + DEVICE_FILE_EXTENSION_ZIP);
			LOGGER.info("Downloaded all devices by category successfully");
			return ResponseEntity.ok().headers(headers).body(fileContent);
		} catch (Exception e) {
			LOGGER.error("Error in downloading device details data", e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failed to download device: " + e.getMessage().getBytes());
		}

	}

}
