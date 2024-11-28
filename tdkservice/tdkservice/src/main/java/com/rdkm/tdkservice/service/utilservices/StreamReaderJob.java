/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
package com.rdkm.tdkservice.service.utilservices;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.concurrent.Callable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.rdkm.tdkservice.util.Constants;

/**
 * This class reads the data from the input stream and returns the data as a
 * string.
 */
public class StreamReaderJob implements Callable<String> {

	public static final Logger LOGGER = LoggerFactory.getLogger(StreamReaderJob.class);

	/**
	 * Holds the input stream. Can be data/error.
	 */
	InputStream inputStream = null;
	String outputFileName = null;
	String intialData = "";
	StringBuilder dataRead = new StringBuilder("");

	/**
	 * Constructor that takes the input stream.
	 * 
	 * @param inputStream The input stream of data.
	 */
	public StreamReaderJob(InputStream inputStream) {
		this.inputStream = inputStream;
	}

	/**
	 * Constructor that takes the input stream and the output file name.
	 * 
	 * @param inputStream    The input stream of data.
	 * @param outputFileName The output file name.
	 */
	public StreamReaderJob(InputStream inputStream, String outputFileName) {
		this.inputStream = inputStream;
		this.outputFileName = outputFileName;
	}

	/**
	 * Constructor that takes the input stream, the output file name and the data
	 * read.
	 * 
	 * @param inputStream    The input stream of data.
	 * @param outputFileName The output file name.
	 * @param dataRead       The data read.
	 */
	public StreamReaderJob(InputStream inputStream, String outputFileName, StringBuilder dataRead) {
		this.inputStream = inputStream;
		this.outputFileName = outputFileName;
		this.dataRead = dataRead;
	}

	/**
	 * This method will be called by the invoking thread. Reads the data from the
	 * input stream and adds the content to a String buffer. On the end of the
	 * stream, the string buffer is returned.
	 * 
	 * @return Data read from the stream.
	 */
	@Override
	public String call() throws Exception {

		InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
		BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
		try {
			String data = "";
			while ((data = bufferedReader.readLine()) != null) {
				dataRead.append(data);
				dataRead.append(Constants.NEW_LINE);

				if (outputFileName != null) {
					writeToOutputFile(outputFileName, data + Constants.NEW_LINE);
				}
			}
			// LOGGER.info("The data is " + dataRead);
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				bufferedReader.close();
				inputStreamReader.close();
				inputStream.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return dataRead.toString();
	}

	/**
	 * This method writes the data to the output file.
	 * 
	 * @param fileName The output file name.
	 * @param data     The data to be written to the file.
	 */
	public void writeToOutputFile(String fileName, String data) {
		try {

			if (data == null || fileName == null) {
				return;
			}

			Path opFilePath = Paths.get(fileName);
			Path parentDir = opFilePath.getParent();

			if (parentDir != null) {
				Files.createDirectories(parentDir);
			}

			if (!Files.exists(opFilePath)) {
				Files.createFile(opFilePath);
			}

//			if(data.contains("SCRIPTEND#!@~")){
//				data = data.replace("SCRIPTEND#!@~","");
//			}
//			
//			if(data.contains(Constants.TDK_ERROR)){
//				data = data.replace(Constants.TDK_ERROR,"");
//			}
//			
//			
//			String htmlData = "";
//			data?.eachLine { line ->
//				htmlData += (line + "<br/>" )
//			}

			for (int i = 0; i < 2; i++) {
				try {
					boolean append = true;
					BufferedWriter buffWriter = Files.newBufferedWriter(opFilePath,
							append ? StandardOpenOption.APPEND : StandardOpenOption.CREATE);
					buffWriter.write(data);
					buffWriter.flush();
					buffWriter.close();
					break;
				} catch (FileNotFoundException ex) {
					LOGGER.error("File not found exception: " + ex.getMessage());
					Thread.sleep(1000);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * This method deletes the output file.
	 * 
	 * @param fileName The output
	 */
	public void deleteOutputFile(String fileName) {
		try {
			File opFile = new File(fileName);
			if (opFile.exists()) {
				opFile.delete();
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}