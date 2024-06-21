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

import com.rdkm.tdkservice.enums.BoxTypeCategory;
import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.model.BoxType;

/**
 * The BoxTypeRepository interface provides methods for box type operations.
 */
@Repository
public interface BoxTypeRepository extends JpaRepository<BoxType, Integer> {
	/**
	 * This method is used to find a box type by name.
	 *
	 * @param boxtype the name of the box type to find
	 * @return a BoxType object containing the box type's information
	 */
	BoxType findByName(String boxtype);

	/**
	 * This method is used to delete a box type by name.
	 *
	 * @param name the name of the box type to delete
	 * @return a BoxType object containing the box type's information
	 */
	BoxType deleteByName(String name);

	/**
	 * This method is used to check if a box type exists by name.
	 *
	 * @param name the name of the box type to check
	 * @return a boolean value indicating whether the box type exists
	 */
	boolean existsByName(String name);

	/**
	 * This method is used to find a list of box types by category.
	 *
	 * @param category the category of the box type to find
	 * @return a list of BoxType objects containing the box type's information
	 */
	List<BoxType> findByCategory(Category category);

	/**
	 * This method is used to find a list of box types by type.
	 *
	 * @param type the type of the box type to find
	 * @return a list of BoxType objects containing the box type's information
	 */
	List<BoxType> findByType(BoxTypeCategory type);

}
