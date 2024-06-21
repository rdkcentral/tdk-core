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

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * This is the DTO class for download device configuration request
 * 
 */
@Data
public class DeviceConfigDownloadDTO {

	/**
	 * Box name for which the device configuration is to be downloaded
	 */
	@NotBlank(message = "Box name is required")
	private String boxName;

	/**
	 * Box type for which the device configuration is to be downloaded
	 */
	@NotBlank(message = "Box Type is required")
	private String boxType;

}
