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
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.rdkm.tdkservice.dto.PrimitiveTestCreateDTO;
import com.rdkm.tdkservice.dto.PrimitiveTestDTO;
import com.rdkm.tdkservice.dto.PrimitiveTestNameAndIdDTO;
import com.rdkm.tdkservice.dto.PrimitiveTestUpdateDTO;
import com.rdkm.tdkservice.service.IPrimitiveTestService;

public class PrimitiveTestControllerTest {

	@InjectMocks
	private PrimitiveTestController primitiveTestController;

	@Mock
	private IPrimitiveTestService primitiveTestService;

	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	@Test
	public void createPrimitiveTest_Success() {
		PrimitiveTestCreateDTO primitiveTestDTO = new PrimitiveTestCreateDTO();
		when(primitiveTestService.createPrimitiveTest(primitiveTestDTO)).thenReturn(true);

		ResponseEntity<String> response = primitiveTestController.createPrimitiveTest(primitiveTestDTO);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
		assertEquals("Primitive Test Created Successfully", response.getBody());
	}

	@Test
	public void createPrimitiveTest_Failure() {
		PrimitiveTestCreateDTO primitiveTestDTO = new PrimitiveTestCreateDTO();
		when(primitiveTestService.createPrimitiveTest(primitiveTestDTO)).thenReturn(false);

		ResponseEntity<String> response = primitiveTestController.createPrimitiveTest(primitiveTestDTO);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Primitive Test Creation Failed", response.getBody());
	}

	@Test
	public void updatePrimitiveTest_Success() {
		PrimitiveTestUpdateDTO primitiveTestDTO = new PrimitiveTestUpdateDTO();
		when(primitiveTestService.updatePrimitiveTest(primitiveTestDTO)).thenReturn(true);

		ResponseEntity<String> response = primitiveTestController.updatePrimitiveTest(primitiveTestDTO);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Primitive Test Updated Successfully", response.getBody());
	}

	@Test
	public void updatePrimitiveTest_Failure() {
		PrimitiveTestUpdateDTO primitiveTestDTO = new PrimitiveTestUpdateDTO();
		when(primitiveTestService.updatePrimitiveTest(primitiveTestDTO)).thenReturn(false);

		ResponseEntity<String> response = primitiveTestController.updatePrimitiveTest(primitiveTestDTO);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Primitive Test Update Failed", response.getBody());
	}

	@Test
	public void deleteById_Success() {
		UUID primitiveTestId = UUID.randomUUID();
		doNothing().when(primitiveTestService).deleteById(primitiveTestId);

		ResponseEntity<String> response = primitiveTestController.deleteById(primitiveTestId);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Primitive test deleted successfully", response.getBody());
	}

	@Test
	public void getPrimitiveTestDetails_Found() {
		UUID primitiveTestId = UUID.randomUUID();
		PrimitiveTestDTO primitiveTestDTO = new PrimitiveTestDTO();
		when(primitiveTestService.getPrimitiveTestDetailsById(primitiveTestId)).thenReturn(primitiveTestDTO);

		ResponseEntity<?> response = primitiveTestController.getPrimitiveTestDetails(primitiveTestId);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(primitiveTestDTO, response.getBody());
	}

	@Test
	public void getPrimitiveTestDetails_NotFound() {
		UUID primitiveTestId = UUID.randomUUID();
		when(primitiveTestService.getPrimitiveTestDetailsById(primitiveTestId)).thenReturn(null);

		ResponseEntity<?> response = primitiveTestController.getPrimitiveTestDetails(primitiveTestId);

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("Primitive test not found", response.getBody());
	}

	@Test
	public void findAllByModuleName_Success() {
		String moduleName = "Module1";
		List<PrimitiveTestDTO> primitiveTestDTOs = Arrays.asList(new PrimitiveTestDTO(), new PrimitiveTestDTO());
		when(primitiveTestService.findAllByModuleName(moduleName)).thenReturn(primitiveTestDTOs);

		ResponseEntity<?> response = primitiveTestController.findAllByModuleName(moduleName);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(primitiveTestDTOs, response.getBody());
	}

	@Test
	public void findAllByModuleName_NotFound() {
		String moduleName = "Module1";
		when(primitiveTestService.findAllByModuleName(moduleName)).thenReturn(null);

		ResponseEntity<?> response = primitiveTestController.findAllByModuleName(moduleName);

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("Primitive test not found", response.getBody());
	}

	@Test
	public void getPrimitiveTestDetailsByModuleName_Success() {
		String moduleName = "Module1";
		List<PrimitiveTestNameAndIdDTO> primitiveTestDTOs = Arrays.asList(new PrimitiveTestNameAndIdDTO(),
				new PrimitiveTestNameAndIdDTO());
		when(primitiveTestService.getPrimitiveTestDetailsByModuleName(moduleName)).thenReturn(primitiveTestDTOs);

		ResponseEntity<?> response = primitiveTestController.getPrimitiveTestDetailsByModuleName(moduleName);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(primitiveTestDTOs, response.getBody());
	}

	@Test
	public void getPrimitiveTestDetailsByModuleName_NotFound() {
		String moduleName = "Module1";
		when(primitiveTestService.getPrimitiveTestDetailsByModuleName(moduleName)).thenReturn(null);

		ResponseEntity<?> response = primitiveTestController.getPrimitiveTestDetailsByModuleName(moduleName);

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("Primitive test not found", response.getBody());
	}
}
