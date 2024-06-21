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

import com.rdkm.tdkservice.enums.Category;
import com.rdkm.tdkservice.enums.DeviceStatus;

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
import lombok.Data;

/**
 * Represents the details of a device entity.
 */
@Data
@Entity
public class Device {

	/**
	 * Represents the unique identifier for the device.
	 */
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	/**
	 * Represents the stbip of the device.
	 */
	@Column(unique = true)
	private String stbIp;

	/**
	 * Represents the stbName of the device.
	 */
	@Column(unique = true)
	private String stbName;

	/**
	 * Represents the stbPort of the device.
	 */
	@Column(nullable = true, columnDefinition = "varchar(255) default '8087'")
	private String stbPort;

	/**
	 * Represents the statusPort of the device.
	 */
	@Column(nullable = true, columnDefinition = "varchar(255) default '8088'")
	private String statusPort;

	/**
	 * Represents the agentMonitorPort of the device.
	 */
	@Column(nullable = true, columnDefinition = "varchar(255) default '8090'")
	private String agentMonitorPort;

	/**
	 * Represents the logTransferPort of the device.
	 */
	@Column(nullable = true, columnDefinition = "varchar(255) default '69'")
	private String logTransferPort;

	/**
	 * Represents the macId of the device.
	 */
	@Column(unique = true)
	private String macId;

	/**
	 * Represents the boxType of the device.
	 */
	@ManyToOne(cascade = CascadeType.PERSIST)
	@JoinColumn(name = "boxtype_id", nullable = false)
	private BoxType boxType;

	/**
	 * Represents the boxManufacturer of the device.
	 * 
	 */
	@ManyToOne(cascade = CascadeType.PERSIST)
	@JoinColumn(name = "boxmanufacturer_id", nullable = false)
	private BoxManufacturer boxManufacturer;

	/**
	 * Represents the socVendor of the device
	 */
	@ManyToOne(cascade = CascadeType.PERSIST)
	@JoinColumn(name = "socvendor_id", nullable = false)
	private SocVendor socVendor;

	/**
	 * Represents the deviceStatus of the device.
	 */
	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private DeviceStatus deviceStatus = DeviceStatus.NOT_FOUND;

	/**
	 * Represents the recorderId of the device.
	 */
	private String recorderId;

	/**
	 * Represents the gatewayIp of the device.
	 */
	private String gatewayIp;

	/**
	 * Represents the is Thunder Enabled.
	 */
	private boolean isThunderEnabled;

	/**
	 * Represents the thunderPort of the device.
	 */
	private String thunderPort;

	/**
	 * Represents the userGroup of the device.
	 */
	@ManyToOne
	@JoinColumn(name = "user_group_id")
	private UserGroup userGroup;

	/**
	 * Represents the category of the device.
	 */
	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private Category category;
}