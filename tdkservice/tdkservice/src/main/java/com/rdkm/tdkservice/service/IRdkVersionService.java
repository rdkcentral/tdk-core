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

import com.rdkm.tdkservice.dto.RdkVersionCreateDTO;
import com.rdkm.tdkservice.dto.RdkVersionDTO;

import jakarta.validation.Valid;

/**
 * The rdk version service.
 */
public interface IRdkVersionService {

	/**
	 * Create the rdk version.
	 * 
	 * @param rdkVersionCreateDTO
	 * @return
	 * 
	 */
	boolean createRdkVersion(@Valid RdkVersionCreateDTO rdkVersionCreateDTO);

	/**
	 * Update the rdk version.
	 * 
	 * @param rdkVersionDTO
	 * @return
	 *
	 */
	boolean updateRdkVersion(RdkVersionDTO rdkVersionDTO);

	/**
	 * Delete the rdk version.
	 * 
	 * @param id
	 * @return
	 * 
	 */
	void deleteRdkVersion(Integer id);

	/**
	 * Find the rdk version by id.
	 * 
	 * @param id
	 * @return
	 * 
	 */
	RdkVersionDTO findRdkVersionById(Integer id);

	/**
	 * Find the rdk version by name.
	 * 
	 * @param buildVersionName
	 * @return
	 * 
	 */
	List<String> getRdkVersionListByCategory(String category);

	/**
	 * Find all the rdk versions list of name by category.
	 * 
	 * @param category
	 * @return
	 * 
	 */
	List<RdkVersionDTO> findAllRdkVersionsByCategory(String category);

	/**
	 * Find all the rdk versions.
	 * 
	 * @return
	 * 
	 */
	List<RdkVersionDTO> findAllRdkVersions();

}
