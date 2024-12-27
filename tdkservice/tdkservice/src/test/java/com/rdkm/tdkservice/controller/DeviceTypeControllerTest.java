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
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.rdkm.tdkservice.dto.DeviceTypeCreateDTO;
import com.rdkm.tdkservice.dto.DeviceTypeDTO;
import com.rdkm.tdkservice.service.IDeviceTypeService;

/*
* This class is used to test the DeviceTypeControllerTest class.
* It uses Mockito to mock the service layer and JUnit for the testing framework.
*/
public class DeviceTypeControllerTest {

	@InjectMocks
// The controller that is being tested
	DeviceTypeController deviceTypeController;

	@Mock
// The service that the controller depends on
	IDeviceTypeService deviceTypeService;

	@BeforeEach
	/*
	 * This method is run before each test. It initializes the mocks.
	 */
	public void init() {
		MockitoAnnotations.openMocks(this);
	}

	/*
	 * This test checks if the createDeviceType method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
//	@Test
//	public void createDeviceTypeSuccessfully() {
//		DeviceTypeCreateDTO deviceTypeRequest = new DeviceTypeCreateDTO();
//		when(deviceTypeService.createDeviceType(deviceTypeRequest)).thenReturn(true);
//
//		ResponseEntity<String> response = deviceTypeController.createDeviceType(deviceTypeRequest);
//
//		assertEquals(HttpStatus.CREATED, response.getStatusCode());
//		assertEquals("Device type created succesfully", response.getBody());
//	}

	/*
	 * This test checks if the createDeviceType method in the controller returns an
	 * error response when the service layer operation fails.
	 */
	@Test
	public void createDeviceTypeFailure() {

		DeviceTypeCreateDTO deviceTypeRequest = new DeviceTypeCreateDTO();
		when(deviceTypeService.createDeviceType(deviceTypeRequest)).thenReturn(false);

		ResponseEntity<String> response = deviceTypeController.createDeviceType(deviceTypeRequest);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Error in saving device type data", response.getBody());
	}

	/*
	 * This test checks if the getAllDeviceTypes method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void getAllDeviceTypesSuccessfully() {
		DeviceTypeDTO deviceTypeDTO = new DeviceTypeDTO();
		when(deviceTypeService.getAllDeviceTypes()).thenReturn(Arrays.asList(deviceTypeDTO));

		ResponseEntity<?> response = deviceTypeController.getAllDeviceTypes();

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/*
	 * This test checks if the getAllDeviceTypes method in the controller returns an
	 * error response when the service layer operation fails.
	 */
	@Test
	public void getAllDeviceTypesNotFound() {
		when(deviceTypeService.getAllDeviceTypes()).thenReturn(null);

		ResponseEntity<?> response = deviceTypeController.getAllDeviceTypes();

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No device types found", response.getBody());
	}

	/*
	 * This test checks if the deleteDeviceType method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	public void deleteDeviceTypeSuccessfully() {
		UUID deviceTypeId = UUID.randomUUID(); // Create a sample UUID

		doNothing().when(deviceTypeService).deleteById(any(UUID.class)); // Mock the service to delete by UUID

		ResponseEntity<String> response = deviceTypeController.deleteDeviceType(deviceTypeId); // Call the controller
																								// method

		assertEquals(HttpStatus.OK, response.getStatusCode()); // Assert that the status is OK
		assertEquals("Successfully deleted the device", response.getBody()); // Assert that the response body is as
																				// expected
	}

	/*
	 * This test checks if the findDeviceTypeById method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void findDeviceTypeByIdSuccessfully() {
		UUID deviceTypeId = UUID.randomUUID();
		DeviceTypeDTO deviceTypeDTO = new DeviceTypeDTO();
		when(deviceTypeService.findById(any(UUID.class))).thenReturn(deviceTypeDTO);

		ResponseEntity<DeviceTypeDTO> response = deviceTypeController.findById(deviceTypeId);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(deviceTypeDTO, response.getBody());
	}

	/*
	 * This test checks if the updateDeviceType method in the controller returns an
	 * error response when the service layer operation fails.
	 */
//	@Test
//	public void updateDeviceTypeNotFound() {
//		// UUID deviceTypeId = UUID.randomUUID();
//		DeviceTypeDTO deviceTypeUpdateDTO = new DeviceTypeDTO();
//
//		when(deviceTypeService.updateDeviceType(any(DeviceTypeDTO.class))).thenReturn(null);
//
//		ResponseEntity<?> response = deviceTypeController.updateDeviceType(deviceTypeUpdateDTO);
//
//		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
//		assertEquals("Device type not found", response.getBody());
//	}

	/*
	 * This test checks if the updateDeviceType method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
//	@Test
//	public void updateDeviceTypeSuccessfully() {
//		
//		DeviceTypeDTO deviceTypeUpdateDTO = new DeviceTypeDTO();
//
//		when(deviceTypeService.updateDeviceType(any(DeviceTypeDTO.class))).thenReturn(deviceTypeUpdateDTO);
//		ResponseEntity<?> response = deviceTypeController.updateDeviceType(deviceTypeUpdateDTO);
//
//		assertEquals(HttpStatus.OK, response.getStatusCode());
//	}

	/*
	 * This test checks if the deleteDeviceType method in the controller returns an
	 * error response when the service layer operation fails.
	 */
	@Test
	public void deleteDeviceTypeFailure() {
		UUID deviceTypeId = UUID.randomUUID();
		doThrow(new RuntimeException()).when(deviceTypeService).deleteById(any((UUID.class)));

		assertThrows(RuntimeException.class, () -> deviceTypeController.deleteDeviceType(deviceTypeId));
	}

	/*
	 * This test checks if the getDeviceTypesByCategory method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void getDeviceTypesByCategorySuccessfully() {
		DeviceTypeDTO deviceTypeDTO = new DeviceTypeDTO();
		when(deviceTypeService.getDeviceTypesByCategory(anyString())).thenReturn(Arrays.asList(deviceTypeDTO));

		ResponseEntity<?> response = deviceTypeController.getDeviceTypesByCategory("category");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/*
	 * This test checks if the getDeviceTypesListByCategory method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void getDeviceTypesListByCategorySuccessfully() {
		when(deviceTypeService.getDeviceTypeNameByCategory(anyString()))
				.thenReturn(Arrays.asList("DeviceType1", "DeviceType2"));

		ResponseEntity<?> response = deviceTypeController.getDeviceTypesListByCategory("category");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/*
	 * This test checks if the getOtherDeviceTypesListByCategory method in the
	 * controller returns a successful response when the service layer operation is
	 * successful.
	 */
	@Test
	public void getOtherDeviceTypesListByCategorySuccessfully() {
		List<String> deviceTypes = new ArrayList<>(Arrays.asList("DeviceType1", "DeviceType2", "DeviceType3"));

		when(deviceTypeService.getDeviceTypeNameByCategory(anyString())).thenReturn(deviceTypes);

		ResponseEntity<?> response = deviceTypeController.getOtherDeviceTypesListByCategory("category", "DeviceType1");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/*
	 * This test checks if the getOtherDeviceTypesListByCategory method in the
	 * controller returns an error response when the service layer operation fails.
	 */
	@Test
	public void getOtherDeviceTypesListByCategoryNotFound() {
		when(deviceTypeService.getDeviceTypeNameByCategory(anyString())).thenReturn(Collections.emptyList());

		ResponseEntity<?> response = deviceTypeController.getOtherDeviceTypesListByCategory("category", "DeviceType1");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No device types found", response.getBody());
	}

	/*
	 * This test checks if the getDeviceTypesByCategory method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void getDeviceTypesByCategoryNotFound() {
		when(deviceTypeService.getDeviceTypesByCategory(anyString())).thenReturn(null);

		ResponseEntity<?> response = deviceTypeController.getDeviceTypesByCategory("category");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No device types found", response.getBody());
	}
}
