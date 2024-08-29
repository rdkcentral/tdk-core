
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

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.rdkm.tdkservice.config.JWTAuthFilter;
import com.rdkm.tdkservice.dto.SigninRequestDTO;
import com.rdkm.tdkservice.dto.SigninResponseDTO;
import com.rdkm.tdkservice.dto.UserDTO;
import com.rdkm.tdkservice.dto.UserGroupDTO;
import com.rdkm.tdkservice.service.IUserGroupService;
import com.rdkm.tdkservice.serviceimpl.LoginService;
import com.rdkm.tdkservice.serviceimpl.UserService;

/**
 * This class is used to test the LoginController
 */

public class LoginControllerTest {

	@InjectMocks
	private LoginController loginController;

	@Mock
	private LoginService loginService;

	@Mock
	private IUserGroupService userGroupService;

	@Mock
	private JWTAuthFilter jwtFilter;

	@Mock
	private UserService userService;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.openMocks(this);
	}

	/**
	 * This method is used to test the signUp method is success
	 * 
	 * 
	 */
	@Test
	void testSignUpSuccess() {
		UserDTO register = new UserDTO();
		register.setUserName("qwert");
		register.setPassword("password");
		register.setUserGroupName("usergroup1");

		when(loginService.register(register)).thenReturn(true);

		ResponseEntity<String> response = loginController.signUp(register);

		assertEquals(HttpStatus.CREATED, response.getStatusCode());
		assertEquals("User created successfully", response.getBody());
	}

	/**
	 * This method is used to test the signUp method with null user
	 * 
	 * 
	 */
	@Test
	void testSignUpWhenUserIsNull() {
		UserDTO register = new UserDTO();
		register.setUserName("qwert");
		register.setPassword("password");
		register.setUserGroupName("usergroup1");
		when(loginService.register(register)).thenReturn(false);

		ResponseEntity<?> response = loginController.signUp(register);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Error in saving user data", response.getBody());
	}

	/**
	 * This method is used to test sign in is success
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignInSuccess() throws Exception {
		SigninRequestDTO signin = new SigninRequestDTO();
		signin.setUsername("usrname");
		signin.setPassword("password");

		SigninResponseDTO signinResponseDTO = new SigninResponseDTO();
		signinResponseDTO.setToken("mock-token");

		when(loginService.signIn(signin)).thenReturn(signinResponseDTO);

		ResponseEntity<SigninResponseDTO> response = loginController.signIn(signin);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(signinResponseDTO, response.getBody());

	}

	@Test
	public void getListOfUserGroupsSuccess() {
		List<UserGroupDTO> userGroups = new ArrayList<>();
		when(userGroupService.findAll()).thenReturn(userGroups);
		ResponseEntity<List<String>> response = loginController.getListOfUserGroups();
		assertEquals(HttpStatus.OK, response.getStatusCode());
	}

}
