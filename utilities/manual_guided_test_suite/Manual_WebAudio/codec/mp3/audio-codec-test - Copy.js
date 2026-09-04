var defaultSampleRate = 44100.0;
var lengthInSeconds = 1;

var context = 0;
var bufferLoader = 0;

// Run test by loading the file specified by |url|.  An optional sample rate can be given to
// select a context with a different sample rate.  The default value is |defaultSampleRate|.
function runDecodingTest(url, optionalSampleRate) 
{
    var sampleRate = (typeof optionalSampleRate === "undefined") ? defaultSampleRate : optionalSampleRate;

    // Create offline audio context.
    context = new OfflineAudioContext(1, sampleRate * lengthInSeconds, sampleRate);
    
    bufferLoader = new BufferLoader(
        context,
        [ url ],
        finishedLoading
    );
    
    bufferLoader.load();
}

function finishedLoading(bufferList)
{
    // Handle the finished loading, e.g., console.log or other actions if needed.
    console.log("Audio decoding finished. Buffer list:", bufferList);
}

// Additional functions or modifications can be added based on your requirements.
