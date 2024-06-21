
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
package com.rdkm.tdkservice.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.rdkm.tdkservice.enums.StreamType;
import com.rdkm.tdkservice.model.StreamingDetails;

/*
 * This interface is used to interact with the StreamingDetails table in the database.
 */

@Repository
public interface StreamingDetailsRepository extends JpaRepository<StreamingDetails, Integer> {

	/**
	 * This method is used to check if a streaming detail exists with the given
	 * streamId.
	 * 
	 * @param streamId This is the streamId of the streaming detail to be checked.
	 * @return boolean This returns true if the streaming detail exists, false
	 *         otherwise.
	 */
	boolean existsByStreamId(String streamId);

	/**
	 * This method is used to find a streaming detail by its streamId.
	 * 
	 * @param streamId This is the streamId of the streaming detail to be found.
	 * @return StreamingDetails This returns the streaming detail with the given
	 *         streamId.
	 */
	List<StreamingDetails> findByStreamType(StreamType streamType);

	/**
	 * This method is used to find a streaming detail by its streamName.
	 * 
	 * @param streamId This is the streamId of the streaming detail to be found.
	 * @return StreamingDetails This returns the streaming detail with the given
	 *         streamId.
	 */
	StreamingDetails findByStreamId(String streamId);
}
