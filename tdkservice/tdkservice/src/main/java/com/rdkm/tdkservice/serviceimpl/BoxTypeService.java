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
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;

import com.rdkm.tdkservice.dto.BoxTypeDTO;
import com.rdkm.tdkservice.dto.BoxTypeUpdateDTO;
import com.rdkm.tdkservice.enums.BoxTypeCategory;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.BoxType;
import com.rdkm.tdkservice.model.BoxtypeSubBoxtypeMap;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.BoxTypeRepository;
import com.rdkm.tdkservice.repository.BoxtypeSubBoxtypeMapRepository;
import com.rdkm.tdkservice.repository.DeviceRepositroy;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.service.IBoxTypeService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;

/**
 * This class provides the implementation for the BoxTypeService interface. It
 * provides methods to perform CRUD operations on BoxType entities.
 */
@Service
public class BoxTypeService implements IBoxTypeService {

	private static final Logger LOGGER = LoggerFactory.getLogger(BoxTypeService.class);

	@Autowired
	BoxTypeRepository boxTypeRepository;

	@Autowired
	DeviceRepositroy deviceRepository;

	@Autowired
	BoxtypeSubBoxtypeMapRepository boxtypeSubBoxtypeMapRepository;

	@Autowired
	UserGroupRepository userGroupRepository;

	/**
	 * This method is used to create a new BoxType.
	 * 
	 * @param boxTypeDTO This is the request object containing the details of the
	 *                   BoxType to be created.
	 * @return boolean This returns true if the BoxType was created successfully,
	 *         false otherwise.
	 */
	@Override
	public boolean createBoxType(BoxTypeDTO boxTypeDTO) {
		LOGGER.info("Going to create Boxtype");
		if (boxTypeRepository.existsByName(boxTypeDTO.getBoxTypeName())) {
			LOGGER.error("Box type already exists with the same name: " + boxTypeDTO.getBoxTypeName());
			throw new ResourceAlreadyExistsException(Constants.BOX_TYPE, boxTypeDTO.getBoxTypeName());
		}

		BoxType boxType = new BoxType();
		boxType.setName(boxTypeDTO.getBoxTypeName());

		BoxTypeCategory boxTypeCategory = BoxTypeCategory.getBoxTypeCategory(boxTypeDTO.getType());
		if (null == boxTypeCategory) {
			throw new ResourceNotFoundException(Constants.BOX_TYPE_TYPE, boxTypeDTO.getType());
		} else {
			boxType.setType(boxTypeCategory);
		}

		Category category = Category.getCategory(boxTypeDTO.getBoxCategory());
		if (null == category) {
			throw new ResourceNotFoundException(Constants.CATEGORY, boxTypeDTO.getBoxCategory());
		} else {
			boxType.setCategory(category);
		}

		UserGroup userGroup = userGroupRepository.findByName(boxTypeDTO.getBoxUserGroup());
		boxType.setUserGroup(userGroup);

		try {
			boxType = boxTypeRepository.save(boxType);
			List<String> subBoxTypeNameList = boxTypeDTO.getSubBoxTypes();
			if (subBoxTypeNameList != null && !subBoxTypeNameList.isEmpty()) {
				for (String subBoxTypeName : subBoxTypeNameList) {
					BoxtypeSubBoxtypeMap boxtypeSubBoxtypeMap = new BoxtypeSubBoxtypeMap();
					BoxType subBoxType = boxTypeRepository.findByName(subBoxTypeName);
					if (null != subBoxType) {
						boxtypeSubBoxtypeMap.setBoxTypeName(boxTypeDTO.getBoxTypeName());
						boxtypeSubBoxtypeMap.setSubBoxType(subBoxType);
						boxtypeSubBoxtypeMapRepository.save(boxtypeSubBoxtypeMap);
					} else {
						LOGGER.error("Sub Box type not found with name: " + subBoxTypeName);
					}
				}
			}

		} catch (Exception e) {
			LOGGER.error("Error occurred while creating BoxType", e);
			return false;
		}
		LOGGER.info("Boxtype creation completed");
		return boxType != null && boxType.getId() > 0;
	}

	/**
	 * This method is used to retrieve all BoxTypes.
	 * 
	 * @return List<BoxTypeDTO> This returns a list of all BoxTypes.
	 */
	@Override
	public List<BoxTypeDTO> getAllBoxTypes() {
		LOGGER.info("Going to fetch all box types");
		List<BoxType> boxTypes = boxTypeRepository.findAll();
		if (boxTypes.isEmpty()) {
			return null;
		}
		return boxTypes.stream().map(this::convertToBoxTypeDTO).collect(Collectors.toList());
	}

	/**
	 * This method is used to delete a BoxType by its id.
	 * 
	 * @param id This is the id of the BoxType to be deleted.
	 */
	@Override
	public void deleteById(Integer id) {
		BoxType boxType = boxTypeRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.BOX_TYPE_ID, id.toString()));
		String boxTypeName = boxType.getName();
		try {
			this.deleteSubBoxTypes(boxTypeName);
			boxTypeRepository.deleteById(id);
		} catch (DataIntegrityViolationException e) {
			LOGGER.error("Error occurred while deleting Box with id: " + id, e);
			throw new DeleteFailedException();
		}

	}

	/**
	 * This method is used to find a BoxType by its id.
	 * 
	 * @param id This is the id of the BoxType to be found.
	 * @return BoxTypeRequest This returns the BoxType.
	 */
	@Override
	public BoxTypeDTO findById(Integer id) {
		LOGGER.info("Executing find BoxType by id method with id: " + id);
		BoxType boxType = boxTypeRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.BOX_TYPE_ID, id.toString()));
		BoxTypeDTO userDTO = null;
		try {
			userDTO = this.convertToBoxTypeDTO(boxType);
		} catch (Exception e) {
			LOGGER.error("Error occurred while fetching BoxType with id: " + id, e);
		}
		return userDTO;

	}

	/**
	 * This method is used to update a BoxType.
	 * 
	 * @param boxTypeDTO This is the request object containing the updated details
	 *                   of the BoxType.
	 * @param id         This is the id of the BoxType to be updated.
	 * @return BoxTypeRequest This returns the updated BoxType.
	 */
	@Override
	public BoxTypeDTO updateBoxType(BoxTypeUpdateDTO boxTypeUpdateDTO, Integer id) {
		BoxType boxType = boxTypeRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.BOX_TYPE_ID, id.toString()));
		if (!Utils.isEmpty(boxTypeUpdateDTO.getBoxTypeName())) {
			if (boxTypeRepository.existsByName(boxTypeUpdateDTO.getBoxTypeName())) {
				LOGGER.info("Box manufacturer already exists with the same name: " + boxTypeUpdateDTO.getBoxTypeName());
				throw new ResourceAlreadyExistsException(Constants.BOX_TYPE, boxTypeUpdateDTO.getBoxTypeName());
			} else {
				boxType.setName(boxTypeUpdateDTO.getBoxTypeName());
			}
		}

		if (boxTypeUpdateDTO.getBoxType() != null) {
			boxType.setType(BoxTypeCategory.getBoxTypeCategory(boxTypeUpdateDTO.getBoxType()));
		}
		if (boxTypeUpdateDTO.getBoxTypeCategory() != null) {
			boxType.setCategory(Category.getCategory(boxTypeUpdateDTO.getBoxTypeCategory()));
		}
		try {
			boxType = boxTypeRepository.save(boxType);
			List<String> subBoxTypeNameList = boxTypeUpdateDTO.getSubBoxTypes();

			if (subBoxTypeNameList != null && !subBoxTypeNameList.isEmpty()) {
				List<String> existingSubBoxTypeNameList = this.getSubBoxTypesForTheBoxType(boxType.getName());
				if (this.checkIfSubBoxTypesNeedUpdate(subBoxTypeNameList, existingSubBoxTypeNameList)) {
					// Delete all the existing sub box types
					this.deleteSubBoxTypes(boxType.getName());
					// Add the new sub box types
					for (String subBoxTypeName : subBoxTypeNameList) {
						BoxtypeSubBoxtypeMap boxtypeSubBoxtypeMap = new BoxtypeSubBoxtypeMap();
						BoxType subBoxType = boxTypeRepository.findByName(subBoxTypeName);
						if (null != subBoxType) {
							boxtypeSubBoxtypeMap.setBoxTypeName(boxTypeUpdateDTO.getBoxTypeName());
							boxtypeSubBoxtypeMap.setSubBoxType(subBoxType);
							boxtypeSubBoxtypeMapRepository.save(boxtypeSubBoxtypeMap);
						} else {
							LOGGER.info("Sub Box type not found with name: " + subBoxTypeName);
						}
					}
				}

			}

		} catch (Exception e) {
			LOGGER.error("Error occurred while updating BoxType", e);
			throw new RuntimeException("Error occurred while updating BoxType", e);
		}
		return MapperUtils.convertToBoxTypeDTO(boxType);

	}

	/**
	 * This method is used to retrieve all BoxTypes by category.
	 * 
	 * @param category This is the category of the BoxTypes to be retrieved.
	 * @return List<BoxTypeDTO> This returns a list of BoxTypes.
	 */

	@Override
	public List<BoxTypeDTO> getBoxTypesByCategory(String category) {
		LOGGER.info("Going to fetch box types by category: " + category);
		List<BoxType> boxTypes = boxTypeRepository.findByCategory(Category.getCategory(category));
		if (boxTypes.isEmpty()) {
			return null;
		}
		return boxTypes.stream().map(this::convertToBoxTypeDTO).collect(Collectors.toList());
	}

	/**
	 * This method is used to retrieve all BoxTypes by category.
	 * 
	 * @param category This is the category of the BoxTypes to be retrieved.
	 * @return List<String> This returns a list of BoxTypes.
	 */
	@Override
	public List<String> getBoxTypeNameByCategory(String category) {
		LOGGER.info("Going to fetch box type names by category: " + category);
		List<BoxType> boxTypes = boxTypeRepository.findByCategory(Category.getCategory(category));
		if (boxTypes.isEmpty()) {
			return null;
		}
		return boxTypes.stream().map(BoxType::getName).collect(Collectors.toList());
	}

	/**
	 * This method is used to convert BoxType to BoxTypeDTO.
	 * 
	 * @param boxType the box type to convert
	 * @return BoxTypeDTO the converted box type
	 */
	private BoxTypeDTO convertToBoxTypeDTO(BoxType boxType) {
		LOGGER.trace("Converting BoxType to BoxTypeDTO");
		BoxTypeDTO boxTypeDTO = MapperUtils.convertToBoxTypeDTO(boxType);
		List<BoxtypeSubBoxtypeMap> subboxTypeList = boxtypeSubBoxtypeMapRepository.findByBoxTypeName(boxType.getName());
		if (subboxTypeList != null && !subboxTypeList.isEmpty()) {
			List<String> subBoxTypeNames = subboxTypeList.stream().map(BoxtypeSubBoxtypeMap::getSubBoxType)
					.map(BoxType::getName).collect(Collectors.toList());
			boxTypeDTO.setSubBoxTypes(subBoxTypeNames);
		}
		return boxTypeDTO;

	}

	/**
	 * This method is used to delete sub box types.
	 * 
	 * @param boxTypeName the name of the box type
	 */
	private void deleteSubBoxTypes(String boxTypeName) {
		List<BoxtypeSubBoxtypeMap> subBoxTypeList = boxtypeSubBoxtypeMapRepository.findByBoxTypeName(boxTypeName);
		if (subBoxTypeList != null && !subBoxTypeList.isEmpty()) {
			for (BoxtypeSubBoxtypeMap subBoxType : subBoxTypeList) {
				boxtypeSubBoxtypeMapRepository.delete(subBoxType);
			}
		}
	}

	/**
	 * This method is used to get sub box types associated with a Boxtype.
	 * 
	 * @param boxTypeName the name of the box type
	 * @return List<String> the list of sub box types
	 */
	private List<String> getSubBoxTypesForTheBoxType(String boxTypeName) {
		List<BoxtypeSubBoxtypeMap> subBoxTypeList = boxtypeSubBoxtypeMapRepository.findByBoxTypeName(boxTypeName);
		if (subBoxTypeList != null && !subBoxTypeList.isEmpty()) {
			return subBoxTypeList.stream().map(BoxtypeSubBoxtypeMap::getSubBoxType).map(BoxType::getName)
					.collect(Collectors.toList());
		}
		return null;
	}

	/**
	 * This method is used to check if sub box types need to be updated.
	 * 
	 * @param subBoxTypeNameList
	 * @param existingSubBoxTypeNameList
	 * @return
	 */
	private boolean checkIfSubBoxTypesNeedUpdate(List<String> subBoxTypeNameList,
			List<String> existingSubBoxTypeNameList) {
		// Convert to ArrayList to sort the list
		if (existingSubBoxTypeNameList == null) {
			return true;
		}
		List<String> subBoxTypeNameArrayList = new ArrayList<>(subBoxTypeNameList);
		List<String> existingSubBoxTypeNameArrayList = new ArrayList<>(existingSubBoxTypeNameList);

		// Sort the lists
		Collections.sort(subBoxTypeNameArrayList);
		Collections.sort(existingSubBoxTypeNameArrayList);

		// Check if the lists are equal
		boolean areListsEqual = subBoxTypeNameList.equals(existingSubBoxTypeNameList);
		return !areListsEqual;
	}

	/**
	 * This method is used to check if the box type is a gateway.
	 * 
	 * @param boxType This is the box type to be checked.
	 * @return boolean This returns true if the box type is a gateway, false
	 *         otherwise.
	 */

	@Override
	public boolean isTheBoxTypeGateway(String boxType) {
		LOGGER.info("Checking if the box type is gateway: " + boxType);
		boolean isGateway = false;
		BoxType boxTypeDetails = boxTypeRepository.findByName(boxType);
		if (boxTypeDetails == null) {
			throw new ResourceNotFoundException(Constants.BOX_TYPE, boxType);
		}
		if (boxTypeDetails.getType() == BoxTypeCategory.GATEWAY || boxTypeDetails.getType() == BoxTypeCategory.STAND_ALONE_CLIENT) {
			isGateway = true;
		}
		return isGateway;

	}

}
