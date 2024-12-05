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

import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ScheduledFuture;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.TaskScheduler;
import org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler;
import org.springframework.scheduling.support.CronTrigger;
import org.springframework.stereotype.Service;

import com.rdkm.tdkservice.dto.ExecutionResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionScheduleDTO;
import com.rdkm.tdkservice.dto.ExecutionSchedulesResponseDTO;
import com.rdkm.tdkservice.dto.ExecutionTriggerDTO;
import com.rdkm.tdkservice.enums.ScheduleStatus;
import com.rdkm.tdkservice.enums.ScheduleType;
import com.rdkm.tdkservice.exception.UserInputException;
import com.rdkm.tdkservice.model.ExecutionSchedule;
import com.rdkm.tdkservice.repository.ExecutionScheduleRepository;
import com.rdkm.tdkservice.util.MapperUtils;

import jakarta.annotation.PostConstruct;

/**
 * The service class for the execution schedule feature
 */
@Service
public class ExecutionScheduleService {

	@Autowired
	ExecutionScheduleRepository executionScheduleRepository;

	@Autowired
	private ExecutionService executionService;

	private TaskScheduler taskScheduler;

	// Map to store the scheduled tasks
	private Map<UUID, ScheduledFuture<?>> scheduledTasks = new ConcurrentHashMap<>();

	private static final Logger LOGGER = LoggerFactory.getLogger(ExecutionScheduleService.class);

	/**
	 * Initializes the task scheduler and loads scheduled tasks.
	 */
	@PostConstruct
	public void init() {
		taskScheduler = new ThreadPoolTaskScheduler();
		((ThreadPoolTaskScheduler) taskScheduler).initialize();
		loadScheduledTasks();
	}

	/**
	 * Schedules a task based on the provided execution schedule.
	 * 
	 * @param schedule the execution schedule containing the details for scheduling
	 *                 the task
	 */
	private void scheduleTask(ExecutionSchedule schedule) {
		// Schedule the task using the cron expression or the execution time
		// TODO: Implement the logic to schedule the task based on the cron expression
		// or the execution time
		if (schedule.getCronExpression() != null) {
			ScheduledFuture<?> future = taskScheduler.schedule(() -> triggerScheduledExecution(schedule),
					new CronTrigger(schedule.getCronExpression()));
			scheduledTasks.put(schedule.getId(), future);
		} else if (schedule.getExecutionTime() != null) {
			ScheduledFuture<?> future = taskScheduler.schedule(() -> triggerScheduledExecution(schedule),
					schedule.getExecutionTime());
			scheduledTasks.put(schedule.getId(), future);
		}

	}

	/**
	 * Loads scheduled tasks from the repository and schedules them if their status
	 * is SCHEDULED.
	 */
	private void loadScheduledTasks() {
		List<ExecutionSchedule> schedules = executionScheduleRepository.findAll();
		// Add the schedules only when the scheudle status is SCHDEULED
		// do not add if the schedule is COmpleted or cancelled
		for (ExecutionSchedule schedule : schedules) {
			if (ScheduleStatus.SCHEDULED.equals(schedule.getScheduleStatus())) {
				scheduleTask(schedule);
			}
		}

	}

	/**
	 * Cancels a scheduled task.
	 * 
	 * @param taskId the ID of the task to be cancelled
	 */
	public void cancelTask(UUID taskId) {
		ScheduledFuture<?> scheduledTask = scheduledTasks.get(taskId);
		if (scheduledTask != null) {
			scheduledTask.cancel(false);
			scheduledTasks.remove(taskId);
		}

		ExecutionSchedule executionSchedule = executionScheduleRepository.findById(taskId).get();
		executionSchedule.setScheduleStatus(ScheduleStatus.CANCELLED);
		executionScheduleRepository.save(executionSchedule);

	}

	/**
	 * Creates a schedule based on the saved execution schedule.
	 * 
	 * @param savedExecutionSchedule the saved execution schedule
	 * @return the created execution schedule
	 */
	public ExecutionSchedule createSchedule(ExecutionSchedule savedExecutionSchedule) {
		scheduleTask(savedExecutionSchedule);
		return savedExecutionSchedule;
	}

	/**
	 * Saves the execution schedule.
	 * 
	 * @param executionScheduleDTO the execution schedule DTO
	 * @return boolean status of the execution
	 */
	public boolean saveScheduleExecution(ExecutionScheduleDTO executionScheduleDTO) {
		LOGGER.info("Creating the execution schedule");
		ExecutionTriggerDTO executionTriggerDTO = executionScheduleDTO.getExecutionTriggerDTO();

		// if execution time is less than the current time, throw exception
		if (executionScheduleDTO.getExecutionTime().isBefore(Instant.now())) {
			throw new UserInputException("Execution time should be greater than the current time");
		}

		// Once the execution DTO is created, check if the trigger request is valid
		// If not valid, throw an exception which will be caught by the controller
		executionService.checkValidTriggerRequest(executionTriggerDTO);

		// Saving the execution schedule object with schedule and execution details
		ExecutionSchedule executionSchedule = MapperUtils.convertToExecutionSchedule(executionScheduleDTO);
		ExecutionSchedule savedExecutionSchedule = executionScheduleRepository.save(executionSchedule);

		// Create the schedule based on the saved execution schedule
		ExecutionSchedule scheduledExecution = this.createSchedule(savedExecutionSchedule);

		if (scheduledExecution != null) {
			return true;
		}
		return false;
	}

	/**
	 * Triggers the scheduled execution.
	 * 
	 * @param executionSchedule the execution schedule
	 * @return the result of the execution
	 */
	public String triggerScheduledExecution(ExecutionSchedule executionSchedule) {
		ExecutionTriggerDTO executionTriggerDTO = convertToExecutionTriggerDTO(executionSchedule);
		ExecutionResponseDTO executionResponseDTO = null;
		try {
			executionResponseDTO = executionService.startExecution(executionTriggerDTO);
			System.out.println("Execution Response: " + executionResponseDTO.toString());
		} catch (Exception e) {
			LOGGER.error("Error while triggering the execution: " + e.getMessage());
			e.printStackTrace();
		}

		if (ScheduleType.ONCE.equals(executionSchedule.getScheduleType())) {

			ExecutionSchedule schedule = executionScheduleRepository.findById(executionSchedule.getId()).get();
			schedule.setScheduleStatus(ScheduleStatus.COMPLETED);
			executionScheduleRepository.save(schedule);
		}
		return null;
	}

	/**
	 * This method is used to convert the execution schedule to execution
	 * 
	 * @param executionSchedule the execution schedule to be converted
	 * @return
	 */
	private ExecutionTriggerDTO convertToExecutionTriggerDTO(ExecutionSchedule executionSchedule) {
		ExecutionTriggerDTO executionTriggerDTO = new ExecutionTriggerDTO();
		// convert comma separated string to list
		List<String> scriptList = Arrays.asList(executionSchedule.getScriptList().split(","));
		executionTriggerDTO.setScriptList(scriptList);

		List<String> deviceList = Arrays.asList(executionSchedule.getDeviceList().split(","));
		executionTriggerDTO.setDeviceList(deviceList);

		List<String> testSuite = Arrays.asList(executionSchedule.getTestSuite().split(","));
		executionTriggerDTO.setTestSuite(testSuite);

		executionTriggerDTO.setTestType(executionSchedule.getTestType());
		executionTriggerDTO.setUser(executionSchedule.getUser());
		executionTriggerDTO.setCategory(executionSchedule.getCategory());
		executionTriggerDTO.setExecutionName(executionSchedule.getExecutionName());
		executionTriggerDTO.setRepeatCount(executionSchedule.getRepeatCount());
		executionTriggerDTO.setRerunOnFailure(executionSchedule.isRerunOnFailure());
		executionTriggerDTO.setDeviceLogsNeeded(executionSchedule.isDeviceLogsNeeded());
		executionTriggerDTO.setPerformanceLogsNeeded(executionSchedule.isPerformanceLogsNeeded());
		executionTriggerDTO.setDiagnosticLogsNeeded(executionSchedule.isDiagnosticLogsNeeded());
		return executionTriggerDTO;

	}

	/**
	 * This method is used to cancel the execution schedule
	 * 
	 * @param executionID the execution ID of the schedule to be cancelled
	 * @return boolean status of the execution cancellation
	 */
	public boolean cancelScheduleExecution(UUID executionID) {
		LOGGER.info("Cancelling the execution schedule");
		ScheduledFuture<?> scheduledTask = scheduledTasks.get(executionID);
		if (scheduledTask != null) {
			scheduledTask.cancel(false);
			scheduledTasks.remove(executionID);
		}
		ExecutionSchedule executionSchedule = executionScheduleRepository.findById(executionID).get();
		executionSchedule.setScheduleStatus(ScheduleStatus.CANCELLED);
		executionScheduleRepository.save(executionSchedule);
		LOGGER.info("Execution schedule cancelled successfully");
		return true;
	}

	/**
	 * 
	 * @param executionID
	 * @return
	 */
	public boolean deleteScheduleExecution(UUID executionID) {
		LOGGER.info("Deleting the execution schedule");
		try {
			ScheduledFuture<?> scheduledTask = scheduledTasks.get(executionID);
			if (scheduledTask != null) {
				scheduledTask.cancel(false);
				scheduledTasks.remove(executionID);
			}
			ExecutionSchedule executionSchedule = executionScheduleRepository.findById(executionID).get();
			executionScheduleRepository.delete(executionSchedule);
			LOGGER.info("Execution schedule deleted successfully");
			return true;
		} catch (Exception e) {
			LOGGER.error("Error while deleting the execution schedule: " + e.getMessage());
			return false;
		}

	}

	public List<ExecutionSchedulesResponseDTO> getAllExecutionSchedules() {
		LOGGER.info("Fetching all the execution schedules");
		List<ExecutionSchedule> listOfExecutionSchedules = executionScheduleRepository.findAll();
		if (listOfExecutionSchedules == null) {
			return null;
		} else {
			return getResponseDTOList(listOfExecutionSchedules);
		}

	}

	private List<ExecutionSchedulesResponseDTO> getResponseDTOList(List<ExecutionSchedule> listOfExecutionSchedules) {
		List<ExecutionSchedulesResponseDTO> responseDTOList = new ArrayList<>();
		for (ExecutionSchedule executionSchedule : listOfExecutionSchedules) {
			ExecutionSchedulesResponseDTO responseDTO = new ExecutionSchedulesResponseDTO();
			responseDTO.setExecutionTime(executionSchedule.getExecutionTime());
			responseDTO.setStatus(executionSchedule.getScheduleStatus().toString());
			responseDTO.setJobName(executionSchedule.getExecutionName());
			responseDTO.setId(executionSchedule.getId().toString());

			if (executionSchedule.getDeviceList() != null) {
				responseDTO.setDevice(executionSchedule.getDeviceList());
			}

			if (executionSchedule.getScriptList() != null) {
				responseDTO.setScriptTestSuite(executionSchedule.getScriptList());
			} else if (executionSchedule.getTestSuite() != null) {
				responseDTO.setScriptTestSuite(executionSchedule.getTestSuite());
			}

			if (executionSchedule.getScheduleType().equals(ScheduleType.ONCE)) {
				responseDTO.setDetails("One time execution");
			} else {
				// TODO - add the cron expression here
			}
			responseDTOList.add(responseDTO);
		}
		return responseDTOList;
	}

}
