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

import com.rdkm.tdkservice.model.Execution;
import com.rdkm.tdkservice.model.ExecutionResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

/**
 * Represents the execution result repository.
 */
@Repository
public interface ExecutionResultRepository extends JpaRepository<ExecutionResult, UUID> {

	/**
	 * Find the execution result by execution.
	 * 
	 * @param execution the execution
	 * @return the list of execution result
	 */
	List<ExecutionResult> findByExecution(Execution execution);
}
