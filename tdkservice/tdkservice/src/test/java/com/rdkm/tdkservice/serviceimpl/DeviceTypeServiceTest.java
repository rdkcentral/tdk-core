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
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import com.rdkm.tdkservice.dto.DeviceTypeDTO;
import com.rdkm.tdkservice.dto.DeviceTypeUpdateDTO;
import com.rdkm.tdkservice.enums.DeviceTypeCategory;
import com.rdkm.tdkservice.model.DeviceType;
import com.rdkm.tdkservice.repository.DeviceTypeRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.dao.DataIntegrityViolationException;


import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.UserGroupRepository;

/*
 * The Test class for DeviceTypeServiceTest Class
 */
public class DeviceTypeServiceTest {

	@Mock
	private DeviceTypeRepository deviceTypeRepository;

	@InjectMocks
	private DeviceTypeService deviceTypeService;

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
	 * This test case verifies that a ResourceAlreadyExistsException is thrown when
	 * trying to create a device type that already exists.
	 */
	@Test
	public void testCreateDeviceType_ResourceAlreadyExistsException() {
		DeviceTypeDTO deviceTypeDTO = new DeviceTypeDTO();
		deviceTypeDTO.setDeviceTypeName("DeviceType1");

		when(deviceTypeRepository.existsByName(anyString())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> {
			deviceTypeService.createDeviceType(deviceTypeDTO);
		});
	}

	/**
	 * This test case verifies that a ResourceNotFoundException is thrown when
	 * trying to create a device type with an invalid type.
	 */
	@Test
	public void testCreateDeviceType_ResourceNotFoundException() {
		DeviceTypeDTO deviceTypeDTO = new DeviceTypeDTO();
		deviceTypeDTO.setDeviceTypeName("DeviceType1");
		deviceTypeDTO.setType("InvalidType");

		when(deviceTypeRepository.existsByName(anyString())).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> {
			deviceTypeService.createDeviceType(deviceTypeDTO);
		});
	}

	/**
	 * This test case verifies that a device type can be successfully created when all
	 * the required conditions are met.
	 */
	@Test
	public void testCreateDeviceType_Success() {
		DeviceTypeDTO deviceTypeDTO = new DeviceTypeDTO();

		deviceTypeDTO.setDeviceTypeName("DeviceType1");
		deviceTypeDTO.setType(DeviceTypeCategory.CLIENT.getName());
		deviceTypeDTO.setDeviceTypeCategory("RDKV");
		deviceTypeDTO.setDeviceTypeUserGroup("userGroup1");

		DeviceType deviceType = new DeviceType();
		deviceType.setId(1);
		deviceType.setName("DeviceType1");
		deviceType.setType(DeviceTypeCategory.CLIENT);
		deviceType.setCategory(Category.RDKV);
		deviceType.setUserGroup(new UserGroup());

		when(deviceTypeRepository.existsByName(anyString())).thenReturn(false);
		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());
		when(deviceTypeRepository.save(any())).thenReturn(deviceType);
		when(deviceTypeRepository.findByName(anyString())).thenReturn(new DeviceType());

		assertTrue(deviceTypeService.createDeviceType(deviceTypeDTO));
	}

	/**
	 * This test case verifies that a RuntimeException is thrown when the repository
	 * fails to save the device type.
	 */
	@Test
	public void testCreateDeviceType_Exception() {
		DeviceTypeDTO deviceTypeDTO = new DeviceTypeDTO();
		deviceTypeDTO.setDeviceTypeName("DeviceType1");
		deviceTypeDTO.setType(DeviceTypeCategory.CLIENT.getName());
		deviceTypeDTO.setDeviceTypeCategory("RDKV");

		when(deviceTypeRepository.existsByName(anyString())).thenReturn(false);
		when(deviceTypeRepository.save(any())).thenThrow(RuntimeException.class);

		assertFalse(deviceTypeService.createDeviceType(deviceTypeDTO));
	}

	/**
	 * This test case verifies that null is returned when there are no device types in
	 * the repository.
	 */
	@Test
	public void testGetAllDeviceTypesReturnsNull() {
		// Arrange
		when(deviceTypeRepository.findAll()).thenReturn(new ArrayList<>());

		// Act
		List<DeviceTypeDTO> result = deviceTypeService.getAllDeviceTypes();

		// Assert
		assertNull(result);
	}

	/**
	 * This test case verifies that a device type can be successfully deleted by its
	 * id.
	 */
	@Test
	public void testDeleteByIdSuccess() {
		// Arrange
		Integer id = 1;
		DeviceType deviceType = new DeviceType();
		deviceType.setId(id);
		when(deviceTypeRepository.findById(id)).thenReturn(Optional.of(deviceType));

		// Act
		deviceTypeService.deleteById(id);

		// Assert
		verify(deviceTypeRepository, times(1)).deleteById(id);
	}

	/**
	 * This test case verifies that a ResourceNotFoundException is thrown when
	 * trying to delete a device type by an invalid id.
	 */
	@Test
	public void testDeleteByIdResourceNotFound() {
		// Arrange
		Integer id = 1;
		when(deviceTypeRepository.findById(id)).thenReturn(Optional.empty());

		// Act & Assert
		assertThrows(ResourceNotFoundException.class, () -> deviceTypeService.deleteById(id));
	}

	/**
	 * This test case verifies that a DeleteFailedException is thrown when the
	 * repository fails to delete the device type.
	 */
	@Test
	public void testDeleteByIdDeleteFailed() {
		// Arrange
		Integer id = 1;
		DeviceType deviceType = new DeviceType();
		deviceType.setId(id);
		when(deviceTypeRepository.findById(id)).thenReturn(Optional.of(deviceType));
		doThrow(DataIntegrityViolationException.class).when(deviceTypeRepository).deleteById(id);

		// Act & Assert
		assertThrows(DeleteFailedException.class, () -> deviceTypeService.deleteById(id));
	}

	/**
	 * This test case verifies that a device type can be successfully found by its id.
	 */
	@Test
	public void testFindByIdSuccess() {
		// Arrange
		Integer id = 1;
		DeviceType deviceType = new DeviceType();
		deviceType.setId(id);
		when(deviceTypeRepository.findById(id)).thenReturn(Optional.of(deviceType));

		// Act
		DeviceTypeDTO result = deviceTypeService.findById(id);

		// Assert
		assertNotNull(result);
	}

	/**
	 * This test case verifies that a ResourceNotFoundException is thrown when
	 * trying to find a device type by an invalid id.
	 */
	@Test
	public void testFindByIdResourceNotFound() {
		// Arrange
		Integer id = 1;
		when(deviceTypeRepository.findById(id)).thenReturn(Optional.empty());

		// Act & Assert
		assertThrows(ResourceNotFoundException.class, () -> deviceTypeService.findById(id));
	}

	/**
	 * This test case verifies that a device type can be successfully updated.
	 */
	@Test
	public void testUpdateDeviceType() {
		DeviceTypeUpdateDTO deviceTypeUpdateDTO = new DeviceTypeUpdateDTO();
		deviceTypeUpdateDTO.setDeviceTypeName("New Device Type");
		deviceTypeUpdateDTO.setDeviceType(DeviceTypeCategory.CLIENT.getName());
		deviceTypeUpdateDTO.setDeviceTypeCategory(Category.RDKB.getName());

		DeviceType existingDeviceType = new DeviceType();
		existingDeviceType.setName("Existing Device Type");
		existingDeviceType.setType(DeviceTypeCategory.CLIENT);
		existingDeviceType.setCategory(Category.getCategory("RDKV"));

		when(deviceTypeRepository.findById(anyInt())).thenReturn(java.util.Optional.of(existingDeviceType));
		when(deviceTypeRepository.existsByName(anyString())).thenReturn(false);
		when(deviceTypeRepository.save(any(DeviceType.class))).thenReturn(existingDeviceType);

		DeviceTypeUpdateDTO updatedDeviceType = deviceTypeService.updateDeviceType(deviceTypeUpdateDTO, 1);

		assertEquals(deviceTypeUpdateDTO.getDeviceTypeName(), updatedDeviceType.getDeviceTypeName());
		assertEquals(deviceTypeUpdateDTO.getDeviceType(), updatedDeviceType.getDeviceType());
		assertEquals(deviceTypeUpdateDTO.getDeviceTypeCategory(), updatedDeviceType.getDeviceTypeCategory());
	}

	/**
	 * This test case verifies that device types can be successfully retrieved by their
	 * category.
	 */
	@Test
	public void testGetDeviceTypesByCategoryReturnsDeviceTypes() {
		String category = "RDKV";
		DeviceType deviceType1 = new DeviceType();
		deviceType1.setName("DeviceType1");
		deviceType1.setCategory(Category.getCategory(category));

		DeviceType deviceType2 = new DeviceType();
		deviceType2.setName("DeviceType2");
		deviceType2.setCategory(Category.getCategory(category));

		when(deviceTypeRepository.findByCategory(Category.getCategory(category))).thenReturn(List.of(deviceType1, deviceType2));

		List<DeviceTypeDTO> result = deviceTypeService.getDeviceTypesByCategory(category);

		assertEquals(2, result.size());
	}

	/**
	 * This test case verifies that null is returned when there are no device types in
	 * the specified category.
	 */
	@Test
	public void testGetDeviceTypeNameByCategoryReturnsNull() {
		String category = "category1";
		when(deviceTypeRepository.findByCategory(Category.getCategory(category))).thenReturn(Collections.emptyList());

		List<String> result = deviceTypeService.getDeviceTypeNameByCategory(category);

		assertNull(result);
	}

	/**
	 * This test case verifies that device type names can be successfully retrieved by
	 * their category.
	 */
	@Test
	public void testGetDeviceTypeNameByCategoryReturnsDeviceTypeNames() {
		String category = "category2";
		DeviceType deviceType1 = new DeviceType();
		deviceType1.setName("DeviceType1");
		deviceType1.setCategory(Category.getCategory(category));

		DeviceType deviceType2 = new DeviceType();
		deviceType2.setName("DeviceType2");
		deviceType2.setCategory(Category.getCategory(category));

		when(deviceTypeRepository.findByCategory(Category.getCategory(category))).thenReturn(List.of(deviceType1, deviceType2));

		List<String> result = deviceTypeService.getDeviceTypeNameByCategory(category);

		assertEquals(2, result.size());
	}

	/**
	 * This test case verifies that all device types can be successfully retrieved.
	 */
	@Test
	public void testGetAllDeviceTypes_Success() {
		// Arrange
		DeviceType deviceType1 = new DeviceType();
		deviceType1.setName("DeviceType1");

		DeviceType deviceType2 = new DeviceType();
		deviceType2.setName("DeviceType2");

		when(deviceTypeRepository.findAll()).thenReturn(List.of(deviceType1, deviceType2));

		// Act
		List<DeviceTypeDTO> result = deviceTypeService.getAllDeviceTypes();

		// Assert
		assertNotNull(result);
		assertEquals(2, result.size());
		verify(deviceTypeRepository, times(1)).findAll();
	}
}
