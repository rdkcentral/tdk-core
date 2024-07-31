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

import java.util.List;

import com.rdkm.tdkservice.dto.ScriptTagCreateDTO;
import com.rdkm.tdkservice.dto.ScriptTagDTO;

import jakarta.validation.Valid;

/**
 * The script tag service.
 */
public interface IScriptTagService {

	/**
	 * Create the script tag.
	 * 
	 * @param scriptTagRequest
	 * @return
	 * 
	 */
	boolean createScriptTag(@Valid ScriptTagCreateDTO scriptTagRequest);

	/**
	 * Update the script tag.
	 * 
	 * @param scriptTagRequest
	 * @return
	 * 
	 */
	boolean updateScriptTag(ScriptTagDTO scriptTagRequest);

	/**
	 * Delete the script tag.
	 * 
	 * @param scriptTagRequest
	 * @return
	 * 
	 */
	void deleteScriptTag(Integer scriptTagRequest);

	/**
	 * Find all the script tag.
	 * 
	 * @return
	 * 
	 */
	List<ScriptTagDTO> findAllScriptTag();

	/**
	 * Find all the script tag by category.
	 * 
	 * @param category
	 * @return
	 * 
	 */
	List<ScriptTagDTO> findAllScriptTagByCategory(String category);

	/**
	 * Find all the script tag by category.
	 * 
	 * @param category
	 * @return
	 * 
	 */
	List<String> getListOfScriptTagByCategory(String category);

	/**
	 * Find the script tag by id.
	 * 
	 * @param id
	 * @return
	 * 
	 */
	ScriptTagDTO findById(Integer id);

}
