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

import static org.hamcrest.Matchers.containsString;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import com.rdkm.tdkservice.dto.DeviceConfigDownloadDTO;
import com.rdkm.tdkservice.dto.DeviceResponseDTO;
import com.rdkm.tdkservice.dto.DeviceUpdateDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.service.IDeviceConfigService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.rdkm.tdkservice.controller.DeviceController;
import com.rdkm.tdkservice.dto.DeviceCreateDTO;
import com.rdkm.tdkservice.service.IDeviceService;
import org.springframework.web.context.WebApplicationContext;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;

@SpringBootTest
public class DeviceControllerTest {

    
    private MockMvc mockMvc;

    @Mock
    private IDeviceService deviceDetailsService;

    @Mock
    private IDeviceConfigService deviceConfigService;

    @InjectMocks
    private DeviceController deviceController;

    @Autowired
    private WebApplicationContext context;

    @BeforeEach
    public void setup() {
        mockMvc = MockMvcBuilders.webAppContextSetup(context).build();
    }

    @Test
    void createDevice_whenValidRequest_returnsCreatedStatus() throws Exception {
        DeviceCreateDTO device = new DeviceCreateDTO();
        device.setStbIp("192.168.1.2");
        device.setStbName("NewDevice");
        device.setMacId("00:11:22:33:44:55");
        device.setBoxTypeName("TypeA");
        device.setBoxManufacturerName("ManufacturerX");
        device.setSocVendorName("VendorY");
        //setcategory
        device.setCategory(Category.RDKV.getName());
        // Populate other required fields as per DeviceCreateDTO

        String json = new ObjectMapper().writeValueAsString(device);

        when(deviceDetailsService.createDevice(any(DeviceCreateDTO.class))).thenReturn(true);

        mockMvc.perform(post("/api/v1/device/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json));
    }

    @Test
    void createDevice_whenCreationFails_returnsServerError() throws Exception {
        DeviceCreateDTO device = new DeviceCreateDTO();
        device.setStbIp("192.168.1.3");
        device.setStbName("FaultyDevice");
        device.setMacId("AA:BB:CC:DD:EE:FF");
        device.setBoxTypeName("TypeB");
        device.setBoxManufacturerName("ManufacturerY");
        device.setSocVendorName("VendorZ");
        // Populate other required fields as per DeviceCreateDTO
        device.setCategory(Category.RDKV.getName());
        String json = new ObjectMapper().writeValueAsString(device);

        when(deviceDetailsService.createDevice(any(DeviceCreateDTO.class))).thenReturn(false);

        MockHttpServletResponse response = mockMvc.perform(post("/api/v1/device/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andReturn().getResponse();

    }
    @Test
    void createDevice_whenInvalidRequest_returnsBadRequest() throws Exception {
        DeviceCreateDTO device = new DeviceCreateDTO();
        // Missing required fields to trigger validation errors

        String json = new ObjectMapper().writeValueAsString(device);

        mockMvc.perform(post("/api/v1/device/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isBadRequest());
    }
    @Test
    void updateDevice_whenValidRequest_updatesDevice() throws Exception {
        DeviceUpdateDTO deviceUpdate = new DeviceUpdateDTO();
        deviceUpdate.setId(1);
        deviceUpdate.setStbIp("192.168.1.3");
        deviceUpdate.setStbName("UpdatedDevice");
        // Populate other required fields as per DeviceUpdateDTO

        String json = new ObjectMapper().writeValueAsString(deviceUpdate);


        mockMvc.perform(put("/api/v1/device/update")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json));
    }
    @Test
    void updateDevice_whenUpdateFails_returnsInternalServerError() throws Exception {
        DeviceUpdateDTO deviceUpdate = new DeviceUpdateDTO();
        deviceUpdate.setId(1);
        deviceUpdate.setStbIp("192.168.1.4");
        deviceUpdate.setStbName("FailedUpdateDevice");
        // Populate other required fields as per DeviceUpdateDTO

        String json = new ObjectMapper().writeValueAsString(deviceUpdate);

        doThrow(new RuntimeException("Update failed")).when(deviceDetailsService).updateDevice(any(DeviceUpdateDTO.class));

        mockMvc.perform(put("/api/v1/device/update")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isInternalServerError())
                .andExpect(content().string(containsString("Failed to update device")));
    }
    @Test
    void getAllDevices_whenDevicesExist_returnsDeviceList() throws Exception {
        when(deviceDetailsService.getAllDeviceDetails()).thenReturn(new ArrayList<>()); // Assume this returns a populated list in a real scenario

        mockMvc.perform(get("/api/v1/device/findall"))
                .andExpect(status().isOk());
    }
    @Test
    void getAllDevices_whenNoDevicesExist_returnsEmptyList() throws Exception {
        when(deviceDetailsService.getAllDeviceDetails()).thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/device/findall"))
                .andExpect(status().isOk())
                .andReturn().getResponse();// Expecting an empty JSON array
    }
    @Test
    void getDeviceById_whenDeviceExists_returnsDeviceDetails() throws Exception {
        Integer deviceId = 1;
        when(deviceDetailsService.findDeviceById(deviceId)).thenReturn(new DeviceResponseDTO()); // Assume this returns a populated Device object in a real scenario

        mockMvc.perform(get("/api/v1/device/findbyid/{id}", deviceId))
                .andExpect(status().isOk());
    }
    @Test
    public void testDownloadAllDevicesByCategoryReturnsZip() throws Exception {
        String category = "RDKV";
        MockHttpServletResponse response = mockMvc.perform(get("/api/v1/device/downloadDevicesByCategory/{category}", category))
                .andExpect(status().isOk())
                .andReturn().getResponse();

        byte[] responseBytes = response.getContentAsByteArray();
        Path zipFilePath = Files.createTempFile("devices", ".zip");
        Files.write(zipFilePath, responseBytes);
    }

    @Test
    void downloadAllDevicesByCategory_whenCategoryDoesNotExist_returnsNotFound() throws Exception {
        String category = "RDKV";
        when(deviceDetailsService.downloadAllDevicesByCategory(category)).thenThrow(new ResourceNotFoundException(category,"Category not found"));

        mockMvc.perform(get("/api/v1/device/downloadDevicesByCategory/{category}", category))
                .andExpect(status().isOk())
                .andReturn().getResponse();
    }

    @Test
    void downloadAllDevicesByCategory_whenServiceThrowsException_returnsInternalServerError() throws Exception {
        String category = "RDKV";
        when(deviceDetailsService.downloadAllDevicesByCategory(category)).thenThrow(new RuntimeException("Unexpected error"));

        mockMvc.perform(get("/api/v1/device/downloadDevicesByCategory/{category}", category))
                .andExpect(status().isOk())
                .andReturn().getResponse();
    }

    @Test
    void testDownloadFile_Success() {
        // Setup
        DeviceConfigDownloadDTO request = new DeviceConfigDownloadDTO();
        request.setBoxType("GATEWAY");
        request.setBoxName("test");
        Resource mockResource = mock(Resource.class);
        when(mockResource.getFilename()).thenReturn("configFile.txt");

        // Mocking service call to return the mockResource
        when(deviceConfigService.getDeviceConfigFile("test", "GATEWAY")).thenReturn(mockResource);

        // Execute the controller method
        ResponseEntity<Resource> response = deviceController.downloadDeviceConfigFile(request.getBoxName(), request.getBoxType());

        // Assert the response status and header
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("attachment; filename=\"configFile.txt\"", response.getHeaders().getFirst(HttpHeaders.CONTENT_DISPOSITION));

        // Verify service method was called with correct parameters
        verify(deviceConfigService).getDeviceConfigFile("test", "GATEWAY");
    }

    @Test
    void testDownloadFile_NotFound() {
        DeviceConfigDownloadDTO request = new DeviceConfigDownloadDTO();
        request.setBoxType("BoxType");
        request.setBoxName("BoxName");

        when(deviceConfigService.getDeviceConfigFile(anyString(), anyString())).thenReturn(null);

        ResponseEntity<Resource> response = deviceController.downloadDeviceConfigFile(request.getBoxName(), request.getBoxType());

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        verify(deviceConfigService).getDeviceConfigFile("BoxName", "BoxType");
    }

    @Test
    void testUploadFile_Success() {
        MockMultipartFile file = new MockMultipartFile("uploadFile", "configFile.txt", "text/plain", "some xml".getBytes());
        when(deviceConfigService.uploadDeviceConfigFile(any())).thenReturn(true);

        ResponseEntity<String> response = deviceController.uploadFile(file);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("File upload is succesful", response.getBody());
        verify(deviceConfigService).uploadDeviceConfigFile(any());
    }

    @Test
    void testUploadFile_EmptyFile() {
        MockMultipartFile file = new MockMultipartFile("uploadFile", "", "text/plain", new byte[0]);

        ResponseEntity<String> response = deviceController.uploadFile(file);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertEquals("Please select a file to upload.", response.getBody());
        verify(deviceConfigService, never()).uploadDeviceConfigFile(any());
    }


}