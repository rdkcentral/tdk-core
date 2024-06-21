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

import com.rdkm.tdkservice.dto.BoxManufacturerDTO;
import com.rdkm.tdkservice.dto.BoxManufacturerUpdateDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.BoxManufacturer;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.BoxManufacturerRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.service.IBoxManufacturerService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;

/**
 * This class provides the implementation for the BoxManufacturerService
 * interface. It provides methods to perform CRUD operations on BoxManufacturer
 * entities.
 */

@Service
public class BoxManufacturerService implements IBoxManufacturerService {

	private static final Logger LOGGER = LoggerFactory.getLogger(BoxManufacturerService.class);

	@Autowired
	BoxManufacturerRepository boxManufacturerRepository;

	@Autowired
	UserGroupRepository userGroupRepository;

	/**
	 * This method is used to create a new BoxManufacturer.
	 * 
	 * @param boxManufacturerRequest This is the request object containing the
	 *                               details of the BoxManufacturer to be created.
	 * @return boolean This returns true if the BoxManufacturer was created
	 *         successfully, false otherwise.
	 */
	@Override
	public boolean createBoxManufacturer(BoxManufacturerDTO boxManufacturerDTO) {
		LOGGER.info("Going to create BoxManufacturer with name: " + boxManufacturerDTO.toString());

		if (boxManufacturerRepository.existsByName(boxManufacturerDTO.getBoxManufacturerName())) {
			LOGGER.info("Box manufacturer already exists with the same name: "
					+ boxManufacturerDTO.getBoxManufacturerName());
			throw new ResourceAlreadyExistsException(Constants.BOXMANUFACTURER_NAME,
					boxManufacturerDTO.getBoxManufacturerName());
		}
		BoxManufacturer boxManufacturer = new BoxManufacturer();
		boxManufacturer.setName(boxManufacturerDTO.getBoxManufacturerName());
		Category category = Category.getCategory(boxManufacturerDTO.getBoxManufacturerCategory());
		if (category != null) {
			boxManufacturer.setCategory(category);
		} else {
			LOGGER.info("Invalid category: " + boxManufacturerDTO.getBoxManufacturerCategory());
			throw new ResourceNotFoundException(Constants.CATEGORY, boxManufacturerDTO.getBoxManufacturerCategory());
		}
		UserGroup userGroup = userGroupRepository.findByName(boxManufacturerDTO.getBoxManufacturerUserGroup());
		boxManufacturer.setUserGroup(userGroup);

		try {
			boxManufacturer = boxManufacturerRepository.save(boxManufacturer);
		} catch (Exception e) {
			LOGGER.error("Error occurred while creating BoxManufacturer", e);
			return false;
		}

		return boxManufacturer != null && boxManufacturer.getId() > 0;

	}

	/**
	 * This method is used to retrieve all BoxManufacturers.
	 * 
	 * @return List<BoxManufacturerRequest> This returns a list of all
	 *         BoxManufacturers.
	 */
	@Override
	public List<BoxManufacturerDTO> getAllBoxManufacturer() {
		LOGGER.info("Going to get all box manufacturers");
		List<BoxManufacturer> boxManufacturers = boxManufacturerRepository.findAll();
		if (boxManufacturers.isEmpty() || boxManufacturers == null) {
			return null;
		}
		return boxManufacturers.stream().map(MapperUtils::convertToBoxManufacturerDTO).collect(Collectors.toList());

	}

	/**
	 * This method is used to delete a BoxManufacturer by its id.
	 * 
	 * @param id This is the id of the BoxManufacturer to be deleted.
	 */
	@Override
	public void deleteBoxManufacturer(Integer id) {
		if (!boxManufacturerRepository.existsById(id)) {
			LOGGER.info("No BoxManufacturer found with id: " + id);
			throw new ResourceNotFoundException(Constants.BOXMANUFACTURER_ID, id.toString());
		}
		try {
			boxManufacturerRepository.deleteById(id);
		} catch (DataIntegrityViolationException e) {
			LOGGER.error("Error occurred while deleting BoxManufacturer with id: " + id, e);
			throw new DeleteFailedException();
		}
	}

	/**
	 * This method is used to find a BoxManufacturer by its id.
	 * 
	 * @param id This is the id of the BoxManufacturer to be found.
	 * @return BoxManufacturerRequest This returns the found BoxManufacturer.
	 */
	@Override
	public BoxManufacturerDTO findById(Integer id) {
		LOGGER.info("Going to find BoxManufacturer with id: " + id);
		BoxManufacturer boxManufacturer = boxManufacturerRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.BOXMANUFACTURER_ID, id.toString()));
		return MapperUtils.convertToBoxManufacturerDTO(boxManufacturer);

	}

	/**
	 * This method is used to update a BoxManufacturer.
	 * 
	 * @param boxManufacturerRequest This is the request object containing the
	 *                               updated details of the BoxManufacturer.
	 * @param id                     This is the id of the BoxManufacturer to be
	 *                               updated.
	 * @return BoxManufacturerRequest This returns the updated BoxManufacturer.
	 */
	@Override
	public BoxManufacturerUpdateDTO updateBoxManufacturer(BoxManufacturerUpdateDTO boxManufacturerUpdateRequest,
			Integer id) {
		LOGGER.info("Going to update BoxManufacturer with id: " + id);

		BoxManufacturer boxManufacturer = boxManufacturerRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.BOXMANUFACTURER_ID, id.toString()));
		if (!Utils.isEmpty(boxManufacturerUpdateRequest.getBoxManufacturerName())) {
			if (boxManufacturerRepository.existsByName(boxManufacturerUpdateRequest.getBoxManufacturerName())) {
				LOGGER.info("Box manufacturer already exists with the same name: "
						+ boxManufacturerUpdateRequest.getBoxManufacturerName());
				throw new ResourceAlreadyExistsException(Constants.BOXMANUFACTURER_NAME,
						boxManufacturerUpdateRequest.getBoxManufacturerName());
			} else {
				boxManufacturer.setName(boxManufacturerUpdateRequest.getBoxManufacturerName());
			}
		}

		if (!Utils.isEmpty(boxManufacturerUpdateRequest.getBoxManufacturerCategory())) {
			boxManufacturer
					.setCategory(Category.getCategory(boxManufacturerUpdateRequest.getBoxManufacturerCategory()));
		}

		try {
			boxManufacturer = boxManufacturerRepository.save(boxManufacturer);
		} catch (Exception e) {
			LOGGER.error("Error occurred while updating BoxManufacturer with id: " + id, e);
		}
		LOGGER.info("BoxManufacturer updated successfully with id: " + id);

		return MapperUtils.convertToBoxManufacturerUpdateDTO(boxManufacturer);

	}

	/**
	 * This method is used to retrieve all BoxManufacturers DTO by category.
	 * 
	 * @param category This is the category of the BoxManufacturers to be retrieved.
	 * @return List<BoxManufacturerRequest> This returns a list of BoxManufacturers.
	 */

	@Override
	public List<BoxManufacturerDTO> getBoxManufacturersByCategory(String category) {
		LOGGER.info("Going to get all box manufacturers by category: " + category);
		List<BoxManufacturer> boxManufacturers = boxManufacturerRepository
				.findByCategory(Category.getCategory(category));
		if (boxManufacturers.isEmpty() || boxManufacturers == null) {
			return null;
		}
		return boxManufacturers.stream().map(MapperUtils::convertToBoxManufacturerDTO).collect(Collectors.toList());
	}

	/**
	 * This method is used to retrieve all BoxManufacturers names list by category.
	 * 
	 * @param category This is the category of the BoxManufacturers to be retrieved.
	 * @return List<String> This returns a list of BoxManufacturers.
	 */

	@Override
	public List<String> getBoxManufacturerListByCategory(String category) {
		LOGGER.info("Going to get all box manufacturers by category: " + category);
		List<BoxManufacturer> boxManufacturers = boxManufacturerRepository
				.findByCategory(Category.getCategory(category));
		if (boxManufacturers.isEmpty() || boxManufacturers == null) {
			return null;
		}
		return boxManufacturers.stream().map(BoxManufacturer::getName).collect(Collectors.toList());
	}

}
