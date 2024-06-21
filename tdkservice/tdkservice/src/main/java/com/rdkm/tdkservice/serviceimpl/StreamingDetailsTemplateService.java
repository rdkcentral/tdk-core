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

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.rdkm.tdkservice.dto.StreamingDetailsTemplateDTO;
import com.rdkm.tdkservice.dto.StreamingMap;
import com.rdkm.tdkservice.dto.StreamingTemplateUpdateDTO;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.StreamingDetails;
import com.rdkm.tdkservice.model.StreamingDetailsTemplate;
import com.rdkm.tdkservice.repository.StreamingDetailsRepository;
import com.rdkm.tdkservice.repository.StreamingDetailsTemplateRepository;
import com.rdkm.tdkservice.dto.StreamingDetailsResponse;
import com.rdkm.tdkservice.service.IStreamingDetailsTemplateService;
import com.rdkm.tdkservice.util.Constants;

/**
 * This class represents the service implementation for managing streaming
 * details templates. It provides methods for creating a new streaming details
 * template, retrieving all streaming details templates, deleting a streaming
 * details template, and updating a streaming details template.
 */
@Service
public class StreamingDetailsTemplateService implements IStreamingDetailsTemplateService {

	private static final Logger LOGGER = LoggerFactory.getLogger(StreamingDetailsTemplateService.class);

	@Autowired
	StreamingDetailsTemplateRepository templateRepository;

	@Autowired
	StreamingDetailsRepository streamingDetailsRepository;

	/**
	 * Creates a new streaming details template.
	 *
	 * @param templateDTO The request object containing the details of the streaming
	 *                    details template.
	 * @return true if the streaming details template is created successfully, false
	 *         otherwise.
	 * @throws ResourceNotFoundException if a streaming details with the same name
	 *                                   already exists.
	 */
	@Override
	public boolean createStreamingDetailsTemplate(StreamingDetailsTemplateDTO templateDTO) {
		LOGGER.info("Received request to create template: " + templateDTO);
		if (templateRepository.existsByTemplateName(templateDTO.getTemplateName())) {
			throw new ResourceAlreadyExistsException(Constants.STREAMING_TEMPLATE_DETAILS,
					templateDTO.getTemplateName());
		}
		// Get all ocapId values
		List<String> ocapIds = templateDTO.getStreamingMaps().stream().map(StreamingMap::getOcapId)
				.collect(Collectors.toList());

		// Check if all ocapId values are unique
		Set<String> uniqueOcapIds = new HashSet<>(ocapIds);
		if (uniqueOcapIds.size() != ocapIds.size()) {
			throw new ResourceAlreadyExistsException("OcapId values must be unique within the same template", "OcapId");
		}
		try {
			// Create a streaming details template for each streaming details
			ArrayList<StreamingMap> streamingMapArray = templateDTO.getStreamingMaps();
			for (StreamingMap streamingMap : streamingMapArray) {
				// Check if streaming details exist with the given streamId
				StreamingDetails streamingDetails = streamingDetailsRepository
						.findByStreamId(streamingMap.getStreamingId());
				if (streamingDetails == null) {
					throw new ResourceNotFoundException(Constants.STREAMING_DETAILS_ID, streamingMap.getStreamingId());
				}
				// Create a new streaming details template
				StreamingDetailsTemplate template = new StreamingDetailsTemplate();
				template.setTemplateName(templateDTO.getTemplateName());
				template.setOcapId(streamingMap.getOcapId());
				template.setStreamingDetails(streamingDetails);
				templateRepository.save(template);
			}

			return true;

		} catch (Exception e) {
			LOGGER.error("Error occurred while creating StreamingDetailsTemplate", e);
			return false;
		}

	}

	/**
	 * Gets streaming details by template name.
	 *
	 * @param templateName
	 * @return
	 */
	@Override
	public List<StreamingDetailsResponse> getStreamingDetailsByTemplateName(String templateName) {
		LOGGER.info("Received request to get streaming details for template: " + templateName);

		try {
			// Get all templates with the given template name
			List<StreamingDetailsTemplate> templates = templateRepository.findByTemplateName(templateName);
			if (templates == null || templates.isEmpty()) {
				throw new ResourceNotFoundException(Constants.STREAMING_TEMPLATE_DETAILS, templateName);
			}
			// Get all streaming details
			List<StreamingDetails> streamingDetails = streamingDetailsRepository.findAll();

			// Create a map of streamId to template
			Map<String, StreamingDetailsTemplate> templateMap = templates.stream()
					.collect(Collectors.toMap(t -> t.getStreamingDetails().getStreamId(), t -> t));

			List<StreamingDetailsResponse> templateDTOs = new ArrayList<>();
			for (StreamingDetails streamingDetail : streamingDetails) {
				// Create a template DTO for each streaming details
				StreamingDetailsTemplate template = templateMap.get(streamingDetail.getStreamId());
				StreamingDetailsResponse templateDTO = new StreamingDetailsResponse();
				templateDTO.setStreamingDetailsId(streamingDetail.getStreamId());
				templateDTO.setOcapId(template != null ? template.getOcapId() : Constants.EMPTY_STRING);
				templateDTO.setAudioType(
						streamingDetail.getAudioType() != null ? streamingDetail.getAudioType().getName() : null);
				templateDTO.setChannelType(
						streamingDetail.getChannelType() != null ? streamingDetail.getChannelType().getName() : null);
				templateDTO.setVideoType(
						streamingDetail.getVideoType() != null ? streamingDetail.getVideoType().getName() : null);
				templateDTOs.add(templateDTO);
			}

			return templateDTOs;
		} catch (Exception e) {
			LOGGER.error("Error occurred while fetching StreamingDetailsTemplate", e);
			return null;
		}

	}

	/**
	 * Updates a template.
	 *
	 * @param updateTemplateDTO
	 * @return
	 */
	public boolean updateTemplate(StreamingTemplateUpdateDTO updateTemplateDTO) {
		LOGGER.info("Received request to update template: " + updateTemplateDTO);
		List<StreamingDetailsTemplate> templates = templateRepository
				.findByTemplateName(updateTemplateDTO.getExistingTemplateName());
		if (templates == null || templates.isEmpty()) {
			throw new ResourceNotFoundException(Constants.STREAMING_TEMPLATE_DETAILS,
					updateTemplateDTO.getExistingTemplateName());
		}
		if (templateRepository.existsByTemplateName(updateTemplateDTO.getNewTemplateName())) {
			throw new ResourceAlreadyExistsException(Constants.STREAMING_TEMPLATE_DETAILS,
					updateTemplateDTO.getNewTemplateName());
		}

		List<String> ocapIds = updateTemplateDTO.getStreamingMaps().stream().map(StreamingMap::getOcapId)
				.collect(Collectors.toList());
		// Check if all ocapId values are unique
		Set<String> uniqueOcapIds = new HashSet<>(ocapIds);
		if (uniqueOcapIds.size() != ocapIds.size()) {
			throw new ResourceAlreadyExistsException("OcapId values must be unique within the same template", "OcapId");
		}
		try {
			// Create a map of streamId to template
			Map<String, StreamingDetailsTemplate> templateMap = templates.stream()
					.collect(Collectors.toMap(t -> t.getStreamingDetails().getStreamId(), t -> t));
			// Update the template if with existing streaming details if any additional
			// streaming details present create streaming template for that also
			ArrayList<StreamingMap> streamingMaps = updateTemplateDTO.getStreamingMaps();
			for (StreamingMap streamingMap : streamingMaps) {
				StreamingDetailsTemplate template = templateMap.get(streamingMap.getStreamingId());
				// If template exists update the template
				if (template != null) {
					template.setOcapId(streamingMap.getOcapId());
					template.setTemplateName(updateTemplateDTO.getNewTemplateName());
				} else {
					// If template does not exist create a new template
					template = new StreamingDetailsTemplate();
					template.setTemplateName(updateTemplateDTO.getNewTemplateName());
					template.setOcapId(streamingMap.getOcapId());
					StreamingDetails streamingDetails = streamingDetailsRepository
							.findByStreamId(streamingMap.getStreamingId());
					if (streamingDetails == null) {
						throw new ResourceNotFoundException(Constants.STREAMING_DETAILS_ID,
								streamingMap.getStreamingId());
					}
					template.setStreamingDetails(streamingDetails);
				}
				templateRepository.save(template);
			}

			return true;
		} catch (Exception e) {
			LOGGER.error("Error occurred while updating StreamingDetailsTemplate", e);
			return false;
		}
	}

	/**
	 * Deletes a template.
	 *
	 * @param templateName
	 * @return
	 */
	@Override
	public boolean deleteTemplate(String templateName) {
		LOGGER.info("Received request to delete template: " + templateName);
		try {
			List<StreamingDetailsTemplate> templates = templateRepository.findByTemplateName(templateName);
			if (templates == null || templates.isEmpty()) {
				throw new ResourceNotFoundException(Constants.STREAMING_TEMPLATE_DETAILS, templateName);
			}
			templateRepository.deleteAll(templates);
			return true;
		} catch (Exception e) {
			LOGGER.error("Error occurred while deleting StreamingDetailsTemplate", e);
			return false;
		}
	}

	/**
	 * Gets a list of templates.
	 *
	 * @return
	 */
	@Override
	public List<String> getTemplateList() {
		LOGGER.info("Received request to get template list");
		try {
			// Get all templates
			List<StreamingDetailsTemplate> templates = templateRepository.findAll();
			if (templates == null || templates.isEmpty()) {
				return null;
			}
			List<String> templateList = new ArrayList<>();
			for (StreamingDetailsTemplate template : templates) {
				String templateName = template.getTemplateName();
				if (!templateList.contains(templateName)) {
					templateList.add(templateName);
				}
			}
			return templateList;
		} catch (Exception e) {
			LOGGER.error("Error occurred while fetching StreamingDetailsTemplate", e);
			return null;
		}
	}

}
