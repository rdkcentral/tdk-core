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

import com.rdkm.tdkservice.dto.SocVendorDTO;
import com.rdkm.tdkservice.dto.SocVendorUpdateDTO;
import com.rdkm.tdkservice.service.ISocVendorService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/**
 * This class is the controller for SocVendor related operations. It handles the
 * creation, retrieval, update, and deletion of SocVendor entities.
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/socvendor")
public class SocVendorController {

	private static final Logger LOGGER = LoggerFactory.getLogger(SocVendorController.class);

	@Autowired
	ISocVendorService socVendorService;

	/**
	 * Creates a new SocVendor entity.
	 * 
	 * @param socVendorRequest
	 * @return
	 */
	@Operation(summary = "Create a new Soc Vendor", description = "Creates a new Soc Vendor in the system.")
	@ApiResponse(responseCode = "201", description = "Soc Vendor created successfully")
	@ApiResponse(responseCode = "500", description = "Error in saving Soc Vendor data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping("/create")
	public ResponseEntity<String> createSocVendor(@RequestBody @Valid SocVendorDTO socVendorRequest) {
		LOGGER.info("Received create soc vendor request: " + socVendorRequest.toString());
		boolean isSocVendorCreated = socVendorService.createSocVendor(socVendorRequest);
		if (isSocVendorCreated) {
			LOGGER.info("Soc vendor created succesfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Soc vendor created succesfully");
		} else {
			LOGGER.error("Error in saving soc vendor data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in saving soc vendor data");
		}

	}

	/**
	 * Retrieves all SOC vendors.
	 *
	 * @return ResponseEntity containing the list of SOC vendors if found, or a
	 *         NOT_FOUND status with an error message if no SOC vendors are found.
	 */
	@Operation(summary = "Retrieve all SOC vendors", description = "Retrieves all SOC vendors in the system.")
	@ApiResponse(responseCode = "200", description = "SOC vendors retrieved successfully")
	@ApiResponse(responseCode = "404", description = "No SOC vendors found")
	@GetMapping("/findall")
	public ResponseEntity<List<SocVendorDTO>> getAllSocVendors() {
		LOGGER.info("Received find all SocVendor request");
		List<SocVendorDTO> socVendors = socVendorService.findAll();
		if (socVendors != null && !socVendors.isEmpty()) {
			LOGGER.info("Soc vendors found");
			return ResponseEntity.status(HttpStatus.OK).body(socVendors);
		} else {
			LOGGER.error("No Soc vendors found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body(socVendors);
		}
	}

	/**
	 * Deletes a Soc vendor with the specified ID.
	 *
	 * @param id The ID of the Soc vendor to delete.
	 * @return A ResponseEntity with the status and message indicating the result of
	 *         the deletion.
	 */
	@Operation(summary = "Delete a Soc Vendor", description = "Deletes a Soc Vendor in the system.")
	@ApiResponse(responseCode = "200", description = "Soc Vendor deleted successfully")
	@ApiResponse(responseCode = "404", description = "Soc Vendor not found")
	@DeleteMapping("/delete/{id}")
	public ResponseEntity<?> deleteSocVendor(@PathVariable Integer id) {
		LOGGER.info("Received delete SocVendor request: " + id);
		socVendorService.deleteSocVendor(id);
		return ResponseEntity.status(HttpStatus.OK).body("Succesfully deleted the Soc vendor");

	}

	/**
	 * Retrieves a SocVendor object by its ID.
	 *
	 * @param id The ID of the SocVendor to retrieve.
	 * @return ResponseEntity containing the SocVendor object if found, or a
	 *         NOT_FOUND status with an error message if not found.
	 */
	@Operation(summary = "Find SocVendor by ID", description = "Retrieves a SocVendor by its ID.")
	@ApiResponse(responseCode = "200", description = "SocVendor found")
	@ApiResponse(responseCode = "404", description = "SocVendor not found")
	@GetMapping("/findbyid/{id}")
	public ResponseEntity<SocVendorDTO> findById(@PathVariable Integer id) {
		LOGGER.info("Received find SocVendor by id request: " + id);
		SocVendorDTO socVendor = socVendorService.findById(id);
		return ResponseEntity.status(HttpStatus.OK).body(socVendor);

	}

	/**
	 * Updates a SocVendor entity based on the provided SocVendorUpdateRequest.
	 * 
	 * @param socVendorUpdateRequest The SocVendorUpdateRequest object containing
	 *                               the updated data.
	 * @return ResponseEntity containing the updated SocVendor entity if it exists,
	 *         or a NOT_FOUND status if it doesn't.
	 */
	@Operation(summary = "Update a SocVendor", description = "Updates a SocVendor in the system.")
	@ApiResponse(responseCode = "200", description = "SocVendor updated successfully")
	@ApiResponse(responseCode = "404", description = "SocVendor not found")
	@ApiResponse(responseCode = "500", description = "Error in updating SocVendor data")
	@PutMapping("/update/{id}")
	public ResponseEntity<?> updateSocVendor(@PathVariable Integer id,
			@RequestBody SocVendorUpdateDTO socVendorUpdateDTO) {
		LOGGER.info("Received update SocVendor request: " + id);
		SocVendorUpdateDTO updatedSocVendor = socVendorService.updateSocVendor(socVendorUpdateDTO, id);
		if (updatedSocVendor != null) {
			LOGGER.info("Soc vendor updated succesfully");
			return ResponseEntity.status(HttpStatus.OK).body(updatedSocVendor);
		} else {
			LOGGER.error("Error in updating soc vendor data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in updating soc vendor data");
		}

	}

	/**
	 * Retrieves all SOC vendors by category.
	 *
	 * @param category The category of the SOC vendors to retrieve.
	 * @return ResponseEntity containing the list of SOC vendors if found, or a
	 *         NOT_FOUND status with an error message if no SOC vendors are found.
	 */

	@Operation(summary = "Find SOC vendors DTO by category", description = "Retrieves all SOC vendors DTO by category.")
	@ApiResponse(responseCode = "200", description = "SOC vendors found")
	@ApiResponse(responseCode = "404", description = "No SOC vendors found")
	@GetMapping("/findallbycategory")
	public ResponseEntity<?> getSOCVendorsByCategory(@RequestParam String category) {
		LOGGER.info("Received find SocVendor by category request: " + category);
		List<SocVendorDTO> socVendors = socVendorService.getSOCVendorsByCategory(category);
		if (socVendors != null && !socVendors.isEmpty()) {
			LOGGER.info("Soc vendors found");
			return ResponseEntity.status(HttpStatus.OK).body(socVendors);
		} else {
			LOGGER.error("No Soc vendors found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No Soc Vendors found with category: " + category);
		}
	}

	/**
	 * Retrieves all SOC vendors by category.
	 *
	 * @param category The category of the SOC vendors to retrieve.
	 * @return ResponseEntity containing the list of SOC vendors if found, or a
	 *         NOT_FOUND status with an error message if no SOC vendors are found.
	 */

	@Operation(summary = "Find SOC vendors name by category", description = "Retrieves all SOC vendors names list by category.")
	@ApiResponse(responseCode = "200", description = "SOC vendors found")
	@ApiResponse(responseCode = "404", description = "No SOC vendors found")
	@GetMapping("/getlistbycategory")
	public ResponseEntity<?> getSOCVendorsListByCategory(String category) {
		LOGGER.info("Received find SocVendor by category request: " + category);
		List<String> socVendorList = socVendorService.getSOCVendorsListByCategory(category);
		if (socVendorList != null && !socVendorList.isEmpty()) {
			LOGGER.info("Soc vendors found");
			return ResponseEntity.status(HttpStatus.OK).body(socVendorList);
		} else {
			LOGGER.error("No Soc vendors found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No Soc Vendors found with category: " + category);
		}

	}

}
