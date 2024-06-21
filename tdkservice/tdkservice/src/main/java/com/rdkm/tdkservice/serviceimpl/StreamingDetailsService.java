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

import java.util.List;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;

import com.rdkm.tdkservice.dto.StreamingDetailsDTO;
import com.rdkm.tdkservice.dto.StreamingDetailsUpdateDTO;
import com.rdkm.tdkservice.enums.AudioType;
import com.rdkm.tdkservice.enums.ChannelType;
import com.rdkm.tdkservice.enums.StreamType;
import com.rdkm.tdkservice.enums.VideoType;
import com.rdkm.tdkservice.exception.DeleteFailedException;
import com.rdkm.tdkservice.exception.ResourceAlreadyExistsException;
import com.rdkm.tdkservice.exception.ResourceNotFoundException;
import com.rdkm.tdkservice.exception.UserInputException;
import com.rdkm.tdkservice.model.StreamingDetails;
import com.rdkm.tdkservice.model.UserGroup;
import com.rdkm.tdkservice.repository.StreamingDetailsRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.service.IStreamingDetailsService;
import com.rdkm.tdkservice.util.Constants;
import com.rdkm.tdkservice.util.MapperUtils;
import com.rdkm.tdkservice.util.Utils;

import jakarta.validation.Valid;

/**
 * This class provides the implementation for the StreamingDetailsService
 * interface. It provides methods to perform CRUD operations on StreamingDetails
 * entities.
 */
@Service
public class StreamingDetailsService implements IStreamingDetailsService {

	private static final Logger LOGGER = LoggerFactory.getLogger(StreamingDetailsService.class);

	@Autowired
	StreamingDetailsRepository streamingDetailsRepository;

	@Autowired
	UserGroupRepository userGroupRepository;

	/**
	 * This method is used to create a new StreamingDetails.
	 * 
	 * @param streamingDetailsRequest This is the request object containing the
	 *                                details of the StreamingDetails to be created.
	 * @return boolean This returns true if the StreamingDetails was created
	 *         successfully, false otherwise.
	 */

	@Override
	public boolean createStreamingDetails(@Valid StreamingDetailsDTO streamingDetailsRequest) {
		LOGGER.info("Received create streaming details request: " + streamingDetailsRequest.toString());

		if (streamingDetailsRepository.existsByStreamId(streamingDetailsRequest.getStreamingDetailsId())) {
			LOGGER.info("Streaming details already exists with the same id: "
					+ streamingDetailsRequest.getStreamingDetailsId());
			throw new ResourceAlreadyExistsException(Constants.STREAMING_DETAILS_ID,
					streamingDetailsRequest.getStreamingDetailsId());
		}

		StreamingDetails streamingDetails = createStreamingDetailsObject(streamingDetailsRequest);
		LOGGER.info("Created streaming details object: " + streamingDetails.toString());
		return saveStreamingDetails(streamingDetails);
	}

	/**
	 * This method is used to delete a StreamingDetails by its id.
	 * 
	 * @param id This is the id of the StreamingDetails to be deleted.
	 */

	@Override
	public List<StreamingDetailsDTO> findAllStreamingDetails() {
		LOGGER.info("Received request to find all streaming details");
		List<StreamingDetails> streamingDetails = streamingDetailsRepository.findAll();
		if (streamingDetails.isEmpty()) {
			LOGGER.info("No streaming details found");
			return null;
		}
		return streamingDetails.stream().map(MapperUtils::convertToStreamingDetailsDTO).collect(Collectors.toList());
	}

	/**
	 * This method is used to update a StreamingDetails.
	 * 
	 * @param streamingDetailsUpdateRequest This is the request object containing
	 *                                      the updated details of the
	 *                                      StreamingDetails.
	 * @param id                            This is the id of the StreamingDetails
	 *                                      to be updated.
	 * @return StreamingDetailsDTO This returns the updated StreamingDetails.
	 */

	@Override
	public StreamingDetailsUpdateDTO updateStreamingDetails(StreamingDetailsUpdateDTO streamingDetailsUpdateRequest) {
		LOGGER.info("Received update streaming details request: " + streamingDetailsUpdateRequest.toString());

		StreamingDetails streamingDetails = getStreamingDetails(streamingDetailsUpdateRequest.getStreamingDetailsId());

		validateAndUpdateStreamName(streamingDetails, streamingDetailsUpdateRequest);
		updateChannelType(streamingDetails, streamingDetailsUpdateRequest);
		updateVideoType(streamingDetails, streamingDetailsUpdateRequest);
		updateAudioType(streamingDetails, streamingDetailsUpdateRequest);

		saveUpdatedStreamingDetails(streamingDetails);

		LOGGER.info("updatedStreamingDetails:" + streamingDetails);
		return MapperUtils.streamingDetailsUpdate(streamingDetails);
	}

	/**
	 * This method is used to find all streaming details ids by stream type.
	 * 
	 * @return List<String> This returns a list of all streaming details ids.
	 */
	@Override
	public List<String> getStreamingDetailsIdsByStreamType() {
		LOGGER.info("Received request to find all streaming details ids by stream type");
		List<StreamingDetails> streamingDetailsIds = streamingDetailsRepository
				.findByStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		if (streamingDetailsIds.isEmpty()) {
			LOGGER.info("No streaming details ids found");
			return null;
		}

		return streamingDetailsIds.stream().map(StreamingDetails::getStreamId).collect(Collectors.toList());
	}

	/**
	 * This method is used to delete a StreamingDetails by its id.
	 * 
	 * @param id This is the id of the StreamingDetails to be deleted.
	 */

	@Override
	public void deleteStreamingDetails(Integer streamId) {
		LOGGER.info("Received request to delete streaming details with id: " + streamId);
		if (!streamingDetailsRepository.existsById(streamId)) {
			LOGGER.info("No streaming details found with id: " + streamId);
			throw new ResourceNotFoundException(Constants.STREAMING_DETAILS_ID, streamId.toString());
		}
		try {
			streamingDetailsRepository.deleteById(streamId);
		} catch (DataIntegrityViolationException e) {
			LOGGER.error("Error occurred while deleting streaming details with id: " + streamId, e);
			throw new DeleteFailedException();
		}

	}

	/**
	 * This method is used to find all radio streaming details ids.
	 * 
	 * @return List<String> This returns a list of all radio streaming details ids.
	 */
	@Override
	public List<String> getRadioStreamingDetailsId() {
		LOGGER.info("Received request to find all radio streaming details ids");
		List<StreamingDetails> radioStreamingDetailsIds = streamingDetailsRepository
				.findByStreamType(StreamType.getStreamType(Constants.RADIO_STREAM_TYPE));
		if (radioStreamingDetailsIds.isEmpty()) {
			LOGGER.info("No radio streaming details ids found");
			return null;
		}
		return radioStreamingDetailsIds.stream().map(StreamingDetails::getStreamId).collect(Collectors.toList());

	}

	/**
	 * This method is used to create a new StreamingDetails object.
	 * 
	 * @param streamingDetailsRequest This is the request object containing the
	 *                                details of the StreamingDetails to be created.
	 * @return StreamingDetails This returns the StreamingDetails object.
	 */
	private StreamingDetails createStreamingDetailsObject(StreamingDetailsDTO streamingDetailsRequest) {
		StreamingDetails streamingDetails = new StreamingDetails();
		switch (streamingDetailsRequest.getStreamType()) {
		case Constants.RADIO_STREAM_TYPE:
			if (streamingDetailsRequest.getStreamingDetailsId().startsWith(Constants.STARTING_WITH_R)) {
				streamingDetails.setStreamId(streamingDetailsRequest.getStreamingDetailsId());
				streamingDetails.setStreamType(StreamType.getStreamType(streamingDetailsRequest.getStreamType()));
				streamingDetails.setChannelType(ChannelType.RADIO);
				streamingDetails.setVideoType(null);
				streamingDetails.setAudioType(null);
			} else {
				LOGGER.error("Stream ID for radio type must start with 'R'");
				throw new UserInputException("Stream ID for radio type must start with 'R'");
			}
			break;
		case Constants.VIDEO_STREAM_TYPE:
			if (!streamingDetailsRequest.getStreamingDetailsId().startsWith(Constants.STARTING_WITH_R)) {
				streamingDetails.setStreamId(streamingDetailsRequest.getStreamingDetailsId());
				streamingDetails.setStreamType(StreamType.getStreamType(streamingDetailsRequest.getStreamType()));
				streamingDetails.setChannelType(ChannelType.getChannelType(streamingDetailsRequest.getChannelType()));
				streamingDetails.setVideoType(VideoType.getVideoType(streamingDetailsRequest.getVideoType()));
				streamingDetails.setAudioType(AudioType.getAudioType(streamingDetailsRequest.getAudioType()));
			} else {
				LOGGER.error("Stream ID for video type must start with 'R'");
				throw new UserInputException("Stream ID for video type must not start with 'R'");

			}
			break;
		}
		UserGroup userGroup = userGroupRepository.findByName(streamingDetailsRequest.getStreamingDetailsUserGroup());
		streamingDetails.setUserGroup(userGroup);

		return streamingDetails;
	}

	/**
	 * This method is used to save a StreamingDetails object.
	 * 
	 * @param streamingDetails This is the StreamingDetails object to be saved.
	 * @return boolean This returns true if the StreamingDetails was saved
	 *         successfully, false otherwise.
	 */
	private boolean saveStreamingDetails(StreamingDetails streamingDetails) {
		try {
			streamingDetailsRepository.save(streamingDetails);
			return true;
		} catch (Exception e) {
			LOGGER.error("Error in saving streaming details data: " + e.getMessage());
			return false;
		}
	}

	/**
	 * This method is used to find a StreamingDetails by its id.
	 * 
	 * @param streamId This is the id of the StreamingDetails to be found.
	 * @return StreamingDetailsDTO This returns the found StreamingDetails.
	 */

	@Override
	public StreamingDetailsDTO findById(Integer streamId) {
		LOGGER.info("Received request to find streaming details by stream id: " + streamId);
		StreamingDetails streamingDetails = streamingDetailsRepository.findById(streamId)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.STREAMING_DETAILS_ID, streamId.toString()));
		return MapperUtils.convertToStreamingDetailsDTO(streamingDetails);
	}

	/**
	 * This method is used to find a StreamingDetails by its id.
	 * 
	 * @param id This is the id of the StreamingDetails to be found.
	 * @return StreamingDetails This returns the found StreamingDetails.
	 */
	private StreamingDetails getStreamingDetails(Integer id) {
		return streamingDetailsRepository.findById(id)
				.orElseThrow(() -> new ResourceNotFoundException(Constants.STREAMING_DETAILS_ID, id.toString()));
	}

	/**
	 * This method is used to update the audio type of a StreamingDetails object.
	 * 
	 * @param streamingDetails This is the StreamingDetails object to be updated.
	 * @param request          This is the request object containing the updated
	 *                         details of the StreamingDetails.
	 */
	private void validateAndUpdateStreamName(StreamingDetails streamingDetails, StreamingDetailsUpdateDTO request) {
		if (!Utils.isEmpty(request.getStreamId())) {
			validateStreamName(request);
			checkIfStreamNameExists(streamingDetails, request);
			streamingDetails.setStreamId(request.getStreamId());
		}
	}

	/**
	 * This method is used to validate the stream name based on the stream type.
	 * 
	 * @param request This is the request object containing the updated details of
	 *                the StreamingDetails.
	 */
	private void validateStreamName(StreamingDetailsUpdateDTO request) {
		if (request.getStreamType().equals(Constants.RADIO_STREAM_TYPE)
				&& !request.getStreamId().startsWith(Constants.STARTING_WITH_R)) {
			LOGGER.error("Stream ID for radio type must start with 'R'");
			throw new UserInputException("Stream ID for radio type must start with 'R'");
		}
		if (request.getStreamType().equals(Constants.VIDEO_STREAM_TYPE)
				&& request.getStreamId().startsWith(Constants.STARTING_WITH_R)) {
			LOGGER.error("Stream ID for video type must not start with 'R'");
			throw new UserInputException("Stream ID for video type must not start with 'R'");
		}
	}

	/**
	 * This method is used to check if a StreamingDetails object with the same name
	 * already exists.
	 * 
	 * @param streamingDetails This is the StreamingDetails object to be updated.
	 * @param request          This is the request object containing the updated
	 *                         details of the StreamingDetails.
	 */

	private void checkIfStreamNameExists(StreamingDetails streamingDetails, StreamingDetailsUpdateDTO request) {
		if (streamingDetailsRepository.existsByStreamId(request.getStreamId())
				&& !streamingDetails.getStreamId().equals(request.getStreamId())) {
			LOGGER.info("Streaming details already exists with the same id: " + request.getStreamId());
			throw new ResourceAlreadyExistsException(Constants.STREAMING_DETAILS_ID, request.getStreamId());
		}
	}

	/**
	 * This method is used to update the channel type of a StreamingDetails object.
	 * 
	 * @param streamingDetails This is the StreamingDetails object to be updated.
	 * @param request          This is the request object containing the updated
	 *                         details of the StreamingDetails.
	 */

	private void updateChannelType(StreamingDetails streamingDetails, StreamingDetailsUpdateDTO request) {
		if (!Utils.isEmpty(request.getChannelType())) {
			ChannelType channelType = ChannelType.getChannelType(request.getChannelType());
			if (channelType != null) {
				streamingDetails.setChannelType(channelType);
			} else {
				LOGGER.error("Channel type not found: " + request.getChannelType());
				throw new ResourceNotFoundException(Constants.CHANNEL_TYPE, request.getChannelType());
			}
		}
	}

	/**
	 * This method is used to update the video type of a StreamingDetails object.
	 * 
	 * @param streamingDetails This is the StreamingDetails object to be updated.
	 * @param request          This is the request object containing the updated
	 *                         details of the StreamingDetails.
	 */
	private void updateVideoType(StreamingDetails streamingDetails, StreamingDetailsUpdateDTO request) {
		if (!Utils.isEmpty(request.getVideoType())) {
			VideoType videoType = VideoType.getVideoType(request.getVideoType());
			if (videoType != null) {
				streamingDetails.setVideoType(videoType);
			} else {
				LOGGER.error("Video type not found: " + request.getVideoType());
				throw new ResourceNotFoundException(Constants.VIDEO_TYPE, request.getVideoType());
			}

		}
	}

	/**
	 * This method is used to update the audio type of a StreamingDetails object.
	 * 
	 * @param streamingDetails This is the StreamingDetails object to be updated.
	 * @param request          This is the request object containing the updated
	 *                         details of the Streaming Details.
	 */
	private void updateAudioType(StreamingDetails streamingDetails, StreamingDetailsUpdateDTO request) {
		if (!Utils.isEmpty(request.getAudioType())) {
			AudioType audioType = AudioType.getAudioType(request.getAudioType());
			if (audioType != null) {
				streamingDetails.setAudioType(audioType);
			} else {
				LOGGER.error("Audio type not found: " + request.getAudioType());
				throw new ResourceNotFoundException(Constants.AUDIO_TYPE, request.getAudioType());
			}
		}
	}

	/**
	 * This method is used to save a StreamingDetails object.
	 * 
	 * @param streamingDetails This is the StreamingDetails object to be saved.
	 */
	private void saveUpdatedStreamingDetails(StreamingDetails streamingDetails) {
		try {
			streamingDetailsRepository.save(streamingDetails);
		} catch (Exception e) {
			LOGGER.error("Error in Updating streaming details data: " + e.getMessage());
			throw new RuntimeException("Error in Updating streaming details data");
		}
	}
}
