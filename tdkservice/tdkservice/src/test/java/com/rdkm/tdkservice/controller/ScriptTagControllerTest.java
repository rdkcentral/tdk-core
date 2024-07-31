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

import com.rdkm.tdkservice.dto.ScriptTagCreateDTO;
import com.rdkm.tdkservice.dto.ScriptTagDTO;
import com.rdkm.tdkservice.service.IScriptTagService;

/**
 * Test class for ScriptTagController.
 */
public class ScriptTagControllerTest {

	@InjectMocks
	private ScriptTagController scriptTagController;

	@Mock
	private IScriptTagService scriptTagService;

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
	public void createScriptTag_Success() {
		ScriptTagCreateDTO scriptTagRequest = new ScriptTagCreateDTO();
		when(scriptTagService.createScriptTag(scriptTagRequest)).thenReturn(true);

		ResponseEntity<String> response = scriptTagController.createScriptTag(scriptTagRequest);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
		assertEquals("Script tag created successfully", response.getBody());
	}

	/**
	 * Test case for script tag creation failure.
	 */
	@Test
	public void createScriptTag_Failure() {
		ScriptTagCreateDTO scriptTagRequest = new ScriptTagCreateDTO();
		when(scriptTagService.createScriptTag(scriptTagRequest)).thenReturn(false);

		ResponseEntity<String> response = scriptTagController.createScriptTag(scriptTagRequest);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Error in saving script tag data", response.getBody());
	}

	/**
	 * Test case for successful script tag update.
	 */
	@Test
	public void updateScriptTag_Success() {
		ScriptTagDTO scriptTagRequest = new ScriptTagDTO();
		when(scriptTagService.updateScriptTag(scriptTagRequest)).thenReturn(true);

		ResponseEntity<String> response = scriptTagController.updateScriptTag(scriptTagRequest);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Script tag updated successfully", response.getBody());
	}

	/**
	 * Test case for script tag update failure.
	 */
	@Test
	public void updateScriptTag_Failure() {
		ScriptTagDTO scriptTagRequest = new ScriptTagDTO();
		when(scriptTagService.updateScriptTag(scriptTagRequest)).thenReturn(false);

		ResponseEntity<String> response = scriptTagController.updateScriptTag(scriptTagRequest);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Error in updating script tag data", response.getBody());
	}

	/**
	 * Test case for successful retrieval of all script tags.
	 */
	@Test
	public void findAllScriptTag_Success() {
		ScriptTagDTO scriptTagDTO = new ScriptTagDTO();
		List<ScriptTagDTO> scriptTags = Collections.singletonList(scriptTagDTO);
		when(scriptTagService.findAllScriptTag()).thenReturn(scriptTags);

		ResponseEntity<?> response = scriptTagController.findAllScriptTag();

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(scriptTags, response.getBody());
	}

	/**
	 * Test case for retrieval of all script tags when list is empty.
	 */
	@Test
	public void findAllScriptTag_Failure() {
		when(scriptTagService.findAllScriptTag()).thenReturn(null);

		ResponseEntity<?> response = scriptTagController.findAllScriptTag();

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No script tags found", response.getBody());
	}

	/**
	 * Test case for successful script tag deletion.
	 */
	@Test
	public void deleteScriptTag_Success() {
		Integer id = 1;
		doNothing().when(scriptTagService).deleteScriptTag(id);

		ResponseEntity<String> response = scriptTagController.deleteScriptTag(id);

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * Test case for successful retrieval of all script tags by category.
	 */
	@Test
	public void findAllScriptTagByCategory_Success() {
		String category = "RDKB";
		List<ScriptTagDTO> scriptTags = Collections.singletonList(new ScriptTagDTO());
		when(scriptTagService.findAllScriptTagByCategory(category)).thenReturn(scriptTags);

		ResponseEntity<?> response = scriptTagController.findAllScriptTagByCategory(category);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(scriptTags, response.getBody());
	}

	/**
	 * Test case for retrieval of all script tags by category when list is empty.
	 */
	@Test
	public void findAllScriptTagByCategory_Failure() {
		String category = "RDKB";
		when(scriptTagService.findAllScriptTagByCategory(category)).thenReturn(null);

		ResponseEntity<?> response = scriptTagController.findAllScriptTagByCategory(category);

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No script tags found", response.getBody());
	}

	/**
	 * Test case for successful retrieval of script tag list by category.
	 */
	@Test
	public void listOfScriptTagByCategory_Success() {
		String category = "test";
		List<String> scriptTags = Collections.singletonList("test1");
		when(scriptTagService.getListOfScriptTagByCategory(category)).thenReturn(scriptTags);

		ResponseEntity<?> response = scriptTagController.listOfScriptTagByCategory(category);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(scriptTags, response.getBody());
	}

	/**
	 * Test case for retrieval of script tag list by category when list is empty.
	 */
	@Test
	public void listOfScriptTagByCategory_Failure() {
		String category = "RDKV";
		when(scriptTagService.getListOfScriptTagByCategory(category)).thenReturn(null);

		ResponseEntity<?> response = scriptTagController.listOfScriptTagByCategory(category);

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No script tags found", response.getBody());
	}

	/**
	 * Test case for successful retrieval of script tag by id.
	 */
	@Test
	public void findById_Success() {
		Integer id = 1;
		ScriptTagDTO scriptTagDTO = new ScriptTagDTO();
		when(scriptTagService.findById(id)).thenReturn(scriptTagDTO);

		ResponseEntity<?> response = scriptTagController.findById(id);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(scriptTagDTO, response.getBody());
	}

	/**
	 * Test case for retrieval of script tag by non-existing id.
	 */
	@Test
	public void findById_Failure() {
		Integer id = 1;
		when(scriptTagService.findById(id)).thenReturn(null);

		ResponseEntity<?> response = scriptTagController.findById(id);

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("Script tag not found", response.getBody());
	}
}
