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
package com.rdkm.tdkservice.dto;

import java.util.ArrayList;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

/**
 * The StreamingTemplateUpdateDTO class is used to map the request body of the
 * streaming template update request.
 */

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class StreamingTemplateUpdateDTO {

	/**
	 * Represents the existing template name of the StreamingTemplate.
	 */
	@NotBlank(message = "Existing template name is required")
	private String existingTemplateName;

	/**
	 * Represents the new template name of the StreamingTemplate
	 */
	private String newTemplateName;

	/*
	 * Represents the streaming maps of the StreamingTemplate
	 */
	@Valid
	@NotNull(message = "StreamingMaps cannot be null")
	private ArrayList<StreamingMap> streamingMaps;

	/**
	 * Represents the user group of the StreamingTemplate
	 */

	private String streamingTemplateUserGroup;

}
