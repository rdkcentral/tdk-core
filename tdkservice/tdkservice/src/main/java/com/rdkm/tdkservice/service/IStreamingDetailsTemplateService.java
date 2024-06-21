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

import com.rdkm.tdkservice.dto.StreamingDetailsTemplateDTO;
import com.rdkm.tdkservice.dto.StreamingTemplateUpdateDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsResponse;

/**
 * Interface for StreamingDetailsTemplateService
 */
public interface IStreamingDetailsTemplateService {

	/**
	 * Method to create streaming details template
	 * 
	 * @param templateDTO
	 * @return boolean
	 */

	boolean createStreamingDetailsTemplate(StreamingDetailsTemplateDTO templateDTO);

	/**
	 * Method to get streaming details by template name
	 * 
	 * @param templateName
	 * @return List<StreamingDetailsResponse>
	 */
	List<StreamingDetailsResponse> getStreamingDetailsByTemplateName(String templateName);

	/**
	 * Method to update streaming details template
	 * 
	 * @param templateDTO
	 * @return boolean
	 */
	boolean updateTemplate(StreamingTemplateUpdateDTO templateDTO);

	/**
	 * Method to get template list
	 * 
	 * @return List<String>
	 */
	List<String> getTemplateList();

	/**
	 * Method to delete template
	 * 
	 * @param templateName
	 * @return boolean
	 */

	boolean deleteTemplate(String templateName);

}
