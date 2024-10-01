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

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockMultipartFile;

import com.rdkm.tdkservice.dto.DeviceConfigDownloadDTO;
import com.rdkm.tdkservice.dto.DeviceCreateDTO;
import com.rdkm.tdkservice.dto.DeviceResponseDTO;
import com.rdkm.tdkservice.dto.DeviceUpdateDTO;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.service.IDeviceConfigService;
import com.rdkm.tdkservice.service.IDeviceService;
/**
 * This class is used to test the DeviceController class.
 * It uses Mockito to mock the service layer and JUnit for the testing framework.
 */
public class DeviceControllerTest {

	@InjectMocks
	private DeviceController deviceController;

	@Mock
	private IDeviceService deviceService;

	@Mock
	private IDeviceConfigService deviceConfigService;

	/*
	 * This method is run before each test. It initializes the mocks.
	 */
	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	@BeforeEach
	/*
	 * This method is run before each test. It initializes the mocks.
	 */
	public void init() {
		MockitoAnnotations.openMocks(this);
	}

	/*
	 * This test checks if the createDevice method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void testCreateDevice() {
		DeviceCreateDTO deviceDTO = new DeviceCreateDTO();
		// populate deviceDTO with test data

		when(deviceService.createDevice(deviceDTO)).thenReturn(true);

		ResponseEntity<String> response = deviceController.createDevice(deviceDTO);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
		assertEquals("Device created successfully", response.getBody());
	}

	/*
	 * This test checks if the createDevice method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void createDeviceFailure() {
		DeviceCreateDTO deviceDTO = new DeviceCreateDTO();
		when(deviceService.createDevice(deviceDTO)).thenReturn(false);
		ResponseEntity<String> response = deviceController.createDevice(deviceDTO);
		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
	}

	/*
	 * This test checks if the deleteDevice method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	void testDeleteDevice_NotFound() {
		Integer deviceId = 1;
		doThrow(new ResourceNotFoundException("Device", deviceId.toString())).when(deviceService)
				.deleteDeviceById(deviceId);

		ResponseEntity<String> response = deviceController.deleteDeviceById(deviceId);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Failed to delete device:  Device - '1' doesnt exist", response.getBody());
		verify(deviceService).deleteDeviceById(deviceId);
	}

	/*
	 * This test checks if the deleteDevice method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	void testDeleteDevice_Success() {
		Integer deviceId = 1;
		doNothing().when(deviceService).deleteDeviceById(deviceId);

		ResponseEntity<String> response = deviceController.deleteDeviceById(deviceId);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Device deleted successfully", response.getBody());
		verify(deviceService).deleteDeviceById(deviceId);
	}

	/*
	 * This test checks if the deleteDevice method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	void testDeleteDevice_Failure() {
		Integer deviceId = 1;
		doThrow(new RuntimeException("Failed to delete device")).when(deviceService).deleteDeviceById(deviceId);

		ResponseEntity<String> response = deviceController.deleteDeviceById(deviceId);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Failed to delete device: Failed to delete device", response.getBody());
		verify(deviceService).deleteDeviceById(deviceId);
	}

	/*
	 * This test checks if the updateDevice method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void testUpdateDevice() {
		DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
		// populate deviceUpdateDTO with test data

		ResponseEntity<String> response = deviceController.updateDevice(deviceUpdateDTO);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Device updated successfully", response.getBody());
	}

	/*
	 * This test checks if the updateDevice method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void testGetAllDevices() {
		when(deviceService.getAllDeviceDetails()).thenReturn(Collections.emptyList());

		ResponseEntity<?> response = deviceController.getAllDevices();

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(Collections.emptyList(), response.getBody());
	}

	/*
	 * This test checks if the getAllDevicesByCategory method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void testGetAllDevicesByCategory() {
		String category = "testCategory";

		when(deviceService.getAllDeviceDetailsByCategory(category)).thenReturn(Collections.emptyList());

		ResponseEntity<?> response = deviceController.getAllDevicesByCategory(category);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(Collections.emptyList(), response.getBody());
	}

	/*
	 * This test checks if the getAllDevicesByCategory method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void testGetDeviceById() {
		Integer id = 1;
		DeviceResponseDTO device = new DeviceResponseDTO();
		device.setId(id);
		device.setStbName("TestDevice");
		device.setMacId("00:11:22:33:44:55");
		// create a device object with test data

		when(deviceService.findDeviceById(id)).thenReturn(device);

		ResponseEntity<?> response = deviceController.getDeviceById(id);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(device, response.getBody());
	}

	/*
	 * This test checks if the getDeviceById method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void testDeleteDeviceById() {
		Integer id = 1;

		// when(deviceService.deleteDeviceById(id)).thenReturn(true);
		ResponseEntity<String> response = deviceController.deleteDeviceById(id);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Device deleted successfully", response.getBody());
	}

	/*
	 * This test checks if the downloadDeviceConfigFile method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	void testDownloadFile_Success() {
		// Setup
		DeviceConfigDownloadDTO request = new DeviceConfigDownloadDTO();
		request.setDeviceType("CLIENT");
		request.setDeviceTypeName("test");
		Resource mockResource = mock(Resource.class);
		when(mockResource.getFilename()).thenReturn("configFile.txt");

		// Mocking service call to return the mockResource
		when(deviceConfigService.getDeviceConfigFile("test", "GATEWAY")).thenReturn(mockResource);

		// Execute the controller method
		ResponseEntity<Resource> response = deviceController.downloadDeviceConfigFile(request.getDeviceTypeName(),
				request.getDeviceType());

		// Assert the response status and header
		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("attachment; filename=\"configFile.txt\"",
				response.getHeaders().getFirst(HttpHeaders.CONTENT_DISPOSITION));

		// Verify service method was called with correct parameters
		verify(deviceConfigService).getDeviceConfigFile("test", "GATEWAY");
	}

	/*
	 * This test checks if the downloadDeviceConfigFile method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	void testDownloadFile_NotFound() {
		DeviceConfigDownloadDTO request = new DeviceConfigDownloadDTO();
		request.setDeviceType("DeviceType");
		request.setDeviceTypeName("DeviceTypeName");

		when(deviceConfigService.getDeviceConfigFile(anyString(), anyString())).thenReturn(null);

		ResponseEntity<Resource> response = deviceController.downloadDeviceConfigFile(request.getDeviceTypeName(),
				request.getDeviceType());

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		verify(deviceConfigService).getDeviceConfigFile("DeviceType", "DeviceTypeName");
	}

	/*
	 * This test checks if the uploadFile method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	void testUploadFile_Success() {
		MockMultipartFile file = new MockMultipartFile("uploadFile", "configFile.txt", "text/plain",
				"some xml".getBytes());
		when(deviceConfigService.uploadDeviceConfigFile(any())).thenReturn(true);

		ResponseEntity<String> response = deviceController.uploadFile(file);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("File upload is succesful", response.getBody());
		verify(deviceConfigService).uploadDeviceConfigFile(any());
	}

	/*
	 * This test checks if the uploadFile method in the controller
	 * returns an error response when the file is empty.
	 */
	@Test
	void testUploadFile_EmptyFile() {
		MockMultipartFile file = new MockMultipartFile("uploadFile", "", "text/plain", new byte[0]);

		ResponseEntity<String> response = deviceController.uploadFile(file);

		assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
		assertEquals("Please select a file to upload.", response.getBody());
		verify(deviceConfigService, never()).uploadDeviceConfigFile(any());
	}

	/*
	 * This test checks if the uploadFile method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	void testUploadFile_Failure() {
		MockMultipartFile file = new MockMultipartFile("uploadFile", "configFile.txt", "text/plain",
				"some xml".getBytes());
		when(deviceConfigService.uploadDeviceConfigFile(any())).thenReturn(false);

		ResponseEntity<String> response = deviceController.uploadFile(file);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Could not upload the device config file", response.getBody());
		verify(deviceConfigService).uploadDeviceConfigFile(any());
	}

	/*
	 * This test checks if the deleteDeviceConfigFile method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void testDeleteDeviceConfigFileSuccess() {
		String fileName = "testFile";
		when(deviceConfigService.deleteDeviceConfigFile(fileName)).thenReturn(true);
		ResponseEntity<String> response = deviceController.deleteDeviceConfigFile(fileName);
		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/*
	 * This test checks if the deleteDeviceConfigFile method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void testDeleteDeviceConfigFileFailure() {
		String fileName = "testFile";
		when(deviceConfigService.deleteDeviceConfigFile(fileName)).thenReturn(false);
		ResponseEntity<String> response = deviceController.deleteDeviceConfigFile(fileName);
		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
	}

	/*
	 * This test checks if the downloadDeviceConfigFile method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void testDownloadDeviceConfigFileSuccess() {
		String deviceTypeName = "testDeviceName";
		String deviceType = "testDeviceType";
		Resource resource = mock(Resource.class);
		when(deviceConfigService.getDeviceConfigFile(deviceTypeName, deviceType)).thenReturn(resource);
		ResponseEntity<Resource> response = deviceController.downloadDeviceConfigFile(deviceTypeName, deviceType);
		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/*
	 * This test checks if the downloadDeviceConfigFile method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void testDownloadDeviceConfigFileFailure() {
		String deviceTypeName = "testDeviceName";
		String deviceType = "testDEviceType";
		when(deviceConfigService.getDeviceConfigFile(deviceTypeName, deviceType)).thenReturn(null);
		ResponseEntity<Resource> response = deviceController.downloadDeviceConfigFile(deviceTypeName, deviceType);
		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}

	/*
	 * This test checks if the createDeviceFromXML method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void createDeviceSuccess() {
		DeviceCreateDTO deviceDTO = new DeviceCreateDTO();
		when(deviceService.createDevice(deviceDTO)).thenReturn(true);
		ResponseEntity<String> response = deviceController.createDevice(deviceDTO);
		assertEquals(HttpStatus.CREATED, response.getStatusCode());
	}
	/*
	 * This test checks if the createDevice method in the controller returns an
	 * error response when the service layer operation fails.
	 */
	@Test
	@DisplayName("Should return OK when getAllDevices is successful")
	public void getAllDevicesSuccess() {
		when(deviceService.getAllDeviceDetails()).thenReturn(new ArrayList<>());
		ResponseEntity<?> response = deviceController.getAllDevices();
		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/*
	 * This test checks if the getAllDevices method in the controller returns an
	 * error response when the service layer operation fails.
	 */
	@Test
	@DisplayName("Should return OK when downloadDeviceConfigFile is successful")
	public void downloadDeviceConfigFileSuccess() {
		String deviceTypeName = "testDeviceName";
		String deviceType = "testDeviceType";
		Resource resource = mock(Resource.class);
		when(deviceConfigService.getDeviceConfigFile(deviceTypeName, deviceType)).thenReturn(resource);
		ResponseEntity<Resource> response = deviceController.downloadDeviceConfigFile(deviceTypeName, deviceType);
		assertEquals(HttpStatus.OK, response.getStatusCode());
	}
	/*
	 * This test checks if the downloadDeviceConfigFile method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	@DisplayName("Should return NOT_FOUND when downloadDeviceConfigFile fails")
	public void downloadDeviceConfigFileFailure() {
		String deviceTypeName = "testDeviceName";
		String deviceType = "testDeviceType";
		when(deviceConfigService.getDeviceConfigFile(deviceTypeName, deviceType)).thenReturn(null);
		ResponseEntity<Resource> response = deviceController.downloadDeviceConfigFile(deviceTypeName, deviceType);
		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}
	/*
	 * This test checks if the uploadFile method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void testCreateDeviceFromXML() throws Exception {
		MockMultipartFile file = new MockMultipartFile("file", "test.xml", "text/xml", "<xml></xml>".getBytes());

		doNothing().when(deviceService).parseXMLForDevice(any());

		ResponseEntity<String> response = deviceController.createDeviceFromXML(file);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
		assertEquals("Device created successfully from XML data", response.getBody());

		verify(deviceService, times(1)).parseXMLForDevice(any());
	}
	/*
	 * This test checks if the downloadXML method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	@DisplayName("Should return OK when downloadXML is successful")
	public void downloadXMLSuccess() {
		String deviceName = "testDevice";
		String xmlContent = "<xml>Test</xml>";
		when(deviceService.downloadDeviceXML(deviceName)).thenReturn(xmlContent);
		ResponseEntity<String> response = deviceController.downloadXML(deviceName);
		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(xmlContent, response.getBody());
	}
	/*
	 * This test checks if the downloadXML method in the controller returns an error
	 * response when the service layer operation fails.
	 */
	@Test
	public void testGetAllDevicesException() {
		when(deviceService.getAllDeviceDetails()).thenThrow(new RuntimeException("Test exception"));

		ResponseEntity<?> response = deviceController.getAllDevices();
		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());

	}
	/*
	 * This test checks if the getAllDevicesByCategory method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void testGetAllDevicesByCategoryException() {
		String category = "testCategory";
		when(deviceService.getAllDeviceDetailsByCategory(category)).thenThrow(new RuntimeException("Test exception"));

		ResponseEntity<?> response = deviceController.getAllDevicesByCategory(category);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
	}
}
