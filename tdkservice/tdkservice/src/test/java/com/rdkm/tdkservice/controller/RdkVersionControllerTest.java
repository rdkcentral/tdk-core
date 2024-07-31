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

import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Collections;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.rdkm.tdkservice.dto.RdkVersionCreateDTO;
import com.rdkm.tdkservice.dto.RdkVersionDTO;
import com.rdkm.tdkservice.service.IRdkVersionService;

/**
 * Test class for RdkVersionController.
 */
public class RdkVersionControllerTest {

	@InjectMocks
	private RdkVersionController rdkVersionController;

	@Mock
	private IRdkVersionService rdkVersionService;

	/**
	 * Setup method for each test case.
	 */
	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	/**
	 * Test case for successful RDK version creation.
	 */
	@Test
	public void createRdkVersion_Success() {
		RdkVersionCreateDTO rdkVersionCreateDTO = new RdkVersionCreateDTO();
		when(rdkVersionService.createRdkVersion(rdkVersionCreateDTO)).thenReturn(true);

		ResponseEntity<?> response = rdkVersionController.createRdkVersion(rdkVersionCreateDTO);

		verify(rdkVersionService).createRdkVersion(rdkVersionCreateDTO);
		assert response.getStatusCode() == HttpStatus.CREATED;
		assert response.getBody().equals("Rdk version created successfully");
	}

	/**
	 * Test case for RDK version creation failure.
	 */
	@Test
	public void createRdkVersion_Failure() {
		RdkVersionCreateDTO rdkVersionCreateDTO = new RdkVersionCreateDTO();
		when(rdkVersionService.createRdkVersion(rdkVersionCreateDTO)).thenReturn(false);

		ResponseEntity<?> response = rdkVersionController.createRdkVersion(rdkVersionCreateDTO);

		verify(rdkVersionService).createRdkVersion(rdkVersionCreateDTO);
		assert response.getStatusCode() == HttpStatus.INTERNAL_SERVER_ERROR;
		assert response.getBody().equals("Error in saving rdk version data");
	}

	/**
	 * Test case for successful RDK version update.
	 */
	@Test
	public void updateRdkVersion_Success() {
		RdkVersionDTO rdkVersionDTO = new RdkVersionDTO();
		when(rdkVersionService.updateRdkVersion(rdkVersionDTO)).thenReturn(true);

		ResponseEntity<?> response = rdkVersionController.updateRdkVersion(rdkVersionDTO);

		verify(rdkVersionService).updateRdkVersion(rdkVersionDTO);
		assert response.getStatusCode() == HttpStatus.OK;
		assert response.getBody().equals("Rdk version updated successfully");
	}

	/**
	 * Test case for RDK version update failure.
	 */
	@Test
	public void updateRdkVersion_Failure() {
		RdkVersionDTO rdkVersionDTO = new RdkVersionDTO();
		when(rdkVersionService.updateRdkVersion(rdkVersionDTO)).thenReturn(false);

		ResponseEntity<?> response = rdkVersionController.updateRdkVersion(rdkVersionDTO);

		verify(rdkVersionService).updateRdkVersion(rdkVersionDTO);
		assert response.getStatusCode() == HttpStatus.INTERNAL_SERVER_ERROR;
		assert response.getBody().equals("Error in updating rdk version data");
	}

	/**
	 * Test case for successful RDK version deletion.
	 */
	@Test
	public void deleteRdkVersion_Success() {
		Integer id = 1;
		doNothing().when(rdkVersionService).deleteRdkVersion(id);

		ResponseEntity<String> response = rdkVersionController.deleteRdkVersion(id);

		verify(rdkVersionService).deleteRdkVersion(id);
		assert response.getStatusCode() == HttpStatus.OK;
		assert response.getBody().equals("Rdk version deleted successfully");
	}

	/**
	 * Test case for successful retrieval of all RDK versions.
	 */
	@Test
	public void findAllRdkVersions_Success() {
		List<RdkVersionDTO> rdkVersionDTOList = Collections.singletonList(new RdkVersionDTO());
		when(rdkVersionService.findAllRdkVersions()).thenReturn(rdkVersionDTOList);

		ResponseEntity<?> response = rdkVersionController.findAllRdkVersions();

		verify(rdkVersionService).findAllRdkVersions();
		assert response.getStatusCode() == HttpStatus.OK;
		assert !((List<?>) response.getBody()).isEmpty();
	}

	/**
	 * Test case for retrieval of all RDK versions when list is empty.
	 */
	@Test
	public void findAllRdkVersions_Failure() {
		when(rdkVersionService.findAllRdkVersions()).thenReturn(null);

		ResponseEntity<?> response = rdkVersionController.findAllRdkVersions();

		verify(rdkVersionService).findAllRdkVersions();
		assert response.getStatusCode() == HttpStatus.NOT_FOUND;
		assert response.getBody().equals("No rdk versions found");
	}

	/**
	 * Test case for successful retrieval of all RDK versions by category.
	 */
	@Test
	public void findAllRdkVersionsByCategory_Success() {
		String category = "test";
		List<RdkVersionDTO> rdkVersionDTOList = Collections.singletonList(new RdkVersionDTO());
		when(rdkVersionService.findAllRdkVersionsByCategory(category)).thenReturn(rdkVersionDTOList);

		ResponseEntity<?> response = rdkVersionController.findAllRdkVersionsByCategory(category);

		verify(rdkVersionService).findAllRdkVersionsByCategory(category);
		assert response.getStatusCode() == HttpStatus.OK;
		assert !((List<?>) response.getBody()).isEmpty();
	}

	/**
	 * Test case for retrieval of all RDK versions by category when list is empty.
	 */
	@Test
	public void findAllRdkVersionsByCategory_Failure() {
		String category = "test";
		when(rdkVersionService.findAllRdkVersionsByCategory(category)).thenReturn(null);

		ResponseEntity<?> response = rdkVersionController.findAllRdkVersionsByCategory(category);

		verify(rdkVersionService).findAllRdkVersionsByCategory(category);
		assert response.getStatusCode() == HttpStatus.NOT_FOUND;
		assert response.getBody().equals("No rdk versions found by category");
	}

	/**
	 * Test case for successful retrieval of RDK version list by category.
	 */
	@Test
	public void getRdkVersionListByCategory_Success() {
		String category = "test";
		List<String> rdkVersionList = Collections.singletonList("Version1");
		when(rdkVersionService.getRdkVersionListByCategory(category)).thenReturn(rdkVersionList);

		ResponseEntity<?> response = rdkVersionController.getRdkVersionListByCategory(category);

		verify(rdkVersionService).getRdkVersionListByCategory(category);
		assert response.getStatusCode() == HttpStatus.OK;
		assert !((List<?>) response.getBody()).isEmpty();
	}

	/**
	 * Test case for retrieval of RDK version list by category when list is empty.
	 */
	@Test
	public void getRdkVersionListByCategory_Failure() {
		String category = "test";
		when(rdkVersionService.getRdkVersionListByCategory(category)).thenReturn(null);

		ResponseEntity<?> response = rdkVersionController.getRdkVersionListByCategory(category);

		verify(rdkVersionService).getRdkVersionListByCategory(category);
		assert response.getStatusCode() == HttpStatus.NOT_FOUND;
		assert response.getBody().equals("No rdk versions found by category");
	}

	/**
	 * Test case for successful retrieval of RDK version by id.
	 */
	@Test
	public void findRdkVersionById_Success() {
		Integer id = 1;
		RdkVersionDTO rdkVersionDTO = new RdkVersionDTO();
		when(rdkVersionService.findRdkVersionById(id)).thenReturn(rdkVersionDTO);

		ResponseEntity<?> response = rdkVersionController.findRdkVersionById(id);

		verify(rdkVersionService).findRdkVersionById(id);
		assert response.getStatusCode() == HttpStatus.OK;
		assert response.getBody().equals(rdkVersionDTO);
	}

	/**
	 * Test case for retrieval of RDK version by non-existing id.
	 */
	@Test
	public void findRdkVersionById_Failure() {
		Integer id = 1;
		when(rdkVersionService.findRdkVersionById(id)).thenReturn(null);

		ResponseEntity<?> response = rdkVersionController.findRdkVersionById(id);

		verify(rdkVersionService).findRdkVersionById(id);
		assert response.getStatusCode() == HttpStatus.NOT_FOUND;
		assert response.getBody().equals("No rdk version found by id");
	}
}
