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

package com.rdkm.tdkservice.service;

import java.io.ByteArrayInputStream;
import java.util.List;

import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.dto.ScriptCreateDTO;
import com.rdkm.tdkservice.dto.ScriptDTO;
import com.rdkm.tdkservice.dto.ScriptListDTO;
import com.rdkm.tdkservice.dto.ScriptModuleDTO;

/**
 * Service for scripts.
 */
public interface IScriptService {

	/**
	 * This method is used to save the script.
	 * 
	 * @param scriptFile      - the script file
	 * @param scriptCreateDTO - the script create dto
	 * @return boolean - true if the script is saved successfully, false otherwise
	 */
	boolean saveScript(MultipartFile scriptFile, ScriptCreateDTO scriptCreateDTO);

	/**
	 * This method is used to update the script.
	 * 
	 * @param scriptFile      - the script file
	 * @param scriptUpdateDTO - the script update dto
	 * @return - true if the script is updated successfully, false otherwise
	 */
	boolean updateScript(MultipartFile scriptFile, ScriptDTO scriptUpdateDTO);

	/**
	 * This method is used to delete the script.
	 * 
	 * @param scriptId - the script
	 * @return - true if the script is deleted successfully, false otherwise
	 */
	boolean deleteScript(Integer scriptId);

	/**
	 * This method is used to get the list of scripts based on the module.
	 * 
	 * @param moduleName - the module name
	 * @return - the list of scripts based on the module
	 */
	List<ScriptListDTO> findAllScriptsByModule(String moduleName);

	/**
	 * This method is used to get all the scripts based on the module by the
	 * category
	 * 
	 * @param category - the category
	 * @return - the list of scripts for all the modules by the given category
	 */
	List<ScriptModuleDTO> findAllScriptByModuleWithCategory(String category);

	/**
	 * This method is used to get the script details by module.
	 * 
	 * @param moduleName - the module name
	 * @return - the script
	 */
	ByteArrayInputStream testCaseToExcelByModule(String moduleName);

	/**
	 * This method is used to get the script details by testScriptName.
	 * 
	 * @param moduleName - the module name
	 * @return - the script
	 */
	ByteArrayInputStream testCaseToExcel(String testScriptName);

	/**
	 * This method is used to get the script details by testscriptId.
	 * 
	 * @param scriptId - the script id
	 * @return - the script
	 */
	ScriptDTO findScriptById(Integer scriptId);

}
