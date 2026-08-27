var defaultSampleRate = 44100.0;
var lengthInSeconds = 1;

var context = 0;
var bufferLoader = 0;

function runDecodingTest(url, optionalSampleRate) {
  var sampleRate = (typeof optionalSampleRate === "undefined") ? defaultSampleRate : optionalSampleRate;
  context = new OfflineAudioContext(1, sampleRate * lengthInSeconds, sampleRate);
  bufferLoader = new BufferLoader(context, [url], finishedLoading);
  bufferLoader.load();
}

function finishedLoading(bufferList) {
  console.log("Audio decoding finished. Buffer list:", bufferList);

  // Extract codec information
  var codecInfo = extractCodecInformation(bufferList[0]);
  
  // Display codec information in HTML
  var codecInfoElement = document.getElementById("codecInfo");
  codecInfoElement.innerHTML = "Audio Codec Information: " + codecInfo;
}

function extractCodecInformation(audioBuffer) {
  var codecInfo = "";
  
  // Access the audioBuffer properties for codec information
  codecInfo += "Sample Rate: " + audioBuffer.sampleRate + " Hz, ";
  codecInfo += "Channels: " + audioBuffer.numberOfChannels + ", ";
  codecInfo += "Duration: " + audioBuffer.duration + " seconds";
  
  return codecInfo;
}
