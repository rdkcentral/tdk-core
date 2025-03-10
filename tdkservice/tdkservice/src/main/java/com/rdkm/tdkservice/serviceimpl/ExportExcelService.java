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
import com.rdkm.tdkservice.dto.ExecutionDetailsResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionResultDTO;
import com.rdkm.tdkservice.dto.ExecutionSummaryResponseDTO;
import com.rdkm.tdkservice.enums.ExecutionOverallResultStatus;
import com.rdkm.tdkservice.enums.ExecutionResultStatus;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.model.*;
import com.rdkm.tdkservice.repository.*;
import com.rdkm.tdkservice.service.IExportExcelService;
import com.rdkm.tdkservice.service.IFileService;
import com.rdkm.tdkservice.service.utilservices.CommonService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import org.apache.poi.common.usermodel.HyperlinkType;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.time.Instant;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

@Service
public class ExportExcelService implements IExportExcelService {

	private static final Logger LOGGER = LoggerFactory.getLogger(ExportExcelService.class);

	@Autowired
	private DeviceRepositroy deviceRepository;

	@Autowired
	private ExecutionRepository executionRepository;

	@Autowired
	private ScriptRepository scriptRepository;

	@Autowired
	private ExecutionResultRepository executionResultRepository;

	@Autowired
	private ExecutionMethodResultRepository executionMethodResultRepository;

	@Autowired
	private ExecutionService executionService;

	@Autowired
	private CommonService commonService;

	@Autowired
	private DeviceStatusService deviceStatusService;

	@Autowired
	private ExecutionResultAnalysisRepository executionResultAnalysisRepository;

	@Autowired
	private ExecutionDeviceRepository executionDeviceRepository;

	@Autowired
	private IFileService fileService;

	@Autowired
	private AppConfig appConfig;

	// Add looger
	private static final Logger logger = LoggerFactory.getLogger(ExportExcelService.class);

	/**
	 * This method used to get execution id
	 *
	 * @param executionId the UUID of the execution
	 * @return
	 */
	@Override
	public Execution getExecutionById(UUID executionId) {
		Execution execution = executionRepository.findById(executionId)
				.orElseThrow(() -> new ResourceNotFoundException("Execution", "id" + executionId));
		return execution;
	}

	/**
	 * Generates an Excel report for the given execution.
	 *
	 * @param execution the execution for which the report is generated
	 * @return a byte array representing the generated Excel report
	 */
	@Override
	public byte[] generateExcelReport(Execution execution) {
		LOGGER.info("Generating Excel report for execution ID: {}", execution.getId());
		// Create a method that give a map of module and execiution Result Id
		Map<String, List<ExecutionResult>> moduleExecutionResultMap = getModuleExecutionResultsMap(execution.getId());
		// Fetch module data
		List<Map<String, Object>> moduleData = getModuleData(execution.getId());

		Workbook workbook = new XSSFWorkbook();
		Sheet summarySheet = workbook.createSheet("Summary");
		int rowNum = 0;

		// Add Device Details at the top
		Map<String, ExecutionSummaryResponseDTO> moduleSummaryMap = executionService
				.getModulewiseExecutionSummary(execution.getId());

		ExecutionSummaryResponseDTO totalSummary = moduleSummaryMap.get(Constants.TOTAL_KEYWORD);
		double overallSuccessPercentage = totalSummary != null ? totalSummary.getSuccessPercentage() : 0.0;

		// Call addDeviceDetails with the percentage
		addDeviceDetails(summarySheet, execution, rowNum, overallSuccessPercentage);

		rowNum += 6; // 5 rows for device details + 1 blank row for spacing

		for (Map.Entry<String, List<ExecutionResult>> entry : moduleExecutionResultMap.entrySet()) {
			String moduleName = entry.getKey();
			List<ExecutionResult> execResults = entry.getValue();
			if (moduleName.equalsIgnoreCase("rdkservices")) {
				List<String> logDatas = new ArrayList<>();
				for (ExecutionResult executionResult : execResults) {
					logDatas.add(executionService.getExecutionLogs(executionResult.getId().toString()));
				}
				rowNum = createConsolidatedSummarySheet(summarySheet, rowNum, logDatas, execution);
				for (ExecutionResult executionResultId : execResults) {
					createTestCaseDetailsSheet(workbook,
							executionService.getExecutionLogs(executionResultId.getId().toString()),
							execution.getCreatedDate(), executionResultId);
				}

			} else {
				// Create Summary Sheet
				createNormalSummarySheet(summarySheet, execution, moduleData, rowNum);
				// Create Module Sheets for each unique module
				if (!moduleData.isEmpty()) {
					Map<String, List<Map<String, Object>>> modulesGrouped = moduleData.stream()
							.collect(Collectors.groupingBy(data -> (String) data.get("moduleName")));

					for (Map.Entry<String, List<Map<String, Object>>> entrys : modulesGrouped.entrySet()) {
						String moduleNames = entrys.getKey();
						if (!moduleNames.equalsIgnoreCase("rdkservices")) {
							List<Map<String, Object>> moduleScripts = entrys.getValue();
							createModuleSheet(moduleScripts, workbook, moduleNames);
						}
					}
				} else {
					logger.warn("No module data available. Skipping module sheet creation.");
				}

			}
		}

		ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
		try {
			workbook.write(outputStream);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		logger.info("Excel file generated with {} sheets.", workbook.getNumberOfSheets());
		return outputStream.toByteArray();
	}

	/**
	 * Get module execution results map
	 *
	 * @param executionId the UUID of the execution
	 * @return map of module and execution result
	 */
	private Map<String, List<ExecutionResult>> getModuleExecutionResultsMap(UUID executionId) {

		LOGGER.info("Fetching Execution for ID: {}", executionId);
		Execution execution = executionRepository.findById(executionId)
				.orElseThrow(() -> new ResourceNotFoundException("Execution", "id" + executionId));
		List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);
		Map<String, List<ExecutionResult>> moduleScriptListMap = new HashMap<>();
		for (ExecutionResult executionResult : executionResults) {

			Script script = scriptRepository.findByName(executionResult.getScript());

			String moduleName = script.getModule().getName();

			if (moduleScriptListMap.containsKey(moduleName)) {
				moduleScriptListMap.get(moduleName).add(executionResult);
			} else {
				List<ExecutionResult> resultList = new ArrayList<>();
				resultList.add(executionResult);
				moduleScriptListMap.put(moduleName, resultList);
			}
		}
		return moduleScriptListMap;

	}

	/**
	 * Create the summary sheet for the given execution.
	 *
	 * @param sheet       the summary sheet
	 * @param execution   the execution
	 * @param summaryData the summary data
	 */
	private void createNormalSummarySheet(Sheet sheet, Execution execution, List<Map<String, Object>> summaryData,
			int rowNum) {
		try {
			String heading = "Module Summary";

			Row rowHead = sheet.createRow(rowNum++);
			Cell headCells = rowHead.createCell(3);
			headCells.setCellValue(heading);
			CellStyle headStyle = sheet.getWorkbook().createCellStyle();
			Font headFont = sheet.getWorkbook().createFont();
			headFont.setUnderline(Font.U_SINGLE);
			headFont.setBold(true);
			headFont.setFontName("Arial");
			headStyle.setFont(headFont);
			headCells.setCellStyle(headStyle);
			rowNum++;

			addTableHeaders(sheet, rowNum++);
			// Add Execution Summary Data
			rowNum = addExecutionSummary(sheet, rowNum, execution);

			// Auto resize columns for summary sheet
			for (int i = 4; i <= 11; i++) { // Adjust columns E to L
				sheet.autoSizeColumn(i);
			}

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * Add device details to the summary sheet.
	 *
	 * @param sheet     the summary sheet
	 * @param execution the execution
	 * @param rowNum    the row number
	 */
	private void addDeviceDetails(Sheet sheet, Execution execution, int rowNum, double overallSuccessPercentage) {
		try {
			String[] deviceHeaders = { "Device", "DeviceIP", "Execution Time (min)", "Image", "Overall Pass %" };
			ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);
			String deviceName = executionDevice != null && executionDevice.getDevice().getName() != null
					? executionDevice.getDevice().getName()
					: "N/A";
			String deviceIp = executionDevice != null && executionDevice.getDevice().getIp() != null
					? executionDevice.getDevice().getIp()
					: "N/A";
			String executionTime = String.valueOf(execution.getExecutionTime());
			String imageName = fileService.getImageName(String.valueOf(execution.getId()));

			if (imageName == null || imageName.isEmpty()) {
				imageName = "Image not available"; // Assign a message if imageName is not found
			}
			String overallPass = String.format("%.2f%%", overallSuccessPercentage);
			String[] deviceValues = { deviceName, deviceIp, executionTime, imageName, overallPass };

			// Create a bold style for headers
			CellStyle boldStyle = sheet.getWorkbook().createCellStyle();
			Font boldFont = sheet.getWorkbook().createFont();
			boldFont.setBold(true);
			boldFont.setFontName("Arial");
			// Set font to bold
			boldStyle.setFont(boldFont);

			for (int i = 0; i < deviceHeaders.length; i++) {
				Row row = sheet.createRow(rowNum++);

				// Create and style header cell
				Cell headerCell = row.createCell(3);
				headerCell.setCellValue(deviceHeaders[i]);
				headerCell.setCellStyle(boldStyle);

				// Create value cell
				row.createCell(4).setCellValue(deviceValues[i]);

				row.getCell(4).setCellStyle(createArialStyle(sheet.getWorkbook()));

			}

			sheet.autoSizeColumn(3);
			sheet.autoSizeColumn(4);

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * Add table headers to the summary sheet.
	 *
	 * @param sheet  the summary sheet
	 * @param rowNum the row number
	 */
	private void addTableHeaders(Sheet sheet, int rowNum) {
		try {
			String[] headers = { "Sl No", "Module", "Executed", "SUCCESS", "FAILURE", "SCRIPT TIME OUT", "N/A",
					"SKIPPED" };
			Row headerRow = sheet.createRow(rowNum);

			// Create header style with bold font
			CellStyle headerStyle = sheet.getWorkbook().createCellStyle();
			Font headerFont = sheet.getWorkbook().createFont();
			headerFont.setBold(true); // Make the font bold
			headerStyle.setFont(headerFont);

			for (int i = 0; i < headers.length; i++) {
				Cell cell = headerRow.createCell(i); // Start from column E
				cell.setCellValue(headers[i]);
				cell.setCellStyle(headerStyle); // Apply bold style
			}

			// Auto resize columns for table headers (E to L)
			for (int i = 0; i <= 7; i++) {
				sheet.autoSizeColumn(i);
			}
			createAndStyleArialHeaders(sheet, rowNum, headers, 0);
		} catch (Exception e) {
			LOGGER.error("Error adding table headers: " + e.getMessage());
		}
	}

	/**
	 * Add execution summary data to the summary sheet.
	 *
	 * @param sheet     the summary sheet
	 * @param rowNum    the row number
	 * @param execution the execution
	 * @return the updated row number
	 */
	private int addExecutionSummary(Sheet sheet, int rowNum, Execution execution) {
		try {
			int slNo = 1;
			UUID executionId = execution.getId();

			// Fetch unique module names
			Set<String> moduleNames = new LinkedHashSet<>(
					executionResultRepository.findDistinctModuleNamesByExecutionId(executionId));
			CreationHelper creationHelper = sheet.getWorkbook().getCreationHelper();
			List<Map<String, Object>> summaryData = new ArrayList<>();

			for (String moduleName : moduleNames) {
				if (!moduleName.equalsIgnoreCase("rdkservices")) {
					Row row = sheet.createRow(rowNum++);

					// Populate Sl No
					row.createCell(0).setCellValue(slNo++);

					// Create and style hyperlink for module name
					Cell moduleCell = row.createCell(1);
					moduleCell.setCellValue(moduleName);

					Hyperlink link = creationHelper.createHyperlink(HyperlinkType.DOCUMENT);
					link.setAddress("'" + moduleName + "'!A1"); // Target module sheet
					moduleCell.setHyperlink(link);

					CellStyle linkStyle = sheet.getWorkbook().createCellStyle();
					Font linkFont = sheet.getWorkbook().createFont();
					linkFont.setUnderline(Font.U_SINGLE);
					linkFont.setColor(IndexedColors.BLUE.getIndex());

					linkFont.setFontName("Arial");
					linkStyle.setFont(linkFont);
					moduleCell.setCellStyle(linkStyle);

					// Fetch execution metrics
					int executed = executionResultRepository.countByExecutionIdAndScriptModuleName(executionId,
							moduleName);
					int success = executionResultRepository.countByExecutionIdAndScriptModuleNameAndResult(executionId,
							moduleName, ExecutionResultStatus.SUCCESS);
					int failure = executionResultRepository.countByExecutionIdAndScriptModuleNameAndResult(executionId,
							moduleName, ExecutionResultStatus.FAILURE);
					int timeout = executionResultRepository.countByExecutionIdAndScriptModuleNameAndResult(executionId,
							moduleName, ExecutionResultStatus.TIMEOUT);
					int notApplicable = executionResultRepository.countByExecutionIdAndScriptModuleNameAndResult(
							executionId, moduleName, ExecutionResultStatus.NA);
					int skipped = executionResultRepository.countByExecutionIdAndScriptModuleNameAndResult(executionId,
							moduleName, ExecutionResultStatus.SKIPPED);

					// Populate other columns
					row.createCell(2).setCellValue(executed);
					row.createCell(3).setCellValue(success);
					row.createCell(4).setCellValue(failure);
					row.createCell(5).setCellValue(timeout);
					row.createCell(6).setCellValue(notApplicable);
					row.createCell(7).setCellValue(skipped);

					// Apply arial font
					for (int i = 2; i < 8; i++) {
						row.getCell(i).setCellStyle(createArialStyle(sheet.getWorkbook()));
					}

					// Add data to summary for totals
					Map<String, Object> rowData = new HashMap<>();
					rowData.put("executed", executed);
					rowData.put("success", success);
					rowData.put("failure", failure);
					rowData.put("timeout", timeout);
					rowData.put("notApplicable", notApplicable);
					rowData.put("skipped", skipped);
					// summary

					summaryData.add(rowData);
				}
			}
			// Auto resize columns
			for (int i = 4; i <= 11; i++) {
				sheet.autoSizeColumn(i);
			}

			// Add total row after all modules
			addTotalRow(sheet, rowNum++, summaryData);

		} catch (Exception e) {
			e.printStackTrace();
		}
		return rowNum;
	}

	/**
	 * Create the module-specific sheet for the given module scripts.
	 *
	 * @param moduleScripts
	 * @param workbook
	 * @param moduleName
	 */
	private void createModuleSheet(List<Map<String, Object>> moduleScripts, Workbook workbook, String moduleName) {
		int rowNum = 0;

		// Create the module-specific sheet
		Sheet moduleSheet = workbook.createSheet(moduleName);

		// Add a "Go to Summary" link at the top
		Row backRow = moduleSheet.createRow(rowNum++);
		Cell backCell = backRow.createCell(0);
		backCell.setCellValue("Go to Summary");

		CreationHelper creationHelper = workbook.getCreationHelper();
		Hyperlink backLink = creationHelper.createHyperlink(HyperlinkType.DOCUMENT);
		backLink.setAddress("'Summary'!A1");
		backCell.setHyperlink(backLink);

		// Create a CellStyle for headers with bold font
		CellStyle headerStyle = workbook.createCellStyle();
		Font headerFont = workbook.createFont();
		headerFont.setBold(true); // Set font to bold
		headerFont.setFontName("Arial");
		headerStyle.setFont(headerFont);

		CellStyle linkStyle = workbook.createCellStyle();
		Font linkFont = workbook.createFont();
		linkFont.setUnderline(Font.U_SINGLE);
		linkFont.setColor(IndexedColors.BLUE.getIndex());
		linkFont.setFontName("Arial");
		linkStyle.setFont(linkFont);

		backCell.setCellStyle(linkStyle);

		// Create headers for the module sheet
		Row headerRow = moduleSheet.createRow(rowNum++);
		String[] headers = { "Sl.No", "Script Name", "Executed", "Status", "Executed On", "Log Data", "Jira ID",
				"Issue Type", "Remarks" };
		for (int i = 0; i < headers.length; i++) {
			Cell cell = headerRow.createCell(i);
			cell.setCellValue(headers[i]);
			cell.setCellStyle(headerStyle);
		}

		// Populate the module sheet with data
		int slNo = 1;
		for (Map<String, Object> result : moduleScripts) {
			Row row = moduleSheet.createRow(rowNum++);
			row.createCell(0).setCellValue(slNo++);
			row.createCell(1).setCellValue((String) result.get("scriptName"));
			row.createCell(2).setCellValue(result.get("executed").toString());
			row.createCell(3).setCellValue(result.get("status").toString());
			row.createCell(4).setCellValue(result.get("executedOn").toString());
			row.createCell(5).setCellValue((String) result.get("logData"));
			row.createCell(6).setCellValue(result.get("jiraId").toString());
			row.createCell(7).setCellValue(result.get("issueType").toString());
			row.createCell(8).setCellValue(result.get("remarks").toString());

			// Apply Arial font to all cells
			for (int i = 0; i < headers.length; i++) {
				row.getCell(i).setCellStyle(createArialStyle(workbook));
			}

		}

		// Adjust column widths
		for (int i = 0; i < headers.length; i++) {
			moduleSheet.autoSizeColumn(i);
		}
	}

	/**
	 * Add total row to the summary sheet.
	 *
	 * @param sheet       the summary sheet
	 * @param rowNum      the row number
	 * @param summaryData the summary data
	 */
	private void addTotalRow(Sheet sheet, int rowNum, List<Map<String, Object>> summaryData) {
		try {
			Row totalRow = sheet.createRow(rowNum);

			int totalScripts = calculateTotal(summaryData, "executed");
			int totalSuccess = calculateTotal(summaryData, "success");
			int totalFailure = calculateTotal(summaryData, "failure");
			int totalTimeout = calculateTotal(summaryData, "timeout");
			int totalNA = calculateTotal(summaryData, "notApplicable");
			int totalSkipped = calculateTotal(summaryData, "skipped");

			totalRow.createCell(0).setCellValue(""); // Blank for Sl No
			totalRow.createCell(1).setCellValue("Total");
			totalRow.createCell(2).setCellValue(totalScripts);
			totalRow.createCell(3).setCellValue(totalSuccess);
			totalRow.createCell(4).setCellValue(totalFailure);
			totalRow.createCell(5).setCellValue(totalTimeout);
			totalRow.createCell(6).setCellValue(totalNA);
			totalRow.createCell(7).setCellValue(totalSkipped);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * Calculate the total for the given key in the summary data.
	 *
	 * @param summaryData the summary data
	 * @param key         the key for which the total is calculated
	 * @return the total value
	 */
	private int calculateTotal(List<Map<String, Object>> summaryData, String key) {
		try {
			return summaryData.stream().mapToInt(data -> {
				Object value = data.getOrDefault(key, 0); // Retrieve the value associated with the key
				if (value instanceof Integer) {
					return (int) value;
				} else {
					System.err.println("Unexpected type for key '" + key + "': " + value.getClass().getName());
					return 0; // Default to 0 for unexpected types
				}
			}).sum();
		} catch (Exception e) {
			System.err.println("Error calculating total for key: " + key + ". " + e.getMessage());
			e.printStackTrace();
			return 0; // Return 0 in case of errors
		}
	}

	/**
	 * Fetch module data for the given execution ID.
	 *
	 * @param executionId the UUID of the execution
	 * @return the list of module data
	 */
	public List<Map<String, Object>> getModuleData(UUID executionId) {
		LOGGER.info("Fetching Execution for ID: {}", executionId);

		Execution execution = executionRepository.findById(executionId)
				.orElseThrow(() -> new ResourceNotFoundException("Execution id ", executionId.toString()));
		List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);
		List<Map<String, Object>> resultDataList = new ArrayList<>();

		for (ExecutionResult result : executionResults) {
			try {
				ExecutionResultAnalysis analysis = executionResultAnalysisRepository.findByExecutionResult(result);
				String scriptName = result.getScript();
				Script script = scriptRepository.findByName(scriptName);

				Map<String, Object> resultData = new HashMap<>();
				resultData.put("executionResultIds", List.of(result.getId().toString()));
				resultData.put("scriptName", scriptName);
				resultData.put("moduleName",
						script != null && script.getModule() != null ? script.getModule().getName() : "Unknown Module");
				resultData.put("executed",
						result.getExecution() != null ? result.getExecution().getResult() : "Unknown Execution Result");
				resultData.put("status", result.getResult());
				resultData.put("executedOn", result.getDateOfExecution() != null ? result.getDateOfExecution() : "N/A");
				resultData.put("executionTime", result.getExecutionTime());

				String logs = executionService.getExecutionLogs(result.getId().toString());
				resultData.put("logData", logs == null || logs.isEmpty() ? null : logs);
				if (analysis != null) {

					resultData.put("jiraId",
							analysis.getAnalysisTicketID() != null ? analysis.getAnalysisTicketID().toString() : "N/A");
					resultData.put("issueType",
							analysis.getAnalysisDefectType().toString() != null
									? analysis.getAnalysisDefectType().toString()
									: "N/A");
					resultData.put("remarks",
							analysis.getAnalysisRemark() != null ? analysis.getAnalysisRemark().toString() : "N/A");
				} else {
					resultData.put("jiraId", "N/A");
					resultData.put("issueType", "N/A");
					resultData.put("remarks", "N/A");

				}
				resultDataList.add(resultData);

			} catch (Exception e) {
				LOGGER.error("Error processing ExecutionResult ID: {}", result.getId(), e);
				e.printStackTrace();
			}
		}

		return resultDataList;
	}

	/**
	 * Generates a combined Excel report for the given list of execution IDs.
	 *
	 * @param executionIds the list of UUIDs of the executions
	 * @return a byte array representing the generated combined Excel report
	 */
	@Override
	public byte[] generateCombinedExcelReport(List<UUID> executionIds) {
		Logger logger = LoggerFactory.getLogger(getClass());

		// Fetch filtered and prioritized module data for all execution IDs
		logger.debug("Fetching filtered and prioritized combined module data.");
		List<Map<String, Object>> combinedModuleData = getFilteredCombinedModuleData(executionIds);
		logger.debug("Fetched combined module data: {}", combinedModuleData);

		// Fetch device details for the execution IDs
		logger.info("Fetching device details for execution IDs.");
		List<Map<String, Object>> deviceDetails = getDeviceDetails(executionIds);
		logger.info("Fetched device details: {}", deviceDetails);

		try (Workbook workbook = new XSSFWorkbook()) {
			// Create Summary Sheet
			logger.info("Creating summary sheet.");
			Sheet summarySheet = workbook.createSheet("Summary");

			// Pass device details to the summary sheet creation
			createCombinedSummarySheet(summarySheet, executionIds, deviceDetails);

			// Create Module Sheets
			if (!combinedModuleData.isEmpty()) {
				logger.debug("Creating module sheets for {} modules.", combinedModuleData.size());
				Map<String, List<Map<String, Object>>> modulesGrouped = combinedModuleData.stream()
						.collect(Collectors.groupingBy(data -> (String) data.get("moduleName")));
				logger.info("Module data: {}", modulesGrouped);

				for (Map.Entry<String, List<Map<String, Object>>> entry : modulesGrouped.entrySet()) {
					String moduleName = entry.getKey();
					List<Map<String, Object>> moduleScripts = entry.getValue();
					logger.info("Creating sheet for module: {} with {} scripts.", moduleName, moduleScripts.size());

					createCombinedModuleSheet(moduleScripts, workbook);
				}
			} else {
				logger.warn("No module data available. Skipping module sheet creation.");
			}

			// Write workbook to a byte array
			logger.debug("Writing workbook to byte array.");
			ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
			workbook.write(outputStream);
			logger.info("Excel file generated with {} sheets.", workbook.getNumberOfSheets());
			return outputStream.toByteArray();
		} catch (IOException e) {
			logger.error("Error generating Excel file", e);
		}
		return new byte[0];
	}

	/**
	 * Fetch filtered and prioritized module data for all execution IDs.
	 *
	 * @param executionIds the list of UUIDs of the executions
	 * @return the list of filtered and prioritized module data
	 */
	private void createCombinedSummarySheet(Sheet sheet, List<UUID> executionIds,
			List<Map<String, Object>> deviceDetails) {
		try {
			int rowNum = 0;

			// Fetch and add Device Details to the Summary Sheet
			rowNum = addCombinedDeviceDetails(sheet, rowNum, deviceDetails);

			// Add Execution Summary Data
			rowNum = addCombinedExecutionSummary(sheet, rowNum, executionIds);

			// Auto resize columns for summary sheet
			for (int i = 4; i <= 11; i++) { // Adjust columns E to L
				sheet.autoSizeColumn(i);
			}

			LOGGER.info("Summary sheet created successfully.");
		} catch (Exception e) {
			LOGGER.error("Error creating summary sheet: {}", e.getMessage(), e);
		}
	}

	/**
	 * Fetch and add device details to the combined summary sheet.
	 *
	 * @param sheet         the summary sheet
	 * @param rowNum        the row number
	 * @param deviceDetails the list of device details
	 * @return the updated row number
	 */
	private int addCombinedExecutionSummary(Sheet sheet, int rowNum, List<UUID> executionIds) {
		try {
			int slNo = 1;

			// Fetch filtered and prioritized module data
			List<Map<String, Object>> filteredModuleData = getFilteredCombinedModuleData(executionIds);
			if (filteredModuleData.isEmpty()) {
				LOGGER.warn("No filtered module data found for execution IDs: {}", executionIds);
			}

			// Group by module name
			Map<String, List<Map<String, Object>>> moduleDataGrouped = filteredModuleData.stream()
					.collect(Collectors.groupingBy(data -> (String) data.get("moduleName")));

			CreationHelper creationHelper = sheet.getWorkbook().getCreationHelper();
			List<Map<String, Object>> summaryData = new ArrayList<>();

			// Add Execution Summary Table Headers
			Row headerRow = sheet.createRow(rowNum++);
			String[] headers = { "Sl No", "Module", "Executed", "SUCCESS", "FAILURE", "SCRIPT TIME OUT", "N/A",
					"SKIPPED" };
			for (int i = 0; i < headers.length; i++) {
				Cell cell = headerRow.createCell(4 + i); // Start from column F
				cell.setCellValue(headers[i]);

				// Style the headers (optional)
				CellStyle headerStyle = sheet.getWorkbook().createCellStyle();
				Font headerFont = sheet.getWorkbook().createFont();
				headerFont.setBold(true);
				headerStyle.setFont(headerFont);
				cell.setCellStyle(headerStyle);
			}

			for (Map.Entry<String, List<Map<String, Object>>> entry : moduleDataGrouped.entrySet()) {
				String moduleName = entry.getKey();
				List<Map<String, Object>> moduleScripts = entry.getValue();

				Row row = sheet.createRow(rowNum++);

				// Populate Sl No
				row.createCell(4).setCellValue(slNo++);

				// Create and style hyperlink for module name
				Cell moduleCell = row.createCell(5);
				moduleCell.setCellValue(moduleName);

				Hyperlink link = creationHelper.createHyperlink(HyperlinkType.DOCUMENT);
				link.setAddress("'" + moduleName + "'!A1"); // Target module sheet
				moduleCell.setHyperlink(link);

				CellStyle linkStyle = sheet.getWorkbook().createCellStyle();
				Font linkFont = sheet.getWorkbook().createFont();
				linkFont.setUnderline(Font.U_SINGLE);
				linkFont.setColor(IndexedColors.BLUE.getIndex());
				linkStyle.setFont(linkFont);
				moduleCell.setCellStyle(linkStyle);

				// Initialize counters
				int executed = moduleScripts.size();
				int success = 0;
				int failure = 0;
				int timeout = 0;
				int notApplicable = 0;
				int skipped = 0;

				// Count statuses
				for (Map<String, Object> scriptData : moduleScripts) {
					ExecutionResultStatus status = (ExecutionResultStatus) scriptData.get("status");
					switch (status) {
					case SUCCESS:
						success++;
						break;
					case FAILURE:
						failure++;
						break;
					case TIMEOUT:
						timeout++;
						break;
					case NA:
						notApplicable++;
						break;
					case SKIPPED:
						skipped++;
						break;
					default:
						LOGGER.warn("Unknown result status: {}", status);
					}
				}

				// Populate columns
				row.createCell(6).setCellValue(executed);
				row.createCell(7).setCellValue(success);
				row.createCell(8).setCellValue(failure);
				row.createCell(9).setCellValue(timeout);
				row.createCell(10).setCellValue(notApplicable);
				row.createCell(11).setCellValue(skipped);

				// Add data to summary for totals
				Map<String, Object> rowData = new HashMap<>();
				rowData.put("executed", executed);
				rowData.put("success", success);
				rowData.put("failure", failure);
				rowData.put("timeout", timeout);
				rowData.put("notApplicable", notApplicable);
				rowData.put("skipped", skipped);
				summaryData.add(rowData);

			}

			// Add total row after all modules
			addTotalRow(sheet, rowNum++, summaryData);

			// Auto resize columns
			for (int i = 4; i <= 11; i++) {
				sheet.autoSizeColumn(i);
			}

		} catch (Exception e) {
			e.printStackTrace();
		}
		return rowNum;
	}

	/**
	 * Fetch and add device details to the combined summary sheet.
	 *
	 * @param sheet         the summary sheet
	 * @param rowNum        the row number
	 * @param deviceDetails the list of device details
	 * @return the updated row number
	 */
	private void createCombinedModuleSheet(List<Map<String, Object>> moduleScripts, Workbook workbook) {
		int rowNum = 0;

		// Extract and map the module name from the first result
		if (moduleScripts.isEmpty()) {
			LOGGER.warn("No scripts available for module sheet population.");
			return;
		}
		String dynamicModuleName = (String) moduleScripts.get(0).get("moduleName");
		if (dynamicModuleName == null || dynamicModuleName.isEmpty()) {
			LOGGER.error("Module name is missing or null in the script data.");
			return;
		}

		// Fetch or create the module sheet
		Sheet moduleSheet = workbook.getSheet(dynamicModuleName);
		if (moduleSheet == null) {
			moduleSheet = workbook.createSheet(dynamicModuleName);
		}

		// Add a "Back to Summary" link at the top (if not already added)
		if (moduleSheet.getRow(0) == null) {
			Row backRow = moduleSheet.createRow(rowNum++);
			Cell backCell = backRow.createCell(0);
			backCell.setCellValue("Back to Summary");
			addHyperlinkToCell(backCell, "'Summary'!A1", workbook);
		}

		// Create headers for the module sheet (if not already created)
		if (moduleSheet.getRow(1) == null) {
			String[] headers = { "Sl.No", "Script Name", "Executed", "Status", "Executed On", "Log Data" };
			createAndStyleHeaders(moduleSheet, rowNum++, headers, 0);
		}

		// Populate the module sheet with data
		int slNo = 1;
		for (Map<String, Object> result : moduleScripts) {
			Row row = moduleSheet.createRow(rowNum++);
			Object[] rowData = { slNo++, result.get("scriptName"), result.get("executed"), result.get("status"),
					result.get("executedOn"), result.get("logData") };
			populateRowData(row, rowData);
		}

		// Adjust column widths
		autoSizeColumns(moduleSheet, 0, 5);
	}

	/**
	 * Creates and styles the header row for a given sheet.
	 *
	 * @param sheet       the sheet where the headers will be created
	 * @param rowNum      the row number where the headers will be placed
	 * @param headers     an array of header names
	 * @param startColumn the starting column index for the headers
	 */
	private void createAndStyleHeaders(Sheet sheet, int rowNum, String[] headers, int startColumn) {
		Row headerRow = sheet.createRow(rowNum);
		CellStyle headerStyle = sheet.getWorkbook().createCellStyle();
		Font headerFont = sheet.getWorkbook().createFont();
		headerFont.setBold(true);
		headerStyle.setFont(headerFont);

		for (int i = 0; i < headers.length; i++) {
			Cell cell = headerRow.createCell(startColumn + i);
			cell.setCellValue(headers[i]);
			cell.setCellStyle(headerStyle);
		}
	}

	/**
	 * Adds a hyperlink to the given cell.
	 *
	 * @param cell     the cell where the hyperlink will be added
	 * @param address  the target address for the hyperlink
	 * @param workbook the workbook where the hyperlink will be created
	 */
	private void addHyperlinkToCell(Cell cell, String address, Workbook workbook) {
		CreationHelper creationHelper = workbook.getCreationHelper();
		Hyperlink link = creationHelper.createHyperlink(HyperlinkType.DOCUMENT);
		link.setAddress(address);
		cell.setHyperlink(link);

		CellStyle linkStyle = workbook.createCellStyle();
		Font linkFont = workbook.createFont();
		linkFont.setUnderline(Font.U_SINGLE);
		linkFont.setColor(IndexedColors.BLUE.getIndex());
		linkStyle.setFont(linkFont);
		cell.setCellStyle(linkStyle);
	}

	/**
	 * Populates the given row with the provided data.
	 *
	 * @param row  the row to be populated
	 * @param data the data to be added to the row
	 */
	private void populateRowData(Row row, Object[] data) {
		for (int i = 0; i < data.length; i++) {
			if (data[i] instanceof String) {
				row.createCell(i).setCellValue((String) data[i]);
			} else if (data[i] instanceof Integer) {
				row.createCell(i).setCellValue((Integer) data[i]);
			} else if (data[i] instanceof Double) {
				row.createCell(i).setCellValue((Double) data[i]);
			} else {
				row.createCell(i).setCellValue(data[i] != null ? data[i].toString() : "N/A");
			}
		}
	}

	/**
	 * Auto resizes the columns in the given sheet.
	 *
	 * @param sheet       the sheet where the columns will be resized
	 * @param startColumn the starting column index
	 * @param endColumn   the ending column index
	 */
	private void autoSizeColumns(Sheet sheet, int startColumn, int endColumn) {
		for (int i = startColumn; i <= endColumn; i++) {
			sheet.autoSizeColumn(i);
		}
	}

	/**
	 * Fetch and add device details to the combined summary sheet.
	 *
	 * @param sheet         the summary sheet
	 * @param rowNum        the row number
	 * @param deviceDetails the list of device details
	 * @return the updated row number
	 */
	public List<Map<String, Object>> getFilteredCombinedModuleData(List<UUID> executionIds) {
		LOGGER.info("Processing execution results for execution IDs: {}", executionIds);

		List<Map<String, Object>> resultDataList = new ArrayList<>();
		Map<String, Map<String, ExecutionResult>> prioritizedResults = new LinkedHashMap<>();

		// Validate device details
		if (!validateDeviceIPs(executionIds)) {
			LOGGER.warn("Devices across executions do not have the same IP address. Skipping comparison.");
			return resultDataList;
		}

		// Fetch and prioritize execution results
		for (UUID executionId : executionIds) {
			processExecutionResults(executionId, prioritizedResults);
		}

		// Convert prioritized results into final output
		return buildResultDataList(prioritizedResults);
	}

	/**
	 * Validates if the devices across executions have the same IP address.
	 *
	 * @param executionIds the list of execution IDs
	 * @return true if the devices have the same IP address, false otherwise
	 */
	private boolean validateDeviceIPs(List<UUID> executionIds) {
		List<Map<String, Object>> deviceDetailsList = getDeviceDetails(executionIds);
		return areDevicesIdenticalByIP(deviceDetailsList);
	}

	/**
	 * Checks if the devices across executions have the same IP address.
	 *
	 * @param deviceDetailsList the list of device details
	 * @return true if the devices have the same IP address, false otherwise
	 */
	private void processExecutionResults(UUID executionId,
			Map<String, Map<String, ExecutionResult>> prioritizedResults) {
		LOGGER.info("Processing execution with ID: {}", executionId);

		Execution execution = executionRepository.findById(executionId).orElseThrow(() -> {
			return new ResourceNotFoundException("Execution", "id " + executionId);
		});

		List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);

		for (ExecutionResult result : executionResults) {
			String scriptName = result.getScript();
			String moduleName = scriptRepository.findByName(scriptName).getModule().getName();

			prioritizedResults.putIfAbsent(moduleName, new HashMap<>());
			prioritizeResult(prioritizedResults.get(moduleName), scriptName, result);
		}
	}

	/**
	 * Prioritizes the execution result based on status and execution date.
	 *
	 * @param moduleResults the map of module results
	 * @param scriptName    the script name
	 * @param newResult     the new execution result
	 */
	private void prioritizeResult(Map<String, ExecutionResult> moduleResults, String scriptName,
			ExecutionResult newResult) {
		if (moduleResults.containsKey(scriptName)) {
			ExecutionResult existingResult = moduleResults.get(scriptName);
			ExecutionResultStatus existingStatus = existingResult.getResult();
			ExecutionResultStatus newStatus = newResult.getResult();

			// Prioritize based on status and execution date
			if (newStatus == ExecutionResultStatus.SUCCESS || (existingStatus != ExecutionResultStatus.SUCCESS
					&& newResult.getDateOfExecution().isAfter(existingResult.getDateOfExecution()))) {
				moduleResults.put(scriptName, newResult);
			}
		} else {
			LOGGER.info("Adding new result for script: {}", scriptName);
			moduleResults.put(scriptName, newResult);
		}
	}

	/**
	 * Builds the final result data list from the prioritized results.
	 *
	 * @param prioritizedResults the prioritized results
	 * @return the list of result data
	 */
	private List<Map<String, Object>> buildResultDataList(
			Map<String, Map<String, ExecutionResult>> prioritizedResults) {
		List<Map<String, Object>> resultDataList = new ArrayList<>();

		for (Map.Entry<String, Map<String, ExecutionResult>> moduleEntry : prioritizedResults.entrySet()) {
			String moduleName = moduleEntry.getKey();

			for (ExecutionResult prioritizedResult : moduleEntry.getValue().values()) {
				Map<String, Object> resultData = new HashMap<>();
				resultData.put("moduleName", moduleName);
				resultData.put("scriptName", prioritizedResult.getScript());
				resultData.put("executed", prioritizedResult.getExecution().getResult());
				resultData.put("status", prioritizedResult.getResult());
				resultData.put("executedOn", Optional.ofNullable(prioritizedResult.getDateOfExecution())
						.map(date -> date.toString()).orElse("N/A"));
				resultData.put("logData", executionService.getExecutionLogs(prioritizedResult.getId().toString()));

				resultDataList.add(resultData);
			}
		}
		return resultDataList;
	}

	/**
	 * This method to get the device details
	 *
	 * @param executionIds
	 * @return
	 */
	private List<Map<String, Object>> getDeviceDetails(List<UUID> executionIds) {
		LOGGER.info("Fetching device details for execution IDs: {}", executionIds);

		List<Map<String, Object>> deviceDetailsList = new ArrayList<>();

		for (UUID executionId : executionIds) {
			try {
				// Fetch Execution object
				Execution execution = executionRepository.findById(executionId)
						.orElseThrow(() -> new ResourceNotFoundException("Execution", "id " + executionId));

				// Fetch ExecutionDevice details associated with the execution
				ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);

				// Fetch Device details
				Device device = executionDevice.getDevice();

				// Fetch execution results
				List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);

				// Calculate pass rate
				int totalExecutionCount = executionResults.size();
				int totalSuccessCount = (int) executionResults.stream()
						.filter(result -> result.getResult() == ExecutionResultStatus.SUCCESS).count();
				int totalNaCount = (int) executionResults.stream()
						.filter(result -> result.getResult() == ExecutionResultStatus.NA).count();

				double overallPassPercent = 0;
				if ((totalExecutionCount - totalNaCount) != 0) {
					overallPassPercent = ((double) totalSuccessCount * 100) / (totalExecutionCount - totalNaCount);
				}

				// Prepare device details map
				Map<String, Object> deviceDetails = new HashMap<>();
				deviceDetails.put("device", device.getName());
				deviceDetails.put("deviceIp", device.getIp());
				deviceDetails.put("executionTime", execution.getExecutionTime());
				deviceDetails.put("overallPassPercent", overallPassPercent);
				deviceDetails.put("deviceImage", executionDevice.getBuildName());
				deviceDetails.put("totalExecutionCount", totalExecutionCount);
				deviceDetails.put("totalSuccessCount", totalSuccessCount);
				deviceDetails.put("totalNaCount", totalNaCount);

				// Add to list
				deviceDetailsList.add(deviceDetails);
			} catch (ResourceNotFoundException ex) {
				LOGGER.error("Resource not found for execution ID: {}. Exception: {}", executionId, ex.getMessage());
			}
		}
		return deviceDetailsList;
	}

	/**
	 * Adds combined device details to the sheet.
	 *
	 * @param sheet         the summary sheet
	 * @param rowNum        the row number
	 * @param deviceDetails the list of device details
	 * @return the updated row number
	 */
	private int addCombinedDeviceDetails(Sheet sheet, int rowNum, List<Map<String, Object>> deviceDetails) {
		LOGGER.info("Starting to add combined device details to the sheet at row number: {}", rowNum);

		if (deviceDetails == null || deviceDetails.isEmpty()) {
			LOGGER.info("No device details available to add. Exiting the method.");
			return rowNum;
		}

		// Consolidate data into lists to maintain all details
		List<String> devices = new ArrayList<>();
		List<String> deviceIPs = new ArrayList<>();
		List<Double> executionTimes = new ArrayList<>();
		List<String> images = new ArrayList<>();
		int totalExecutionCount = 0;
		int totalSuccessCount = 0;
		int totalNaCount = 0;

		for (Map<String, Object> device : deviceDetails) {
			devices.add((String) device.get("device"));
			deviceIPs.add((String) device.get("deviceIp"));
			executionTimes.add((Double) device.get("executionTime"));
			images.add((String) device.get("deviceImage"));

			// Accumulate totals for overall percentage calculation
			totalExecutionCount += (int) device.get("totalExecutionCount");
			totalSuccessCount += (int) device.get("totalSuccessCount");
			totalNaCount += (int) device.get("totalNaCount");
		}

		// Write consolidated data to the sheet
		String[] headers = { "Device", "DeviceIP", "Execution Time (min)", "Image" };
		String[] values = { devices.toString(), deviceIPs.toString(), executionTimes.toString(), images.toString() };

		for (int i = 0; i < headers.length; i++) {
			LOGGER.debug("Writing header '{}' and value '{}' to the sheet at row number: {}", headers[i], values[i],
					rowNum);

			Row row = sheet.createRow(rowNum++);
			Cell headerCell = row.createCell(4); // Header in Column F
			headerCell.setCellValue(headers[i]);
			headerCell.setCellStyle(createBoldCellStyle(sheet.getWorkbook())); // Apply bold style to headers

			row.createCell(5).setCellValue(values[i]); // Value in Column G
		}

		// Calculate overall success rate
		double overallSuccessRate = 0;
		if ((totalExecutionCount - totalNaCount) != 0) {
			overallSuccessRate = ((double) totalSuccessCount * 100) / (totalExecutionCount - totalNaCount);
		}

		// Add overall success rate to the sheet
		Row overallRow = sheet.createRow(rowNum++);
		Cell overallHeaderCell = overallRow.createCell(4); // Header in Column F
		overallHeaderCell.setCellValue("Overall Pass %");
		overallHeaderCell.setCellStyle(createBoldCellStyle(sheet.getWorkbook()));
		overallRow.createCell(5).setCellValue(overallSuccessRate + "%");

		return rowNum;
	}

	/**
	 * Creates a bold cell style for the given workbook.
	 *
	 * @param workbook the workbook
	 * @return the bold cell style
	 */
	private CellStyle createBoldCellStyle(Workbook workbook) {
		CellStyle headerStyle = workbook.createCellStyle();
		Font headerFont = workbook.createFont();
		headerFont.setBold(true);
		headerStyle.setFont(headerFont);
		return headerStyle;
	}

	/**
	 * Checks if the devices across executions have the same IP address.
	 *
	 * @param deviceDetailsList the list of device details
	 * @return true if the devices have the same IP address, false otherwise
	 */
	private boolean areDevicesIdenticalByIP(List<Map<String, Object>> deviceDetailsList) {
		if (deviceDetailsList.isEmpty()) {
			LOGGER.warn("No device details found.");
			return false;
		}
		// Extract the IP address from the first device
		String referenceIp = (String) deviceDetailsList.get(0).get("deviceIp");
		// Check if all device IPs match the reference IP
		boolean allMatch = deviceDetailsList.stream().allMatch(details -> referenceIp.equals(details.get("deviceIp")));

		if (!allMatch) {
			LOGGER.warn("Device IP mismatch detected.");
		}

		return allMatch;
	}

	/**
	 * Generates a raw report for the given execution ID.
	 *
	 * @param executionId the UUID of the execution
	 * @return a byte array representing the generated raw report
	 */
	public byte[] generateRawReport(UUID executionId) {
		LOGGER.info("Generating raw report for execution ID: {}", executionId);

		// Fetch module data using existing logic
		List<Map<String, Object>> moduleData = getModuleData(executionId);

		try (Workbook workbook = new XSSFWorkbook()) {
			// Create a sheet for the raw report
			Sheet rawSheet = workbook.createSheet("Raw Report");
			int rowNum = 0;

			// Add device details
			Execution execution = executionRepository.findById(executionId)
					.orElseThrow(() -> new ResourceNotFoundException("Execution", executionId.toString()));
			addRawReportDeviceDetails(rawSheet, execution);
			rowNum += 5; // Adjust rowNum after adding device details
			rowNum++; // Add an extra blank row

			// Add "Summary" section
			rowNum++;
			Row emptyRowBefore = rawSheet.createRow(rowNum++);
			emptyRowBefore.createCell(0).setCellValue("");
			CellStyle boldStyle = workbook.createCellStyle();
			Font boldFont = workbook.createFont();
			boldFont.setBold(true);
			boldStyle.setFont(boldFont);

			Row summaryRow = rawSheet.createRow(rowNum++);
			Cell summaryCell = summaryRow.createCell(0);
			summaryCell.setCellValue("Summary");
			summaryCell.setCellStyle(boldStyle);
			rowNum++;

			// Process each module
			for (Map<String, Object> module : moduleData) {

				// Add module-level details
				Row row = rawSheet.createRow(rowNum++);
				row.createCell(0).setCellValue("Module Name");
				row.createCell(1).setCellValue((String) module.get("moduleName"));

				row = rawSheet.createRow(rowNum++);
				row.createCell(0).setCellValue("Script Name");
				row.createCell(1).setCellValue((String) module.get("scriptName"));

				row = rawSheet.createRow(rowNum++);
				row.createCell(0).setCellValue("Execution Status");
				row.createCell(1).setCellValue(module.get("status").toString());

				row = rawSheet.createRow(rowNum++);
				row.createCell(0).setCellValue("Execution Time");
				row.createCell(1).setCellValue(module.get("executionTime").toString());

				// Handle multiple executionResultIds
				List<String> executionResultIds = (List<String>) module.get("executionResultIds");
				LOGGER.info("Processing executionResultIds: {}", executionResultIds);

				if (executionResultIds != null && !executionResultIds.isEmpty()) {
					for (String executionResultId : executionResultIds) {
						Optional<ExecutionResult> executionResultOpt = executionResultRepository
								.findById(UUID.fromString(executionResultId));

						if (executionResultOpt.isPresent()) {
							ExecutionResult executionResult = executionResultOpt.get();
							LOGGER.info("Found ExecutionResult for ID: {}", executionResultId);

							// Fetch ExecutionMethodResults based on ExecutionResult
							List<ExecutionMethodResult> executionMethodResultList = executionMethodResultRepository
									.findByExecutionResult(executionResult);

							if (executionMethodResultList != null && !executionMethodResultList.isEmpty()) {
								row = rawSheet.createRow(rowNum++);
								row.createCell(0).setCellValue("Function Details");

								for (ExecutionMethodResult executionMethodResultInstance : executionMethodResultList) {
									String functionName = executionMethodResultInstance.getFunctionName();
									String functionDetails = getFunctionDetails(executionMethodResultInstance,
											functionName);

									// Add function details to the report
									row = rawSheet.createRow(rowNum++);
									row.createCell(0).setCellValue("Function: " + functionName);
									row.createCell(1).setCellValue(functionDetails);
								}
							} else {
								LOGGER.warn("No ExecutionMethodResults found for ExecutionResult ID: {}",
										executionResultId);
							}
						} else {
							LOGGER.warn("ExecutionResult not found for executionResultId: {}", executionResultId);
						}
					}
				} else {
					LOGGER.warn("No executionResultIds found for module: {}", module.get("moduleName"));
				}

				// Add log data after function details
				row = rawSheet.createRow(rowNum++);
				row.createCell(0).setCellValue("Log Data");
				String logData = (String) module.get("logData");
				row.createCell(1).setCellValue(logData);

				// Auto-size columns
				for (int i = 0; i < 2; i++) {
					rawSheet.autoSizeColumn(i);
				}
			}

			// Write workbook to byte array
			try (ByteArrayOutputStream outputStream = new ByteArrayOutputStream()) {
				workbook.write(outputStream);
				return outputStream.toByteArray();
			}
		} catch (IOException e) {
			LOGGER.error("Error writing workbook to output stream", e);
		}

		return new byte[0];
	}

	/**
	 * This method used to get function details
	 *
	 * @param executionMethodResultInstance
	 * @param functionName
	 * @return
	 */
	private static String getFunctionDetails(ExecutionMethodResult executionMethodResultInstance, String functionName) {
		String expectedResult = String.valueOf(executionMethodResultInstance.getExpectedResult());
		String actualResult = String.valueOf(executionMethodResultInstance.getActualResult());
		String functionStatus = String.valueOf(executionMethodResultInstance.getMethodResult());

		// Create the key-value pair for the function details
		return String.format("Expected Result: %s, Actual Result: %s, Function Status: %s", expectedResult,
				actualResult, functionStatus);
	}

	/**
	 * Adds device details to the raw report sheet.
	 *
	 * @param sheet     the raw report sheet
	 * @param execution the execution
	 */
	private void addRawReportDeviceDetails(Sheet sheet, Execution execution) {
		try {
			LOGGER.info("Adding device details for execution: {}", execution.getId());

			String[] deviceHeaders = { "Device", "DeviceIP", "Execution Time (min)", "Image", "Overall Pass %" };
			ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);
			Map<String, ExecutionSummaryResponseDTO> moduleSummaryMap = executionService
					.getModulewiseExecutionSummary(execution.getId());

			ExecutionSummaryResponseDTO totalSummary = moduleSummaryMap.get(Constants.TOTAL_KEYWORD);
			double overallSuccessPercentage = totalSummary != null ? totalSummary.getSuccessPercentage() : 0.0;

			String deviceName = executionDevice != null && executionDevice.getDevice() != null
					? executionDevice.getDevice().getName()
					: "N/A";
			String deviceIp = executionDevice != null && executionDevice.getDevice() != null
					? executionDevice.getDevice().getIp()
					: "N/A";
			String executionTime = String.valueOf(execution.getExecutionTime());
			String imageName = executionDevice != null ? executionDevice.getBuildName() : null; // Placeholder, replace
			// with actual data if
			// available
			String overallPass = String.format("%.2f%%", overallSuccessPercentage);

			String[] deviceValues = { deviceName, deviceIp, executionTime, imageName, overallPass };

			// Create a bold style for headers
			CellStyle boldStyle = sheet.getWorkbook().createCellStyle();
			Font boldFont = sheet.getWorkbook().createFont();
			boldFont.setBold(true); // Set font to bold
			boldStyle.setFont(boldFont);

			// Ensure device details start from row 3
			int rowNum = 3;

			for (int i = 0; i < deviceHeaders.length; i++) {
				Row row = sheet.createRow(rowNum++);

				// Create and style header cell
				Cell headerCell = row.createCell(0); // Column A (index 0)
				headerCell.setCellValue(deviceHeaders[i]);
				headerCell.setCellStyle(boldStyle);

				// Create value cell
				row.createCell(1).setCellValue(deviceValues[i]); // Column B (index 1)
			}

			// Auto resize columns for device details (A and B)
			sheet.autoSizeColumn(0); // Column A
			sheet.autoSizeColumn(1); // Column B
		} catch (Exception e) {
			LOGGER.error("Error adding device details: {}", e.getMessage(), e);
		}
	}

	/**
	 * Generates an XML report for the given execution.
	 *
	 * @param execution the execution
	 * @return the XML report as a byte array
	 */
	public byte[] generateXmlReport(Execution execution) throws ParserConfigurationException, TransformerException {
		DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder docBuilder = docFactory.newDocumentBuilder();

		// Root element
		Document doc = docBuilder.newDocument();
		Element rootElement = doc.createElement("executionResult");
		rootElement.setAttribute("name", execution.getName());
		rootElement.setAttribute("status", execution.getExecutionStatus().toString());
		doc.appendChild(rootElement);

		ExecutionDevice executionDevice = executionDeviceRepository.findByExecution(execution);
		// Device element
		Element device = doc.createElement("device");
		device.setAttribute("name", executionDevice.getDevice().getName());
		device.setAttribute("deviceIp", executionDevice.getDevice().getIp());
		device.setAttribute("executiondate", execution.getCreatedDate().toString());
		device.setAttribute("timetakentoexecute", String.valueOf(execution.getExecutionTime()));
		device.setAttribute("status", execution.getExecutionStatus().toString());
		rootElement.appendChild(device);

		// Fetch summary details
		ExecutionSummaryResponseDTO summaryDetails = executionService.getExecutionSummary(execution);

		// Summary element
		Element summary = doc.createElement("Summary");
		summary.appendChild(
				createElementWithText(doc, "TotalScripts", String.valueOf(summaryDetails.getTotalScripts())));
		summary.appendChild(createElementWithText(doc, "Executed", String.valueOf(summaryDetails.getExecuted())));
		summary.appendChild(createElementWithText(doc, "Success", String.valueOf(summaryDetails.getSuccess())));
		summary.appendChild(createElementWithText(doc, "Failure", String.valueOf(summaryDetails.getFailure())));
		summary.appendChild(createElementWithText(doc, "NotApplicable", String.valueOf(summaryDetails.getNa())));
		summary.appendChild(createElementWithText(doc, "Pending", String.valueOf(summaryDetails.getPending())));
		summary.appendChild(createElementWithText(doc, "ScriptTimedOut", String.valueOf(summaryDetails.getTimeout())));
		device.appendChild(summary);

		// Fetch execution results
		List<ExecutionResultDTO> executionResults = executionService.getExecutionResults(execution);

		// Scripts element
		for (ExecutionResultDTO executionResult : executionResults) {
			Element scripts = doc.createElement("scripts");
			scripts.setAttribute("name", executionResult.getName());
			scripts.setAttribute("status", executionResult.getStatus());
			scripts.setAttribute("scriptexecutiontime", String.valueOf(execution.getExecutionTime()));
			device.appendChild(scripts);

			List<ExecutionMethodResult> executionMethodResultList = executionMethodResultRepository
					.findByExecutionResult(MapperUtils.convertToExecutionResult(executionResult)); // Fetch function
			// details

			for (ExecutionMethodResult executionMethodResultInstance : executionMethodResultList) {
				String functionName = executionMethodResultInstance.getFunctionName();

				Element function = doc.createElement("function");
				function.setAttribute("name", functionName); // Use the functionName directly for the attribute.

// Extract individual details from getFunctionDetails
				String expectedResultDetail = String.valueOf(executionMethodResultInstance.getExpectedResult());
				String actualResultDetail = String.valueOf(executionMethodResultInstance.getActualResult());
				String functionStatusDetail = String.valueOf(executionMethodResultInstance.getMethodResult());

// Map each detail to XML child nodes
				Element expectedResult = doc.createElement("expectedResult");
				expectedResult.appendChild(doc.createTextNode(expectedResultDetail));
				function.appendChild(expectedResult);

				Element actualResult = doc.createElement("actualResult");
				actualResult.appendChild(doc.createTextNode(actualResultDetail));
				function.appendChild(actualResult);

				Element functionStatus = doc.createElement("functionStatus");
				functionStatus.appendChild(doc.createTextNode(functionStatusDetail));
				function.appendChild(functionStatus);

				scripts.appendChild(function);

			}

			// LogData element
			Element logData = doc.createElement("logData");
			logData.appendChild(doc.createTextNode(
					executionService.getExecutionLogs(String.valueOf(executionResult.getExecutionResultID()))));
			scripts.appendChild(logData);
		}

		// Convert the document to a byte array
		TransformerFactory transformerFactory = TransformerFactory.newInstance();
		Transformer transformer = transformerFactory.newTransformer();
		transformer.setOutputProperty(OutputKeys.INDENT, "yes");
		DOMSource source = new DOMSource(doc);
		ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
		StreamResult result = new StreamResult(outputStream);
		transformer.transform(source, result);

		return outputStream.toByteArray();
	}

	/**
	 * Creates an XML element with the given tag name and text content.
	 *
	 * @param doc         the document
	 * @param tagName     the tag name
	 * @param textContent the text content
	 * @return the created element
	 */
	private Element createElementWithText(Document doc, String tagName, String textContent) {
		Element element = doc.createElement(tagName);
		element.appendChild(doc.createTextNode(textContent));
		return element;
	}

	/**
	 * Adds logs to the ZIP file for a given script.
	 *
	 * @param zipOutputStream the ZIP output stream
	 * @param result          the execution result
	 * @param script          the script
	 * @param executionId     the execution ID
	 * @throws IOException if an I/O error occurs
	 */
	private void addLogsToZip(ZipOutputStream zipOutputStream, ExecutionResult result, Script script, UUID executionId)
			throws IOException {
		String scriptName = result.getScript();
		String logData = executionService.getExecutionLogs(String.valueOf(result.getId()));
		if (logData == null || logData.isEmpty()) {
			return; // Skip if log data is not found
		}
		// Add script log data to the script folder in .txt format
		zipOutputStream.putNextEntry(
				new ZipEntry(script.getModule().getName() + "/" + scriptName + "/" + scriptName + "_Log.txt"));
		zipOutputStream.write(logData.getBytes());
		zipOutputStream.closeEntry();

		// Add device logs if available
		String deviceLogsPath = commonService.getDeviceLogsPathForTheExecution(executionId.toString(),
				result.getId().toString(), commonService.getBaseLogPath());
		File deviceLogsDir = new File(deviceLogsPath);
		if (deviceLogsDir.exists() && deviceLogsDir.isDirectory()) {
			for (File logFile : deviceLogsDir.listFiles()) {
				zipOutputStream.putNextEntry(new ZipEntry(
						script.getModule().getName() + "/" + scriptName + "/device_logs/" + logFile.getName()));
				zipOutputStream.write(Files.readAllBytes(logFile.toPath()));
				zipOutputStream.closeEntry();
			}
		}

		// Add agent logs if available
		String agentLogsPath = commonService.getAgentLogPath(executionId.toString(), result.getId().toString(),
				commonService.getBaseLogPath());
		File agentLogsDir = new File(agentLogsPath);
		if (agentLogsDir.exists() && agentLogsDir.isDirectory()) {
			for (File logFile : agentLogsDir.listFiles()) {
				zipOutputStream.putNextEntry(new ZipEntry(
						script.getModule().getName() + "/" + scriptName + "/agent_logs/" + logFile.getName()));
				zipOutputStream.write(Files.readAllBytes(logFile.toPath()));
				zipOutputStream.closeEntry();
			}
		}
	}

	/**
	 * Generates a ZIP file containing logs for all scripts in an execution.
	 *
	 * @param executionId the execution ID
	 * @return the byte array of the ZIP file
	 * @throws IOException if an I/O error occurs
	 */
	public byte[] generateExecutionResultsZip(UUID executionId) throws IOException {

		Optional<Execution> executionOptional = executionRepository.findById(executionId);
		if (!executionOptional.isPresent()) {
			throw new ResourceNotFoundException("Execution not found for id: ", executionId.toString());
		}
		Execution execution = executionOptional.get();
		List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);
		ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
		try (ZipOutputStream zipOutputStream = new ZipOutputStream(byteArrayOutputStream)) {
			for (ExecutionResult result : executionResults) {
				String scriptName = result.getScript();
				Script script = scriptRepository.findByName(scriptName);
				if (script == null) {
					throw new ResourceNotFoundException("Script not found for name: ", scriptName);
				}
				addLogsToZip(zipOutputStream, result, script, executionId);
			}
		}
		return byteArrayOutputStream.toByteArray();
	}

	/**
	 * Generates a ZIP file containing logs of failed scripts for a given execution.
	 *
	 * @param executionId the execution ID
	 * @return the byte array of the ZIP file
	 * @throws IOException if an I/O error occurs
	 */
	public byte[] generateExecutionFailureScriptsResultsZip(UUID executionId) throws IOException {
		// Fetch execution results using the executionId
		Optional<Execution> executionOptional = executionRepository.findById(executionId);
		if (!executionOptional.isPresent()) {
			throw new ResourceNotFoundException("Execution not found for id: ", executionId.toString());
		}
		Execution execution = executionOptional.get();
		List<ExecutionResult> executionResults = executionResultRepository.findByExecution(execution);

		// Filter to include only failure scripts
		List<ExecutionResult> failedResults = executionResults.stream()
				.filter(result -> result.getResult().equals(ExecutionResultStatus.FAILURE)).toList();
		if (failedResults.isEmpty()) {
			throw new ResourceNotFoundException("No failure scripts found for execution id: ", executionId.toString());
		}

		ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
		try (ZipOutputStream zipOutputStream = new ZipOutputStream(byteArrayOutputStream)) {
			for (ExecutionResult result : failedResults) {
				String scriptName = result.getScript();
				Script script = scriptRepository.findByName(scriptName);
				if (script == null) {
					throw new ResourceNotFoundException("Script not found for name: ", scriptName);
				}
				addLogsToZip(zipOutputStream, result, script, executionId);
			}
		}
		return byteArrayOutputStream.toByteArray();
	}

	/**
	 * Generates a comparison Excel report based on the provided base execution ID
	 * and a list of execution IDs.
	 *
	 * @param baseExecId   the UUID of the base execution ID
	 * @param executionIds the list of UUIDs of the execution IDs to compare
	 * @return a ByteArrayInputStream containing the generated Excel report
	 * @throws IOException if an I/O error occurs during report generation
	 */
	@Override
	public ByteArrayInputStream generateComparisonExcelReport(UUID baseExecId, List<UUID> executionIds)
			throws IOException {
		LOGGER.info("Generating comparison report for base execution ID: {} and execution IDs: {}", baseExecId,
				executionIds);
		Workbook workBook = new XSSFWorkbook();
		ByteArrayOutputStream out = new ByteArrayOutputStream();

		createSummarySheet(workBook, baseExecId, executionIds);
		createScriptComparisonSheet(workBook, baseExecId, executionIds);

		workBook.write(out);
		workBook.close();
		LOGGER.info("Comparison report generated");
		return new ByteArrayInputStream(out.toByteArray());
	}

	/**
	 * Creates a summary sheet in the given workbook with execution details.
	 *
	 * @param workBook     The workbook where the summary sheet will be created.
	 * @param baseExecId   The UUID of the base execution.
	 * @param executionIds A list of UUIDs of the executions to be included in the
	 *                     summary.
	 */
	private void createSummarySheet(Workbook workBook, UUID baseExecId, List<UUID> executionIds) {
		Sheet sheet = workBook.createSheet("Summary");
		String[] headers = { "Sl No", "Execution Name", "Test Suite", "Image Name", "Executed", "SUCCESS", "FAILURE",
				"SCRIPT TIME OUT", "N/A", "SKIPPED", "Pass %", "New Failure Script Count", "New Timedout Script Count",
				"New Script Count" };

		Row baseExecutionRow = sheet.createRow(0);
		Cell baseExecutionCell = baseExecutionRow.createCell(1);
		baseExecutionCell.setCellValue("Base Execution");
		Cell baseExecutionName = baseExecutionRow.createCell(2);
		baseExecutionName.setCellValue(executionRepository.findById(baseExecId).get().getName());

		Row deviceNameRow = sheet.createRow(1);
		Cell deviceNameCell = deviceNameRow.createCell(1);
		deviceNameCell.setCellValue("Device Name");
		Cell deviceName = deviceNameRow.createCell(2);
		deviceName.setCellValue(executionDeviceRepository
				.findByExecution(executionRepository.findById(baseExecId).get()).getDevice().getName());

		// Add style to above two cells
		CellStyle style = createArialStyle(workBook);
		CellStyle boldStyle = createBoldStyle(workBook);
		baseExecutionCell.setCellStyle(boldStyle);
		baseExecutionName.setCellStyle(boldStyle);
		deviceNameCell.setCellStyle(boldStyle);
		deviceName.setCellStyle(boldStyle);

		createAndStyleArialHeaders(sheet, 5, headers, 0);

		ExecutionDetailsResponseDTO baseExecutionDetails = executionService.getExecutionDetails(baseExecId);
		List<ExecutionDetailsResponseDTO> executionDetails = new ArrayList<>();
		List<String> executionNames = new ArrayList<>();
		executionDetails.add(baseExecutionDetails);
		for (UUID executionId : executionIds) {
			executionDetails.add(executionService.getExecutionDetails(executionId));
		}

		Map<String, ExecutionDetailsResponseDTO> executionDetailsMap = new HashMap<>();
		Execution execution = executionRepository.findById(baseExecId).get();
		executionNames.add(execution.getName());
		executionDetailsMap.put(execution.getName(), baseExecutionDetails);
		for (UUID executionId : executionIds) {
			execution = executionRepository.findById(executionId).get();
			executionNames.add(execution.getName());
			executionDetailsMap.put(execution.getName(), executionService.getExecutionDetails(executionId));
		}

		int rowNum = 6;
		int slNo = 1;
		for (Map.Entry<String, ExecutionDetailsResponseDTO> entry : executionDetailsMap.entrySet()) {
			Row row = sheet.createRow(rowNum++);
			row.createCell(0).setCellValue(slNo++);
			row.createCell(1).setCellValue(entry.getKey());
			row.createCell(2).setCellValue(entry.getValue().getScriptTestSuite());
			row.createCell(3).setCellValue(entry.getValue().getDeviceImageName());
			row.createCell(4).setCellValue(entry.getValue().getSummary().getExecuted());
			row.createCell(5).setCellValue(entry.getValue().getSummary().getSuccess());
			row.createCell(6).setCellValue(entry.getValue().getSummary().getFailure());
			row.createCell(7).setCellValue(entry.getValue().getSummary().getTimeout());
			row.createCell(8).setCellValue(entry.getValue().getSummary().getNa());
			row.createCell(9).setCellValue(entry.getValue().getSummary().getSkipped());
			row.createCell(10).setCellValue(entry.getValue().getSummary().getSuccessPercentage());

			// TODO: Need to add new failure script count, new timedout script count, new
			// script count
			row.createCell(11).setCellValue(0);
			row.createCell(12).setCellValue(0);
			row.createCell(13).setCellValue(0);
			for (int i = 0; i < headers.length; i++) {
				row.getCell(i).setCellStyle(style);
			}
		}

		// set cell style

		autoSizeColumns(sheet, 0, 13);
	}

	/**
	 * Creates a script comparison sheet in the provided workbook.
	 *
	 * @param workBook     The workbook where the sheet will be created.
	 * @param baseExecId   The base execution ID to be compared.
	 * @param executionIds The list of execution IDs to be compared.
	 */
	private void createScriptComparisonSheet(Workbook workBook, UUID baseExecId, List<UUID> executionIds) {
		Sheet scriptSheet = workBook.createSheet("Comparison_Results");

		List<UUID> execId = new ArrayList<>();
		execId.add(baseExecId);
		execId.addAll(executionIds);
		List<String> executionNames = new ArrayList<>();
		for (UUID id : execId) {
			executionNames.add(executionRepository.findById(id).get().getName());
		}

		Map<String, List<String>> moduleScriptMap = new HashMap<>();
		for (UUID id : execId) {
			Execution executionObj = executionRepository.findById(id).get();
			List<ExecutionResult> executionResults = executionResultRepository.findByExecution(executionObj);
			for (ExecutionResult result : executionResults) {
				String scriptName = result.getScript();
				String moduleName = scriptRepository.findByName(scriptName).getModule().getName();
				moduleScriptMap.putIfAbsent(moduleName, new ArrayList<>());
				if (!moduleScriptMap.get(moduleName).contains(scriptName)) {
					moduleScriptMap.get(moduleName).add(scriptName);
				}
			}
		}

		String[] headersForComparison = { "Sl No", "Module Name", "Script Name", "Pass %" };
		List<String> headersList = new ArrayList<>(Arrays.asList(headersForComparison));
		headersList.addAll(executionNames);
		createAndStyleArialHeaders(scriptSheet, 0, headersList.toArray(new String[0]), 0);

		int rowNo = 1;
		int slNos = 1;
		for (Map.Entry<String, List<String>> entry : moduleScriptMap.entrySet()) {
			for (String scriptName : entry.getValue()) {
				Row row = scriptSheet.createRow(rowNo++);
				row.createCell(0).setCellValue(slNos++);
				row.createCell(1).setCellValue(entry.getKey());
				row.createCell(2).setCellValue(scriptName);

				double passPercent = getComparisonResult(scriptName, row, executionNames);
				row.createCell(3).setCellValue(passPercent);

				for (int i = 0; i < headersList.size(); i++) {
					row.getCell(i).setCellStyle(createArialStyle(workBook.getSheetAt(1).getWorkbook()));
				}
			}

			autoSizeColumns(scriptSheet, 0, headersList.size() - 1);
		}
	}

	/**
	 * Calculates the comparison result for a given script name and updates the
	 * provided row with execution results.
	 *
	 * @param scriptName the name of the script to compare results for
	 * @param row        the Excel row to update with execution results
	 * @param execNames  the list of execution names to compare against
	 * @return the percentage of successful executions up to 2 decimal places
	 */
	private double getComparisonResult(String scriptName, Row row, List<String> execNames) {
		int total = 0;
		int pass = 0;
		for (String name : execNames) {
			Execution execution = executionRepository.findByName(name);
			List<ExecutionResult> result = executionResultRepository.findByExecution(execution);
			for (ExecutionResult executionResult : result) {
				if (executionResult.getScript().equals(scriptName)) {
					total++;
					row.createCell(execNames.indexOf(name) + 4).setCellValue(executionResult.getResult().toString());
					if (executionResult.getResult().equals(ExecutionResultStatus.SUCCESS)) {
						pass++;
					}
					break;
				} else {
					row.createCell(execNames.indexOf(name) + 4).setCellValue("Not Executed");
				}
			}
		}

		// percentage up to 2 decimal
		return Math.round((double) pass / total * 100 * 100.0) / 100.0;

	}

	/**
	 * Creates a CellStyle with Arial font for the given Workbook.
	 *
	 * @param workbook the Workbook to create the CellStyle for
	 * @return a CellStyle with Arial font set to size 10
	 */
	private CellStyle createArialStyle(Workbook workbook) {
		CellStyle style = workbook.createCellStyle();
		Font font = workbook.createFont();
		font.setFontName("Arial");
		font.setFontHeightInPoints((short) 10);
		style.setFont(font);
		return style;
	}

	/**
	 * Creates a bold cell style with Arial font, size 10.
	 *
	 * @param workBook the workbook to create the cell style in
	 * @return the created bold cell style
	 */
	private CellStyle createBoldStyle(Workbook workBook) {
		CellStyle style = workBook.createCellStyle();
		Font font = workBook.createFont();
		font.setBold(true);
		font.setFontName("Arial");
		font.setFontHeightInPoints((short) 10);
		style.setFont(font);
		return style;
	}

	/**
	 * Creates and styles header cells in a given sheet using Arial font.
	 *
	 * @param sheet       the sheet where the headers will be created
	 * @param rowNum      the row number where the headers will be placed
	 * @param headers     an array of header titles to be set in the cells
	 * @param startColumn the starting column index for the headers
	 */
	private void createAndStyleArialHeaders(Sheet sheet, int rowNum, String[] headers, int startColumn) {
		Row headerRow = sheet.createRow(rowNum);
		CellStyle headerStyle = sheet.getWorkbook().createCellStyle();
		Font headerFont = sheet.getWorkbook().createFont();
		headerFont.setBold(true);
		headerFont.setFontName("Arial");
		headerFont.setFontHeightInPoints((short) 10);
		headerStyle.setFont(headerFont);

		for (int i = 0; i < headers.length; i++) {
			Cell cell = headerRow.createCell(startColumn + i);
			cell.setCellValue(headers[i]);
			cell.setCellStyle(headerStyle);
		}
	}

	/**
	 * Creates test case details sheet for the given workbook with execution
	 * details.
	 *
	 * @param workBook        The workbook where the test case details sheet will be
	 *                        created.
	 * @param logDatas        The list of log data for each test case .
	 * 
	 * @param instant         The instant of the execution.
	 * @param executionResult The execution result.
	 */
	private void createTestCaseDetailsSheet(Workbook workBook, String logData, Instant createdDate,
			ExecutionResult executionResult) {
		ExecutionResultAnalysis analysis = executionResultAnalysisRepository.findByExecutionResult(executionResult);

		LOGGER.info("Creating test case details sheet for execution result: {}", executionResult.getId());
		Pattern pluginPattern = Pattern.compile("PLUGIN NAME : (.*?)\\n");
		Matcher pluginMatcher = pluginPattern.matcher(logData);
		String pluginName = null;
		if (pluginMatcher.find()) {
			pluginName = pluginMatcher.group(1).trim();
		}
		Sheet sheet = workBook.createSheet(pluginName.toLowerCase());
		int rowNum = 0;
		// Add a "Back to Summary" link at the top
		Row backRow = sheet.createRow(rowNum++);
		Cell backCell = backRow.createCell(0);
		backCell.setCellValue("Back to Summary");

		CreationHelper creationHelper = workBook.getCreationHelper();
		Hyperlink backLink = creationHelper.createHyperlink(HyperlinkType.DOCUMENT);
		backLink.setAddress("'Summary'!A1");
		backCell.setHyperlink(backLink);

		// Create a CellStyle for headers with bold font
		CellStyle headerStyle = workBook.createCellStyle();
		Font headerFont = workBook.createFont();
		headerFont.setBold(true); // Set font to bold
		headerStyle.setFont(headerFont);

		CellStyle linkStyle = workBook.createCellStyle();
		Font linkFont = workBook.createFont();
		linkFont.setUnderline(Font.U_SINGLE);
		linkFont.setColor(IndexedColors.BLUE.getIndex());
		linkStyle.setFont(linkFont);
		backCell.setCellStyle(linkStyle);

		Pattern entirePreReqSectionPattern = Pattern
				.compile("#---------------------------- Plugin Pre-requisite ----------------------------#\\r?\\n"
						+ "(.*?)" + "Plugin Pre-requisite Status\\s*:\\s*\\w+\\r?\\n", Pattern.DOTALL);

		// Then, pattern to match each individual pre-requisite block within the section
		Pattern individualPreReqPattern = Pattern
				.compile("Pre Requisite\\s*:\\s*(.*?)\\r?\\n" + "Pre Requisite No\\s*:\\s*(\\d+)\\r?\\n" + "(.*?)"
						+ "#--------- \\[Pre-requisite Status\\]\\s*:\\s*(.*?)\\s*----------#", Pattern.DOTALL);

		// First, find the entire pre-requisite section
		Matcher sectionMatcher = entirePreReqSectionPattern.matcher(logData);
		if (sectionMatcher.find()) {
			String entirePreReqSection = sectionMatcher.group(1);

			// Now find all individual pre-requisite blocks within that section
			Matcher individualPreReqMatcher = individualPreReqPattern.matcher(entirePreReqSection);

			int preReqNum = 1;
			boolean preReqHeaderCreated = false;

			while (individualPreReqMatcher.find()) {
				String[] preReqHeaders = { "Sl.No", "Pre-Requisite Name", "Status", "Executed On", "Log Data",
						"Jira ID", "Issue Type", "Remarks" };
				if (!preReqHeaderCreated) {
					// Create header row for pre-requisites
					createAndStyleArialHeaders(sheet, rowNum++, preReqHeaders, 0);
					preReqHeaderCreated = true;
				}

				Row row = sheet.createRow(rowNum++);
				row.createCell(0).setCellValue(preReqNum++);
				row.createCell(1).setCellValue(individualPreReqMatcher.group(1).trim()); // Pre-Requisite Name
				row.createCell(2).setCellValue(individualPreReqMatcher.group(4).trim()); // Status from [Pre-requisite
																							// Status]
				row.createCell(3).setCellValue(createdDate.toString()); // Replace with actual execution time if
																		// available
				row.createCell(4).setCellValue(individualPreReqMatcher.group(0).trim()); // Log Data);

				if (analysis != null) {
					row.createCell(5).setCellValue(
							analysis.getAnalysisTicketID() != null ? analysis.getAnalysisTicketID().toString() : "N/A");
					row.createCell(6)
							.setCellValue(analysis.getAnalysisDefectType().toString() != null
									? analysis.getAnalysisDefectType().toString()
									: "N/A");
					row.createCell(7).setCellValue(
							analysis.getAnalysisRemark() != null ? analysis.getAnalysisRemark().toString() : "N/A");
				} else {
					row.createCell(5).setCellValue("N/A");
					row.createCell(6).setCellValue("N/A");
					row.createCell(7).setCellValue("N/A");
				}

				for (int i = 0; i < preReqHeaders.length; i++) {
					row.getCell(i).setCellStyle(createArialStyle(workBook.getSheetAt(0).getWorkbook()));
				}
			}
		}

		// Create header row for test cases
		String[] testCaseHeaders = { "Sl.No", "Test Case Name", "Status", "Executed On", "Log Data", "Jira ID",
				"Issue Type", "Remarks" };

		createAndStyleArialHeaders(sheet, rowNum++, testCaseHeaders, 0);
		// Parse test cases and populate rows
		Pattern testCasePattern = Pattern.compile(
				"#==============================================================================#\\nTEST CASE NAME\\s*:\\s*(.*?)\\n.*?TEST CASE ID\\s*:\\s*(.*?)\\n.*?DESCRIPTION\\s*:\\s*(.*?)\\n.*?TEST STEP STATUS\\s*:\\s*(.*?)\\n.*?##--------- \\[TEST EXECUTION STATUS\\]\\s*:\\s*(.*?)\\s*----------##",
				Pattern.DOTALL);
		Matcher testCaseMatcher = testCasePattern.matcher(logData);
		int testCaseNum = 1;
		while (testCaseMatcher.find()) {
			Row row = sheet.createRow(rowNum++);
			row.createCell(0).setCellValue(testCaseNum++);
			row.createCell(1).setCellValue(testCaseMatcher.group(1).trim());
			row.createCell(2).setCellValue(testCaseMatcher.group(4).trim());
			row.createCell(3).setCellValue(createdDate.toString()); // Replace with actual execution time if available
			row.createCell(4).setCellValue(testCaseMatcher.group(0).trim());
			if (analysis != null) {
				row.createCell(5).setCellValue(
						analysis.getAnalysisTicketID() != null ? analysis.getAnalysisTicketID().toString() : "N/A");
				row.createCell(6)
						.setCellValue(analysis.getAnalysisDefectType().toString() != null
								? analysis.getAnalysisDefectType().toString()
								: "N/A");
				row.createCell(7).setCellValue(
						analysis.getAnalysisRemark() != null ? analysis.getAnalysisRemark().toString() : "N/A");
			} else {

				row.createCell(5).setCellValue("N/A");
				row.createCell(6).setCellValue("N/A");
				row.createCell(7).setCellValue("N/A");

			}
			for (int i = 0; i < testCaseHeaders.length; i++) {
				row.getCell(i).setCellStyle(createArialStyle(workBook.getSheetAt(0).getWorkbook()));
			}
		}

		// Parse post-requisites and populate rows (if any)
		Pattern postReqPattern = Pattern.compile(
				"Post Requisite : (.*?)\\n.*?#--------- \\[Post-requisite Status\\] : (.*?) ----------#",
				Pattern.DOTALL);
		Matcher postReqMatcher = postReqPattern.matcher(logData);
		boolean postReqHeaderCreated = false;
		int postReqNum = 1;
		while (postReqMatcher.find()) {
			if (!postReqHeaderCreated) {
				// Create header row for post-requisites
				String[] postReqHeaders = { "Sl.No", "Post-Requisite Name", "Status", "Executed On", "Log Data",
						"Jira ID", "Issue Type", "Remarks" };
				createAndStyleArialHeaders(sheet, rowNum++, postReqHeaders, 0);
				postReqHeaderCreated = true;
			}

			Row row = sheet.createRow(rowNum++);
			row.createCell(0).setCellValue(postReqNum++);
			row.createCell(1).setCellValue(postReqMatcher.group(1).trim());
			row.createCell(2).setCellValue(postReqMatcher.group(2).trim());
			row.createCell(3).setCellValue(createdDate.toString()); // Replace with actual execution time if available
			row.createCell(4).setCellValue(postReqMatcher.group(0).trim());
			if (analysis != null) {
				row.createCell(5).setCellValue(
						analysis.getAnalysisTicketID() != null ? analysis.getAnalysisTicketID().toString() : "N/A");
				row.createCell(6)
						.setCellValue(analysis.getAnalysisDefectType().toString() != null
								? analysis.getAnalysisDefectType().toString()
								: "N/A");
				row.createCell(7).setCellValue(
						analysis.getAnalysisRemark() != null ? analysis.getAnalysisRemark().toString() : "N/A");
			} else {

				row.createCell(5).setCellValue("N/A");
				row.createCell(6).setCellValue("N/A");
				row.createCell(7).setCellValue("N/A");

			}
			for (int i = 0; i < testCaseHeaders.length; i++) {
				row.getCell(i).setCellStyle(createArialStyle(workBook.getSheetAt(0).getWorkbook()));
			}
		}
		File tmConfigFile = new File(
				AppConfig.getBaselocation() + Constants.FILE_PATH_SEPERATOR + Constants.TM_CONFIG_FILE);
		String logLink = commonService.getConfigProperty(tmConfigFile, Constants.TM_URL)
				+ "/execution/getExecutionLogs?executionResultID=" + executionResult.getId();
		Row logLinkRow = sheet.createRow(rowNum + 2);
		Cell logLinkCell = logLinkRow.createCell(0);
		logLinkCell.setCellValue("LogLink");
		CreationHelper createHelper = workBook.getCreationHelper();
		Hyperlink hyperlink = createHelper.createHyperlink(HyperlinkType.URL);
		hyperlink.setAddress(logLink);
		Cell logLinkCellValue = logLinkRow.createCell(1);
		logLinkCellValue.setCellValue(logLink);
		logLinkCellValue.setHyperlink(hyperlink);
		logLinkCellValue.setCellStyle(linkStyle);
		autoSizeColumns(sheet, 0, 4);
	}

	/**
	 * Create consolidated summary sheet
	 * 
	 * @param workBook
	 * @param logData
	 * @param execution
	 * @throws IOException
	 */
	private int createConsolidatedSummarySheet(Sheet sheet, int rowCount, List<String> logData, Execution execution) {

		String heading = "RDKSERVICES Summary";
		Row rowHead = sheet.createRow(rowCount++);
		Cell headCells = rowHead.createCell(3);
		headCells.setCellValue(heading);
		CellStyle headStyle = sheet.getWorkbook().createCellStyle();
		Font headFont = sheet.getWorkbook().createFont();
		headFont.setUnderline(Font.U_SINGLE);
		headFont.setBold(true);
		headFont.setFontName("Arial");
		headStyle.setFont(headFont);
		headCells.setCellStyle(headStyle);
		rowCount++;

		String[] headers = { "Sl No", "Plugins", "Script Status", "Total Test Case", "Executed", "SUCCESS", "FAILURE",
				"N/A" };
		createAndStyleArialHeaders(sheet, rowCount++, headers, 0);
		System.out.println("Log Data: " + logData);
		// Define the pattern to extract the required information
		Pattern pattern = Pattern.compile("======================== PLUGIN TEST SUMMARY ======================\\r?\\n"
				+ "PLUGIN NAME\\s*:\\s*(.*?)\\r?\\n" + "TOTAL TESTS\\s*:\\s*(\\d+)\\r?\\n"
				+ "EXECUTED TESTS\\s*:\\s*(\\d+)\\r?\\n" + "PASSED TESTS\\s*:\\s*(\\d+)\\r?\\n"
				+ "FAILED TESTS\\s*:\\s*(\\d+)\\r?\\n" + "N/A TESTS\\s*:\\s*(\\d+)\\r?\\n" + "\\r?\\n"
				+ "Final Plugin Tests Status\\s*:\\s*(.*?)\\r?\\n", Pattern.DOTALL);
		// Find all matches in the log data
		int totalTestCasesSum = 0;
		int executedTestCasesSum = 0;
		int successTestCasesSum = 0;
		int failureTestCasesSum = 0;
		int naTestCasesSum = 0;
		for (String log : logData) {
			Matcher matcher = pattern.matcher(log);
			// Create a row for each match
			int slNo = 1;
			// i need to add up for each finder

			while (matcher.find()) {
				Row row = sheet.createRow(rowCount++);
				row.createCell(0).setCellValue(slNo++);
				// row.createCell(1).setCellValue(matcher.group(1).trim());
				// Create and style hyperlink for module name
				Cell pluginCell = row.createCell(1);
				pluginCell.setCellValue(matcher.group(1).trim().toLowerCase());
				CreationHelper creationHelper = sheet.getWorkbook().getCreationHelper();
				Hyperlink link = creationHelper.createHyperlink(HyperlinkType.DOCUMENT);
				link.setAddress("'" + matcher.group(1).trim().toLowerCase() + "'!A1"); // Target module sheet
				pluginCell.setHyperlink(link);

				CellStyle linkStyle = sheet.getWorkbook().createCellStyle();
				Font linkFont = sheet.getWorkbook().createFont();
				linkFont.setUnderline(Font.U_SINGLE);
				linkFont.setColor(IndexedColors.BLUE.getIndex());
				linkFont.setFontName("Arial");
				linkStyle.setFont(linkFont);
				pluginCell.setCellStyle(linkStyle);

				row.createCell(2).setCellValue(matcher.group(7).trim());
				row.createCell(3).setCellValue(Integer.parseInt(matcher.group(2).trim()));
				row.createCell(4).setCellValue(Integer.parseInt(matcher.group(3).trim()));
				row.createCell(5).setCellValue(Integer.parseInt(matcher.group(4).trim()));
				row.createCell(6).setCellValue(Integer.parseInt(matcher.group(5).trim()));
				row.createCell(7).setCellValue(Integer.parseInt(matcher.group(6).trim()));

				for (int i = 2; i < headers.length; i++) {
					row.getCell(i).setCellStyle(createArialStyle(sheet.getWorkbook()));
				}

				// I need to get the sum of all the test cases , executed test cases, success
				int totalTestCases = Integer.parseInt(matcher.group(2).trim());
				int executedTestCases = Integer.parseInt(matcher.group(3).trim());
				int successTestCases = Integer.parseInt(matcher.group(4).trim());
				int failureTestCases = Integer.parseInt(matcher.group(5).trim());
				int naTestCases = Integer.parseInt(matcher.group(6).trim());

				// i need to add up for each finder
				totalTestCasesSum += totalTestCases;
				executedTestCasesSum += executedTestCases;
				successTestCasesSum += successTestCases;
				failureTestCasesSum += failureTestCases;
				naTestCasesSum += naTestCases;
			}

		}

		// Create a row for the total
		Row rowTotal = sheet.createRow(rowCount++);
		rowTotal.createCell(0).setCellValue("");
		rowTotal.createCell(1).setCellValue("Total");
		rowTotal.createCell(2).setCellValue("");
		rowTotal.createCell(3).setCellValue(totalTestCasesSum);
		rowTotal.createCell(4).setCellValue(executedTestCasesSum);
		rowTotal.createCell(5).setCellValue(successTestCasesSum);
		rowTotal.createCell(6).setCellValue(failureTestCasesSum);
		rowTotal.createCell(7).setCellValue(naTestCasesSum);
		for (int i = 0; i < headers.length; i++) {
			rowTotal.getCell(i).setCellStyle(createArialStyle(sheet.getWorkbook()));
		}

		autoSizeColumns(sheet, 0, 7);

		return rowCount;

	}

}
