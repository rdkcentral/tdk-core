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

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.service.IDeviceConfigService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.Utils;

/**
 * This class is used to provide the service to get the device configuration
 * file for a given box name or box type or default device configuration file
 * and to upload the device configuration file
 * 
 */
@Service
public class DeviceConfigService implements IDeviceConfigService {

	private static final Logger LOGGER = LoggerFactory.getLogger(DeviceConfigService.class);

	@Autowired
	private ResourceLoader resourceLoader;

	/**
	 * This method is used to get the device configuration file for a given box name
	 * or box type or default device configuration file.
	 * 
	 * @param boxName - the box name
	 * @param boxtype - the box type
	 * @return Resource - the device configuration file null - if the device config
	 *         file is not found
	 */
	@Override
	public Resource getDeviceConfigFile(String boxName, String boxtype) {
		LOGGER.info("Inside getDeviceConfigFile method with boxName: {}, boxtype: {}", boxName, boxtype);
		String configFile;
		// Get the device config file for the given box name
		Resource resource = null;
		if (!Utils.isEmpty(boxName)) {
			configFile = boxName + Constants.CONFIG_FILE_EXTENSION;
			resource = getDeviceConfigFileGivenName(configFile);
			if (resource != null) {
				return resource;
			}
		}

		// Get the device config file for the given box type of there is no config file
		// for the box name
		if (resource == null && !Utils.isEmpty(boxtype)) {
			configFile = boxtype + Constants.CONFIG_FILE_EXTENSION;
			resource = getDeviceConfigFileGivenName(configFile);
			if (resource != null) {
				return resource;
			}
		}

		// Get the default device config file if there is no config file for the box
		// name and box type
		if (resource == null) {
			configFile = Constants.DEFAULT_DEVICE_CONFIG_FILE;
			resource = getDeviceConfigFileGivenName(configFile);

		}
		return resource;

	}

	/**
	 * This method is used to upload the device configuration file
	 * 
	 * @param file - the device configuration file
	 * @return boolean - true if the device config file is uploaded successfully
	 *         false - if the device config file is not uploaded successfully
	 */
	public boolean uploadDeviceConfigFile(MultipartFile file) {
		LOGGER.info("Inside uploadDeviceConfigFile method with file: {}", file.getOriginalFilename());

		try {
			Path uploadPath = Paths.get(Constants.BASE_FILESTORE_DIR);
			if (!Files.exists(uploadPath)) {
				Files.createDirectories(uploadPath);
			}
			// Save the file to the path
			Path filePath = uploadPath.resolve(file.getOriginalFilename());

			Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
			LOGGER.info("File uploaded successfully: {}", file.getOriginalFilename());
			return true;
		} catch (IOException ex) {
			LOGGER.error("Upload device Config file failed due to this exception - {}", ex.getMessage());
			return false;
		} catch (Exception ex) {
			LOGGER.error("Upload device Config file failed due to this exception - {}", ex.getMessage());
			return false;
		}

	}

	/**
	 * This method is used to delete the device configuration file
	 * 
	 * @param fileName - the device configuration file name
	 * @return boolean - true if the device config file is deleted successfully
	 *                   false - if the device config file is not deleted
	 */
	@Override
	public boolean deleteDeviceConfigFile(String deviceConfigFileName) {
		LOGGER.info("Inside deleteDeviceConfigFile method with deviceConfigFileName: {}", deviceConfigFileName);
		Path filePath = Paths.get(Constants.BASE_FILESTORE_DIR + deviceConfigFileName);
		try {
			Files.delete(filePath);
			LOGGER.info("File deleted successfully: {}", deviceConfigFileName);
			return true;
		} catch (IOException ex) {
			LOGGER.error("Delete device Config file failed due to this exception - {}", ex.getMessage());
			return false;
		} catch (Exception ex) {
			LOGGER.error("Delete device Config file failed due to this exception - {}", ex.getMessage());
			return false;
		}
	}

	/**
	 * This method is used to get the device configuration file for a given config
	 * file name
	 * 
	 * @param configFileName - the config file name
	 * @return Resource - the device configuration file null - if the device config
	 *         file is not found
	 */
	private Resource getDeviceConfigFileGivenName(String configFileName) {
		LOGGER.info("Inside getDeviceConfigFileGivenName method with configFileName: {}", configFileName);
		String configFileLocation = Constants.FILESTORE_LOCATION + configFileName;
		Resource resource = resourceLoader.getResource(configFileLocation);

		if (!resource.exists()) {
			LOGGER.error("Device config file not found: {}", configFileName);
			return null;
		}
		return resource;
	}

}
