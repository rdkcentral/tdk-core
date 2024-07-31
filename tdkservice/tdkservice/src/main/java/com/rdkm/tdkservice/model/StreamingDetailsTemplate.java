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

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.EqualsAndHashCode;

/*
 * The Streaming details template db model class
 */

@Data
@Entity
@EqualsAndHashCode(callSuper = true)
@Table(name = "streaming_detail_template")
public class StreamingDetailsTemplate extends BaseEntity {

	/*
	 * The name of the streaming details template.
	 */
	@Column(nullable = false)
	private String templateName;

	/*
	 * The ocap id of the streaming details template.
	 */
	private String ocapId;

	/*
	 * The streaming details of the streaming details template.
	 */
	@ManyToOne(cascade = CascadeType.PERSIST)
	@JoinColumn(name = "streaming_details_id")
	private StreamingDetails streamingDetails;

}
