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

import com.rdkm.tdkservice.dto.SocVendorDTO;
import com.rdkm.tdkservice.dto.SocVendorUpdateDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.SocVendor;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.SocVendorRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.service.ISocVendorService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;

/**
 * This class represents the service implementation for managing SOC vendors. It
 * provides methods for creating a new SOC vendor, retrieving all SOC vendors,
 * deleting a SOC vendor, and updating a SOC vendor.
 */
@Service
public class SocVendorService implements ISocVendorService {

	private static final Logger LOGGER = LoggerFactory.getLogger(SocVendorService.class);
	@Autowired
	SocVendorRepository socVendorRepository;

	@Autowired
	UserGroupRepository userGroupRepository;

	/**
	 * Creates a new SOC vendor.
	 *
	 * @param socVendorDTO The request object containing the details of the SOC
	 *                     vendor.
	 * @return true if the SOC vendor is created successfully, false otherwise.
	 * @throws ResourceAlreadyExistsException if a SOC vendor with the same name
	 *                                        already exists.
	 */
	@Override
	public boolean createSocVendor(SocVendorDTO socVendorDTO) {
		LOGGER.info("SocVendorDTO: " + socVendorDTO);
		if (socVendorRepository.existsByName(socVendorDTO.getSocVendorName())) {
			LOGGER.info("Soc vendor already exists with the same name: " + socVendorDTO.getSocVendorName());
			throw new ResourceAlreadyExistsException(Constants.SOCVENDOR_NAME, socVendorDTO.getSocVendorName());
		}
		SocVendor socVendor = new SocVendor();
		socVendor.setName(socVendorDTO.getSocVendorName());
		socVendor.setCategory(Category.getCategory(socVendorDTO.getSocVendorCategory()));
		UserGroup userGroup = userGroupRepository.findByName(socVendorDTO.getSocVendorUserGroup());
		socVendor.setUserGroup(userGroup);
		try {
			socVendor = socVendorRepository.save(socVendor);
		} catch (Exception e) {
			LOGGER.error("Error while saving SocVendor: " + e.getMessage());
			return false;
		}

		return socVendor != null && socVendor.getId() > 0;

	}

	/**
	 * Retrieves all SOC vendors.
	 *
	 * @return a list of all SOC vendors.
	 */
	@Override
	public List<SocVendorDTO> findAll() {
		LOGGER.info("Going to fetch all the soc vendors");
		List<SocVendor> socVendors = socVendorRepository.findAll();
		if (socVendors == null || socVendors.isEmpty()) {
			LOGGER.info("No soc vendors found");
			return null;
		}
		return socVendors.stream().map(MapperUtils::convertToSocVendorDTO).collect(Collectors.toList());

	}

	/**
	 * Deletes a SOC vendor by ID.
	 *
	 * @param id the ID of the SOC vendor to delete
	 * @throws ResourceNotFoundException if the SOC vendor with the provided ID does
	 *                                   not exist.
	 */
	@Override
	public void deleteSocVendor(Integer id) {
		if (!socVendorRepository.existsById(id)) {
			LOGGER.info("Soc vendor with id: " + id + " does not exist");
			throw new ResourceNotFoundException(Constants.SOCVENDOR_ID, id.toString());
		}
		try {
			socVendorRepository.deleteById(id);
		} catch (DataIntegrityViolationException e) {
			LOGGER.error("Error while deleting SocVendor: " + e.getMessage());
			throw new DeleteFailedException();
		}
	}

	/**
	 * Retrieves a SOC vendor by its ID.
	 *
	 * @param id the ID of the SOC vendor to retrieve
	 * @return the SOC vendor if found, or a NOT_FOUND status with an error message
	 *         if not found
	 */
	@Override
	public SocVendorDTO findById(Integer id) {
		LOGGER.info("Going to fetch SocVendor with id: " + id);
		SocVendor socVendor = socVendorRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.SOCVENDOR_ID, id.toString()));
		return MapperUtils.convertToSocVendorDTO(socVendor);

	}

	/**
	 * Updates a SOC vendor based on the provided SocVendorUpdateDTO.
	 *
	 * @param socVendorUpdateDTO The DTO containing the updated details of the SOC
	 *                           vendor.
	 * @param id                 The ID of the SOC vendor to be updated.
	 * @return SocVendorUpdateDTO The DTO representation of the updated SOC vendor
	 *         object.
	 * @throws ResourceNotFoundException If the SOC vendor with the provided ID does
	 *                                   not exist.
	 */
	@Override
	public SocVendorUpdateDTO updateSocVendor(SocVendorUpdateDTO socVendorUpdateDTO, Integer id) {
		LOGGER.info("Going to update SocVendor with id: " + id);
		SocVendor socVendor = socVendorRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.SOCVENDOR_ID, id.toString()));
		if (!Utils.isEmpty(socVendorUpdateDTO.getSocVendorName())) {
			if (socVendorRepository.existsByName(socVendorUpdateDTO.getSocVendorName())) {
				LOGGER.info("Soc vendor already exists with the same name: " + socVendorUpdateDTO.getSocVendorName());
				throw new ResourceAlreadyExistsException(Constants.SOCVENDOR_NAME,
						socVendorUpdateDTO.getSocVendorName());
			} else {
				socVendor.setName(socVendorUpdateDTO.getSocVendorName());
			}
		}

		if (socVendorUpdateDTO.getSocVendorCategory() != null) {
			socVendor.setCategory(Category.getCategory(socVendorUpdateDTO.getSocVendorCategory()));
		}
		try {
			socVendor = socVendorRepository.save(socVendor);
		} catch (Exception e) {
			LOGGER.error("Error while saving SocVendor: " + e.getMessage());
			throw new RuntimeException("Error occurred while updating SocVendor with id: " + id, e);
		}

		return MapperUtils.convertToSocVendorUpdateDTO(socVendor);

	}

	/**
	 * Retrieves all SOC vendors DTO by category.
	 *
	 * @param category the category of the SOC vendors to retrieve
	 * @return a list of all SOC vendors with the specified category
	 */

	@Override
	public List<SocVendorDTO> getSOCVendorsByCategory(String category) {
		LOGGER.info("Going to fetch soc vendors by category: " + category);
		Category categoryName = Category.getCategory(category);
		if (null == categoryName) {
			throw new ResourceNotFoundException(Constants.CATEGORY, category);
		}
		List<SocVendor> socVendors = socVendorRepository.findByCategory(categoryName);
		if (socVendors == null || socVendors.isEmpty()) {
			LOGGER.info("No soc vendors found with category: " + category);
			return null;
		}
		return socVendors.stream().map(MapperUtils::convertToSocVendorDTO).collect(Collectors.toList());
	}

	/**
	 * Retrieves all SOC vendors names by category.
	 *
	 * @param category the category of the SOC vendors to retrieve
	 * @return a list of all SOC vendors with the specified category
	 */

	@Override
	public List<String> getSOCVendorsListByCategory(String category) {
		LOGGER.info("Going to fetch soc vendors by category: " + category);
		Category categoryName = Category.getCategory(category);
		if (null == categoryName) {
			throw new ResourceNotFoundException(Constants.CATEGORY, category);
		}
		List<SocVendor> socVendors = socVendorRepository.findByCategory(categoryName);
		if (socVendors == null || socVendors.isEmpty()) {
			LOGGER.info("No soc vendors found with category: " + category);
			return null;
		}
		return socVendors.stream().map(SocVendor::getName).collect(Collectors.toList());
	}
}
