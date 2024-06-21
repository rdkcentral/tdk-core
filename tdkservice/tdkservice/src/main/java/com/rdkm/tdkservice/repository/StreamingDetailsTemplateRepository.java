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

import com.rdkm.tdkservice.model.StreamingDetailsTemplate;

/**
 * This interface is used to interact with the StreamingDetailsTemplate table in
 * the database.
 */
@Repository
public interface StreamingDetailsTemplateRepository extends JpaRepository<StreamingDetailsTemplate, Integer> {

	/*
	 * This method is used to find all streaming details templates.
	 */

	List<StreamingDetailsTemplate> findAll();

	/*
	 * This method is used to find a streaming details template by its template
	 * name.
	 * 
	 * @param templateName This is the template name of the streaming details
	 * template to be found.
	 * 
	 * @return List<StreamingDetailsTemplate> This returns the streaming details
	 * template with the given template name.
	 */
	List<StreamingDetailsTemplate> findByTemplateName(String templateName);

	/*
	 * This method is used to check if a streaming details template exists by its
	 * template name.
	 * 
	 * @param templateName This is the template name of the streaming details
	 * template to be checked.
	 * 
	 * @return boolean This returns true if the streaming details template exists by
	 * the given template name, else false.
	 */

	boolean existsByTemplateName(String templateName);

}
