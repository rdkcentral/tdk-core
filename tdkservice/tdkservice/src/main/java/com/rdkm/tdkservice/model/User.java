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
package com.rdkm.tdkservice.model;

import java.util.Collection;
import java.util.Date;
import java.util.List;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import com.rdkm.tdkservice.enums.Theme;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.Temporal;
import jakarta.persistence.TemporalType;
import jakarta.persistence.UniqueConstraint;
import lombok.Data;

/**
 * User entity class
 */
@Data
@Entity
@Table(name = "user", uniqueConstraints = { @UniqueConstraint(columnNames = "username"),
		@UniqueConstraint(columnNames = "email") })
public class User implements UserDetails {

	private static final long serialVersionUID = 1L;

	/**
	 * The unique identifier of the user.
	 */

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;

	/*
	 * The User name of the user.
	 */

	@Column(nullable = false)
	private String username;

	/**
	 * The password of the user.
	 */
	private String password;

	/**
	 * The email of the user.
	 */

	@Column(nullable = false)
	private String email;

	/**
	 * The display name of the user.
	 */
	private String displayName;

	/**
	 * The created date of the user.
	 */
	@CreationTimestamp
	@Temporal(TemporalType.TIMESTAMP)
	@Column(name = "created_date")
	private String createdDate;

	/*
	 * The updated date of user
	 */

	@UpdateTimestamp
	@Column(name = "updated_at")
	private Date updatedAt;

	/**
	 * The status of the user.
	 */
	private String status;

	/**
	 * The theme of the user.
	 */
	@Enumerated(EnumType.STRING)
	private Theme theme;

	/**
	 * The user group of the user.
	 */
	@ManyToOne(cascade = CascadeType.PERSIST)
	@JoinColumn(name = "user_group_id")
	private UserGroup userGroup;

	/**
	 * The user role of the user.
	 */
	@ManyToOne(cascade = CascadeType.PERSIST)
	@JoinColumn(name = "user_role_id")
	private UserRole userRole;

	@Override
	public Collection<? extends GrantedAuthority> getAuthorities() {
		return List.of(new SimpleGrantedAuthority(userRole.getName()));
	}

	@Override
	public String getUsername() {
		return username;
	}

	@Override
	public boolean isAccountNonExpired() {
		return true;
	}

	@Override
	public boolean isAccountNonLocked() {
		return true;
	}

	@Override
	public boolean isCredentialsNonExpired() {
		return true;
	}

	@Override
	public boolean isEnabled() {
		return true;
	}

}
