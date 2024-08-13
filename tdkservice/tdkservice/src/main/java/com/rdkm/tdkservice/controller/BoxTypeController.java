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

import com.rdkm.tdkservice.dto.BoxTypeDTO;
import com.rdkm.tdkservice.dto.BoxTypeUpdateDTO;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.service.IBoxTypeService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/**
 * The controller class that handles the endpoints related to box types.
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/boxtype")
public class BoxTypeController {

	private static final Logger LOGGER = LoggerFactory.getLogger(BoxTypeController.class);

	/*
	 * The service that handles the business logic for box types.
	 */

	@Autowired
	IBoxTypeService boxTypeService;

	/**
	 * Creates a new box type based on the provided box type request.
	 *
	 * @param boxTypeRequest The request object containing the details of the box
	 *                       type.
	 * @return A ResponseEntity containing the created box type if successful, or an
	 *         error message if unsuccessful.
	 * @throws ResourceAlreadyExistsException If a box type with the same name
	 *                                        already exists.
	 */
	@Operation(summary = "Create a new box type", description = "Creates a new box type in the system.")
	@ApiResponse(responseCode = "201", description = "Box type created successfully")
	@ApiResponse(responseCode = "500", description = "Error in saving box type data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping("/create")
	public ResponseEntity<String> createBoxType(@RequestBody @Valid BoxTypeDTO boxTypeRequest) {
		LOGGER.info("Received create box type request: " + boxTypeRequest.toString());

		boolean isBoxTypeCreated = boxTypeService.createBoxType(boxTypeRequest);

		if (isBoxTypeCreated) {
			LOGGER.info("Box type created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Box type created succesfully");
		} else {
			LOGGER.error("Error in saving box type data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in saving box type data");
		}

	}

	/**
	 * Retrieves all box types.
	 *
	 * @return ResponseEntity containing the list of box types if found, or a
	 *         ResponseEntity with status NOT_FOUND and a message if no box types
	 *         are found.
	 */
	@Operation(summary = "Get all box types", description = "Retrieves all box types in the system.")
	@ApiResponse(responseCode = "200", description = "Box types retrieved successfully")
	@ApiResponse(responseCode = "404", description = "No box types found")
	@GetMapping("/findall")
	public ResponseEntity<?> getAllBoxTypes() {
		LOGGER.info("Going to fetch all box types");
		List<BoxTypeDTO> boxTypes = boxTypeService.getAllBoxTypes();
		if (null != boxTypes) {
			LOGGER.info("Box types found");
			return ResponseEntity.status(HttpStatus.OK).body(boxTypes);
		} else {
			LOGGER.info("No box types found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No box types found");
		}

	}

	/**
	 * Deletes a box type with the specified ID.
	 *
	 * @param id the ID of the box type to delete
	 * @return a ResponseEntity with the status and message indicating the result of
	 *         the deletion
	 */
	@Operation(summary = "Delete a box type", description = "Deletes a box type from the system.")
	@ApiResponse(responseCode = "200", description = "Box type deleted successfully")
	@ApiResponse(responseCode = "404", description = "Box type not found")
	@DeleteMapping("/delete/{id}")
	public ResponseEntity<String> deleteBoxType(@PathVariable Integer id) {
		LOGGER.info("Received delete box type request: " + id);
		boxTypeService.deleteById(id);
		return ResponseEntity.status(HttpStatus.OK).body("Succesfully deleted the box");

	}

	/**
	 * Retrieves a box type by its ID.
	 *
	 * @param id the ID of the box type to retrieve
	 * @return a ResponseEntity containing the box type if found, or a NOT_FOUND
	 *         status with an error message if not found
	 */
	@Operation(summary = "Find box type by ID", description = "Retrieves a box type by its ID.")
	@ApiResponse(responseCode = "200", description = "Box type found")
	@ApiResponse(responseCode = "404", description = "Box type not found")
	@GetMapping("/findbyid/{id}")
	public ResponseEntity<BoxTypeDTO> findById(@PathVariable Integer id) {
		LOGGER.info("Received find box type by id request: " + id);
		BoxTypeDTO boxType = boxTypeService.findById(id);
		return ResponseEntity.status(HttpStatus.OK).body(boxType);

	}

	/**
	 * Updates a box type based on the provided BoxTypeUpdateRequest.
	 * 
	 * @param boxTypeUpdateRequest The BoxTypeUpdateRequest containing the updated
	 *                             box type information.
	 * @return ResponseEntity containing the updated BoxType if it exists, or a
	 *         NOT_FOUND status with an error message if the box type is not found.
	 */
	@Operation(summary = "Update a box type", description = "Updates a box type in the system.")
	@ApiResponse(responseCode = "200", description = "Box type updated successfully")
	@ApiResponse(responseCode = "404", description = "Box type not found")
	@ApiResponse(responseCode = "500", description = "Error in updating box type data")
	@PutMapping("/update/{id}")
	public ResponseEntity<?> updateBoxType(@PathVariable Integer id, @RequestBody BoxTypeUpdateDTO boxTypeUpdateDTO) {
		LOGGER.info("Received update box type request: " + boxTypeUpdateDTO.toString());
		BoxTypeUpdateDTO boxType = boxTypeService.updateBoxType(boxTypeUpdateDTO, id);
		if (null != boxType) {
			LOGGER.info("Box type updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body(boxType);
		} else {
			LOGGER.error("Error in updating box type data");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Box type not found");
		}

	}

	/**
	 * Retrieves all box types in the system by category.
	 *
	 * @param category the category of the box types to retrieve
	 * @return a ResponseEntity containing the list of box types if found, or a
	 *         ResponseEntity with status NOT_FOUND and a message if no box types
	 *         are found.
	 */
	@Operation(summary = "Get box types by category", description = "Retrieves all box types in the system by category.")
	@ApiResponse(responseCode = "200", description = "Box types retrieved successfully")
	@ApiResponse(responseCode = "404", description = "No box types found")
	@GetMapping("/findallbycategory")
	public ResponseEntity<?> getBoxTypesByCategory(@RequestParam String category) {
		LOGGER.info("Received find box type by category request: " + category);
		List<BoxTypeDTO> boxTypeDTO = boxTypeService.getBoxTypesByCategory(category);
		if (null != boxTypeDTO) {
			LOGGER.info("Box types found");
			return ResponseEntity.status(HttpStatus.OK).body(boxTypeDTO);
		} else {
			LOGGER.error("No box types found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No box types found");
		}

	}

	/**
	 * Retrieves all box type names in the system by category.
	 *
	 * @param category the category of the box types to retrieve
	 * @return a ResponseEntity containing the list of box types if found, or a
	 *         ResponseEntity with status NOT_FOUND and a message if no box types
	 *         are found.
	 */
	@Operation(summary = "Get box types by category", description = "Retrieves all box types in the system by category.")
	@ApiResponse(responseCode = "200", description = "Box types retrieved successfully")
	@ApiResponse(responseCode = "404", description = "No box types found")
	@GetMapping("/getlistbycategory")
	public ResponseEntity<?> getBoxTypesListByCategory(@RequestParam String category) {
		LOGGER.info("Received find box type by category request: " + category);
		List<String> boxTypeDTO = boxTypeService.getBoxTypeNameByCategory(category);
		if (null != boxTypeDTO) {
			LOGGER.info("Box types found");
			return ResponseEntity.status(HttpStatus.OK).body(boxTypeDTO);
		} else {
			LOGGER.error("No box types found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No box types found");
		}
	}

	/**
	 * Check if the box type is gateway.
	 *
	 * @param boxType the box type to check
	 * @return a boolean indicating if the box type is gateway
	 */

	@Operation(summary = "Check if the box type is gateway", description = "Check if the box type is gateway.")
	@ApiResponse(responseCode = "200", description = "Box type is gateway")
	@ApiResponse(responseCode = "404", description = "Box type is not gateway")
	@GetMapping("/istheboxtypegateway")
	public boolean isTheBoxTypeGateway(@RequestParam String boxType) {
		LOGGER.info("Received find box type by category request: " + boxType);
		return boxTypeService.isTheBoxTypeGateway(boxType);
	}

	/**
	 * Retrieves all box type names in the system by category other than the box
	 * type name
	 *
	 * @param category the category of the box types to retrieve
	 * @param boxtype  the name of the box type to exclude
	 * @return a ResponseEntity containing the list of box types if found, or a
	 *         ResponseEntity with status NOT_FOUND and a message if no box types
	 *         are found.
	 */
	@Operation(summary = "Get  box types list by category other than the box type name passed ", description = "Retrieves all box types in the system by category, excluded the boxtype name passed.")
	@ApiResponse(responseCode = "200", description = "Box types retrieved successfully")
	@ApiResponse(responseCode = "404", description = "No box types found")
	@GetMapping("/getlistofotherboxesbycategory")
	public ResponseEntity<?> getOtherBoxTypesListByCategory(@RequestParam String category,
			@RequestParam String boxtype) {
		LOGGER.info("Received find box type by category request: " + category);
		List<String> boxTypeDTO = boxTypeService.getBoxTypeNameByCategory(category);
		boxTypeDTO.remove(boxtype);
		if (null != boxTypeDTO && !boxTypeDTO.isEmpty()) {
			LOGGER.info("Box types found");
			return ResponseEntity.status(HttpStatus.OK).body(boxTypeDTO);
		} else {
			LOGGER.error("No box types found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No box types found");
		}
	}

}
