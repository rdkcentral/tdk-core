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

import java.util.List;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;

import com.rdkm.tdkservice.dto.ScriptTagCreateDTO;
import com.rdkm.tdkservice.dto.ScriptTagDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.ScriptTag;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.ScriptTagRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.service.IScriptTagService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;

import jakarta.validation.Valid;
/*
 * The script tag service.
 */

@Service
public class ScriptTagService implements IScriptTagService {

	private static final Logger LOGGER = LoggerFactory.getLogger(ScriptTagService.class);

	@Autowired
	ScriptTagRepository scriptTagRepository;

	@Autowired
	UserGroupRepository userGroupRepository;

	/**
	 * Create the script tag.
	 * 
	 * @param scriptTagRequest
	 * @return
	 * 
	 */
	@Override
	public boolean createScriptTag(@Valid ScriptTagCreateDTO scriptTagRequest) {
		LOGGER.info("Creating script tag: " + scriptTagRequest.toString());
		if (scriptTagRepository.existsByName(scriptTagRequest.getScriptTagName())) {
			LOGGER.info("Script tag already exists with the same name: " + scriptTagRequest.getScriptTagName());
			throw new ResourceAlreadyExistsException(Constants.SCRIPT_TAG_NAME, scriptTagRequest.getScriptTagName());
		}
		ScriptTag scriptTag = new ScriptTag();
		scriptTag.setName(scriptTagRequest.getScriptTagName());
		Category category = Category.getCategory(scriptTagRequest.getScriptTagCategory());
		if (category == null) {
			LOGGER.error("Invalid category: " + scriptTagRequest.getScriptTagCategory());
			throw new ResourceNotFoundException(Constants.CATEGORY, scriptTagRequest.getScriptTagCategory());
		}
		scriptTag.setCategory(category);
		UserGroup userGroup = userGroupRepository.findByName(scriptTagRequest.getScriptTagUserGroup());
		scriptTag.setUserGroup(userGroup);
		try {
			scriptTagRepository.save(scriptTag);
		} catch (Exception e) {
			LOGGER.error("Error in saving script tag data: " + e.getMessage());
			return false;
		}
		return true;

	}

	/**
	 * Update the script tag.
	 * 
	 * @param scriptTagRequest
	 * @return
	 * 
	 */
	@Override
	public boolean updateScriptTag(ScriptTagDTO scriptTagRequest) {
		LOGGER.info("Updating script tag: " + scriptTagRequest.toString());
		ScriptTag scriptTag = scriptTagRepository.findById(scriptTagRequest.getScriptTagId())
				.orElseThrow(() -> new ResourceNotFoundException(Constants.SCRIPT_TAG_ID,
						scriptTagRequest.getScriptTagId().toString()));
		// Check if the script tag name is not empty and it is not same as the existing name
		if (!Utils.isEmpty(scriptTagRequest.getScriptTagName())) {
			if (scriptTagRepository.existsByName(scriptTagRequest.getScriptTagName())) {
				LOGGER.info("Script tag already exists with the same name: " + scriptTagRequest.getScriptTagName());
				throw new ResourceAlreadyExistsException(Constants.SCRIPT_TAG_NAME,
						scriptTagRequest.getScriptTagName());
			} else {
				scriptTag.setName(scriptTagRequest.getScriptTagName());
			}
		}
		if (!Utils.isEmpty(scriptTagRequest.getScriptTagCategory())) {
			Category category = Category.getCategory(scriptTagRequest.getScriptTagCategory());
			if (category == null) {
				LOGGER.error("Invalid category: " + scriptTagRequest.getScriptTagCategory());
				throw new ResourceNotFoundException(Constants.CATEGORY, scriptTagRequest.getScriptTagCategory());
			}
			scriptTag.setCategory(category);
		}
		try {
			scriptTagRepository.save(scriptTag);
		} catch (Exception e) {
			LOGGER.error("Error in updating script tag data: " + e.getMessage());
			return false;
		}

		return true;

	}

	/**
	 * Delete the script tag.
	 * 
	 * @param id
	 * @return
	 * 
	 */
	@Override
	public void deleteScriptTag(Integer id) {
		LOGGER.info("Deleting script tag: " + id.toString());
		ScriptTag scriptTag = scriptTagRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.SCRIPT_TAG_ID, id.toString()));
		try {
			scriptTagRepository.delete(scriptTag);
		} catch (DataIntegrityViolationException e) {
			LOGGER.error("Error in deleting script tag data: " + e.getMessage());
			throw new DeleteFailedException();

		}

	}

	/**
	 * Find all the script tag.
	 * 
	 * @return
	 * 
	 */
	@Override
	public List<ScriptTagDTO> findAllScriptTag() {
		LOGGER.info("Finding all script tags");
		List<ScriptTag> scriptTags = scriptTagRepository.findAll();
		if (null == scriptTags || scriptTags.isEmpty()) {
			return null;
		}
		return scriptTags.stream().map(MapperUtils::convertToScriptTagDTO).collect(Collectors.toList());
	}

	/**
	 * Find all the script tag by category.
	 * 
	 * @param category
	 * @return
	 * 
	 */
	@Override
	public List<ScriptTagDTO> findAllScriptTagByCategory(String category) {
		LOGGER.info("Finding all script tags by category: " + category);
		Utils.checkCategoryValid(category);
		List<ScriptTag> scriptTags = scriptTagRepository.findByCategory(Category.getCategory(category));
		if (null == scriptTags || scriptTags.isEmpty()) {
			return null;
		}
		return scriptTags.stream().map(MapperUtils::convertToScriptTagDTO).collect(Collectors.toList());

	}

	/**
	 * Find all the script tag by category.
	 * 
	 * @param category
	 * @return
	 * 
	 */
	@Override
	public List<String> getListOfScriptTagByCategory(String category) {
		LOGGER.info("Getting list of script tags by category: " + category);
		Utils.checkCategoryValid(category);
		List<ScriptTag> scriptTags = scriptTagRepository.findByCategory(Category.getCategory(category));
		if (null == scriptTags || scriptTags.isEmpty()) {
			return null;
		}
		return scriptTags.stream().map(ScriptTag::getName).collect(Collectors.toList());
	}

	/**
	 * Find the script tag by id.
	 * 
	 * @param id
	 * @return
	 * 
	 */
	@Override
	public ScriptTagDTO findById(Integer id) {
		LOGGER.info("Finding script tag by id: " + id.toString());
		ScriptTag scriptTag = scriptTagRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.SCRIPT_TAG_ID, id.toString()));
		return MapperUtils.convertToScriptTagDTO(scriptTag);
	}

}
