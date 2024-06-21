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

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.rdkm.tdkservice.dto.ChangePasswordRequestDTO;
import com.rdkm.tdkservice.dto.UserDTO;
import com.rdkm.tdkservice.dto.UserUpdateDTO;
import com.rdkm.tdkservice.serviceimpl.UserService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;

/**
 * The UserController class handles all the user-related operations in the
 * application. It uses the UserService to perform these operations.
 * 
 * The class is annotated with @RestController, which means it's a special type
 * of Controller that includes @Controller and @ResponseBody annotations. It's
 * used to handle HTTP requests and the response is automatically serialized
 * into JSON and passed back into the HttpResponse.
 */
@RestController
@CrossOrigin
@RequestMapping("/api/v1/users/")
public class UserController {

	private static final Logger LOGGER = LoggerFactory.getLogger(UserController.class);

	@Autowired
	private UserService userService;

	/**
	 * This method is used to create the user
	 *
	 * @param userRequestDTO - User object
	 * @return ResponseEntity<String> - response entity - message
	 */

	@Operation(summary = "API to Crreate the User", description = "This API is used to create the user")
	@ApiResponse(responseCode = "201", description = "Successfully signed in")
	@ApiResponse(responseCode = "500", description = "Internal Server Error")
	@ApiResponse(responseCode = "400", description = "Bad Request")
	@ApiResponse(responseCode = "409", description = "Conflict")
	@PostMapping("/create")
	public ResponseEntity<String> saveUser(@RequestBody @Valid UserDTO userRequestDTO) {
		LOGGER.info("Executing saveUser method with request: " + userRequestDTO.toString());
		boolean isUserCreated = userService.createUser(userRequestDTO);
		if (isUserCreated) {
			LOGGER.info("User created successfully");
			return ResponseEntity.status(HttpStatus.CREATED).body("User created succesfully");
		} else {
			LOGGER.error("Error in saving user data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("User creation failed");
		}
	}

	/**
	 * This method is used to find the user by id
	 * 
	 * @param id - Integer
	 * @return ResponseEntity<User> - response entity - user object
	 */
	@Operation(summary = "API to find the User by Id", description = "This API is used to find the user by id")
	@ApiResponse(responseCode = "200", description = "Successfully found the user")
	@ApiResponse(responseCode = "404", description = "User not found")
	@GetMapping("findById/{id}")
	public ResponseEntity<UserDTO> findUserById(@PathVariable Integer id) {
		LOGGER.info("Executing findUserById method with id: " + id);
		UserDTO user = userService.findUserById(id);
		return ResponseEntity.status(HttpStatus.OK).body(user);
	}

	/**
	 * This method is used to update the user
	 *
	 * @param user - User object
	 * @return ResponseEntity<User> - response entity - user object
	 */
	@Operation(summary = "API to update the User", description = "This API is used to update the user")
	@ApiResponse(responseCode = "200", description = "Successfully updated the user")
	@ApiResponse(responseCode = "500", description = "Internal Server Error")
	@ApiResponse(responseCode = "400", description = "Bad Request")
	@ApiResponse(responseCode = "404", description = "User not found")
	@ApiResponse(responseCode = "409", description = "Conflict")
	@PutMapping("/update")
	public ResponseEntity<?> updateUser(@Valid @RequestBody UserUpdateDTO userRequest) {
		LOGGER.info("Executing updateUser method with request: " + userRequest.toString());
		UserDTO updatedUser = userService.updateUser(userRequest);
		if (null != updatedUser) {
			LOGGER.info("User updated successfully");
			return ResponseEntity.status(HttpStatus.OK).body(updatedUser);
		} else {
			LOGGER.error("Error in updating user data");
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error in updating user data");
		}

	}

	/**
	 * This method is used to get all the users
	 *
	 * @return ResponseEntity<List<User>> - response entity - list of users
	 */
	@Operation(summary = "API to get all the Users", description = "This API is used to get all the users")
	@ApiResponse(responseCode = "200", description = "Successfully found the users")
	@ApiResponse(responseCode = "404", description = "No users found")
	@ApiResponse(responseCode = "500", description = "Internal Server Error")
	@ApiResponse(responseCode = "400", description = "Bad Request")
	@ApiResponse(responseCode = "409", description = "Conflict")
	@GetMapping("/findAll")
	public ResponseEntity<?> getAllUsers() {
		LOGGER.info("Executing getAllUsers method");
		List<UserDTO> users = userService.getAllUsers();
		if (null != users) {
			LOGGER.info("Users found successfully ");
			return ResponseEntity.status(HttpStatus.OK).body(users);
		} else {
			LOGGER.error("No users found");
			return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No users found");
		}

	}

	/**
	 * This method is used to delete the user
	 *
	 * @param id - Integer
	 * @return ResponseEntity<String> - response entity - message
	 */
	@Operation(summary = "API to delete the User", description = "This API is used to delete the user")
	@ApiResponse(responseCode = "200", description = "Successfully deleted the user")
	@ApiResponse(responseCode = "500", description = "Internal Server Error")
	@ApiResponse(responseCode = "400", description = "Bad Request")
	@ApiResponse(responseCode = "404", description = "User not found")
	@ApiResponse(responseCode = "409", description = "Conflict")
	@DeleteMapping("/delete")
	public ResponseEntity<String> deleteUser(@RequestParam Integer id) {
		LOGGER.info("Executing deleteUser method with id: " + id);
		userService.deleteUser(id);
		return ResponseEntity.status(HttpStatus.OK).body("User got deleted successfully");
	}

	/**
	 * This method is used to change the password of a user. It receives a POST
	 * request at the "/changepassword" endpoint with a ChangePasswordRequestDTO
	 * object in the request body. The ChangePasswordRequestDTO object should
	 * contain the necessary information for changing the password of a user.
	 *
	 * @param changePasswordRequest A ChangePasswordRequestDTO object that contains
	 *                              the information of the user whose password is to
	 *                              be changed.
	 * @return ResponseEntity<String> If the password is successfully changed, it
	 *         returns a 200 status code with a success message. If there is an
	 *         error in changing the password, it returns a 400 status code with an
	 *         error message.
	 * @throws Exception If any exception occurs during the execution of the method,
	 *                   it is thrown to the caller to handle.
	 */
	@Operation(summary = "API to change the password", description = "This API is used to change the password of a user")
	@ApiResponse(responseCode = "200", description = "Successfully updated the password")
	@ApiResponse(responseCode = "500", description = "Internal Server Error")
	@ApiResponse(responseCode = "400", description = "Bad Request")
	@ApiResponse(responseCode = "404", description = "User not found")
	@ApiResponse(responseCode = "409", description = "Conflict")
	@ApiResponse(responseCode = "401", description = "Unauthorized")
	@ApiResponse(responseCode = "403", description = "Forbidden")
	@PostMapping("/changepassword")
	public ResponseEntity<String> changePassword(@RequestBody @Valid ChangePasswordRequestDTO changePasswordRequest) {
		LOGGER.info("The change password request is " + changePasswordRequest.toString());
		boolean isChangePassword = userService.changePassword(changePasswordRequest);
		if (isChangePassword) {
			LOGGER.info("Password change is successful");
			return ResponseEntity.status(HttpStatus.OK).body("Succesfully updated the password");
		} else {
			LOGGER.error("Password change failed");
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Old password doesnt match with the username");

		}

	}

}
