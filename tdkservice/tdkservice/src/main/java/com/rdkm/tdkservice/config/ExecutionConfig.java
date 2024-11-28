
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
package com.rdkm.tdkservice.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

import com.rdkm.tdkservice.util.Utils;

/**
 * This configuration class is designed to read the properties from the
 * execution.properties file and store them in the variables.
 */

@Configuration
@PropertySource("classpath:execution.properties")
public class ExecutionConfig {

	@Value("${ipv4.interface}")
	private String ipv4Interface;

	@Value("${ipv6.interface}")
	private String ipv6Interface;

	@Value("${python.command}")
	private String pythonCommand;

	@Value("${execution.log.base.path}")
	private String executionLogBasePath;

	public String getIPV4Interface() {
		return ipv4Interface;
	}

	public String getIPV6Interface() {
		return ipv6Interface;
	}

	public String getPythonCommand() {
		if (Utils.isEmpty(pythonCommand)) {
			return "python";
		}
		return pythonCommand;
	}

	public String getExecutionLogBasePath() {
		return executionLogBasePath;
	}

}
