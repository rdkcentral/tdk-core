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
package com.rdkm.tdkservice.enums;

/**
 * This enum class is used to define the different types of channels.
 */
public enum ChannelType {

	HD("HD"), SD("SD"), RADIO("RADIO");

	private String name;

	ChannelType(String name) {
		this.name = name;

	}

	public String getName() {
		return name;
	}

	/**
	 * This method is used to get the ChannelType enum based on the name of the
	 * channel type.
	 * 
	 * @param name This is the name of the channel type.
	 * @return ChannelType This returns the ChannelType enum based on the name of
	 *         the channel type.
	 */

	public static ChannelType getChannelType(String name) {
		for (ChannelType channelType : ChannelType.values()) {
			if (channelType.getName().equals(name)) {
				return channelType;
			}
		}
		return null;
	}
}
