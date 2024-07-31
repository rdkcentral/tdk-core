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

import jakarta.validation.constraints.NotNull;
import lombok.Data;

/*
 * The RDk version DTO. This DTO is using for update ,find all operations
 */
@Data
public class RdkVersionDTO {

	/*
	 * The rdk version id.
	 */
	@NotNull(message = "Rdk version id cannot be null. As we are update operations and find all operation is done on the basis of Id.")
	private Integer rdkVersionId;

	/*
	 * The build version name.
	 */
	private String buildVersionName;

	/*
	 * The rdK version category
	 * 
	 */
	private String rdkVersionCategory;

	/*
	 * The rdk version user group.
	 */
	private String rdkVersionUserGroup;

}
