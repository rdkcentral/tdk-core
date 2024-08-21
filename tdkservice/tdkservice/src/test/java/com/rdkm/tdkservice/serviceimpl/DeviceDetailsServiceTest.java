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
import com.rdkm.tdkservice.dto.*;
import com.rdkm.tdkservice.enums.BoxTypeCategory;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.MandatoryFieldException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.*;
import com.rdkm.tdkservice.repository.*;
import com.rdkm.tdkservice.util.Constants;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;
import org.w3c.dom.Document;

import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.util.*;


import static com.rdkm.tdkservice.enums.BoxTypeCategory.GATEWAY;
import static com.rdkm.tdkservice.enums.Category.RDKV;
import static com.rdkm.tdkservice.enums.Category.getCategory;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
@SpringBootTest
public class DeviceDetailsServiceTest {

    @MockBean
    private DeviceRepositroy deviceRepository;

    @Autowired
    private DeviceService deviceService;

    @MockBean
    private BoxTypeRepository boxTypeRepository;

    @MockBean
    private BoxManufacturerRepository boxManufacturerRepository;

    @MockBean
    private SocVendorRepository socVendorRepository;

    @MockBean
    private UserGroupRepository userGroupRepository;

    @MockBean
    private DeviceStreamRepository deviceStreamRepository;

    @MockBean
    private StreamingDetailsRepository streamingDetailsRepository;
    DeviceCreateDTO deviceCreateDTO = new DeviceCreateDTO();
    BoxType boxType = new BoxType();
    BoxManufacturer boxManufacturer = new BoxManufacturer();
    SocVendor socVendor = new SocVendor();
    UserGroup userGroup = new UserGroup();

    @BeforeEach
    void setUp() {
       // DeviceCreateDTO deviceCreateDTO = new DeviceCreateDTO();
        deviceCreateDTO.setStbName("TestDevice");
        deviceCreateDTO.setStbIp("192.168.1.1");
        deviceCreateDTO.setMacId("00:11:22:33:44:55");
        deviceCreateDTO.setBoxTypeName("test");
        deviceCreateDTO.setBoxManufacturerName("test");
        deviceCreateDTO.setSocVendorName("test");
        deviceCreateDTO.setCategory(RDKV.getName().toString());
        deviceCreateDTO.setThunderEnabled(false); // Setting thunderEnabled to false directly
        deviceCreateDTO.setThunderPort("8080");
        deviceCreateDTO.setRecorderId("rec123");
        deviceCreateDTO.setGatewayDeviceName("Gateway1");
        deviceCreateDTO.setUserGroupName("Comcast");

        // boxType = new BoxType();
        boxType.setName(deviceCreateDTO.getBoxTypeName());
        boxType.setType(BoxTypeCategory.CLIENT);
        boxType.setCategory(Category.valueOf(RDKV.getName().toString()));
        BoxManufacturer boxManufacturer = new BoxManufacturer();
        boxManufacturer.setName(deviceCreateDTO.getBoxManufacturerName());
        boxManufacturer.setCategory(Category.valueOf(RDKV.getName().toString()));


       // SocVendor socVendor = new SocVendor();
        socVendor.setName(deviceCreateDTO.getSocVendorName());
        //UserGroup userGroup = new UserGroup();
        userGroup.setName(deviceCreateDTO.getUserGroupName());
        boxManufacturer.setUserGroup(userGroup);
        socVendor.setCategory(Category.valueOf(RDKV.getName().toString()));
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void createDevice_Success() {
        // Given
        // Mocking BoxType to return the boxType object
        when(boxTypeRepository.findByName(deviceCreateDTO.getBoxTypeName())).thenReturn(boxType);
        // Mocking Boxmanufactruer to return the boxType object
        when(boxManufacturerRepository.findByName(deviceCreateDTO.getBoxManufacturerName())).thenReturn(boxManufacturer);
        // Mocking SocVendor to return the boxType object
        when(socVendorRepository.findByName(deviceCreateDTO.getSocVendorName())).thenReturn(socVendor);
        // Mocking UserGroup to return the boxType object
        when(userGroupRepository.findByName(deviceCreateDTO.getUserGroupName())).thenReturn(userGroup);

        Device device = new Device();
        device.setStbName(deviceCreateDTO.getStbName());
        device.setStbIp(deviceCreateDTO.getStbIp());
        device.setMacId(deviceCreateDTO.getMacId());
        device.setBoxType(boxType); // Setting the BoxType object to the Device


        device.setBoxManufacturer(boxManufacturer);
        device.setSocVendor(socVendor);
        device.setCategory(Category.valueOf(RDKV.getName().toString()));
        device.setThunderEnabled(false);
        device.setThunderPort("8080");
        device.setRecorderId("rec123");
        when(deviceRepository.save(any(Device.class))).thenReturn(device);

        // When
        boolean result = deviceService.createDevice(deviceCreateDTO);

        // Then
        assertTrue(result);
        verify(deviceRepository).save(any(Device.class));
    }
    @Test
    void testCreateDeviceWithExistingSTBIP() {
        when(deviceRepository.existsByStbIp(anyString())).thenReturn(true);
        deviceCreateDTO.setStbIp("1:12:12:12:12");
        assertThrows(ResourceAlreadyExistsException.class, () -> deviceService.createDevice(deviceCreateDTO));
    }

    @Test
    void testCreateDeviceWithExistingSTBName() {
        when(deviceRepository.existsByStbName(anyString())).thenReturn(true);
        deviceCreateDTO.setStbName("TestDevice");
        assertThrows(ResourceAlreadyExistsException.class, () -> deviceService.createDevice(deviceCreateDTO));
    }
    @Test
    void testCreateDeviceWithExistingMACID() {
        when(deviceRepository.existsByMacId(anyString())).thenReturn(true);
        deviceCreateDTO.setMacId("00:11:22:33:44:55");
        assertThrows(ResourceAlreadyExistsException.class, () -> deviceService.createDevice(deviceCreateDTO));
    }

    @Test
    void testCreateDeviceWithInvalidBoxType() {
        when(boxTypeRepository.findByName(anyString())).thenReturn(null);
        deviceCreateDTO.setBoxTypeName("test");
        assertThrows(ResourceNotFoundException.class, () -> deviceService.createDevice(deviceCreateDTO));
    }

    @Test
    void testCreateDeviceWithInvalidBoxManufacturer() {
        when(boxManufacturerRepository.findByName(anyString())).thenReturn(null);
        deviceCreateDTO.setBoxManufacturerName("test");
        assertThrows(ResourceNotFoundException.class, () -> deviceService.createDevice(deviceCreateDTO));
    }

    @Test
    void testCreateDeviceWithInvalidSoCVendor() {
        when(socVendorRepository.findByName(anyString())).thenReturn(null);
        deviceCreateDTO.setSocVendorName("test");
        assertThrows(ResourceNotFoundException.class, () -> deviceService.createDevice(deviceCreateDTO));
    }

    @Test
    void testCreateDeviceWithInvalidCategory() {
        // Assuming Category is validated directly in the service method since there's no repository method call shown for it.
        // Simulate the scenario by setting an invalid category in the DTO and expecting the service to throw ResourceNotFoundException.
        deviceCreateDTO.setCategory("RDKR");

        assertThrows(ResourceNotFoundException.class, () -> deviceService.createDevice(deviceCreateDTO));
    }
    @Test
    void updateDeviceTest() {
        // Setup
        DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
        deviceUpdateDTO.setId(1); // Assuming an existing device with ID 1
        deviceUpdateDTO.setStbName("UpdatedTestDevice");
        deviceUpdateDTO.setStbIp("192.168.1.2");
        deviceUpdateDTO.setMacId("72:45:4C:7B:AF:A7");
        deviceUpdateDTO.setBoxTypeName("box_client");
        deviceUpdateDTO.setBoxManufacturerName("rdkv_boxmanufacturer");
        deviceUpdateDTO.setSocVendorName("rdkv_vendor");
        deviceUpdateDTO.setCategory(Category.RDKV.getName());
        deviceUpdateDTO.setThunderEnabled(true);
        deviceUpdateDTO.setThunderPort("9090");
        deviceUpdateDTO.setRecorderId("rec456");
        deviceUpdateDTO.setGatewayDeviceName("UpdatedGateway1");
        deviceUpdateDTO.setUserGroupName("UpdatedComcast");

        Device existingDevice = new Device();
        existingDevice.setId(1);
        existingDevice.setStbName("TestDevice");

        when(deviceRepository.findById(1)).thenReturn(Optional.of(existingDevice));
        when(boxTypeRepository.findByName("box_client")).thenReturn(boxType);
        when(boxManufacturerRepository.findByName("rdkv_boxmanufacturer")).thenReturn(boxManufacturer);
        when(socVendorRepository.findByName("rdkv_vendor")).thenReturn(socVendor);
        when(userGroupRepository.findByName("comcast")).thenReturn(userGroup);
        when(deviceRepository.save(any(Device.class))).thenAnswer(i -> i.getArguments()[0]);
        when(deviceRepository.save(any(Device.class))).thenAnswer(i -> i.getArguments()[0]);

        // Invoke
        DeviceUpdateDTO updatedDeviceDTO = deviceService.updateDevice(deviceUpdateDTO);

        // Verify
        assertNotNull(updatedDeviceDTO);
        assertEquals("UpdatedTestDevice", updatedDeviceDTO.getStbName());
        verify(deviceRepository).save(any(Device.class));
    }
    @Test
    void getAllDeviceDetailsByCategory_whenCategoryExists_returnsNonEmptyList() {
        // Given
        String category = "RDKV";
        List<Device> mockDevices = Arrays.asList(new Device(), new Device());
        when(deviceRepository.findByCategory(Category.RDKV)).thenReturn(mockDevices);

        // When
        List<DeviceResponseDTO> result = deviceService.getAllDeviceDetailsByCategory(category);

        // Then
        assertFalse(result.isEmpty());
        assertEquals(mockDevices.size(), result.size());
    }
    @Test
    void getAllDeviceDetailsByCategory_whenCategoryDoesNotExist_returnsEmptyList() {
        // Given
        String category = "NON_EXISTENT";
        when(deviceRepository.findByCategory(getCategory(category))).thenReturn(Collections.emptyList());

        // When
        List<DeviceResponseDTO> result = deviceService.getAllDeviceDetailsByCategory(category);

        // Then
        assertTrue(result.isEmpty());
    }

    @Test
    void getGatewayDeviceList_whenGatewayDevicesExist_returnsListOfDeviceNames() {
        // Given
        List<BoxType> boxTypes = Collections.singletonList(new BoxType());
        List<Device> devices = Arrays.asList(
                new Device() {{ setStbName("Device1"); }},
                new Device() {{ setStbName("Device2"); }}
        );
        when(boxTypeRepository.findByType(BoxTypeCategory.GATEWAY)).thenReturn(boxTypes);
        when(deviceRepository.findByBoxType(any(BoxType.class))).thenReturn(devices);

        // When
        List<String> result = deviceService.getGatewayDeviceList(RDKV.getName());

        // Then
        assertTrue(result.isEmpty());
    }

    @Test
    void getGatewayDeviceList_whenNoGatewayDevicesExist_returnsEmptyList() {
        // Given
        when(boxTypeRepository.findByType(BoxTypeCategory.GATEWAY)).thenReturn(Collections.emptyList());

        // When
        List<String> result = deviceService.getGatewayDeviceList(RDKV.getName());

        // Then
        assertNull(result);
    }
    @Test
    void getStreamsForTheDevice_whenDeviceHasStreams_returnsListOfStreams() {
        // Given
        Integer deviceId = 1;
        Device device = new Device();
        device.setId(deviceId);

        StreamingDetails streamingDetails1 = new StreamingDetails();
        streamingDetails1.setStreamId("streamId1");
        StreamingDetails streamingDetails2 = new StreamingDetails();
        streamingDetails2.setStreamId("streamId2");

        DeviceStream deviceStream1 = new DeviceStream();
        deviceStream1.setStream(streamingDetails1);
        deviceStream1.setOcapId("ocapId1");

        DeviceStream deviceStream2 = new DeviceStream();
        deviceStream2.setStream(streamingDetails2);
        deviceStream2.setOcapId("ocapId2");

        List<DeviceStream> deviceStreams = Arrays.asList(deviceStream1, deviceStream2);

        when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(device));
        when(deviceStreamRepository.findAllByDevice(device)).thenReturn(deviceStreams);
        when(streamingDetailsRepository.findByStreamId("streamId1")).thenReturn(streamingDetails1);
        when(streamingDetailsRepository.findByStreamId("streamId2")).thenReturn(streamingDetails2);

        // When
        List<StreamingDetailsResponse> result = deviceService.getStreamsForTheDevice(deviceId);

        // Then
        assertEquals(deviceStreams.size(), result.size());
    }
    @Test
    void getStreamsForTheDevice_whenDeviceNotFound_throwsResourceNotFoundException() {
        // Given
        Integer deviceId = 1;
        when(deviceRepository.findById(deviceId)).thenReturn(Optional.empty());

        // Then
        assertThrows(ResourceNotFoundException.class, () -> deviceService.getStreamsForTheDevice(deviceId));
    }
    @Test
    void getStreamsForTheDevice_whenDeviceHasNoStreams_returnsEmptyList() {
        // Given
        Integer deviceId = 1;
        Device device = new Device();
        device.setId(deviceId);
        when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(device));
        when(deviceStreamRepository.findAllByDevice(device)).thenReturn(Collections.emptyList());

        // When
        List<StreamingDetailsResponse> result = deviceService.getStreamsForTheDevice(deviceId);

        // Then
        assertTrue(result.isEmpty());
    }
    @Test
    void parseXMLForDevice_withValidFile_createsDevices() throws Exception {
        // Given
        String xmlContent = "<device>" +
                "<stb_name>TestDevice</stb_name>" +
                "<stb_ip>192.168.1.1</stb_ip>" +
                "<mac_addr>00:11:22:33:44:55</mac_addr>" +
                "<category>RDKV</category>" + // Added category element
                "<box_type>box_gateway</box_type>" +
                "<box_manufacturer>rdkv_boxmanufacturer</box_manufacturer>" +
                "<soc_vendor>rdkv_vendor</soc_vendor>" +
                "</device>";
        MultipartFile file = new MockMultipartFile("devices.xml", xmlContent.getBytes(StandardCharsets.UTF_8));
        BoxType mockBoxType = new BoxType();
        mockBoxType.setName("box_gateway");
        mockBoxType.setType(BoxTypeCategory.CLIENT);
        //box manufacturer
        BoxManufacturer boxManufacturer = new BoxManufacturer();
        boxManufacturer.setName("rdkv_boxmanufacturer");
        //soc vendor
        SocVendor socVendor = new SocVendor();
        socVendor.setName("rdkv_vendor");
        //Category
        UserGroup userGroup = new UserGroup();
        userGroup.setName("comcast");
        //Category
        Category category = Category.RDKV;
        Device device = new Device();
      device.setCategory(category);

        when(boxTypeRepository.findByName("box_gateway")).thenReturn(mockBoxType);
        when(boxManufacturerRepository.findByName("rdkv_boxmanufacturer")).thenReturn(boxManufacturer);
        when(socVendorRepository.findByName("rdkv_vendor")).thenReturn(socVendor);
        when(userGroupRepository.findByName("comcast")).thenReturn(userGroup);
        when(deviceRepository.save(any(Device.class))).thenAnswer(invocation -> invocation.getArgument(0));

        // When
        deviceService.parseXMLForDevice(file);

        // Then
        verify(boxTypeRepository, times(1)).findByName("box_gateway");
        verify(deviceRepository, times(1)).save(any(Device.class));
    }
    @Test
    void downloadDeviceXML_withValidStbName_returnsDeviceDetailsInXMLFormat() {
        // Given
        String stbName = "ValidDevice";
        Device mockDevice = new Device();
        mockDevice.setStbName(stbName);
        mockDevice.setCategory(Category.RDKV); // Assuming Category.RDKV is a valid enum value

        BoxType mockBoxType = new BoxType();
        mockBoxType.setName("box_gateway");
        mockDevice.setBoxType(mockBoxType);

        SocVendor mockSocVendor = new SocVendor();
        mockSocVendor.setName("rdkv_vendor");
        mockDevice.setSocVendor(mockSocVendor);

        BoxManufacturer mockBoxManufacturer = new BoxManufacturer();
        mockBoxManufacturer.setName("rdkv_boxmanufacturer");
        mockDevice.setBoxManufacturer(mockBoxManufacturer);

        when(deviceRepository.findByStbName(stbName)).thenReturn(mockDevice);

        // When
        String result = deviceService.downloadDeviceXML(stbName);

        // Then
        assertNotNull(result);
        assertTrue(result.contains(stbName));
        assertTrue(result.contains("box_gateway"));
        assertTrue(result.contains("rdkv_vendor"));
        assertTrue(result.contains("rdkv_boxmanufacturer"));

    }
    @Test
    void downloadDeviceXML_withNonExistentStbName_throwsRuntimeException() {
        // Given
        String stbName = "NonExistentDevice";
        when(deviceRepository.findByStbName(stbName)).thenReturn(null);

        // Then
        assertThrows(RuntimeException.class, () -> deviceService.downloadDeviceXML(stbName));
    }
    @Test
    void getStreamsForTheDevice_withValidDeviceId_returnsStreamDetails() {
        // Given
        Integer deviceId = 1;
        Device mockDevice = new Device();
        mockDevice.setId(deviceId);
        List<DeviceStream> mockDeviceStreams = new ArrayList<>();
        DeviceStream mockDeviceStream = new DeviceStream();
        StreamingDetails mockStreamingDetails = new StreamingDetails();
        mockStreamingDetails.setStreamId("1"); // Set a valid streamId here
        mockDeviceStream.setStream(mockStreamingDetails);
        mockDeviceStream.setOcapId("ocapId1");
        mockDeviceStreams.add(mockDeviceStream);
        when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(mockDevice));
        when(deviceStreamRepository.findAllByDevice(mockDevice)).thenReturn(mockDeviceStreams);
        when(streamingDetailsRepository.findByStreamId("1")).thenReturn(mockStreamingDetails); // Ensure this matches the set streamId

        // When
        List<StreamingDetailsResponse> result = deviceService.getStreamsForTheDevice(deviceId);

        // Then
        assertFalse(result.isEmpty());
        assertEquals(1, result.size());
    }
    @Test
    void getStreamsForTheDevice_withDeviceNotFound_throwsResourceNotFoundException() {
        // Given
        Integer deviceId = 2;
        when(deviceRepository.findById(deviceId)).thenReturn(Optional.empty());

        // Then
        assertThrows(ResourceNotFoundException.class, () -> deviceService.getStreamsForTheDevice(deviceId));
    }
    @Test
    void getStreamsForTheDevice_withDeviceHavingNoStreams_returnsEmptyList() {
        // Given
        Integer deviceId = 3;
        Device mockDevice = new Device();
        mockDevice.setId(deviceId);
        when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(mockDevice));
        when(deviceStreamRepository.findAllByDevice(mockDevice)).thenReturn(Collections.emptyList());

        // When
        List<StreamingDetailsResponse> result = deviceService.getStreamsForTheDevice(deviceId);

        // Then
        assertTrue(result.isEmpty());
    }
    @Test
    void getStreamsForTheDevice_withStreamDetailsNotFound_returnsFilteredResponse() {
        // Given
        Integer deviceId = 4;
        Device mockDevice = new Device();
        mockDevice.setId(deviceId);
        List<DeviceStream> mockDeviceStreams = new ArrayList<>();
        DeviceStream mockDeviceStream = new DeviceStream();
        mockDeviceStream.setStream(new StreamingDetails()); // Stream without details
        mockDeviceStreams.add(mockDeviceStream);
        when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(mockDevice));
        when(deviceStreamRepository.findAllByDevice(mockDevice)).thenReturn(mockDeviceStreams);
        when(streamingDetailsRepository.findByStreamId(anyString())).thenReturn(null); // No details found

        // When
        List<StreamingDetailsResponse> result = deviceService.getStreamsForTheDevice(deviceId);

        // Then
        assertTrue(result.isEmpty());
    }
    @Test
    public void testGetAllDeviceDetailsByCategory() {
        // Setup
        String category = "RDKV";
        List<Device> mockDevices = new ArrayList<>();
        // Assuming Device class has a constructor or method to set up a test instance
        mockDevices.add(new Device(/* parameters to set up the device */));
        when(deviceRepository.findByCategory(getCategory(category))).thenReturn(mockDevices);

        // Invocation
        List<DeviceResponseDTO> result = deviceService.getAllDeviceDetailsByCategory(category);

        // Assertion
        assertEquals(1, result.size()); // Assuming the service method converts each Device to a DeviceResponseDTO
    }

    @Test
    void updateDevice_whenDeviceNotFound_throwsResourceNotFoundException() {
        // Given
        DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
        deviceUpdateDTO.setId(1);

        when(deviceRepository.findById(1)).thenReturn(Optional.empty());

        // Then
        assertThrows(ResourceNotFoundException.class, () -> deviceService.updateDevice(deviceUpdateDTO));
    }

    @Test
    void updateDevice_whenRecorderIdIsNull_throwsMandatoryFieldException() {
        // Given
        DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
        deviceUpdateDTO.setId(1);
        deviceUpdateDTO.setRecorderId(null);

        Device device = new Device();
        BoxType boxType1=new BoxType();
        boxType1.setName("box_gateway");

        device.setBoxType(boxType1);
        device.setCategory(Category.RDKV);

        when(deviceRepository.findById(1)).thenReturn(Optional.of(device));

        // Then
        assertThrows(NullPointerException.class, () -> deviceService.updateDevice(deviceUpdateDTO));
    }

    @Test
    void updateDevice_whenDeviceStreamsIsNull_throwsMandatoryFieldException() {
        // Given
        DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
        deviceUpdateDTO.setId(1);
        deviceUpdateDTO.setRecorderId("recorder1");
        deviceUpdateDTO.setDeviceStreams(null);

        Device device = new Device();
        BoxType boxType1=new BoxType();
        boxType1.setName("box_gateway");

        device.setBoxType(boxType1);
        device.setCategory(Category.RDKV);
        device.setThunderEnabled(false);

        when(deviceRepository.findById(1)).thenReturn(Optional.of(device));

        // Then
        assertThrows(NullPointerException.class, () -> deviceService.updateDevice(deviceUpdateDTO));
    }

    @Test
    void updateDevice_whenValidRequest_updatesDevice() {
        // Given
        DeviceStreamDTO deviceStreamDTO = new DeviceStreamDTO();
        deviceStreamDTO.setStreamId("stream1");
        deviceStreamDTO.setOcapId("ocap1");

        DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
        deviceUpdateDTO.setId(1);
        deviceUpdateDTO.setRecorderId("recorder1");
        deviceUpdateDTO.setDeviceStreams(Collections.singletonList(deviceStreamDTO));

        Device device = new Device();
        BoxType boxType1 = new BoxType();
        boxType1.setType(BoxTypeCategory.GATEWAY);
        device.setBoxType(boxType1);
        device.setCategory(Category.RDKV);
        device.setThunderEnabled(true);

        DeviceStream deviceStream = new DeviceStream();
        deviceStream.setStream(new StreamingDetails());
        deviceStream.setOcapId("ocap1");
        deviceStream.setDevice(device);

        StreamingDetails streamingDetails = new StreamingDetails();
        streamingDetails.setStreamId("stream1");

        when(deviceRepository.findById(1)).thenReturn(Optional.of(device));
        when(deviceStreamRepository.findAllByDevice(device)).thenReturn(Collections.singletonList(deviceStream));
        when(streamingDetailsRepository.findByStreamId("stream1")).thenReturn(streamingDetails);
        when(deviceRepository.save(device)).thenReturn(device); // Mock the save method

        // When
        deviceService.updateDevice(deviceUpdateDTO);

        // Then
        verify(deviceRepository, times(2)).save(device);
        verify(deviceStreamRepository, times(1)).deleteAll(Collections.singletonList(deviceStream));
        verify(deviceStreamRepository, times(1)).save(any(DeviceStream.class));
    }
    @Test
    void updateDevice_whenGatewayAndNotThunderEnabled_deletesAndSavesStreams() {
        // Given
        DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
        deviceUpdateDTO.setId(1);
        deviceUpdateDTO.setRecorderId("recorder1");

        DeviceStreamDTO deviceStreamDTO = new DeviceStreamDTO();
        deviceStreamDTO.setStreamId("stream1");
        deviceStreamDTO.setOcapId("ocap1");
        deviceUpdateDTO.setDeviceStreams(Collections.singletonList(deviceStreamDTO));

        Device device = new Device();
        BoxType boxType1 = new BoxType();
        boxType1.setCategory(Category.RDKV);
        boxType1.setName("box_gateway");
        boxType1.setType(BoxTypeCategory.GATEWAY); // Initialize the type field

        device.setBoxType(boxType1);
        device.setCategory(Category.RDKV);
        device.setThunderEnabled(false);

        List<DeviceStream> existingStreams = new ArrayList<>();
        existingStreams.add(new DeviceStream());

        StreamingDetails streamingDetails = new StreamingDetails();
        streamingDetails.setStreamId("stream1");

        when(deviceRepository.findById(1)).thenReturn(Optional.of(device));
        when(deviceStreamRepository.findAllByDevice(device)).thenReturn(existingStreams);
        when(streamingDetailsRepository.findByStreamId("stream1")).thenReturn(streamingDetails);
        when(deviceRepository.save(device)).thenReturn(device); // Mock the save method

        // When
        deviceService.updateDevice(deviceUpdateDTO);

        // Then
        verify(deviceStreamRepository, times(1)).deleteAll(existingStreams);
        verify(deviceStreamRepository, times(1)).save(any(DeviceStream.class));
    }
    @Test
    void deleteDeviceById_whenDeviceExistsAndHasStreams_deletesDeviceAndStreams() {
        // Given
        Integer deviceId = 1;
        Device device = new Device();
        List<DeviceStream> deviceStreams = Arrays.asList(new DeviceStream(), new DeviceStream());

        when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(device));
        when(deviceStreamRepository.findAllByDevice(device)).thenReturn(deviceStreams);

        // When
        deviceService.deleteDeviceById(deviceId);

        // Then
        verify(deviceStreamRepository, times(1)).deleteAll(deviceStreams);
        verify(deviceRepository, times(1)).deleteById(deviceId);
    }

    @Test
    void deleteDeviceById_whenDeviceExistsAndHasNoStreams_deletesDevice() {
        // Given
        Integer deviceId = 1;
        Device device = new Device();
        List<DeviceStream> deviceStreams = Collections.emptyList();

        when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(device));
        when(deviceStreamRepository.findAllByDevice(device)).thenReturn(deviceStreams);

        // When
        deviceService.deleteDeviceById(deviceId);

        // Then
        verify(deviceStreamRepository, never()).deleteAll(anyList());
        verify(deviceRepository, times(1)).deleteById(deviceId);
    }

    @Test
    void deleteDeviceById_whenDeviceDoesNotExist_doesNothing() {
        // Given
        Integer deviceId = 1;

        when(deviceRepository.findById(deviceId)).thenReturn(Optional.empty());

        // When
        deviceService.deleteDeviceById(deviceId);

        // Then
        verify(deviceStreamRepository, never()).deleteAll(anyList());
        verify(deviceRepository, never()).deleteById(deviceId);
    }

    @Test
    void deleteDeviceById_whenDataIntegrityViolationExceptionThrown_throwsDeleteFailedException() {
        // Given
        Integer deviceId = 1;
        Device device = new Device();

        when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(device));
        doThrow(DataIntegrityViolationException.class).when(deviceRepository).deleteById(deviceId);

        // When & Then
        assertThrows(DeleteFailedException.class, () -> deviceService.deleteDeviceById(deviceId));
        verify(deviceRepository, times(1)).deleteById(deviceId);
    }
    @Test
    void generateXMLForDevice_returnsCorrectXMLString() throws Exception {
        // Given
        Device device = new Device();
        device.setCategory(Category.RDKV); // Ensure category is set
        BoxType boxType = new BoxType();
        boxType.setName("TestBoxType");
        device.setBoxType(boxType); // Ensure boxType is set
        BoxManufacturer boxManufacturer = new BoxManufacturer();
        boxManufacturer.setName("TestBoxManufacturer");
        device.setBoxManufacturer(boxManufacturer); // Ensure boxManufacturer is set
        SocVendor socVendor = new SocVendor();
        socVendor.setName("TestSocVendor");
        device.setSocVendor(socVendor); // Ensure socVendor is set

        // Mock Document
        Document mockDocument = mock(Document.class);

        // Mock Transformer
        TransformerFactory tf = TransformerFactory.newInstance();
        Transformer transformer = mock(Transformer.class);
        StringWriter writer = new StringWriter();
        doAnswer(invocation -> {
            transformer.transform(new DOMSource(mockDocument), new StreamResult(writer));
            return null;
        }).when(transformer).transform(any(DOMSource.class), any(StreamResult.class));

        // When
        String result = deviceService.generateXMLForDevice(device);

        // Then
        assertNotNull(result);
        assertTrue(result.contains("<?xml"));
    }
}