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
package com.rdkm.tdkservice.serviceimpl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.enums.TestGroup;
import com.rdkm.tdkservice.util.Constants;

/**
 * This class is used to provide common services.
 */
@Service
public class CommonService {

	public static final Logger LOGGER = LoggerFactory.getLogger(CommonService.class);

	/**
	 * This method is used to get the folder name based on the module type.
	 * 
	 * @param testGroup
	 * @return
	 */
	public String getFolderBasedOnModuleType(TestGroup testGroup) {
		LOGGER.info("Inside getFolderBasedOnModuleType method with testGroup: {}", testGroup);
		String folderName = "";
		switch (testGroup) {
		case COMPONENT:
			folderName = "component";
			break;
		case CERTIFICATION:
			folderName = "certification";
			break;
		case E2E:
			folderName = "integration";
			break;
		default:
			LOGGER.error("Invalid test type: " + testGroup.getName());
		}
		return folderName;

	}

	/**
	 * This method is used to get the folder name based on the category.
	 * 
	 * @param category - RDKV, RDKB, RDKC
	 * @return folder name based on the category - RDKV, RDKB, RDKC
	 */
	public String getFolderBasedOnCategory(Category category) {
		String folderName = "";
		switch (category) {
		case RDKV:
			folderName = Constants.RDKV_FOLDER_NAME;
			break;
		case RDKV_RDKSERVICE:
			folderName = Constants.RDKV_FOLDER_NAME;
			break;
		case RDKB:
			folderName = Constants.RDKB_FOLDER_NAME;
			break;
		case RDKC:
			folderName = Constants.RDKC_FOLDER_NAME;
			break;
		default:
			LOGGER.error("Invalid category: " + category.getName());
		}
		return folderName;
	}

}
