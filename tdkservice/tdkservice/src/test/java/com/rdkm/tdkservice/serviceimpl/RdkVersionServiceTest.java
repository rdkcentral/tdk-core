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
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.dao.DataIntegrityViolationException;

import com.rdkm.tdkservice.dto.RdkVersionCreateDTO;
import com.rdkm.tdkservice.dto.RdkVersionDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.RdkVersion;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.RdkVersionRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;

/**
 * Test class for RdkVersionService.
 */
public class RdkVersionServiceTest {

	@InjectMocks
	private RdkVersionService rdkVersionService;

	@Mock
	private RdkVersionRepository rdkVersionRepository;

	@Mock
	private UserGroupRepository userGroupRepository;

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
	public void createRdkVersionSuccessfully() {
		RdkVersionCreateDTO rdkVersionCreateDTO = new RdkVersionCreateDTO();
		rdkVersionCreateDTO.setBuildVersionName("1.0.0");
		rdkVersionCreateDTO.setRdkVersionCategory("RDKB");
		rdkVersionCreateDTO.setRdkVersionUserGroup("UserGroup1");

		when(rdkVersionRepository.existsByName(anyString())).thenReturn(false);
		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());

		assertTrue(rdkVersionService.createRdkVersion(rdkVersionCreateDTO));
	}

	/**
	 * Test case for RDK version creation with invalid category.
	 */
	@Test
	public void createRdkVersionWithInvalidCategory() {
		RdkVersionCreateDTO rdkVersionCreateDTO = new RdkVersionCreateDTO();
		rdkVersionCreateDTO.setBuildVersionName("1.0.0");
		rdkVersionCreateDTO.setRdkVersionCategory("RKV");
		rdkVersionCreateDTO.setRdkVersionUserGroup("UserGroup1");

		when(rdkVersionRepository.existsByName(anyString())).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> rdkVersionService.createRdkVersion(rdkVersionCreateDTO));
	}

	/**
	 * Test case for RDK version creation with existing name.
	 */
	@Test
	public void createRdkVersionWithExistingName() {
		RdkVersionCreateDTO rdkVersionCreateDTO = new RdkVersionCreateDTO();
		rdkVersionCreateDTO.setBuildVersionName("1.0.0");
		rdkVersionCreateDTO.setRdkVersionCategory("RDKV");
		rdkVersionCreateDTO.setRdkVersionUserGroup("UserGroup1");

		when(rdkVersionRepository.existsByName(anyString())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class,
				() -> rdkVersionService.createRdkVersion(rdkVersionCreateDTO));
	}

	/**
	 * Test case for successful RDK version update.
	 */
	@Test
	public void updateRdkVersionSuccessfully() {
		RdkVersionDTO rdkVersionDTO = new RdkVersionDTO();
		rdkVersionDTO.setRdkVersionId(1);
		rdkVersionDTO.setBuildVersionName("1.0.1");
		rdkVersionDTO.setRdkVersionCategory("RDKB");

		when(rdkVersionRepository.findById(anyInt())).thenReturn(Optional.of(new RdkVersion()));
		when(rdkVersionRepository.existsByName(anyString())).thenReturn(false);

		assertTrue(rdkVersionService.updateRdkVersion(rdkVersionDTO));
	}

	/**
	 * Test case for RDK version update with non-existing id.
	 */
	@Test
	public void updateRdkVersionWithNonExistingId() {
		RdkVersionDTO rdkVersionDTO = new RdkVersionDTO();
		rdkVersionDTO.setRdkVersionId(1);
		rdkVersionDTO.setBuildVersionName("1.0.1");
		rdkVersionDTO.setRdkVersionCategory("RDKV");

		when(rdkVersionRepository.findById(anyInt())).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> rdkVersionService.updateRdkVersion(rdkVersionDTO));
	}

	/**
	 * Test case for successful RDK version deletion.
	 */
	@Test
	public void deleteRdkVersionSuccessfully() {
		when(rdkVersionRepository.findById(anyInt())).thenReturn(Optional.of(new RdkVersion()));

		assertDoesNotThrow(() -> rdkVersionService.deleteRdkVersion(1));
	}

	/**
	 * Test case for RDK version deletion with non-existing id.
	 */
	@Test
	public void deleteNonExistingRdkVersion() {
		when(rdkVersionRepository.findById(anyInt())).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> rdkVersionService.deleteRdkVersion(1));
	}

	/**
	 * Test case for RDK version update with existing name.
	 */
	@Test
	public void updateRdkVersionWithExistingName() {
		RdkVersionDTO rdkVersionDTO = new RdkVersionDTO();
		rdkVersionDTO.setRdkVersionId(1);
		rdkVersionDTO.setBuildVersionName("1.0.0"); // This name already exists
		rdkVersionDTO.setRdkVersionCategory("RDKV");

		when(rdkVersionRepository.findById(anyInt())).thenReturn(Optional.of(new RdkVersion()));
		when(rdkVersionRepository.existsByName(anyString())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> rdkVersionService.updateRdkVersion(rdkVersionDTO));
	}

	/**
	 * Test case for RDK version update with invalid category.
	 */
	@Test
	public void updateRdkVersionWithInvalidCategory() {
		RdkVersionDTO rdkVersionDTO = new RdkVersionDTO();
		rdkVersionDTO.setRdkVersionId(1);
		rdkVersionDTO.setBuildVersionName("1.0.0"); // This name already exists
		rdkVersionDTO.setRdkVersionCategory("RDKb");

		when(rdkVersionRepository.findById(anyInt())).thenReturn(Optional.of(new RdkVersion()));
		when(rdkVersionRepository.existsByName(anyString())).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> rdkVersionService.updateRdkVersion(rdkVersionDTO));
	}

	/**
	 * Test case for RDK version deletion with delete exception.
	 */
	@Test
	public void testDeleteRdkVersion_DeleteFailedException() {
		// Arrange
		Integer id = 1;
		RdkVersion rdkVersion = new RdkVersion();
		rdkVersion.setId(id);

		when(rdkVersionRepository.findById(id)).thenReturn(Optional.of(rdkVersion));
		doThrow(DataIntegrityViolationException.class).when(rdkVersionRepository).delete(rdkVersion);

		// Act and Assert
		assertThrows(DeleteFailedException.class, () -> rdkVersionService.deleteRdkVersion(id));

		verify(rdkVersionRepository, times(1)).findById(id);
		verify(rdkVersionRepository, times(1)).delete(rdkVersion);
	}

	/**
	 * Test case for retrieval of all RDK versions when list is empty.
	 */
	@Test
	public void testFindAllRdkVersions_EmptyList() {
		// Arrange
		when(rdkVersionRepository.findAll()).thenReturn(Collections.emptyList());

		// Act
		List<RdkVersionDTO> result = rdkVersionService.findAllRdkVersions();

		// Assert
		assertTrue(result == null || result.isEmpty());
	}

	/**
	 * Test case for successful retrieval of all RDK versions.
	 */
	@Test
	public void testFindAllRdkVersions_ReturnsList() {
		// Arrange
		RdkVersion rdkVersion = new RdkVersion();
		rdkVersion.setId(1);
		rdkVersion.setCategory(Category.RDKB);
		when(rdkVersionRepository.findAll()).thenReturn(Collections.singletonList(rdkVersion));
		// Act
		List<RdkVersionDTO> result = rdkVersionService.findAllRdkVersions();
		// Assert
		assertNotNull(result);
		assertFalse(result.isEmpty());
		assertEquals(1, result.size());
		assertEquals(rdkVersion.getId(), result.get(0).getRdkVersionId());
	}

	/**
	 * Test case for successful retrieval of all RDK versions by category.
	 */
	@Test
	public void testFindAllRdkVersionsByCategory() {
		// Arrange
		String category = "RDKB";
		RdkVersion rdkVersion = new RdkVersion();
		rdkVersion.setId(1);
		rdkVersion.setCategory(Category.RDKB);
		when(rdkVersionRepository.findByCategory(Category.getCategory(category)))
				.thenReturn(Collections.singletonList(rdkVersion));

		// Act
		List<RdkVersionDTO> result = rdkVersionService.findAllRdkVersionsByCategory(category);

		// Assert
		assertNotNull(result);
		assertFalse(result.isEmpty());
		assertEquals(1, result.size());
		assertEquals(rdkVersion.getId(), result.get(0).getRdkVersionId());
	}

	/**
	 * Test case for successful retrieval of RDK version list by category.
	 */
	@Test
	public void testGetRdkVersionListByCategory() {
		// Arrange
		String category = "RDKB";
		RdkVersion rdkVersion = new RdkVersion();
		rdkVersion.setId(1);
		rdkVersion.setCategory(Category.RDKB);
		rdkVersion.setName("Version1");
		when(rdkVersionRepository.findByCategory(Category.getCategory(category)))
				.thenReturn(Collections.singletonList(rdkVersion));

		// Act
		List<String> result = rdkVersionService.getRdkVersionListByCategory(category);

		// Assert
		assertNotNull(result);
		assertFalse(result.isEmpty());
		assertEquals(1, result.size());
		assertEquals(rdkVersion.getName(), result.get(0));
	}

	/**
	 * Test case for retrieval of all RDK versions by category when list is empty.
	 */
	@Test
	public void testFindAllRdkVersionsByCategory_ReturnsNull() {
		// Arrange
		String category = "RDKB";
		when(rdkVersionRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		// Act
		List<RdkVersionDTO> result = rdkVersionService.findAllRdkVersionsByCategory(category);

		// Assert
		assertNull(result);
	}

	/**
	 * Test case for retrieval of RDK version list by category when list is empty.
	 */
	@Test
	public void testGetRdkVersionListByCategory_ReturnsNull() {
		// Arrange
		String category = "RDKB";
		when(rdkVersionRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		// Act
		List<String> result = rdkVersionService.getRdkVersionListByCategory(category);

		// Assert
		assertNull(result);
	}

	/**
	 * Test case for successful retrieval of RDK version by id.
	 */
	@Test
	public void testFindRdkVersionById_Success() {
		// Arrange
		Integer id = 1;
		RdkVersion rdkVersion = new RdkVersion();
		rdkVersion.setId(id);
		rdkVersion.setCategory(Category.RDKB);
		when(rdkVersionRepository.findById(id)).thenReturn(Optional.of(rdkVersion));

		// Act
		RdkVersionDTO result = rdkVersionService.findRdkVersionById(id);

		// Assert
		assertNotNull(result);
		assertEquals(rdkVersion.getId(), result.getRdkVersionId());
	}

	/**
	 * Test case for retrieval of RDK version by non-existing id.
	 */
	@Test
	public void testFindRdkVersionById_ThrowsException() {
		// Arrange
		Integer id = 1;
		when(rdkVersionRepository.findById(id)).thenReturn(Optional.empty());

		// Act and Assert
		assertThrows(ResourceNotFoundException.class, () -> rdkVersionService.findRdkVersionById(id));
	}
}
