package com.rdkm.tdkservice.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.rdkm.tdkservice.model.ExecutionSchedule;

@Repository
public interface ExecutionScheduleRepository extends JpaRepository<ExecutionSchedule, UUID> {

	/**
	 * This method is used to check the existence of the execution by name.
	 * 
	 * @param executionName
	 * @return boolean - true if the execution exists, false otherwise
	 */
	boolean existsByExecutionName(String executionName);
}