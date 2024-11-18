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
package com.rdkm.tdkservice.serviceimpl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import com.rdkm.tdkservice.dto.ParameterCreateDTO;
import com.rdkm.tdkservice.dto.ParameterDTO;
import com.rdkm.tdkservice.enums.ParameterDataType;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.Function;
import com.rdkm.tdkservice.model.Parameter;
import com.rdkm.tdkservice.repository.FunctionRepository;
import com.rdkm.tdkservice.repository.ParameterRepository;

public class ParameterServiceTest {

	@Mock
	private ParameterRepository parameterRepository;

	@Mock
	private FunctionRepository functionRepository;

	@InjectMocks
	private ParameterService parameterService;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.openMocks(this);
	}

	@Test
	void testCreateParameter_Success() {
		UUID parameterId = UUID.randomUUID();
		ParameterCreateDTO parameterCreateDTO = new ParameterCreateDTO();
		parameterCreateDTO.setParameterName("NewParameter");
		parameterCreateDTO.setFunction("TestFunction");
		parameterCreateDTO.setParameterDataType(ParameterDataType.STRING);
		parameterCreateDTO.setParameterRangeVal("100");

		Function function = new Function();
		function.setName("TestFunction");

		Parameter savedParameter = new Parameter();
		savedParameter.setId(parameterId);
		savedParameter.setName("NewParameter");
		savedParameter.setFunction(function);
		savedParameter.setParameterDataType(ParameterDataType.STRING);

		when(parameterRepository.existsByName(parameterCreateDTO.getParameterName())).thenReturn(false);
		when(functionRepository.findByName(parameterCreateDTO.getFunction())).thenReturn(function);

		when(parameterRepository.save(any(Parameter.class))).thenAnswer(invocation -> {
			Parameter parameter = invocation.getArgument(0);
			parameter.setId(parameterId); // Set the id to simulate saving to DB
			return parameter;
		});
		boolean result = parameterService.createParameter(parameterCreateDTO);
		assertTrue(result);
	}

	@Test
	void testCreateParameter_FunctionNotFound() {
		ParameterCreateDTO parameterCreateDTO = new ParameterCreateDTO();
		parameterCreateDTO.setFunction("NonExistentFunction");

		when(functionRepository.findByName(parameterCreateDTO.getFunction())).thenReturn(null);

		assertThrows(ResourceNotFoundException.class, () -> parameterService.createParameter(parameterCreateDTO));
	}

	@Test
	void testUpdateParameter_Success() {
		UUID parameterId = UUID.randomUUID();
		ParameterDTO parameterDTO = new ParameterDTO();
		parameterDTO.setId(parameterId);
		parameterDTO.setParameterName("OldParameter");
		parameterDTO.setFunction("TestFunction");

		Function function = new Function();
		function.setName("TestFunction");
		Parameter parameter = new Parameter();
		parameter.setId(parameterId);
		parameter.setParameterDataType(ParameterDataType.FLOAT);
		parameter.setRangeVal("33");
		parameter.setName("OldParameter1");
		parameter.setFunction(function);

		when(parameterRepository.findById(parameterId)).thenReturn(Optional.of(parameter));
		when(functionRepository.findByName(parameterDTO.getFunction())).thenReturn(function);
		when(parameterRepository.existsByNameAndFunction(parameterDTO.getParameterName(), function)).thenReturn(false);


		boolean result = parameterService.updateParameter(parameterDTO);

		assertTrue(result);
		verify(parameterRepository).save(parameter);
	}

	@Test
	void testUpdateParameter_NotFound() {
		UUID parameterId = UUID.randomUUID();
		ParameterDTO parameterDTO = new ParameterDTO();
		parameterDTO.setId(parameterId);

		when(parameterRepository.findById(parameterDTO.getId())).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> parameterService.updateParameter(parameterDTO));
	}

	@Test
	void testUpdateParameter_NameAlreadyExists() {
		UUID parameterId = UUID.randomUUID();
		ParameterDTO parameterDTO = new ParameterDTO();
		parameterDTO.setId(parameterId);
		parameterDTO.setParameterName("OldParameter");
		parameterDTO.setFunction("TestFunction");

		Function function = new Function();
		function.setName("TestFunction");
		Parameter parameter = new Parameter();
		parameter.setId(parameterId);
		parameter.setParameterDataType(ParameterDataType.FLOAT);
		parameter.setRangeVal("33");
		parameter.setName("OldParameter1");
		parameter.setFunction(function);

		when(parameterRepository.findById(parameterId)).thenReturn(Optional.of(parameter));
		when(functionRepository.findByName(parameterDTO.getFunction())).thenReturn(function);
		when(parameterRepository.existsByNameAndFunction(parameterDTO.getParameterName(), function)).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> parameterService.updateParameter(parameterDTO));
	}

	@Test
	void testFindAllParameters() {
		List<Parameter> parameters = Arrays.asList(new Parameter(), new Parameter());

		when(parameterRepository.findAll()).thenReturn(parameters);

		List<ParameterDTO> result = parameterService.findAllParameters();

		assertFalse(result.isEmpty());
		assertEquals(parameters.size(), result.size());
	}

	@Test
	void testFindParameterById_Success() {
		UUID parameterId = UUID.randomUUID();
		Parameter parameter = new Parameter();
		parameter.setId(parameterId);

		when(parameterRepository.findById(parameterId)).thenReturn(Optional.of(parameter));

		ParameterDTO result = parameterService.findParameterById(parameterId);

		assertNotNull(result);
		assertEquals(parameterId, result.getId());
	}

	@Test
	void testFindParameterById_NotFound() {
		UUID parameterId = UUID.randomUUID();
		when(parameterRepository.findById(parameterId)).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> parameterService.findParameterById(parameterId));
	}

	@Test
	void testDeleteParameter_Success() {
		UUID parameterId = UUID.randomUUID();

		doNothing().when(parameterRepository).deleteById(parameterId);

		boolean result = parameterService.deleteParameter(parameterId);

		assertTrue(result);
		verify(parameterRepository).deleteById(parameterId);
	}

	@Test
	void testDeleteParameter_Failure() {
		UUID parameterId = UUID.randomUUID();

		doThrow(new RuntimeException()).when(parameterRepository).deleteById(parameterId);

		boolean result = parameterService.deleteParameter(parameterId);

		assertFalse(result);
	}

	@Test
	void testFindAllParametersByFunction_Success() {
		UUID functionId = UUID.randomUUID();
		String functionName = "TestFunction";
		Function function = new Function();
		function.setId(functionId);
		function.setName(functionName);

		List<Parameter> parameters = Arrays.asList(new Parameter(), new Parameter());

		when(functionRepository.findByName(functionName)).thenReturn(function);
		when(parameterRepository.findAllByFunctionId(function.getId())).thenReturn(parameters);

		List<ParameterDTO> result = parameterService.findAllParametersByFunction(functionName);

		assertFalse(result.isEmpty());
		assertEquals(parameters.size(), result.size());
	}

	@Test
	void testFindAllParametersByFunction_FunctionNotFound() {
		String functionName = "NonExistentFunction";

		when(functionRepository.findByName(functionName)).thenReturn(null);

		assertThrows(ResourceNotFoundException.class, () -> parameterService.findAllParametersByFunction(functionName));
	}

	@Test
	void testGetAllParameterEnums() {
		List<ParameterDataType> result = parameterService.getAllParameterEnums();

		assertNotNull(result);
		assertEquals(ParameterDataType.values().length, result.size());
	}
}