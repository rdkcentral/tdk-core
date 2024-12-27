///*
//* If not stated otherwise in this file or this component's Licenses.txt file the
//* following copyright and licenses apply:
//*
//* Copyright 2024 RDK Management
//*
//* Licensed under the Apache License, Version 2.0 (the "License");
//* you may not use this file except in compliance with the License.
//* You may obtain a copy of the License at
//*
//*
//http://www.apache.org/licenses/LICENSE-2.0
//*
//* Unless required by applicable law or agreed to in writing, software
//* distributed under the License is distributed on an "AS IS" BASIS,
//* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//* See the License for the specific language governing permissions and
//* limitations under the License.
//*/
//package com.rdkm.tdkservice.serviceimpl;
//
//import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
//import static org.junit.jupiter.api.Assertions.assertEquals;
//import static org.junit.jupiter.api.Assertions.assertFalse;
//import static org.junit.jupiter.api.Assertions.assertNotNull;
//import static org.junit.jupiter.api.Assertions.assertNull;
//import static org.junit.jupiter.api.Assertions.assertThrows;
//import static org.junit.jupiter.api.Assertions.assertTrue;
//import static org.mockito.ArgumentMatchers.any;
//import static org.mockito.ArgumentMatchers.anyString;
//import static org.mockito.Mockito.doNothing;
//import static org.mockito.Mockito.doThrow;
//import static org.mockito.Mockito.when;
//
//import java.util.Arrays;
//import java.util.Collections;
//import java.util.List;
//import java.util.Optional;
//import java.util.UUID;
//
//import org.junit.jupiter.api.BeforeEach;
//import org.junit.jupiter.api.Test;
//import org.mockito.InjectMocks;
//import org.mockito.Mock;
//import org.mockito.MockitoAnnotations;
//import org.springframework.dao.DataIntegrityViolationException;
//
//import com.rdkm.tdkservice.dto.OemCreateDTO;
//import com.rdkm.tdkservice.dto.OemDTO;
//import com.rdkm.tdkservice.enums.Category;
//import com.rdkm.tdkservice.exception.DeleteFailedException;
//import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
//import com.rdkm.tdkservice.exception.ResourceNotFoundException;
//import com.rdkm.tdkservice.model.Oem;
//import com.rdkm.tdkservice.model.UserGroup;
//import com.rdkm.tdkservice.repository.OemRepository;
//import com.rdkm.tdkservice.repository.UserGroupRepository;
//
///**
// * This class is used to test the OemServiceTest class. It uses Mockito to mock
// * the repository layer and JUnit for the testing framework.
// */
//public class OemServiceTest {
//
//	/**
//	 * The service that is being tested.
//	 */
//	@InjectMocks
//	private OemService oemService;
//
//	/**
//	 * The repository for oem entities.
//	 */
//	@Mock
//	private OemRepository oemRepository;
//
//	/**
//	 * The repository for UserGroup entities.
//	 */
//	@Mock
//	private UserGroupRepository userGroupRepository;
//
//	/**
//	 * This method is executed before each test. It initializes the mocks.
//	 */
//	@BeforeEach
//	public void setup() {
//		MockitoAnnotations.openMocks(this);
//	}
//
//	/**
//	 * Test case for successful creation of a oem.
//	 */
//	@Test
//	public void testCreateOem_Success() {
//		UUID oemId = UUID.randomUUID();
//		OemCreateDTO oemDTO = new OemCreateDTO();
//		oemDTO.setOemName("Test Manufacturer");
//		oemDTO.setOemCategory("RDKV");
//		oemDTO.setOemUserGroup("UserGroup1");
//
//		Oem oem = new Oem();
//		oem.setId(oemId);
//		oem.setName("Test Manufacturer");
//		oem.setCategory(Category.RDKV);
//		oem.setUserGroup(new UserGroup());
//
//		when(oemRepository.existsByName(anyString())).thenReturn(false);
//		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());
//		when(oemRepository.save(any())).thenReturn(oem);
//
//		assertTrue(oemService.createOem(oemDTO));
//	}
//
//	/**
//	 * Test case for creation of an Oem when an Oem with the same name already
//	 * exists.
//	 */
//	@Test
//	public void testCreateOem_ResourceAlreadyExistsException() {
//		OemCreateDTO oemCreateDTO = new OemCreateDTO();
//		oemCreateDTO.setOemName("Test Manufacturer");
//
//		when(oemRepository.existsByName(anyString())).thenReturn(true);
//
//		assertThrows(ResourceAlreadyExistsException.class, () -> oemService.createOem(oemCreateDTO));
//	}
//
//	/**
//	 * Test case for creation of an Oem when the category is invalid.
//	 */
//	@Test
//	public void testCreateOem_ResourceNotFoundException() {
//		OemCreateDTO oemCreateDTO = new OemCreateDTO();
//		oemCreateDTO.setOemName("Test Manufacturer");
//		oemCreateDTO.setOemCategory("Invalid Category");
//
//		when(oemRepository.existsByName(anyString())).thenReturn(false);
//
//		assertThrows(ResourceNotFoundException.class, () -> oemService.createOem(oemCreateDTO));
//	}
//
//	/**
//	 * Test case for creation of an Oem when an exception occurs while saving the
//	 * Oem.
//	 */
//	@Test
//	public void testCreateOem_ExceptionWhileSaving() {
//		OemCreateDTO oemCreateDTO = new OemCreateDTO();
//		oemCreateDTO.setOemName("Test Manufacturer");
//		oemCreateDTO.setOemCategory("RDKB");
//		oemCreateDTO.setOemUserGroup("Test User Group");
//
//		when(oemRepository.existsByName(anyString())).thenReturn(false);
//		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());
//		when(oemRepository.save(any())).thenThrow(new RuntimeException());
//
//		assertFalse(oemService.createOem(oemCreateDTO));
//	}
//
//	/**
//	 * Test case for retrieving all Oems when there are some present.
//	 */
//	@Test
//	public void testGetAllOemReturnsList() {
//		// Arrange
//		Oem oem = new Oem();
//		oem.setName("Test Manufacturer");
//		when(oemRepository.findAll()).thenReturn(Arrays.asList(oem));
//
//		// Act
//		List<OemDTO> result = oemService.getAllOem();
//
//		// Assert
//		assertNotNull(result);
//		assertFalse(result.isEmpty());
//	}
//
//	/**
//	 * Test case for retrieving all Oems when there are none.
//	 */
//	@Test
//	public void testGetAllOemReturnsNull() {
//		// Arrange
//		when(oemRepository.findAll()).thenReturn(Collections.emptyList());
//
//		// Act
//		List<OemDTO> result = oemService.getAllOem();
//
//		// Assert
//		assertNull(result);
//	}
//
//	/**
//	 * Test case for deleting an Oem when it does not exist.
//	 */
//	@Test
//	public void testDeleteOemThrowsResourceNotFoundException() {
//		// Arrange
//		UUID oemId = UUID.randomUUID();
//		when(oemRepository.existsById(oemId)).thenReturn(false);
//
//		// Act & Assert
//		assertThrows(ResourceNotFoundException.class, () -> oemService.deleteOem(oemId));
//	}
//
//	/**
//	 * Test case for deleting an Oem when an exception occurs while deleting.
//	 */
//	@Test
//	public void testDeleteOemThrowsDeleteFailedException() {
//		// Arrange
//		UUID oemId = UUID.randomUUID();
//		when(oemRepository.existsById(oemId)).thenReturn(true);
//		doThrow(DataIntegrityViolationException.class).when(oemRepository).deleteById(oemId);
//
//		// Act & Assert
//		assertThrows(DeleteFailedException.class, () -> oemService.deleteOem(oemId));
//	}
//
//	/**
//	 * Test case for successful deletion of an Oem.
//	 */
//	@Test
//	public void testDeleteOemSuccess() {
//		// Arrange
//		UUID oemId = UUID.randomUUID();
//		when(oemRepository.existsById(oemId)).thenReturn(true);
//		doNothing().when(oemRepository).deleteById(oemId);
//
//		// Act & Assert
//		assertDoesNotThrow(() -> oemService.deleteOem(oemId));
//	}
//
//	/**
//	 * Test case for finding an Oem by id when it exists.
//	 */
//	@Test
//	public void testFindByIdReturnsOemCreateDTO() {
//		// Arrange
//		UUID oemId = UUID.randomUUID();
//		Oem oem = new Oem();
//		oem.setName("Test Manufacturer");
//		when(oemRepository.findById(oemId)).thenReturn(Optional.of(oem));
//
//		// Act
//		OemDTO result = oemService.findById(oemId);
//
//		// Assert
//		assertNotNull(result);
//	}
//
//	/**
//	 * Test case for finding an Oem by id when it does not exist.
//	 */
//	@Test
//	public void testFindByIdThrowsResourceNotFoundException() {
//		// Arrange
//		UUID oemId = UUID.randomUUID();
//		when(oemRepository.findById(oemId)).thenReturn(Optional.empty());
//
//		// Act & Assert
//		assertThrows(ResourceNotFoundException.class, () -> oemService.findById(oemId));
//	}
//
//	/**
//	 * Test case for retrieving Oems by category when there are some present.
//	 */
//	@Test
//	public void testGetOemsByCategoryReturnsList() {
//		// Arrange
//		String category = "RDKV";
//		Oem oem = new Oem();
//		oem.setName("Test Manufacturer");
//		when(oemRepository.findByCategory(Category.getCategory(category))).thenReturn(Arrays.asList(oem));
//
//		// Act
//		List<OemDTO> result = oemService.getOemsByCategory(category);
//
//		// Assert
//		assertNotNull(result);
//		assertFalse(result.isEmpty());
//	}
//
//	/**
//	 * Test case for retrieving Oems by category when there are none.
//	 */
//	@Test
//	public void testGetOemsByCategoryReturnsNull() {
//		// Arrange
//		String category = "RDKV";
//		when(oemRepository.findByCategory(Category.getCategory(category))).thenReturn(Collections.emptyList());
//
//		// Act
//		List<OemDTO> result = oemService.getOemsByCategory(category);
//
//		// Assert
//		assertNull(result);
//	}
//
//	/**
//	 * Test case for retrieving a list of Oem names by category when there are some
//	 * present.
//	 */
//	@Test
//	public void testGetOemListByCategoryReturnsList() {
//		// Arrange
//		String category = "RDKV";
//		Oem oem = new Oem();
//		oem.setName("Test Manufacturer");
//		when(oemRepository.findByCategory(Category.getCategory(category))).thenReturn(Arrays.asList(oem));
//
//		// Act
//		List<String> result = oemService.getOemListByCategory(category);
//
//		// Assert
//		assertNotNull(result);
//		assertFalse(result.isEmpty());
//	}
//
//	/**
//	 * Test case for retrieving a list of Oem names by category when there are none.
//	 */
//	@Test
//	public void testGetOemListByCategoryReturnsNull() {
//		// Arrange
//		String category = "RDKV";
//		when(oemRepository.findByCategory(Category.getCategory(category))).thenReturn(Collections.emptyList());
//
//		// Act
//		List<String> result = oemService.getOemListByCategory(category);
//
//		// Assert
//		assertNull(result);
//	}
//
//	/**
//	 * Test case for updating an Oem when it does not exist.
//	 */
//	@Test
//	public void testUpdateOemThrowsResourceNotFoundException() {
//		// Arrange
//		UUID oemId = UUID.randomUUID();
//		OemDTO oemUpdateDTO = new OemDTO();
//		oemUpdateDTO.setOemId(oemId);
//		oemUpdateDTO.setOemName("Test Manufacturer");
//		when(oemRepository.findById(oemId)).thenReturn(Optional.empty());
//
//		// Act & Assert
//		assertThrows(ResourceNotFoundException.class, () -> oemService.updateOem(oemUpdateDTO));
//	}
//
//	/**
//	 * Test case for successful update of a oem.
//	 */
//	@Test
//	public void testUpdateOemSuccess() {
//
//		// Arrange
//		UUID oemId = UUID.randomUUID();
//		OemDTO oemUpdateDTO = new OemDTO();
//		oemUpdateDTO.setOemId(oemId);
//		oemUpdateDTO.setOemName("Test");
//		oemUpdateDTO.setOemCategory("RDKV");
//		Oem oem = new Oem();
//		oem.setId(oemId);
//		oem.setName("Test Manufacturer");
//		oem.setCategory(Category.RDKB);
//
//		when(oemRepository.findById(oemId)).thenReturn(Optional.of(oem));
//
//		when(oemRepository.existsByName(oemUpdateDTO.getOemName())).thenReturn(false);
//		when(oemRepository.save(any(Oem.class))).thenReturn(oem);
//		OemDTO result = oemService.updateOem(oemUpdateDTO);
//
//		assertEquals("Test", result.getOemName());
//		assertEquals(Category.RDKV.name(), result.getOemCategory());
//
//	}
//}
