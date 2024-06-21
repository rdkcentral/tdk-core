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
package com.rdkm.tdkservice.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.model.BoxManufacturer;

/**
 * The BoxManufacturerRepository interface provides methods for box manufacturer
 * operations.
 */

@Repository
public interface BoxManufacturerRepository extends JpaRepository<BoxManufacturer, Integer> {
	
	/**
	 * This method is used to find a box manufacturer by name.
	 *
	 * @param boxManufacturer the name of the box manufacturer to find
	 * @return a BoxManufacturer object containing the box manufacturer's
	 *         information
	 */
	BoxManufacturer findByName(String boxManufacturer);

	/**
	 * This method is used to delete a box manufacturer by name.
	 *
	 * @param name the name of the box manufacturer to delete
	 * @return a BoxManufacturer object containing the box manufacturer's
	 *         information
	 */
	BoxManufacturer deleteByName(String name);

	/**
	 * This method is used to check if a box manufacturer exists by name.
	 *
	 * @param name the name of the box manufacturer to check
	 * @return a boolean value indicating whether the box manufacturer exists
	 */
	boolean existsByName(String name);

	/**
	 * This method is used to find a list of box manufacturers by category.
	 *
	 * @param category the category of the box manufacturer to find
	 * @return a list of BoxManufacturer objects containing the box manufacturer's
	 *         information
	 */
	List<BoxManufacturer> findByCategory(Category category);

}
