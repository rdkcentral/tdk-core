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
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import com.rdkm.tdkservice.dto.FunctionCreateDTO;
import com.rdkm.tdkservice.dto.FunctionDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.Function;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.model.Parameter;
import com.rdkm.tdkservice.repository.FunctionRepository;
import com.rdkm.tdkservice.repository.ModuleRepository;
import com.rdkm.tdkservice.repository.ParameterRepository;

public class FunctionServiceTest {

	@Mock
	private FunctionRepository functionRepository;

	@Mock
	private ModuleRepository moduleRepository;

	@Mock
	private ParameterRepository parameterRepository;

	@InjectMocks
	private FunctionService functionService;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.openMocks(this);
	}

	@Test
	void testCreateFunction_Success() {
		UUID functionId = UUID.randomUUID();
		FunctionCreateDTO functionCreateDTO = new FunctionCreateDTO();
		functionCreateDTO.setFunctionName("TestFunction");
		functionCreateDTO.setFunctionCategory("RDKV");

		Module module = new Module();
		module.setName("TestModule");
		functionCreateDTO.setModuleName(module.getName());
		when(moduleRepository.findByName("TestModule")).thenReturn(module);
		when(functionRepository.existsByName("TestFunction")).thenReturn(false);
		// Mock the save operation to set the id on the function
		when(functionRepository.save(any(Function.class))).thenAnswer(invocation -> {
			Function savedFunction = invocation.getArgument(0);
			savedFunction.setId(functionId); // Set the id to simulate saving to DB
			return savedFunction;
		});
		boolean result = functionService.createFunction(functionCreateDTO);
		assertTrue(result);
		verify(functionRepository).save(any(Function.class));
	}

	@Test
	void testCreateFunction_AlreadyExists() {
		FunctionCreateDTO functionCreateDTO = new FunctionCreateDTO();
		functionCreateDTO.setModuleName("TestModule");
		functionCreateDTO.setFunctionName("TestFunction");

		when(functionRepository.existsByName("TestFunction")).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> functionService.createFunction(functionCreateDTO));
	}

	@Test
	void testUpdateFunction_Success() {
		UUID functionId = UUID.randomUUID();
		FunctionDTO functionDTO = new FunctionDTO();
		functionDTO.setId(functionId);
		functionDTO.setFunctionName("UpdatedFunction");

		Function function = new Function();
		function.setId(functionId);
		function.setName("OldFunction");

		when(functionRepository.findById(functionId)).thenReturn(Optional.of(function));
		when(functionRepository.existsByName("UpdatedFunction")).thenReturn(false);

		boolean result = functionService.updateFunction(functionDTO);

		assertTrue(result);
		verify(functionRepository).save(function);
	}

	@Test
	void testUpdateFunction_NotFound() {
		UUID functionId = UUID.randomUUID();
		FunctionDTO functionDTO = new FunctionDTO();
		functionDTO.setId(functionId);
		functionDTO.setFunctionName("UpdatedFunction");
		functionDTO.setFunctionCategory("RDKV");
		functionDTO.setModuleName("TestModule");

		when(functionRepository.findById(functionId)).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> functionService.updateFunction(functionDTO));
	}

	@Test
	void testFindAllFunctions() {
		List<Function> functions = Arrays.asList(new Function(), new Function());
		when(functionRepository.findAll()).thenReturn(functions);

		List<FunctionDTO> result = functionService.findAllFunctions();

		assertEquals(functions.size(), result.size());
	}

	@Test
	void testFindFunctionById_Success() {
		UUID functionId = UUID.randomUUID();
		Function function = new Function();
		function.setId(functionId);
		function.setCategory(Category.RDKV);
		function.setModule(new Module());
		function.setName("TestFunction");

		when(functionRepository.findById(functionId)).thenReturn(Optional.of(function));

		FunctionDTO result = functionService.findFunctionById(functionId);

		assertNotNull(result);
		assertEquals(functionId, result.getId());
	}

	@Test
	void testFindFunctionById_NotFound() {
		UUID functionId = UUID.randomUUID();
		when(functionRepository.findById(functionId)).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> functionService.findFunctionById(functionId));
	}

	@Test
	void testDeleteFunction_Success() {
		UUID functionId = UUID.randomUUID();
		when(functionRepository.existsById(functionId)).thenReturn(true);
		when(parameterRepository.findAllByFunctionId(functionId)).thenReturn(Collections.emptyList());

		functionService.deleteFunction(functionId);

		verify(functionRepository).deleteById(functionId);
	}

	@Test
	void testDeleteFunction_NotFound() {
		UUID functionId = UUID.randomUUID();
		when(functionRepository.existsById(functionId)).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> functionService.deleteFunction(functionId));
	}

	@Test
	void testFindAllByCategory() {
		List<Function> functions = Arrays.asList(new Function(), new Function());
		when(functionRepository.findAllByCategory(Category.RDKV)).thenReturn(functions);

		List<FunctionDTO> result = functionService.findAllByCategory("RDKV");

		assertEquals(functions.size(), result.size());
	}

	@Test
	void testFindAllByCategory_Empty() {
		when(functionRepository.findAllByCategory(Category.RDKV)).thenReturn(Collections.emptyList());

		List<FunctionDTO> result = functionService.findAllByCategory("RDKV");

		assertTrue(result.isEmpty());
	}

	@Test
	void testDeleteFunction_WithParameters() {
		UUID functionId = UUID.randomUUID();
		Function function = new Function();
		function.setId(functionId);

		Parameter parameter = new Parameter();
		parameter.setId(functionId);

		when(functionRepository.existsById(functionId)).thenReturn(true);
		when(parameterRepository.findAllByFunctionId(functionId)).thenReturn(Arrays.asList(parameter));

		functionService.deleteFunction(functionId);

		verify(parameterRepository).deleteById(functionId); // Verify correct method call
		verify(functionRepository).deleteById(functionId); // Verify function deletion
	}

}
