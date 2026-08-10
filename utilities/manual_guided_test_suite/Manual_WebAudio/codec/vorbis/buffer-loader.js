/*
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2026 RDK Management

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
         You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
         WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
         See the License for the specific language governing permissions and
 limitations under the License.
*/

/*
 Uses code from webkit, which is:
 Copyright WebKit Authors
 Licensed under the BSD-2 License
*/

function BufferLoader(context, urlList, callback) {
  this.context = context;
  this.urlList = urlList;
  this.onload = callback;
  this.bufferList = new Array();
  this.loadCount = 0;
}

BufferLoader.prototype.loadBuffer =
    function(url, index) {
  // Load buffer asynchronously
  let request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.responseType = 'arraybuffer';

  let loader = this;

  request.onload =
      function() {
    loader.context.decodeAudioData(
        request.response,
        function(decodedAudio) {
          try {
            loader.bufferList[index] = decodedAudio;
            if (++loader.loadCount == loader.urlList.length)
              loader.onload(loader.bufferList);
          } catch (e) {
            console.log(e);
            alert(
                'BufferLoader: unable to load buffer ' + index +
                ', url: ' + loader.urlList[index]);
          }
        },
        function() {
          alert('error decoding file data: ' + url);
        });
  }

      request.onerror =
          function() {
    alert('BufferLoader: XHR error');
  }

          request.send();
}

    BufferLoader.prototype.load = function() {
  for (let i = 0; i < this.urlList.length; ++i)
    this.loadBuffer(this.urlList[i], i);
}
