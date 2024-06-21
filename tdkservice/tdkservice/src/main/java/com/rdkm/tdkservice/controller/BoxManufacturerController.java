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

import com.rdkm.tdkservice.dto.BoxManufacturerDTO;
import com.rdkm.tdkservice.dto.BoxManufacturerUpdateDTO;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.service.IBoxManufacturerService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/**
 * The controller class that handles the API endpoints related to box
 * manufacturers.
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/boxmanufacturer")
public class BoxManufacturerController {

	private static final Logger LOGGER = LoggerFactory.getLogger(BoxManufacturerController.class);

	@Autowired
	IBoxManufacturerService boxManufacturerService;

	/**
	 * Creates a new box manufacturer type.
	 *
	 * @param boxManufacturerRequest The request object containing the details of
	 *                               the box manufacturer.
	 * @return ResponseEntity containing the created box manufacturer if successful,
	 *         or an error message if unsuccessful.
	 * @throws ResourceAlreadyExistsException if a box type with the same name
	 *                                        already exists.
	 */
	@Operation(summary = "Create a new box manufacturer type", description = "Creates a new box manufacturer type in the system.")
	@ApiResponse(responseCode = "201", description = "Box manufacturer created successfully")
	@ApiResponse(responseCode = "500", description = "Error in saving box manufacturer type data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping("/create")
	public ResponseEntity<String> createBoxManufacturerType(
			@RequestBody @Valid BoxManufacturerDTO boxManufacturerRequest) {
		LOGGER.info("Received create box manufacturer type request: " + boxManufacturerRequest.toString());
		boolean isBoxManufacturerCreated = boxManufacturerService.createBoxManufacturer(boxManufacturerRequest);
		if (isBoxManufacturerCreated) {
			LOGGER.info("Box manufacturer created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Box manufacturer created succesfully");
		} else {
			LOGGER.error("Error in saving box manufacturer type data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in saving box manufacturer type data");
		}

	}

	/**
	 * Retrieves all box manufacturer types.
	 *
	 * @return ResponseEntity containing the list of box manufacturer types if
	 *         found, or a NOT_FOUND status with an error message if not found.
	 */
	@Operation(summary = "Find all box manufacturer types", description = "Retrieves all box manufacturer types from the system.")
	@ApiResponse(responseCode = "200", description = "Box manufacturer types found")
	@ApiResponse(responseCode = "404", description = "No box manufacturer types found")
	@GetMapping("/findall")
	public ResponseEntity<?> findAllBoxManufacturerTypes() {
		LOGGER.info("Received find all box manufacturer types request");
		List<BoxManufacturerDTO> boxManufacturerList = boxManufacturerService.getAllBoxManufacturer();
		if (boxManufacturerList != null && !boxManufacturerList.isEmpty()) {
			LOGGER.info("Box manufacturer types found successfully");
			return ResponseEntity.ok(boxManufacturerList);
		} else {
			LOGGER.error("No box manufacturer types found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No box manufacturer types found");
		}

	}

	/**
	 * Deletes a box manufacturer by ID.
	 *
	 * @param id The ID of the box manufacturer to delete.
	 * @return A ResponseEntity with the status and message indicating the result of
	 *         the deletion.
	 */
	@Operation(summary = "Delete a box manufacturer type", description = "Deletes a box manufacturer type from the system.")
	@ApiResponse(responseCode = "200", description = "Box manufacturer deleted successfully")
	@ApiResponse(responseCode = "404", description = "Box manufacturer not found")
	@DeleteMapping("/delete/{id}")
	public ResponseEntity<String> deleteBoxManufacturerType(@PathVariable Integer id) {
		LOGGER.info("Received delete box manufacturer type request for ID: " + id);
		boxManufacturerService.deleteBoxManufacturer(id);
		return ResponseEntity.status(HttpStatus.OK).body("Succesfully deleted the box manufacturer");
	}

	/**
	 * Retrieves a BoxManufacturer by its ID.
	 *
	 * @param id the ID of the BoxManufacturer to retrieve
	 * @return a ResponseEntity containing the BoxManufacturer if found, or a
	 *         NOT_FOUND status with an error message if not found
	 */
	@Operation(summary = "Find box manufacturer by ID", description = "Retrieves a box manufacturer by its ID.")
	@ApiResponse(responseCode = "200", description = "Box manufacturer found")
	@ApiResponse(responseCode = "500", description = "Box manufacturer not found")

	@GetMapping("/findbyid/{id}")
	public ResponseEntity<BoxManufacturerDTO> findById(@PathVariable Integer id) {
		LOGGER.info("Received find box manufacturer by id request: " + id);
		BoxManufacturerDTO boxManufacturer = boxManufacturerService.findById(id);
		return ResponseEntity.status(HttpStatus.OK).body(boxManufacturer);

	}

	/**
	 * Updates the box manufacturer with the specified ID.
	 *
	 * @param id                     the ID of the box manufacturer to update
	 * @param boxManufacturerRequest the updated box manufacturer details
	 * @return a ResponseEntity containing the updated box manufacturer if
	 *         successful, or an error message if unsuccessful
	 */
	@Operation(summary = "Update a box manufacturer", description = "Updates a box manufacturer in the system.")
	@ApiResponse(responseCode = "200", description = "Box manufacturer updated successfully")
	@ApiResponse(responseCode = "500", description = "Error in updating box manufacturer")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PutMapping("/update/{id}")
	public ResponseEntity<?> updateBoxManufacturer(@PathVariable Integer id,
			@RequestBody BoxManufacturerUpdateDTO boxManufacturerRequest) {
		LOGGER.info("Received update box manufacturer request: " + boxManufacturerRequest.toString());
		BoxManufacturerUpdateDTO updatedBoxManufacturer = boxManufacturerService
				.updateBoxManufacturer(boxManufacturerRequest, id);
		if (updatedBoxManufacturer != null) {
			LOGGER.info("Box manufacturer updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body(updatedBoxManufacturer);
        } else {
        	LOGGER.error("Error in updating box manufacturer");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in updating box manufacturer");
		}
		
	}

	/**
	 * Retrieves all box manufacturers by category.
	 *
	 * @param category the category of the box manufacturers to retrieve
	 * @return a ResponseEntity containing the list of box manufacturers if found,
	 *         or a NOT_FOUND status with an error message if not found
	 */
	@Operation(summary = "Find box manufacturers DTO by category", description = "Retrieves all box manufacturers by category.")
	@ApiResponse(responseCode = "200", description = "Box manufacturers found")
	@ApiResponse(responseCode = "404", description = "No box manufacturers found")
	@GetMapping("/findallbycategory")
	public ResponseEntity<?> getBoxManufacturersByCategory(String category) {
		LOGGER.info("Received find box manufacturers by category request: " + category);
		List<BoxManufacturerDTO> boxManufacturerList = boxManufacturerService.getBoxManufacturersByCategory(category);
		if (boxManufacturerList != null && !boxManufacturerList.isEmpty()) {
			LOGGER.info("Box manufacturers found");
			return ResponseEntity.status(HttpStatus.OK).body(boxManufacturerList);
		} else {
			LOGGER.error("No box manufacturers found for the category");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No box manufacturers found");
		}
	}

	/**
	 * Retrieves all box manufacturers by category.
	 *
	 * @param category the category of the box manufacturers to retrieve
	 * @return a ResponseEntity containing the list of box manufacturers if found,
	 *         or a NOT_FOUND status with an error message if not found
	 */

	@Operation(summary = "Get box manufacturers name list by category", description = "Retrieves all box manufacturers by category.")
	@ApiResponse(responseCode = "200", description = "Box manufacturers retrieved successfully")
	@ApiResponse(responseCode = "404", description = "No box manufacturers found")
	@GetMapping("/getlistbycategory")
	public ResponseEntity<?> getBoxmanufacturerListByCategory(@RequestParam String category) {
		LOGGER.info("Received find box manufacturer by category request: " + category);
		List<String> boxManufacturerList = boxManufacturerService.getBoxManufacturerListByCategory(category);
		if (boxManufacturerList != null && !boxManufacturerList.isEmpty()) {
			LOGGER.info("Box manufacturers found successfully");
			return ResponseEntity.status(HttpStatus.OK).body(boxManufacturerList);
		} else {
			LOGGER.error("No box manufacturers found for the category");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No box manufacturers found");
		}
	}

}
