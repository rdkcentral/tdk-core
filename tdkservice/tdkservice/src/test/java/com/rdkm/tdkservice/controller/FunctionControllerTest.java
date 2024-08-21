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

import com.rdkm.tdkservice.controller.FunctionController;
import com.rdkm.tdkservice.dto.FunctionCreateDTO;
import com.rdkm.tdkservice.dto.FunctionDTO;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.service.IFunctionService;
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

public class FunctionControllerTest {

    @Mock
    private IFunctionService functionService;

    @InjectMocks
    private FunctionController functionController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testCreateFunction_Success() {
        FunctionCreateDTO functionCreateDTO = new FunctionCreateDTO();
        when(functionService.createFunction(functionCreateDTO)).thenReturn(true);

        ResponseEntity<String> response = functionController.createFunction(functionCreateDTO);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertEquals("Function created successfully", response.getBody());
    }

    @Test
    void testCreateFunction_Failure() {
        FunctionCreateDTO functionCreateDTO = new FunctionCreateDTO();
        when(functionService.createFunction(functionCreateDTO)).thenReturn(false);

        ResponseEntity<String> response = functionController.createFunction(functionCreateDTO);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertEquals("Failed to create function", response.getBody());
    }

    @Test
    void testUpdateFunction_Success() {
        FunctionDTO functionDTO = new FunctionDTO();
        when(functionService.updateFunction(functionDTO)).thenReturn(true);

        ResponseEntity<String> response = functionController.updateFunction(functionDTO);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("Function updated successfully", response.getBody());
    }

    @Test
    void testUpdateFunction_Failure() {
        FunctionDTO functionDTO = new FunctionDTO();
        when(functionService.updateFunction(functionDTO)).thenReturn(false);

        ResponseEntity<String> response = functionController.updateFunction(functionDTO);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertEquals("Failed to update function", response.getBody());
    }

    @Test
    void testFindAllFunctions() {
        List<FunctionDTO> functions = Arrays.asList(new FunctionDTO(), new FunctionDTO());
        when(functionService.findAllFunctions()).thenReturn(functions);

        ResponseEntity<List<FunctionDTO>> response = functionController.findAllFunctions();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(functions, response.getBody());
    }

    @Test
    void testFindFunctionById_Success() {
        Integer id = 1;
        FunctionDTO functionDTO = new FunctionDTO();
        when(functionService.findFunctionById(id)).thenReturn(functionDTO);

        ResponseEntity<FunctionDTO> response = functionController.findFunctionById(id);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(functionDTO, response.getBody());
    }

    @Test
    void testFindFunctionById_NotFound() {
        Integer id = 1;


        when(functionService.findFunctionById(id)).thenReturn(null);

        ResponseEntity<FunctionDTO> response = functionController.findFunctionById(id);


        assertNull(response.getBody());
    }

    @Test
    void testDeleteFunction_Success() {
        Integer id = 1;
        doNothing().when(functionService).deleteFunction(id);

        ResponseEntity<String> response = functionController.deleteFunction(id);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("Function deleted successfully", response.getBody());
    }


    @Test
    void testFindAllByCategory() {
        String category = "RDKV";
        List<FunctionDTO> functions = Arrays.asList(new FunctionDTO(), new FunctionDTO());
        when(functionService.findAllByCategory(category)).thenReturn(functions);

        ResponseEntity<List<FunctionDTO>> response = functionController.findAllByCategory(category);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(functions, response.getBody());
    }

    @Test
    void testFindAllByCategory_NotFound() {
        String category = "RDV";
        when(functionService.findAllByCategory(category)).thenReturn(Collections.emptyList());

        ResponseEntity<List<FunctionDTO>> response = functionController.findAllByCategory(category);
        assertTrue(response.getBody().isEmpty());
    }

    @Test
    void testFindAllFunctionsByModule() {
        String moduleName = "TestModule";
        List<FunctionDTO> functions = Arrays.asList(new FunctionDTO(), new FunctionDTO());
        when(functionService.findAllFunctionsByModule(moduleName)).thenReturn(functions);

        ResponseEntity<List<FunctionDTO>> response = functionController.findAllFunctionsByModule(moduleName);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(functions, response.getBody());
    }

    @Test
    void testFindAllFunctionsByModule_NotFound() {
        String moduleName = "TestModule";
        when(functionService.findAllFunctionsByModule(moduleName)).thenReturn(Collections.emptyList());

        ResponseEntity<List<FunctionDTO>> response = functionController.findAllFunctionsByModule(moduleName);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertTrue(response.getBody().isEmpty());
    }
}