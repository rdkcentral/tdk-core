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
package com.rdkm.tdkservice.controller;

import java.util.List;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.rdkm.tdkservice.dto.SigninRequestDTO;
import com.rdkm.tdkservice.dto.SigninResponseDTO;
import com.rdkm.tdkservice.dto.UserCreateDTO;
import com.rdkm.tdkservice.dto.UserGroupDTO;
import com.rdkm.tdkservice.service.ILoginService;
import com.rdkm.tdkservice.service.IUserGroupService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/**
 * The LoginController class is a REST controller that handles login and
 * registration requests. It provides endpoints for user registration, sign in,
 * and password change. This class uses the ILoginService to perform the actual
 * business logic.
 *
 * Endpoints: POST /tdk/signup: Register a new user. POST /tdk/signin: Sign in a
 * user. POST /tdk/changepassword: Change the password of a user.
 * 
 */
@Validated
@RestController
@CrossOrigin
@RequestMapping("/api/v1/auth/")
public class LoginController {

	private static final Logger LOGGER = LoggerFactory.getLogger(LoginController.class);

	@Autowired
	private ILoginService loginService;

	@Autowired
	private IUserGroupService userGroupService;

	/**
	 * This method is used to register a new user. It receives a POST request at the
	 * "/signup" endpoint with a UserDTO object in the request body. The UserDTO
	 * object should contain the necessary information for creating a new user.
	 * 
	 * @param registerRequest A UserDTO object that contains the information of the
	 *                        user to be registered.
	 * @return ResponseEntity<String> If the user is successfully created, it
	 *         returns a 201 status code with a success message. If there is an
	 *         error in saving the user data, it returns a 500 status code with an
	 *         error message.
	 * @throws Exception
	 */
	@Operation(summary = "Register a new user", description = "Registers a new user in the system.")
	@ApiResponse(responseCode = "201", description = "User created successfully")
	@ApiResponse(responseCode = "500", description = "Error in saving user data")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "409", description = "Conflict")

	@PostMapping("/signup")
	public ResponseEntity<String> signUp(@RequestBody @Valid UserCreateDTO registerRequest) {
		LOGGER.info("Received signup request: " + registerRequest.toString());
		boolean isUserCreated = loginService.register(registerRequest);
		if (isUserCreated) {
			LOGGER.info("User creation is successfull");
			return ResponseEntity.status(HttpStatus.CREATED).body("User created successfully");
		} else {
			LOGGER.error("User creation failed");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in saving user data");
		}

	}

	/**
	 * This method is used to sign in a user. It receives a POST request at the
	 * "/signin" endpoint with a SigninRequestDTO object in the request body. The
	 * SigninRequestDTO object should contain the necessary information for signing
	 * in a user.
	 *
	 * @param signinRequest A SigninRequestDTO object that contains the information
	 *                      of the user to be signed in.
	 * @return ResponseEntity<SigninResponseDTO> If the user is successfully signed
	 *         in, it returns a 200 status code with a SigninResponseDTO object. The
	 *         SigninResponseDTO object contains the details of the signed in user.
	 *         If there is an error in signing in the user, it returns an
	 *         appropriate error status code with an error message.
	 * @throws Exception If any exception occurs during the execution of the method,
	 *                   it is thrown to the caller to handle.
	 */
	@Operation(summary = "Sign in a user", description = "Signs in a user in the system.")
	@ApiResponse(responseCode = "200", description = "User signed in successfully")
	@ApiResponse(responseCode = "500", description = "Error in signing in user")
	@ApiResponse(responseCode = "400", description = "Bad request")
	@ApiResponse(responseCode = "401", description = "Unauthorized")
	@ApiResponse(responseCode = "403", description = "Forbidden")
	@ApiResponse(responseCode = "404", description = "User not found")
	@PostMapping("/signin")
	public ResponseEntity<SigninResponseDTO> signIn(@RequestBody @Valid SigninRequestDTO signinRequest) {
		LOGGER.info("Received sign request: " + signinRequest.toString());
		SigninResponseDTO signinResponseDTO = loginService.signIn(signinRequest);
		LOGGER.info("Finished signin request, response id: " + signinResponseDTO.toString());
		return ResponseEntity.status(HttpStatus.OK).body(signinResponseDTO);
	}

	/**
	 * This method is mapped to the "/getList" endpoint and is responsible for
	 * retrieving all user groups. It uses the findAll method of the
	 * userGroupService to get a list of all UserGroupDTO objects. Then, it uses a
	 * stream to map each UserGroupDTO to its name and collects these names into a
	 * list. Finally, it returns a ResponseEntity containing this list of user group
	 * names.
	 *
	 * @return ResponseEntity containing a list of user group names
	 */
	@Operation(summary = "Get list of user groups", description = "Retrieves a list of all user groups in the system.")
	@ApiResponse(responseCode = "200", description = "User groups retrieved successfully")
	@ApiResponse(responseCode = "404", description = "No user groups found")
	@GetMapping("/getList")
	public ResponseEntity<List<String>> getListOfUserGroups() {
		List<UserGroupDTO> userGroups = userGroupService.findAll();
		LOGGER.info("Received user groups: " + userGroups.toString());
		List<String> userGroupNames = userGroups.stream().map(UserGroupDTO::getUserGroupName)
				.collect(Collectors.toList());
		LOGGER.info("User groups found: " + userGroupNames);
		return ResponseEntity.ok(userGroupNames);
	}

}
