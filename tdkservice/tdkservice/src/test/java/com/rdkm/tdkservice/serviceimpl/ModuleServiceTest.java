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
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
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

import com.rdkm.tdkservice.dto.ModuleCreateDTO;
import com.rdkm.tdkservice.dto.ModuleDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.enums.TestGroup;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.Function;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.model.Parameter;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.FunctionRepository;
import com.rdkm.tdkservice.repository.ModuleRepository;
import com.rdkm.tdkservice.repository.ParameterRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;

public class ModuleServiceTest {

	@Mock
	private ModuleRepository moduleRepository;

	@Mock
	private UserGroupRepository userGroupRepository;

	@Mock
	private FunctionRepository functionRepository;

	@Mock
	private ParameterRepository parameterRepository;

	@InjectMocks
	private ModuleService moduleService;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.openMocks(this);
	}

	@Test
	void testSaveModule_Success() {
	    UUID moduleId = UUID.randomUUID();
	    ModuleCreateDTO moduleDTO = new ModuleCreateDTO();

	    moduleDTO.setModuleName("TestModule");
	    moduleDTO.setExecutionTime(10);
	    moduleDTO.setTestGroup(TestGroup.E2E.getName());
	    moduleDTO.setModuleCategory(Category.RDKV.getName());
	    moduleDTO.setUserGroup("userGroup1");

	    Module module = new Module();
	    module.setName(moduleDTO.getModuleName());
	    module.setExecutionTime(moduleDTO.getExecutionTime());
	    module.setCategory(Category.valueOf(moduleDTO.getModuleCategory()));
	    module.setTestGroup(TestGroup.valueOf(moduleDTO.getTestGroup()));
	    UserGroup userGroup = new UserGroup();
	    userGroup.setName("userGroup1");
	    module.setUserGroup(userGroup);

	    when(moduleRepository.existsByName(moduleDTO.getModuleName())).thenReturn(false);
	    when(userGroupRepository.findByName(anyString())).thenReturn(userGroup);

	    // Mock the save operation to set the id on the module
	    when(moduleRepository.save(any(Module.class))).thenAnswer(invocation -> {
	        Module savedModule = invocation.getArgument(0);
	        savedModule.setId(moduleId);  // Set the id to simulate saving to DB
	        return savedModule;
	    });

	    boolean result = moduleService.saveModule(moduleDTO);

	    assertTrue(result);
	    verify(moduleRepository).save(any(Module.class));
	}

	@Test
	void testSaveModule_AlreadyExists() {
		ModuleCreateDTO moduleDTO = new ModuleCreateDTO();
		moduleDTO.setModuleName("TestModule");

		when(moduleRepository.existsByName(moduleDTO.getModuleName())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> moduleService.saveModule(moduleDTO));
	}

	@Test
	void testSaveModule_InvalidCategory() {
		ModuleCreateDTO moduleDTO = new ModuleCreateDTO();
		moduleDTO.setModuleName("TestModule");
		moduleDTO.setModuleCategory("INVALID");
		moduleDTO.setTestGroup("E2E");
		moduleDTO.setUserGroup("tata"); // Ensure user group is set

		when(moduleRepository.existsByName(moduleDTO.getModuleName())).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> moduleService.saveModule(moduleDTO));
	}

	@Test
	void testUpdateModule_Success() {
		UUID moduleId = UUID.randomUUID();
		ModuleDTO moduleDTO = new ModuleDTO();
		moduleDTO.setId(moduleId);
		moduleDTO.setModuleName("UpdatedModule");
		moduleDTO.setExecutionTime(10);
		moduleDTO.setTestGroup(TestGroup.E2E.getName());
		moduleDTO.setModuleCategory(Category.RDKV.getName());

		Module existingModule = new Module();
		existingModule.setId(moduleId);
		existingModule.setName("OldModule");

		when(moduleRepository.findById(moduleDTO.getId())).thenReturn(Optional.of(existingModule));
		when(moduleRepository.save(any(Module.class))).thenReturn(existingModule);

		boolean result = moduleService.updateModule(moduleDTO);

		assertTrue(result);
		verify(moduleRepository).save(any(Module.class));
	}

	@Test
	void testUpdateModule_NotFound() {
		UUID moduleId = UUID.randomUUID();
		ModuleDTO moduleDTO = new ModuleDTO();
		moduleDTO.setId(moduleId);

		when(moduleRepository.findById(moduleDTO.getId())).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> moduleService.updateModule(moduleDTO));
	}

	@Test
	void testUpdateModule_NameAlreadyExists() {
		UUID moduleId = UUID.randomUUID();
		ModuleDTO moduleDTO = new ModuleDTO();
		moduleDTO.setId(moduleId);
		moduleDTO.setModuleName("UpdatedModule");

		Module existingModule = new Module();
		existingModule.setId(moduleId);
		existingModule.setName("OldModule");

		when(moduleRepository.findById(moduleDTO.getId())).thenReturn(Optional.of(existingModule));
		when(moduleRepository.existsByName(moduleDTO.getModuleName())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> moduleService.updateModule(moduleDTO));
	}

	@Test
	void testFindAllModules_Success() {
		// Arrange
		Module module1 = new Module();
		module1.setId(UUID.randomUUID());
		module1.setName("Module1");
		module1.setCategory(Category.RDKV);
		module1.setTestGroup(TestGroup.E2E);

		Module module2 = new Module();
		module2.setId(UUID.randomUUID());
		module2.setName("Module2");
		module2.setCategory(Category.RDKV);
		module2.setTestGroup(TestGroup.E2E);

		List<Module> modules = Arrays.asList(module1, module2);

		when(moduleRepository.findAll()).thenReturn(modules);

		// Act
		List<ModuleDTO> result = moduleService.findAllModules();

		// Assert
		assertFalse(result.isEmpty());
		assertEquals(modules.size(), result.size());
		assertEquals("Module1", result.get(0).getModuleName());
		assertEquals("Module2", result.get(1).getModuleName());
	}

	@Test
	void testFindAllModules_Empty() {
		when(moduleRepository.findAll()).thenReturn(Collections.emptyList());

		List<ModuleDTO> result = moduleService.findAllModules();

		assertTrue(result.isEmpty());
	}

	@Test
	void testFindModuleById_Success() {
		// Arrange
		UUID moduleId = UUID.randomUUID();
		Module module = new Module();
		module.setId(moduleId);
		module.setTestGroup(TestGroup.E2E);
		module.setCategory(Category.RDKV);
		module.setUserGroup(new UserGroup());
		when(moduleRepository.findById(moduleId)).thenReturn(Optional.of(module));

		// Act
		// ModuleDTO result = moduleService.findModuleById(id);
	}

	@Test
	void testFindModuleById_NotFound() {
		UUID moduleId = UUID.randomUUID();
		when(moduleRepository.findById(moduleId)).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> moduleService.findModuleById(moduleId));
	}

	@Test
	void testFindAllByCategory_Success() {
		List<Module> modules = new ArrayList<>();
		// Arrange
		Module module1 = new Module();
		module1.setId(UUID.randomUUID());
		module1.setName("Module1");
		module1.setCategory(Category.RDKV);
		module1.setTestGroup(TestGroup.E2E);
		modules.add(module1);

		Module module2 = new Module();
		module2.setId(UUID.randomUUID());
		module2.setName("Module2");
		module2.setCategory(Category.RDKV);
		module2.setTestGroup(TestGroup.E2E);
		modules.add(module2);

		List<Category> categories = new ArrayList<>();
		categories.add(Category.RDKV);
		categories.add(Category.RDKV_RDKSERVICE);

		when(moduleRepository.findAllByCategoryIn(categories)).thenReturn(modules);

		// Act
		List<ModuleDTO> result = moduleService.findAllByCategory("RDKV");

		// Assert
		assertFalse(result.isEmpty());
		assertEquals(modules.size(), result.size());
		assertEquals("Module1", result.get(0).getModuleName());
		assertEquals("Module2", result.get(1).getModuleName());
	}

	@Test
	void testFindAllByCategory_Empty() {
		when(moduleRepository.findAllByCategory(Category.RDKV)).thenReturn(Collections.emptyList());

		List<ModuleDTO> result = moduleService.findAllByCategory("RDKV");

		assertTrue(result.isEmpty());
	}

	@Test
	void testDeleteModule_Success() {
		UUID moduleId = UUID.randomUUID();
		Module module = new Module();
		module.setId(moduleId);

		when(moduleRepository.findById(moduleId)).thenReturn(Optional.of(module));
		when(functionRepository.findAllByModuleId(moduleId)).thenReturn(Collections.emptyList());

		boolean result = moduleService.deleteModule(moduleId);

		assertTrue(result);
		verify(moduleRepository).deleteById(moduleId);
	}

	@Test
	void testDeleteModule_NotFound() {
		UUID moduleId = UUID.randomUUID();
		when(moduleRepository.findById(moduleId)).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> moduleService.deleteModule(moduleId));
	}

	@Test
	void testDeleteModule_WithFunctionsAndParameters() {
		UUID moduleId = UUID.randomUUID();
		Module module = new Module();
		module.setId(moduleId);

		when(moduleRepository.findById(moduleId)).thenReturn(Optional.of(module));

		boolean result = moduleService.deleteModule(moduleId);

		assertTrue(result);
		verify(moduleRepository).deleteById(moduleId);
	}
}