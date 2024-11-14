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
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.service.IRDKCertificationService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;

/**
 * Controller class for RDK Certification
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/rdkcertification")
public class RDKCertificationController {

	private static final Logger LOGGER =LoggerFactory.getLogger(RDKCertificationController.class);

	@Autowired
	IRDKCertificationService rdkCertificationService;

	/**
	 * API to create a new config file ,update an existing config file and upload also
	 * 
	 * @param file
	 * @return ResponseEntity<String>
	 */
	@Operation(summary = "Create a new config file", description = "Creates a new config file in the system.")
	@ApiResponse(responseCode = "201", description = "Config file created successfully")
	@ApiResponse(responseCode = "500", description = "Error in creating config file")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping("/create")
	public ResponseEntity<String> createOrUpdateOrUploadConfigFile(@RequestPart("pythonFile") MultipartFile file) {
		LOGGER.info("Inside createConfigFile method with fileName: {}", file.getOriginalFilename());
		boolean isConfigFileCreated = rdkCertificationService.createOrUpdateOrUploadConfigFile(file);
		if (isConfigFileCreated) {
			LOGGER.info("Config file created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Config file created successfully");
		} else {
			LOGGER.error("Error in creating config file");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in creating config file");
		}
	}

	/**
	 * API to download a config file
	 * 
	 * @param fileName
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Download a config file", description = "Download a config file in the system.")
	@ApiResponse(responseCode = "200", description = "Config file downloaded successfully")
	@ApiResponse(responseCode = "500", description = "Error in downloading config file")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/download")
	public ResponseEntity<?> downloadConfigFile(@RequestParam String fileName) {
		LOGGER.info("Inside downloadConfigFile method with fileName: {}");
		Resource resource = rdkCertificationService.downloadConfigFile(fileName);
		if (resource != null) {
			LOGGER.info("Config file downloaded successfully");
			return ResponseEntity.status(HttpStatus.OK)
					.header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + resource.getFilename() + "\"")
					.header("Access-Control-Expose-Headers", "content-disposition").body(resource);
		} else {
			LOGGER.error("Error in downloading config file");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in downloading config file");
		}

	}

	/**
	 * API to get all config file names
	 * 
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Get all config file names", description = "Get all config file names in the system.")
	@ApiResponse(responseCode = "200", description = "Config file names found")
	@ApiResponse(responseCode = "500", description = "Error in getting config file names")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/getall")
	public ResponseEntity<?> getAllConfigFileNames() {
		LOGGER.info("Inside getAllConfigFileNames method");
		List<String> configFileNames = rdkCertificationService.getAllConfigFileNames();
		if (configFileNames != null && !configFileNames.isEmpty()) {
			LOGGER.info("Config file names found successfully");
			return ResponseEntity.status(HttpStatus.OK).body(configFileNames);
		} else {
			LOGGER.error("No config file names found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No config file names found");
		}
	}
	
	/**
	 * API to get config file content
	 * 
	 * @param fileName
	 * @return ResponseEntity<?>
	 */
	@Operation(summary = "Get config file content", description = "Get config file content by file name.")
	@ApiResponse(responseCode = "200", description = "Config file content found")
	@ApiResponse(responseCode = "500", description = "Error in getting config file content")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/getconfigfilecontent")
	public ResponseEntity<?> getConfigFileContent(@RequestParam String fileName) {
		LOGGER.info("Inside getConfigFileContent method with fileName: {}");
		String configFileContent = rdkCertificationService.getConfigFileContent(fileName);
		if (configFileContent != null) {
			LOGGER.info("Config file content found successfully");
			return ResponseEntity.status(HttpStatus.OK).body(configFileContent);
		} else {
			LOGGER.error("No config file content found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No config file content found");
		}
	}

}
