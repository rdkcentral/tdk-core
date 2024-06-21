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
package com.rdkm.tdkservice.service;

import java.util.List;

import com.rdkm.tdkservice.dto.StreamingDetailsDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsUpdateDTO;

import jakarta.validation.Valid;

/**
 * The service interface that provides the methods for managing streaming
 * details.
 */
public interface IStreamingDetailsService {

	/**
	 * Creates a new streaming details based on the provided streaming details
	 * request.
	 *
	 * @param streamingDetailsRequest The request object containing the details of
	 *                                the streaming details.
	 * @return A boolean value indicating whether the streaming details were created
	 *         successfully.
	 */

	boolean createStreamingDetails(@Valid StreamingDetailsDTO streamingDetailsRequest);

	/**
	 * Retrieves all streaming details from the database.
	 *
	 * @return A list of all streaming details.
	 */
	List<StreamingDetailsDTO> findAllStreamingDetails();

	/**
	 * Updates the streaming details with the provided id based on the provided
	 * streaming details update request.
	 *
	 * @param streamingDetailsUpdateRequest The request object containing the
	 *                                      updated details of the streaming
	 *                                      details.
	 * @param id                            The id of the streaming details to be
	 *                                      updated.
	 * @return The updated streaming details.
	 */
	StreamingDetailsUpdateDTO updateStreamingDetails(StreamingDetailsUpdateDTO streamingDetailsUpdateRequest);

	/**
	 * Retrieves the streaming details with the provided id.
	 *
	 * @param id The id of the streaming details to be retrieved.
	 * @return The streaming details with the provided id.
	 */
	List<String> getStreamingDetailsIdsByStreamType();

	/**
	 * Deletes the streaming details with the provided id.
	 *
	 * @param streamId The id of the streaming details to be deleted.
	 */
	void deleteStreamingDetails(Integer streamId);

	/**
	 * Retrieves the streaming details with the provided id.
	 *
	 * @param streamId The id of the streaming details to be retrieved.
	 * @return The streaming details with the provided id.
	 */
	List<String> getRadioStreamingDetailsId();

	/**
	 * Retrieves the streaming details with the provided id.
	 *
	 * @param streamId The id of the streaming details to be retrieved.
	 * @return The streaming details with the provided
	 */
	StreamingDetailsDTO findById(Integer streamId);

}
