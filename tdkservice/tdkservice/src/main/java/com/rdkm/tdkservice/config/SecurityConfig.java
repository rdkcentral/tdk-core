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
package com.rdkm.tdkservice.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import com.rdkm.tdkservice.serviceimpl.UserService;

/**
 * This class is used to configure the security for the application using Spring
 * Security and JWT token.
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

	@Autowired
	UserService userDetailsService;

	@Autowired
	JWTAuthFilter jwtAuthFilter;

	private static final Logger LOGGER = LoggerFactory.getLogger(SecurityConfig.class);

	/**
	 * This method is used to configure the security for the application using
	 * Spring Security and JWT token. This method will filter the apis.
	 * 
	 * @param httpSecurity - HttpSecurity
	 * @return SecurityFilterChain
	 * @throws Exception
	 */
	@Bean
	SecurityFilterChain filterChain(HttpSecurity httpSecurity) throws Exception {
		try {
			httpSecurity.csrf(AbstractHttpConfigurer::disable).cors(Customizer.withDefaults())
					// TODO : Change the user apis from here later also change the swagger ui
					.authorizeHttpRequests(request -> request
							.requestMatchers("/api/v1/auth/**", "/api/v1/usergroup/**", "/api/v1/userrole/**",
									"/api/v1/oem/**", "/api/v1/devicetype/**", "/api/v1/soc/**", "/api/v1/device/**",
									"/api/v1/module/**", "/api/v1/function/**", "/api/v1/parameter/**",
									"/api/v1/primitivetest/**", "/api/v1/script/**", "/api/v1/testsuite/**",
									"/api/v1/rdkcertification/**", "/api/execution/**", "/primitiveTest/**",
									"/execution/**", "/deviceGroup/**", "/api/v1/users/**",
									"/api/v1/executionScheduler/**", "/api/v1/analysis/**", "/api/v1/packagemanager/**")
							.permitAll().requestMatchers("/api/v1/users/**").hasAuthority("admin")
							.requestMatchers(SWAGGER_UI).permitAll().anyRequest().authenticated())
					.sessionManagement(manager -> manager.sessionCreationPolicy(SessionCreationPolicy.STATELESS))

					.authenticationProvider(authenticationProvider())
					.addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);
		} catch (Exception e) {
			LOGGER.error("Error while configuring the security filter chain", e);

		}

		return httpSecurity.build();

	}

	/**
	 * This method is used to configure the swagger ui
	 */
	private static final String[] SWAGGER_UI = { "/swagger-resources/**", "/swagger-ui.html", "/swagger-ui/**",
			"/v3/api-docs/**" };

	/**
	 * This method is used to configure the authentication provider
	 * 
	 * @return
	 */
	@Bean
	AuthenticationProvider authenticationProvider() {
		// Configure the authentication provider
		DaoAuthenticationProvider daoAuthenticationProvider = new DaoAuthenticationProvider();
		daoAuthenticationProvider.setUserDetailsService(userDetailsService);
		daoAuthenticationProvider.setPasswordEncoder(PasswordEncoder());

		return daoAuthenticationProvider;
	}

	/**
	 * This method is used to configure the password encoder
	 * 
	 * @return
	 */
	@Bean
	PasswordEncoder PasswordEncoder() {
		return new BCryptPasswordEncoder();

	}

	/**
	 * This method is used to configure the authentication manager
	 * 
	 * @param authenticationConfiguration
	 * @return AuthenticationManager
	 * @throws Exception
	 */
	@Bean
	AuthenticationManager authenticationManager(AuthenticationConfiguration authenticationConfiguration)
			throws Exception {

		return authenticationConfiguration.getAuthenticationManager();

	}

}
