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

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import java.util.Arrays;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.rdkm.tdkservice.dto.StreamingDetailsDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsUpdateDTO;
import com.rdkm.tdkservice.service.IStreamingDetailsService;
import com.rdkm.tdkservice.util.Constants;

/**
 * This class is used to test the StreamingDetailsController
 */
@SpringBootTest
@AutoConfigureMockMvc
public class StreamingDetailsControllerTest {

	@InjectMocks
	private StreamingDetailsController streamingDetailsController;

	@Mock
	private IStreamingDetailsService streamingDetailsService;

	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	@Autowired
	private MockMvc mockMvc;

	
	/**
	 * This method is used to test the createStreamingDetails method of the
	 * StreamingDetailsController
	 */
	@Test
	public void createStreamingDetails_Successful() {
		StreamingDetailsDTO streamingDetailsRequest = new StreamingDetailsDTO();
		when(streamingDetailsService.createStreamingDetails(streamingDetailsRequest)).thenReturn(true);

		ResponseEntity<String> response = streamingDetailsController.createStreamingDetails(streamingDetailsRequest);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
		assertEquals("Streaming details created succesfully", response.getBody());
	}

	/**
	 * This method is used to test the createStreamingDetail with internal server error
	 */
	@Test
	public void createStreamingDetails_Unsuccessful() {
		StreamingDetailsDTO streamingDetailsRequest = new StreamingDetailsDTO();
		when(streamingDetailsService.createStreamingDetails(streamingDetailsRequest)).thenReturn(false);

		ResponseEntity<String> response = streamingDetailsController.createStreamingDetails(streamingDetailsRequest);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Error in saving streaming details data", response.getBody());
	}

	/**
	 * This method is used to test the findAllStreamingDetails method of the
	 * StreamingDetailsController
	 */
	@Test
	public void findAllStreamingDetails_StreamingDetailsFound() {
		StreamingDetailsDTO streamingDetails = new StreamingDetailsDTO();
		when(streamingDetailsService.findAllStreamingDetails()).thenReturn(Arrays.asList(streamingDetails));

		ResponseEntity<?> response = streamingDetailsController.findAllStreamingDetails();

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(Arrays.asList(streamingDetails), response.getBody());
	}

	/**
	 * This method is used to test the findAllStreamingDetails with no streaming
	 * details found
	 */
	@Test
	public void findAllStreamingDetails_NoStreamingDetailsFound() {
		when(streamingDetailsService.findAllStreamingDetails()).thenReturn(null);

		ResponseEntity<?> response = streamingDetailsController.findAllStreamingDetails();

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("No Streaming Details found", response.getBody());
	}

	/**
	 * This method is used to test the updateStreamingDetails method of the
	 * StreamingDetailsController
	 */
	@Test
	public void updateStreamingDetails_Successful() {
		StreamingDetailsUpdateDTO streamingDetailsUpdateRequest = new StreamingDetailsUpdateDTO();
		when(streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateRequest))
				.thenReturn(streamingDetailsUpdateRequest);

		ResponseEntity<?> response = streamingDetailsController.updateStreamingDetails(streamingDetailsUpdateRequest);

		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

	/**
	 * This method is used to test the updateStreamingDetails with streaming details
	 * not found
	 */
	@Test
	public void getStreamingDetailsIds_StreamingDetailsIdsFound() {
		List<String> streamingDetailsIds = Arrays.asList("id1", "id2");
		when(streamingDetailsService.getStreamingDetailsIdsByStreamType()).thenReturn(streamingDetailsIds);

		ResponseEntity<?> response = streamingDetailsController.getStreamingDetailsIds();

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(streamingDetailsIds, response.getBody());
	}

	/**
	 * This method is used to test the getStreamingDetailsIds with no streaming
	 * details ids found
	 */
	@Test
	public void getStreamingDetailsIds_NoStreamingDetailsIdsFound() {
		when(streamingDetailsService.getStreamingDetailsIdsByStreamType()).thenReturn(null);

		ResponseEntity<?> response = streamingDetailsController.getStreamingDetailsIds();

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No streaming details ids found", response.getBody());
	}

	/**
	 * This method is used to test the getRadioStreamingDetailsId method of the
	 * StreamingDetailsController
	 */
	@Test
	public void getRadioStreamingDetailsId_RadioStreamingDetailsIdFound() {
		List<String> radioStreamingDetailsId = Arrays.asList("radioId1", "radioId2");
		when(streamingDetailsService.getRadioStreamingDetailsId()).thenReturn(radioStreamingDetailsId);

		ResponseEntity<?> response = streamingDetailsController.getRadioStreamingDetailsId();

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(radioStreamingDetailsId, response.getBody());
	}

	/**
	 * This method is used to test the getRadioStreamingDetailsId with no radio
	 * streaming details id found
	 */
	@Test
	public void getRadioStreamingDetailsId_NoRadioStreamingDetailsIdFound() {
		when(streamingDetailsService.getRadioStreamingDetailsId()).thenReturn(null);

		ResponseEntity<?> response = streamingDetailsController.getRadioStreamingDetailsId();

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("No radio streaming details id found", response.getBody());
	}

	/**
	 * This method is used to test the deleteStreamingDetails method of the
	 * StreamingDetailsController
	 */
	@Test
	public void deleteStreamingDetails_StreamingDetailsDeletedSuccessfully() {
		Integer id = 1;

		ResponseEntity<String> response = streamingDetailsController.deleteStreamingDetails(id);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals("Streaming details deleted successfully", response.getBody());
	}

	/**
	 * This method is used to test the deleteStreamingDetails with streaming details
	 * not found
	 */
	@Test
	public void findByStreamId_StreamingDetailsFound() {
		Integer id = 1;
		StreamingDetailsDTO streamingDetails = new StreamingDetailsDTO();
		when(streamingDetailsService.findById(id)).thenReturn(streamingDetails);

		ResponseEntity<?> response = streamingDetailsController.findByStreamId(id);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(streamingDetails, response.getBody());
	}

	/**
	 * This method is used to test the findByStreamId with streaming details not
	 * found
	 */
	@Test
	public void findByStreamId_StreamingDetailsNotFound() {
		Integer id = 1;
		when(streamingDetailsService.findById(id)).thenReturn(null);

		ResponseEntity<?> response = streamingDetailsController.findByStreamId(id);

		assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
		assertEquals("Streaming details with ID 1 not found.", response.getBody());
	}

	/**
	 * This method is used to test the createStreamingDetails with null stream type
	 * 
	 * @throws Exception
	 */
	@Test
	public void testCreateStreamingDetailsWithNullStreamType() throws Exception {
		StreamingDetailsDTO streamingDetailsDTO = new StreamingDetailsDTO();
		streamingDetailsDTO.setStreamingDetailsId("1234");
		streamingDetailsDTO.setStreamType(null);

		String json = new ObjectMapper().writeValueAsString(streamingDetailsDTO);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/streamingdetail/create")
				.contentType(MediaType.APPLICATION_JSON).content(json))
				.andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.streamType").value("Stream type is required"));
	}

	/*
	 * This method is used to test the createStreamingDetails with null stream id
	 */
	@Test
	public void testCreateStreamingDetailsWithNullStreamId() throws Exception {
		StreamingDetailsDTO streamingDetailsDTO = new StreamingDetailsDTO();
		streamingDetailsDTO.setChannelType(null);
		streamingDetailsDTO.setStreamingDetailsId(null);
		streamingDetailsDTO.setStreamType(Constants.RADIO_STREAM_TYPE);

		String json = new ObjectMapper().writeValueAsString(streamingDetailsDTO);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/streamingdetail/create")
				.contentType(MediaType.APPLICATION_JSON).content(json))
				.andExpect(MockMvcResultMatchers.status().isBadRequest()).andExpect(MockMvcResultMatchers
						.jsonPath("$.streamingDetailsId").value("Streaming details id is required"));
	}
}