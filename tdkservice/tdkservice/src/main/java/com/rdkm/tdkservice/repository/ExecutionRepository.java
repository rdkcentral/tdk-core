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

import java.sql.Date;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.model.Execution;
import com.rdkm.tdkservice.model.User;

/**
 * Repository class for Execution entity.
 */
@Repository
public interface ExecutionRepository extends JpaRepository<Execution, UUID> {

	/**
	 * This method is used to find the execution by name.
	 * 
	 * @param name
	 * 
	 */
	Execution findByName(String name);

	/**
	 * This method is used to check the existence of the execution by name.
	 * 
	 * @param executionName
	 */
	boolean existsByName(String executionName);

	/**
	 * This method is used to find the execution by name and category.
	 * 
	 * @param name
	 * @param category
	 */
	Page<Execution> findByCategory(Category category, Pageable pageable);

	/**
	 * This method is used to find the execution by device name
	 * 
	 * @param deviceName - name of the device
	 * @param pageable   - pageable object
	 * @return Pagination for execution
	 */
	@Query("SELECT ed.execution FROM ExecutionDevice ed WHERE ed.device.name LIKE %:deviceName%")
	Page<Execution> findByDeviceName(String deviceName, Pageable pageable);

	/**
	 * This method is used to search the execution by script test suite name and
	 * category.
	 * 
	 * @param scriptTestSuite - script test suite name or part of it
	 * @param category        - category of the execution
	 * @param pageable        - pageable object
	 * @return Pagination for execution
	 */
	Page<Execution> findByscripttestSuiteNameContainingAndCategory(String scriptTestSuite, Category category,
			Pageable pageable);

	/**
	 * This method is used to find the execution by user
	 * 
	 * @param user     - user object
	 * @param pageable - pageable object
	 * @return Pagination for execution
	 */
	Page<Execution> findByUserAndCategory(User user, Category category, Pageable pageable);

	/**
	 * This method is used to get execution list between date ranges
	 * 
	 * @param fromDate - start {@link Date}
	 * @param toDate   - end {@link Date}
	 */
	@Query("SELECT ex From  Execution ex WHERE ex.createdDate BETWEEN :fromDate AND :toDate")
	List<Execution> executionListInDateRange(Instant fromDate, Instant toDate);

}
