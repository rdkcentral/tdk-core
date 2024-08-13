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

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.dao.DataIntegrityViolationException;

import com.rdkm.tdkservice.dto.BoxTypeDTO;
import com.rdkm.tdkservice.dto.BoxTypeUpdateDTO;
import com.rdkm.tdkservice.enums.BoxTypeCategory;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.BoxType;
import com.rdkm.tdkservice.model.BoxtypeSubBoxtypeMap;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.BoxTypeRepository;
import com.rdkm.tdkservice.repository.BoxtypeSubBoxtypeMapRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;

/*
 * The Test class for BoxTypeService Class
 */
public class BoxTypeServiceTest {

	@Mock
	private BoxTypeRepository boxTypeRepository;

	@InjectMocks
	private BoxTypeService boxTypeService;

	@Mock
	private UserGroupRepository userGroupRepository;

	@Mock
	private BoxtypeSubBoxtypeMapRepository boxtypeSubBoxtypeMapRepository;

	/**
	 * Setup method for each test case.
	 */
	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	/**
	 * This test case verifies that a ResourceAlreadyExistsException is thrown when
	 * trying to create a box type that already exists.
	 */
	@Test
	public void testCreateBoxType_ResourceAlreadyExistsException() {
		BoxTypeDTO boxTypeDTO = new BoxTypeDTO();
		boxTypeDTO.setBoxTypeName("BoxType1");

		when(boxTypeRepository.existsByName(anyString())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> {
			boxTypeService.createBoxType(boxTypeDTO);
		});
	}

	/**
	 * This test case verifies that a ResourceNotFoundException is thrown when
	 * trying to create a box type with an invalid type.
	 */
	@Test
	public void testCreateBoxType_ResourceNotFoundException() {
		BoxTypeDTO boxTypeDTO = new BoxTypeDTO();
		boxTypeDTO.setBoxTypeName("BoxType1");
		boxTypeDTO.setType("InvalidType");

		when(boxTypeRepository.existsByName(anyString())).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> {
			boxTypeService.createBoxType(boxTypeDTO);
		});
	}

	/**
	 * This test case verifies that a box type can be successfully created when all
	 * the required conditions are met.
	 */
	@Test
	public void testCreateBoxType_Success() {
		BoxTypeDTO boxTypeDTO = new BoxTypeDTO();

		boxTypeDTO.setBoxTypeName("BoxType1");
		boxTypeDTO.setType(BoxTypeCategory.GATEWAY.getName());
		boxTypeDTO.setBoxCategory("RDKV");
		boxTypeDTO.setBoxUserGroup("userGroup1");
		boxTypeDTO.setSubBoxTypes(List.of("subBoxType1", "subBoxType2"));

		BoxType boxType = new BoxType();
		boxType.setId(1);
		boxType.setName("BoxType1");
		boxType.setType(BoxTypeCategory.GATEWAY);
		boxType.setCategory(Category.RDKV);
		boxType.setUserGroup(new UserGroup());

		when(boxTypeRepository.existsByName(anyString())).thenReturn(false);
		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());
		when(boxTypeRepository.save(any())).thenReturn(boxType);
		when(boxTypeRepository.findByName(anyString())).thenReturn(new BoxType());

		assertTrue(boxTypeService.createBoxType(boxTypeDTO));
	}

	/**
	 * This test case verifies that a RuntimeException is thrown when the repository
	 * fails to save the box type.
	 */
	@Test
	public void testCreateBoxType_Exception() {
		BoxTypeDTO boxTypeDTO = new BoxTypeDTO();
		boxTypeDTO.setBoxTypeName("BoxType1");
		boxTypeDTO.setType(BoxTypeCategory.GATEWAY.getName());
		boxTypeDTO.setBoxCategory("RDKV");

		when(boxTypeRepository.existsByName(anyString())).thenReturn(false);
		when(boxTypeRepository.save(any())).thenThrow(RuntimeException.class);

		assertFalse(boxTypeService.createBoxType(boxTypeDTO));
	}

	/**
	 * This test case verifies that null is returned when there are no box types in
	 * the repository.
	 */
	@Test
	public void testGetAllBoxTypesReturnsNull() {
		// Arrange
		when(boxTypeRepository.findAll()).thenReturn(new ArrayList<>());

		// Act
		List<BoxTypeDTO> result = boxTypeService.getAllBoxTypes();

		// Assert
		assertNull(result);
	}

	/**
	 * This test case verifies that a box type can be successfully deleted by its
	 * id.
	 */
	@Test
	public void testDeleteByIdSuccess() {
		// Arrange
		Integer id = 1;
		BoxType boxType = new BoxType();
		boxType.setId(id);
		when(boxTypeRepository.findById(id)).thenReturn(Optional.of(boxType));

		// Act
		boxTypeService.deleteById(id);

		// Assert
		verify(boxTypeRepository, times(1)).deleteById(id);
	}

	/**
	 * This test case verifies that a ResourceNotFoundException is thrown when
	 * trying to delete a box type by an invalid id.
	 */
	@Test
	public void testDeleteByIdResourceNotFound() {
		// Arrange
		Integer id = 1;
		when(boxTypeRepository.findById(id)).thenReturn(Optional.empty());

		// Act & Assert
		assertThrows(ResourceNotFoundException.class, () -> boxTypeService.deleteById(id));
	}

	/**
	 * This test case verifies that a DeleteFailedException is thrown when the
	 * repository fails to delete the box type.
	 */
	@Test
	public void testDeleteByIdDeleteFailed() {
		// Arrange
		Integer id = 1;
		BoxType boxType = new BoxType();
		boxType.setId(id);
		when(boxTypeRepository.findById(id)).thenReturn(Optional.of(boxType));
		doThrow(DataIntegrityViolationException.class).when(boxTypeRepository).deleteById(id);

		// Act & Assert
		assertThrows(DeleteFailedException.class, () -> boxTypeService.deleteById(id));
	}

	/**
	 * This test case verifies that a box type can be successfully found by its id.
	 */
	@Test
	public void testFindByIdSuccess() {
		// Arrange
		Integer id = 1;
		BoxType boxType = new BoxType();
		boxType.setId(id);
		when(boxTypeRepository.findById(id)).thenReturn(Optional.of(boxType));

		// Act
		BoxTypeDTO result = boxTypeService.findById(id);

		// Assert
		assertNotNull(result);

	}

	/**
	 * This test case verifies that a ResourceNotFoundException is thrown when
	 * trying to find a box type by an invalid id.
	 */
	@Test
	public void testFindByIdResourceNotFound() {
		// Arrange
		Integer id = 1;
		when(boxTypeRepository.findById(id)).thenReturn(Optional.empty());

		// Act & Assert
		assertThrows(ResourceNotFoundException.class, () -> boxTypeService.findById(id));
	}

	/**
	 * This test case verifies that a box type can be successfully updated.
	 */
	@Test
	public void testUpdateBoxType() {
		BoxTypeUpdateDTO boxTypeUpdateDTO = new BoxTypeUpdateDTO();
		boxTypeUpdateDTO.setBoxTypeName("New Box Type");
		boxTypeUpdateDTO.setBoxType(BoxTypeCategory.CLIENT.getName());
		boxTypeUpdateDTO.setBoxTypeCategory(Category.RDKB.getName());
		boxTypeUpdateDTO.setSubBoxTypes(List.of("Sub Box Type 1", "Sub Box Type 2"));

		BoxType existingBoxType = new BoxType();
		existingBoxType.setName("Existing Box Type");
		existingBoxType.setType(BoxTypeCategory.getBoxTypeCategory("GATEWAY"));
		existingBoxType.setCategory(Category.getCategory("RDKV"));

		BoxtypeSubBoxtypeMap boxtypeSubBoxtypeMap = new BoxtypeSubBoxtypeMap();
		boxtypeSubBoxtypeMap.setBoxTypeName("Existing Box Type");
		boxtypeSubBoxtypeMap.setSubBoxType(new BoxType());

		when(boxtypeSubBoxtypeMapRepository.findByBoxTypeName(anyString())).thenReturn(List.of(boxtypeSubBoxtypeMap));

		when(boxTypeRepository.findById(anyInt())).thenReturn(java.util.Optional.of(existingBoxType));
		when(boxTypeRepository.existsByName(anyString())).thenReturn(false);
		when(boxTypeRepository.save(any(BoxType.class))).thenReturn(existingBoxType);

		BoxTypeUpdateDTO updatedBoxType = boxTypeService.updateBoxType(boxTypeUpdateDTO, 1);

		assertEquals(boxTypeUpdateDTO.getBoxTypeName(), updatedBoxType.getBoxTypeName());
		assertEquals(boxTypeUpdateDTO.getBoxType(), updatedBoxType.getBoxType());
		assertEquals(boxTypeUpdateDTO.getBoxTypeCategory(), updatedBoxType.getBoxTypeCategory());
	}

	/**
	 * This test case verifies that box types can be successfully retrieved by their
	 * category.
	 */
	@Test
	public void testGetBoxTypesByCategoryReturnsBoxTypes() {
		String category = "RDKV";
		BoxType boxType1 = new BoxType();
		boxType1.setName("BoxType1");
		boxType1.setCategory(Category.getCategory(category));

		BoxType boxType2 = new BoxType();
		boxType2.setName("BoxType2");
		boxType2.setCategory(Category.getCategory(category));

		when(boxTypeRepository.findByCategory(Category.getCategory(category))).thenReturn(List.of(boxType1, boxType2));

		List<BoxTypeDTO> result = boxTypeService.getBoxTypesByCategory(category);

		assertEquals(2, result.size());
	}

	/**
	 * This test case verifies that null is returned when there are no box types in
	 * the specified category.
	 */
	@Test
	public void testGetBoxTypeNameByCategoryReturnsNull() {
		String category = "category1";
		when(boxTypeRepository.findByCategory(Category.getCategory(category))).thenReturn(Collections.emptyList());

		List<String> result = boxTypeService.getBoxTypeNameByCategory(category);

		assertNull(result);
	}

	/**
	 * This test case verifies that box type names can be successfully retrieved by
	 * their category.
	 */
	@Test
	public void testGetBoxTypeNameByCategoryReturnsBoxTypeNames() {
		String category = "category2";
		BoxType boxType1 = new BoxType();
		boxType1.setName("BoxType1");
		boxType1.setCategory(Category.getCategory(category));

		BoxType boxType2 = new BoxType();
		boxType2.setName("BoxType2");
		boxType2.setCategory(Category.getCategory(category));

		when(boxTypeRepository.findByCategory(Category.getCategory(category))).thenReturn(List.of(boxType1, boxType2));

		List<String> result = boxTypeService.getBoxTypeNameByCategory(category);

		assertEquals(2, result.size());
	}

	/**
	 * This test case verifies that a box type is a gateway.
	 */
	@Test
	public void testIsTheBoxTypeGatewayReturnsTrue() {
		String boxTypeName = "BoxType1";
		BoxType boxType = new BoxType();
		boxType.setName(boxTypeName);
		boxType.setType(BoxTypeCategory.GATEWAY);

		when(boxTypeRepository.findByName(boxTypeName)).thenReturn(boxType);

		boolean result = boxTypeService.isTheBoxTypeGateway(boxTypeName);

		assertTrue(result);
	}

	/**
	 * This test case verifies that a box type is not a gateway.
	 */
	@Test
	public void testIsTheBoxTypeGatewayReturnsFalse() {
		String boxTypeName = "BoxType2";
		BoxType boxType = new BoxType();
		boxType.setName(boxTypeName);
		boxType.setType(BoxTypeCategory.CLIENT);

		when(boxTypeRepository.findByName(boxTypeName)).thenReturn(boxType);

		boolean result = boxTypeService.isTheBoxTypeGateway(boxTypeName);

		assertFalse(result);
	}

	/**
	 * This test case verifies that all box types can be successfully retrieved.
	 */
	@Test
	public void testGetAllBoxTypes_Success() {
		// Arrange
		BoxType boxType1 = new BoxType();
		boxType1.setName("BoxType1");

		BoxType boxType2 = new BoxType();
		boxType2.setName("BoxType2");

		when(boxTypeRepository.findAll()).thenReturn(List.of(boxType1, boxType2));

		// Act
		List<BoxTypeDTO> result = boxTypeService.getAllBoxTypes();

		// Assert
		assertNotNull(result);
		assertEquals(2, result.size());
		verify(boxTypeRepository, times(1)).findAll();
	}
}
