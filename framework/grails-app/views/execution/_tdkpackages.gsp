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
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery.jqplot.min.css')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'shCoreDefault.min.css')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'shThemejqPlot.min.css')}" />

<head>
<g:javascript library="select2" />
<g:javascript library="chartview" />
<meta name="layout" content="main">
<script>

    var selectedFiles = []; // Define JavaScript variable to store selected file names
    // Function to update selectedFiles array when checkbox state changes
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



function handleInstallButtonClick() {
    // Disable the install button to prevent multiple clicks
    $('#installButton').prop('disabled', true);
    $('#installButton').css('cursor', 'not-allowed');
	
}

$('#installButton').click(handleInstallButtonClick);

</script>
<div id="popup-container">

  <form method="POST" controller="execution" action="captureSelectedFiles" method="POST">
    <input type="hidden" id="additionalParam1" name="deviceeeId" value="${deviceeeId}" />
        <div class="file-list">
				<table>
				<thead>
				<tr>
					<th style="padding: 10px; text-align: left; font-size: 16px;">Select the TDK package for installation</th>
				</tr>
				</thead>
				<tbody style="margin-bottom: 16px;">
                    <g:each in="${allFilesList}" var="file" style="margin-bottom: 16px;">
                        <tr class="file-item">
                            <td>
                                <label>
                                    <g:checkBox name="selectedFiles" value="${file}" checked="false" style="margin-top: 16px;"/><span style="font-weight: bold;margin-top: 16px;font-size: 1.2em;">${file}</span>
                                </label>
                            </td>
                        </tr>
                    </g:each>
                </tbody>
		</table>
		</div>
		    <g:hiddenField name="deviceeeId" value="${deviceeeId}"/>
			
        <div class="button-row">
			 <button type="button" id="installButton" style="padding: 10px 10px; cursor: pointer; background-color: #007bff; color: #fff; border: none; border-radius: 5px;display: block;margin-bottom: 16px;" onclick="submitForm(event)">Install</button>
				
        </div>
   
		<div id="popup" style="display: none;font-size: 1.2em;">
			              Please wait.....<img id="s" src="${resource(dir:'images',file:'spinner.gif')}" />
			    
				</div>
				<div id="copyFiles" style="display: none; font-size: 1.2em;">copying files is in progress..</div>
				<div id="FetchLoges" style="display: none; font-size: 1.2em;">copied files successfully.</div>
				
				 <div id="progressContainer" style="display: none;width: 100%;background-color: #f3f3f3;margin-bottom: 16px;">
        <div id="progressBar" style="width: 1%;height: 15px;background-color: #4caf50;" style="display: none;margin-bottom: 16px;" ></div>
    </div>

				<div id="LogsFetched" style="display: none; font-size: 1.2em;">TDK Installation logs are below...</div>
				<div id="outputDiv" class="shell-script-container" >${outputOfShellScript}</div>
				
    </form>
	
</div>
<div id="InstalltionCompleted" style="display: none;margin-bottom: 16px;color:#4CAF50;font-weight: bold; font-size: 1.2em;">TDK installation has been completed successfully</div>