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
import org.springframework.web.bind.annotation.RestController;

import com.rdkm.tdkservice.dto.StreamingDetailsDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsUpdateDTO;
import com.rdkm.tdkservice.service.IStreamingDetailsService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/**
 * The controller class that handles the API end points related to streaming
 * details.
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/streamingdetail")
public class StreamingDetailsController {

	private static final Logger LOGGER = LoggerFactory.getLogger(StreamingDetailsController.class);

	@Autowired
	IStreamingDetailsService streamingDetailsService;

	/**
	 * Creates a new streaming details based on the provided streaming details
	 * request.
	 *
	 * @param streamingDetailsRequest The request object containing the details of
	 *                                the streaming details.
	 * @return A ResponseEntity containing the created streaming details if
	 *         successful, or an error message if unsuccessful.
	 */
	@Operation(summary = "Create a new streaming details", description = "Creates a new streaming details in the system.")
	@ApiResponse(responseCode = "201", description = "Streaming details created successfully")
	@ApiResponse(responseCode = "500", description = "Error in saving streaming details data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PostMapping("/create")
	public ResponseEntity<String> createStreamingDetails(
			@RequestBody @Valid StreamingDetailsDTO streamingDetailsRequest) {
		LOGGER.info("Received create streaming details request: " + streamingDetailsRequest.toString());
		boolean isStreamingDetailsCreated = streamingDetailsService.createStreamingDetails(streamingDetailsRequest);
		if (isStreamingDetailsCreated) {
			LOGGER.info("Streaming details created succesfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("Streaming details created succesfully");
		} else {
			LOGGER.error("Error in saving streaming details data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Error in saving streaming details data");
		}

	}

	/**
	 * Find all streaming details in the system.
	 *
	 * @return A ResponseEntity containing the list of streaming details if found,
	 *         or an error message if no streaming details are found.
	 */

	@Operation(summary = "Find all streaming details", description = "Find all streaming details in the system.")
	@ApiResponse(responseCode = "200", description = "Streaming details found")
	@ApiResponse(responseCode = "500", description = "Error in finding streaming details")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@GetMapping("/findall")
	public ResponseEntity<?> findAllStreamingDetails() {
		LOGGER.info("Received find all streaming details request");
		List<StreamingDetailsDTO> streamingDetails = streamingDetailsService.findAllStreamingDetails();
		if (streamingDetails != null) {
			LOGGER.info("Streaming details found");
			return ResponseEntity.status(HttpStatus.OK).body(streamingDetails);
		} else {
			LOGGER.error("No Streaming Details found");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("No Streaming Details found");
		}

	}

	/**
	 * Find streaming details by streamId.
	 *
	 * @param streamId The ID of the streaming details to retrieve.
	 * @return A ResponseEntity containing the streaming details if found, or an
	 *         error message if not found.
	 */

	@Operation(summary = "Get list of streaming details ids by stream type", description = "Retrieves a list of streaming details ids by stream type in the system.")
	@ApiResponse(responseCode = "200", description = "Streaming details ids found")
	@ApiResponse(responseCode = "404", description = "No streaming details ids found")
	@GetMapping("/getlistofstreamids")
	public ResponseEntity<?> getStreamingDetailsIds() {
		LOGGER.info("Received request to find all streaming details ids by stream type");
		List<String> streamingDetailsIds = streamingDetailsService.getStreamingDetailsIdsByStreamType();
		if (streamingDetailsIds != null && !streamingDetailsIds.isEmpty()) {
			LOGGER.info("Streaming details ids found");
			return ResponseEntity.status(HttpStatus.OK).body(streamingDetailsIds);
		} else {
			LOGGER.error("No streaming details ids found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No streaming details ids found");
		}
	}

	/**
	 * Find streaming details by streamId.
	 *
	 * @param streamId The ID of the streaming details to retrieve.
	 * @return A ResponseEntity containing the streaming details if found, or an
	 *         error message if not found.
	 */
	@Operation(summary = "Get radio streaming details id", description = "Retrieves radio streaming details id in the system.")
	@ApiResponse(responseCode = "200", description = "Radio streaming details id found")
	@ApiResponse(responseCode = "404", description = "No radio streaming details id found")
	@GetMapping("/getradiostreamid")
	public ResponseEntity<?> getRadioStreamingDetailsId() {
		LOGGER.info("Received request to find radio streaming details id");
		List<String> radioStreamingDetailsId = streamingDetailsService.getRadioStreamingDetailsId();
		if (radioStreamingDetailsId != null) {
			LOGGER.info("Radio streaming details id found");
			return ResponseEntity.status(HttpStatus.OK).body(radioStreamingDetailsId);
		} else {
			LOGGER.error("No radio streaming details id found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No radio streaming details id found");
		}
	}

	/**
	 * Find streaming details by streamId.
	 *
	 * @param streamId The ID of the streaming details to retrieve.
	 * @return A ResponseEntity containing the streaming details if found, or an
	 *         error message if not found.
	 */

	@Operation(summary = "Delete streaming details by streamId", description = "Delete streaming details in the system.")
	@ApiResponse(responseCode = "200", description = "Streaming details deleted successfully")
	@ApiResponse(responseCode = "500", description = "Error in deleting streaming details")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@DeleteMapping("/delete/{Id}")
	public ResponseEntity<String> deleteStreamingDetails(@PathVariable Integer Id) {
		LOGGER.info("Received delete streaming details request: " + Id);
		streamingDetailsService.deleteStreamingDetails(Id);
		LOGGER.info("Streaming details deleted successfully");
		return ResponseEntity.status(HttpStatus.OK).body("Streaming details deleted successfully");

	}

	/**
	 * Update streaming details in the system.
	 *
	 * @param id                            The id of the streaming details to be
	 *                                      updated.
	 * @param streamingDetailsUpdateRequest The request object containing the
	 *                                      details to be updated.
	 * @return A ResponseEntity containing the updated streaming details if
	 *         successful, or an error message if unsuccessful.
	 */

	@Operation(summary = "Update streaming details", description = "Update streaming details in the system.")
	@ApiResponse(responseCode = "200", description = "Streaming details updated successfully")
	@ApiResponse(responseCode = "500", description = "Error in updating streaming details")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@PutMapping("/update")
	public ResponseEntity<?> updateStreamingDetails(
			@RequestBody StreamingDetailsUpdateDTO streamingDetailsUpdateRequest) {
		LOGGER.info("Received update streaming details request: " + streamingDetailsUpdateRequest.toString());
		StreamingDetailsUpdateDTO streamingDetails = streamingDetailsService
				.updateStreamingDetails(streamingDetailsUpdateRequest);
		if (streamingDetails != null) {
			LOGGER.info("Streaming details updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body(streamingDetails);
		} else {
			LOGGER.error("Error in updating streaming details");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in updating streaming details");
		}
	
	}

	/**
	 * Find streaming details by streamId.
	 *
	 * @param streamId The ID of the streaming details to retrieve.
	 * @return A ResponseEntity containing the streaming details if found, or an
	 *         error message if not found.
	 */
	@Operation(summary = "Find streaming details by streamId", description = "Find streaming details by streamId in the system.")
	@ApiResponse(responseCode = "200", description = "Streaming details found")
	@ApiResponse(responseCode = "404", description = "Streaming details not found")
	@GetMapping("/findbystreamid/{Id}")
	public ResponseEntity<?> findByStreamId(@PathVariable Integer Id) {
		LOGGER.info("Received find streaming details by streamId request: " + Id);
		StreamingDetailsDTO streamingDetails = streamingDetailsService.findById(Id);
		if (streamingDetails != null) {
			LOGGER.info("Streaming details found");
			return ResponseEntity.status(HttpStatus.OK).body(streamingDetails);
		} else {
			LOGGER.error("Streaming details with ID " + Id + " not found ");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Streaming details with ID " + Id + " not found.");
		}
	}

}
