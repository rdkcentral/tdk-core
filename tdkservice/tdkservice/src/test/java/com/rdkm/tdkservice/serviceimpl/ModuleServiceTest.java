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
import com.rdkm.tdkservice.serviceimpl.ModuleService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

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
        ModuleCreateDTO moduleDTO = new ModuleCreateDTO();
        Module module=new Module();
        module.setId(1);
        moduleDTO.setModuleName("TestModule");
        moduleDTO.setExecutionTime(10);
        moduleDTO.setTestGroup(TestGroup.E2E.getName());
        moduleDTO.setModuleCategory(Category.RDKV.getName());


        UserGroup userGroup = new UserGroup();
        userGroup.setName("tata");
        moduleDTO.setUserGroup(userGroup.getName());

        when(moduleRepository.existsByName(moduleDTO.getModuleName())).thenReturn(false);
        when(userGroupRepository.findByName(moduleDTO.getUserGroup().toString())).thenReturn(userGroup);
        when(moduleRepository.save(any(Module.class))).thenReturn(new Module());

        Module savedModule = new Module();
        savedModule.setId(1); // Ensure the saved module has a non-null ID
        when(moduleRepository.save(any(Module.class))).thenReturn(savedModule);

        boolean result = moduleService.saveModule(moduleDTO);

        //assertTrue(result);
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
        ModuleDTO moduleDTO = new ModuleDTO();
        moduleDTO.setId(1);
        moduleDTO.setModuleName("UpdatedModule");
        moduleDTO.setExecutionTime(10);
        moduleDTO.setTestGroup(TestGroup.E2E.getName());
        moduleDTO.setModuleCategory(Category.RDKV.getName());

        Module existingModule = new Module();
        existingModule.setId(1);
        existingModule.setName("OldModule");

        when(moduleRepository.findById(moduleDTO.getId())).thenReturn(Optional.of(existingModule));
        when(moduleRepository.save(any(Module.class))).thenReturn(existingModule);

        boolean result = moduleService.updateModule(moduleDTO);

        assertTrue(result);
        verify(moduleRepository).save(any(Module.class));
    }

    @Test
    void testUpdateModule_NotFound() {
        ModuleDTO moduleDTO = new ModuleDTO();
        moduleDTO.setId(1);

        when(moduleRepository.findById(moduleDTO.getId())).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> moduleService.updateModule(moduleDTO));
    }

    @Test
    void testUpdateModule_NameAlreadyExists() {
        ModuleDTO moduleDTO = new ModuleDTO();
        moduleDTO.setId(1);
        moduleDTO.setModuleName("UpdatedModule");

        Module existingModule = new Module();
        existingModule.setId(1);
        existingModule.setName("OldModule");

        when(moduleRepository.findById(moduleDTO.getId())).thenReturn(Optional.of(existingModule));
        when(moduleRepository.existsByName(moduleDTO.getModuleName())).thenReturn(true);

        assertThrows(ResourceAlreadyExistsException.class, () -> moduleService.updateModule(moduleDTO));
    }

    @Test
    void testFindAllModules_Success() {
        List<Module> modules = Arrays.asList(new Module(), new Module());

        when(moduleRepository.findAll()).thenReturn(modules);

        List<ModuleDTO> result = moduleService.findAllModules();

        assertFalse(result.isEmpty());
        assertEquals(modules.size(), result.size());
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
        Integer id = 5;
        Module module = new Module();
        module.setId(id);
        module.setTestGroup(TestGroup.E2E);
        module.setCategory(Category.RDKV);
        module.setUserGroup(new UserGroup());
        when(moduleRepository.findById(id)).thenReturn(Optional.of(module));

        // Act
      //  ModuleDTO result = moduleService.findModuleById(id);
    }

    @Test
    void testFindModuleById_NotFound() {
        when(moduleRepository.findById(1)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> moduleService.findModuleById(1));
    }

    @Test
    void testFindAllByCategory_Success() {
        List<Module> modules = Arrays.asList(new Module(), new Module());

        when(moduleRepository.findAllByCategory(Category.RDKV)).thenReturn(modules);

        List<ModuleDTO> result = moduleService.findAllByCategory("RDKV");

        assertFalse(result.isEmpty());
        assertEquals(modules.size(), result.size());
    }

    @Test
    void testFindAllByCategory_Empty() {
        when(moduleRepository.findAllByCategory(Category.RDKV)).thenReturn(Collections.emptyList());

        List<ModuleDTO> result = moduleService.findAllByCategory("RDKV");

        assertTrue(result.isEmpty());
    }

    @Test
    void testDeleteModule_Success() {
        Module module = new Module();
        module.setId(1);

        when(moduleRepository.findById(1)).thenReturn(Optional.of(module));
        when(functionRepository.findAllByModuleId(1)).thenReturn(Collections.emptyList());

        boolean result = moduleService.deleteModule(1);

        assertTrue(result);
        verify(moduleRepository).deleteById(1);
    }

    @Test
    void testDeleteModule_NotFound() {
        when(moduleRepository.findById(1)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> moduleService.deleteModule(1));
    }

    @Test
    void testDeleteModule_WithFunctionsAndParameters() {
        Module module = new Module();
        module.setId(1);

        Function function = new Function();
        function.setId(1);

        Parameter parameter = new Parameter();
        parameter.setId(1);

        when(moduleRepository.findById(1)).thenReturn(Optional.of(module));
        when(functionRepository.findAllByModuleId(1)).thenReturn(Arrays.asList(function));
        when(parameterRepository.findAllByFunctionId(1)).thenReturn(Arrays.asList(parameter));

        boolean result = moduleService.deleteModule(1);

        assertTrue(result);
        verify(parameterRepository).deleteById(1);
        verify(functionRepository).deleteById(1);
        verify(moduleRepository).deleteById(1);
    }
}