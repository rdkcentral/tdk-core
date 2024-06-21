
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

import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.rdkm.tdkservice.dto.SigninRequestDTO;
import com.rdkm.tdkservice.dto.SigninResponseDTO;
import com.rdkm.tdkservice.dto.UserDTO;
import com.rdkm.tdkservice.serviceimpl.LoginService;

/**
 * This class is used to test the LoginController
 */

@SpringBootTest
@AutoConfigureMockMvc
public class LoginControllerTest {

	@InjectMocks
	private LoginController loginController;

	@Mock
	private LoginService authService;

	@Autowired
	private MockMvc mockMvc;

	/**
	 * This method is used to test the signUp method with null user name 
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignUpWithEmptyUsername() throws Exception {
		UserDTO register = new UserDTO();
		register.setUserName(null);
		register.setPassword("password");
		register.setUserGroupName("usergroup1");
		register.setUserEmail("abcd@gmail.com");
		String json = new ObjectMapper().writeValueAsString(register);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signup").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.userName").value("Username is required"));

	}

	/**
	 * This method is used to test the signUp method of LoginController with empty password
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignUpWithEmptyPassword() throws Exception {
		UserDTO register = new UserDTO();
		register.setUserName("username");
		register.setPassword(null);
		register.setUserGroupName("usergroup1");
		register.setUserEmail("abcd@gmail.com");
		String json = new ObjectMapper().writeValueAsString(register);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signup").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.password").value("Password is required"));
	}

	/**
	 * This method is used to test the signUp method with empty user group
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignUpWithEmptyUserGroup() throws Exception {
		UserDTO register = new UserDTO();
		register.setUserName("username");
		register.setPassword("password");
		register.setUserGroupName(null);
		register.setUserEmail("abcd@gmail.com");
		String json = new ObjectMapper().writeValueAsString(register);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signup").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.userGroupName").value("Usergroup is required"));
	}

	/**
	 * This method is used to test the signUp method of LoginController with empty user name and password
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignUpWithEmptyUsernameAndPassword() throws Exception {
		UserDTO register = new UserDTO();
		register.setUserName(null);
		register.setPassword(null);
		register.setUserGroupName("usergroup1");
		register.setUserEmail("abcd@gmail.com");
		String json = new ObjectMapper().writeValueAsString(register);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signup").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.userName").value("Username is required"))
				.andExpect(MockMvcResultMatchers.jsonPath("$.password").value("Password is required"));
	}

	/**
	 * This method is used to test the signUp with empty user name, password and user group
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignUpWithEmptyUsernamePasswordAndUserGroup() throws Exception {
		UserDTO register = new UserDTO();
		register.setUserName(null);
		register.setPassword(null);
		register.setUserGroupName(null);
		String json = new ObjectMapper().writeValueAsString(register);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signup").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.userName").value("Username is required"))
				.andExpect(MockMvcResultMatchers.jsonPath("$.password").value("Password is required"))
				.andExpect(MockMvcResultMatchers.jsonPath("$.userGroupName").value("Usergroup is required"));
	}

	/**
	 * This method is used to test the signUp with invalid email
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignUpWithValidEmail() throws Exception {
		UserDTO register = new UserDTO();
		register.setUserName("username");
		register.setPassword("password");
		register.setUserGroupName("usergroup1");
		register.setUserEmail("abcde");
		String json = new ObjectMapper().writeValueAsString(register);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signup").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.userEmail").value("Email should be valid"));
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

		when(authService.register(register)).thenReturn(true);

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
		when(authService.register(register)).thenReturn(false);

		ResponseEntity<?> response = loginController.signUp(register);

		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
		assertEquals("Error in saving user data", response.getBody());
	}

	/**
	 * This method is used to test the signIn method with no username
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignInWithNoUsername() throws Exception {
		SigninRequestDTO signin = new SigninRequestDTO();
		signin.setUsername(null);
		signin.setPassword("password");
		String json = new ObjectMapper().writeValueAsString(signin);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signin").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.username").value("Username is required"));

	}

	/**
	 * This method is used to test the signIn method with no password
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignInWithNoPassword() throws Exception {
		SigninRequestDTO signin = new SigninRequestDTO();
		signin.setUsername("username");
		signin.setPassword(null);
		String json = new ObjectMapper().writeValueAsString(signin);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signin").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.password").value("Password is required"));

	}

	/**
	 * This method is used to test the signIn method with empty password
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignInWithEmptyPassword() throws Exception {
		SigninRequestDTO signin = new SigninRequestDTO();
		signin.setUsername("username");
		signin.setPassword("");
		String json = new ObjectMapper().writeValueAsString(signin);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signin").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.password").value("Password is required"));

	}

	/**
	 * This method is used to test the signIn method with empty user name
	 * 
	 * @throws Exception
	 */
	@Test
	public void testSignInWithEmptyUsername() throws Exception {
		SigninRequestDTO signin = new SigninRequestDTO();
		signin.setUsername("");
		signin.setPassword("password");
		String json = new ObjectMapper().writeValueAsString(signin);

		mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/auth/signin").contentType(MediaType.APPLICATION_JSON)
				.content(json)).andExpect(MockMvcResultMatchers.status().isBadRequest())
				.andExpect(MockMvcResultMatchers.jsonPath("$.username").value("Username is required"));

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

		when(authService.signIn(signin)).thenReturn(signinResponseDTO);

		ResponseEntity<SigninResponseDTO> response = loginController.signIn(signin);

		assertEquals(HttpStatus.OK, response.getStatusCode());
		assertEquals(signinResponseDTO, response.getBody());

	}

}
