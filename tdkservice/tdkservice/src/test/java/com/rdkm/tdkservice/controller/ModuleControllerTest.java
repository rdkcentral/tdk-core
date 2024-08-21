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

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import com.rdkm.tdkservice.controller.ModuleController;
import com.rdkm.tdkservice.dto.ModuleCreateDTO;
import com.rdkm.tdkservice.dto.ModuleDTO;
import com.rdkm.tdkservice.service.IModuleService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class ModuleControllerTest {

    @Mock
    private IModuleService moduleService;

    @InjectMocks
    private ModuleController moduleController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testCreateModule_Success() {
        ModuleCreateDTO moduleCreateDTO = new ModuleCreateDTO();
        when(moduleService.saveModule(moduleCreateDTO)).thenReturn(true);

        ResponseEntity<String> response = moduleController.createModule(moduleCreateDTO);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("Module created successfully", response.getBody());
    }

    @Test
    void testCreateModule_Failure() {
        ModuleCreateDTO moduleCreateDTO = new ModuleCreateDTO();
        when(moduleService.saveModule(moduleCreateDTO)).thenReturn(false);

        ResponseEntity<String> response = moduleController.createModule(moduleCreateDTO);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertEquals("Failed to create module", response.getBody());
    }

    @Test
    void testUpdateModule_Success() {
        ModuleDTO moduleDTO = new ModuleDTO();
        when(moduleService.updateModule(moduleDTO)).thenReturn(true);

        ResponseEntity<String> response = moduleController.updateModule(moduleDTO);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertEquals("Module updated successfully", response.getBody());
    }

    @Test
    void testUpdateModule_Failure() {
        ModuleDTO moduleDTO = new ModuleDTO();
        when(moduleService.updateModule(moduleDTO)).thenReturn(false);

        ResponseEntity<String> response = moduleController.updateModule(moduleDTO);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertEquals("Failed to update module", response.getBody());
    }

    @Test
    void testFindAllModules() {
        List<ModuleDTO> modules = Arrays.asList(new ModuleDTO(), new ModuleDTO());
        when(moduleService.findAllModules()).thenReturn(modules);

        ResponseEntity<List<ModuleDTO>> response = moduleController.findAllModules();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(modules, response.getBody());
    }

    @Test
    void testFindModuleById_Success() {
        Integer id = 1;
        ModuleDTO moduleDTO = new ModuleDTO();
        when(moduleService.findModuleById(id)).thenReturn(moduleDTO);

        ResponseEntity<ModuleDTO> response = moduleController.findModuleById(id);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(moduleDTO, response.getBody());
    }

    @Test
    void testFindModuleById_NotFound() {
        Integer id = 1;
        when(moduleService.findModuleById(id)).thenReturn(null);

        ResponseEntity<ModuleDTO> response = moduleController.findModuleById(id);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
    }

    @Test
    void testFindAllByCategory_Success() {
        String category = "RDKV";
        List<ModuleDTO> modules = Arrays.asList(new ModuleDTO(), new ModuleDTO());
        when(moduleService.findAllByCategory(category)).thenReturn(modules);

        ResponseEntity<List<ModuleDTO>> response = moduleController.findAllByCategory(category);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(modules, response.getBody());
    }

    @Test
    void testFindAllByCategory_NotFound() {
        String category = "RDKV";
        when(moduleService.findAllByCategory(category)).thenReturn(Collections.emptyList());

        ResponseEntity<List<ModuleDTO>> response = moduleController.findAllByCategory(category);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
    }

    @Test
    void testDeleteModule_Success() {
        Integer id = 1;
        when(moduleService.deleteModule(id)).thenReturn(true);

        ResponseEntity<String> response = moduleController.deleteModule(id);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertEquals("Module deleted successfully", response.getBody());
    }

    @Test
    void testDeleteModule_NotFound() {
        Integer id = 1;
        when(moduleService.deleteModule(id)).thenReturn(false);

        ResponseEntity<String> response = moduleController.deleteModule(id);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals("Module not found", response.getBody());
    }

    @Test
    void testGetAllTestGroups() {
        List<String> testGroups = Arrays.asList("E2E", "UNIT");
        when(moduleService.findAllTestGroupsFromEnum()).thenReturn(testGroups);

        ResponseEntity<List<String>> response = moduleController.getAllTestGroups();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testGroups, response.getBody());
    }
}
