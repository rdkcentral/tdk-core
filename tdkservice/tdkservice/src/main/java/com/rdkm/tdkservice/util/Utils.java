
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
package com.rdkm.tdkservice.util;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;

/**
 * This class is used to store the utility methods used in the application
 */
public class Utils {

	private static final Logger LOGGER = LoggerFactory.getLogger(Utils.class);

	/**
	 * This method is used to check if the string is empty or not
	 * 
	 * @param string
	 * @return boolean
	 */
	public static boolean isEmpty(final String string) {
		// Null-safe, short-circuit evaluation.
		return string == null || string.trim().isEmpty();
	}

	/**
	 * This method is used to check if the string is not empty
	 * 
	 * @param string
	 * @return boolean
	 */
	public static void checkCategoryValid(String category) {
		if (Category.getCategory(category) == null) {
			LOGGER.error("Invalid category: " + category);
			throw new ResourceNotFoundException(Constants.CATEGORY, category);
		}
	}

	/**
	 * This method is to convert list of strings to comma separated string
	 * 
	 * @param list - list of strings
	 * @return - comma separated string
	 */
	public static String convertListToCommaSeparatedString(List<String> list) {
		LOGGER.info("Inside convertListToCommaSeparatedString method with list");
		if (list == null || list.isEmpty()) {
			return null;
		}
		StringBuilder sb = new StringBuilder();
		for (String s : list) {
			sb.append(s);
			if (list.indexOf(s) == list.size() - 1)
				break;
			sb.append(",");
		}
		LOGGER.info("Converted string is" + sb.toString());
		return sb.toString();
	}
}
