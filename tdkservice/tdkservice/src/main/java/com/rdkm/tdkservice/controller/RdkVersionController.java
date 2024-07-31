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

import com.rdkm.tdkservice.dto.RdkVersionCreateDTO;
import com.rdkm.tdkservice.dto.RdkVersionDTO;
import com.rdkm.tdkservice.service.IRdkVersionService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/*
 * The RdkVersionController class is a REST controller that handles rdk version operations.
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/rdkversion")
public class RdkVersionController {

	private static final Logger LOGGER = LoggerFactory.getLogger(RdkVersionController.class);

	@Autowired
	IRdkVersionService rdkVersionService;

	/**
	 * This method is used to create the rdk version
	 *
	 * @param rdkVersionCreateDTO - RdkVersionCreateDTO object
	 * @return ResponseEntity<String> - response entity - message
	 */
	@Operation(summary = "Create Rdk Version", description = "Create Rdk Version")
	@ApiResponse(responseCode = "201", description = "Rdk version created successfully")
	@ApiResponse(responseCode = "500", description = "Error in saving rdk version data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping("/create")
	public ResponseEntity<?> createRdkVersion(@Valid @RequestBody RdkVersionCreateDTO rdkVersionCreateDTO) {
		LOGGER.info("Received create rdk version request: " + rdkVersionCreateDTO.toString());
		boolean isRdkVersionCreated = rdkVersionService.createRdkVersion(rdkVersionCreateDTO);
		if (isRdkVersionCreated) {
			LOGGER.info("Rdk version created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Rdk version created successfully");
		} else {
			LOGGER.error("Error in saving rdk version data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in saving rdk version data");
		}

	}

	/**
	 * This method is used to update the rdk version
	 *
	 * @param rdkVersionDTO - RdkVersionDTO object
	 * @return ResponseEntity<String> - response entity - message
	 */
	@Operation(summary = "Update Rdk Version", description = "Update Rdk Version")
	@ApiResponse(responseCode = "200", description = "Rdk version updated successfully")
	@ApiResponse(responseCode = "500", description = "Error in updating rdk version data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PutMapping("/update")
	public ResponseEntity<?> updateRdkVersion(@Valid @RequestBody RdkVersionDTO rdkVersionDTO) {
		LOGGER.info("Received update rdk version request: " + rdkVersionDTO.toString());
		boolean isRdkVersionUpdated = rdkVersionService.updateRdkVersion(rdkVersionDTO);
		if (isRdkVersionUpdated) {
			LOGGER.info("Rdk version updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Rdk version updated successfully");
		} else {
			LOGGER.error("Error in updating rdk version data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in updating rdk version data");
		}
	}

	/**
	 * This method is used to delete the rdk version
	 *
	 * @param id - Integer - the rdk version id
	 * @return ResponseEntity<String> - response entity - message
	 */
	@Operation(summary = "Delete Rdk Version", description = "Delete Rdk Version")
	@ApiResponse(responseCode = "200", description = "Rdk version deleted successfully")
	@ApiResponse(responseCode = "500", description = "Error in deleting rdk version")
	@DeleteMapping("/delete/{id}")
	public ResponseEntity<String> deleteRdkVersion(@PathVariable Integer id) {
		LOGGER.info("Received delete rdk version request: " + id.toString());
		rdkVersionService.deleteRdkVersion(id);
		LOGGER.info("Rdk version deleted successfully");
		return ResponseEntity.status(HttpStatus.OK).body("Rdk version deleted successfully");

	}

	/**
	 * This method is used to find all rdk versions
	 *
	 * @return ResponseEntity<List<RdkVersionDTO>> - response entity - list of rdk
	 *         versions
	 */
	@Operation(summary = "Find All Rdk Versions", description = "Find All Rdk Versions")
	@ApiResponse(responseCode = "200", description = "Rdk versions found")
	@ApiResponse(responseCode = "404", description = "No rdk versions found")
	@GetMapping("/findall")
	public ResponseEntity<?> findAllRdkVersions() {
		LOGGER.info("Received find all rdk versions request");
		List<RdkVersionDTO> rdkVersionDTOList = rdkVersionService.findAllRdkVersions();
		if (null != rdkVersionDTOList && !rdkVersionDTOList.isEmpty()) {
			LOGGER.info("Found all rdk versions:" + rdkVersionDTOList.toString());
			return ResponseEntity.status(HttpStatus.OK).body(rdkVersionDTOList);
		} else {
			LOGGER.error("No rdk versions found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No rdk versions found");
		}
	}

	/**
	 * This method is used to find all rdk versions by category
	 *
	 * @param category - String - the rdk version category
	 * @return ResponseEntity<List<RdkVersionDTO>> - response entity - list of rdk
	 *         versions
	 */
	@Operation(summary = "Find All Rdk Versions By Category", description = "Find All Rdk Versions By Category")
	@ApiResponse(responseCode = "200", description = "Rdk versions found by category")
	@ApiResponse(responseCode = "404", description = "No rdk versions found by category")
	@GetMapping("/findallbycategory")
	public ResponseEntity<?> findAllRdkVersionsByCategory(@RequestParam String category) {
		LOGGER.info("Received find all rdk versions by category request: " + category);
		List<RdkVersionDTO> rdkVersionDTOList = rdkVersionService.findAllRdkVersionsByCategory(category);
		if (null != rdkVersionDTOList && !rdkVersionDTOList.isEmpty()) {
			LOGGER.info("Found all rdk versions by category:" + rdkVersionDTOList.toString());
			return ResponseEntity.status(HttpStatus.OK).body(rdkVersionDTOList);
		} else {
			LOGGER.error("No rdk versions found by category");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No rdk versions found by category");
		}
	}

	/**
	 * This method is used to get rdk version list by category
	 *
	 * @param category - String - the rdk version category
	 * @return ResponseEntity<List<String>> - response entity - list of rdk versions
	 */
	@Operation(summary = "Get Rdk Version List By Category", description = "Get Rdk Version List By Category")
	@ApiResponse(responseCode = "200", description = "Rdk versions found by category")
	@ApiResponse(responseCode = "404", description = "No rdk versions found by category")
	@GetMapping("/getlistbycategory")
	public ResponseEntity<?> getRdkVersionListByCategory(@RequestParam String category) {
		LOGGER.info("Received get rdk version list by category request: " + category);
		List<String> rdkVersionList = rdkVersionService.getRdkVersionListByCategory(category);
		if (null != rdkVersionList && !rdkVersionList.isEmpty()) {
			LOGGER.info("Found rdk versions by category:" + rdkVersionList);
			return ResponseEntity.status(HttpStatus.OK).body(rdkVersionList);
		} else {
			LOGGER.error("No rdk versions found by category");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No rdk versions found by category");
		}
	}

	/**
	 * This method is used to find rdk version by id
	 *
	 * @param id - Integer the rdk version id
	 * @return ResponseEntity<RdkVersionDTO> - response entity - rdk version
	 **/
	@Operation(summary = "Find Rdk Version By Id", description = "Find Rdk Version By Id")
	@ApiResponse(responseCode = "200", description = "Rdk version found by id")
	@ApiResponse(responseCode = "404", description = "No rdk version found by id")
	@GetMapping("/findbyid/{id}")
	public ResponseEntity<?> findRdkVersionById(@PathVariable Integer id) {
		LOGGER.info("Received find rdk version by id request: " + id.toString());
		RdkVersionDTO rdkVersionDTO = rdkVersionService.findRdkVersionById(id);
		if (null != rdkVersionDTO) {
			LOGGER.info("Found rdk version by id:" + rdkVersionDTO.toString());
			return ResponseEntity.status(HttpStatus.OK).body(rdkVersionDTO);
		} else {
			LOGGER.error("No rdk version found by id");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No rdk version found by id");
		}
	}
}
