package com.rdkm.tdkservice.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ScriptDetailsResponse {

	/**
	 * The id of the Script.
	 */
	UUID id;

	/**
	 * The name of the Script.
	 */
	String scriptName;
}
