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
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.rdkm.tdkservice.config.AppConfig;
import com.rdkm.tdkservice.enums.DeviceStatus;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.exception.UserInputException;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.repository.DeviceRepositroy;
import com.rdkm.tdkservice.response.CreatePackageResponse;
import com.rdkm.tdkservice.service.IPackageManagerService;
import com.rdkm.tdkservice.service.utilservices.ScriptExecutorService;
import com.rdkm.tdkservice.util.Constants;

@Service
public class PackageManagerServiceImpl implements IPackageManagerService {

	// logger
	private static final Logger LOGGER = LoggerFactory.getLogger(PackageManagerServiceImpl.class);

	@Autowired
	DeviceRepositroy deviceRepository;

	@Autowired
	DeviceStatusService deviceStatusService;

	@Autowired
	private ScriptExecutorService scriptExecutorService;

	/**
	 * Creates a package for the specified device.
	 *
	 * @param type   the type of the package to be created
	 * @param device the name of the device for which the package is to be created
	 * @return a CreatePackageResponse object containing the status and logs of the
	 *         package creation process
	 * @throws UserInputException if the specified device is not found
	 */

	@Override
	public CreatePackageResponse createPackage(String type, String device) {

		LOGGER.info("Creating package for device " + device);
		CreatePackageResponse createPackageResponse = new CreatePackageResponse();

		Device deviceObj = deviceRepository.findByName(device);
		if (deviceObj == null) {
			LOGGER.error("Device not found");
			throw new UserInputException("Device " + device + " not found");
		}
		String socName = deviceObj.getSoc().getName();
		if (socName == null || socName.isEmpty()) {
			LOGGER.error("Soc name  not found for the device");
			throw new UserInputException("Soc name  " + socName + " not found for this device");
		}

		String shellScriptPath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + "createTDKPackage.sh";
		File createTdkPackageFile = new File(shellScriptPath);
		String createTdkPackageFilePath = createTdkPackageFile.getParent();
		String createTdkPackageFileName = createTdkPackageFile.getName();

		StringBuilder commandBuilder = new StringBuilder();
		commandBuilder.append("cd ").append(createTdkPackageFilePath).append(" && ./").append(createTdkPackageFileName)
				.append(" ").append(deviceObj.getSoc().getName().toLowerCase());
		String[] command = { "sh", "-c", commandBuilder.toString() };

		String outputData;
		try {
			outputData = scriptExecutorService.executeScript(command, 60);
		} catch (Exception e) {
			LOGGER.error("Error executing script", e);
			createPackageResponse.setStatus("Error executing script");
			return createPackageResponse;
		}

		Pattern pattern = Pattern.compile("Created TDK_Package_.*.tar.gz successfully");
		if (pattern.matcher(outputData).find()) {
			createPackageResponse.setStatus("Created TDK Package successfully");
			createPackageResponse.setLogs(outputData);
			LOGGER.info("Package created successfully");
		} else {
			createPackageResponse.setStatus("Failed to create TDK Package");
			createPackageResponse.setLogs(outputData);
			LOGGER.error("Failed to create package");

		}
		return createPackageResponse;
	}

	/**
	 * Retrieves a list of available packages for a given device.
	 *
	 * @param device the name of the device for which to retrieve available packages
	 * @return a list of available package names, or null if no packages are found
	 * @throws UserInputException if the specified device is not found
	 */
	@Override
	public List<String> getAvailablePackages(String device) {

		LOGGER.info("Getting available packages for device " + device);
		Device deviceObj = deviceRepository.findByName(device);
		if (deviceObj == null) {
			LOGGER.error("Device not found");
			throw new UserInputException("Device " + device + " not found");
		}
		String socName = deviceObj.getSoc().getName();

		if (socName == null || socName.isEmpty()) {
			LOGGER.error("Soc name  not found for the device");
			throw new UserInputException("Soc name  " + socName + " not found for this device");
		}
		String tdkPackagesLocation = AppConfig.getBaselocation() + "/tdk_packages/" + socName.toLowerCase();
		File file = new File(tdkPackagesLocation);
		if (!file.exists()) {
			LOGGER.error("No packages found for the device");
			return null;
		}
		return List.of(file.list());

	}

	/**
	 * Uploads a package file for a specified device.
	 *
	 * @param uploadFile the MultipartFile to be uploaded, must be a .tar.gz file
	 * @param device     the name of the device for which the package is being
	 *                   uploaded
	 * @return true if the package is uploaded successfully, false otherwise
	 * @throws UserInputException if the file format is invalid or the device is not
	 *                            found
	 */
	@Override
	public boolean uploadPackage(MultipartFile uploadFile, String device) {
		LOGGER.info("Uploading package for device {}", device);

		// Add validation that upoaded file must be .tar.gz
		String fileName = uploadFile.getOriginalFilename();
		if (fileName == null || fileName.isEmpty() || !fileName.endsWith(".tar.gz")) {
			LOGGER.error("Invalid file name");
			throw new UserInputException("Invalid package format");
		}
		Device deviceObj = deviceRepository.findByName(device);
		if (deviceObj == null) {
			LOGGER.error("Device not found");
			throw new UserInputException("Device " + device + " not found");
		}

		String socName = deviceObj.getSoc().getName();
		if (socName == null || socName.isEmpty()) {
			LOGGER.error("Soc name  not found for the device");
			throw new UserInputException("Soc name  " + socName + " not found for this device");
		}
		String tdkPackagesLocation = AppConfig.getBaselocation() + "/tdk_packages/" + socName.toLowerCase();
		File directory = new File(tdkPackagesLocation);
		if (!directory.exists()) {
			if (!directory.mkdirs()) {
				LOGGER.error("Failed to create directory {}", tdkPackagesLocation);
				return false;
			}
		}

		if (fileName == null || fileName.isEmpty()) {
			LOGGER.error("Invalid file name");
			return false;
		}

		File destination = new File(directory, fileName);
		try {
			uploadFile.transferTo(destination);
			LOGGER.info("Package uploaded successfully to {}", destination.getAbsolutePath());
			return true;
		} catch (Exception e) {
			LOGGER.error("Error uploading the package", e);
			return false;
		}

	}

	/**
	 * Installs a specified package on a given device.
	 *
	 * @param device      the name of the device on which the package is to be
	 *                    installed
	 * @param packageName the name of the package to be installed
	 * @return the output of the script execution
	 * @throws UserInputException        if the device is not found or is offline
	 * @throws ResourceNotFoundException if the package or the installation script
	 *                                   is not found
	 * @throws RuntimeException          if there is an error executing the script
	 */
	public String installPackage(String device, String packageName) {
		LOGGER.info("Installing package {} on device {}", packageName, device);

		Device deviceObj = deviceRepository.findByName(device);
		if (deviceObj == null) {
			LOGGER.error("Device not found");
			throw new UserInputException("Device " + device + " not found");
		}
		String socName = deviceObj.getSoc().getName();
		if (socName == null || socName.isEmpty()) {
			LOGGER.error("Soc name  not found for the device");
			throw new UserInputException("Soc name  " + socName + " not found for this device");
		}
		DeviceStatus deviceStatus = deviceStatusService.fetchDeviceStatus(deviceObj);
		if (deviceStatus == DeviceStatus.FREE) {
			deviceStatusService.setDeviceStatus(DeviceStatus.IN_USE, deviceObj);
		} else if (deviceStatus == DeviceStatus.NOT_FOUND) {
			LOGGER.error("Device is offline");
			throw new UserInputException("Device " + device + " is down");
		} else {
			LOGGER.error("Device is not available");
			throw new UserInputException("Device " + device + " is not available for update");
		}

		String tdkPackagesLocation = AppConfig.getBaselocation() + "/tdk_packages/" + socName.toLowerCase() + "/"
				+ packageName;
		File packageFile = new File(tdkPackagesLocation);
		if (!packageFile.exists()) {
			LOGGER.error("Package not found");
			throw new ResourceNotFoundException("Package ", packageName);
		}

		String scriptPath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + "InstallTDKPackage.sh";
		if (!new File(scriptPath).exists()) {
			LOGGER.error("Script not found");
			throw new ResourceNotFoundException("Script ", scriptPath);
		}

		String remoteFilePath = "/opt/TDK/logs/tdk_agent.log";
		String deviceIp = deviceObj.getIp();
		String sshOptions = "-o StrictHostKeyChecking=no";
		String sshPass = "sshpass";
		String password = ""; // Your password here
		String user = "root";
		String userPassword = "root";
		String[] copyPackageCommand = { sshPass, "-p", password, "scp", sshOptions, tdkPackagesLocation,
				user + "@" + deviceIp + ":/" };
		String[] copyScriptCommand = { sshPass, "-p", password, "scp", sshOptions, scriptPath,
				user + "@" + deviceIp + ":/" };
		String[] executeScriptCommand = { sshPass, "-p", userPassword, "ssh", sshOptions, user + "@" + deviceIp,
				"mkdir -p $(dirname " + remoteFilePath + ") && sh /InstallTDKPackage.sh \"" + packageName
						+ "\" --disable-reboot > " + remoteFilePath + " && cat " + remoteFilePath };
		String[] rebootCommand = { sshPass, "-p", userPassword, "ssh", sshOptions, user + "@" + deviceIp,
				"/sbin/reboot" };

		LOGGER.info("copyPackageCommand: " + Arrays.toString(copyPackageCommand));
		LOGGER.info("copyScriptCommand: " + Arrays.toString(copyScriptCommand));
		LOGGER.info("executeScriptCommand: " + Arrays.toString(executeScriptCommand));
		LOGGER.info("rebootCommand: " + Arrays.toString(rebootCommand));
		try {

			scriptExecutorService.executeScript(copyPackageCommand, 60);
			scriptExecutorService.executeScript(copyScriptCommand, 60);
			String output = scriptExecutorService.executeScript(executeScriptCommand, 60);
			if (output.contains("Going to reboot the device")) {
				String message = "\nPackage installed successfully.";
				output = output + message;
			} else {
				String errorMessage = "\n Error Occured While Installation";
				output = output + errorMessage;
			}
			return output;

		} catch (Exception e) {
			LOGGER.error("Error executing script", e);
			throw new RuntimeException("Error executing script", e);
		} finally {
			scriptExecutorService.executeScript(rebootCommand, 60);
			deviceStatusService.fetchAndUpdateDeviceStatus(deviceObj);
		}

	}

}
