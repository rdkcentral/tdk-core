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

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import com.rdkm.tdkservice.dto.ParameterCreateDTO;
import com.rdkm.tdkservice.dto.ParameterDTO;
import com.rdkm.tdkservice.enums.ParameterDataType;
import com.rdkm.tdkservice.service.IParameterService;

public class ParameterControllerTest {

	@Mock
	private IParameterService parameterService;

	@InjectMocks
	private ParameterController parameterController;

	private MockMvc mockMvc;

	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
		mockMvc = MockMvcBuilders.standaloneSetup(parameterController).build();
	}

	@Test
	public void testCreateParameter() throws Exception {
		when(parameterService.createParameter(any(ParameterCreateDTO.class))).thenReturn(true);

		mockMvc.perform(post("/api/v1/parameter/create").contentType(MediaType.APPLICATION_JSON)
				.content("{\"someField\":\"someValue\"}")).andExpect(status().isCreated())
				.andExpect(content().string("Parameter created successfully"));
	}

	@Test
	public void testUpdateParameter() throws Exception {
		when(parameterService.updateParameter(any(ParameterDTO.class))).thenReturn(true);

		mockMvc.perform(put("/api/v1/parameter/update").contentType(MediaType.APPLICATION_JSON)
				.content("{\"someField\":\"someValue\"}")).andExpect(status().isOk())
				.andExpect(content().string("Parameter updated successfully"));
	}

	@Test
	public void testFindAllParameter() throws Exception {
		List<ParameterDTO> parameters = Arrays.asList(new ParameterDTO(), new ParameterDTO());
		when(parameterService.findAllParameters()).thenReturn(parameters);

		mockMvc.perform(get("/api/v1/parameter/findAll")).andExpect(status().isOk())
				.andExpect(content().contentType(MediaType.APPLICATION_JSON)).andExpect(jsonPath("$").isArray())
				.andExpect(jsonPath("$.length()").value(2));
	}

	@Test
	public void testFindParameterById() throws Exception {
	    UUID parameterId = UUID.randomUUID(); // Generate a sample UUID
	    ParameterDTO dto = new ParameterDTO(); // Create a mock ParameterDTO object

	    // Mock the service to return the DTO when findParameterById is called with the parameterId
	    when(parameterService.findParameterById(parameterId)).thenReturn(dto);

	    // Correct the URL to include the actual UUID instead of "parameterId"
	    mockMvc.perform(get("/api/v1/parameter/findById/" + parameterId))
	            .andExpect(status().isOk()) // Check if status is 200 (OK)
	            .andExpect(content().contentType(MediaType.APPLICATION_JSON)); // Check if content type is JSON
	}

	@Test
	public void testDeleteParameter() throws Exception {
		UUID parameterId = UUID.randomUUID();
		when(parameterService.deleteParameter(parameterId)).thenReturn(true);

		mockMvc.perform(delete("/api/v1/parameter/delete/"+ parameterId)).andExpect(status().isOk())
				.andExpect(content().string("Parameter deleted successfully"));
	}

	@Test
	public void testFindAllParametersByFunction() throws Exception {
		List<ParameterDTO> parameters = Arrays.asList(new ParameterDTO(), new ParameterDTO());
		when(parameterService.findAllParametersByFunction(anyString())).thenReturn(parameters);

		mockMvc.perform(get("/api/v1/parameter/findAllByFunction/testFunction")).andExpect(status().isOk())
				.andExpect(content().contentType(MediaType.APPLICATION_JSON)).andExpect(jsonPath("$").isArray())
				.andExpect(jsonPath("$.length()").value(2));
	}

	@Test
	public void testGetAllParameterEnums() throws Exception {
		List<ParameterDataType> enums = Arrays.asList(ParameterDataType.STRING, ParameterDataType.INTEGER);
		when(parameterService.getAllParameterEnums()).thenReturn(enums);

		mockMvc.perform(get("/api/v1/parameter/getListOfParameterEnums")).andExpect(status().isOk())
				.andExpect(content().contentType(MediaType.APPLICATION_JSON)).andExpect(jsonPath("$").isArray())
				.andExpect(jsonPath("$.length()").value(2));
	}

}
