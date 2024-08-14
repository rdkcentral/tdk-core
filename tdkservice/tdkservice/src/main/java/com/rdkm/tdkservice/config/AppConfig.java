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

import org.springframework.context.annotation.Configuration;

import jakarta.annotation.PostConstruct;
import jakarta.servlet.ServletContext;

/**
 * This configuration class is designed to initialize and store the real path of
 * the servlet context in a static variable. The realPath is set once during the
 * initialization phase and can be accessed statically throughout the
 * application using the getRealPath method.
 */
@Configuration
public class AppConfig {

	// Static varible that stores the servlet context path
	private static String realPath;

	// Servlet context
	private final ServletContext servletContext;

	/**
	 * Constructor injection and it is injected as dependency
	 * 
	 * @param servletContext
	 */
	public AppConfig(ServletContext servletContext) {
		this.servletContext = servletContext;
	}

	/**
	 * The @PostConstruct annotation ensures the init method is called after the
	 * bean is constructed.
	 */
	@PostConstruct
	public void init() {
		realPath = servletContext.getRealPath("/");
	}

	/**
	 * The getRealPath method provides a static access point to the cached real
	 * path.
	 * 
	 * @return realpath - It will be the path to webapps folder in case of
	 *         development run and base directory in case of standalone deployment
	 *         in webservers
	 * 
	 */
	public static String getRealPath() {
		return realPath;
	}
}