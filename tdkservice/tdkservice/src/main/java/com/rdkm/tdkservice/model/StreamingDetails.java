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

import com.rdkm.tdkservice.enums.AudioType;
import com.rdkm.tdkservice.enums.ChannelType;
import com.rdkm.tdkservice.enums.StreamType;
import com.rdkm.tdkservice.enums.VideoType;

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
import jakarta.persistence.UniqueConstraint;
import lombok.Data;

/**
 * Represents the details of a streaming entity.
 */
@Data
@Entity
@Table(name = "streaming_detail", uniqueConstraints = { @UniqueConstraint(columnNames = "streamId") })
public class StreamingDetails {

	/**
	 * The unique identifier of the streaming detail.
	 */
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;

	/**
	 * The unique identifier of the stream.
	 */
	@Column(nullable = false, unique = true)
	private String streamId;

	/**
	 * The type of channel for the streaming detail.
	 */
	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private ChannelType channelType;

	/**
	 * The type of video for the streaming detail.
	 */
	@Enumerated(EnumType.STRING)
	private VideoType videoType;

	/**
	 * The type of audio for the streaming detail.
	 */
	@Enumerated(EnumType.STRING)
	private AudioType audioType;

	/**
	 * The type of stream for the streaming detail.
	 */
	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private StreamType streamType;

	/**
	 * The user group associated with the streaming detail.
	 */
	@ManyToOne(cascade = CascadeType.PERSIST)
	@JoinColumn(name = "user_group_id")
	private UserGroup userGroup;
}
