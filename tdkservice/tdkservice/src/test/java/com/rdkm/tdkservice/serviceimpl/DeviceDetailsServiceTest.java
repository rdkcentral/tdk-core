///*
//* If not stated otherwise in this file or this component's Licenses.txt file the
//* following copyright and licenses apply:
//*
//* Copyright 2024 RDK Management
//*
//* Licensed under the Apache License, Version 2.0 (the "License");
//* you may not use this file except in compliance with the License.
//* You may obtain a copy of the License at
//*
//*
//http://www.apache.org/licenses/LICENSE-2.0
//*
//* Unless required by applicable law or agreed to in writing, software
//* distributed under the License is distributed on an "AS IS" BASIS,
//* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//* See the License for the specific language governing permissions and
//* limitations under the License.
//*/
//package com.rdkm.tdkservice.serviceimpl;
//
//import static com.rdkm.tdkservice.enums.Category.RDKV;
//import static com.rdkm.tdkservice.enums.Category.getCategory;
//import static org.junit.jupiter.api.Assertions.assertEquals;
//import static org.junit.jupiter.api.Assertions.assertFalse;
//import static org.junit.jupiter.api.Assertions.assertNotNull;
//import static org.junit.jupiter.api.Assertions.assertThrows;
//import static org.junit.jupiter.api.Assertions.assertTrue;
//import static org.mockito.ArgumentMatchers.any;
//import static org.mockito.ArgumentMatchers.anyString;
//import static org.mockito.Mockito.doAnswer;
//import static org.mockito.Mockito.doThrow;
//import static org.mockito.Mockito.mock;
//import static org.mockito.Mockito.times;
//import static org.mockito.Mockito.verify;
//import static org.mockito.Mockito.when;
//
//import java.io.StringWriter;
//import java.nio.charset.StandardCharsets;
//import java.util.ArrayList;
//import java.util.Arrays;
//import java.util.Collections;
//import java.util.List;
//import java.util.Optional;
//import java.util.UUID;
//
//import javax.xml.transform.Transformer;
//import javax.xml.transform.dom.DOMSource;
//import javax.xml.transform.stream.StreamResult;
//
//import org.junit.jupiter.api.BeforeEach;
//import org.junit.jupiter.api.Test;
//import org.mockito.InjectMocks;
//import org.mockito.Mock;
//import org.mockito.MockitoAnnotations;
//import org.springframework.dao.DataIntegrityViolationException;
//import org.springframework.mock.web.MockMultipartFile;
//import org.springframework.web.multipart.MultipartFile;
//import org.w3c.dom.Document;
//
//import com.rdkm.tdkservice.dto.DeviceCreateDTO;
//import com.rdkm.tdkservice.dto.DeviceResponseDTO;
//import com.rdkm.tdkservice.dto.DeviceUpdateDTO;
//import com.rdkm.tdkservice.enums.Category;
//import com.rdkm.tdkservice.enums.DeviceTypeCategory;
//import com.rdkm.tdkservice.exception.DeleteFailedException;
//import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
//import com.rdkm.tdkservice.exception.ResourceNotFoundException;
//import com.rdkm.tdkservice.model.Device;
//import com.rdkm.tdkservice.model.DeviceType;
//import com.rdkm.tdkservice.model.Oem;
//import com.rdkm.tdkservice.model.Soc;
//import com.rdkm.tdkservice.model.UserGroup;
//import com.rdkm.tdkservice.repository.DeviceRepositroy;
//import com.rdkm.tdkservice.repository.DeviceTypeRepository;
//import com.rdkm.tdkservice.repository.OemRepository;
//import com.rdkm.tdkservice.repository.SocRepository;
//import com.rdkm.tdkservice.repository.UserGroupRepository;
//
////@SpringBootTest
//public class DeviceDetailsServiceTest {
//
//	@Mock
//	private DeviceRepositroy deviceRepository;
//
//	@InjectMocks
//	private DeviceService deviceService;
//
//	@Mock
//	private DeviceTypeRepository deviceTypeRepository;
//
//	@Mock
//	private OemRepository oemRepository;
//
//	@Mock
//	private SocRepository socRepository;
//
//	@Mock
//	private UserGroupRepository userGroupRepository;
//
//	DeviceCreateDTO deviceCreateDTO = new DeviceCreateDTO();
//	DeviceType deviceType = new DeviceType();
//	Oem oem = new Oem();
//	Soc soc = new Soc();
//	UserGroup userGroup = new UserGroup();
//
//	@BeforeEach
//	void setUp() {
//		deviceCreateDTO.setDeviceName("TestDevice");
//		deviceCreateDTO.setDeviceIp("192.168.1.1");
//		deviceCreateDTO.setMacId("00:11:22:33:44:55");
//		deviceCreateDTO.setDeviceTypeName("test");
//		deviceCreateDTO.setOemName("test");
//		deviceCreateDTO.setSocName("test");
//		deviceCreateDTO.setCategory(RDKV.getName().toString());
//		deviceCreateDTO.setThunderEnabled(false);
//		deviceCreateDTO.setThunderPort("8080");
//		deviceCreateDTO.setUserGroupName("Comcast");
//
//		deviceType.setName(deviceCreateDTO.getDeviceTypeName());
//		deviceType.setType(DeviceTypeCategory.CLIENT);
//		deviceType.setCategory(Category.valueOf(RDKV.getName().toString()));
//
//		oem.setName(deviceCreateDTO.getOemName());
//		oem.setCategory(Category.valueOf(RDKV.getName().toString()));
//
//		soc.setName(deviceCreateDTO.getSocName());
//		userGroup.setName(deviceCreateDTO.getUserGroupName());
//		oem.setUserGroup(userGroup);
//		soc.setCategory(Category.valueOf(RDKV.getName().toString()));
//
//		MockitoAnnotations.openMocks(this);
//	}
//
//	@Test
//	void createDevice_Success() {
//		when(deviceTypeRepository.findByName(deviceCreateDTO.getDeviceTypeName())).thenReturn(deviceType);
//		when(oemRepository.findByName(deviceCreateDTO.getOemName())).thenReturn(oem);
//		when(socRepository.findByName(deviceCreateDTO.getSocName())).thenReturn(soc);
//		when(userGroupRepository.findByName(deviceCreateDTO.getUserGroupName())).thenReturn(userGroup);
//
//		Device device = new Device();
//		device.setName(deviceCreateDTO.getDeviceName());
//		device.setIp(deviceCreateDTO.getDeviceIp());
//		device.setMacId(deviceCreateDTO.getMacId());
//		device.setDeviceType(deviceType);
//		device.setOem(oem);
//		device.setSoc(soc);
//		device.setCategory(Category.valueOf(RDKV.getName().toString()));
//		device.setThunderEnabled(false);
//		device.setThunderPort("8080");
//
//		when(deviceRepository.save(any(Device.class))).thenReturn(device);
//
//		boolean result = deviceService.createDevice(deviceCreateDTO);
//
//		assertTrue(result);
//		verify(deviceRepository).save(any(Device.class));
//	}
//
//	@Test
//	void testCreateDeviceWithExistingSTBIP() {
//		when(deviceRepository.existsByIp(anyString())).thenReturn(true);
//		deviceCreateDTO.setDeviceIp("1:12:12:12:12");
//		assertThrows(ResourceAlreadyExistsException.class, () -> deviceService.createDevice(deviceCreateDTO));
//	}
//
//	@Test
//	void testCreateDeviceWithExistingSTBName() {
//		when(deviceRepository.existsByName(anyString())).thenReturn(true);
//		deviceCreateDTO.setDeviceName("TestDevice");
//		assertThrows(ResourceAlreadyExistsException.class, () -> deviceService.createDevice(deviceCreateDTO));
//	}
//
//	@Test
//	void testCreateDeviceWithExistingMACID() {
//		when(deviceRepository.existsByMacId(anyString())).thenReturn(true);
//		deviceCreateDTO.setMacId("00:11:22:33:44:55");
//		assertThrows(ResourceAlreadyExistsException.class, () -> deviceService.createDevice(deviceCreateDTO));
//	}
//
//	@Test
//	void testCreateDeviceWithInvalidDeviceType() {
//		when(deviceTypeRepository.findByName(anyString())).thenReturn(null);
//		deviceCreateDTO.setDeviceTypeName("test");
//		assertThrows(ResourceNotFoundException.class, () -> deviceService.createDevice(deviceCreateDTO));
//	}
//
//	@Test
//	void testCreateDeviceWithInvalidOem() {
//		when(oemRepository.findByName(anyString())).thenReturn(null);
//		deviceCreateDTO.setOemName("test");
//		assertThrows(ResourceNotFoundException.class, () -> deviceService.createDevice(deviceCreateDTO));
//	}
//
//	@Test
//	void testCreateDeviceWithInvalidSoc() {
//		when(socRepository.findByName(anyString())).thenReturn(null);
//		deviceCreateDTO.setSocName("test");
//		assertThrows(ResourceNotFoundException.class, () -> deviceService.createDevice(deviceCreateDTO));
//	}
//
//	@Test
//	void testCreateDeviceWithInvalidCategory() {
//		deviceCreateDTO.setCategory("RDKR");
//		assertThrows(ResourceNotFoundException.class, () -> deviceService.createDevice(deviceCreateDTO));
//	}
//
//	@Test
//	void updateDeviceTest() {
//		UUID deviceId = UUID.randomUUID();
//		DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
//		deviceUpdateDTO.setId(deviceId);
//		deviceUpdateDTO.setDeviceName("UpdatedTestDevice");
//		deviceUpdateDTO.setDeviceIp("192.168.1.2");
//		deviceUpdateDTO.setMacId("72:45:4C:7B:AF:A7");
//		deviceUpdateDTO.setDeviceTypeName("device_client");
//		deviceUpdateDTO.setOemName("rdkv_oem");
//		deviceUpdateDTO.setSocName("rdkv_soc");
//		deviceUpdateDTO.setCategory(Category.RDKV.getName());
//		deviceUpdateDTO.setThunderEnabled(true);
//		deviceUpdateDTO.setThunderPort("9090");
//		deviceUpdateDTO.setUserGroupName("UpdatedComcast");
//
//		Device existingDevice = new Device();
//		existingDevice.setId(deviceId);
//		existingDevice.setName("TestDevice");
//
//		when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(existingDevice));
//		when(deviceTypeRepository.findByName("device_client")).thenReturn(deviceType);
//		when(oemRepository.findByName("rdkv_oem")).thenReturn(oem);
//		when(socRepository.findByName("rdkv_soc")).thenReturn(soc);
//		when(userGroupRepository.findByName("comcast")).thenReturn(userGroup);
//		when(deviceRepository.save(any(Device.class))).thenAnswer(i -> i.getArguments()[0]);
//
//		boolean updatedDeviceDTO = deviceService.updateDevice(deviceUpdateDTO);
//
//		assertTrue(updatedDeviceDTO);
//
//		verify(deviceRepository).save(any(Device.class));
//	}
//
//	@Test
//	void getAllDeviceDetailsByCategory_whenCategoryExists_returnsNonEmptyList() {
//		String category = "RDKV";
//		List<Device> mockDevices = Arrays.asList(new Device(), new Device());
//		when(deviceRepository.findByCategory(Category.RDKV)).thenReturn(mockDevices);
//
//		List<DeviceResponseDTO> result = deviceService.getAllDeviceDetailsByCategory(category);
//
//		assertFalse(result.isEmpty());
//		assertEquals(mockDevices.size(), result.size());
//	}
//
//	@Test
//	void getAllDeviceDetailsByCategory_whenCategoryDoesNotExist_returnsEmptyList() {
//		String category = "NON_EXISTENT";
//		when(deviceRepository.findByCategory(getCategory(category))).thenReturn(Collections.emptyList());
//
//		List<DeviceResponseDTO> result = deviceService.getAllDeviceDetailsByCategory(category);
//
//		assertTrue(result.isEmpty());
//	}
//
//	@Test
//	void parseXMLForDevice_withValidFile_createsDevices() throws Exception {
//		String xmlContent = "<device>" + "<device_name>TestDevice</device_name>" + "<device_ip>192.168.1.1</device_ip>"
//				+ "<mac_addr>00:11:22:33:44:55</mac_addr>" + "<category>RDKV</category>"
//				+ "<device_type>device_gateway</device_type>" + "<oem>rdkv_oem</oem>" + "<soc>rdkv_soc</soc>"
//				+ "</device>";
//		MultipartFile file = new MockMultipartFile("devices.xml", "devices.xml", "text/xml",
//				xmlContent.getBytes(StandardCharsets.UTF_8));
//		System.out.println("DDD" + file.getOriginalFilename());
//		DeviceType mockDeviceType = new DeviceType();
//		mockDeviceType.setName("device_gateway");
//		mockDeviceType.setType(DeviceTypeCategory.CLIENT);
//
//		Oem oem = new Oem();
//		oem.setName("rdkv_oem");
//
//		Soc soc = new Soc();
//		soc.setName("rdkv_soc");
//
//		UserGroup userGroup = new UserGroup();
//		userGroup.setName("comcast");
//
//		Category category = Category.RDKV;
//		Device device = new Device();
//		device.setCategory(category);
//
//		when(deviceTypeRepository.findByName("device_gateway")).thenReturn(mockDeviceType);
//		when(oemRepository.findByName("rdkv_oem")).thenReturn(oem);
//		when(socRepository.findByName("rdkv_soc")).thenReturn(soc);
//		when(userGroupRepository.findByName("comcast")).thenReturn(userGroup);
//		when(deviceRepository.save(any(Device.class))).thenAnswer(invocation -> invocation.getArgument(0));
//
//		boolean xmlUpload = deviceService.parseXMLForDevice(file);
//		assertTrue(xmlUpload);
//
//	}
//
//	@Test
//	void downloadDeviceXML_withValidStbName_returnsDeviceDetailsInXMLFormat() {
//		String stbName = "ValidDevice";
//		Device mockDevice = new Device();
//		mockDevice.setName(stbName);
//		mockDevice.setCategory(Category.RDKV);
//
//		DeviceType mockDeviceType = new DeviceType();
//		mockDeviceType.setName("device_gateway");
//		mockDevice.setDeviceType(mockDeviceType);
//
//		Soc mockSoc = new Soc();
//		mockSoc.setName("rdkv_soc");
//		mockDevice.setSoc(mockSoc);
//
//		Oem mockOem = new Oem();
//		mockOem.setName("rdkv_oem");
//		mockDevice.setOem(mockOem);
//
//		when(deviceRepository.findByName(stbName)).thenReturn(mockDevice);
//
//		String result = deviceService.downloadDeviceXML(stbName);
//
//		assertNotNull(result);
//		assertTrue(result.contains(stbName));
//		assertTrue(result.contains("device_gateway"));
//		assertTrue(result.contains("rdkv_soc"));
//		assertTrue(result.contains("rdkv_oem"));
//	}
//
//	@Test
//	void downloadDeviceXML_withNonExistentStbName_throwsRuntimeException() {
//		String stbName = "NonExistentDevice";
//		when(deviceRepository.findByName(stbName)).thenReturn(null);
//
//		assertThrows(RuntimeException.class, () -> deviceService.downloadDeviceXML(stbName));
//	}
//
//	@Test
//	public void testGetAllDeviceDetailsByCategory() {
//		String category = "RDKV";
//		List<Device> mockDevices = new ArrayList<>();
//		mockDevices.add(new Device());
//		when(deviceRepository.findByCategory(getCategory(category))).thenReturn(mockDevices);
//
//		List<DeviceResponseDTO> result = deviceService.getAllDeviceDetailsByCategory(category);
//
//		assertEquals(1, result.size());
//	}
//
//	@Test
//	void updateDevice_whenDeviceNotFound_throwsResourceNotFoundException() {
//		UUID deviceId = UUID.randomUUID();
//		DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
//		deviceUpdateDTO.setId(deviceId);
//
//		when(deviceRepository.findById(deviceId)).thenReturn(Optional.empty());
//
//		assertThrows(ResourceNotFoundException.class, () -> deviceService.updateDevice(deviceUpdateDTO));
//	}
//
//	@Test
//	void updateDevice_whenValidRequest_updatesDevice() {
//
//		UUID deviceId = UUID.randomUUID();
//
//		DeviceUpdateDTO deviceUpdateDTO = new DeviceUpdateDTO();
//		deviceUpdateDTO.setId(deviceId);
//
//		Device device = new Device();
//		DeviceType deviceType1 = new DeviceType();
//		deviceType1.setType(DeviceTypeCategory.CLIENT);
//		device.setDeviceType(deviceType1);
//		device.setCategory(Category.RDKV);
//		device.setThunderEnabled(true);
//
//		when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(device));
//		when(deviceRepository.save(device)).thenReturn(device);
//
//		boolean deviceUpdate = deviceService.updateDevice(deviceUpdateDTO);
//		assertTrue(deviceUpdate);
//	}
//
//	@Test
//	void deleteDeviceById_whenDataIntegrityViolationExceptionThrown_throwsDeleteFailedException() {
//		UUID deviceId = UUID.randomUUID();
//		Device device = new Device();
//
//		when(deviceRepository.findById(deviceId)).thenReturn(Optional.of(device));
//		doThrow(DataIntegrityViolationException.class).when(deviceRepository).deleteById(deviceId);
//
//		assertThrows(DeleteFailedException.class, () -> deviceService.deleteDeviceById(deviceId));
//		verify(deviceRepository, times(1)).deleteById(deviceId);
//	}
//
//	@Test
//	void generateXMLForDevice_returnsCorrectXMLString() throws Exception {
//		Device device = new Device();
//		device.setCategory(Category.RDKV);
//		DeviceType deviceType = new DeviceType();
//		deviceType.setName("TestDeviceType");
//		device.setDeviceType(deviceType);
//		Oem oem = new Oem();
//		oem.setName("TestOem");
//		device.setOem(oem);
//		Soc soc = new Soc();
//		soc.setName("TestSoc");
//		device.setSoc(soc);
//
//		Document mockDocument = mock(Document.class);
//		Transformer transformer = mock(Transformer.class);
//		StringWriter writer = new StringWriter();
//		doAnswer(invocation -> {
//			transformer.transform(new DOMSource(mockDocument), new StreamResult(writer));
//			return null;
//		}).when(transformer).transform(any(DOMSource.class), any(StreamResult.class));
//
//		String result = deviceService.generateXMLForDevice(device);
//
//		assertNotNull(result);
//		assertTrue(result.contains("<?xml"));
//	}
//}