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

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.config.AppConfig;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.exception.TDKServiceException;
import com.rdkm.tdkservice.service.IRDKCertificationService;
import com.rdkm.tdkservice.util.Constants;

/**
 * Service class for RDK Certification
 */
@Service
public class RDKCertificationService implements IRDKCertificationService {

	private static final Logger LOGGER = LoggerFactory.getLogger(RDKCertificationService.class);

	@Autowired
	CommonService commonService;

	/**
	 * Method to create or update or upload a config file
	 * 
	 * @param file
	 * @return boolean
	 */
	@Override
	public boolean createOrUpdateOrUploadConfigFile(MultipartFile file) {
		LOGGER.info("Inside createOrUpdateConfigFile method with fileName: {}", file.getOriginalFilename());
		commonService.validatePythonFile(file);
		try {

			MultipartFile fileWithHeader = commonService.addHeader(file);
			Path uploadPath = Paths.get(AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
					+ Constants.RDK_CERTIFICATION_CONFIG_PATH + Constants.FILE_PATH_SEPERATOR);
			if (!Files.exists(uploadPath)) {
				Files.createDirectories(uploadPath);
			}
			Path filePath = uploadPath.resolve(fileWithHeader.getOriginalFilename());
			Files.copy(fileWithHeader.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
			LOGGER.info("File uploaded successfully: {}", fileWithHeader.getOriginalFilename());
			return true;
		} catch (IOException e) {
			LOGGER.error("Error saving file: " + e.getMessage());
			throw new TDKServiceException("Error saving file: " + e.getMessage());
		} catch (Exception ex) {
			LOGGER.error("Error saving file: ", ex.getMessage());
			throw new TDKServiceException("Error saving file: " + ex.getMessage());

		}
	}

	/**
	 * Method to download a config file
	 * 
	 * @param fileName
	 * @return Resource
	 */
	@Override
	public Resource downloadConfigFile(String fileName) {
		LOGGER.info("Inside downloadConfigFile method with configFileName: {}", fileName);
		String configFileLocation = AppConfig.getRealPath() + Constants.BASE_FILESTORE_DIR
				+ Constants.FILE_PATH_SEPERATOR + Constants.RDK_CERTIFICATION_CONFIG_PATH;
		Path path = Paths.get(configFileLocation).resolve(fileName + Constants.PYTHON_FILE_EXTENSION);
		if (!Files.exists(path)) {
			LOGGER.error("Python config file not found: {}", fileName);
			throw new ResourceNotFoundException("Python Config file",fileName);
		}
		Resource resource = null;
		try {
			resource = new UrlResource(path.toUri());
		} catch (MalformedURLException e) {
			LOGGER.error("Python config file not found: {}", fileName);
		}
		// Loads the resource and checks if it exists
		if (null != resource && !resource.exists()) {
			LOGGER.error("Python config file not found: {}", fileName);
			return null;
		}
		return resource;
	}

	/**
	 * Method to get all config file names
	 * 
	 * @return List<String>
	 */
	@Override
	public List<String> getAllConfigFileNames() {
		LOGGER.info("Inside getAllConfigFileNames method");
		List<String> configFileNames = new ArrayList<>();
		try {
			String filePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
					+ Constants.RDK_CERTIFICATION_CONFIG_PATH;
			File folder = new File(filePath);
			File[] listOfFiles = folder.listFiles();
			if (listOfFiles != null) {
				for (File file : listOfFiles) {
					if (file.isFile()) {
						configFileNames.add(file.getName().replace(Constants.PYTHON_FILE_EXTENSION, ""));
					}
				}
			}
		} catch (Exception e) {
			LOGGER.error("Error in getting config file names: " + e.getMessage());
			throw new TDKServiceException("Error in getting config file names: " + e.getMessage());
		}
		return configFileNames;
	}

	/**
	 * Method to get the content of the config file
	 * 
	 * @param fileName
	 * @return String
	 * 
	 */
	@Override
	public String getConfigFileContent(String fileName) {
		LOGGER.info("Inside getConfigFileContent method with fileName: {}", fileName);
		String fileContent = "";
		try {
			String filePath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
					+ Constants.RDK_CERTIFICATION_CONFIG_PATH + Constants.FILE_PATH_SEPERATOR + fileName
					+ Constants.PYTHON_FILE_EXTENSION;
			File file = new File(filePath);
			if (file.exists()) {
				fileContent = new String(Files.readAllBytes(file.toPath()));

			}
		} catch (Exception e) {
			LOGGER.error("Error in getting config file content: " + e.getMessage());
			throw new TDKServiceException("Error in getting config file content: " + e.getMessage());
		}
		return fileContent;
	}
}
