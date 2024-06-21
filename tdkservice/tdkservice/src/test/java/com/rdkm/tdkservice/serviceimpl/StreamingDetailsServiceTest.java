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

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.dao.DataIntegrityViolationException;

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
import com.rdkm.tdkservice.repository.StreamingDetailsRepository;
import com.rdkm.tdkservice.repository.UserGroupRepository;
import com.rdkm.tdkservice.util.Constants;

/**
 * This class is used to test the StreamingDetailsService class
 */
public class StreamingDetailsServiceTest {

	@InjectMocks
	StreamingDetailsService streamingDetailsService;

	@Mock
	StreamingDetailsRepository streamingDetailsRepository;

	@Mock
	UserGroupRepository userGroupRepository;

	@BeforeEach
	public void setup() {
		MockitoAnnotations.openMocks(this);
	}

	/**
	 * Test case to verify the successful creation of streaming details.
	 */
	@Test
	public void shouldCreateStreamingDetailsSuccessfully() {
		StreamingDetailsDTO streamingDetailsDTO = new StreamingDetailsDTO();
		streamingDetailsDTO.setStreamingDetailsId("123");
		streamingDetailsDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);
		streamingDetailsDTO.setChannelType(ChannelType.HD.name());
		streamingDetailsDTO.setVideoType(VideoType.MPEG2.name());
		streamingDetailsDTO.setAudioType(AudioType.MP3.name());
		streamingDetailsDTO.setStreamingDetailsUserGroup("userGroup");

		when(streamingDetailsRepository.existsByStreamId(anyString())).thenReturn(false);
		when(streamingDetailsRepository.save(any(StreamingDetails.class))).thenAnswer(i -> {
			StreamingDetails streamingDetails = i.getArgument(0);
			streamingDetails.setId(1);
			return streamingDetails;
		});

		boolean result = streamingDetailsService.createStreamingDetails(streamingDetailsDTO);

		assertTrue(result);
	}

	/**
	 * Test case to verify the successful creation of radio streaming details.
	 */
	@Test
	public void shouldCreateRadioStreamingDetailsSuccessfully() {
		StreamingDetailsDTO streamingDetailsDTO = new StreamingDetailsDTO();
		streamingDetailsDTO.setStreamingDetailsId("R123");
		streamingDetailsDTO.setStreamType(Constants.RADIO_STREAM_TYPE);

		when(streamingDetailsRepository.existsByStreamId(anyString())).thenReturn(false);
		when(streamingDetailsRepository.save(any(StreamingDetails.class))).thenAnswer(i -> {
			StreamingDetails streamingDetails = i.getArgument(0);
			streamingDetails.setId(1);
			return streamingDetails;
		});

		boolean result = streamingDetailsService.createStreamingDetails(streamingDetailsDTO);

		assertTrue(result);
	}

	/**
	 * Test case to verify that a UserInputException is thrown when creating radio
	 * streaming details with a streaming details ID starting with 'R'.
	 */
	@Test
	public void shouldThrowUserInputExceptionWhenCreatingRadioStreamingDetailsWithStartingWithR() {
		StreamingDetailsDTO streamingDetailsDTO = new StreamingDetailsDTO();
		streamingDetailsDTO.setStreamingDetailsId("123");
		streamingDetailsDTO.setStreamType(Constants.RADIO_STREAM_TYPE);

		assertThrows(UserInputException.class, () -> {
			streamingDetailsService.createStreamingDetails(streamingDetailsDTO);
		});
	}

	/**
	 * Test case to verify that a UserInputException is thrown when creating a
	 * streaming details with a streaming details ID starting with 'R'.
	 * 
	 * This test ensures that the createStreamingDetails method of the
	 * StreamingDetailsService throws a UserInputException when the streaming
	 * details ID starts with 'R'. It creates a new StreamingDetailsDTO object with
	 * a streaming details ID starting with 'R' and sets the stream type to
	 * Constants.VIDEO_STREAM_TYPE. The assertThrows method is used to verify that a
	 * UserInputException is thrown when the createStreamingDetails method is called
	 * with the streamingDetailsDTO object.
	 */
	@Test
	public void shouldThrowUserInputExceptionWhenCreatingStreamingDetailsMustNotStartsWithR() {
		StreamingDetailsDTO streamingDetailsDTO = new StreamingDetailsDTO();
		streamingDetailsDTO.setStreamingDetailsId("R123");
		streamingDetailsDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);

		assertThrows(UserInputException.class, () -> {
			streamingDetailsService.createStreamingDetails(streamingDetailsDTO);
		});
	}

	/**
	 * Test case to verify that a ResourceAlreadyExistsException is thrown when
	 * creating a streaming details with an existing ID.
	 */
	@Test
	public void shouldThrowResourceAlreadyExistsExceptionWhenCreatingStreamingDetailsWithExistingId() {
		StreamingDetailsDTO streamingDetailsDTO = new StreamingDetailsDTO();
		streamingDetailsDTO.setStreamingDetailsId("123");
		streamingDetailsDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);
		streamingDetailsDTO.setChannelType(ChannelType.HD.name());
		streamingDetailsDTO.setVideoType(VideoType.MPEG2.name());
		streamingDetailsDTO.setAudioType(AudioType.MP3.name());
		streamingDetailsDTO.setStreamingDetailsUserGroup("userGroup");

		when(streamingDetailsRepository.existsByStreamId(anyString())).thenReturn(true);

		assertThrows(ResourceAlreadyExistsException.class, () -> {
			streamingDetailsService.createStreamingDetails(streamingDetailsDTO);
		});
	}

	/**
	 * Test case to verify that the createStreamingDetails method returns false when
	 * saving throws an exception.
	 */
	@Test
	public void shouldReturnFalseWhileSavingThrowsException() {
		StreamingDetailsDTO streamingDetailsDTO = new StreamingDetailsDTO();
		streamingDetailsDTO.setStreamingDetailsId("123");
		streamingDetailsDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);
		streamingDetailsDTO.setChannelType(ChannelType.HD.name());
		streamingDetailsDTO.setVideoType(VideoType.MPEG2.name());
		streamingDetailsDTO.setAudioType(AudioType.MP3.name());
		streamingDetailsDTO.setStreamingDetailsUserGroup("userGroup");

		when(streamingDetailsRepository.save(any(StreamingDetails.class))).thenThrow(new RuntimeException());

		boolean result = streamingDetailsService.createStreamingDetails(streamingDetailsDTO);

		assertFalse(result);
	}

	/**
	 * Test case to verify that all streaming details are returned successfully.
	 */
	@Test
	public void shouldReturnAllStreamingDetails() {
		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setId(1);
		streamingDetails.setStreamId("123");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		streamingDetails.setChannelType(ChannelType.HD);
		streamingDetails.setVideoType(VideoType.MPEG2);
		streamingDetails.setAudioType(AudioType.MP3);

		when(streamingDetailsRepository.findAll()).thenReturn(Arrays.asList(streamingDetails));

		List<StreamingDetailsDTO> result = streamingDetailsService.findAllStreamingDetails();

		assertEquals(1, result.size());
		assertEquals("123", result.get(0).getStreamingDetailsId());
		assertEquals(Constants.VIDEO_STREAM_TYPE, result.get(0).getStreamType());
		assertEquals(ChannelType.HD.name(), result.get(0).getChannelType());
		assertEquals(VideoType.MPEG2.name(), result.get(0).getVideoType());
		assertEquals(AudioType.MP3.name(), result.get(0).getAudioType());
	}

	/*
	 * Test case to verify that null is returned when no streaming details are
	 * found.
	 */

	@Test
	public void shouldReturnNullWhenNoStreamingDetailsAreFound() {
		when(streamingDetailsRepository.findAll()).thenReturn(Collections.emptyList());

		List<StreamingDetailsDTO> result = streamingDetailsService.findAllStreamingDetails();

		assertNull(result);
	}

	/**
	 * Test case to verify that the streaming details are updated successfully.
	 */
	@Test
	public void shouldUpdateStreamingDetailsSuccessfully() {
		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamingDetailsId(1);
		streamingDetailsUpdateDTO.setStreamId("123");
		streamingDetailsUpdateDTO.setChannelType(ChannelType.HD.name());
		streamingDetailsUpdateDTO.setVideoType(VideoType.MPEG2.name());
		streamingDetailsUpdateDTO.setAudioType(AudioType.MP3.name());
		streamingDetailsUpdateDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);

		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setStreamId("123");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		streamingDetails.setChannelType(ChannelType.SD);
		streamingDetails.setVideoType(VideoType.MPEG4);
		streamingDetails.setAudioType(AudioType.MP3);

		when(streamingDetailsRepository.findById(anyInt())).thenReturn(Optional.of(streamingDetails));
		when(streamingDetailsRepository.save(any(StreamingDetails.class))).thenReturn(streamingDetails);

		StreamingDetailsUpdateDTO result = streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateDTO);

		assertEquals("123", result.getStreamId());
		assertEquals(ChannelType.HD.name(), result.getChannelType());
		assertEquals(VideoType.MPEG2.name(), result.getVideoType());
		assertEquals(AudioType.MP3.name(), result.getAudioType());
	}

	/**
	 * Test case to verify that a ResourceNotFoundException is thrown when updating
	 * streaming details with a non-existing ID.
	 */
	@Test
	public void shouldThrowResourceNotFoundExceptionWhenUpdatingStreamingDetailsWithNonExistingId() {
		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamingDetailsId(1);
		streamingDetailsUpdateDTO.setStreamId("S123");
		streamingDetailsUpdateDTO.setChannelType(ChannelType.HD.name());
		streamingDetailsUpdateDTO.setVideoType(VideoType.MPEG2.name());
		streamingDetailsUpdateDTO.setAudioType(AudioType.MP3.name());
		streamingDetailsUpdateDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);

		when(streamingDetailsRepository.findById(anyInt())).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> {
			streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateDTO);
		});
	}

	/**
	 * Test case to verify that the streaming details can be deleted successfully.
	 */
	@Test
	public void shouldDeleteStreamingDetailsSuccessfully() {
		Integer streamId = 1;

		when(streamingDetailsRepository.existsById(anyInt())).thenReturn(true);

		assertDoesNotThrow(() -> {
			streamingDetailsService.deleteStreamingDetails(streamId);
		});

		verify(streamingDetailsRepository, times(1)).deleteById(streamId);
	}

	/**
	 * Test case to verify that a ResourceNotFoundException is thrown when deleting
	 * non-existing streaming details.
	 */
	@Test
	public void shouldThrowResourceNotFoundExceptionWhenDeletingNonExistingStreamingDetails() {
		Integer streamId = 1;

		when(streamingDetailsRepository.existsById(anyInt())).thenReturn(false);

		assertThrows(ResourceNotFoundException.class, () -> {
			streamingDetailsService.deleteStreamingDetails(streamId);
		});
	}

	/**
	 * Test case to verify that a DeleteFailedException is thrown when deleting
	 * streaming details fails.
	 */
	@Test
	public void shouldThrowDeleteFailedExceptionWhenDeletingStreamingDetailsFails() {
		Integer streamId = 1;

		when(streamingDetailsRepository.existsById(anyInt())).thenReturn(true);
		doThrow(DataIntegrityViolationException.class).when(streamingDetailsRepository).deleteById(streamId);

		assertThrows(DeleteFailedException.class, () -> {
			streamingDetailsService.deleteStreamingDetails(streamId);
		});
	}

	/**
	 * Test case to verify that the streaming details are found by ID.
	 */
	@Test
	public void shouldGetStreamingDetailsById() {
		Integer streamId = 1;

		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setId(streamId);
		streamingDetails.setStreamId("123");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		streamingDetails.setChannelType(ChannelType.HD);
		streamingDetails.setVideoType(VideoType.MPEG2);
		streamingDetails.setAudioType(AudioType.MP3);

		when(streamingDetailsRepository.findById(anyInt())).thenReturn(Optional.of(streamingDetails));

		StreamingDetailsDTO result = streamingDetailsService.findById(streamId);

		assertEquals("123", result.getStreamingDetailsId());
		assertEquals(Constants.VIDEO_STREAM_TYPE, result.getStreamType());
		assertEquals(ChannelType.HD.name(), result.getChannelType());
		assertEquals(VideoType.MPEG2.name(), result.getVideoType());
		assertEquals(AudioType.MP3.name(), result.getAudioType());
	}

	/**
	 * Test case to verify that a ResourceNotFoundException is thrown when getting
	 * non-existing streaming details by ID.
	 */
	@Test
	public void shouldThrowResourceNotFoundExceptionWhenGettingNonExistingStreamingDetailsById() {
		Integer streamId = 1;

		when(streamingDetailsRepository.findById(anyInt())).thenReturn(Optional.empty());

		assertThrows(ResourceNotFoundException.class, () -> {
			streamingDetailsService.findById(streamId);
		});
	}

	/**
	 * Test case to verify that the streaming details are found by stream ID.
	 */
	@Test
	public void shouldGetStreamingDetailsIdsByStreamType() {
		List<StreamingDetails> streamingDetailsIds = Arrays.asList(
				createStreamingDetails("123", Constants.VIDEO_STREAM_TYPE),
				createStreamingDetails("456", Constants.VIDEO_STREAM_TYPE)

		);

		when(streamingDetailsRepository.findByStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE)))
				.thenReturn(streamingDetailsIds);
		List<String> result = streamingDetailsService.getStreamingDetailsIdsByStreamType();
		System.out.println("Result" + result);

		assertEquals(2, result.size());
		assertTrue(result.contains("123"));
		assertTrue(result.contains("456"));
		assertFalse(result.contains("789"));
	}

	/**
	 * Test case to verify that null is returned when no streaming details IDs are
	 * found by stream type.
	 */
	@Test
	public void shouldReturnNullWhenNoStreamingDetailsIdsAreFoundByStreamType() {
		when(streamingDetailsRepository.findByStreamType(any())).thenReturn(Collections.emptyList());

		List<String> result = streamingDetailsService.getStreamingDetailsIdsByStreamType();

		assertNull(result);
	}

	/**
	 * Test case to verify that the radio streaming details IDs are found.
	 */
	@Test
	public void shouldGetRadioStreamingDetailsId() {
		List<StreamingDetails> radioStreamingDetailsIds = Arrays.asList(
				createStreamingDetails("123", Constants.RADIO_STREAM_TYPE),
				createStreamingDetails("456", Constants.RADIO_STREAM_TYPE));

		when(streamingDetailsRepository.findByStreamType(StreamType.getStreamType(Constants.RADIO_STREAM_TYPE)))
				.thenReturn(radioStreamingDetailsIds);

		List<String> result = streamingDetailsService.getRadioStreamingDetailsId();

		assertEquals(2, result.size());
		assertTrue(result.contains("123"));
		assertTrue(result.contains("456"));
	}

	/**
	 * Test case to verify that null is returned when no radio streaming details IDs
	 * are found.
	 */
	@Test
	public void shouldReturnNullWhenNoRadioStreamingDetailsIdsAreFound() {
		when(streamingDetailsRepository.findByStreamType(any())).thenReturn(Collections.emptyList());

		List<String> result = streamingDetailsService.getRadioStreamingDetailsId();

		assertNull(result);
	}

	/**
	 * Test case to throw UserInputException When Updating StreamingDetails must not
	 * start With R.
	 */
	@Test
	public void shouldThrowUserInputExceptionWhenUpdatingStreamingDetailsMustNotStartWithR() {

		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setId(100);
		streamingDetails.setStreamId("123");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		streamingDetails.setChannelType(null);
		streamingDetails.setVideoType(null);
		streamingDetails.setAudioType(null);
		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamingDetailsId(100);
		streamingDetailsUpdateDTO.setStreamId("R123");
		streamingDetailsUpdateDTO.setChannelType(ChannelType.HD.name());
		streamingDetailsUpdateDTO.setVideoType(VideoType.MPEG2.name());
		streamingDetailsUpdateDTO.setAudioType(AudioType.MP3.name());
		streamingDetailsUpdateDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);
		when(streamingDetailsRepository.findById(100)).thenReturn(Optional.of(streamingDetails));
		assertThrows(UserInputException.class, () -> {
			streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateDTO);
		});
	}

	/**
	 * Test case to throw UserInputException When Updating Radio StreamingDetails
	 * must start With R.
	 */
	@Test
	public void shouldThrowUserInputExceptionWhenUpdatingRadioStreamingDetailsMustStartWithR() {

		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setId(100);
		streamingDetails.setStreamId("R123");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.RADIO_STREAM_TYPE));
		streamingDetails.setChannelType(null);
		streamingDetails.setVideoType(null);
		streamingDetails.setAudioType(null);
		Integer Id = streamingDetails.getId();
		System.out.println("id" + Id);
		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamingDetailsId(Id);
		streamingDetailsUpdateDTO.setStreamId("123");
		streamingDetailsUpdateDTO.setStreamType(Constants.RADIO_STREAM_TYPE);
		when(streamingDetailsRepository.findById(100)).thenReturn(Optional.of(streamingDetails));
		assertThrows(UserInputException.class, () -> {
			streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateDTO);
		});
	}

	/**
	 * Test case to verify that the updateStreamingDetails method throws a
	 * ResourceNotFoundException when updating streaming details with a non-existing
	 * video type.
	 * 
	 * This test ensures that the updateStreamingDetails method of the
	 * StreamingDetailsService throws a ResourceNotFoundException when the Video
	 * type of the streaming details to be updated does not exist. It creates a new
	 * StreamingDetails object and sets its properties. Then, it creates a
	 * StreamingDetailsUpdateDTO object and sets its properties. It mocks the
	 * behavior of the streamingDetailsRepository.findById method to return the
	 * optional of the created streamingDetails object. Finally, it asserts that a
	 * ResourceNotFoundException is thrown when the updateStreamingDetails method is
	 * called with the streamingDetailsUpdateDTO.
	 */
	@Test
	public void shouldThrowResourceNotFoundExceptionWhenUpdatingStreamingDetailsWithNonExistingVideoType() {
		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setId(100);
		streamingDetails.setStreamId("1235");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		streamingDetails.setChannelType(ChannelType.SD);
		streamingDetails.setVideoType(VideoType.MPEG4);
		streamingDetails.setAudioType(AudioType.MP3);
		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamingDetailsId(100);
		streamingDetailsUpdateDTO.setStreamId("123");
		streamingDetailsUpdateDTO.setChannelType("HD");
		streamingDetailsUpdateDTO.setVideoType("mpeg2");
		streamingDetailsUpdateDTO.setAudioType("MP3");
		streamingDetailsUpdateDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);

		when(streamingDetailsRepository.findById(anyInt())).thenReturn(Optional.of(streamingDetails));

		assertThrows(ResourceNotFoundException.class, () -> {
			streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateDTO);
		});
	}

	/**
	 * Test case to verify that the updateStreamingDetails method throws a
	 * ResourceNotFoundException when updating streaming details with a non-existing
	 * Audio type.
	 * 
	 * This test ensures that the updateStreamingDetails method of the
	 * StreamingDetailsService throws a ResourceNotFoundException when the Audio
	 * type of the streaming details to be updated does not exist. It creates a new
	 * StreamingDetails object and sets its properties. Then, it creates a
	 * StreamingDetailsUpdateDTO object and sets its properties. It mocks the
	 * behavior of the streamingDetailsRepository.findById method to return the
	 * optional of the created streamingDetails object. Finally, it asserts that a
	 * ResourceNotFoundException is thrown when the updateStreamingDetails method is
	 * called with the streamingDetailsUpdateDTO.
	 */
	@Test
	public void shouldThrowResourceNotFoundExceptionWhenUpdatingStreamingDetailsWithNonExistingAudioType() {
		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setId(100);
		streamingDetails.setStreamId("1235");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		streamingDetails.setChannelType(ChannelType.SD);
		streamingDetails.setVideoType(VideoType.MPEG4);
		streamingDetails.setAudioType(AudioType.MP3);
		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamingDetailsId(100);
		streamingDetailsUpdateDTO.setStreamId("123");
		streamingDetailsUpdateDTO.setChannelType("HD");
		streamingDetailsUpdateDTO.setVideoType("MPEG2");
		streamingDetailsUpdateDTO.setAudioType("mp3");
		streamingDetailsUpdateDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);

		when(streamingDetailsRepository.findById(anyInt())).thenReturn(Optional.of(streamingDetails));

		assertThrows(ResourceNotFoundException.class, () -> {
			streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateDTO);
		});
	}

	/**
	 * Test case to verify that the updateStreamingDetails method throws a
	 * ResourceNotFoundException when updating streaming details with a non-existing
	 * channel type.
	 * 
	 * This test ensures that the updateStreamingDetails method of the
	 * StreamingDetailsService throws a ResourceNotFoundException when the channel
	 * type of the streaming details to be updated does not exist. It creates a new
	 * StreamingDetails object and sets its properties. Then, it creates a
	 * StreamingDetailsUpdateDTO object and sets its properties. It mocks the
	 * behavior of the streamingDetailsRepository.findById method to return the
	 * optional of the created streamingDetails object. Finally, it asserts that a
	 * ResourceNotFoundException is thrown when the updateStreamingDetails method is
	 * called with the streamingDetailsUpdateDTO.
	 */
	@Test
	public void shouldThrowResourceNotFoundExceptionWhenUpdatingStreamingDetailsWithNonExistingChannelType() {

		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setId(100);
		streamingDetails.setStreamId("1235");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		streamingDetails.setChannelType(ChannelType.SD);
		streamingDetails.setVideoType(VideoType.MPEG4);
		streamingDetails.setAudioType(AudioType.MP3);
		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamingDetailsId(100);
		streamingDetailsUpdateDTO.setStreamId("123");
		streamingDetailsUpdateDTO.setChannelType("sd");
		streamingDetailsUpdateDTO.setVideoType("MPEG2");
		streamingDetailsUpdateDTO.setAudioType("MP3");
		streamingDetailsUpdateDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);

		when(streamingDetailsRepository.findById(anyInt())).thenReturn(Optional.of(streamingDetails));
		assertThrows(ResourceNotFoundException.class, () -> {
			streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateDTO);
		});
	}

	/**
	 * Test case to verify that the updateStreamingDetails method throws a
	 * ResourceAlreadyExistsException when updating streaming details with an
	 * existing stream ID.
	 * 
	 * This test ensures that the updateStreamingDetails method of the
	 * StreamingDetailsService throws a ResourceAlreadyExistsException when the
	 * stream ID of the streaming details to be updated already exists. It creates a
	 * new StreamingDetails object and sets its properties. Then, it creates a
	 * StreamingDetailsUpdateDTO object and sets its properties. It mocks the
	 * behavior of the streamingDetailsRepository.existsByStreamId method to return
	 * true. It mocks the behavior of the streamingDetailsRepository.findById method
	 * to return the optional of the created streamingDetails object. Finally, it
	 * asserts that a ResourceAlreadyExistsException is thrown when the
	 * updateStreamingDetails method is called with the streamingDetailsUpdateDTO.
	 */
	@Test
	public void shouldThrowResourceAlreadyExistsExceptionWhenUpdatingStreamingDetailsWithExistingStreamId() {

		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setId(100);
		streamingDetails.setStreamId("1235");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		streamingDetails.setChannelType(ChannelType.SD);
		streamingDetails.setVideoType(VideoType.MPEG4);
		streamingDetails.setAudioType(AudioType.MP3);

		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamingDetailsId(100);
		streamingDetailsUpdateDTO.setStreamId("123");
		streamingDetailsUpdateDTO.setChannelType(ChannelType.HD.name());
		streamingDetailsUpdateDTO.setVideoType(VideoType.MPEG2.name());
		streamingDetailsUpdateDTO.setAudioType(AudioType.MP3.name());
		streamingDetailsUpdateDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);

		when(streamingDetailsRepository.existsByStreamId(anyString())).thenReturn(true);
		when(streamingDetailsRepository.findById(100)).thenReturn(Optional.of(streamingDetails));
		assertThrows(ResourceAlreadyExistsException.class, () -> {
			streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateDTO);
		});
	}

	/*
	 * Method to create streaming details
	 */
	private StreamingDetails createStreamingDetails(String streamId, String streamType) {
		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setStreamId(streamId);
		streamingDetails.setStreamType(StreamType.getStreamType(streamType));
		streamingDetails.setChannelType(ChannelType.HD);
		streamingDetails.setVideoType(VideoType.MPEG2);
		streamingDetails.setAudioType(AudioType.MP3);
		System.out.println("StreamDetails" + streamingDetails.toString());
		return streamingDetails;
	}

	/**
	 * Test case to verify that the updateStreamingDetails method throws a
	 * RuntimeException when an exception occurs while saving the updated streaming
	 * details.
	 * 
	 * It creates a new StreamingDetails object and sets its properties. Then, it
	 * creates a StreamingDetailsUpdateDTO object and sets its properties. It mocks
	 * the behavior of the streamingDetailsRepository.findById method to return the
	 * optional of the created streamingDetails object. It mocks the behavior of the
	 * streamingDetailsRepository.save method to throw a RuntimeException. Finally,
	 * it asserts that a RuntimeException is thrown when the updateStreamingDetails
	 * method is called with the streamingDetailsUpdateDTO.
	 */
	@Test
	public void shouldReturnFalseWhileUpdateSavingThrowsException() {

		StreamingDetails streamingDetails = new StreamingDetails();
		streamingDetails.setId(100);
		streamingDetails.setStreamId("1235");
		streamingDetails.setStreamType(StreamType.getStreamType(Constants.VIDEO_STREAM_TYPE));
		streamingDetails.setChannelType(ChannelType.SD);
		streamingDetails.setVideoType(VideoType.MPEG4);
		streamingDetails.setAudioType(AudioType.MP3);
		StreamingDetailsUpdateDTO streamingDetailsUpdateDTO = new StreamingDetailsUpdateDTO();
		streamingDetailsUpdateDTO.setStreamingDetailsId(100);
		streamingDetailsUpdateDTO.setStreamId("123");
		streamingDetailsUpdateDTO.setStreamType(Constants.VIDEO_STREAM_TYPE);

		when(streamingDetailsRepository.findById(anyInt())).thenReturn(Optional.of(streamingDetails));
		when(streamingDetailsRepository.save(any(StreamingDetails.class))).thenThrow(new RuntimeException());

		assertThrows(RuntimeException.class, () -> {
			streamingDetailsService.updateStreamingDetails(streamingDetailsUpdateDTO);
		});

	}

}
