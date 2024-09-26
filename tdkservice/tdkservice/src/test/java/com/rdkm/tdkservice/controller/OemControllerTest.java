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

import com.rdkm.tdkservice.dto.OemDTO;
import com.rdkm.tdkservice.dto.OemUpdateDTO;
import com.rdkm.tdkservice.service.IOemService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

/*
* This class is used to test the OemControllerTest class.
* It uses Mockito to mock the service layer and JUnit for the testing framework.
*/
public class OemControllerTest {

	@InjectMocks
// The controller that is being tested
	private OemController oemController;

	@Mock
// The service that the controller depends on
	private IOemService oemService;

	@BeforeEach
	/*
	 * This method is run before each test. It initializes the mocks.
	 */
	public void init() {
		MockitoAnnotations.openMocks(this);
	}


	/*
	 * This test checks if the createOem method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void createOem_success() {
		OemDTO oemDTO = new OemDTO();
		when(oemService.createOem(any(OemDTO.class))).thenReturn(true);

		ResponseEntity<String> response = oemController.createOemType(oemDTO);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
		assertEquals("oem created successfully", response.getBody());
	}


	/*
	 * This test checks if the createOem method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void createOem_failure() {
		OemDTO oemDTO = new OemDTO();
		when(oemService.createOem(any(OemDTO.class))).thenReturn(false);

		ResponseEntity<String> response = oemController.createOemType(oemDTO);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Error in saving oem data", response.getBody());
	}


	/*
	 * This test checks if the findAllOems method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void findAllOems_found() {
		when(oemService.getAllOem()).thenReturn(Arrays.asList(new OemDTO()));

		ResponseEntity<?> response = oemController.findAllOemTypes();

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}


	/*
	 * This test checks if the findAllOems method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void findAllOems_notFound() {
		when(oemService.getAllOem()).thenReturn(Arrays.asList());

		ResponseEntity<?> response = oemController.findAllOemTypes();

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}


	/*
	 * This test checks if the deleteOem method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void deleteOem() {
		doNothing().when(oemService).deleteOem(anyInt());

		ResponseEntity<String> response = oemController.deleteOemType(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Successfully deleted the oem", response.getBody());
	}


	/*
	 * This test checks if the findById method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void findById_found() {
		OemDTO oemDTO = new OemDTO();
		when(oemService.findById(anyInt())).thenReturn(oemDTO);

		ResponseEntity<OemDTO> response = oemController.findById(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(oemDTO, response.getBody());
	}


	/*
	 * This test checks if the updateOem method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void updateOem_success() {
		OemUpdateDTO oemUpdateDTO = new OemUpdateDTO();
		when(oemService.updateOem(any(OemUpdateDTO.class), anyInt()))
				.thenReturn(oemUpdateDTO);

		ResponseEntity<?> response = oemController.updateOemType(1, oemUpdateDTO);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(oemUpdateDTO, response.getBody());
	}


	/*
	 * This test checks if the updateOem method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void updateOem_failure() {
		when(oemService.updateOem(any(OemUpdateDTO.class), anyInt()))
				.thenReturn(null);

		ResponseEntity<?> response = oemController.updateOemType(1, new OemUpdateDTO());

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
	}


	/*
	 * This test checks if the getOemsByCategory method in the
	 * controller returns a successful response when the service layer operation is
	 * successful.
	 */
	@Test
	public void getOemsByCategory_found() {
		when(oemService.getOemsByCategory(anyString()))
				.thenReturn(Arrays.asList(new OemDTO()));

		ResponseEntity<?> response = oemController.getOemsByCategory("category");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}


	/*
	 * This test checks if the getOemsByCategory method in the
	 * controller returns an error response when the service layer operation fails.
	 */
	@Test
	public void getOemsByCategory_notFound() {
		when(oemService.getOemsByCategory(anyString())).thenReturn(Arrays.asList());

		ResponseEntity<?> response = oemController.getOemsByCategory("category");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}

	@Test
	/*
	 * This test checks if the getOemListByCategory method in the
	 * controller returns a successful response when the service layer operation is
	 * successful.
	 */
	public void getOemListByCategory_found() {
		when(oemService.getOemListByCategory(anyString()))
				.thenReturn(Arrays.asList("name1", "name2"));

		ResponseEntity<?> response = oemController.getOemListByCategory("category");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	@Test
	/*
	 * This test checks if the getOemListByCategory method in the
	 * controller returns an error response when the service layer operation fails.
	 */
	public void getOemListByCategory_notFound() {
		when(oemService.getOemListByCategory(anyString())).thenReturn(Arrays.asList());

		ResponseEntity<?> response = oemController.getOemListByCategory("category");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}
}
