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
import static org.mockito.Mockito.doThrow;
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

import com.rdkm.tdkservice.dto.ScriptTagCreateDTO;
import com.rdkm.tdkservice.dto.ScriptTagDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.ScriptTag;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.ScriptTagRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;

/**
 * Test class for ScriptTagService.
 */
public class ScriptTagServiceTest {

	@InjectMocks
	private ScriptTagService scriptTagService;

	@Mock
	private ScriptTagRepository scriptTagRepository;

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
	 * Test case for successful script tag creation.
	 */
	@Test
	public void createScriptTagSuccessfully() {
		ScriptTagCreateDTO scriptTagRequest = new ScriptTagCreateDTO();
		scriptTagRequest.setScriptTagName("Test Script Tag");
		scriptTagRequest.setScriptTagCategory("RDKB");
		scriptTagRequest.setScriptTagUserGroup("Test User Group");

		when(scriptTagRepository.existsByName(anyString())).thenReturn(false);
		when(userGroupRepository.findByName(anyString())).thenReturn(new UserGroup());

		assertTrue(scriptTagService.createScriptTag(scriptTagRequest));
	}

	/**
	 * Test case for script tag creation with existing name.
	 */
	@Test
	public void createScriptTagWithExistingName() {
		ScriptTagCreateDTO scriptTagRequest = new ScriptTagCreateDTO();
		scriptTagRequest.setScriptTagName("Existing Script Tag");

		when(scriptTagRepository.existsByName(anyString())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> scriptTagService.createScriptTag(scriptTagRequest));
	}

	/**
	 * Test case for script tag creation with invalid category.
	 */
	@Test
	public void createScriptTagWithInvalidCategory() {
		ScriptTagCreateDTO scriptTagRequest = new ScriptTagCreateDTO();
		scriptTagRequest.setScriptTagName("Script Tag");
		scriptTagRequest.setScriptTagCategory("Invalid Category");

		when(scriptTagRepository.existsByName(anyString())).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> scriptTagService.createScriptTag(scriptTagRequest));
	}

	/**
	 * Test case for successful script tag update.
	 */
	@Test
	public void updateScriptTagSuccessfully() {
		ScriptTagDTO scriptTagRequest = new ScriptTagDTO();
		scriptTagRequest.setScriptTagId(1);
		scriptTagRequest.setScriptTagName("Updated Script Tag");
		scriptTagRequest.setScriptTagCategory("RDKB");

		when(scriptTagRepository.findById(anyInt())).thenReturn(Optional.of(new ScriptTag()));
		when(scriptTagRepository.existsByName(anyString())).thenReturn(false);

		assertTrue(scriptTagService.updateScriptTag(scriptTagRequest));
	}

	/**
	 * Test case for script tag update with non-existing id.
	 */
	@Test
	public void updateScriptTagWithNonExistingId() {
		ScriptTagDTO scriptTagRequest = new ScriptTagDTO();
		scriptTagRequest.setScriptTagId(1);

		when(scriptTagRepository.findById(anyInt())).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> scriptTagService.updateScriptTag(scriptTagRequest));
	}

	/**
	 * Test case for script tag update with existing name.
	 */
	@Test
	public void updateScriptTagWithExistingName() {
		ScriptTagDTO scriptTagRequest = new ScriptTagDTO();
		scriptTagRequest.setScriptTagId(1);
		scriptTagRequest.setScriptTagName("Existing Script Tag");

		when(scriptTagRepository.findById(anyInt())).thenReturn(Optional.of(new ScriptTag()));
		when(scriptTagRepository.existsByName(anyString())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> scriptTagService.updateScriptTag(scriptTagRequest));
	}

	/**
	 * Test case for script tag update with invalid category.
	 */
	@Test
	public void updateScriptTagWithInvalidCategory() {
		ScriptTagDTO scriptTagRequest = new ScriptTagDTO();
		scriptTagRequest.setScriptTagId(1);
		scriptTagRequest.setScriptTagName("Script Tag");
		scriptTagRequest.setScriptTagCategory("Invalid Category");

		when(scriptTagRepository.findById(anyInt())).thenReturn(Optional.of(new ScriptTag()));
		when(scriptTagRepository.existsByName(anyString())).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> scriptTagService.updateScriptTag(scriptTagRequest));
	}

	/**
	 * Test case for successful script tag deletion.
	 */
	@Test
	public void deleteScriptTagSuccessfully() {
		when(scriptTagRepository.findById(anyInt())).thenReturn(Optional.of(new ScriptTag()));

		assertDoesNotThrow(() -> scriptTagService.deleteScriptTag(1));
	}

	/**
	 * Test case for script tag deletion with non-existing id.
	 */
	@Test
	public void deleteScriptTagWithNonExistingId() {
		when(scriptTagRepository.findById(anyInt())).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> scriptTagService.deleteScriptTag(1));
	}

	/**
	 * Test case for script tag deletion with delete exception.
	 */
	@Test
	public void deleteScriptTagWithDeleteException() {
		when(scriptTagRepository.findById(anyInt())).thenReturn(Optional.of(new ScriptTag()));
		doThrow(new DataIntegrityViolationException("Error in deleting script tag data")).when(scriptTagRepository)
				.delete(any(ScriptTag.class));

		assertThrows(DeleteFailedException.class, () -> scriptTagService.deleteScriptTag(1));
	}

	/**
	 * Test case for successful retrieval of all script tags.
	 */
	@Test
	public void findAllScriptTagSuccessfully() {
		ScriptTag scriptTag = new ScriptTag();
		scriptTag.setId(1);
		scriptTag.setName("Test Script Tag");
		scriptTag.setCategory(Category.RDKB);
		scriptTag.setUserGroup(new UserGroup());

		when(scriptTagRepository.findAll()).thenReturn(Collections.singletonList(scriptTag));

		assertNotNull(scriptTagService.findAllScriptTag());
	}

	/**
	 * Test case for retrieval of all script tags when list is empty.
	 */
	@Test
	public void findAllScriptTag_ReturnsNull() {
		when(scriptTagRepository.findAll()).thenReturn(null);

		assertNull(scriptTagService.findAllScriptTag());
	}

	/**
	 * Test case for successful retrieval of all script tags by category.
	 */
	@Test
	public void findAllScriptTagByCategorySuccessfully() {
		ScriptTag scriptTag = new ScriptTag();
		scriptTag.setId(1);
		scriptTag.setName("Test Script Tag");
		scriptTag.setCategory(Category.RDKB);
		scriptTag.setUserGroup(new UserGroup());

		when(scriptTagRepository.findByCategory(Category.RDKB)).thenReturn(Collections.singletonList(scriptTag));

		assertNotNull(scriptTagService.findAllScriptTagByCategory("RDKB"));
	}

	/**
	 * Test case for retrieval of all script tags by category when list is empty.
	 */
	@Test
	public void findAllScriptTagByCategory_ReturnsNull() {
		when(scriptTagRepository.findByCategory(any(Category.class))).thenReturn(null);

		assertNull(scriptTagService.findAllScriptTagByCategory("RDKB"));
	}

	/**
	 * Test case for retrieval of all script tags by invalid category.
	 */
	@Test
	public void findAllScriptTagByCategoryWithInvalidCategory() {
		assertThrows(ResourceNotFoundException.class,
				() -> scriptTagService.findAllScriptTagByCategory("Invalid Category"));
	}

	/**
	 * Test case for retrieval of all script tags by null category.
	 */
	@Test
	public void findAllScriptTagByCategoryWithNullCategory() {
		assertThrows(ResourceNotFoundException.class, () -> scriptTagService.findAllScriptTagByCategory(null));
	}

	/**
	 * Test case for successful retrieval of script tag list by category.
	 */
	@Test
	public void testGetScriptTagListByCategory() {
		String category = "RDKB";
		ScriptTag scriptTags = new ScriptTag();
		scriptTags.setId(1);
		scriptTags.setCategory(Category.RDKB);
		scriptTags.setName("Version1");

		when(scriptTagRepository.findByCategory(Category.getCategory(category)))
				.thenReturn(Collections.singletonList(scriptTags));

		List<String> result = scriptTagService.getListOfScriptTagByCategory(category);

		assertNotNull(result);
		assertFalse(result.isEmpty());
		assertEquals(1, result.size());
	}

	/**
	 * Test case for retrieval of script tag list by category when list is empty.
	 */
	@Test
	public void testGetScriptTagListByCategory_ReturnsNull() {
		String category = "RDKB";

		when(scriptTagRepository.findByCategory(Category.getCategory(category))).thenReturn(null);

		assertNull(scriptTagService.getListOfScriptTagByCategory(category));
	}

	/**
	 * Test case for retrieval of script tag list by invalid category.
	 */
	@Test
	public void getListOfScriptTagByCategoryWithInvalidCategory() {
		String category = "Invalid Category";

		assertThrows(ResourceNotFoundException.class, () -> scriptTagService.getListOfScriptTagByCategory(category));
	}

	/**
	 * Test case for retrieval of script tag list by category when no script tags
	 * exist.
	 */
	@Test
	public void getListOfScriptTagByCategoryWithNoScriptTags() {
		String category = "RDKB";

		when(scriptTagRepository.findByCategory(any(Category.class))).thenReturn(null);

		assertNull(scriptTagService.getListOfScriptTagByCategory(category));
	}

	/**
	 * Test case for successful retrieval of script tag by id.
	 */
	@Test
	public void findByIdSuccessfully() {
		Integer id = 1;
		ScriptTag scriptTag = new ScriptTag();
		scriptTag.setName("scriptTag1");
		scriptTag.setCategory(Category.RDKB);

		when(scriptTagRepository.findById(anyInt())).thenReturn(Optional.of(scriptTag));

		ScriptTagDTO result = scriptTagService.findById(id);

		assertNotNull(result);
		assertEquals("scriptTag1", result.getScriptTagName());
	}

	/**
	 * Test case for retrieval of script tag by non-existing id.
	 */
	@Test
	public void findByIdWithNonExistingId() {
		Integer id = 1;

		when(scriptTagRepository.findById(anyInt())).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> scriptTagService.findById(id));
	}
}
