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

import static com.rdkm.tdkservice.enums.BoxTypeCategory.CLIENT;
import static com.rdkm.tdkservice.enums.BoxTypeCategory.GATEWAY;
import static com.rdkm.tdkservice.enums.BoxTypeCategory.STAND_ALONE_CLIENT;
import static com.rdkm.tdkservice.enums.Category.getCategory;
import static com.rdkm.tdkservice.util.Constants.DEVICE_FILE_EXTENSION_ZIP;
import static com.rdkm.tdkservice.util.Constants.DEVICE_XML_FILE_EXTENSION;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.w3c.dom.Attr;
import org.w3c.dom.Comment;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import com.rdkm.tdkservice.dto.DeviceCreateDTO;
import com.rdkm.tdkservice.dto.DeviceStreamDTO;
import com.rdkm.tdkservice.dto.DeviceUpdateDTO;
import com.rdkm.tdkservice.enums.BoxTypeCategory;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.MandatoryFieldException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.BoxManufacturer;
import com.rdkm.tdkservice.model.BoxType;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.model.DeviceStream;
import com.rdkm.tdkservice.model.SocVendor;
import com.rdkm.tdkservice.model.StreamingDetails;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.BoxManufacturerRepository;
import com.rdkm.tdkservice.repository.BoxTypeRepository;
import com.rdkm.tdkservice.repository.DeviceRepositroy;
import com.rdkm.tdkservice.repository.DeviceStreamRepository;
import com.rdkm.tdkservice.repository.SocVendorRepository;
import com.rdkm.tdkservice.repository.StreamingDetailsRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.dto.DeviceResponseDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsResponse;
import com.rdkm.tdkservice.service.IDeviceService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;

@Service
public class DeviceService implements IDeviceService {

	private static final Logger LOGGER = LoggerFactory.getLogger(DeviceService.class);

	@Autowired
	private DeviceRepositroy deviceRepository;

	@Autowired
	private BoxTypeRepository boxTypeRepository;

	@Autowired
	private BoxManufacturerRepository boxManufacturerRepository;

	@Autowired
	private SocVendorRepository socVendorRepository;

	@Autowired
	private UserGroupRepository userGroupRepository;

	@Autowired
	private DeviceStreamRepository deviceStreamRepository;

	@Autowired
	private StreamingDetailsRepository streamingDetailsRepository;

	/**
	 * This method is used to create a new device. It receives a POST request at the
	 * "/createDevice" endpoint with a DeviceDTO object in the request body. The
	 * DeviceDTO object should contain the necessary information for creating a new
	 * device.
	 *
	 * @param deviceCreateDTO The request object containing the details of the
	 *                        device.
	 * @return A ResponseEntity containing the created device if successful, or an
	 *         error message if unsuccessful.
	 */
	public boolean createDevice(DeviceCreateDTO deviceCreateDTO) {
		LOGGER.info("Going to create Device");

		Device device = MapperUtils.populateDeviceDTO(deviceCreateDTO);
		// call setPropetietsCreateDTO meeethod here
		setDevicePropertiesFromCreateDTO(device, deviceCreateDTO);
		// save device return true if save success otherwise return false
		Device savedDevice = null;

		// Check if the device is a gateway and is not thunder enabled
		if ((device.getBoxType().getType().toString().equalsIgnoreCase(GATEWAY.toString())
				|| device.getBoxType().getType().toString().equalsIgnoreCase(STAND_ALONE_CLIENT.toString()))
				&& device.getCategory() == Category.RDKV) {
			if (device.getRecorderId() == null || device.getRecorderId().isEmpty()) {
				LOGGER.info("RecorderId should not be null or empty");
				throw new MandatoryFieldException(" RecorderId should not be null or empty");
			}
			if (!device.isThunderEnabled() && deviceCreateDTO.getDeviceStreams() != null) {
				LOGGER.info("Device is a gateway and is not thunder enabled");
				// Save the device streams
				if (deviceCreateDTO.getDeviceStreams() != null) {
					LOGGER.info(deviceCreateDTO.getDeviceStreams().toString());
					List<DeviceStreamDTO> deviceStreamDTOList = new ArrayList<>();
					deviceStreamDTOList.addAll(deviceCreateDTO.getDeviceStreams());
					saveDeviceStream(deviceStreamDTOList, device);
				} else {
					LOGGER.info("Device streams are null");
					throw new MandatoryFieldException("Device streams should not be null ");
				}
			}
		}

		// if box type not equal to gateway and not equal to standlone client
		if (!(device.getBoxType().getType().toString().equalsIgnoreCase(GATEWAY.toString()))
				|| !(device.getBoxType().getType().toString().equalsIgnoreCase(STAND_ALONE_CLIENT.toString()))) {
			savedDevice = deviceRepository.save(device);
		}

		// save device return true if save success otherwise return false
		return savedDevice != null;

	}

	/**
	 * This method is used to save the device streams for a device. It receives a
	 * list of stream IDs, a list of OCAP IDs, and a Device object. It then saves
	 * the device streams for the device.
	 *
	 * @param deviceStreamDTOList The list of stream IDs to save.
	 * @param deviceInstance      The list of OCAP IDs to save.
	 * @param deviceInstance      The device for which to save the device streams.
	 */
	private void saveDeviceStream(List<DeviceStreamDTO> deviceStreamDTOList, Device deviceInstance) {
		LOGGER.info("Validating device streams for device: {}", deviceInstance.getId());

		Set<String> uniqueOcapIds = deviceStreamDTOList.stream().map(DeviceStreamDTO::getOcapId)
				.collect(Collectors.toSet());

		for (DeviceStreamDTO deviceStreamDTO : deviceStreamDTOList) {
			String streamId = deviceStreamDTO.getStreamId();
			String ocapId = deviceStreamDTO.getOcapId();
			LOGGER.info("Validating stream with ID: {} and OCAP ID: {}", streamId, ocapId);

			StreamingDetails stream = streamingDetailsRepository.findByStreamId(streamId);

			if (stream == null) {
				LOGGER.error("Stream not found with ID: {}", streamId);
				throw new ResourceNotFoundException("Stream Id", streamId);
			}
			if (ocapId == null || ocapId.isEmpty()) {
				LOGGER.error("OCAP ID is null or empty");
				throw new MandatoryFieldException("ocapId should not be null or empty");
			}
			if (uniqueOcapIds.size() != deviceStreamDTOList.size()) {
				LOGGER.error("OCAP ID values are not unique within the same device");
				throw new ResourceAlreadyExistsException("OcapId values must be unique within the same device",
						"OcapId");
			}
		}

		Device savedDevice = deviceRepository.save(deviceInstance);

		for (DeviceStreamDTO deviceStreamDTO : deviceStreamDTOList) {
			String streamId = deviceStreamDTO.getStreamId();
			String ocapId = deviceStreamDTO.getOcapId();
			StreamingDetails stream = streamingDetailsRepository.findByStreamId(streamId);

			DeviceStream existingDeviceStream = deviceStreamRepository.findByDeviceAndStreamAndOcapId(savedDevice,
					stream, ocapId);
			if (existingDeviceStream == null) {
				LOGGER.info("Creating new device stream for device: {} and stream: {}", savedDevice.getId(), streamId);
				DeviceStream deviceStream = new DeviceStream();
				deviceStream.setDevice(savedDevice);
				deviceStream.setStream(stream);
				deviceStream.setOcapId(ocapId);
				deviceStreamRepository.save(deviceStream);
				LOGGER.info("Device stream created successfully");
			} else {
				LOGGER.info("Updating existing device stream for device: {} and stream: {}", savedDevice.getId(),
						streamId);
				existingDeviceStream.setOcapId(ocapId);
				existingDeviceStream.setStream(stream);
				deviceStreamRepository.save(existingDeviceStream);
				LOGGER.info("Device stream updated successfully");
			}
		}
	}

	/**
	 * This method is used to update an existing device. It receives a POST request
	 * at the "/updateDevice" endpoint with a DeviceUpdateDTO object in the request
	 * body. The DeviceUpdateDTO object should contain the necessary information for
	 * updating an existing device.
	 *
	 * @param deviceUpdateDTO The request object containing the details of the
	 *                        device to be updated.
	 * @return A ResponseEntity containing the updated device if successful, or an
	 *         error message if unsuccessful.
	 */
	@Override
	public DeviceUpdateDTO updateDevice(DeviceUpdateDTO deviceUpdateDTO) {
		LOGGER.info("Going to update Device with id: " + deviceUpdateDTO.getId());
		Device device = deviceRepository.findById(deviceUpdateDTO.getId())
				.orElseThrow(() -> new ResourceNotFoundException("Device Id", deviceUpdateDTO.getId().toString()));

		// call setPropetietsUpdateDTO meeethod here
		MapperUtils.updateDeviceProperties(device, deviceUpdateDTO);
		setDevicePropertiesFromUpdateDTO(device, deviceUpdateDTO);

		// check the boxtype is gateway and category is RDKV and thunder is not enabled
		if ((device.getBoxType().getType().toString().equalsIgnoreCase(GATEWAY.toString())
				|| device.getBoxType().getType().toString().equalsIgnoreCase(STAND_ALONE_CLIENT.toString()))
				&& device.getCategory() == Category.RDKV) {
			if (deviceUpdateDTO.getRecorderId() != null && !deviceUpdateDTO.getRecorderId().isEmpty()) {
				device.setRecorderId(deviceUpdateDTO.getRecorderId());
			} else if (device.getRecorderId() == null || device.getRecorderId().isEmpty()) {
				LOGGER.info("RecorderId should not be null or empty");
				throw new MandatoryFieldException(" RecorderId should not be null or empty");
			}
			if (!device.isThunderEnabled() && deviceUpdateDTO.getDeviceStreams() != null) {
				LOGGER.info("Device is a gateway and is not thunder enabled");
				List<DeviceStream> existingStreams = deviceStreamRepository.findAllByDevice(device);
				if (!existingStreams.isEmpty()) {
					deviceStreamRepository.deleteAll(existingStreams);
				}
				if (deviceUpdateDTO.getDeviceStreams() != null) {
					LOGGER.info(deviceUpdateDTO.getDeviceStreams().toString());
					List<DeviceStreamDTO> deviceStreamDTOList = new ArrayList<>();
					deviceStreamDTOList.addAll(deviceUpdateDTO.getDeviceStreams());
					saveDeviceStream(deviceStreamDTOList, device);
				} else {
					LOGGER.info("Device streams are null");
					throw new MandatoryFieldException("Device streams should not be null ");
				}
			}
		}

		if (!(device.getBoxType().getType().toString().equalsIgnoreCase(GATEWAY.toString()))
				|| !(device.getBoxType().getType().toString().equalsIgnoreCase(STAND_ALONE_CLIENT.toString()))) {
			deviceRepository.save(device);
		}

		return deviceUpdateDTO;
	}

	/**
	 * This method is used to find all devices. It receives a GET request at the
	 * "/findAll" endpoint. It then returns a list of all devices.
	 *
	 * @return A List containing all devices.
	 */
	@Override
	public List<DeviceResponseDTO> getAllDeviceDetails() {
		LOGGER.info("Going to fetch all devices");
		List<Device> devices = null;
		try {
			devices = deviceRepository.findAll();
		} catch (Exception e) {
			LOGGER.error("Error occurred while fetching all devices", e);
		}
		if (devices.isEmpty()) {
			return Collections.emptyList();
		}
		return devices.stream().map(this::convertToDeviceDTO).collect(Collectors.toList());
	}

	/**
	 * This method is used to find a device by its ID. It receives a GET request at
	 * the "/findDeviceById/{id}" endpoint with the ID of the device to be found. It
	 * then returns the device with the given ID.
	 *
	 * @param id The ID of the device to be found.
	 * @return A Device object containing the details of the device with the given
	 *         ID.
	 */
	@Override
	public DeviceResponseDTO findDeviceById(Integer id) {
		LOGGER.info("Executing find Device by id method with id: " + id);
		Device device = deviceRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException("Device Id", id.toString()));
		DeviceResponseDTO deviceDTO = null;
		try {
			deviceDTO = this.convertToDeviceDTO(device);
		} catch (Exception e) {
			LOGGER.error("Error occurred while fetching Device with id: " + id, e);
		}
		return deviceDTO;
	}

	/**
	 * This method is used to delete a device by its ID. It receives a DELETE
	 * request at the "/delete/{id}" endpoint with the ID of the device to be
	 * deleted. It then deletes the device with the given ID.
	 *
	 * @param id The ID of the device to be deleted.
	 * @return A ResponseEntity containing a success message if the device is
	 *         deleted successfully, or an error message if the device is not found.
	 */
	@Override
	public void deleteDeviceById(Integer id) {
		LOGGER.info("Going to delete Device with id: " + id);
		try {
			// First, delete the associated device streams
			Device device = deviceRepository.findById(id).orElse(null);
			if (device != null) {
				List<DeviceStream> deviceStreams = deviceStreamRepository.findAllByDevice(device);
				if (!deviceStreams.isEmpty()) {
					deviceStreamRepository.deleteAll(deviceStreams);
				}
				// Then, delete the device
				deviceRepository.deleteById(id);
			}
		} catch (DataIntegrityViolationException e) {
			LOGGER.error("Error occurred while deleting Device with id: " + id, e);
			throw new DeleteFailedException();
		}
	}

	/**
	 * This method is used to retrieve all devices by category.
	 *
	 * @param category The category of the devices to retrieve.
	 * @return A List containing all devices with the given category.
	 */
	@Override
	public List<DeviceResponseDTO> getAllDeviceDetailsByCategory(String category) {
		LOGGER.info("Starting getAllDeviceDetailsByCategory method with category: {}", category);
		List<Device> devices = new ArrayList<>();
		try {
			devices = deviceRepository.findByCategory(getCategory(category));
		} catch (Exception e) {
			LOGGER.error("Error occurred while fetching devices by category: " + category, e);
		}
		if (devices != null && !devices.isEmpty()) {
			LOGGER.info("Found {} devices", devices.size());
			return devices.stream().map(this::convertToDeviceDTO).collect(Collectors.toList());
		} else {
			LOGGER.warn("No devices found for category: " + category);
			return Collections.emptyList();
		}
	}

	/**
	 * This method is get all gateway devices.
	 * 
	 * 
	 * @return List<String> This returns a list of gateway devices.
	 */
	@Override
	public List<String> getGatewayDeviceList(String category) {
		LOGGER.info("Fetching device details");

		Category categoryVariable = Category.getCategory(category);
		if (categoryVariable == null) {
			LOGGER.error("Invalid category: " + category);
			throw new ResourceNotFoundException(Constants.CATEGORY, category);
		}

		List<BoxType> boxTypes = boxTypeRepository.findByType(BoxTypeCategory.GATEWAY);
		LOGGER.info("Fetched box types: " + boxTypes);

		if (boxTypes.isEmpty() || boxTypes == null) {
			return null;
		}

		List<String> deviceStbNames = new ArrayList<>();
		for (BoxType boxType : boxTypes) {
			List<Device> devices = deviceRepository.findByBoxTypeAndCategory(boxType, categoryVariable);
			if (devices != null) {
				for (Device device : devices) {
					deviceStbNames.add(device.getStbName());
				}
			}
		}

		LOGGER.info("Fetched device STB names: " + deviceStbNames);
		return deviceStbNames;
	}

	/**
	 * This method is used to retrieve all streams for a device.
	 *
	 * @param id The ID of the device to retrieve the streams for.
	 * @return A List containing all streams for the device with the given ID.
	 */
	@Override
	public List<StreamingDetailsResponse> getStreamsForTheDevice(Integer id) {
		LOGGER.info("Starting getStreamsForTheDevice method with ID: {}", id);
		Device device = deviceRepository.findById(id).orElseThrow(() -> {
			LOGGER.error("Device not found with ID: {}", id);
			return new ResourceNotFoundException("Device Id", id.toString());
		});
		LOGGER.info("Device found with ID: {}", id);
		List<DeviceStream> deviceStreams = deviceStreamRepository.findAllByDevice(device);
		LOGGER.info("Found {} device streams for device with ID: {}", deviceStreams.size(), id);
		return deviceStreams.stream().map(deviceStream -> {
			LOGGER.info("Processing device stream with ID: {}", deviceStream.getId());
					if (deviceStream.getStream() != null) {
						StreamingDetails details = streamingDetailsRepository
					.findByStreamId(deviceStream.getStream().getStreamId());
			if (details == null) {
				LOGGER.error("No StreamingDetails found for stream ID: {}", deviceStream.getStream());
				return null; // or throw an exception
			}
			LOGGER.info("Found streaming details for stream ID: {}", deviceStream.getStream());
			return convertToStreamingDetailsResponse(details, deviceStream.getOcapId());
					} else {
						LOGGER.warn("DeviceStream with ID: {} has no associated StreamingDetails", deviceStream.getId());
						return null;
					}
		}).filter(response -> response != null) // filter out null responses
				.peek(streamingDetailsResponse -> LOGGER.info("Converted to StreamingDetailsResponse: {}",
						streamingDetailsResponse))
				.collect(Collectors.toList());
	}

	/**
	 * This method is used to convert a StreamingDetails object to a
	 * StreamingDetailsResponse object.
	 *
	 * @param details The StreamingDetails object to convert.
	 * @param ocapId  The OCAP ID of the StreamingDetails object.
	 * @return A StreamingDetailsResponse object containing the details of the
	 *         StreamingDetails object.
	 */
	private StreamingDetailsResponse convertToStreamingDetailsResponse(StreamingDetails details, String ocapId) {
		LOGGER.trace("Converting StreamingDetails to StreamingDetailsResponse");
		StreamingDetailsResponse response = new StreamingDetailsResponse();
		response.setStreamingDetailsId(details.getStreamId());
		response.setOcapId(ocapId);
		if (details.getAudioType() != null) {
			response.setAudioType(details.getAudioType().getName());
		} else {
			response.setAudioType(null); // or set to a default value
		}

		if (details.getChannelType() != null) {
			response.setChannelType(details.getChannelType().getName());
		} else {
			response.setChannelType(null); // or set to a default value
		}
		if (details.getVideoType() != null) {
			response.setVideoType(details.getVideoType().getName());
		} else {
			response.setVideoType(null); // or set to a default value
		}

		return response;
	}

	/**
	 * This method is used to convert a Device object to a DeviceDTO object.
	 *
	 * @param device The Device object to convert.
	 * @return A DeviceDTO object containing the details of the Device object.
	 */
	private DeviceResponseDTO convertToDeviceDTO(Device device) {
		LOGGER.trace("Converting Device to DeviceDTO");
		DeviceResponseDTO deviceDTO = MapperUtils.convertToDeviceDTO(device);
		Device gatewayDevice = deviceRepository.findByStbIp(device.getGatewayIp());
		if (gatewayDevice != null) {
			deviceDTO.setGatewayDeviceName(gatewayDevice.getStbName());
		}
		return deviceDTO;
	}

	/**
	 * This method is used to parse an XML file for device details.
	 *
	 * @param file The XML file to parse.
	 */
	public void parseXMLForDevice(MultipartFile file) {
		LOGGER.info("Parsing XML file for device details");
		try {
			Document doc = getDocumentFromXMLFile(file);
			ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
			Validator validator = factory.getValidator();

			NodeList nList = doc.getElementsByTagName("device");

			for (int temp = 0; temp < nList.getLength(); temp++) {
				Node nNode = nList.item(temp);
				LOGGER.info("\nCurrent Element :" + nNode.getNodeName());
				if (nNode.getNodeType() == Node.ELEMENT_NODE) {
					Element eElement = (Element) nNode;
					DeviceCreateDTO deviceDTO = createDeviceDTOFromElement(eElement);
					validateAndCreateDevice(deviceDTO, validator);
				}
			}
		} catch (ParserConfigurationException | SAXException | IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * This method is used to create a DeviceCreateDTO object from an XML element.
	 *
	 * @param eElement The XML element to create the DeviceCreateDTO object from.
	 * @return A DeviceCreateDTO object containing the details of the XML element.
	 */
	private DeviceCreateDTO createDeviceDTOFromElement(Element eElement) {
		LOGGER.info("Creating DeviceDTO from Element");
		DeviceCreateDTO deviceDTO = new DeviceCreateDTO();

		// Set the category of the device from the XML element
		deviceDTO.setCategory(getNodeTextContent(eElement, Constants.XML_TAG_CATEGORY));

		// If the category is RDKB, set the STB name and IP from the gateway name and IP
		if (deviceDTO.getCategory().equalsIgnoreCase(Category.RDKB.getName())) {
			deviceDTO.setStbName(getNodeTextContent(eElement, Constants.XML_TAG_GATEWAY_NAME));
			deviceDTO.setStbIp(getNodeTextContent(eElement, Constants.XML_TAG_GATEWAY_IP));
		}
		// If the category is RDKC, set the STB name and IP from the camera name and IP
		else if (deviceDTO.getCategory().equalsIgnoreCase(Category.RDKC.getName())) {
			deviceDTO.setStbName(getNodeTextContent(eElement, Constants.XML_TAG_CAMERA_NAME));
			deviceDTO.setStbIp(getNodeTextContent(eElement, Constants.XML_TAG_CAMERA_IP));
		}

		// Set the STB name, IP, MAC ID, box type name, box manufacturer name, SoC
		// vendor name,
		// thunder enabled status, thunder port, recorder ID, and gateway device name
		// from the XML element
		deviceDTO.setStbName(getNodeTextContent(eElement, Constants.XML_TAG_STB_NAME));
		deviceDTO.setStbIp(getNodeTextContent(eElement, Constants.XML_TAG_STB_IP));
		deviceDTO.setMacId(getNodeTextContent(eElement, Constants.XML_TAG_MAC_ADDR));
		deviceDTO.setBoxTypeName(getNodeTextContent(eElement, Constants.XML_TAG_BOX_TYPE));
		deviceDTO.setBoxManufacturerName(getNodeTextContent(eElement, Constants.XML_TAG_BOX_MANUFACTURER));
		deviceDTO.setSocVendorName(getNodeTextContent(eElement, Constants.XML_TAG_SOC_VENDOR));
		deviceDTO.setThunderEnabled(
				Boolean.parseBoolean(getNodeTextContent(eElement, Constants.XML_TAG_IS_THUNDER_ENABLED)));
		deviceDTO.setThunderPort(getNodeTextContent(eElement, Constants.XML_TAG_THUNDER_PORT));
		deviceDTO.setRecorderId(getNodeTextContent(eElement, Constants.XML_TAG_RECORDER_ID));
		deviceDTO.setGatewayDeviceName(getNodeTextContent(eElement, Constants.XML_TAG_GATEWAY_NAME));

		// Get the list of streams from the XML element
		NodeList streamList = eElement.getElementsByTagName(Constants.XML_TAG_STREAM);
		ArrayList<DeviceStreamDTO> deviceStreamDTOList = new ArrayList<>();

		// For each stream in the list, create a DeviceStreamDTO object and add it to
		// the list
		for (int i = 0; i < streamList.getLength(); i++) {
			Node streamNode = streamList.item(i);
			if (streamNode.getNodeType() == Node.ELEMENT_NODE) {
				Element streamElement = (Element) streamNode;
				DeviceStreamDTO deviceStreamDTO = new DeviceStreamDTO();
				deviceStreamDTO.setStreamId(streamElement.getAttribute(Constants.XML_TAG_ID));
				deviceStreamDTO.setOcapId(streamElement.getTextContent());
				deviceStreamDTOList.add(deviceStreamDTO);
			}
		}

		// Set the list of streams in the DeviceCreateDTO object
		deviceDTO.setDeviceStreams(deviceStreamDTOList);

		return deviceDTO;
	}

	/**
	 * This method is used to get the text content of a node in an XML element.
	 *
	 * @param eElement The XML element containing the node.
	 * @param tagName  The name of the node to get the text content of.
	 * @return A String containing the text content of the node.
	 */
	private String getNodeTextContent(Element eElement, String tagName) {
		Node node = eElement.getElementsByTagName(tagName).item(0);
		return node != null ? node.getTextContent() : null;
	}

	/**
	 * This method is used to validate the device details and create a new device.
	 *
	 * @param deviceDTO The DeviceDTO object containing the details of the device.
	 * @param validator The Validator object to validate the device details.
	 */
	private void validateAndCreateDevice(DeviceCreateDTO deviceDTO, Validator validator) {
		Set<ConstraintViolation<DeviceCreateDTO>> violations = validator.validate(deviceDTO);
		if (!violations.isEmpty()) {
			StringBuilder sb = new StringBuilder();
			for (ConstraintViolation<DeviceCreateDTO> violation : violations) {
				sb.append(violation.getMessage()).append("\n");
			}
			throw new IllegalArgumentException("Validation errors: \n" + sb.toString());
		}

		createDevice(deviceDTO);
	}

	/**
	 * This method is used to download the device details in XML format.
	 *
	 * @param stbName The name of the device to download the details for.
	 * @return A String containing the device details in XML format.
	 */
	public String downloadDeviceXML(String stbName) {
		Device device = deviceRepository.findByStbName(stbName);
		try {
			Document doc = createDeviceXMLDocument(device);
			return convertDocumentToString(doc);
		} catch (Exception e) {
			throw new RuntimeException("Error generating XML", e);
		}
	}

	/**
	 * This method is used to create an XML document from a Device object.
	 *
	 * @param device The Device object to create the XML document from.
	 * @return A Document object containing the XML document.
	 * @throws ParserConfigurationException If a DocumentBuilder cannot be created.
	 */
	private void setDevicePropertiesFromCreateDTO(Device device, DeviceCreateDTO deviceDTO) {
		// Set common properties
		if (deviceRepository.existsByStbIp(deviceDTO.getStbIp())) {
			LOGGER.info("Device with the same stbip already exists");
			throw new ResourceAlreadyExistsException("StpIp: ", deviceDTO.getStbIp());
		}

		// Check if a device with the same stbName already exists
		if (deviceRepository.existsByStbName(deviceDTO.getStbName())) {
			LOGGER.info("Device with the same stbName already exists");
			throw new ResourceAlreadyExistsException("StbName: ", deviceDTO.getStbName());
		}

		// Check if a device with the same macid already exists
		if (deviceRepository.existsByMacId(deviceDTO.getMacId())) {
			LOGGER.info("Device with the same macid already exists");
			throw new ResourceAlreadyExistsException("MacId: ", deviceDTO.getMacId());
		}

		// Set BoxType
		BoxType boxType = boxTypeRepository.findByName(deviceDTO.getBoxTypeName());
		if (boxType != null) {
			device.setBoxType(boxType);
		} else {
			throw new ResourceNotFoundException("BoxType: ", deviceDTO.getBoxTypeName());
		}

		// Set BoxManufacturer
		BoxManufacturer boxManufacturer = boxManufacturerRepository.findByName(deviceDTO.getBoxManufacturerName());
		if (boxManufacturer != null) {
			device.setBoxManufacturer(boxManufacturer);
		} else {
			throw new ResourceNotFoundException("BoxManufacturer: ", deviceDTO.getBoxManufacturerName());
		}

		// Set SocVendor
		SocVendor socVendor = socVendorRepository.findByName(deviceDTO.getSocVendorName());
		if (socVendor != null) {
			device.setSocVendor(socVendor);
		} else {
			throw new ResourceNotFoundException("SocVendor: ", deviceDTO.getSocVendorName());
		}

		// Set UserGroup
		UserGroup userGroup = userGroupRepository.findByName(deviceDTO.getUserGroupName());
		if (userGroup != null) {
			device.setUserGroup(userGroup);
		}

		// Set Category
		Category category = Category.valueOf(deviceDTO.getCategory().toUpperCase());
		if (category != null) {
			device.setCategory(category);
		} else {
			throw new ResourceNotFoundException("Category not found", deviceDTO.getCategory());
		}

		// Check if thunder is enabled and port is set
		if (device.isThunderEnabled() && (device.getThunderPort() == null || device.getThunderPort().isEmpty())) {
			LOGGER.info("ThunderPort should not be null or empty");
			throw new MandatoryFieldException(" ThunderPort should not be null or empty");
		}

		// uf device box type type is Cline set gatewaydevice name
		if ((device.getBoxType().getType().toString().equalsIgnoreCase(CLIENT.toString())
				|| device.getBoxType().getType().toString().equalsIgnoreCase(STAND_ALONE_CLIENT.toString()))
				&& (deviceDTO.getCategory().equalsIgnoreCase(Category.RDKV.toString()))) {
			Device gatewayDevice = deviceRepository.findByStbName(deviceDTO.getGatewayDeviceName());
			if (gatewayDevice != null) {
				LOGGER.info("GatewayDevice: " + gatewayDevice);
				device.setGatewayIp(gatewayDevice.getStbIp());
			}
		}

	}

	/**
	 * This method is used to set the properties of a Device object from a
	 * DeviceUpdateDTO object.
	 *
	 * @param device          The Device object to set the properties for.
	 * @param deviceUpdateDTO The DeviceUpdateDTO object containing the properties
	 *                        to set.
	 */
	private void setDevicePropertiesFromUpdateDTO(Device device, DeviceUpdateDTO deviceUpdateDTO) {

		if (!Utils.isEmpty(deviceUpdateDTO.getBoxTypeName())) {
			BoxType boxType = boxTypeRepository.findByName(deviceUpdateDTO.getBoxTypeName());
			if (boxType != null) {
				device.setBoxType(boxType);
			} else {
				throw new ResourceNotFoundException("BoxType: ", deviceUpdateDTO.getBoxTypeName());
			}
		}

		if (!Utils.isEmpty(deviceUpdateDTO.getBoxManufacturerName())) {
			BoxManufacturer boxManufacturer = boxManufacturerRepository
					.findByName(deviceUpdateDTO.getBoxManufacturerName());
			if (boxManufacturer != null) {
				device.setBoxManufacturer(boxManufacturer);
			} else {
				throw new ResourceNotFoundException("BoxManufacturer: ", deviceUpdateDTO.getBoxManufacturerName());
			}
		}

		if (!Utils.isEmpty(deviceUpdateDTO.getSocVendorName())) {
			SocVendor socVendor = socVendorRepository.findByName(deviceUpdateDTO.getSocVendorName());
			if (socVendor != null) {
				device.setSocVendor(socVendor);
			} else {
				throw new ResourceNotFoundException("SocVendor: ", deviceUpdateDTO.getSocVendorName());
			}
		}
		UserGroup userGroup = userGroupRepository.findByName(deviceUpdateDTO.getUserGroupName());
		if (null != userGroup)
			device.setUserGroup(userGroup);
		// Check if thunder is enabled and port is set
		if (device.isThunderEnabled()) {
			if (deviceUpdateDTO.getThunderPort() != null && !deviceUpdateDTO.getThunderPort().isEmpty()) {
				device.setThunderPort(deviceUpdateDTO.getThunderPort());
			} else if (device.getThunderPort() == null || device.getThunderPort().isEmpty()) {
				LOGGER.info("ThunderPort should not be null or empty");
				throw new MandatoryFieldException(" ThunderPort should not be null or empty");
			}
		}

// If device box type is Client, set gateway device name
		if ((device.getBoxType().getType().toString().equalsIgnoreCase(CLIENT.toString())
				|| device.getBoxType().getType().toString().equalsIgnoreCase(STAND_ALONE_CLIENT.toString()))
				&& (deviceUpdateDTO.getCategory().equalsIgnoreCase(Category.RDKV.toString()))) {
			if (deviceUpdateDTO.getGatewayDeviceName() != null && !deviceUpdateDTO.getGatewayDeviceName().isEmpty()) {
				Device gatewayDevice = deviceRepository.findByStbName(deviceUpdateDTO.getGatewayDeviceName());
				if (gatewayDevice != null) {
					LOGGER.info("GatewayDevice: " + gatewayDevice);
					device.setGatewayIp(gatewayDevice.getStbIp());
				}
			}
		}

	}

	/**
	 * This method is used to get a Document object from an XML file.
	 *
	 * @param file The XML file to get the Document object from.
	 * @return A Document object containing the contents of the XML file.
	 * @throws ParserConfigurationException If a DocumentBuilder cannot be created.
	 * @throws SAXException                 If an error occurs while parsing the XML
	 *                                      file.
	 * @throws IOException                  If an error occurs while reading the XML
	 *                                      file.
	 */
	private Document getDocumentFromXMLFile(MultipartFile file)
			throws ParserConfigurationException, SAXException, IOException {
		String xmlData = new String(file.getBytes(), StandardCharsets.UTF_8);
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
		InputSource is = new InputSource(new StringReader(xmlData));
		return dBuilder.parse(is);
	}

	/**
	 * This method is used to create an XML document for a device.
	 *
	 * @param device The device for which to create the XML document.
	 * @return A Document object containing the device details in XML format.
	 */
	private Document createDeviceXMLDocument(Device device) throws ParserConfigurationException {
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
		Document doc = dBuilder.newDocument();

		Element rootElement = doc.createElement(Constants.XML_TAG_ROOT);
		doc.appendChild(rootElement);

		Element deviceElement = doc.createElement(Constants.XML_TAG_DEVICE);
		rootElement.appendChild(deviceElement);

		// Add comments to the XML document
		String nameTag = selectTag(device, Constants.XML_TAG_GATEWAY_NAME, Constants.XML_TAG_CAMERA_NAME,
				Constants.XML_TAG_STB_NAME);
		appendElement(deviceElement, nameTag, device.getStbName(), "  Unique name for the STB");

		String ipTag = selectTag(device, Constants.XML_TAG_GATEWAY_IP, Constants.XML_TAG_CAMERA_IP,
				Constants.XML_TAG_STB_IP);
		appendElement(deviceElement, ipTag, device.getStbIp(), " Unique IP for the STB");

		appendElement(deviceElement, Constants.XML_TAG_MAC_ADDR, device.getMacId(), " Mac Addr for the STB");
		appendElement(deviceElement, Constants.XML_TAG_IS_THUNDER_ENABLED, String.valueOf(device.isThunderEnabled()),
				" Is Thunder enabled for STB");
		appendElement(deviceElement, Constants.XML_TAG_THUNDER_PORT, device.getThunderPort(),
				" Thunder port for thunder devices");
		appendElement(deviceElement, Constants.XML_TAG_BOX_TYPE, device.getBoxType().getName(), " BoxType for STB");
		appendElement(deviceElement, Constants.XML_TAG_BOX_MANUFACTURER, device.getBoxManufacturer().getName(),
				" BoxManufacture for the STB");
		appendElement(deviceElement, Constants.XML_TAG_SOC_VENDOR, device.getSocVendor().getName(),
				" SoC vendor for the STB");
		appendElement(deviceElement, Constants.XML_TAG_CATEGORY, device.getCategory().toString(),
				" Category for the STB");
		appendElement(deviceElement, Constants.XML_TAG_RECORDER_ID, device.getRecorderId(), " Recorder ID for the STB");
		appendElement(deviceElement, Constants.XML_TAG_GATEWAY_IP_device, device.getGatewayIp(),
				" Gateway device IP for the STB");

		List<DeviceStream> deviceStreams = deviceStreamRepository.findAllByDevice(device);
		if (deviceStreams != null && !deviceStreams.isEmpty()) {
			Element streamsElement = doc.createElement(Constants.XML_TAG_STREAMS);
			deviceElement.appendChild(streamsElement);
			for (DeviceStream deviceStream : deviceStreams) {

				// Add a comment before each stream element
				Comment comment = doc.createComment(" Stream details for the STB");
				streamsElement.appendChild(comment);

				Element streamElement = doc.createElement(Constants.XML_TAG_STREAM);
				Attr attr = doc.createAttribute(Constants.XML_TAG_ID);
				attr.setValue(deviceStream.getStream().getStreamId());
				streamElement.setAttributeNode(attr);
				streamElement.appendChild(doc.createTextNode(deviceStream.getOcapId()));
				streamsElement.appendChild(streamElement);
			}
		}
		return doc;
	}

	/**
	 * This method is used to append an element to a parent element.
	 *
	 * @param parent      The parent element to append the new element to.
	 * @param tagName     The name of the new element to append.
	 * @param textContent The text content of the new element.
	 */
	private void appendElement(Element parent, String tagName, String textContent, String commentText) {
		if (textContent != null && !textContent.isEmpty()) {
			Document doc = parent.getOwnerDocument();
			Comment comment = doc.createComment(commentText);
			parent.appendChild(comment);
			Element element = doc.createElement(tagName);
			element.appendChild(doc.createTextNode(textContent));
			parent.appendChild(element);
		}
	}

	/**
	 * This method is used to select a tag based on the device category.
	 *
	 * @param device     The device for which to select the tag.
	 * @param gatewayTag The tag to select if the device is a gateway.
	 * @param cameraTag  The tag to select if the device is a camera.
	 * @param defaultTag The default tag to select if the device is neither a
	 *                   gateway nor a camera.
	 * @return A String containing the selected tag.
	 */
	private String selectTag(Device device, String gatewayTag, String cameraTag, String defaultTag) {
		if (device.getCategory().getName().equalsIgnoreCase(Category.RDKB.getName())) {
			return gatewayTag;
		} else if (device.getCategory().getName().equalsIgnoreCase(Category.RDKC.getName())) {
			return cameraTag;
		} else {
			return defaultTag;
		}
	}

	/**
	 * This method is used to convert a Document object to a String.
	 *
	 * @param doc The Document object to convert.
	 * @return A String containing the contents of the Document object.
	 * @throws TransformerException If an error occurs while transforming the
	 *                              Document object.
	 */
	private String convertDocumentToString(Document doc) throws TransformerException {
		TransformerFactory transformerFactory = TransformerFactory.newInstance();
		Transformer transformer = transformerFactory.newTransformer();
		transformer.setOutputProperty(OutputKeys.INDENT, "yes");
		// Set standalone to yes
		DOMSource source = new DOMSource(doc);
		StringWriter writer = new StringWriter();
		StreamResult result = new StreamResult(writer);
		transformer.transform(source, result);

		return writer.toString();
	}

	/**
	 * This method is used to generate an XML file for a device.
	 *
	 * @param device The device for which to generate the XML file.
	 * @return A String containing the XML content for the device.
	 * @throws Exception If an error occurs while generating the XML content.
	 */
	public String generateXMLForDevice(Device device) throws Exception {
		Document doc = createDeviceXMLDocument(device);
		TransformerFactory tf = TransformerFactory.newInstance();
		Transformer transformer = tf.newTransformer();
		StringWriter writer = new StringWriter();
		transformer.transform(new DOMSource(doc), new StreamResult(writer));
		return writer.getBuffer().toString();
	}

	/**
	 *
	 * @param category This is the category of the Devices to be downloaded.
	 * @return
	 * @throws Exception
	 */
	@Override
	public Path downloadAllDevicesByCategory(String category) throws Exception {
		LOGGER.info("Downloading all devices for category: {}", category);
		List<Device> devices = deviceRepository.findAllByCategory(Category.valueOf(category.toUpperCase()));
		Path zipFilePath = Paths.get("devices_" + category + DEVICE_FILE_EXTENSION_ZIP);
		try (ZipOutputStream zipOut = new ZipOutputStream(new FileOutputStream(zipFilePath.toFile()))) {
			// Add each device to the zip file
			for (Device device : devices) {
				// Create an XML document for the device
				Document doc = createDeviceXMLDocument(device);
				String xmlString = convertDocumentToString(doc);
				// Add the XML content to the zip file
				ZipEntry zipEntry = new ZipEntry(device.getStbName() + DEVICE_XML_FILE_EXTENSION);
				zipOut.putNextEntry(zipEntry);
				// Write the XML content to the zip file
				byte[] bytes = xmlString.getBytes();
				zipOut.write(bytes, 0, bytes.length);
				zipOut.closeEntry();
			}
		}

		return zipFilePath;
	}

}
