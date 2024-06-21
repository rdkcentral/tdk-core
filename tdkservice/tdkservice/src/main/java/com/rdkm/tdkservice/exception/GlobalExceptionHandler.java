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
package com.rdkm.tdkservice.exception;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.InternalAuthenticationServiceException;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.resource.NoResourceFoundException;

import com.rdkm.tdkservice.response.ErrorResponse;

/**
 * This class is used to handle the global exceptions using Spring boot
 * exception handling mechanism
 */
@ControllerAdvice
public class GlobalExceptionHandler {
	private static final Logger logger = Logger.getLogger(GlobalExceptionHandler.class.getName());

	/**
	 * This method is used to handle the validation exceptions and return the error
	 * response with the field name and error message in the response body for
	 * controller methods with @Valid annotation
	 */
	@ExceptionHandler(MethodArgumentNotValidException.class)
	@ResponseStatus(HttpStatus.BAD_REQUEST)
	@ResponseBody
	public ResponseEntity<Map<String, String>> handleValidationExceptions(MethodArgumentNotValidException ex) {
		logger.info("Validation failed: " + ex.getMessage());
		Map<String, String> errors = new HashMap<>();
		ex.getBindingResult().getAllErrors().forEach((error) -> {
			String fieldName = ((FieldError) error).getField();
			String errorMessage = error.getDefaultMessage();
			errors.put(fieldName, errorMessage);
		});
		return ResponseEntity.badRequest().body(errors);
	}

	/*
	 * This method is used to handle user name not found exception and return the
	 * error response with the error message in the response body
	 */

	@ExceptionHandler(UsernameNotFoundException.class)
	public ResponseEntity<String> handleUsernameNotFoundException() {
		return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User not found");
	}

	/**
	 * This method is used to handle the ResourceAlreadyExistsException and return
	 * the error response with the error message in the response body
	 * 
	 * @param ex
	 * @return
	 */
	@ExceptionHandler(ResourceAlreadyExistsException.class)
	public ResponseEntity<Object> handleResourceAlreadyRegistered(ResourceAlreadyExistsException ex) {
		ErrorResponse error = new ErrorResponse(ex.getMessage());
		return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
	}

	/**
	 * This method is used to handle the ResourceNotFoundException and return the
	 * error response with the error message in the response body
	 * 
	 * @param ex
	 * @return
	 */

	@ExceptionHandler(ResourceNotFoundException.class)
	public ResponseEntity<Object> handleResourceNotExists(ResourceNotFoundException ex) {
		ErrorResponse error = new ErrorResponse(ex.getMessage());
		return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
	}

	/**
	 * This method is used to handle the NoResourceFoundException and return the
	 * error response with the error message in the response body
	 * 
	 * @param ex
	 * @return
	 */
	@ExceptionHandler(NoResourceFoundException.class)
	public ResponseEntity<Object> handleResourceNotExists(NoResourceFoundException ex) {
		ErrorResponse error = new ErrorResponse("API endpoint not found");
		return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
	}

	/**
	 * This method is used to handle the Global Exception and return the error
	 * response with the error message in the response body
	 * 
	 * @param ex
	 * @param request
	 * @return
	 */

	@ExceptionHandler(Exception.class)
	public ResponseEntity<Object> handleGlobalException(Exception ex, WebRequest request) {
		ex.printStackTrace();

		return new ResponseEntity<>("An unexpected error occurred: " + ex.getMessage(),
				HttpStatus.INTERNAL_SERVER_ERROR);
	}

	/**
	 * This method is used to handle the BadCredentialsException and return the
	 * error response with the error message in the response body
	 * 
	 * @return
	 * 
	 */

	@ExceptionHandler(BadCredentialsException.class)
	public ResponseEntity<String> handleBadCredentialsException() {
		return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Incorrect password");
	}

	/**
	 * This method is used to handle the InternalAuthenticationServiceException and
	 * return the error response with the error message in the response body
	 * 
	 * @return
	 * 
	 */
	@ExceptionHandler(InternalAuthenticationServiceException.class)
	public ResponseEntity<String> handleInternalAuthenticationServiceException() {
		return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Incorrect username or password");
	}

	/**
	 * This method is used to handle the UserInputException and return the error
	 * response with the error message in the response body
	 * 
	 * @param ex
	 * @return
	 */
	@ExceptionHandler(UserInputException.class)
	public ResponseEntity<ErrorResponse> handleUserInputException(UserInputException ex) {
		ErrorResponse errorResponse = new ErrorResponse(ex.getMessage());
		return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errorResponse);

	}

	/**
	 * This method is used to handle the DeleteFailedException and return the error
	 * response with the error message in the response body
	 * 
	 * @param ex
	 * @return
	 */
	@ExceptionHandler(DeleteFailedException.class)
	public ResponseEntity<ErrorResponse> handleDeleteFailedException(DeleteFailedException ex) {
		ErrorResponse errorResponse = new ErrorResponse(ex.getMessage());
		return ResponseEntity.status(HttpStatus.CONFLICT).body(errorResponse);
	}

}