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

import java.util.Collections;
import java.util.List;
import java.util.UUID;

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
import org.springframework.web.bind.annotation.RestController;

import com.rdkm.tdkservice.dto.FunctionCreateDTO;
import com.rdkm.tdkservice.dto.FunctionDTO;
import com.rdkm.tdkservice.service.IFunctionService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import jakarta.validation.Valid;

/**
 * REST controller for managing functions.
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/function")
public class FunctionController {

	private static final Logger LOGGER = LoggerFactory.getLogger(FunctionController.class);

	@Autowired
	private IFunctionService functionService;

	/**
	 * Creates a new function.
	 *
	 * @param functionCreateDTO the function creation data transfer object
	 * @return ResponseEntity with a success or failure message
	 */
	@Operation(summary = "Create a new function")
	@ApiResponse(responseCode = "200", description = "Function created successfully")
	@ApiResponse(responseCode = "500", description = "Failed to create function")
	@ApiResponse(responseCode = "404", description = "Function already exists")
	@ApiResponse(responseCode = "400", description = "Invalid input")
	@ApiResponse(responseCode = "401", description = "Unauthorized")
	@PostMapping("/create")
	public ResponseEntity<String> createFunction(@RequestBody @Valid FunctionCreateDTO functionCreateDTO) {
		LOGGER.info("Creating new function: {}", functionCreateDTO);
		boolean isCreated = functionService.createFunction(functionCreateDTO);
		if (isCreated) {
			LOGGER.info("Function created successfully: {}", functionCreateDTO);
			return ResponseEntity.status(HttpStatus.CREATED).body("Function created successfully");
		} else {
			LOGGER.error("Failed to create function: {}", functionCreateDTO);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to create function");
		}
	}

	/**
	 * Updates an existing function.
	 *
	 * @param functionDTO the function data transfer object
	 * @return ResponseEntity with a success or failure message
	 */
	@Operation(summary = "Update an existing function")
	@ApiResponse(responseCode = "200", description = "Function updated successfully")
	@ApiResponse(responseCode = "500", description = "Failed to update function")
	@ApiResponse(responseCode = "400", description = "Invalid input")
	@ApiResponse(responseCode = "401", description = "Unauthorized")
	@ApiResponse(responseCode = "404", description = "Function not found")
	@PutMapping("/update")
	public ResponseEntity<String> updateFunction(@RequestBody @Valid FunctionDTO functionDTO) {
		LOGGER.info("Updating function: {}", functionDTO);
		boolean isUpdated = functionService.updateFunction(functionDTO);
		if (isUpdated) {
			LOGGER.info("Function updated successfully: {}", functionDTO);
			return ResponseEntity.status(HttpStatus.OK).body("Function updated successfully");
		} else {
			LOGGER.error("Failed to update function: {}", functionDTO);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to update function");
		}
	}

	/**
	 * Retrieves all functions.
	 *
	 * @return ResponseEntity with a list of all functions
	 */
	@Operation(summary = "Find all functions")
	@ApiResponse(responseCode = "200", description = "Functions found")
	@ApiResponse(responseCode = "404", description = "No functions found")
	@ApiResponse(responseCode = "401", description = "Unauthorized")
	@ApiResponse(responseCode = "500", description = "Internal server error")
	@GetMapping("/findAll")
	public ResponseEntity<List<FunctionDTO>> findAllFunctions() {
		LOGGER.info("Retrieving all functions");
		List<FunctionDTO> functions = functionService.findAllFunctions();
		LOGGER.info("Successfully retrieved all functions");
		return ResponseEntity.ok(functions);
	}

	/**
	 * Retrieves a function by its ID.
	 *
	 * @param id the ID of the function
	 * @return ResponseEntity with the function data transfer object
	 */
	@Operation(summary = "Find a function by ID")
	@ApiResponse(responseCode = "200", description = "Function found")
	@ApiResponse(responseCode = "404", description = "Function not found")
	@ApiResponse(responseCode = "401", description = "Unauthorized")
	@ApiResponse(responseCode = "500", description = "Internal server error")
	@GetMapping("/findById/{id}")
	public ResponseEntity<FunctionDTO> findFunctionById(@PathVariable UUID id) {
		LOGGER.info("Retrieving function by ID: {}", id);
		FunctionDTO function = functionService.findFunctionById(id);
		LOGGER.info("Successfully retrieved function: {}", function);
		return ResponseEntity.status(HttpStatus.OK).body(function);
	}

	/**
	 * Deletes a function by its ID.
	 *
	 * @param id the ID of the function
	 * @return ResponseEntity with a success or failure message
	 */
	@Operation(summary = "Delete a function by ID")
	@ApiResponse(responseCode = "200", description = "Function deleted successfully")
	@ApiResponse(responseCode = "500", description = "Failed to delete function")
	@ApiResponse(responseCode = "401", description = "Unauthorized")
	@ApiResponse(responseCode = "404", description = "Function not found")
	@DeleteMapping("/delete/{id}")
	public ResponseEntity<String> deleteFunction(@PathVariable UUID id) {
		LOGGER.info("Deleting function by ID: {}", id);
		functionService.deleteFunction(id);
		LOGGER.info("Function deleted successfully: {}", id);
		return ResponseEntity.status(HttpStatus.OK).body("Function deleted successfully");
	}

	/**
	 * Retrieves all functions by category.
	 *
	 * @param category the category of the functions
	 * @return ResponseEntity with a list of functions in the specified category
	 */
	@Operation(summary = "Find all functions by category")
	@ApiResponse(responseCode = "200", description = "Functions found")
	@ApiResponse(responseCode = "404", description = "No functions found")
	@ApiResponse(responseCode = "401", description = "Unauthorized")
	@ApiResponse(responseCode = "500", description = "Internal server error")
	@GetMapping("/findAllByCategory/{category}")
	public ResponseEntity<List<FunctionDTO>> findAllByCategory(@PathVariable String category) {
		LOGGER.info("Retrieving functions by category: {}", category);
		List<FunctionDTO> functions = functionService.findAllByCategory(category);
		LOGGER.info("Successfully retrieved functions by category: {}", category);
		return ResponseEntity.status(HttpStatus.OK).body(functions);
	}

	@Operation(summary = "Retrieve all functions names by module name", description = "Retrieves a list of all functions by module name.")
	@ApiResponses(value = { @ApiResponse(responseCode = "200", description = "Successfully retrieved all functions"),
			@ApiResponse(responseCode = "404", description = "No functions found"),
			@ApiResponse(responseCode = "401", description = "Unauthorized"),
			@ApiResponse(responseCode = "500", description = "Internal server error") })
	@GetMapping("/getlistoffunctionbymodulename/{moduleName}")
	public ResponseEntity<List<String>> findAllFunctionNameByModule(@PathVariable String moduleName) {
		LOGGER.info("Retrieving functions by category: {}", moduleName);
		List<String> functions = functionService.findAllFunctionNameByModule(moduleName);
		if (functions != null && !functions.isEmpty()) {
			LOGGER.info("Successfully retrieved functions by category: {}", moduleName);
			return ResponseEntity.status(HttpStatus.OK).body(functions);
		} else {
			LOGGER.warn("No functions found for module name: {}", moduleName);
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
		}
	}

	/**
	 * Retrieves all functions by module name.
	 *
	 * @param moduleName the name of the module
	 * @return ResponseEntity with a list of functions in the specified module
	 */
	@Operation(summary = "Retrieve all functions by module name", description = "Retrieves a list of all functions by module name.")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Successfully retrieved all functions"),
			@ApiResponse(responseCode = "404", description = "No functions found"),
			@ApiResponse(responseCode = "401", description = "Unauthorized"),
            @ApiResponse(responseCode = "500", description = "Internal server error")
    })
	@GetMapping("/findAllByModule/{moduleName}")
	public ResponseEntity<List<FunctionDTO>> findAllFunctionsByModule(@PathVariable String moduleName) {
		LOGGER.info("Retrieving all functions by module name: {}", moduleName);
		List<FunctionDTO> functions = functionService.findAllFunctionsByModule(moduleName);
		if (functions != null && !functions.isEmpty()) {
			LOGGER.info("Successfully retrieved all functions by module name: {}", moduleName);
			return ResponseEntity.status(HttpStatus.OK).body(functions);
		} else {
			LOGGER.warn("No functions found for module name: {}", moduleName);
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Collections.emptyList());
		}
	}
}