package com.rdkm.tdkservice.service;

import com.rdkm.tdkservice.dto.ModuleCreateDTO;
import com.rdkm.tdkservice.dto.ModuleDTO;
import com.rdkm.tdkservice.model.Module;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Service interface for managing module details.
 */
public interface IModuleService {

	/**
	 * Saves a new module.
	 *
	 * @param moduleDTO the data transfer object containing the module details
	 * @return true if the module was saved successfully, false otherwise
	 */
	public boolean saveModule(ModuleCreateDTO moduleDTO);

	/**
	 * Updates an existing module.
	 *
     * @param moduleDTO the data transfer object containing the updated module details
	 * @return true if the module was updated successfully, false otherwise
	 */
	public boolean updateModule(ModuleDTO moduleDTO);

	/**
	 * Finds all modules.
	 *
	 * @return a list of data transfer objects containing the details of all modules
	 */
	public List<ModuleDTO> findAllModules();

	/**
	 * Finds a module by its ID.
	 *
	 * @param id the ID of the module
     * @return the data transfer object containing the details of the module, or null if not found
	 */
	public ModuleDTO findModuleById(Integer id);

	/**
	 * Finds a module by its category.
	 *
	 * @param category the category of the module
     * @return the data transfer object containing the details of the module, or null if not found
	 */
	public List<ModuleDTO> findAllByCategory(String category);

	/**
	 * Deletes a module by its ID.
	 *
	 * @param id the ID of the module
	 * @return true if the module was deleted successfully, false otherwise
	 */
	public boolean deleteModule(Integer id);

	/**
	 * Finds all test groups.
	 *
	 * @return a list of all test groups
	 */
	public List<String> findAllTestGroupsFromEnum();

	/**
	 * Finds all module names by category.
	 *
	 * @return a list of all module names
	 */
	public List<String> findAllModuleNameByCategory(String category);
}