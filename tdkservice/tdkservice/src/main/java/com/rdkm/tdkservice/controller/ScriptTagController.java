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

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.rdkm.tdkservice.dto.ScriptTagCreateDTO;
import com.rdkm.tdkservice.dto.ScriptTagDTO;
import com.rdkm.tdkservice.service.IScriptTagService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/*
 * The ScriptTagController class is a REST controller that handles script tag operations.
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/scripttag")
public class ScriptTagController {

	private static final Logger LOGGER = LoggerFactory.getLogger(ScriptTagController.class);

	@Autowired
	IScriptTagService scriptTagService;

	/**
	 * This method is used to create a new script tag. It receives a POST request at
	 * the "/create" endpoint with a ScriptTagCreateDTO object in the request body.
	 * The ScriptTagCreateDTO object should contain the necessary information for
	 * creating a new script tag.
	 * 
	 * @param scriptTagRequest - ScriptTagCreateDTO object
	 * @return ResponseEntity<String> - response entity - message
	 */
	@Operation(summary = "Create a new script tag", description = "Create a new script tag")
	@ApiResponse(responseCode = "201", description = "Script tag created successfully")
	@ApiResponse(responseCode = "500", description = "Error in saving script tag data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping("/create")
	public ResponseEntity<String> createScriptTag(@RequestBody @Valid ScriptTagCreateDTO scriptTagRequest) {
		LOGGER.info("Received create script tag request: " + scriptTagRequest.toString());
		boolean isScriptTagCreated = scriptTagService.createScriptTag(scriptTagRequest);
		if (isScriptTagCreated) {
			LOGGER.info("Script tag created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Script tag created successfully");
		} else {
			LOGGER.error("Error in saving script tag data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in saving script tag data");
		}
	}

	/**
	 * This method is used to update an existing script tag. It receives a PUT
	 * request at the "/update" endpoint with a ScriptTagDTO object in the request
	 * body. The ScriptTagDTO object should contain the necessary information for
	 * updating an existing script tag.
	 * 
	 * @param scriptTagRequest - ScriptTagDTO object
	 * @return ResponseEntity<String> - response entity - message
	 */
	@Operation(summary = "Update an existing script tag", description = "Update an existing script tag")
	@ApiResponse(responseCode = "200", description = "Script tag updated successfully")
	@ApiResponse(responseCode = "500", description = "Error in updating script tag data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PutMapping("/update")
	public ResponseEntity<String> updateScriptTag(@Valid @RequestBody ScriptTagDTO scriptTagRequest) {
		LOGGER.info("Received update script tag request: " + scriptTagRequest.toString());
		boolean isScriptTagUpdated = scriptTagService.updateScriptTag(scriptTagRequest);
		if (isScriptTagUpdated) {
			LOGGER.info("Script tag updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Script tag updated successfully");
		} else {
			LOGGER.error("Error in updating script tag data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in updating script tag data");
		}
	}

	/**
	 * This method is used to delete an existing script tag. It receives a DELETE
	 * request at the "/delete/{id}" endpoint with the id of the script tag to be
	 * deleted.
	 * 
	 * @param id - Integer -The script tag
	 * @return ResponseEntity<String> - response entity - message
	 */
	@Operation(summary = "Delete an existing script tag", description = "Delete an existing script tag")
	@ApiResponse(responseCode = "200", description = "Script tag deleted successfully")
	@ApiResponse(responseCode = "404", description = "Script tag not found")
	@DeleteMapping("/delete/{id}")
	public ResponseEntity<String> deleteScriptTag(@PathVariable Integer id) {
		LOGGER.info("Received delete script tag request: " + id.toString());
		scriptTagService.deleteScriptTag(id);
		LOGGER.info("Script tag deleted successfully");
		return ResponseEntity.status(HttpStatus.OK).body("Script tag deleted successfully");

	}

	/**
	 * This method is used to find all script tags.
	 * 
	 * @return ResponseEntity<List<ScriptTagDTO>> - response entity - list of script
	 *         tags
	 */
	@Operation(summary = "Find all script tags", description = "Find all script tags")
	@ApiResponse(responseCode = "200", description = "Script tags found")
	@ApiResponse(responseCode = "404", description = "No script tags found")
	@GetMapping("/findall")
	public ResponseEntity<?> findAllScriptTag() {
		LOGGER.info("Received find all script tag request");
		List<ScriptTagDTO> scriptTags = scriptTagService.findAllScriptTag();
		if (null != scriptTags && !scriptTags.isEmpty()) {
			LOGGER.info("Returning all script tags:" + scriptTags.toString());
			return ResponseEntity.status(HttpStatus.OK).body(scriptTags);
		} else {
			LOGGER.error("No script tags found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No script tags found");
		}
	}

	/**
	 * This method is used to find all script tags by category. It receives a GET
	 * request at the "/findallbycategory" endpoint with the category of the script
	 * tags to be found.
	 * 
	 * @param category - String - the script tag category
	 * @return ResponseEntity<List<ScriptTagDTO>> - response entity - list of script
	 *         tags
	 **/
	@Operation(summary = "Find all script tags by category", description = "Find all script tags by category")
	@ApiResponse(responseCode = "200", description = "Script tags found")
	@ApiResponse(responseCode = "404", description = "No script tags found")
	@GetMapping("/findallbycategory")
	public ResponseEntity<?> findAllScriptTagByCategory(@RequestParam String category) {
		LOGGER.info("Received find all script tag by category request");
		List<ScriptTagDTO> scriptTags = scriptTagService.findAllScriptTagByCategory(category);
		if (null != scriptTags && !scriptTags.isEmpty()) {
			LOGGER.info("Returning all script tags by category:" + scriptTags.toString());
			return ResponseEntity.status(HttpStatus.OK).body(scriptTags);
		} else {
			LOGGER.error("No script tags found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No script tags found");
		}
	}

	/**
	 * This method is used to get the list of script tags by category. It receives a
	 * GET request at the "/getlistbycategory" endpoint with the category of the
	 * script tags to be found.
	 * 
	 * @param category - String - the script tag category
	 * @return ResponseEntity<List<String>> - response entity - list of script tags
	 **/
	@Operation(summary = "List of script tags by category", description = "List of script tags by category")
	@ApiResponse(responseCode = "200", description = "Script tags found")
	@ApiResponse(responseCode = "404", description = "No script tags found")
	@GetMapping("/getlistbycategory")
	public ResponseEntity<?> listOfScriptTagByCategory(@RequestParam String category) {
		LOGGER.info("Received list of script tag by category request");
		List<String> scriptTags = scriptTagService.getListOfScriptTagByCategory(category);
		if (null != scriptTags && !scriptTags.isEmpty()) {
			LOGGER.info("Returning list of script tags by category:" + scriptTags.toString());
			return ResponseEntity.status(HttpStatus.OK).body(scriptTags);
		} else {
			LOGGER.error("No script tags found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No script tags found");
		}
	}

	/**
	 * This method is used to find script tag by id. It receives a GET request at
	 * the "/findbyid/{id}" endpoint with the id of the script tag to be found.
	 * 
	 * @param id - Integer - the script tag id
	 * @return ResponseEntity<ScriptTagDTO> - response entity - script tag
	 **/
	@Operation(summary = "Find script tag by id", description = "Find script tag by id")
	@ApiResponse(responseCode = "200", description = "Script tag found")
	@ApiResponse(responseCode = "404", description = "Script tag not found")
	@GetMapping("/findbyid/{id}")
	public ResponseEntity<?> findById(@PathVariable Integer id) {
		LOGGER.info("Received find script tag by id request");
		ScriptTagDTO scriptTag = scriptTagService.findById(id);
		if (null != scriptTag) {
			LOGGER.info("Returning script tag:" + scriptTag.toString());
			return ResponseEntity.status(HttpStatus.OK).body(scriptTag);
		} else {
			LOGGER.error("Script tag not found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Script tag not found");
		}
	}

}
