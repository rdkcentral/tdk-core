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
package com.rdkm.tdkservice.serviceimpl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.dao.DataIntegrityViolationException;

import com.rdkm.tdkservice.dto.SocCreateDTO;
import com.rdkm.tdkservice.dto.SocDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.Soc;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.SocRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;

/**
 * The SocServiceTest class contains unit tests for the SocService class. It
 * uses Mockito for mocking dependencies and JUnit for running the tests.
 */
public class SocServiceTest {

	/**
	 * The service under test.
	 */
	/**
	 * The service under test.
	 */
	@InjectMocks
	private SocService socService;

	/**
	 * A mock SocRepository for simulating database operations.
	 */
	@Mock
	private SocRepository socRepository;

	/**
	 * A mock UserGroupRepository for simulating database operations.
	 */
	@Mock
	private UserGroupRepository userGroupRepository;

	/**
	 * This method is executed before each test. It initializes the mocks.
	 */
	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	/**
	 * Test case for successful Soc creation.
	 */
	@Test
	public void createSocSuccessfully() {
		UUID socId = UUID.randomUUID();
		SocCreateDTO socDTO = new SocCreateDTO();
		socDTO.setSocName("Test Soc");
		socDTO.setSocCategory("RDKV");
		socDTO.setSocUserGroup("UserGroup1");

		Soc soc = new Soc();
		soc.setId(socId);
		soc.setName(socDTO.getSocName());
		soc.setCategory(Category.getCategory(socDTO.getSocCategory()));
		soc.setUserGroup(new UserGroup());

		when(socRepository.existsByName(socDTO.getSocName())).thenReturn(false);
		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());
		when(socRepository.save(any(Soc.class))).thenReturn(soc);

		boolean result = socService.createSoc(socDTO);

		assertTrue(result);
	}

	/**
	 * Test case for Soc creation failure due to a RuntimeException.
	 */
	@Test
	public void createSocFailure() {
		SocCreateDTO socDTO = new SocCreateDTO();
		socDTO.setSocName("Test Soc");

		when(socRepository.existsByName(socDTO.getSocName())).thenReturn(false);
		when(socRepository.save(any(Soc.class))).thenThrow(RuntimeException.class);

		boolean result = socService.createSoc(socDTO);
		assertFalse(result);
	}

	/**
	 * Test case for Soc creation failure due to the resource already existing.
	 */
	@Test
	public void createSocResourceAlreadyExists() {
		SocCreateDTO socDTO = new SocCreateDTO();
		socDTO.setSocName("Test Soc");

		when(socRepository.existsByName(socDTO.getSocName())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> socService.createSoc(socDTO));
	}

	/**
	 * Test case for Soc update failure due to the resource not being found.
	 */
	@Test
	public void updateSocResourceNotFound() {
		UUID socId = UUID.randomUUID();
		SocDTO socUpdateDTO = new SocDTO();
		socUpdateDTO.setSocId(socId);
		socUpdateDTO.setSocName("Test Soc");

		when(socRepository.findById(socId)).thenReturn(java.util.Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> socService.updateSoc(socUpdateDTO));
	}

	/**
	 * Test case for Soc update failure due to the resource already existing.
	 */
	@Test
	public void updateSocResourceAlreadyExists() {
		UUID socId = UUID.randomUUID();
		SocDTO socUpdateDTO = new SocDTO();
		socUpdateDTO.setSocId(socId);
		socUpdateDTO.setSocName("Test Soc");

		Soc soc = new Soc();
		soc.setName("Test Soc");
		soc.setId(socId);

		when(socRepository.findById(socId)).thenReturn(java.util.Optional.of(soc));
		when(socRepository.existsByName(socUpdateDTO.getSocName())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> socService.updateSoc(socUpdateDTO));
	}

	/**
	 * Test case for successful Soc update.
	 */
	@Test
	public void updateSocSuccessfully() {
		UUID socId = UUID.randomUUID();
		SocDTO socUpdateDTO = new SocDTO();
		socUpdateDTO.setSocId(socId);
		socUpdateDTO.setSocName("Test Soc");
		socUpdateDTO.setSocCategory("RDKV");

		Soc soc = new Soc();
		soc.setName("Test Soc");
		soc.setId(socId);
		soc.setCategory(Category.RDKB);

		when(socRepository.findById(socId)).thenReturn(java.util.Optional.of(soc));
		when(socRepository.existsByName(socUpdateDTO.getSocName())).thenReturn(false);
		when(socRepository.save(any(Soc.class))).thenReturn(soc);

		SocDTO result = socService.updateSoc(socUpdateDTO);

		assertNotNull(result);
		assertEquals("Test Soc", result.getSocName());
		assertEquals("RDKV", result.getSocCategory());
	}

	/**
	 * Test case for Soc update failure due to a RuntimeException.
	 */
	@Test
	public void updateSocExceptionWhileSaving() {
		UUID socId = UUID.randomUUID();
		SocDTO socUpdateDTO = new SocDTO();
		socUpdateDTO.setSocName("Test Soc");

		Soc soc = new Soc();
		soc.setName("Test Soc");
		soc.setId(socId);

		when(socRepository.findById(socId)).thenReturn(java.util.Optional.of(soc));
		when(socRepository.existsByName(socUpdateDTO.getSocName())).thenReturn(false);
		when(socRepository.save(any(Soc.class))).thenThrow(RuntimeException.class);

		assertThrows(RuntimeException.class, () -> socService.updateSoc(socUpdateDTO));
	}

	/**
	 * Test case for successful Soc retrieval by ID.
	 */
	@Test
	public void findByIdSuccess() {
		UUID socId = UUID.randomUUID();
		Soc soc = new Soc();
		soc.setName("Test Soc");
		soc.setId(socId);

		when(socRepository.findById(socId)).thenReturn(java.util.Optional.of(soc));

		SocDTO result = socService.findById(socId);

		assertNotNull(result);
		assertEquals("Test Soc", result.getSocName());
	}

	/**
	 * Test case for Soc retrieval failure due to the resource not being found.
	 */
	@Test
	public void findByIdFailure() {
		UUID socId = UUID.randomUUID();
		when(socRepository.findById(socId)).thenReturn(java.util.Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> socService.findById(socId));
	}

	/**
	 * Test case for successful Soc deletion.
	 */
	@Test
	public void deleteSocSuccess() {
		UUID socId = UUID.randomUUID();
		when(socRepository.existsById(socId)).thenReturn(true);

		socService.deleteSoc(socId);

		verify(socRepository, times(1)).deleteById(socId);
	}

	/**
	 * Test case for Soc deletion failure due to the resource not being found.
	 */
	@Test
	public void deleteSocFailure() {
		UUID socId = UUID.randomUUID();
		when(socRepository.existsById(socId)).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> socService.deleteSoc(socId));
	}

	/**
	 * Test case for Soc deletion failure due to a DataIntegrityViolationException.
	 */
	@Test
	public void deleteSocException() {
		UUID socId = UUID.randomUUID();
		when(socRepository.existsById(socId)).thenReturn(true);

		doThrow(DataIntegrityViolationException.class).when(socRepository).deleteById(socId);
		assertThrows(DeleteFailedException.class, () -> socService.deleteSoc(socId));
	}

	/**
	 * Test case for retrieving Socs by category when the category returns null.
	 */
	@Test
	public void testGetSocsByCategoryReturnsNull() {
		String category = "RDKV";
		when(socRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		List<SocDTO> result = socService.getSOCsByCategory(category);
		assertNull(result);
	}

	/**
	 * Test case for retrieving a list of Socs by category when the category returns
	 * null.
	 */
	@Test
	public void testGetSocsListByCategoryReturnsNull() {
		String category = "RDKV";
		when(socRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		List<String> result = socService.getSOCsListByCategory(category);
		assertNull(result);
	}

	/**
	 * Test case for retrieving Socs by category when the category does not exist.
	 */
	@Test
	public void testGetSocsByCategoryThrowsResourceNotFoundException() {
		String category = "NonExistentCategory";
		when(socRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		assertThrows(ResourceNotFoundException.class, () -> {
			socService.getSOCsByCategory(category);
		});
	}

	/**
	 * Test case for retrieving a list of Socs by category when the category does
	 * not exist.
	 */
	@Test
	public void testGetSocsListByCategoryThrowsResourceNotFoundException() {
		String category = "NonExistentCategory";
		when(socRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		assertThrows(ResourceNotFoundException.class, () -> {
			socService.getSOCsListByCategory(category);
		});
	}

	/**
	 * Test case for successful retrieval of Socs by category.
	 */
	@Test
	public void getSocsByCategorySuccess() {
		UUID socId = UUID.randomUUID();
		Soc soc = new Soc();
		soc.setName("Test Soc");
		soc.setId(socId);

		when(socRepository.findByCategory(any())).thenReturn(Arrays.asList(soc));

		List<SocDTO> result = socService.getSOCsByCategory("RDKV");

		assertNotNull(result);
		assertEquals(1, result.size());
	}

	/**
	 * Test case for successful retrieval of a list of Socs by category.
	 */
	@Test
	public void getSocsListByCategorySuccess() {
		UUID socId = UUID.randomUUID();
		Soc soc = new Soc();
		soc.setName("Test Soc");
		soc.setId(socId);

		when(socRepository.findByCategory(any())).thenReturn(Arrays.asList(soc));

		List<String> result = socService.getSOCsListByCategory("RDKV");

		assertNotNull(result);
		assertEquals(1, result.size());
	}

	/**
	 * Test case for successful retrieval of all Socs.
	 */
	@Test
	public void testFindAll() {

		// Arrange
		Soc soc1 = new Soc();
		soc1.setName("Soc1");
		Soc soc2 = new Soc();
		soc2.setName("Soc2");

		when(socRepository.findAll()).thenReturn(Arrays.asList(soc1, soc2));

		// Act
		List<SocDTO> result = socService.findAll();

		// Assert
		assertEquals(2, result.size());
		assertEquals("Soc1", result.get(0).getSocName());
		assertEquals("Soc2", result.get(1).getSocName());
	}

	/**
	 * Test case for retrieving all Socs when none exist.
	 */
	@Test
	public void testFindAllReturnsNull() {
		// Arrange
		when(socRepository.findAll()).thenReturn(null);

		// Act
		List<SocDTO> result = socService.findAll();

		// Assert
		assertNull(result);
	}

}