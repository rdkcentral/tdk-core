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

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.rdkm.tdkservice.dto.SocVendorDTO;
import com.rdkm.tdkservice.dto.SocVendorUpdateDTO;
import com.rdkm.tdkservice.service.ISocVendorService;

/*
 * The class is used to test the SocVendorController class.
 */
public class SocVendorControllerTest {

	@InjectMocks
	// The controller under test
	private SocVendorController socVendorController;

	@Mock
	// The service that the controller depends on
	private ISocVendorService socVendorService;

	/**
	 * This method sets up the mocks before each test.
	 */
	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	/**
	 * This test ensures that a SOC Vendor is created successfully.
	 */
	@Test
	public void createSocVendorSuccessfully() {
		SocVendorDTO socVendorDTO = new SocVendorDTO();
		when(socVendorService.createSocVendor(socVendorDTO)).thenReturn(true);

		ResponseEntity<String> response = socVendorController.createSocVendor(socVendorDTO);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
	}

	/**
	 * This test ensures that the system handles SOC Vendor creation failure
	 * correctly.
	 */
	@Test
	public void createSocVendorFailure() {
		SocVendorDTO socVendorDTO = new SocVendorDTO();
		when(socVendorService.createSocVendor(socVendorDTO)).thenReturn(false);

		ResponseEntity<String> response = socVendorController.createSocVendor(socVendorDTO);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
	}

	/**
	 * This test ensures that all SOC Vendors are returned correctly when data is
	 * present.
	 */
	@Test
	public void getAllSocVendorsReturnsData() {
		SocVendorDTO socVendorDTO = new SocVendorDTO();
		when(socVendorService.findAll()).thenReturn(Arrays.asList(socVendorDTO));

		ResponseEntity<List<SocVendorDTO>> response = socVendorController.getAllSocVendors();

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(1, response.getBody().size());
	}

	/**
	 * This test ensures that the system handles the case when no SOC Vendors are
	 * found.
	 */
	@Test
	public void getAllSocVendorsReturnsNotFound() {
		when(socVendorService.findAll()).thenReturn(Arrays.asList());

		ResponseEntity<List<SocVendorDTO>> response = socVendorController.getAllSocVendors();

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}

	/**
	 * This test ensures that a SOC Vendor is deleted correctly.
	 */
	@Test
	public void deleteSocVendor() {
		doNothing().when(socVendorService).deleteSocVendor(1);

		ResponseEntity<?> response = socVendorController.deleteSocVendor(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that a SOC Vendor is found by ID correctly when data is
	 * present.
	 */
	@Test
	public void findByIdReturnsData() {
		SocVendorDTO socVendorDTO = new SocVendorDTO();
		when(socVendorService.findById(1)).thenReturn(socVendorDTO);

		ResponseEntity<SocVendorDTO> response = socVendorController.findById(1);

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that a SOC Vendor is updated successfully.
	 */
	@Test
	public void updateSocVendorSuccessfully() {
		SocVendorUpdateDTO socVendorUpdateDTO = new SocVendorUpdateDTO();
		when(socVendorService.updateSocVendor(socVendorUpdateDTO, 1)).thenReturn(socVendorUpdateDTO);

		ResponseEntity<?> response = socVendorController.updateSocVendor(1, socVendorUpdateDTO);

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that the system handles SOC Vendor update failure
	 * correctly.
	 */
	@Test
	public void updateSocVendorFailure() {
		SocVendorUpdateDTO socVendorUpdateDTO = new SocVendorUpdateDTO();
		when(socVendorService.updateSocVendor(socVendorUpdateDTO, 1)).thenReturn(null);

		ResponseEntity<?> response = socVendorController.updateSocVendor(1, socVendorUpdateDTO);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
	}

	/**
	 * This test ensures that SOC Vendors are returned correctly by category when
	 * data is present.
	 */
	@Test
	public void getSOCVendorsByCategoryReturnsData() {
		SocVendorDTO socVendorDTO = new SocVendorDTO();
		when(socVendorService.getSOCVendorsByCategory("RDKV")).thenReturn(Arrays.asList(socVendorDTO));

		ResponseEntity<?> response = socVendorController.getSOCVendorsByCategory("RDKV");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that the system handles the case when no SOC Vendors are
	 * found by category.
	 */
	@Test
	public void getSOCVendorsByCategoryReturnsNotFound() {
		when(socVendorService.getSOCVendorsByCategory("category")).thenReturn(Arrays.asList());

		ResponseEntity<?> response = socVendorController.getSOCVendorsByCategory("RDKV");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		verify(socVendorService, times(1)).getSOCVendorsByCategory("RDKV");
	}

	/**
	 * This test ensures that a list of SOC Vendors is returned correctly by
	 * category when data is present.
	 */
	@Test
	public void getSOCVendorsListByCategoryReturnsData() {
		when(socVendorService.getSOCVendorsListByCategory("RDKB")).thenReturn(Arrays.asList("vendor1"));

		ResponseEntity<?> response = socVendorController.getSOCVendorsListByCategory("RDKB");

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This test ensures that the system handles the case when no list of SOC
	 * Vendors is found by category.
	 */
	@Test
	public void getSOCVendorsListByCategoryReturnsNotFound() {
		when(socVendorService.getSOCVendorsListByCategory("RDKB")).thenReturn(Arrays.asList());

		ResponseEntity<?> response = socVendorController.getSOCVendorsListByCategory("RDKB");

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
	}

}