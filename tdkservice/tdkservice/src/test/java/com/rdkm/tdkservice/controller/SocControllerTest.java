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
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Arrays;
import java.util.List;

import com.rdkm.tdkservice.dto.SocDTO;
import com.rdkm.tdkservice.dto.SocUpdateDTO;
import com.rdkm.tdkservice.service.ISocService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

/*
 * The class is used to test the SocVendorController class.
 */
public class SocControllerTest {

	@InjectMocks
// The controller under test
	private SocController socController;

	@Mock
// The service that the controller depends on
	private ISocService socService;

	/**
	 * This method sets up the mocks before each test.
	 */
	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	/**
	 * This test ensures that a SOC is created successfully.
	 */
	@Test
	public void createSocSuccessfully() {
		SocDTO socDTO = new SocDTO();
		when(socService.createSoc(socDTO)).thenReturn(true);

		ResponseEntity<String> response = socController.createSoc(socDTO);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
	}

	/**
	 * This test ensures that the system handles SOC creation failure correctly.
	 */
	@Test
	public void createSocFailure() {
		SocDTO socDTO = new SocDTO();
		when(socService.createSoc(socDTO)).thenReturn(false);

		ResponseEntity<String> response = socController.createSoc(socDTO);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
	}

	/**
	 * This test ensures that all SOCs are returned correctly when data is present.
	 */
	@Test
	public void getAllSocsReturnsData() {
		SocDTO socDTO = new SocDTO();
		when(socService.findAll()).thenReturn(Arrays.asList(socDTO));

		ResponseEntity<List<SocDTO>> response = socController.getAllSocs();

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(1, response.getBody().size());
	}

	/**
	 * This test ensures that the system handles the case when no SOCs are found.
	 */
	@Test
	public void getAllSocsReturnsNotFound() {
		when(socService.findAll()).thenReturn(Arrays.asList());

		ResponseEntity<List<SocDTO>> response = socController.getAllSocs();

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}

	/**
	 * This test ensures that a SOC is deleted correctly.
	 */
	@Test
	public void deleteSoc() {
		doNothing().when(socService).deleteSoc(1);

		ResponseEntity<?> response = socController.deleteSoc(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that a SOC is found by ID correctly when data is present.
	 */
	@Test
	public void findByIdReturnsData() {
		SocDTO socDTO = new SocDTO();
		when(socService.findById(1)).thenReturn(socDTO);

		ResponseEntity<SocDTO> response = socController.findById(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that a SOC is updated successfully.
	 */
	@Test
	public void updateSocSuccessfully() {
		SocUpdateDTO socUpdateDTO = new SocUpdateDTO();
		when(socService.updateSoc(socUpdateDTO, 1)).thenReturn(socUpdateDTO);

		ResponseEntity<?> response = socController.updateSoc(1, socUpdateDTO);

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that the system handles SOC update failure correctly.
	 */
	@Test
	public void updateSocFailure() {
		SocUpdateDTO socUpdateDTO = new SocUpdateDTO();
		when(socService.updateSoc(socUpdateDTO, 1)).thenReturn(null);

		ResponseEntity<?> response = socController.updateSoc(1, socUpdateDTO);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
	}

	/**
	 * This test ensures that SOCs are returned correctly by category when data is present.
	 */
	@Test
	public void getSocsByCategoryReturnsData() {
		SocDTO socDTO = new SocDTO();
		when(socService.getSOCsByCategory("RDKV")).thenReturn(Arrays.asList(socDTO));

		ResponseEntity<?> response = socController.getSOCsByCategory("RDKV");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that the system handles the case when no SOCs are found by category.
	 */
	@Test
	public void getSocsByCategoryReturnsNotFound() {
		when(socService.getSOCsByCategory("category")).thenReturn(Arrays.asList());

		ResponseEntity<?> response = socController.getSOCsByCategory("RDKV");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		verify(socService, times(1)).getSOCsByCategory("RDKV");
	}

	/**
	 * This test ensures that a list of SOCs is returned correctly by category when data is present.
	 */
	@Test
	public void getSocsListByCategoryReturnsData() {
		when(socService.getSOCsListByCategory("RDKB")).thenReturn(Arrays.asList("vendor1"));

		ResponseEntity<?> response = socController.getSOCsListByCategory("RDKB");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that the system handles the case when no list of SOCs is found by category.
	 */
	@Test
	public void getSocsListByCategoryReturnsNotFound() {
		when(socService.getSOCsListByCategory("RDKB")).thenReturn(Arrays.asList());

		ResponseEntity<?> response = socController.getSOCsListByCategory("RDKB");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}
}