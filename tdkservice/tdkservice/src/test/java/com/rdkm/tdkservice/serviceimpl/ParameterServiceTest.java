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

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import com.rdkm.tdkservice.dto.ParameterCreateDTO;
import com.rdkm.tdkservice.dto.ParameterDTO;
import com.rdkm.tdkservice.enums.ParameterDataType;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.Function;
import com.rdkm.tdkservice.model.Parameter;
import com.rdkm.tdkservice.repository.FunctionRepository;
import com.rdkm.tdkservice.repository.ParameterRepository;
import com.rdkm.tdkservice.serviceimpl.ParameterService;
import com.rdkm.tdkservice.util.Constants;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

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
        ParameterCreateDTO parameterCreateDTO = new ParameterCreateDTO();
        parameterCreateDTO.setParameterName("NewParameter");
        parameterCreateDTO.setFunction("TestFunction");
        parameterCreateDTO.setParameterDataType(ParameterDataType.STRING);
        parameterCreateDTO.setParameterRangeVal("0-100");

        Function function = new Function();
        function.setName("TestFunction");

        Parameter savedParameter = new Parameter();
        savedParameter.setId(1);

        when(parameterRepository.existsByName(parameterCreateDTO.getParameterName())).thenReturn(false);
        when(functionRepository.findByName(parameterCreateDTO.getFunction())).thenReturn(function);
        when(parameterRepository.save(any(Parameter.class))).thenReturn(savedParameter);

        boolean result = parameterService.createParameter(parameterCreateDTO);
    }

    @Test
    void testCreateParameter_AlreadyExists() {
        ParameterCreateDTO parameterCreateDTO = new ParameterCreateDTO();
        parameterCreateDTO.setParameterName("ExistingParameter");


        when(parameterRepository.existsByName(parameterCreateDTO.getParameterName())).thenReturn(true);

        assertThrows(ResourceAlreadyExistsException.class, () -> parameterService.createParameter(parameterCreateDTO));
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
        ParameterDTO parameterDTO = new ParameterDTO();
        parameterDTO.setId(1);
        parameterDTO.setParameterName("UpdatedParameter");

        Parameter parameter = new Parameter();
        parameter.setId(1);
        parameter.setName("OldParameter");

        when(parameterRepository.findById(parameterDTO.getId())).thenReturn(Optional.of(parameter));
        when(parameterRepository.existsByName(parameterDTO.getParameterName())).thenReturn(false);

        boolean result = parameterService.updateParameter(parameterDTO);

        assertTrue(result);
        verify(parameterRepository).save(parameter);
    }

    @Test
    void testUpdateParameter_NotFound() {
        ParameterDTO parameterDTO = new ParameterDTO();
        parameterDTO.setId(1);

        when(parameterRepository.findById(parameterDTO.getId())).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> parameterService.updateParameter(parameterDTO));
    }

    @Test
    void testUpdateParameter_NameAlreadyExists() {
        ParameterDTO parameterDTO = new ParameterDTO();
        parameterDTO.setId(1);
        parameterDTO.setParameterName("ExistingParameter");

        Parameter parameter = new Parameter();
        parameter.setId(1);
        parameter.setName("OldParameter");

        when(parameterRepository.findById(parameterDTO.getId())).thenReturn(Optional.of(parameter));
        when(parameterRepository.existsByName(parameterDTO.getParameterName())).thenReturn(true);

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
        Integer id = 1;
        Parameter parameter = new Parameter();
        parameter.setId(id);

        when(parameterRepository.findById(id)).thenReturn(Optional.of(parameter));

        ParameterDTO result = parameterService.findParameterById(id);

        assertNotNull(result);
        assertEquals(id, result.getId());
    }

    @Test
    void testFindParameterById_NotFound() {
        Integer id = 1;

        when(parameterRepository.findById(id)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> parameterService.findParameterById(id));
    }

    @Test
    void testDeleteParameter_Success() {
        Integer id = 1;

        doNothing().when(parameterRepository).deleteById(id);

        boolean result = parameterService.deleteParameter(id);

        assertTrue(result);
        verify(parameterRepository).deleteById(id);
    }

    @Test
    void testDeleteParameter_Failure() {
        Integer id = 1;

        doThrow(new RuntimeException()).when(parameterRepository).deleteById(id);

        boolean result = parameterService.deleteParameter(id);

        assertFalse(result);
    }

    @Test
    void testFindAllParametersByFunction_Success() {
        String functionName = "TestFunction";
        Function function = new Function();
        function.setId(1);
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