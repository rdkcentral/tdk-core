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

import com.rdkm.tdkservice.enums.BoxTypeCategory;
import com.rdkm.tdkservice.enums.Category;

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
import lombok.Data;

/*
 * The BoxType Entity
 */
@Data
@Entity
@Table(name = "box_type")
public class BoxType {

	/*
	 * The unique identifier of the box type.
	 */
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;

	/*
	 * The name of the box type.
	 */
	@Column(nullable = false, unique = true)
	private String name;

	/*
	 * The type
	 * 
	 */
	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private BoxTypeCategory type;

	/*
	 * The user group
	 * 
	 */
	@ManyToOne
	@JoinColumn(name = "user_group_id")
	private UserGroup userGroup;

	/*
	 * The category
	 * 
	 */
	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private Category category;

}
