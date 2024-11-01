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
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import com.rdkm.tdkservice.dto.ParameterValueDTO;
import com.rdkm.tdkservice.dto.PrimitiveTestCreateDTO;
import com.rdkm.tdkservice.dto.PrimitiveTestDTO;
import com.rdkm.tdkservice.dto.PrimitiveTestNameAndIdDTO;
import com.rdkm.tdkservice.dto.PrimitiveTestUpdateDTO;
import com.rdkm.tdkservice.enums.ParameterDataType;
import com.rdkm.tdkservice.model.Function;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.model.Parameter;
import com.rdkm.tdkservice.model.PrimitiveTest;
import com.rdkm.tdkservice.model.PrimitiveTestParameter;
import com.rdkm.tdkservice.repository.FunctionRepository;
import com.rdkm.tdkservice.repository.ModuleRepository;
import com.rdkm.tdkservice.repository.ParameterRepository;
import com.rdkm.tdkservice.repository.PrimitiveTestParameterRepository;
import com.rdkm.tdkservice.repository.PrimitiveTestRepository;

public class PrimitiveTestServiceTest {

	@InjectMocks
	private PrimitiveTestService primitiveTestService;

	@Mock
	private PrimitiveTestRepository primitiveTestRepository;

	@Mock
	private ModuleRepository moduleRepository;

	@Mock
	private FunctionRepository functionRepository;

	@Mock
	private ParameterRepository parameterRepository;

	@Mock
	private PrimitiveTestParameterRepository primitiveTestParameterRepository;

	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	@Test
	public void testCreatePrimitiveTest() {
		// Arrange
		PrimitiveTestCreateDTO primitiveTestDTO = new PrimitiveTestCreateDTO();
		primitiveTestDTO.setPrimitiveTestname("testName");
		primitiveTestDTO.setPrimitiveTestModuleName("testModule");
		primitiveTestDTO.setPrimitiveTestfunctionName("testFunction");
		primitiveTestDTO.setPrimitiveTestUserGroup("testUserGroup");
		List<ParameterValueDTO> parameters = new ArrayList<>();
		ParameterValueDTO parameterValueDTO = new ParameterValueDTO();
		parameterValueDTO.setParameterName("param1");

		parameterValueDTO.setParameterValue("value1");
		parameters.add(parameterValueDTO);
		primitiveTestDTO.setPrimitiveTestParameters(parameters);
		List<Parameter> parameterList = new ArrayList<>();
		Parameter parameter = new Parameter();
		parameter.setName("param1");
		parameter.setParameterDataType(ParameterDataType.STRING);
		parameter.setRangeVal("10");
		parameterList.add(parameter);

		when(primitiveTestRepository.existsByName(any(String.class))).thenReturn(false);
		when(moduleRepository.findByName(any(String.class))).thenReturn(new Module());
		when(functionRepository.findByName(any(String.class))).thenReturn(new Function());
		when(parameterRepository.findByFunction(any(Function.class))).thenReturn(parameterList);

		// Act
		boolean result = primitiveTestService.createPrimitiveTest(primitiveTestDTO);

		// Assert
		assertTrue(result);
	}

	@Test
	public void testDeleteById() {
		UUID primitiveTestId = UUID.randomUUID();
		PrimitiveTest primitiveTest = new PrimitiveTest();
		primitiveTest.setId(primitiveTestId);

		when(primitiveTestRepository.findById(primitiveTestId)).thenReturn(Optional.of(primitiveTest));

		// Act
		primitiveTestService.deleteById(primitiveTestId);

		// Assert
		verify(primitiveTestRepository, times(1)).delete(primitiveTest);
	}

	@Test
	public void testGetPrimitiveTestDetailsById() {
		// Arrange
		UUID primitiveTestId = UUID.randomUUID();
		PrimitiveTest primitiveTest = new PrimitiveTest();
		primitiveTest.setId(primitiveTestId);
		primitiveTest.setName("testName");

		Function function = new Function();
		function.setName("testFunction");
		primitiveTest.setFunction(function);

		Module module = new Module();
		module.setName("testModule");
		primitiveTest.setModule(module);

		when(primitiveTestRepository.findById(primitiveTestId)).thenReturn(Optional.of(primitiveTest));

		List<Parameter> parameters = new ArrayList<>();
		Parameter parameter = new Parameter();
		parameter.setName("param1");
		parameter.setParameterDataType(ParameterDataType.STRING); // Ensure ParameterDataType is set
		parameter.setFunction(function);
		parameters.add(parameter);
		Parameter parameter2 = new Parameter();
		parameter2.setName("param2");
		parameter2.setParameterDataType(ParameterDataType.STRING); // Ensure ParameterDataType is set
		parameter2.setFunction(function);
		parameters.add(parameter2);
		when(parameterRepository.findByFunction(function)).thenReturn(parameters);

		List<PrimitiveTestParameter> primitiveTestParameters = new ArrayList<>();
		PrimitiveTestParameter primitiveTestParameter = new PrimitiveTestParameter();
		primitiveTestParameter.setParameterName("param1");
		primitiveTestParameter.setParameterType("STRING");
		primitiveTestParameter.setParameterRange("50");
		primitiveTestParameter.setParameterValue("18");

		primitiveTestParameters.add(primitiveTestParameter);
		when(primitiveTestParameterRepository.findByPrimitiveTest(any(PrimitiveTest.class)))
				.thenReturn(primitiveTestParameters);

		// Act
		PrimitiveTestDTO result = primitiveTestService.getPrimitiveTestDetailsById(primitiveTestId);

		// Assert
		assertEquals(primitiveTestId, result.getPrimitiveTestId());
		assertEquals("testName", result.getPrimitiveTestName());
		assertEquals("testModule", result.getPrimitivetestModule());
		assertEquals("testFunction", result.getPrimitiveTestfunction());
		assertEquals("param1", result.getPrimitiveTestParameters().get(0).getParameterName());
		assertEquals("18", result.getPrimitiveTestParameters().get(0).getParameterValue());
	}

	@Test
	public void testUpdatePrimitiveTest() {
		UUID primitiveTestId = UUID.randomUUID();
		PrimitiveTestUpdateDTO primitiveTestDTO = new PrimitiveTestUpdateDTO();
		primitiveTestDTO.setPrimitiveTestId(primitiveTestId);
		List<ParameterValueDTO> parameters = new ArrayList<>();
		ParameterValueDTO parameterValueDTO = new ParameterValueDTO();
		parameterValueDTO.setParameterName("param1");
		parameterValueDTO.setParameterValue("value1");
		parameters.add(parameterValueDTO);
		ParameterValueDTO parameterValueDTO2 = new ParameterValueDTO();
		parameterValueDTO2.setParameterName("param2");
		parameterValueDTO2.setParameterValue("value2");
		parameters.add(parameterValueDTO2);
		primitiveTestDTO.setPrimitiveTestParameters(parameters);

		PrimitiveTest primitiveTest = new PrimitiveTest();
		// primitiveTest.setId(1);
		primitiveTest.setName("testName");
		primitiveTest.setModule(new Module());
		primitiveTest.setFunction(new Function());

		PrimitiveTestParameter primitiveTestParameter = new PrimitiveTestParameter();
		primitiveTestParameter.setPrimitiveTest(primitiveTest);
		primitiveTestParameter.setParameterName("param1");
		parameterValueDTO.setParameterValue("value");
		Parameter parameter = new Parameter();
		parameter.setName("param2");
		parameter.setParameterDataType(ParameterDataType.STRING);
		parameter.setRangeVal("10");

		when(primitiveTestRepository.findById(primitiveTestId)).thenReturn(Optional.of(primitiveTest));
		when(primitiveTestParameterRepository.findByPrimitiveTest(primitiveTest))
				.thenReturn(Arrays.asList(primitiveTestParameter));
		when(parameterRepository.findByName("param2")).thenReturn(parameter);

		boolean result = primitiveTestService.updatePrimitiveTest(primitiveTestDTO);
		assertTrue(result);

	}

	@Test
	public void testGetPrimitiveTestDetailsByModuleName() {
		String moduleName = "testModule";
		Module module = new Module();
		module.setName(moduleName);

		PrimitiveTest primitiveTest = new PrimitiveTest();
		primitiveTest.setModule(module);

		PrimitiveTestNameAndIdDTO primitiveTestDTO = new PrimitiveTestNameAndIdDTO();
		primitiveTestDTO.setPrimitiveTestId(primitiveTest.getId());
		primitiveTestDTO.setPrimitiveTestName(primitiveTest.getName());

		when(moduleRepository.findByName(moduleName)).thenReturn(module);
		when(primitiveTestRepository.findByModule(module)).thenReturn(Arrays.asList(primitiveTest));

		List<PrimitiveTestNameAndIdDTO> result = primitiveTestService.getPrimitiveTestDetailsByModuleName(moduleName);

		assertEquals(1, result.size());
		assertEquals(primitiveTestDTO.getPrimitiveTestId(), result.get(0).getPrimitiveTestId());
		assertEquals(primitiveTestDTO.getPrimitiveTestName(), result.get(0).getPrimitiveTestName());
	}

	@Test
	public void testFindAllByModuleName() {
		UUID primitiveTestId = UUID.randomUUID();
		// Arrange
		String moduleName = "testModule";
		Module module = new Module();
		module.setName(moduleName);

		Function function = new Function();
		function.setName("testFunction");
		function.setModule(module);

		PrimitiveTest primitiveTest1 = new PrimitiveTest();
		primitiveTest1.setId(primitiveTestId);
		primitiveTest1.setName("test1");
		primitiveTest1.setModule(module);
		primitiveTest1.setFunction(function);

		PrimitiveTest primitiveTest2 = new PrimitiveTest();
		primitiveTest2.setId(primitiveTestId);
		primitiveTest2.setName("test2");
		primitiveTest2.setModule(module);
		primitiveTest2.setFunction(function);

		List<PrimitiveTest> primitiveTests = Arrays.asList(primitiveTest1, primitiveTest2);

		when(moduleRepository.findByName(moduleName)).thenReturn(module);
		when(primitiveTestRepository.findByModule(module)).thenReturn(primitiveTests);

		// Act
		List<PrimitiveTestDTO> result = primitiveTestService.findAllByModuleName(moduleName);

		// Assert
		assertEquals(2, result.size());
		assertEquals("test1", result.get(0).getPrimitiveTestName());
		assertEquals("test2", result.get(1).getPrimitiveTestName());
	}

}
