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

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.dao.DataIntegrityViolationException;

import com.rdkm.tdkservice.dto.SocVendorDTO;
import com.rdkm.tdkservice.dto.SocVendorUpdateDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.SocVendor;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.SocVendorRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;

/**
 * The SocVendorServiceTest class contains unit tests for the SocVendorService
 * class. It uses Mockito for mocking dependencies and JUnit for running the
 * tests.
 */
public class SocVendorServiceTest {

	/**
	 * The service under test.
	 */
	@InjectMocks
	private SocVendorService socVendorService;

	/**
	 * A mock SocVendorRepository for simulating database operations.
	 */
	@Mock
	private SocVendorRepository socVendorRepository;

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
	 * Test case for successful SocVendor creation.
	 */
	@Test
	public void createSocVendorSuccessfully() {
		SocVendorDTO socVendorDTO = new SocVendorDTO();
		socVendorDTO.setSocVendorName("Test Vendor");
		socVendorDTO.setSocVendorCategory("RDKV");
		socVendorDTO.setSocVendorUserGroup("UserGroup1");

		SocVendor socVendor = new SocVendor();
		socVendor.setId(1);
		socVendor.setName(socVendorDTO.getSocVendorName());
		socVendor.setCategory(Category.getCategory(socVendorDTO.getSocVendorCategory()));
		socVendor.setUserGroup(new UserGroup());

		when(socVendorRepository.existsByName(socVendorDTO.getSocVendorName())).thenReturn(false);
		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());
		when(socVendorRepository.save(any(SocVendor.class))).thenReturn(socVendor);

		boolean result = socVendorService.createSocVendor(socVendorDTO);

		assertTrue(result);
	}

	/**
	 * Test case for SocVendor creation failure due to a RuntimeException.
	 */
	@Test
	public void createSocVendorFailure() {
		SocVendorDTO socVendorDTO = new SocVendorDTO();
		socVendorDTO.setSocVendorName("Test Vendor");

		when(socVendorRepository.existsByName(socVendorDTO.getSocVendorName())).thenReturn(false);
		when(socVendorRepository.save(any(SocVendor.class))).thenThrow(RuntimeException.class);

		boolean result = socVendorService.createSocVendor(socVendorDTO);
		assertFalse(result);

	}

	/**
	 * Test case for SocVendor creation failure due to the resource already
	 * existing.
	 */
	@Test
	public void createSocVendorResourceAlreadyExists() {
		SocVendorDTO socVendorDTO = new SocVendorDTO();
		socVendorDTO.setSocVendorName("Test Vendor");

		when(socVendorRepository.existsByName(socVendorDTO.getSocVendorName())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> socVendorService.createSocVendor(socVendorDTO));
	}

	/**
	 * Test case for SocVendor update failure due to the resource not being found.
	 */
	@Test
	public void updateSocVendorResourceNotFound() {
		SocVendorUpdateDTO socVendorUpdateDTO = new SocVendorUpdateDTO();
		socVendorUpdateDTO.setSocVendorName("Test Vendor");

		when(socVendorRepository.findById(1)).thenReturn(java.util.Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> socVendorService.updateSocVendor(socVendorUpdateDTO, 1));

	}

	/**
	 * Test case for SocVendor update failure due to the resource already existing.
	 */
	@Test
	public void updateSocVendorResourceAlreadyExists() {
		SocVendorUpdateDTO socVendorUpdateDTO = new SocVendorUpdateDTO();
		socVendorUpdateDTO.setSocVendorName("Test Vendor");

		SocVendor socVendor = new SocVendor();
		socVendor.setName("Test Vendor");
		socVendor.setId(1);

		when(socVendorRepository.findById(1)).thenReturn(java.util.Optional.of(socVendor));
		when(socVendorRepository.existsByName(socVendorUpdateDTO.getSocVendorName())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class,
				() -> socVendorService.updateSocVendor(socVendorUpdateDTO, 1));

	}

	/**
	 * Test case for successful SocVendor update.
	 */
	@Test
	public void updateSocVendorSuccessfully() {
		SocVendorUpdateDTO socVendorUpdateDTO = new SocVendorUpdateDTO();
		socVendorUpdateDTO.setSocVendorName("Test Vendor");
		socVendorUpdateDTO.setSocVendorCategory("RDKV");

		SocVendor socVendor = new SocVendor();
		socVendor.setName("Test Vendor");
		socVendor.setId(1);
		socVendor.setCategory(Category.RDKB);

		when(socVendorRepository.findById(1)).thenReturn(java.util.Optional.of(socVendor));
		when(socVendorRepository.existsByName(socVendorUpdateDTO.getSocVendorName())).thenReturn(false);
		when(socVendorRepository.save(any(SocVendor.class))).thenReturn(socVendor);

		SocVendorUpdateDTO result = socVendorService.updateSocVendor(socVendorUpdateDTO, 1);

		assertNotNull(result);
		assertEquals("Test Vendor", result.getSocVendorName());
		assertEquals("RDKV", result.getSocVendorCategory());

	}

	/**
	 * Test case for SocVendor update failure due to a RuntimeException.
	 */
	@Test
	public void updateSocVendorExceptionWhileSaving() {
		SocVendorUpdateDTO socVendorUpdateDTO = new SocVendorUpdateDTO();
		socVendorUpdateDTO.setSocVendorName("Test Vendor");

		SocVendor socVendor = new SocVendor();
		socVendor.setName("Test Vendor");
		socVendor.setId(1);

		when(socVendorRepository.findById(1)).thenReturn(java.util.Optional.of(socVendor));
		when(socVendorRepository.existsByName(socVendorUpdateDTO.getSocVendorName())).thenReturn(false);
		when(socVendorRepository.save(any(SocVendor.class))).thenThrow(RuntimeException.class);

		assertThrows(RuntimeException.class, () -> socVendorService.updateSocVendor(socVendorUpdateDTO, 1));

	}

	/**
	 * Test case for successful SocVendor retrieval by ID.
	 */
	@Test
	public void findByIdSuccess() {
		SocVendor socVendor = new SocVendor();
		socVendor.setName("Test Vendor");
		socVendor.setId(1);

		when(socVendorRepository.findById(1)).thenReturn(java.util.Optional.of(socVendor));

		SocVendorDTO result = socVendorService.findById(1);

		assertNotNull(result);
		assertEquals("Test Vendor", result.getSocVendorName());

	}

	/**
	 * Test case for SocVendor retrieval failure due to the resource not being
	 * found.
	 */
	@Test
	public void findByIdFailure() {
		when(socVendorRepository.findById(1)).thenReturn(java.util.Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> socVendorService.findById(1));

	}

	/**
	 * Test case for successful SocVendor deletion.
	 */
	@Test
	public void deleteSocVendorSuccess() {
		when(socVendorRepository.existsById(1)).thenReturn(true);

		socVendorService.deleteSocVendor(1);

		verify(socVendorRepository, times(1)).deleteById(1);
	}

	/**
	 * Test case for SocVendor deletion failure due to the resource not being found.
	 */
	@Test
	public void deleteSocVendorFailure() {
		when(socVendorRepository.existsById(1)).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> socVendorService.deleteSocVendor(1));

	}

	/**
	 * Test case for SocVendor deletion failure due to a
	 * DataIntegrityViolationException.
	 */
	@Test
	public void deleteSocVendorException() {
		when(socVendorRepository.existsById(1)).thenReturn(true);

		doThrow(DataIntegrityViolationException.class).when(socVendorRepository).deleteById(1);
		assertThrows(DeleteFailedException.class, () -> socVendorService.deleteSocVendor(1));
	}

	/**
	 * Test case for retrieving SOCVendors by category when the category returns
	 * null.
	 */
	@Test
	public void testGetSOCVendorsByCategoryReturnsNull() {
		String category = "RDKV";
		when(socVendorRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		List<SocVendorDTO> result = socVendorService.getSOCVendorsByCategory(category);
		assertNull(result);
	}

	/**
	 * Test case for retrieving a list of SOCVendors by category when the category
	 * returns null.
	 */
	@Test
	public void testGetSOCVendorsListByCategoryReturnsNull() {
		String category = "RDKV";
		when(socVendorRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		List<String> result = socVendorService.getSOCVendorsListByCategory(category);
		assertNull(result);
	}

	/**
	 * Test case for retrieving SOCVendors by category when the category does not
	 * exist.
	 */
	@Test
	public void testGetSOCVendorsByCategoryThrowsResourceNotFoundException() {
		String category = "NonExistentCategory";
		when(socVendorRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		assertThrows(ResourceNotFoundException.class, () -> {
			socVendorService.getSOCVendorsByCategory(category);
		});
	}

	/**
	 * Test case for retrieving a list of SOCVendors by category when the category
	 * does not exist.
	 */
	@Test
	public void testGetSOCVendorsListByCategoryThrowsResourceNotFoundException() {
		String category = "NonExistentCategory";
		when(socVendorRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		assertThrows(ResourceNotFoundException.class, () -> {
			socVendorService.getSOCVendorsListByCategory(category);
		});
	}

	/**
	 * Test case for successful retrieval of SOCVendors by category.
	 */
	@Test
	public void getSOCVendorsByCategorySuccess() {
		SocVendor socVendor = new SocVendor();
		socVendor.setName("Test Vendor");
		socVendor.setId(1);

		when(socVendorRepository.findByCategory(any())).thenReturn(Arrays.asList(socVendor));

		List<SocVendorDTO> result = socVendorService.getSOCVendorsByCategory("RDKV");

		assertNotNull(result);
		assertEquals(1, result.size());

	}

	/**
	 * Test case for successful retrieval of a list of SOCVendors by category.
	 */
	@Test
	public void getSOCVendorsListByCategorySuccess() {
		SocVendor socVendor = new SocVendor();
		socVendor.setName("Test Vendor");
		socVendor.setId(1);

		when(socVendorRepository.findByCategory(any())).thenReturn(Arrays.asList(socVendor));

		List<String> result = socVendorService.getSOCVendorsListByCategory("RDKV");

		assertNotNull(result);
		assertEquals(1, result.size());

	}

	/**
	 * Test case for successful retrieval of all SOCVendors.
	 */
	@Test
	public void testFindAll() {
		// Arrange
		SocVendor socVendor1 = new SocVendor();
		socVendor1.setName("Vendor1");
		SocVendor socVendor2 = new SocVendor();
		socVendor2.setName("Vendor2");

		when(socVendorRepository.findAll()).thenReturn(Arrays.asList(socVendor1, socVendor2));

		// Act
		List<SocVendorDTO> result = socVendorService.findAll();

		// Assert
		assertEquals(2, result.size());
		assertEquals("Vendor1", result.get(0).getSocVendorName());
		assertEquals("Vendor2", result.get(1).getSocVendorName());

	}

	/**
	 * Test case for retrieving all SOCVendors when none exist.
	 */
	@Test
	public void testFindAllReturnsNull() {
		// Arrange
		when(socVendorRepository.findAll()).thenReturn(null);

		// Act
		List<SocVendorDTO> result = socVendorService.findAll();

		// Assert
		assertNull(result);

	}

}