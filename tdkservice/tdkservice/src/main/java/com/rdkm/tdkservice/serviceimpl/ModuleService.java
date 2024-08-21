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

import com.rdkm.tdkservice.dto.ModuleCreateDTO;
import com.rdkm.tdkservice.dto.ModuleDTO;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.enums.TestGroup;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.Function;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.model.Parameter;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.FunctionRepository;
import com.rdkm.tdkservice.repository.ModuleRepository;
import com.rdkm.tdkservice.repository.ParameterRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.service.IModuleService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;


/**
 * Service implementation for managing module details.
 */
@Service
public class ModuleService implements IModuleService {

	@Autowired
	private ModuleRepository moduleRepository;

	@Autowired
	private UserGroupRepository userGroupRepository;

	@Autowired
	private FunctionRepository functionRepository;

	@Autowired
	private ParameterRepository parameterRepository;

	private static final Logger LOGGER = LoggerFactory.getLogger(ModuleService.class);

	/**
	 * Saves a new module.
	 *
	 * @param moduleDTO the data transfer object containing the module details
	 * @return true if the module was saved successfully, false otherwise
	 */
	@Override
	public boolean saveModule(ModuleCreateDTO moduleDTO) {
		if (moduleRepository.existsByName(moduleDTO.getModuleName())) {
			LOGGER.error("Module with name {} already exists", moduleDTO.getModuleName());
			throw new ResourceAlreadyExistsException(Constants.MODULE_NAME, moduleDTO.getModuleName());
		}
		UserGroup userGroup = userGroupRepository.findByName(moduleDTO.getUserGroup().toString());
		LOGGER.info("UserGroup found: {}", userGroup);

		Module module = MapperUtils.toModuleEntity(moduleDTO, userGroup);
		Category category = Category.getCategory(moduleDTO.getModuleCategory());
		if (null == category) {
			throw new ResourceNotFoundException(Constants.CATEGORY, moduleDTO.getModuleCategory());
		} else {
			module.setCategory(category);
		}
		try {
			moduleRepository.save(module);
		} catch (Exception e) {
			LOGGER.error("Error saving module: {}", e.getMessage());
			return false;
		}

        return module != null && module.getId() != null && module.getId() > 0;

	}

	/**
	 * Updates an existing module.
	 *
     * @param moduleDTO the data transfer object containing the updated module details
	 * @return true if the module was updated successfully, false otherwise
	 */
	@Override
	public boolean updateModule(ModuleDTO moduleDTO) {
		Module existingModule = moduleRepository.findById(moduleDTO.getId()).orElse(null);
		if (existingModule == null) {
			LOGGER.error("Module with ID {} not found", moduleDTO.getId());
			throw new ResourceNotFoundException(Constants.MODULE_NAME, moduleDTO.getId().toString());
		}
		if (!Utils.isEmpty(moduleDTO.getModuleName())
				&& !(moduleDTO.getModuleName().equals(existingModule.getName()))) {
			if (moduleRepository.existsByName(moduleDTO.getModuleName())) {
				LOGGER.info("Module already exists with the same name: " + moduleDTO.getModuleName());
				throw new ResourceAlreadyExistsException(Constants.MODULE_NAME, moduleDTO.getModuleName());
			} else {
				existingModule.setName(moduleDTO.getModuleName());
			}
		}
		MapperUtils.updateModuleProperties(existingModule, moduleDTO);
		try {
			moduleRepository.save(existingModule);
			return true;
		} catch (Exception e) {
			LOGGER.error("Failed to update module: {}", e.getMessage());
			return false;
		}
	}

	/**
	 * Finds all modules.
	 *
	 * @return a list of data transfer objects containing the details of all modules
	 */
	@Override
	public List<ModuleDTO> findAllModules() {
		LOGGER.info("Going to fetch all modules");
		List<Module> modules;
		try {
			modules = moduleRepository.findAll();
		} catch (Exception e) {
			LOGGER.error("Error occurred while fetching all modules", e);
			return Collections.emptyList();
		}
		if (modules.isEmpty()) {
			return Collections.emptyList();
		}
		return modules.stream().map(MapperUtils::convertToModuleDTO).collect(Collectors.toList());
	}

	/**
	 * Finds a module by its ID.
	 *
	 * @param id the ID of the module
     * @return the data transfer object containing the details of the module, or null if not found
	 */
	@Override
	public ModuleDTO findModuleById(Integer id) {
		LOGGER.info("Going to fetch module with ID: {}", id);
		if (!moduleRepository.existsById(id)) {
			LOGGER.error("Module with ID {} not found", id);
			throw new ResourceNotFoundException("Module id :: ", id.toString());
		}
		Module module = moduleRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException("Module not found for this id :: ", id.toString()));
		return MapperUtils.convertToModuleDTO(module);
	}

	/**
	 * Finds all modules by category.
	 *
	 * @param category the category of the module
	 * @return a list of data transfer objects containing the details of all modules
	 */
	@Override
	public List<ModuleDTO> findAllByCategory(String category) {
		LOGGER.info("Going to fetch all modules by category: {}", category);
		List<Module> modules = moduleRepository.findAllByCategory(Category.valueOf(category));
		Utils.checkCategoryValid(category);
		if (modules.isEmpty()) {
			return Collections.emptyList();
		}
		return modules.stream().map(MapperUtils::convertToModuleDTO).collect(Collectors.toList());
	}

	/**
	 * Deletes a module by its ID.
	 *
	 * @param id the ID of the module
	 * @return true if the module was deleted successfully, false otherwise
	 */

	@Override
	@Transactional
	public boolean deleteModule(Integer id) {
		LOGGER.info("Going to delete module with ID: {}", id);
		Module module = moduleRepository.findById(id).orElse(null);
		if (module == null) {
			LOGGER.error("Module with ID {} not found", id);
			throw new ResourceNotFoundException(Constants.MODULE_NAME, id.toString());
		}
		List<Function> functions = functionRepository.findAllByModuleId(id);
		LOGGER.info("Deleting functions for module ID: {}", id);
		for (Function function : functions) {
			LOGGER.info("Deleting function: {}", function);
			// Fetch parameters by function ID
			List<Parameter> parameters = parameterRepository.findAllByFunctionId(function.getId());
			for (Parameter parameter : parameters) {
				LOGGER.info("Deleting parameter with ID: {}", parameter.getId());
				parameterRepository.deleteById(parameter.getId());
			}
			LOGGER.info("Deleting function with ID: {}", function.getId());
			functionRepository.deleteById(function.getId());
		}
		try {
			moduleRepository.deleteById(id);
			LOGGER.info("Module deleted successfully: {}", id);
			return true;
		} catch (DeleteFailedException e) {
			LOGGER.error("Error deleting module: {}", e.getMessage());
			throw new DeleteFailedException();
		}
	}
	@Override
	public List<String> findAllTestGroupsFromEnum() {
		LOGGER.info("Fetching all test groups from enum");
        return Arrays.stream(TestGroup.values())
                .map(TestGroup::name)
                .collect(Collectors.toList());
	}

	/**
	 * Finds all modules names by category.
	 *
	 * @param category the category of the module
	 * @return a list of all modules names by category
	 */
	@Override
	public List<String> findAllModuleNameByCategory(String category) {
		LOGGER.info("Going to fetch all modules by category: {}", category);
		List<Module> modules = moduleRepository.findAllByCategory(Category.valueOf(category));
		Utils.checkCategoryValid(category);
		if (modules.isEmpty()) {
			return Collections.emptyList();
		}

		return modules.stream().map(Module::getName).collect(Collectors.toList());
	}
}