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
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.response.CreatePackageResponse;
import com.rdkm.tdkservice.service.IPackageManagerService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;

/*
 * The controller class that handles the API endpoints related to TDK package installation.
 */

@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/packagemanager")
public class PackageManagerController {

	private static final Logger LOGGER = LoggerFactory.getLogger(PackageManagerController.class);

	@Autowired
	private IPackageManagerService packageManagerService;

	/**
	 * This method is used to create the package.
	 * 
	 * @param type   -TDK,VTS
	 * @param device -Device name
	 * @return ResponseEntity<String>
	 */
	@Operation(summary = "Create Package API")
	@ApiResponse(responseCode = "200", description = "Created Package Successfully")
	@ApiResponse(responseCode = "400", description = "Bad Request")
	@ApiResponse(responseCode = "500", description = "Internal Server Error")
	@PostMapping("/createPackageAPI")
	public ResponseEntity<?> createPackageAPI(@RequestParam String type, @RequestParam String device) {
		LOGGER.info("createPackageAPI method is called");
		CreatePackageResponse response = packageManagerService.createPackage(type, device);
		if (response != null) {
			LOGGER.info("Package created successfully");
			return ResponseEntity.status(HttpStatus.OK).body(response);
		} else {
			LOGGER.error("Package creation failed");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Package creation failed");
		}

	}

	/**
	 * This method is used to get the available packages.
	 * 
	 * @param device name
	 * @return ResponseEntity<?> - List of available packages
	 */
	@Operation(summary = "Get Available Packages API")
	@ApiResponse(responseCode = "200", description = "Get Available Packages Successfully")
	@ApiResponse(responseCode = "400", description = "Bad Request")
	@ApiResponse(responseCode = "500", description = "Internal Server Error")
	@GetMapping("/getAvailablePackages")
	public ResponseEntity<?> getAvailablePackages(@RequestParam String device) {
		LOGGER.info("getAvailablePackages method is called");
		List<String> availablePackages = packageManagerService.getAvailablePackages(device);
		if (availablePackages != null) {
			LOGGER.info("Available packages are: {}", availablePackages);
			return ResponseEntity.status(HttpStatus.OK).body(availablePackages);
		} else {
			LOGGER.error("No available packages");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No available packages");
		}

	}

	/**
	 * This method is used to upload the package.
	 * 
	 * @param uploadFile -file to upload
	 * @return ResponseEntity<String> -success or failure message
	 */
	@Operation(summary = "Upload Package API")
	@ApiResponse(responseCode = "201", description = "Package Uploaded Successfully")
	@ApiResponse(responseCode = "400", description = "Bad Request")
	@ApiResponse(responseCode = "500", description = "Internal Server Error")
	@PostMapping("/uploadPackage")
	public ResponseEntity<String> uploadPackage(@RequestParam MultipartFile uploadFile, @RequestParam String device) {
		LOGGER.info("uploadPackage method is called");
		boolean status = packageManagerService.uploadPackage(uploadFile, device);
		if (status) {
			LOGGER.info("Package uploaded successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Package uploaded successfully");
		} else {
			LOGGER.error("Package upload failed");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Package upload failed");
		}
	}

	/**
	 * This method is used to install the package.
	 * 
	 * @param device      name
	 * @param packageName
	 * @return ResponseEntity<String> -success or failure message
	 */
	@Operation(summary = "Install Package API")
	@ApiResponse(responseCode = "200", description = "Package Installed Successfully")
	@ApiResponse(responseCode = "400", description = "Bad Request")
	@ApiResponse(responseCode = "500", description = "Internal Server Error")
	@GetMapping("/installPackage")
	public ResponseEntity<String> installPackage(@RequestParam String device, @RequestParam String packageName) {
		LOGGER.info("installPackage method is called");
		String log = packageManagerService.installPackage(device, packageName);
		if (log != null) {
			LOGGER.info("Package installed successfully");
			return ResponseEntity.status(HttpStatus.OK).body(log);
		} else {
			LOGGER.error("Package installation failed");
			return ResponseEntity.status(HttpStatus.OK).body("Package installation failed");

		}

	}
}
