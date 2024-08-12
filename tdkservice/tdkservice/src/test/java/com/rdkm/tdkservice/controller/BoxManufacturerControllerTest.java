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
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;

import java.util.Arrays;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.rdkm.tdkservice.dto.BoxManufacturerDTO;
import com.rdkm.tdkservice.dto.BoxManufacturerUpdateDTO;
import com.rdkm.tdkservice.service.IBoxManufacturerService;

/*
* This class is used to test the BoxManufacturerController class.
* It uses Mockito to mock the service layer and JUnit for the testing framework.
*/
public class BoxManufacturerControllerTest {

	@InjectMocks
	// The controller that is being tested
	private BoxManufacturerController boxManufacturerController;

	@Mock
	// The service that the controller depends on
	private IBoxManufacturerService boxManufacturerService;

	@BeforeEach
	/*
	 * This method is run before each test. It initializes the mocks.
	 */
	public void init() {
		MockitoAnnotations.openMocks(this);
	}

	
	/*
	 * This test checks if the createBoxManufacturerType method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void createBoxManufacturerType_success() {
		BoxManufacturerDTO boxManufacturerDTO = new BoxManufacturerDTO();
		when(boxManufacturerService.createBoxManufacturer(any(BoxManufacturerDTO.class))).thenReturn(true);

		ResponseEntity<String> response = boxManufacturerController.createBoxManufacturerType(boxManufacturerDTO);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
		assertEquals("Box manufacturer created succesfully", response.getBody());
	}

	
	/*
	 * This test checks if the createBoxManufacturerType method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void createBoxManufacturerType_failure() {
		BoxManufacturerDTO boxManufacturerDTO = new BoxManufacturerDTO();
		when(boxManufacturerService.createBoxManufacturer(any(BoxManufacturerDTO.class))).thenReturn(false);

		ResponseEntity<String> response = boxManufacturerController.createBoxManufacturerType(boxManufacturerDTO);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Error in saving box manufacturer type data", response.getBody());
	}

	
	/*
	 * This test checks if the findAllBoxManufacturerTypes method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void findAllBoxManufacturerTypes_found() {
		when(boxManufacturerService.getAllBoxManufacturer()).thenReturn(Arrays.asList(new BoxManufacturerDTO()));

		ResponseEntity<?> response = boxManufacturerController.findAllBoxManufacturerTypes();

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	
	/*
	 * This test checks if the findAllBoxManufacturerTypes method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void findAllBoxManufacturerTypes_notFound() {
		when(boxManufacturerService.getAllBoxManufacturer()).thenReturn(Arrays.asList());

		ResponseEntity<?> response = boxManufacturerController.findAllBoxManufacturerTypes();

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}

	
	/*
	 * This test checks if the deleteBoxManufacturerType method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void deleteBoxManufacturerType() {
		doNothing().when(boxManufacturerService).deleteBoxManufacturer(anyInt());

		ResponseEntity<String> response = boxManufacturerController.deleteBoxManufacturerType(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Succesfully deleted the box manufacturer", response.getBody());
	}

	
	/*
	 * This test checks if the findById method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void findById_found() {
		BoxManufacturerDTO boxManufacturerDTO = new BoxManufacturerDTO();
		when(boxManufacturerService.findById(anyInt())).thenReturn(boxManufacturerDTO);

		ResponseEntity<BoxManufacturerDTO> response = boxManufacturerController.findById(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(boxManufacturerDTO, response.getBody());
	}

	
	/*
	 * This test checks if the updateBoxManufacturer method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void updateBoxManufacturer_success() {
		BoxManufacturerUpdateDTO boxManufacturerUpdateDTO = new BoxManufacturerUpdateDTO();
		when(boxManufacturerService.updateBoxManufacturer(any(BoxManufacturerUpdateDTO.class), anyInt()))
				.thenReturn(boxManufacturerUpdateDTO);

		ResponseEntity<?> response = boxManufacturerController.updateBoxManufacturer(1, boxManufacturerUpdateDTO);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(boxManufacturerUpdateDTO, response.getBody());
	}

	
	/*
	 * This test checks if the updateBoxManufacturer method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void updateBoxManufacturer_failure() {
		when(boxManufacturerService.updateBoxManufacturer(any(BoxManufacturerUpdateDTO.class), anyInt()))
				.thenReturn(null);

		ResponseEntity<?> response = boxManufacturerController.updateBoxManufacturer(1, new BoxManufacturerUpdateDTO());

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
	}

	
	/*
	 * This test checks if the getBoxManufacturersByCategory method in the
	 * controller returns a successful response when the service layer operation is
	 * successful.
	 */
	@Test
	public void getBoxManufacturersByCategory_found() {
		when(boxManufacturerService.getBoxManufacturersByCategory(anyString()))
				.thenReturn(Arrays.asList(new BoxManufacturerDTO()));

		ResponseEntity<?> response = boxManufacturerController.getBoxManufacturersByCategory("category");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	
	/*
	 * This test checks if the getBoxManufacturersByCategory method in the
	 * controller returns an error response when the service layer operation fails.
	 */
	@Test
	public void getBoxManufacturersByCategory_notFound() {
		when(boxManufacturerService.getBoxManufacturersByCategory(anyString())).thenReturn(Arrays.asList());

		ResponseEntity<?> response = boxManufacturerController.getBoxManufacturersByCategory("category");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}

	@Test
	/*
	 * This test checks if the getBoxmanufacturerListByCategory method in the
	 * controller returns a successful response when the service layer operation is
	 * successful.
	 */
	public void getBoxmanufacturerListByCategory_found() {
		when(boxManufacturerService.getBoxManufacturerListByCategory(anyString()))
				.thenReturn(Arrays.asList("name1", "name2"));

		ResponseEntity<?> response = boxManufacturerController.getBoxmanufacturerListByCategory("category");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	@Test
	/*
	 * This test checks if the getBoxmanufacturerListByCategory method in the
	 * controller returns an error response when the service layer operation fails.
	 */
	public void getBoxmanufacturerListByCategory_notFound() {
		when(boxManufacturerService.getBoxManufacturerListByCategory(anyString())).thenReturn(Arrays.asList());

		ResponseEntity<?> response = boxManufacturerController.getBoxmanufacturerListByCategory("category");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}
}
