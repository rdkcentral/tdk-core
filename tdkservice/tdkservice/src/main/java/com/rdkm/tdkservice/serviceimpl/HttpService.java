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

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

/*
 * The HttpService class provides methods for sending HTTP requests.
 */
@Service
public class HttpService {

	private static final Logger LOGGER = LoggerFactory.getLogger(HttpService.class);

	private final RestTemplate restTemplate;

	public HttpService(RestTemplate restTemplate) {
		this.restTemplate = restTemplate;
	}

	/**
	 * Sends a GET request to the specified URL with the provided headers.
	 *
	 * @param url     the URL to send the GET request to; must not be null or empty
	 * @param headers a map of headers to include in the request; can be null
	 * @return a ResponseEntity containing the response as a String
	 * @throws IllegalArgumentException if the URL is null or empty
	 * @throws RuntimeException         if an error occurs during the GET request
	 */
	public ResponseEntity<String> sendGetRequest(String url, Map<String, String> headers) {
		if (url == null || url.isEmpty()) {
			LOGGER.error("URL is null or empty");
			throw new IllegalArgumentException("URL must not be null or empty");
		}

		HttpHeaders httpHeaders = new HttpHeaders();
		if (headers != null) {
			headers.forEach(httpHeaders::set);
		}
		HttpEntity<String> entity = new HttpEntity<>(httpHeaders);

		try {
			LOGGER.info("Sending GET request to URL: {}", url);
			return restTemplate.exchange(url, HttpMethod.GET, entity, String.class);
		} catch (RestClientException e) {
			LOGGER.error("Error during GET request to URL: {}", url, e);
			throw new RuntimeException("Error during GET request", e);
		}
	}

	/**
	 * Sends a POST request to the specified URL with the given request body and
	 * headers.
	 *
	 * @param url         the URL to send the POST request to; must not be null or
	 *                    empty
	 * @param requestBody the body of the request; must not be null
	 * @param headers     a map of headers to include in the request; can be null
	 * @return a ResponseEntity containing the response as a String
	 * @throws IllegalArgumentException if the URL or request body is null or empty
	 * @throws RuntimeException         if an error occurs during the POST request
	 */
	public ResponseEntity<String> sendPostRequest(String url, Object requestBody, Map<String, String> headers) {
		if (url == null || url.isEmpty()) {
			LOGGER.error("URL is null or empty");
			throw new IllegalArgumentException("URL must not be null or empty");
		}
		if (requestBody == null) {
			LOGGER.error("Request body is null");
			throw new IllegalArgumentException("Request body must not be null");
		}

		HttpHeaders httpHeaders = new HttpHeaders();
		httpHeaders.setContentType(MediaType.APPLICATION_JSON);
		if (headers != null) {
			headers.forEach(httpHeaders::set);
		}
		HttpEntity<Object> entity = new HttpEntity<>(requestBody, httpHeaders);

		try {
			LOGGER.info("Sending POST request to URL: {}", url);
			return restTemplate.exchange(url, HttpMethod.POST, entity, String.class);
		} catch (RestClientException e) {
			LOGGER.error("Error during POST request to URL: {}", url, e);
			throw new RuntimeException("Error during POST request", e);
		}
	}

}
