<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2019 RDK Management

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
<%@ page import="java.io.*"%>
<%@page import="java.text.DecimalFormat"%>
<%@ page import="com.comcast.rdk.Execution"%>
<!DOCTYPE html>
<html>
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery.jqplot.min.css')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'shCoreDefault.min.css')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'shThemejqPlot.min.css')}" />

<head>
<g:javascript library="select2" />
<g:javascript library="chartview" />
<meta name="layout" content="main"/>
<script>

    var selectedFiles = []; // Define JavaScript variable to store selected file names
    // Function to update selectedFiles array when checkbox state changes
    document.querySelectorAll('.checkbox-custom').forEach(el => {
    el.style.width = '80%'; // Remove this or modify it
});
    
	document.querySelectorAll('input[name="selectedFiles"]').forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        if (this.checked) {
            // If this checkbox is checked, uncheck all other checkboxes
            document.querySelectorAll('input[name="selectedFiles"]').forEach(function(otherCheckbox) {
                if (otherCheckbox !== checkbox) {
                    otherCheckbox.checked = false;
                    otherCheckbox.disabled = true;
                }
            });
            // Add the value of this checkbox to the selectedFiles array
            selectedFiles.push(this.value);
        } else {
            // Remove the value of this checkbox from the selectedFiles array
            selectedFiles = selectedFiles.filter(function(file) {
                return file !== this.value;
            }.bind(this));
            // Re-enable all checkboxes
            document.querySelectorAll('input[name="selectedFiles"]').forEach(function(otherCheckbox) {
                otherCheckbox.disabled = false;
            });
        }
        
    });
});

	
	var selectedVtsFiles = []; // Store selected VTS files

	document.querySelectorAll('input[name="selectedVtsFiles"]').forEach(function(checkbox) {
	    checkbox.addEventListener('change', function() {
	        if (this.checked) {
	            // Uncheck all other checkboxes
	            document.querySelectorAll('input[name="selectedVtsFiles"]').forEach(function(otherCheckbox) {
	                if (otherCheckbox !== checkbox) {
	                    otherCheckbox.checked = false;
	                    otherCheckbox.disabled = true;
	                }
	            });
	            // Add the value of this checkbox to the selectedVtsFiles array
	            selectedVtsFiles.push(this.value);
	        } else {
	            // Remove from the selectedVtsFiles array
	            selectedVtsFiles = selectedVtsFiles.filter(file => file !== this.value);
	            // Re-enable all checkboxes
	            document.querySelectorAll('input[name="selectedVtsFiles"]').forEach(function(otherCheckbox) {
	                otherCheckbox.disabled = false;
	            });
	        }
	    });
	});
		


function handleInstallButtonClick() {
    // Disable the install button to prevent multiple clicks
    $('#installButton').prop('disabled', true);
    $('#installButton').css('cursor', 'not-allowed');
	
}

$('#installButton').click(handleInstallButtonClick);

</script>

<head>
    <title>Package Manager</title>
    <meta name="layout" content="main"/>
    <link rel="stylesheet" href="${resource(dir:'css',file:'jquery.jqplot.min.css')}" />
    <script>
   

    </script>
    <style>
        body { font-family: Arial, sans-serif; }
        .tab-buttons { display: flex; justify-content: center; margin-bottom: 10px; }
        .tab-buttons button { padding: 8px 12px; margin: 0 5px; font-size: 14px; cursor: pointer; border: none; background-color: #ddd; }
        .tab-buttons button.active { background-color: #46A7E1; color: white; }
        .container { width: 700px; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); background-color: #ffffff; text-align: center; }
        button { padding: 6px 8px; font-size: 12px; cursor: pointer; border-radius: 3px; }
         .popup-container {
            width: 500px;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #ffffff;
            text-align: center;
        }
        h2 {
            color: #333;
        }
        .tab-buttons {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .tab-buttons button {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            background-color: #f9f9f9;
            transition: background-color 0.3s;
            margin: 0 5px;
        }
        .tab-buttons .active {
            background-color: #46A7E1;
            color: white;
        }
        .file-list {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            text-align: left;
        }
        .vts-file-list {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            text-align: left;
        }
         .button-container {
          
            margin-bottom: 20px;
        }
        button {
            padding: 10px 15px;
            border: none;
            border-radius: 6px;
            font-size: 12px !important;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        #installButton { background-color: #007bff; color: white;
    }
          #createPackageButton { background-color: #28A745; color: white; }
        #uploadPackageButton { background-color: #007BFF; color: white; }
        #outputContainer {
    margin-top: 10px;
    background: #f5f5f5;
}

#outputDiv {
    background: #f5f5f5;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
    font-family: monospace;
    white-space: pre-wrap;
    max-height: 300px;
    overflow-y: auto;
}

        
        .progress-bar {
            width: 100%;
            background-color: #f3f3f3;
            border-radius: 8px;
            margin-top: 10px;
            height: 10px;
            overflow: hidden;
        }
        .progress-bar div {
            height: 100%;
            width: 1%;
            background-color: #4caf50;
        }
        
.checkbox-container {
    display: flex;
    align-items: center;

}
.vts-checkbox-container{
	display: flex;
    align-items: center;
}

.checkbox-custom {
    width: auto !important;
    padding: 0 !important;
    margin: 8px !important;
}
.buttons {
 width: 40% !important;
}
button.create {
display: flex;
    align-items: center;
    padding: 12px 2px;
    font-size: 8px;
    border: 1px solid #ccc;
    background-color: #f8f8f8;
    white-space: nowrap;
    width: 140px !important;
    height: 25px;
    margin-right: 3px;

}
button.buttons {
 padding: 10px !important;
    margin: 15px;
    width: 90px !important

}    
    </style>
</head>
<body>
  <div class="popup-container">
       <h1 style="font-size: 20px; position: relative; text-align: center; margin-bottom: 10px;">
    Package Manager
</h1>

        
        <!-- Tab Navigation -->
        <div class="tab-buttons">
            <button id="tdkTabButton" class="active" onclick="switchTab('TDK')">TDK</button>
            <button id="vtsTabButton" onclick="switchTab('VTS')">VTS</button>
        </div>

        <!-- TDK Tab -->
        <div id="tdkTab">
          <form method="POST" action="createTDKPackage" enctype="multipart/form-data">
          
    <input type="hidden" id="deviceId" name="deviceId" value="${deviceId}" />
    <input type="hidden" id="deviceeeId" name="deviceeeId" value="${deviceeeId}" />
<input type="hidden" id="deviceNotFreeFlag" value="${deviceNotFree}"/>
<input type="hidden" id="noFilesFlag" value="${noFiles}"/>
<input type="hidden" id="noTdkFilesFlag" value="${noTdkFiles}"/>
<input type="hidden" id="noVtsFilesFlag" value="${noVtsFiles}"/>

    <div class="button-container" style="display: flex; align-items: center; gap: 150px; margin-left: 30px;">
    <!-- Create Package Button -->
    <button type="button" onclick="createTDKPackage()" class="create">
        <img src="../images/skin/database_add.png" alt="Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 5px;">
        Create Package
    </button>

    <!-- Always Visible Upload Button -->
    <div>
        <button type="button" onclick="document.getElementById('packageFile').click()" class="create">
            <img src="../images/reorder_up.png" alt="Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 5px;">
            Upload Package
        </button>
        <input type="file" id="packageFile" name="packageFile" style="display: none;" onchange="uploadPackage()">
    </div>
	
</div>

    <!-- Shared Output Section -->
    <div id="outputSection" style="margin-top: 20px;">
        <!-- Create Package Logs -->
        <div id="packageSuccess" style="display: none; color: #4CAF50; font-weight: bold; font-size: 1.2em;">
            Package created successfully!
        </div>
        <div id="packageError" style="display: none; color: red; font-weight: bold; font-size: 1.2em;">
            Failed to create package. Please try again.
        </div>

        <!-- Upload Progress Message -->
        <div id="uploadProgress" style="display: none; font-size: 1.2em;">
            Uploading... Please wait...
        </div>

        <!-- Upload Success Message -->
        <div id="uploadSuccess" style="display: none; color: #28A745; font-weight: bold; font-size: 1.2em;">
            Package uploaded successfully!
        </div>

        <!-- Upload Error Message -->
        <div id="uploadError" style="display: none; color: red; font-weight: bold; font-size: 1.2em;">
            Failed to upload package. Please try again.
        </div>

        <!-- Logs Output (Shared for Both Actions) -->
        <pre id="scriptOutput" style="background: #f5f5f5; padding: 10px; border-radius: 5px; border: 1px solid #ddd;
             font-family: monospace; white-space: pre-wrap; max-height: 300px; overflow-y: auto;display: none;"></pre>
    </div>
    <div style="height: 10px;"></div>
</form>

<p></p>
<p></p>

            <!-- File Selection and Install -->
            <form method="POST" action="installPackages">
    <input type="hidden" name="deviceId" value="${deviceId}" />
    <div class="file-list" id="fileListTable">
        <table>
            <thead>
                <tr><th>Select the TDK package for installation</th></tr>
            </thead>
            <tbody>

     

            <!-- Show error if no TDK files are available -->
            <g:if test="${noTdkFiles}">
                <tr>
                    <td style="text-align: center; font-weight: bold; color: red;">
                        No TDK packages available.
                    </td>
                </tr>
            </g:if>

            <!-- Show TDK package selection if files exist -->
            <g:if test="${!noTdkFiles}">
                <g:each in="${allFilesList}" var="file">
                    <tr>
                        <td>
                            <label class="checkbox-container">
                                <input type="checkbox" name="selectedFiles" value="${file}" class="checkbox-custom" />
                                &nbsp;
                                <span>${file}</span>
                            </label>
                        </td>
                    </tr>
                </g:each>
            </g:if>

            </tbody>
        </table>
    </div>

    <div class="button-row">
        <button type="button" onclick="submitForm(event)" class="buttons" style="width: 40%; padding: 8px; margin-bottom: 10px;">Install</button>
    </div>
</form>
            	 <div id="installation" style="display: none; font-size: 1.2em;"> Package is getting Installed...please wait</div>
                <div id="LogsFetched" style="font-size: 1.2em;text-align: left;display: none;"> Logs are below...</div>
<div id="outputContainer">
    <pre id="outputDiv" class="shell-script-container" style="display: none;">${outputOfShellScript}</pre>
</div>	
            
        </div>
	
        <!-- VTS Tab -->
        <div id="vtsTab" style="display:none;">
        <form method="POST" action="createVTSPackage" enctype="multipart/form-data">
            <input type="hidden" id="deviceId" name="deviceId" value="${deviceId}" />

    <div class="button-container" style="display: flex; align-items: center; gap: 150px; margin-left: 30px;">
        <!-- Create Package Button (Left) -->
        <button type="button" onclick="createVTSPackage()" class="create" >
         <img src="../images/skin/database_add.png" alt="Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 5px;">
    Create Package
</button>
           

        <!-- Upload Package Button (Right) -->
        <button type="button" onclick="document.getElementById('vtspackageFile').click()" class="create" >
                 <img src="../images/reorder_up.png" alt="Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 5px;">
        
            Upload Package
        </button>
        <input type="file" id="vtspackageFile" name="vtspackageFile" style="display: none;" onchange="uploadVTSPackage()">
    </div>

    <!-- Shared Output Section -->
    <div id="outputVTSSection" style="margin-top: 20px;">
        <!-- Create Package Logs -->
        <div id="vtspackageSuccess" style="display: none; color: #4CAF50; font-weight: bold; font-size: 1.2em;">
            Package created successfully!
        </div>
        <div id="vtspackageError" style="display: none; color: red; font-weight: bold; font-size: 1.2em;">
            Failed to create package. Please try again.
        </div>

        <!-- Upload Progress Message -->
        <div id="vtsuploadProgress" style="display: none; font-size: 1.2em;">
            Uploading... Please wait...
        </div>

        <div id="vtsuploadSuccess" style="display: none; color: #28A745; font-weight: bold; font-size: 1.2em;">
            Package uploaded successfully!
        </div>

        <!-- Upload Error Message -->
        <div id="vtsuploadError" style="display: none; color: red; font-weight: bold; font-size: 1.2em;">
            Failed to upload package. Please try again.
        </div>

        <!-- Logs Output (Shared for Both Actions) -->
        <pre id="vtsscriptOutput" style="background: #f5f5f5; padding: 10px; border-radius: 5px; border: 1px solid #ddd;
             font-family: monospace; white-space: pre-wrap; max-height: 300px; overflow-y: auto;display: none;"></pre>
    </div>
    <div style="height: 10px;"></div>
</form>

<!-- VTS File List -->
   <form method="POST" action="installPackages">
    <div class="vts-file-list" id="vtsFileListTable">
        <table>
            <thead>
                <tr><th>Select the VTS package for installation</th></tr>
            </thead>
            <tbody>

            <!-- Show error if no VTS files are available -->
            <g:if test="${noVtsFiles}">
                <tr>
                    <td style="text-align: center; font-weight: bold; color: red;">
                        No VTS packages available.
                    </td>
                </tr>
            </g:if>

            <!-- Show VTS package selection if files exist -->
            <g:if test="${!noVtsFiles}">
                <g:each in="${allVtsFilesList}" var="file">
    <tr>
        <td>
            <label class="vts-checkbox-container">
                <input type="checkbox" name="selectedVtsFiles" value="${file}" class="checkbox-custom" />
                &nbsp; <!-- This adds a space -->
                <span>${file}</span>
            </label>
        </td>
    </tr>
</g:each>

            </g:if>

            </tbody>
        </table>
    </div>

    <div class="button-row">
        <button type="button" onclick="submitVtsForm(event)" class="buttons" style="width: 40%; padding: 8px; margin-bottom: 10px;">Install</button>
    </div>
</form>
<div id="vtsinstallation" style="display: none; font-size: 1.2em;"> Package is getting Installed...please wait</div>
                <div id="vtsLogsFetched" style="font-size: 1.2em;text-align: left;display: none;"> Logs are below...</div>
<div id="vtsoutputContainer">
    <pre id="vtsoutputDiv" class="vtsshell-script-container" style="display: none;">${outputOfShellScript}</pre>
</div>	
</div>

</div>
</body>



