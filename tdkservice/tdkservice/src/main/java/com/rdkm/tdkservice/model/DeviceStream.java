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

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.Data;

/*
 * Device Stream entity
 */
@Data
@Entity
@Table(name = "device_stream", uniqueConstraints = {
		@UniqueConstraint(columnNames = { "device_id", "stream_id", "ocap_id" }) })
public class DeviceStream {
	/**
	 * The unique identifier of the device stream.
	 */

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	/**
	 * The device entity.
	 */
	@ManyToOne
	@JoinColumn(name = "device_id", referencedColumnName = "id", nullable = false)
	private Device device;

	/**
	 * The streaming details entity
	 * 
	 */
	@ManyToOne
	@JoinColumn(name = "stream_id", referencedColumnName = "id", nullable = false)
	private StreamingDetails stream;

	/**
	 * The ocap id
	 */
	@Column(name = "ocap_id", nullable = false)
	private String ocapId;

}
