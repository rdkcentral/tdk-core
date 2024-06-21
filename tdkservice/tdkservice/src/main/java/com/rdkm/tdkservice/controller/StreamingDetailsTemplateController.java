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
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.rdkm.tdkservice.dto.StreamingDetailsTemplateDTO;
import com.rdkm.tdkservice.dto.StreamingTemplateUpdateDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsResponse;
import com.rdkm.tdkservice.service.IStreamingDetailsTemplateService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/**
 * The controller class that handles the API endpoints related to streaming
 * details templates.
 */

@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/streamingdetailstemplate")
public class StreamingDetailsTemplateController {

	private static final Logger LOGGER = LoggerFactory.getLogger(StreamingDetailsTemplateController.class);

	@Autowired
	IStreamingDetailsTemplateService streamingDetailsTemplateService;

	/**
	 * This method is used to create a new streaming details template in the system.
	 * It takes a StreamingDetailsTemplateDTO object as input, validates it and then
	 * calls the service method to create the template. If the template is created
	 * successfully, it returns a ResponseEntity with HTTP status 201 (Created) and
	 * a success message. If there is an error in creating the template, it returns
	 * a ResponseEntity with HTTP status 500 (Internal Server Error) and an error
	 * message.
	 * 
	 * @param templateDTO
	 * @return
	 */
	@Operation(summary = "Create a new Streaming Details Template", description = "Creates a new Streaming Details Template in the system.")
	@ApiResponse(responseCode = "201", description = "Template created successfully")
	@ApiResponse(responseCode = "500", description = "Error in saving template")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping("/create")
	public ResponseEntity<?> createStreamingTemplate(@RequestBody @Valid StreamingDetailsTemplateDTO templateDTO) {
		LOGGER.info("Received request to create template: " + templateDTO);
		boolean isTemplateCreated = streamingDetailsTemplateService.createStreamingDetailsTemplate(templateDTO);
		if (isTemplateCreated) {
			LOGGER.info("Template created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Template created succesfully");
		} else {
			LOGGER.error("Error in saving template data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in saving template");
		}
	}

	/**
	 * This method retrieves the streaming details for the provided template name.
	 * It calls the service method to get the streaming details and returns them in
	 * the response. If no streaming details are found, it returns a ResponseEntity
	 * with HTTP status 404 (Not Found) and an error message.
	 * 
	 * @param templateName
	 * @return
	 */
	@Operation(summary = "Get Streaming Details by Template Name", description = "Gets the streaming details for the provided template name.")
	@ApiResponse(responseCode = "200", description = "Streaming details retrieved successfully")
	@ApiResponse(responseCode = "404", description = "Streaming details not found")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/getstreamingdetailsbytemplatename")
	public ResponseEntity<?> getStreamingDetailsByTemplateName(@RequestParam String templateName) {
		LOGGER.info("Received request to get streaming details for template: " + templateName);
		List<StreamingDetailsResponse> streamingDetails = streamingDetailsTemplateService
				.getStreamingDetailsByTemplateName(templateName);
		if (streamingDetails != null && !streamingDetails.isEmpty()) {
			LOGGER.info("Streaming details found for the template");
			return ResponseEntity.status(HttpStatus.OK).body(streamingDetails);
		} else {
			LOGGER.error("No streaming details found for the template");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No streaming details found for the template");
		}

	}

	/**
	 * This method updates a streaming details template in the system. It takes a
	 * StreamingTemplateUpdateDTO object as input, validates it and then calls the
	 * service method to update the template. If the template is updated
	 * successfully, it returns a ResponseEntity with HTTP status 200 (OK) and a
	 * success message. If there is an error in updating the template, it returns a
	 * ResponseEntity with HTTP status 500 (Internal Server Error) and an error
	 * message.
	 * 
	 * @param templateDTO
	 * @return
	 */

	@Operation(summary = "Update a Streaming Details Template", description = "Updates a Streaming Details Template in the system.")
	@ApiResponse(responseCode = "200", description = "Template updated successfully")
	@ApiResponse(responseCode = "500", description = "Error in updating template")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PutMapping("/update")
	public ResponseEntity<?> updateTemplate(@RequestBody @Valid StreamingTemplateUpdateDTO templateDTO) {
		LOGGER.info("Received request to update template: " + templateDTO);
		boolean isTemplateUpdated = streamingDetailsTemplateService.updateTemplate(templateDTO);
		if (isTemplateUpdated) {
			LOGGER.info("Template updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Template updated succesfully");
		} else {
			LOGGER.error("Error in updating template data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in updating template");
		}
	}

	/**
	 * This method deletes a streaming details template in the system. It takes the
	 * name of the template as input and calls the service method to delete the
	 * template. If the template is deleted successfully, it returns a
	 * ResponseEntity with HTTP status 200 (OK) and a success message. If there is
	 * an error in deleting the template, it returns a ResponseEntity with HTTP
	 * status 500 (Internal Server Error) and an error message.
	 * 
	 * @param templateName
	 * @return
	 */

	@Operation(summary = "Delete  Streaming Details Template", description = "Deletes a Streaming Details Template in the system.")
	@ApiResponse(responseCode = "200", description = "Template deleted successfully")
	@ApiResponse(responseCode = "500", description = "Error in deleting template")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@DeleteMapping("/delete")
	public ResponseEntity<String> deleteTemplate(@RequestParam String templateName) {
		LOGGER.info("Received request to delete template: " + templateName);
		boolean isTemplateDeleted = streamingDetailsTemplateService.deleteTemplate(templateName);
		if (isTemplateDeleted) {
			LOGGER.info("Template deleted successfully");
			return ResponseEntity.status(HttpStatus.OK).body("Template deleted succesfully");
		} else {
			LOGGER.error("Error in deleting template data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in deleting template");
		}
	}

	/**
	 * This method retrieves a list of all streaming details templates in the
	 * system. It calls the service method to get the list of templates and returns
	 * them in the response. If no templates are found, it returns a ResponseEntity
	 * with HTTP status 404 (Not Found) and an error message.
	 * 
	 * @return
	 */
	@Operation(summary = "Get list of templates", description = "Retrieves a list of templates in the system.")
	@ApiResponse(responseCode = "200", description = "Templates found")
	@ApiResponse(responseCode = "404", description = "No templates found")
	@ApiResponse(responseCode = "500", description = "Error in fetching templates")
	@GetMapping("/gettemplatelist")
	public ResponseEntity<?> getTemplateList() {
		LOGGER.info("Received request to get template list");
		List<String> templateList = streamingDetailsTemplateService.getTemplateList();
		if (templateList != null && !templateList.isEmpty()) {
			LOGGER.info("Templates found:", templateList.toString());
			return ResponseEntity.status(HttpStatus.OK).body(templateList);
		} else {
			LOGGER.error("No template found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No template found");
		}
	}

}
