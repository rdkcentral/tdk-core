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

import com.rdkm.tdkservice.config.AppConfig;
import com.rdkm.tdkservice.config.ExecutionConfig;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.Device;
import com.rdkm.tdkservice.model.Module;
import com.rdkm.tdkservice.repository.DeviceRepositroy;
import com.rdkm.tdkservice.repository.ModuleRepository;
import com.rdkm.tdkservice.service.IFileService;
import com.rdkm.tdkservice.service.utilservices.CommonService;
import com.rdkm.tdkservice.service.utilservices.ScriptExecutorService;
import com.rdkm.tdkservice.util.Constants;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MaxUploadSizeExceededException;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import static com.rdkm.tdkservice.util.Constants.*;

/**
 *This method is used to transfer the log files for thunder enabled/disabled devices
 */
@Service
public class FileTransferService implements IFileService {

	public static final Logger LOGGER = LoggerFactory.getLogger(FileTransferService.class);

	@Autowired
	private ModuleRepository moduleRepository;

	@Autowired
	private DeviceRepositroy deviceRepository;

	@Autowired
	private CommonService commonService;

	@Autowired
	private ScriptExecutorService scriptExecutorService;

	@Autowired
	private ExecutionConfig executionConfig;

	@Autowired
	private AppConfig appConfig;

	/**
	 * Transfer device logs for thunder enabled devices This will transfer logs from
	 * the device based on the module configuration
	 * @param moduleName
	 * @param executionId
	 * @param executionResultId
	 */
	public void transferDeviceLogsForThunderEnabled(String moduleName, UUID executionId, UUID executionResultId,
			String deviceIP) {
		try {
			LOGGER.info("Starting transferSTBLogRdkService for request: {}", executionId.toString());
			String baseLogPath = commonService.getBaseLogPath();

			Module module = null;
			try {
				module = moduleRepository.findByName(moduleName);
				LOGGER.info("Module retrieved: {}", module.getName());
			} catch (Exception e) {
				LOGGER.error("Error retrieving module for name {}: {}", moduleName, e.getMessage(), e);
			}

			List<String> deviceLogFiles = null;
			if (module != null) {
				deviceLogFiles = new ArrayList<>(module.getLogFileNames());
				LOGGER.info("Device log files retrieved from module: {}", deviceLogFiles);
			}

			String deviceLogFilesPath = commonService.getDeviceLogsPathForTheExecution(executionId.toString(),
					executionResultId.toString(), baseLogPath);

			new File(deviceLogFilesPath).mkdirs();
			LOGGER.info("Ensured directory exists at: {}", deviceLogFilesPath);

			Device device = null;
			try {
				device = deviceRepository.findByIp(deviceIP);
				LOGGER.info("Device retrieved: {}", device);
			} catch (Exception e) {
				LOGGER.error("Error retrieving device for IP {}: {}", deviceIP, e.getMessage(), e);
			}

			if (deviceLogFiles != null) {
				LOGGER.info("Processing {} log files.", deviceLogFiles.size());
				for (String name : deviceLogFiles) {
					LOGGER.info("Processing log file: {}", name);

					File deviceLogTransferScriptFile = new File(AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR
							+ FILE_TRANSFER_SCRIPT_RDKSERVICE);
					LOGGER.info("Device log transfer script file located at: {}", deviceLogTransferScriptFile);

					String deviceLogTransferScriptFilePath = deviceLogTransferScriptFile.getAbsolutePath();
					LOGGER.info("Device log transfer script file absolute path: {}", deviceLogTransferScriptFilePath);

					String[] fname = name.split("/");
					LOGGER.debug("Split file name: {}", (Object) fname);

					String fileName = fname[fname.length - 1];
					LOGGER.info("Extracted file name: {}", fileName);

					if (!deviceLogTransferScriptFilePath.isEmpty()) {
						assert device != null;
						String[] cmd = commandForTransferThunderEnabledLogFiles(commonService.getPythonCommandFromConfig(), deviceLogTransferScriptFilePath, device.getIp(), name,
								deviceLogFilesPath, fileName);
						try {
							String outputData = scriptExecutorService.executeScript(cmd, 1);
						} catch (Exception e) {
							LOGGER.error("Error executing script: {}", e.getMessage(), e);
						}
					} else {
						LOGGER.warn("Device log transfer script file path is empty, skipping execution.");
					}
				}
			} else {
				LOGGER.warn("No device log files to process.");
			}
		} catch (Exception e) {
			LOGGER.error("Error in transferDeviceLogsForThunderEnabled: {}", e.getMessage(), e);
		}
	}

	/**
	 * Prepare command for file transfer
	 * 
	 * @param pythonCommand
	 * @param scriptFilePath
	 * @param deviceIP
	 * @param fileNameToBeTransferred
	 * @param destinationPath
	 * @param fileNameToBeSaved
	 * @return Array of the python command
	 */
	private String[] commandForTransferThunderEnabledLogFiles(String pythonCommand, String scriptFilePath, String deviceIP,
			String fileNameToBeTransferred, String destinationPath, String fileNameToBeSaved) {
		LOGGER.debug(
				"Preparing command with parameters: pythonCommand={}, scriptFilePath={}, deviceIP={}, fileNameToBeTransferred={}, destinationPath={}, fileNameToBeSaved={}",
				pythonCommand, scriptFilePath, deviceIP, fileNameToBeTransferred, destinationPath, fileNameToBeSaved);
		return new String[] { pythonCommand, scriptFilePath, deviceIP, ROOT_STRING, NONE_STRING,
				fileNameToBeTransferred, destinationPath, fileNameToBeSaved };
	}

	/**
	 * This method is used to get the device log files available for the execution
	 * say wpeframework logs, thunder logs etc.
	 * 
	 * @param executionId
	 * @param executionResId    return list of filenames
	 */
	@Override
	public List<String> getDeviceLogFileNames(String executionId, String executionResId) {
		try {
			LOGGER.debug("Getting log file names with parameters: executionId={}, executionResId={}", executionId,
					executionResId);
			String baselogpath = commonService.getBaseLogPath();
			String logsDirectory = commonService.getDeviceLogsPathForTheExecution(executionId, executionResId,
					baselogpath);
			List<String> fileNames = commonService.getFilenamesFromDirectory(logsDirectory, executionId);
			LOGGER.debug("Log file names: {}", fileNames);
			return fileNames;
		} catch (Exception e) {
			LOGGER.error("Error in getLogFileNames: {}", e.getMessage(), e);
			return Collections.emptyList();
		}
	}

	/**
	 * Method to download a log file
	 *
	 * @param executionId The execution ID
	 * @param executionResId The execution resource ID
	 * @param fileName The name of the file to download
	 * @return Resource
	 */
	@Override
	public Resource downloadDeviceLogFile(String executionId, String executionResId, String fileName) {
		LOGGER.info("Inside downloadDeviceLogFile method with fileName: {}", fileName);

		// Get log file names for the execution
		List<String> logFileNames = this.getDeviceLogFileNames(executionId, executionResId);
		if (!logFileNames.contains(fileName)) {
			LOGGER.error("Log file not found: {}", fileName);
			throw new ResourceNotFoundException("Log file", fileName);
		}

		// Determine the path for the log file
		String baseLogPath = commonService.getBaseLogPath();
		String logsDirectory = commonService.getDeviceLogsPathForTheExecution(executionId, executionResId, baseLogPath);

		// Use the helper method to get the resource
		return getFileAsResource(logsDirectory, fileName);
	}

	/**
	 * Download all log files
	 *  This method is used to download all the log files for the given execution ID
	 * @param
	 * @param executionId
	 * @param executionResId
	 * return byte[]
	 */
	@Override
	public byte[] downloadAllDeviceLogFiles(String executionId, String executionResId) throws IOException {
		List<String> logFileNames = this.getDeviceLogFileNames(executionId, executionResId);

		if (logFileNames.isEmpty()) {
			throw new FileNotFoundException("No log files found for the given execution ID and executionRes ID.");
		}

		String baselogpath = commonService.getBaseLogPath();
		String logsDirectory = commonService.getDeviceLogsPathForTheExecution(executionId, executionResId, baselogpath);

		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		try (ZipOutputStream zos = new ZipOutputStream(baos)) {
			for (String fileName : logFileNames) {
				String filePath = logsDirectory + Constants.FILE_PATH_SEPERATOR + fileName;

				File file = new File(filePath);
				if (file.exists() && file.isFile()) {
					try (FileInputStream fis = new FileInputStream(file)) {
						ZipEntry zipEntry = new ZipEntry(file.getName());
						zos.putNextEntry(zipEntry);

						byte[] buffer = new byte[1024];
						int bytesRead;
						while ((bytesRead = fis.read(buffer)) != -1) {
							zos.write(buffer, 0, bytesRead);
						}
						zos.closeEntry();
					}
				}
			}
		}
		return baos.toByteArray();
	}

	/**
	 * This method is used to get the image name.
	 * @param executionID
	 * @param executionResultID
	 * @param executionResultID
	 */
	public void transferAgentLogs(String deviceIP, String executionID, String executionResultID) {
		try {
			String baseLogPath = commonService.getBaseLogPath();

			Device device = deviceRepository.findByIp(deviceIP);
			LOGGER.info("Fetched device by IP: {}", device);

			String scriptName = this.getAgentConsoleFileTransferScriptName(device);
			String scriptPath = Paths.get(AppConfig.getRealPath() + Constants.FILE_PATH_SEPERATOR + scriptName)
					.toString();
			LOGGER.info("Script path: {}", scriptPath);
			String logTransferFileNameForTheExecution = executionResultID + Constants.UNDERSCORE
					+ AGENT_CONSOLE_LOG_FILE;

			List<String> cmdList = buildCommandListForAgentLogTransfer(scriptPath, deviceIP,
					device.getAgentMonitorPort(), AGENT_CONSOLE_LOG_FILE, logTransferFileNameForTheExecution, device);

			String output=scriptExecutorService.executeScript(cmdList.toArray(new String[0]), 2);
			String agentLogTransferFilePath = commonService.getAgentLogPath(executionID, executionResultID,
					baseLogPath);
			// TODO : Need to check for the sleep time and then the wait time to be added
			Thread.sleep(4000);
			copyAgentconsoleLogIntoDir(agentLogTransferFilePath, executionResultID);

		} catch (Exception e) {
			LOGGER.error("Error during log transfer: {}", e.getMessage(), e);
		}
	}

	/**
	 * Get Agent console file transfer script name
	 * 
	 * @param device -- the device entity
	 * @return Agent console file transfer pyhton script name
	 */
	private String getAgentConsoleFileTransferScriptName(Device device) {
		// String scriptName = Constants.CONSOLE_FILE_TRANSFER_SCRIPT;
		// TODO CONSOLE_FILE_TRANSFER_SCRIPT is for tftp, now we are not implementing
		return CONSOLE_FILE_UPLOAD_SCRIPT;
	}

	/**
	 * Copy agent console log into the specified directory
	 *
	 * @param logTransferFilePath
	 * @param executionResultId
	 */
	private void copyAgentconsoleLogIntoDir(String logTransferFilePath, String executionResultId) {
		try {
			// Get the base file path for upload log
			String getBaseFilePathForUploadLogAPI = commonService.getBaseFilePathForUploadLogAPI();
			File logDir = new File(getBaseFilePathForUploadLogAPI);
			LOGGER.info("Log directory: {}", logDir);
			if (logDir.isDirectory()) {
				for (File file : Objects.requireNonNull(logDir.listFiles())) {
					if (file.getName().contains(AGENT_CONSOLE_LOG_FILE)) {
						String[] logFileName = file.getName().split(Constants.UNDERSCORE);
						if (logFileName.length >= 3 && executionResultId.equals(logFileName[0])) {
							new File(logTransferFilePath).mkdirs();
							File logTransferPath = new File(logTransferFilePath);
							if (file.exists()) {
								file.renameTo(new File(logTransferPath, file.getName()));
							}
						}
					}
				}
			}
		} catch (Exception e) {
			System.out.println("Error: " + e.getMessage());
			e.printStackTrace();
		}
	}

	/**
	 * Build command list
	 * This method is to build the command list for agent log transfer
	 * @param scriptPath
	 * @param deviceIP
	 * @param agentMonitorPort
	 * @param sourceFileName
	 * @param targetFileName
	 * @param device
	 * @return List of command
	 */
	private List<String> buildCommandListForAgentLogTransfer(String scriptPath, String deviceIP,
			String agentMonitorPort, String sourceFileName, String targetFileName, Device device) {
		List<String> cmdList = new ArrayList<>();
		cmdList.add(commonService.getPythonCommandFromConfig());
		cmdList.add(scriptPath);
		cmdList.add(deviceIP);
		cmdList.add(agentMonitorPort);
		cmdList.add(sourceFileName);
		cmdList.add(targetFileName);
		String urlFromConfigFile = commonService.getTMUrlFromConfigFile();
		cmdList.add(urlFromConfigFile);
		LOGGER.info("Script cmdList path: {}", cmdList);
		return cmdList;
	}

	/**
	 * This method is to do version transfer for thunder disabled devices
	 * @param executionID
	 * @param deviceName
	 * @return
	 */
	private boolean createVersionFileForThunderDisabled(String executionID, String deviceName) {
		try {
			String versionFileName = executionID + Constants.UNDERSCORE + "version.txt";
			String versionFilePath = commonService.getVersionLogFilePathForTheExecution(executionID);

			Device device = deviceRepository.findByName(deviceName);

			// Build the command list for file transfer
			List<String> cmdList = buildCommandListForFileTransfer(device, "/version.txt", versionFileName);

			// Log the command being executed
			LOGGER.info("Executing command: {}", String.join(" ", cmdList));

			// Execute the script
			String outputData = scriptExecutorService.executeScript(cmdList.toArray(new String[0]), 1);
			LOGGER.info("Script executed successfully. Output data: {}", outputData);

			// Copy version logs into the specified directory
			copyVersionLogsIntoDir(versionFilePath, executionID);

			return true;
		} catch (Exception e) {
			LOGGER.error("Error occurred during version transfer script execution: {}", e.getMessage(), e);
			return false;
		}
	}

	/**
	 * This method is for uploading the files to the destination location via api
	 * call
	 * 
	 * @param logFile  - log file
	 * @param fileName - name in which the file needs to be saved
	 * @return
	 */
	@Override
	public String uploadLogs(MultipartFile logFile, String fileName) {
		String data = "";
		LOGGER.info("Starting uploadLogs method.");
		try {
			if (logFile != null && !logFile.isEmpty()) {
				// Read the uploaded file content
				List<String> fileContent = readUploadedFileContent(logFile);

				// Get the real path for logs
				String uploadLogPath = commonService.getBaseFilePathForUploadLogAPI();
				File logFilePath = new File(uploadLogPath + Constants.FILE_PATH_SEPERATOR + fileName);

				// Ensure the directories exist
				File logDir = new File(uploadLogPath);
				if (!logDir.exists()) {
					logDir.mkdirs();
					LOGGER.info("Created directories for log file path: {}", uploadLogPath);
				}

				// Write content to the file
				writeContentToFile(logFilePath, fileContent);

				// Combine the file content into a single string
				data = String.join("\n", fileContent);
			} else {
				LOGGER.warn("No file was uploaded or the file is empty.");
			}
		} catch (IOException e) {
			LOGGER.error("IOException: An I/O error occurred while processing the file.", e);
		} catch (MaxUploadSizeExceededException e) {
			LOGGER.error("MaxUploadSizeExceededException: Uploaded file size exceeds the maximum limit.", e);
		} catch (Exception e) {
			LOGGER.error("uploadLogs ERROR: {}", e.getMessage(), e);
		}
		LOGGER.info("uploadLogs method completed.");
		return data;
	}

	/**
	 * This method is used to upload file content
	 * @param uploadedFile
	 * @return
	 * @throws IOException
	 */
	private List<String> readUploadedFileContent(MultipartFile uploadedFile) throws IOException {
		try (BufferedReader reader = new BufferedReader(new InputStreamReader(uploadedFile.getInputStream()))) {
			return reader.lines().toList();
		}
	}

	/**
	 * Write content to the file
	 * @param logFile
	 * @param fileContent
	 * @throws IOException
	 */
	private void writeContentToFile(File logFile, List<String> fileContent) throws IOException {
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(logFile))) {
			for (String log : fileContent) {
				writer.write(log);
				writer.newLine();
			}
		}
	}

	/**
	 * This method is to build command list for file transfer for thunder disabled
	 * 
	 * @param device         - Device entity
	 * @param sourceFilePath - source file path in the device
	 * @param targetFileName - name, where the source file needs to be saved when
	 *                       uplaoded
	 * @return List of command
	 */
	private List<String> buildCommandListForFileTransfer(Device device, String sourceFilePath, String targetFileName) {
		List<String> cmdList = new ArrayList<>();
		cmdList.add(commonService.getPythonCommandFromConfig());
		cmdList.add(AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + getFileTransferScriptNameForTDKEnabled());
		cmdList.add(device.getIp());
		cmdList.add(device.getAgentMonitorPort());
		cmdList.add(sourceFilePath);
		cmdList.add(targetFileName);
		String configFileUrl = commonService.getTMUrlFromConfigFile();
		cmdList.add(configFileUrl);

		// Log the command list
		LOGGER.info("Thunder disabled command: {}", String.join(" ", cmdList));

		return cmdList;
	}

	/**
	 * Get file transfer script name based on the device type
	 * 
	 * @param  - the device entity
	 * @return the file transfer script name
	 */
	private String getFileTransferScriptNameForTDKEnabled() {
		String scriptName = Constants.FILE_UPLOAD_SCRIPT;
		return scriptName;
	}

	/**
	 * This method is to retrieve the version file for thunder disabled devices
	 * 
	 * @param logTransferFilePath
	 * @param executionId
	 */
	public void copyVersionLogsIntoDir(String logTransferFilePath, String executionId) {
		try {
			String baseLogUploadPathForUploadAPI = commonService.getBaseFilePathForUploadLogAPI();

			File logDir = new File(baseLogUploadPathForUploadAPI);
			if (!logDir.isDirectory()) {
				LOGGER.warn("Log directory does not exist: {}", baseLogUploadPathForUploadAPI);
				return;
			}

			Files.walk(Paths.get(baseLogUploadPathForUploadAPI)).filter(Files::isRegularFile)
					.forEach(filePath -> transferThunderDisabledVersionFile(filePath.toFile(), logTransferFilePath, executionId));
		} catch (IOException e) {
			LOGGER.error("Error while accessing log directory: {}", e.getMessage(), e);
		}
	}

	/**
	 * This method is to transfer the version.txt file for thunder disabled devices
	 * to the destination location
	 * 
	 * @param file
	 * @param logTransferFilePath
	 * @param executionId
	 */
	private void transferThunderDisabledVersionFile(File file, String logTransferFilePath, String executionId) {
		LOGGER.info("Processing file: {}", file.getName());
		if (!file.getName().contains("version.txt")) {
			return;
		}

		String[] logFileNameParts = file.getName().split("_");
		if (logFileNameParts.length > 1 && executionId != null && executionId.toString().equals(logFileNameParts[0])) {

			String versionFileName = executionId + Constants.UNDERSCORE + "_version.txt";
			File logTransferDir = new File(logTransferFilePath);

			if (logTransferDir.mkdirs() || logTransferDir.exists()) {
				File movedFile = new File(logTransferFilePath, versionFileName);
				if (file.renameTo(movedFile)) {
					LOGGER.info("File moved successfully: {}", file.getName());
				} else {
					LOGGER.warn("Failed to move file: {}", file.getName());
				}
			} else {
				LOGGER.error("Failed to create log transfer directory: {}", logTransferFilePath);
			}
		}
	}

	/**
	 * This method is to transfer the version.txt file for thunder enabled devices
	 * to the destination location
	 * @param executionId
	 * @param executionDeviceId
	 * @param deviceIP
	 * @return boolean
	 */
	public boolean createVersionFileForThunderEnabled(String executionId, String executionDeviceId, String deviceIP) {
		LOGGER.info("Creating version file for thunder enabled devices");
		try {

			boolean versionFileStatus = false;

			String versionFilePath = commonService.getVersionLogFilePathForTheExecution(executionId);
			LOGGER.info("Creating version file path: {}", versionFilePath);

			if (createDirectories(versionFilePath)) {

				String versionFileName = executionId + "_version.txt";
				String versionFileAbsolutePath = versionFilePath + versionFileName;

				File versionFile = new File(versionFileAbsolutePath);

				boolean versionFileTransferredStatus = transferFileForThunderEnabled(deviceIP, versionFilePath,
						versionFileName, SLASH_VERSION_TXT_FILE);
				LOGGER.info("transferThunderFile status: {}", versionFileTransferredStatus);

				if (!versionFileTransferredStatus) {
					String thunderVersionDetails = retrieveFirmwareVersionForThunderEnabled(deviceIP);

					versionFileStatus = createVersionFile(versionFile, thunderVersionDetails);
					LOGGER.info("Version file created: {}", versionFileStatus);
				} else {
					LOGGER.info("Version file transferred successfully.");
					versionFileStatus = true;
				}
			}
			return versionFileStatus;
		} catch (Exception e) {
			LOGGER.error("Exception in createThunderVersionFile", e);
			return false;
		}
	}

	/**
	 * This method is to transfer the file for thunder enabled devices
	 * @param deviceIP
	 * @param destinationPath
	 * @param fileNameToBeSaved
	 * @param fileNameToBeTransferred
	 * @return boolean
	 */
	private boolean transferFileForThunderEnabled(String deviceIP, String destinationPath, String fileNameToBeSaved,
			String fileNameToBeTransferred) {
		boolean fileTransferredStatus = false;
		boolean fileRenamedStatus = false;

		try {
			String transferScriptFilePath = getScriptFilePathForThunderEnabledFiletransfer();
			String pythonCommand = executionConfig.getPythonCommand();
			String[] cmd = commandForTransferThunderEnabledLogFiles(pythonCommand, transferScriptFilePath, deviceIP, fileNameToBeTransferred,
					destinationPath, fileNameToBeSaved);
			String exitCode = scriptExecutorService.executeScript(cmd, 1);
			LOGGER.info("Thunder enabled file transfer Script exit code: {}", exitCode);
			fileTransferredStatus = verifyFileTransfer(destinationPath, fileNameToBeTransferred);
			LOGGER.info("Execution instance directory path: {}", fileTransferredStatus);
			if (fileTransferredStatus) {
				fileRenamedStatus = renameTransferredFile(destinationPath, fileNameToBeTransferred, fileNameToBeSaved);
			}

		} catch (Exception e) {
			LOGGER.error("Error: {}", e.getMessage());
			e.printStackTrace();
		}

		return fileRenamedStatus;
	}

	/**
	 * This method is to get the script file path for thunder enabled file transfer
	 * @return String
	 */
	private String getScriptFilePathForThunderEnabledFiletransfer() {
		return AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + FILE_TRANSFER_SCRIPT_RDKSERVICE;
	}

	/**
	 *  This method is to verify the file transfer
	 * @param destinationPath
	 * @param fileNameToBeTransferred
	 * @return boolean
	 */
	private boolean verifyFileTransfer(String destinationPath, String fileNameToBeTransferred) {
		String transferredFilePath = Paths.get(destinationPath, fileNameToBeTransferred).toString();
		LOGGER.info("Transferred file path: {}", transferredFilePath);
		File transferredFile = new File(transferredFilePath);
		boolean fileTransferredStatus = transferredFile.isFile();
		LOGGER.info("File transferred status: {}", fileTransferredStatus);
		return fileTransferredStatus;
	}

	/**
	 * THis method is to rename the transferred file
	 * @param destinationPath
	 * @param fileNameToBeTransferred
	 * @param fileNameToBeSaved
	 * @return boolean
	 */
	private boolean renameTransferredFile(String destinationPath, String fileNameToBeTransferred,
			String fileNameToBeSaved) {
		String fileNameToBeSavedFullPath = destinationPath + Constants.FILE_PATH_SEPERATOR + fileNameToBeSaved;
		LOGGER.info("File name to be saved full path: {}", fileNameToBeSavedFullPath);
		File transferredFile = new File(destinationPath + Constants.FILE_PATH_SEPERATOR + fileNameToBeTransferred);
		boolean fileRenamedStatus = transferredFile.renameTo(new File(fileNameToBeSavedFullPath));
		LOGGER.info("File renamed status: {}", fileRenamedStatus);
		return fileRenamedStatus;
	}

	/**
	 * This method is to create directories
	 * @param path
	 * @return boolean
	 */
	private boolean createDirectories(String path) {
		File dir = new File(path);
		if (!dir.exists() && dir.mkdirs()) {
			LOGGER.info("Directory created successfully: {}", path);
			return true;
		}
		return false;
	}

	/**
	 * This method is to create the version file
	 * @param versionFile
	 * @param content
	 * @return boolean
	 */
	private boolean createVersionFile(File versionFile, String content) {
		try {
			if (versionFile.createNewFile()) {
				try (FileWriter fr = new FileWriter(versionFile)) {
					fr.write(content);
					return true;
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return false;
	}

	/**
	 * This method is to retrieve the firmware version for thunder enabled devices
	 * @param deviceIP
	 * @return String
	 */
	public String retrieveFirmwareVersionForThunderEnabled(String deviceIP) {
		String thunderVersionDetailsFormatted = "";
		String thunderPort = Constants.THUNDER_DEFAULT_PORT;

		Device dev = deviceRepository.findByIp(deviceIP);
		if (dev != null) {
			thunderPort = dev.getThunderPort();
		}

		try {
			String urlString = "http://" + deviceIP + ":" + thunderPort + "/jsonrpc";
			URL url = new URL(urlString);
			URLConnection con = url.openConnection();
			HttpURLConnection http = (HttpURLConnection) con;

			http.setRequestMethod("POST");
			http.setDoOutput(true);
			String jsonInputString = "{\"jsonrpc\": \"2.0\",\"id\": 1234567890,\"method\": \"org.rdk.System.1.getDownloadedFirmwareInfo\"}";
			byte[] out = jsonInputString.getBytes(StandardCharsets.UTF_8);
			int length = out.length;
			http.setFixedLengthStreamingMode(length);
			http.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
			http.setRequestProperty("Accept", "application/json");

			con.getOutputStream().write(out);
			http.connect();

			try (InputStream iStream = con.getInputStream();
					BufferedReader reader = new BufferedReader(
							new InputStreamReader(iStream, StandardCharsets.UTF_8))) {
				StringBuilder result = new StringBuilder();
				String line;
				while ((line = reader.readLine()) != null) {
					result.append(line);
				}
				String response = result.toString();

				JSONObject jsonObject = new JSONObject(response);
				JSONObject resultJsonObject = jsonObject.getJSONObject("result");
				if (resultJsonObject.has("currentFWVersion")) {
					String currentFWVersion = resultJsonObject.getString("currentFWVersion");
					thunderVersionDetailsFormatted = "currentFWVersion: " + currentFWVersion;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

		return thunderVersionDetailsFormatted;
	}

	/**
	 * This method is to transfer the device logs for TDK enabled devices
	 * @param moduleName
	 * @param deviceIp
	 * @param execId
	 * @param execResultId
	 */
	public void transferDeviceLogsForTDKEnabled(String moduleName, String deviceIp, UUID execId, UUID execResultId) {
		try {
			// Fetch device details
			Device device = deviceRepository.findByIp(deviceIp);
			String baseLogPath = commonService.getBaseLogPath();

			// Fetch module and log file names
			Module module = moduleRepository.findByName(moduleName);
			Set<String> deviceLogFiles = (module != null)
					? module.getLogFileNames().stream()
					.map(Object::toString) // Convert each Object to String
					.collect(Collectors.toSet())
					: Collections.emptySet();

			// Generate STB log file path
			String deviceDestinationFilePath = commonService.getDeviceLogsPathForTheExecution(
					execId.toString(), execResultId.toString(), baseLogPath);

			// Fetch script details
			String scriptName = getFileTransferScriptNameForTDKEnabled();
			String fileTransferScriptPath = AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + scriptName;
			String tmUrl = commonService.getTMUrlFromConfigFile();
			LOGGER.info(" deviceLogFiles: {}",deviceLogFiles);
			for (String logFileName : deviceLogFiles) {
				try {
					LOGGER.info("Processing device log file: {}", logFileName);

					// Sanitize file name
					String sanitizedFileName = logFileName.replaceAll("//", "_").replaceAll("/", "_");
					LOGGER.info(" sanitizedFileName: {}",sanitizedFileName);
					// Prepare command for file transfer
					List<String> cmdList = new ArrayList<>(Arrays.asList(
							commonService.getPythonCommandFromConfig(),
							fileTransferScriptPath,
							device.getIp(),
							device.getAgentMonitorPort(),
							logFileName,
							execResultId + "_" + sanitizedFileName,
							tmUrl
					));
					LOGGER.info(" cmdList: {}",cmdList);
					// Execute the script
					String outputData = scriptExecutorService.executeScript(cmdList.toArray(new String[0]), 1);
					LOGGER.info(" outputDat: {}",outputData);
					// Copy logs into the specified directory
					copyDeviceLogsIntoDir(deviceDestinationFilePath, execId, execResultId);

					LOGGER.info("File transfer and log copying completed for: {}", logFileName);

				} catch (Exception e) {
					LOGGER.error("Error processing log file {}: {}", logFileName, e.getMessage(), e);
				}
			}
		} catch (Exception e) {
			LOGGER.error("Error in transferDeviceLogsForTDKEnabled: {}", e.getMessage(), e);
		}
	}

	/**
	 *This method is to copy the device logs into the specified directory
	 * @param deviceLogDestPath
	 * @param executionId
	 * @param executionResultId
	 */
	public void copyDeviceLogsIntoDir(String deviceLogDestPath, UUID executionId, UUID executionResultId) {
		try {
			// Get the base log path
			String baseLogPath =commonService.getBaseFilePathForUploadLogAPI();
			File logDir = new File(baseLogPath);
			if (logDir.isDirectory()) {
				for (File file : Objects.requireNonNull(logDir.listFiles())) {
					// Skip unwanted files
					if (file.getName().matches(".*(version\\.txt|benchmark\\.log|memused\\.log|cpu\\.log|AgentConsoleLog\\.log).*")) {
						continue;
					}

					String[] logFileName = file.getName().split("_");
					if (logFileName.length >= 3 &
							executionResultId.toString().equals(logFileName[0])) {

						String sanitizedFileName = file.getName().replaceAll("\\s", "").replaceAll("\\$:", "Undefined");

						// Create log transfer directory if it doesn't exist
						new File(deviceLogDestPath).mkdirs();
						File logTransferPath = new File(deviceLogDestPath);

						// Move the file
						boolean fileMoved = file.renameTo(new File(logTransferPath, sanitizedFileName));
						if (fileMoved) {
							LOGGER.info("File moved successfully: {}", sanitizedFileName);
						} else {
							LOGGER.warn("Failed to move file: {}", sanitizedFileName);
						}
					}
				}
			}
		} catch (Exception e) {
			LOGGER.error("Error while copying logs: {}", e.getMessage(), e);
		}
	}

	/**
	 * Get image name from file
	 * @param executionId
	 * @return image name
	 */
	public String getImageName(String executionId) {
		LOGGER.info("Getting image name for executionId: {}", executionId);
		String imageNameValue = "";
		try {
			String filePath = commonService.getVersionLogFilePathForTheExecution(executionId);
			File file = new File(filePath);

			if (file.exists() && file.isFile()) { // Check if it's a file
				try (BufferedReader br = new BufferedReader(new FileReader(file))) {
					String line;
					while ((line = br.readLine()) != null) {
						if (line.startsWith("imagename:")) {
							imageNameValue = line.split(":", 2)[1].trim();
							break; // Exit the loop once the imagename is found
						} else if (line.startsWith("currentFWVersion:")) {
							imageNameValue = line.split(":", 2)[1].trim();
							break; // Exit the loop once the currentFWVersion is found
						}
					}
				}
			} else {
				if (file.exists()) {
					LOGGER.warn("The path points to a directory, not a file: {}", filePath);
				} else {
					LOGGER.warn("File not found: {}", filePath);
				}
			}
		} catch (IOException e) {
			LOGGER.error("Error reading image name: {}", e.getMessage(), e);
		}

		// Log the obtained image name value
		if (!imageNameValue.isEmpty()) {
			LOGGER.info("Image name obtained: {}", imageNameValue);
		} else {
			LOGGER.info("No valid image name or firmware version found in file: {}", executionId);
		}

		return imageNameValue;
	}

	/**
	 * This method get the agent log file content
	 * @param executionId
	 * @param executionResultId
	 * @param baseLogPath
	 * @return String
	 */
	@Override
	public String getAgentLogContent(String executionId, String executionResultId, String baseLogPath) {
		// Generate the agent logs path using the existing method
		LOGGER.info("Getting agent log content for executionId: {}, executionResultId: {}", executionId, executionResultId);
		String agentLogPath = commonService.getAgentLogPath(executionId, executionResultId, baseLogPath);

		File file = new File(agentLogPath);
		StringBuilder fileContent = new StringBuilder();

		// Check if the file exists and is a file
		if (file.exists() && file.isFile()) {
			try (BufferedReader br = new BufferedReader(new FileReader(file))) {
				String line;
				while ((line = br.readLine()) != null) {
					fileContent.append(line).append("\n");
				}
			} catch (IOException e) {
				// Handle IO exceptions and log error
				LOGGER.error("Error reading agent log file: {}", e.getMessage(), e);
				return "Error reading log file";
			}
		} else {
			return "Log file not found";
		}

		return fileContent.toString();
	}

	/**
	 * This method is to download the agent log file
	 * @param executionId
	 * @param executionResId
	 * @param fileName
	 * @return Resource
	 */
	@Override
	public Resource downloadAgentLogFile(String executionId, String executionResId, String fileName) {
		LOGGER.info("Inside downloadAgentLogFile method with fileName: {}", fileName);

		// Determine the path for the agent log file
		String baseLogPath = commonService.getBaseLogPath();
		String agentLogsDirectory = commonService.getAgentLogPath(executionId, executionResId, baseLogPath);

		// Use the helper method to get the resource
		return getFileAsResource(agentLogsDirectory, fileName);
	}


	/**
	 * Helper method to retrieve a file as a Resource.
	 *
	 * @param directoryPath The directory where the file is located.
	 * @param fileName      The name of the file to retrieve.
	 * @return Resource representing the file.
	 */
	private Resource getFileAsResource(String directoryPath, String fileName) {
		Path filePath = Paths.get(directoryPath, fileName);

		// Check if the file exists
		if (!Files.exists(filePath)) {
			LOGGER.error("{} not found: {}", "Log file", fileName);
			throw new ResourceNotFoundException("Log file", fileName);
		}

		// Load the resource
		Resource resource;
		try {
			resource = new UrlResource(filePath.toUri());
		} catch (MalformedURLException e) {
			LOGGER.error("Error loading {}: {}", "Log file", e.getMessage(), e);
			throw new RuntimeException("Error loading " + "Log file", e);
		}

		// Check if the resource exists
		if (resource == null || !resource.exists()) {
			LOGGER.error("{} not found: {}", "Log file", fileName);
			throw new ResourceNotFoundException("Log file", fileName);
		}

		return resource;
	}



}
