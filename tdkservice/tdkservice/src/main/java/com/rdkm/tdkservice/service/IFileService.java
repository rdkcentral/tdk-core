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

import org.springframework.core.io.Resource;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

/**
 * The IFileService interface is used to provide the services for the file
 * transfer.
 */
public interface IFileService {

	/**
	 * This method is used to get the list of log file names.
	 * 
	 * @param executionResId
	 * @return List<String>
	 */
	List<String> getDeviceLogFileNames(String executionResId);

	/**
	 * This method is used to download the log file.
	 * 
	 * @param executionId
	 * @param executionResId
	 * @param fileName
	 * @return Resource
	 */
	Resource downloadDeviceLogFile(String executionResId, String fileName);

	/**
	 * This method is used to download all the log files.
	 * 
	 * @param executionId
	 * @param executionResId
	 * @return byte[]
	 * @throws IOException
	 */
	byte[] downloadAllDeviceLogFiles(String executionResultId) throws IOException;

	/**
	 * This method is used to upload the log file.
	 * 
	 * @param logFile
	 * @param fileName
	 * @return String
	 */
	String uploadLogs(MultipartFile logFile, String fileName);

	/**
	 * This method is used to get the image name.
	 * 
	 * @param executionId
	 * @return String
	 */
	String getImageName(String executionId);

	/**
	 * This method is used to get the list of log file names.
	 * 
	 * @param executionId
	 * @param executionResultId
	 * @param baseLogPath
	 * @return String
	 */
	String getAgentLogContent(String executionResultId);

	/**
	 * This method is used to download the agentLog file
	 * 
	 * @param executionId
	 * @param executionResId
	 * @param fileName
	 * @return
	 */
	Resource downloadAgentLogFile(String executionResId);
}
