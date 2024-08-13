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
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.rdkm.tdkservice.dto.BoxTypeDTO;
import com.rdkm.tdkservice.dto.BoxTypeUpdateDTO;
import com.rdkm.tdkservice.service.IBoxTypeService;

/*
* This class is used to test the BoxTypeController class.
* It uses Mockito to mock the service layer and JUnit for the testing framework.
*/
public class BoxTypeControllerTest {

	@InjectMocks
	// The controller that is being tested
	BoxTypeController boxTypeController;

	@Mock
	// The service that the controller depends on
	IBoxTypeService boxTypeService;

	@BeforeEach
	/*
	 * This method is run before each test. It initializes the mocks.
	 */
	public void init() {
		MockitoAnnotations.openMocks(this);
	}

	
	/*
	 * This test checks if the createBoxType method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void createBoxTypeSuccessfully() {
		BoxTypeDTO boxTypeRequest = new BoxTypeDTO();
		when(boxTypeService.createBoxType(boxTypeRequest)).thenReturn(true);

		ResponseEntity<String> response = boxTypeController.createBoxType(boxTypeRequest);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
		assertEquals("Box type created succesfully", response.getBody());
	}

	
	/*
	 * This test checks if the createBoxType method in the controller returns an
	 * error response when the service layer operation fails.
	 */
	@Test
	public void createBoxTypeFailure() {
		BoxTypeDTO boxTypeRequest = new BoxTypeDTO();
		when(boxTypeService.createBoxType(boxTypeRequest)).thenReturn(false);

		ResponseEntity<String> response = boxTypeController.createBoxType(boxTypeRequest);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Error in saving box type data", response.getBody());
	}

	
	/*
	 * This test checks if the getAllBoxTypes method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void getAllBoxTypesSuccessfully() {
		BoxTypeDTO boxTypeDTO = new BoxTypeDTO();
		when(boxTypeService.getAllBoxTypes()).thenReturn(Arrays.asList(boxTypeDTO));

		ResponseEntity<?> response = boxTypeController.getAllBoxTypes();

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	
	/*
	 * This test checks if the getAllBoxTypes method in the controller returns an
	 * error response when the service layer operation fails.
	 */
	@Test
	public void getAllBoxTypesNotFound() {
		when(boxTypeService.getAllBoxTypes()).thenReturn(null);

		ResponseEntity<?> response = boxTypeController.getAllBoxTypes();

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No box types found", response.getBody());
	}

	
	/*
	 * This test checks if the deleteBoxType method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void deleteBoxTypeSuccessfully() {
		doNothing().when(boxTypeService).deleteById(anyInt());

		ResponseEntity<String> response = boxTypeController.deleteBoxType(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Succesfully deleted the box", response.getBody());
	}

	
	/*
	 * This test checks if the findBoxTypeById method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void findBoxTypeByIdSuccessfully() {
		BoxTypeDTO boxTypeDTO = new BoxTypeDTO();
		when(boxTypeService.findById(anyInt())).thenReturn(boxTypeDTO);

		ResponseEntity<BoxTypeDTO> response = boxTypeController.findById(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(boxTypeDTO, response.getBody());
	}

	
	/*
	 * This test checks if the updateBoxType method in the controller returns an
	 * error response when the service layer operation fails.
	 */
	@Test
	public void updateBoxTypeNotFound() {
		BoxTypeUpdateDTO boxTypeUpdateDTO = new BoxTypeUpdateDTO();

		when(boxTypeService.updateBoxType(any(BoxTypeUpdateDTO.class), anyInt())).thenReturn(null);

		ResponseEntity<?> response = boxTypeController.updateBoxType(1, boxTypeUpdateDTO);

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("Box type not found", response.getBody());
	}

	
	/*
	 * This test checks if the updateBoxType method in the controller returns a
	 * successful response when the service layer operation is successful.
	 */
	@Test
	public void updateBoxTypeSuccessfully() {
		BoxTypeUpdateDTO boxTypeUpdateDTO = new BoxTypeUpdateDTO();

		when(boxTypeService.updateBoxType(any(BoxTypeUpdateDTO.class), anyInt())).thenReturn(boxTypeUpdateDTO);

		ResponseEntity<?> response = boxTypeController.updateBoxType(1, boxTypeUpdateDTO);

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	
	/*
	 * This test checks if the deleteBoxType method in the controller returns an
	 * error response when the service layer operation fails.
	 */
	@Test
	public void deleteBoxTypeFailure() {
		doThrow(new RuntimeException()).when(boxTypeService).deleteById(anyInt());

		assertThrows(RuntimeException.class, () -> boxTypeController.deleteBoxType(1));
	}

	
	/*
	 * This test checks if the getBoxTypesByCategory method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void getBoxTypesByCategorySuccessfully() {
		BoxTypeDTO boxTypeDTO = new BoxTypeDTO();
		when(boxTypeService.getBoxTypesByCategory(anyString())).thenReturn(Arrays.asList(boxTypeDTO));

		ResponseEntity<?> response = boxTypeController.getBoxTypesByCategory("category");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	
	/*
	 * This test checks if the getBoxTypesListByCategory method in the controller
	 * returns a successful response when the service layer operation is successful.
	 */
	@Test
	public void getBoxTypesListByCategorySuccessfully() {
		when(boxTypeService.getBoxTypeNameByCategory(anyString())).thenReturn(Arrays.asList("BoxType1", "BoxType2"));

		ResponseEntity<?> response = boxTypeController.getBoxTypesListByCategory("category");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	
	/*
	 * This test checks if the isTheBoxTypeGateway method in the controller returns
	 * a successful response when the service layer operation is successful.
	 */
	@Test
	public void isTheBoxTypeGatewaySuccessfully() {
		when(boxTypeService.isTheBoxTypeGateway(anyString())).thenReturn(true);

		boolean response = boxTypeController.isTheBoxTypeGateway("BoxType1");

		assertTrue(response);
	}

	
	/*
	 * This test checks if the getOtherBoxTypesListByCategory method in the
	 * controller returns a successful response when the service layer operation is
	 * successful.
	 */
	@Test
	public void getOtherBoxTypesListByCategorySuccessfully() {
		List<String> boxTypes = new ArrayList<>(Arrays.asList("BoxType1", "BoxType2", "BoxType3"));

		when(boxTypeService.getBoxTypeNameByCategory(anyString())).thenReturn(boxTypes);

		ResponseEntity<?> response = boxTypeController.getOtherBoxTypesListByCategory("category", "BoxType1");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	
	/*
	 * This test checks if the getOtherBoxTypesListByCategory method in the
	 * controller returns an error response when the service layer operation fails.
	 */
	@Test
	public void getOtherBoxTypesListByCategoryNotFound() {
		when(boxTypeService.getBoxTypeNameByCategory(anyString())).thenReturn(Collections.emptyList());

		ResponseEntity<?> response = boxTypeController.getOtherBoxTypesListByCategory("category", "BoxType1");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No box types found", response.getBody());
	}

	
	/*
	 * This test checks if the getBoxTypesByCategory method in the controller
	 * returns an error response when the service layer operation fails.
	 */
	@Test
	public void getBoxTypesByCategoryNotFound() {
		when(boxTypeService.getBoxTypesByCategory(anyString())).thenReturn(null);

		ResponseEntity<?> response = boxTypeController.getBoxTypesByCategory("category");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No box types found", response.getBody());
	}
}
