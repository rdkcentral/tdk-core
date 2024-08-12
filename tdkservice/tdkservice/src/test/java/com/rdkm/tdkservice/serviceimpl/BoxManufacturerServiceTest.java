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

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.when;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.dao.DataIntegrityViolationException;

import com.rdkm.tdkservice.dto.BoxManufacturerDTO;
import com.rdkm.tdkservice.dto.BoxManufacturerUpdateDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.BoxManufacturer;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.BoxManufacturerRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;

/**
 * This class is used to test the BoxManufacturerService class. It uses Mockito
 * to mock the repository layer and JUnit for the testing framework.
 */
public class BoxManufacturerServiceTest {

	/**
	 * The service that is being tested.
	 */
	@InjectMocks
	private BoxManufacturerService boxManufacturerService;

	/**
	 * The repository for BoxManufacturer entities.
	 */
	@Mock
	private BoxManufacturerRepository boxManufacturerRepository;

	/**
	 * The repository for UserGroup entities.
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
	 * Test case for successful creation of a BoxManufacturer.
	 */
	@Test
	public void testCreateBoxManufacturer_Success() {
		BoxManufacturerDTO boxManufacturerDTO = new BoxManufacturerDTO();
		boxManufacturerDTO.setBoxManufacturerName("Test Manufacturer");
		boxManufacturerDTO.setBoxManufacturerCategory("RDKV");
		boxManufacturerDTO.setBoxManufacturerUserGroup("UserGroup1");

		BoxManufacturer boxManufacturer = new BoxManufacturer();
		boxManufacturer.setId(1);
		boxManufacturer.setName("Test Manufacturer");
		boxManufacturer.setCategory(Category.RDKV);
		boxManufacturer.setUserGroup(new UserGroup());

		when(boxManufacturerRepository.existsByName(anyString())).thenReturn(false);
		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());
		when(boxManufacturerRepository.save(any())).thenReturn(boxManufacturer);

		assertTrue(boxManufacturerService.createBoxManufacturer(boxManufacturerDTO));
	}

	/**
	 * Test case for creation of a BoxManufacturer when a BoxManufacturer with the
	 * same name already exists.
	 */
	@Test
	public void testCreateBoxManufacturer_ResourceAlreadyExistsException() {
		BoxManufacturerDTO boxManufacturerDTO = new BoxManufacturerDTO();
		boxManufacturerDTO.setBoxManufacturerName("Test Manufacturer");

		when(boxManufacturerRepository.existsByName(anyString())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class,
				() -> boxManufacturerService.createBoxManufacturer(boxManufacturerDTO));
	}

	/**
	 * Test case for creation of a BoxManufacturer when the category is invalid.
	 */
	@Test
	public void testCreateBoxManufacturer_ResourceNotFoundException() {
		BoxManufacturerDTO boxManufacturerDTO = new BoxManufacturerDTO();
		boxManufacturerDTO.setBoxManufacturerName("Test Manufacturer");
		boxManufacturerDTO.setBoxManufacturerCategory("Invalid Category");

		when(boxManufacturerRepository.existsByName(anyString())).thenReturn(false);

		assertThrows(ResourceNotFoundException.class,
				() -> boxManufacturerService.createBoxManufacturer(boxManufacturerDTO));
	}

	/**
	 * Test case for creation of a BoxManufacturer when an exception occurs while
	 * saving the BoxManufacturer.
	 */
	@Test
	public void testCreateBoxManufacturer_ExceptionWhileSaving() {
		BoxManufacturerDTO boxManufacturerDTO = new BoxManufacturerDTO();
		boxManufacturerDTO.setBoxManufacturerName("Test Manufacturer");
		boxManufacturerDTO.setBoxManufacturerCategory("RDKB");
		boxManufacturerDTO.setBoxManufacturerUserGroup("Test User Group");

		when(boxManufacturerRepository.existsByName(anyString())).thenReturn(false);
		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());
		when(boxManufacturerRepository.save(any())).thenThrow(new RuntimeException());

		assertFalse(boxManufacturerService.createBoxManufacturer(boxManufacturerDTO));
	}

	/**
	 * Test case for retrieving all BoxManufacturers when there are some present.
	 */
	@Test
	public void testGetAllBoxManufacturerReturnsList() {
		// Arrange
		BoxManufacturer boxManufacturer = new BoxManufacturer();
		boxManufacturer.setName("Test Manufacturer");
		when(boxManufacturerRepository.findAll()).thenReturn(Arrays.asList(boxManufacturer));

		// Act
		List<BoxManufacturerDTO> result = boxManufacturerService.getAllBoxManufacturer();

		// Assert
		assertNotNull(result);
		assertFalse(result.isEmpty());
	}

	/**
	 * Test case for retrieving all BoxManufacturers when there are none.
	 */
	@Test
	public void testGetAllBoxManufacturerReturnsNull() {
		// Arrange
		when(boxManufacturerRepository.findAll()).thenReturn(Collections.emptyList());

		// Act
		List<BoxManufacturerDTO> result = boxManufacturerService.getAllBoxManufacturer();

		// Assert
		assertNull(result);
	}

	/**
	 * Test case for deleting a BoxManufacturer when it does not exist.
	 */
	@Test
	public void testDeleteBoxManufacturerThrowsResourceNotFoundException() {
		// Arrange
		Integer id = 1;
		when(boxManufacturerRepository.existsById(id)).thenReturn(false);

		// Act & Assert
		assertThrows(ResourceNotFoundException.class, () -> boxManufacturerService.deleteBoxManufacturer(id));
	}

	/**
	 * Test case for deleting a BoxManufacturer when an exception occurs while
	 * deleting.
	 */
	@Test
	public void testDeleteBoxManufacturerThrowsDeleteFailedException() {
		// Arrange
		Integer id = 1;
		when(boxManufacturerRepository.existsById(id)).thenReturn(true);
		doThrow(DataIntegrityViolationException.class).when(boxManufacturerRepository).deleteById(id);

		// Act & Assert
		assertThrows(DeleteFailedException.class, () -> boxManufacturerService.deleteBoxManufacturer(id));
	}

	/**
	 * Test case for successful deletion of a BoxManufacturer.
	 */
	@Test
	public void testDeleteBoxManufacturerSuccess() {
		// Arrange
		Integer id = 1;
		when(boxManufacturerRepository.existsById(id)).thenReturn(true);
		doNothing().when(boxManufacturerRepository).deleteById(id);

		// Act & Assert
		assertDoesNotThrow(() -> boxManufacturerService.deleteBoxManufacturer(id));
	}

	/**
	 * Test case for finding a BoxManufacturer by id when it exists.
	 */
	@Test
	public void testFindByIdReturnsBoxManufacturerDTO() {
		// Arrange
		Integer id = 1;
		BoxManufacturer boxManufacturer = new BoxManufacturer();
		boxManufacturer.setName("Test Manufacturer");
		when(boxManufacturerRepository.findById(id)).thenReturn(Optional.of(boxManufacturer));

		// Act
		BoxManufacturerDTO result = boxManufacturerService.findById(id);

		// Assert
		assertNotNull(result);
	}

	/**
	 * Test case for finding a BoxManufacturer by id when it does not exist.
	 */
	@Test
	public void testFindByIdThrowsResourceNotFoundException() {
		// Arrange
		Integer id = 1;
		when(boxManufacturerRepository.findById(id)).thenReturn(Optional.empty());

		// Act & Assert
		assertThrows(ResourceNotFoundException.class, () -> boxManufacturerService.findById(id));
	}

	/**
	 * Test case for retrieving BoxManufacturers by category when there are some
	 * present.
	 */
	@Test
	public void testGetBoxManufacturersByCategoryReturnsList() {
		// Arrange
		String category = "RDKV";
		BoxManufacturer boxManufacturer = new BoxManufacturer();
		boxManufacturer.setName("Test Manufacturer");
		when(boxManufacturerRepository.findByCategory(Category.getCategory(category)))
				.thenReturn(Arrays.asList(boxManufacturer));

		// Act
		List<BoxManufacturerDTO> result = boxManufacturerService.getBoxManufacturersByCategory(category);

		// Assert
		assertNotNull(result);
		assertFalse(result.isEmpty());
	}

	/**
	 * Test case for retrieving BoxManufacturers by category when there are none.
	 */
	@Test
	public void testGetBoxManufacturersByCategoryReturnsNull() {
		// Arrange
		String category = "RDKV";
		when(boxManufacturerRepository.findByCategory(Category.getCategory(category)))
				.thenReturn(Collections.emptyList());

		// Act
		List<BoxManufacturerDTO> result = boxManufacturerService.getBoxManufacturersByCategory(category);

		// Assert
		assertNull(result);
	}

	/**
	 * Test case for retrieving a list of BoxManufacturer names by category when
	 * there are some present.
	 */
	@Test
	public void testGetBoxManufacturerListByCategoryReturnsList() {
		// Arrange
		String category = "RDKV";
		BoxManufacturer boxManufacturer = new BoxManufacturer();
		boxManufacturer.setName("Test Manufacturer");
		when(boxManufacturerRepository.findByCategory(Category.getCategory(category)))
				.thenReturn(Arrays.asList(boxManufacturer));

		// Act
		List<String> result = boxManufacturerService.getBoxManufacturerListByCategory(category);

		// Assert
		assertNotNull(result);
		assertFalse(result.isEmpty());
	}

	/**
	 * Test case for retrieving a list of BoxManufacturer names by category when
	 * there are none.
	 */
	@Test
	public void testGetBoxManufacturerListByCategoryReturnsNull() {
		// Arrange
		String category = "RDKV";
		when(boxManufacturerRepository.findByCategory(Category.getCategory(category)))
				.thenReturn(Collections.emptyList());

		// Act
		List<String> result = boxManufacturerService.getBoxManufacturerListByCategory(category);

		// Assert
		assertNull(result);
	}

	/**
	 * Test case for updating a BoxManufacturer when it does not exist.
	 */
	@Test
	public void testUpdateBoxManufacturerThrowsResourceNotFoundException() {
		// Arrange
		Integer id = 1;
		BoxManufacturerUpdateDTO boxManufacturerUpdateDTO = new BoxManufacturerUpdateDTO();
		boxManufacturerUpdateDTO.setBoxManufacturerName("Test Manufacturer");
		when(boxManufacturerRepository.findById(id)).thenReturn(Optional.empty());

		// Act & Assert
		assertThrows(ResourceNotFoundException.class,
				() -> boxManufacturerService.updateBoxManufacturer(boxManufacturerUpdateDTO, id));
	}

	/**
	 * Test case for updating a BoxManufacturer when a BoxManufacturer with the new
	 * name already exists.
	 */
	@Test
	public void testUpdateBoxManufacturerThrowsResourceAlreadyExistsException() {
		// Arrange
		Integer id = 1;
		BoxManufacturerUpdateDTO boxManufacturerUpdateDTO = new BoxManufacturerUpdateDTO();
		boxManufacturerUpdateDTO.setBoxManufacturerName("Test Manufacturer");
		BoxManufacturer boxManufacturer = new BoxManufacturer();
		boxManufacturer.setName("Test Manufacturer");
		when(boxManufacturerRepository.findById(id)).thenReturn(Optional.of(boxManufacturer));
		when(boxManufacturerRepository.existsByName(boxManufacturerUpdateDTO.getBoxManufacturerName()))
				.thenReturn(true);

		// Act & Assert
		assertThrows(ResourceAlreadyExistsException.class,
				() -> boxManufacturerService.updateBoxManufacturer(boxManufacturerUpdateDTO, id));
	}

	/**
	 * Test case for successful update of a BoxManufacturer.
	 */
	@Test
	public void testUpdateBoxManufacturerSuccess() {

		// Arrange
		Integer id = 1;
		BoxManufacturerUpdateDTO boxManufacturerUpdateDTO = new BoxManufacturerUpdateDTO();
		boxManufacturerUpdateDTO.setBoxManufacturerName("Test");
		boxManufacturerUpdateDTO.setBoxManufacturerCategory("RDKV");
		BoxManufacturer boxManufacturer = new BoxManufacturer();
		boxManufacturer.setId(1);
		boxManufacturer.setName("Test Manufacturer");
		boxManufacturer.setCategory(Category.RDKB);

		when(boxManufacturerRepository.findById(anyInt())).thenReturn(Optional.of(boxManufacturer));

		when(boxManufacturerRepository.existsByName(boxManufacturerUpdateDTO.getBoxManufacturerName()))
				.thenReturn(false);
		when(boxManufacturerRepository.save(any(BoxManufacturer.class))).thenReturn(boxManufacturer);
		BoxManufacturerUpdateDTO result = boxManufacturerService.updateBoxManufacturer(boxManufacturerUpdateDTO, id);

		assertEquals("Test", result.getBoxManufacturerName());
		assertEquals(Category.RDKV.name(), result.getBoxManufacturerCategory());

	}
}
