##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################
import json

# Test Scenario : To vaidate getJRPCTokenData
# Purpose       : Sample Token to be set as test string
tokenData = {}
tokenData[token] = "tdk-1234-test-45678-token-90ABCDEFGHIJ"
tokenTestString = json.dumps(tokenData)[:-1] + ',"success":true}'

# Test Scenario : To validate getMetaDataFile API
# Purpose       : Create sample packages in test_dir directory and getMetaDataFile API should be able to retrieve the same
test_dir = "/opt/test_dir/"
test_packages = [ "TDK_1_package.json" , "TDK_2_package.json" ]

# Test Scenario : To validate makeHttpHttps API
# Purpose       : Test Strings which has "http" or "https" to be passed to makeHttpHttps API
testStrings= [ "http://tdk_testing.com", "https://tdk_testing_https.com", "http://tdk_testing_http.com", "https://tdk_testing_http.com", "https://tdk_testing_https.com" ]

# Test Scenario : To validate mergeLists API
# Purpose       : Sample lists to validate mergeLists
list1 = " /opt/test_dir/TDK_01_package.json /opt/test_dir/TDK_002_package.json"
list2 = " /opt/test_dir/TDK_003_package.json /opt/test_dir/TDK_00004_package.json "

# Test Scenario : To validate mergeLists API with duplicate elements
# Purpose       : Sample lists with one duplicate element - "ca-store-update-bundle_package.json"
List1 = " ca-store-update-bundle_package.json ca-store-update-bundle_2.0_package.json "
List2 = " ca-store-update-bundle_package.json lxyupdate-bundle_package.json"


# Test Scenario : To validate stripinvalidchar APIstripinvalidchar API
# Purpose       : Test String with control characters and a test string with space in between
testStringsInvalidChar= [ "A\n", "B\t" , "C\b" , "D\r" , "E\a", "F\f", "G\0", "A B"]
