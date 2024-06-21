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

import com.rdkm.tdkservice.dto.BoxManufacturerDTO;
import com.rdkm.tdkservice.dto.BoxManufacturerUpdateDTO;

/**
 * This is the IBoxManufacturerService interface and contains the methods
 * related to BoxManufacturer.
 * 
 */

public interface IBoxManufacturerService {

	/**
	 * This method is used to create a new BoxManufacturer.
	 * 
	 * @param boxManufacturerRequest This is the request object containing the
	 *                               details of the BoxManufacturer to be created.
	 * @return boolean This returns true if the BoxManufacturer was created
	 *         successfully, false otherwise.
	 */

	boolean createBoxManufacturer(BoxManufacturerDTO boxManufacturerRequest);

	/**
	 * This method is used to retrieve all BoxManufacturers.
	 * 
	 * @return List<BoxManufacturerRequest> This returns a list of all
	 *         BoxManufacturers.
	 */

	List<BoxManufacturerDTO> getAllBoxManufacturer();

	/**
	 * This method is used to delete a BoxManufacturer by its id.
	 * 
	 * @param id This is the id of the BoxManufacturer to be deleted.
	 */

	void deleteBoxManufacturer(Integer id);

	/**
	 * This method is used to find a BoxManufacturer by its id.
	 * 
	 * @param id This is the id of the BoxManufacturer to be found.
	 * @return BoxManufacturerRequest This returns the found BoxManufacturer.
	 */

	BoxManufacturerDTO findById(Integer id);

	/**
	 * This method is used to update a BoxManufacturer.
	 * 
	 * @param boxManufacturerRequest This is the request object containing the
	 *                               updated details of the BoxManufacturer.
	 * @param id                     This is the id of the BoxManufacturer to be
	 *                               updated.
	 * @return BoxManufacturerRequest This returns the updated BoxManufacturer.
	 */

	BoxManufacturerUpdateDTO updateBoxManufacturer(BoxManufacturerUpdateDTO boxManufacturerRequest, Integer id);

	/**
	 * This method is used to retrieve all BoxManufacturers by category.
	 * 
	 * @param category This is the category of the BoxManufacturers to be retrieved.
	 * @return List<BoxManufacturerRequest> This returns a list of BoxManufacturers.
	 */
	List<BoxManufacturerDTO> getBoxManufacturersByCategory(String category);

	/**
	 * This method is used to retrieve all BoxManufacturers by category.
	 * 
	 * @param category This is the category of the BoxManufacturers to be retrieved.
	 * @return List<String> This returns a list of BoxManufacturers.
	 */
	List<String> getBoxManufacturerListByCategory(String category);

}
