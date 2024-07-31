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

import com.rdkm.tdkservice.dto.RdkVersionCreateDTO;
import com.rdkm.tdkservice.dto.RdkVersionDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.RdkVersion;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.RdkVersionRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.service.IRdkVersionService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;

/**
 * The rdk version service.
 */
@Service
public class RdkVersionService implements IRdkVersionService {

	public static final Logger LOGGER = LoggerFactory.getLogger(RdkVersionService.class);

	@Autowired
	RdkVersionRepository rdkVersionRepository;

	@Autowired
	UserGroupRepository userGroupRepository;

	/**
	 * Create the rdk version.
	 * 
	 * @param rdkVersionCreateDTO
	 * @return
	 * 
	 */
	@Override
	public boolean createRdkVersion(RdkVersionCreateDTO rdkVersionCreateDTO) {
		LOGGER.info("Creating rdk version: " + rdkVersionCreateDTO.toString());
		if (rdkVersionRepository.existsByName(rdkVersionCreateDTO.getBuildVersionName())) {
			LOGGER.info("Rdk version already exists with the same name: " + rdkVersionCreateDTO.getBuildVersionName());
			throw new ResourceAlreadyExistsException(Constants.RDK_VERSION_NAME,
					rdkVersionCreateDTO.getBuildVersionName());
		}
		RdkVersion rdkVersion = new RdkVersion();
		rdkVersion.setName(rdkVersionCreateDTO.getBuildVersionName());
		Category category = Category.getCategory(rdkVersionCreateDTO.getRdkVersionCategory());
		if (category == null) {
			LOGGER.error("Invalid category: " + rdkVersionCreateDTO.getRdkVersionCategory());
			throw new ResourceNotFoundException(Constants.CATEGORY, rdkVersionCreateDTO.getRdkVersionCategory());
		}
		rdkVersion.setCategory(category);
		UserGroup userGroup = userGroupRepository.findByName(rdkVersionCreateDTO.getRdkVersionUserGroup());
		rdkVersion.setUserGroup(userGroup);
		try {
			rdkVersionRepository.save(rdkVersion);
		} catch (Exception e) {
			LOGGER.error("Error in saving rdk version data: " + e.getMessage());
			return false;
		}
		return true;
	}

	/**
	 * Update the rdk version.
	 * 
	 * @param rdkVersionDTO
	 * @return
	 * 
	 */
	@Override
	public boolean updateRdkVersion(RdkVersionDTO rdkVersionDTO) {
		LOGGER.info("Updating rdk version: " + rdkVersionDTO.toString());
		RdkVersion rdkVersion = rdkVersionRepository.findById(rdkVersionDTO.getRdkVersionId())
				.orElseThrow(() -> new ResourceNotFoundException(Constants.RDK_VERSION_ID,
						rdkVersionDTO.getRdkVersionId().toString()));
		if (!Utils.isEmpty(rdkVersionDTO.getBuildVersionName())) {
			if (rdkVersionRepository.existsByName(rdkVersionDTO.getBuildVersionName())) {
				LOGGER.info("Rdk version already exists with the same name: " + rdkVersionDTO.getBuildVersionName());
				throw new ResourceAlreadyExistsException(Constants.RDK_VERSION_NAME,
						rdkVersionDTO.getBuildVersionName());
			} else {
				rdkVersion.setName(rdkVersionDTO.getBuildVersionName());
			}

		}
		if (!Utils.isEmpty(rdkVersionDTO.getRdkVersionCategory())) {
			Category category = Category.getCategory(rdkVersionDTO.getRdkVersionCategory());
			if (category == null) {
				LOGGER.error("Invalid category: " + rdkVersionDTO.getRdkVersionCategory());
				throw new ResourceNotFoundException(Constants.CATEGORY, rdkVersionDTO.getRdkVersionCategory());
			}
			rdkVersion.setCategory(category);
		}
		try {
			rdkVersionRepository.save(rdkVersion);
		} catch (Exception e) {
			LOGGER.error("Error in updating rdk version data: " + e.getMessage());
			return false;
		}
		return true;

	}

	/**
	 * Delete the rdk version.
	 * 
	 * @param id
	 * @return
	 * 
	 */
	@Override
	public void deleteRdkVersion(Integer id) {
		LOGGER.info("Deleting rdk version: " + id.toString());
		RdkVersion rdkVersion = rdkVersionRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.RDK_VERSION_ID, id.toString()));
		try {
			rdkVersionRepository.delete(rdkVersion);
		} catch (DataIntegrityViolationException e) {
			LOGGER.error("Error in deleting rdk version data: " + e.getMessage());
			throw new DeleteFailedException();
		}

	}

	/**
	 * Find all the rdk versions.
	 * 
	 * @return
	 * 
	 */
	@Override
	public List<RdkVersionDTO> findAllRdkVersions() {
		LOGGER.info("Finding all rdk versions");
		List<RdkVersion> rdkVersionList = rdkVersionRepository.findAll();
		if ((null == rdkVersionList) || rdkVersionList.isEmpty()) {
			return null;
		}
		return rdkVersionList.stream().map(MapperUtils::convertToRdkVersionDTO).collect(Collectors.toList());
	}

	/**
	 * Find all the rdk versions by category.
	 * 
	 * @param category
	 * @return
	 * 
	 */
	@Override
	public List<RdkVersionDTO> findAllRdkVersionsByCategory(String category) {
		LOGGER.info("Finding all rdk versions by category: " + category);
		Utils.checkCategoryValid(category);
		List<RdkVersion> rdkVersionList = rdkVersionRepository.findByCategory(Category.getCategory(category));
		if ((null == rdkVersionList) || rdkVersionList.isEmpty()) {
			return null;
		}
		return rdkVersionList.stream().map(MapperUtils::convertToRdkVersionDTO).collect(Collectors.toList());
	}

	/**
	 * Find all rdk version name.
	 * 
	 * @param buildVersionName
	 * @return
	 * 
	 */
	@Override
	public List<String> getRdkVersionListByCategory(String category) {
		LOGGER.info("Getting rdk version list by category: " + category);
		Utils.checkCategoryValid(category);
		List<RdkVersion> rdkVersionList = rdkVersionRepository.findByCategory(Category.getCategory(category));
		if ((null == rdkVersionList) || rdkVersionList.isEmpty()) {
			return null;
		}
		return rdkVersionList.stream().map(RdkVersion::getName).collect(Collectors.toList());

	}

	/**
	 * Find the rdk version by id.
	 * 
	 * @param id
	 * @return
	 * 
	 */
	@Override
	public RdkVersionDTO findRdkVersionById(Integer id) {
		LOGGER.info("Finding rdk version by id: " + id.toString());
		RdkVersion rdkVersion = rdkVersionRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.RDK_VERSION_ID, id.toString()));
		return MapperUtils.convertToRdkVersionDTO(rdkVersion);

	}

}
