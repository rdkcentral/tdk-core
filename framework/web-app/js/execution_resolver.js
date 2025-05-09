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

var flagMark = false

$(document).ready(function() {
	$.ajaxSetup ({cache: false});
	timedRefresh();	
	deviceStatusRefresh();	
	$("#browser").treeview({
		
		animated:"normal",
		persist: "cookie"
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});	
	
	$('.filedevicebusy').contextMenu('childs_menu', {
		bindings : {			
			'reset_device' : function(node) {
				if (confirm('Make sure no scripts is currently executed in the device. Do you want to reset the device?')) {
					resetDevice(node.id);
				}
			}
		}
	});
	
	
	/*$('.filedevicefree').contextMenu('childs_menu', {
		bindings : {			
			'reset_IpRule' : function(node) {
				if (confirm('Make sure no scripts is currently executed in the device. Are you want to reset the device?')) {
					resetIPRule(node.id);
				}
			}
		}
	});*/
		
	var decider_id = $("#decider").val();
	$("#execid").addClass("changecolor");	

	$("#scripts").select2();

	$(":checkbox").each(function() {
		$('.resultCheckbox').prop('checked', false);
		mark(this);
	});
	
	$('.markAll').prop('checked', false);
	
	$('#repeatId').attr('readonly', false);
	$('#individualRepeatId').attr('readonly', false);
	if(document.getElementById("scheduleBtnID") != null){
		document.getElementById("scheduleBtnID").disabled = false;
	}
		/*
jQuery 1.9+   $('#inputId').prop('readonly', true);
	 */

	/**
	 * Change the boxtype dropdown according to the category selected
	 */
	$("#categoryId").live('change', function(){
		var category_id = $(this).val();
		if(category_id != '') {
			getBoxTypes(category_id);
		}
		else {
			$("#boxTypeId").html('<select><option value="">Please Select</option></select>');
		}
	});
	
});

/**
 * Function to get the box types according to category and fill it in the boxtype dropdown 
 * @param category_id
 */
function getBoxTypes(category_id) {
	var url = $("#url").val();
	if(category_id != '') {
		$.get(url+'/boxType/getBoxTypeFromCategory', {category: category_id}, function(data) {
			var select = '<select id="boxType" name="boxType"><option value="">Please Select</option>';
			for(var index = 0; index < data.length; index ++ ) {
				select += '<option value="' + data[index].name + '">' + data[index].name + '</option>';
			}
			select += '</select>';
			$("#boxTypeId").html(''); 
			$("#boxTypeId").html(select); 
		});
	}
	else {
		$("#boxTypeId").html('');
	}
}

function stopExecution(obj){
	if (confirm('Execution will be stopped after finishing the current test case execution.\nDo you want to stop the execution ? ')) {
		$.get('stopExecution', {execid: obj}, function(data) {});
	}
	
}

function isNumberKey(evt)
{
   var charCode = (evt.which) ? evt.which : event.keyCode
   if (charCode > 31 && (charCode < 48 || charCode > 57))
      return false;

   return true;
}

function showSchedule(){
	if($("#scheduletest").prop('checked') == true){		
		$('#scheduleOptionDiv').show();
	}
	else{
		$('#scheduleOptionDiv').hide();
	}
}

function showSuite(){
	
	$('#testSuite').show();
	$('#singletest').hide();
	$('#scriptSpan').hide();
	$('#testSuiteSpan').show();
	checkRepeat();
	scheduleToggle();
}

function showSingle(){
	$('#singletest').show();
	$('#testSuite').hide();
	$('#scriptSpan').show();
	$('#testSuiteSpan').hide();
	checkRepeat();
	scheduleToggle();
}

function jsExecution(){
	var testSuite = document.getElementById("testSuiteRadioThunder");
	var singleTest = document.getElementById("singleTestRadioThunder");
	var thunderJavascriptExecuteButtons = document.getElementById("thunderJavascriptExecuteButtons");
	var thunderPythonExecuteButtons = document.getElementById("thunderPythonExecuteButtons");
	var thunderPythonLogTransferCheckBox = document.getElementById("rdkCertificationStbLogTransferId");
	thunderPythonLogTransferCheckBox.disabled = true;
	var thunderPythonDiagnosisCheckBox = document.getElementById("rdkCertificationDiagnosisId");
	thunderPythonDiagnosisCheckBox.disabled = true;
	var thunderPythonPerformanceCheckBox = document.getElementById("rdkCertificationPerformanceId");
	thunderPythonPerformanceCheckBox.disabled = true;	
	document.getElementById("rdkProfilingAlertCheckBoxId").disabled = true;
	thunderJavascriptExecuteButtons.style.display = "block";
	thunderPythonExecuteButtons.style.display = "none";
	document.getElementById("thunderExecutionType").value = "javascript";
	document.getElementById("category").value = "RDKV_THUNDER";
	if(singleTest.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').hide();
		$('#singletestThunder').show();
		$('#scriptSpan').show();
		$('#testSuiteSpan').hide();
	}else if(testSuite.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').show();
		$('#singletestThunder').hide();
		$('#scriptSpan').hide();
		$('#testSuiteSpan').show();
	}
	checkRepeat();
	scheduleToggle();
}

function pythonExecution(){
	var testSuite = document.getElementById("testSuiteRadioThunder");
	var singleTest = document.getElementById("singleTestRadioThunder");
	document.getElementById("thunderExecutionType").value = "rdkservice";
	var thunderJavascriptExecuteButtons = document.getElementById("thunderJavascriptExecuteButtons");
	var thunderPythonExecuteButtons = document.getElementById("thunderPythonExecuteButtons");
	var thunderPythonLogTransferCheckBox = document.getElementById("rdkCertificationStbLogTransferId");
	thunderPythonLogTransferCheckBox.disabled = false;
	var thunderPythonDiagnosisCheckBox = document.getElementById("rdkCertificationDiagnosisId");
	thunderPythonDiagnosisCheckBox.disabled = false;
	var thunderPythonPerformanceCheckBox = document.getElementById("rdkCertificationPerformanceId");
	thunderPythonPerformanceCheckBox.disabled = false;
	document.getElementById("rdkProfilingAlertCheckBoxId").disabled = false;
	thunderJavascriptExecuteButtons.style.display = "none";
	thunderPythonExecuteButtons.style.display = "block";
	document.getElementById("category").value = "RDKV";
	if(singleTest.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').show();
		$('#testSuiteThunder').hide();
		$('#singletestThunder').hide();
		$('#scriptSpan').show();
		$('#testSuiteSpan').hide();
	}else if(testSuite.checked){
		$('#testSuiteThunderPython').show();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').hide();
		$('#singletestThunder').hide();
		$('#scriptSpan').hide();
		$('#testSuiteSpan').show();
	}
	checkRepeat();
	scheduleToggle();
}

function showfullRepeat(){
	var fullRepeatCount = document.getElementById("repeatId");
	var individualRepeatCount = document.getElementById("individualRepeatId");
	fullRepeatCount.style.display = "inline";
	individualRepeatCount.style.display = "none";
	document.getElementById("repeatType").value = "full";
	checkRepeat();
	scheduleToggle();
}

function showindividualRepeat(){
	var fullRepeatCount = document.getElementById("repeatId");
	var individualRepeatCount = document.getElementById("individualRepeatId");
	fullRepeatCount.style.display = "none";
	individualRepeatCount.style.display = "inline";
	document.getElementById("repeatType").value = "individual";
	checkRepeat();
	scheduleToggle();
}

/**
 * Function to display thunder test suites in execution page when the user clicks on a device
 */
function showSuiteThunder(){
	var executionTypePython = document.getElementById("pythonThunderRadio");
	var executionTypeJavascript = document.getElementById("javaScriptThunderRadio");
	if(executionTypePython.checked){
		$('#testSuiteThunderPython').show();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').hide();
		$('#singletestThunder').hide();
		$('#scriptSpan').hide();
		$('#testSuiteSpan').show();
	}else if(executionTypeJavascript.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').show();
		$('#singletestThunder').hide();
		$('#scriptSpan').hide();
		$('#testSuiteSpan').show();
	}
	checkRepeat();
	scheduleToggle();
}

/**
 * Function to display thunder scripts in execution page when the user clicks on a device
 */
function showSingleThunder(){
	var executionTypePython = document.getElementById("pythonThunderRadio");
	var executionTypeJavascript = document.getElementById("javaScriptThunderRadio");
	if(executionTypePython.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').show();
		$('#singletestThunder').hide();
		$('#testSuiteThunder').hide();
		$('#scriptSpan').show();
		$('#testSuiteSpan').hide();
	}else if(executionTypeJavascript.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').hide();
		$('#singletestThunder').show();
		$('#testSuiteThunder').hide();
		$('#scriptSpan').show();
		$('#testSuiteSpan').hide();
	}
	checkRepeat();
	scheduleToggle();
}
function pageLoadOnScriptType(category, id){
	var isTestSuiteRadio = document.getElementById('testSuiteRadio').checked;
	var isSingleTestRadio = document.getElementById('singleTestRadio').checked;
	var isFullRepeatRadio = document.getElementById('fullRepeatRadio').checked;
	var isIndividualRepeatRadio = document.getElementById('individualRepeatRadio').checked;
	$.get('showDevices', {id: id, category: category}, function(data) {
		$("#responseDiv").html(data);
		//alert(data);
		if(category === 'RDKB_TCL'){
			document.getElementById('pythonRadio').checked = false;
			document.getElementById('tclRadio').checked = true;
		}
		else{
			document.getElementById('pythonRadio').checked = true;
			document.getElementById('tclRadio').checked = false;
		}
		if(isTestSuiteRadio){
			document.getElementById('testSuiteRadio').checked = true;
			document.getElementById('singleTestRadio').checked = false;
			showSuite();
		}
		if(isSingleTestRadio){
			document.getElementById('testSuiteRadio').checked = false;
			document.getElementById('singleTestRadio').checked = true;
			showSingle();
		}
		if(isFullRepeatRadio){
			document.getElementById('fullRepeatRadio').checked = true;
			document.getElementById('individualRepeatRadio').checked = false;
			showfullRepeat();
		}
		if(isIndividualRepeatRadio){
			document.getElementById('individualRepeatRadio').checked = true;
			document.getElementById('fullRepeatRadio').checked = false;
			showindividualRepeat();
		}
	});
	
	
//	alert(' isTestSuiteRadio : '+isTestSuiteRadio);
//	alert('isSingleTestRadio : '+isSingleTestRadio);
	//alert(' isPythonRadio : '+isPythonRadio);
	//alert('isTclRadio : '+isTclRadio);
	//$.get('showDevices', {id: id, category: category}, function(data) { $("#responseDiv").html(data); });
	
}

function showOnetimeSchedule(){
	$('#onetimeScheduleDiv').show();
	$('#reccuranceScheduleDiv').hide();
}

function showReccuranceSchedule(){
	$('#reccuranceScheduleDiv').show();
	$('#onetimeScheduleDiv').hide();
}

function showDaily(){
	$('#reccurDaily').show();
	$('#reccurWeekly').hide();
	$('#reccurMonthly').hide();
}

function showWeekly(){
	$('#reccurDaily').hide();
	$('#reccurWeekly').show();
	$('#reccurMonthly').hide();
}

function showMonthly(){
	$('#reccurDaily').hide();
	$('#reccurWeekly').hide();
	$('#reccurMonthly').show();
}

function showScript(id, category){
	$.get('showDevices', {id: id, category: category}, function(data) { $("#responseDiv").html(data); });
	$.get('updateDeviceStatus', {id: id,category: 'RDKV'}, function(data) {refreshDevices(data,'RDKV');});
	$.get('updateDeviceStatus', {id: id,category: 'RDKB'}, function(data) {refreshDevices(data,  'RDKB');});
	$.get('updateDeviceStatus', {id: id,category: 'RDKC'}, function(data) {refreshDevices(data,  'RDKC');});
	//$.get('updateDeviceStatus', {id: id,category: 'RDKB'}, function(data) {refreshDevices(data,  'RDKB');});
}

function refreshDevices(data, category){
	var conatiner = null
	if("RDKV" === category){
		container = document.getElementById("device_statusV");
	}
	else if("RDKB" === category){
		container = document.getElementById("device_statusB");
	}
	else if("RDKC" === category){
		container = document.getElementById("device_statusC");
	}
	//container = document.getElementById("device_statusTotal");
	container.innerHTML= data;
	
	var selectedId = $("#selectedDevice").val();
	var deviceInstanceTotal = $("#deviceInstanceTotal").val();
	highlightTreeElement('deviceExecutionList_', selectedId, deviceInstanceTotal);
}

/*function refreshDevices(data){
	var container = document.getElementById("device_status");
	container.innerHTML= data;
	
	var selectedId = $("#selectedDevice").val();
	var deviceInstanceTotal = $("#deviceInstanceTotal").val();
	highlightTreeElement('deviceExecutionList_', selectedId, deviceInstanceTotal);
}*/

function resetDevice(id){
	$.get('resetDevice', {id: id}, function(data) { document.location.reload(); });
}


function resetIPRule(id){
	$.get('resetIPRule', {id: id}, function(data) { document.location.reload(); });
}


function changeStyle(){
	$('#resultDiv').css('display','table');
}

function showExecutionLog(id){
	$.get('showLog', {id: id}, function(data) { $("#executionLogPopup").html(data); });		
	$("#executionLogPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}

function executionStatus(id){	
	$.get('executionStatus', {id: id}, function(data) { $("#executionStatusPopup").html(data); });		
	$("#executionStatusPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}

/**
 * RdkService schedule function
 * @param id
 * @param category
 * @returns {Boolean}
 */
function showSchedulerRdkService(id, category){	
	var scriptGroup = $("#scriptGrpThunderPython").val();
	var scripts = $("#scriptsThunderPython").val();
    var deviceList = $("#devices").val();
	var repeatid = $("#repeatId").val();

	 if ($('input[name=myGroupThunder]:checked').val()=='TestSuite'){     	
	    	scripts = "";
	 }
	 else{     	
	    	scriptGroup ="";
	 }

	var reRun = "";
	var benchmark = "false";
	var systemDiag = "false"
	var isLogReqd =" false"
	var isAlertChecked =" false"
    if ($("#rerunId").prop('checked')==true){     	
    	reRun = "true";
    }
	if ($("#rdkCertificationStbLogTransferId").prop('checked')==true){  
		isLogReqd = "true";
	}
	
	if ($("#rdkProfilingAlertCheckBoxId").prop('checked')==true){  
		isAlertChecked = "true";
	}
	
	if( (deviceList =="" || deviceList == null ) ){
		alert("Please select Device");
		return false;
	}
	
	if(deviceList.length > 1){	
		alert("Scheduling is not currently allowed for multiple devices");
		return false;
	}
	else{
		id = deviceList.toString();		
	}

	if((scripts=="" || scripts == null )&& scriptGroup == "" ){
		alert("Please select Script/ScriptGroup");
		return false;
	}
	var scriptVals = ""
	if(scripts){
		scriptVals = scripts.toString();
	} 
	var scriptGroupVals = ""
	if(scriptGroup){
		scriptGroupVals = scriptGroup.toString()
	}
	$.get('showSchedular', {deviceId : id, devices : deviceList.toString(), scriptGroup : scriptGroupVals, scripts:scriptVals, repeatId:repeatid, rerun:reRun, systemDiagnostics : systemDiag , benchMarking : benchmark  ,isLogReqd :isLogReqd, category:category, isAlertChecked:isAlertChecked }, function(data) { $("#scheduleJobPopup").html(data); });		
	$("#scheduleJobPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	$("#scheduletable").dataTable( {
		"sPaginationType": "full_numbers",
		 "bRetrieve": "true" 
	} );	
}

function showScheduler(id, category){	
	
	var scriptGroup = $("#scriptGrp").val();
	var scripts = $("#scripts").val();
    var deviceList = $("#devices").val();
	var repeatid = $("#repeatId").val();

	 if ($('input[name=myGroup]:checked').val()=='TestSuite'){     	
	    	scripts = "";
	 }
	 else{     	
	    	scriptGroup ="";
	 }

	var reRun = "";
	var benchmark = "false";
	var systemDiag = "false"
	var isLogReqd =" false"
    if ($("#rerunId").prop('checked')==true){     	
    	reRun = "true";
    }
	if ($("#benchmarkId").prop('checked')==true){     	
		benchmark = "true";
	}
	if ($("#systemDiagId").prop('checked')==true){     	
		systemDiag = "true";
	}
	if ($("#transferLogsId").prop('checked')==true){  
		
		isLogReqd = "true";
	}
	
	
	if( (deviceList =="" || deviceList == null ) ){
		alert("Please select Device");
		return false;
	}
	
	if(deviceList.length > 1){	
		alert("Scheduling is not currently allowed for multiple devices");
		return false;
	}
	else{
		id = deviceList.toString();		
	}

	if((scripts=="" || scripts == null )&& scriptGroup == "" ){
		alert("Please select Script/ScriptGroup");
		return false;
	}
	var scriptVals = ""
	if(scripts){
		scriptVals = scripts.toString();
	} 
	var scriptGroupVals = ""
	if(scriptGroup){
		scriptGroupVals = scriptGroup.toString()
	}
	$.get('showSchedular', {deviceId : id, devices : deviceList.toString(), scriptGroup : scriptGroupVals, scripts:scriptVals, repeatId:repeatid, rerun:reRun, systemDiagnostics : systemDiag , benchMarking : benchmark  ,isLogReqd :isLogReqd, category:category }, function(data) { $("#scheduleJobPopup").html(data); });		
	$("#scheduleJobPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	$("#scheduletable").dataTable( {
		"sPaginationType": "full_numbers",
		 "bRetrieve": "true" 
	} );	
}

function showCleanUpPopUp(){
	$("#cleanupPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 600,
	            height: 250	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}

function showDateTime(){
	$('#defexecName').val(" ");
	checkDeviceList();
	var stbName
	var deviceList = $("#devices").val();
	 if(deviceList == null){
		 stbName = ""
	 }else if(deviceList.length > 1){	
		 stbName = "multiple"
	 }else{
		 stbName = $('#stbname').val();
	 }
	
	$.get('showDateTime', {}, function(data) { 	
		$('#defexecName').val(stbName+"-"+data[0]);
		$('#newexecName').val(stbName+"-"+data[0]);
	});
	checkRepeat();
	scheduleToggle();
}

function checkDeviceList(){
	 var deviceList = $("#devices").val();
	 if(deviceList != null && deviceList.length > 1){		
		 $("#repeatId").val(1);
		// document.getElementById("repeatId").disabled = true;
		 $('#repeatId').attr('readonly', true);
			
	 }
	 else{
		 $('#repeatId').attr('readonly', false);			
		// document.getElementById("repeatId").disabled = false;
	 }
}

function checkRepeat(){
	 var IndividualRepeat = document.getElementById("individualRepeatRadio");
	 var singleSelectedTdk = document.getElementById("singleTestRadio");
	 var singleSelectedRdkService = document.getElementById("singleTestRadioThunder");
	 var thunderExecutionType = document.getElementById("thunderExecutionType").value;
	 var scriptList = $("#scripts").val();
	 var scriptListRdkService = $("#scriptsThunderPython").val();
	 var isThunderEnabled = document.getElementById("stbtype").value;
	 if((isThunderEnabled != 1 && singleSelectedTdk && singleSelectedTdk.checked && IndividualRepeat.checked && scriptList!= null && scriptList.length <=1) || (thunderExecutionType == "rdkservice" && isThunderEnabled == 1 && singleSelectedRdkService && singleSelectedRdkService.checked && IndividualRepeat.checked && scriptListRdkService != null && scriptListRdkService.length <=1)||(thunderExecutionType == "javascript" && isThunderEnabled == 1)){
		 $("#individualRepeatId").val(1);
		 $('#individualRepeatId').attr('readonly', true);
	 }else{
		 $('#individualRepeatId').attr('readonly', false);
	 }
}

function scheduleToggle(){
	 var isThunderEnabled = document.getElementById("stbtype").value;
	 var IndividualRepeat = document.getElementById("individualRepeatRadio");
	 if(isThunderEnabled != 1){
		 var suiteSelectedTdk = document.getElementById("testSuiteRadio");
		 var scriptGroupListTdk = $("#scriptGrp").val();
		 if((suiteSelectedTdk.checked && scriptGroupListTdk!= null && scriptGroupListTdk.length > 1) || (IndividualRepeat.checked)){ 
			 document.getElementById("scheduleBtnID").disabled = true;
		 }else{
			 document.getElementById("scheduleBtnID").disabled = false;
		 }
	 }else{
		 var thunderExecutionType = document.getElementById("thunderExecutionType").value;
		 if(thunderExecutionType == "rdkservice"){
			 var suiteSelectedRdkservice = document.getElementById("testSuiteRadioThunder");
			 var scriptGroupListRdkservice = $("#scriptGrpThunderPython").val();
			 if((suiteSelectedRdkservice.checked && scriptGroupListRdkservice!= null && scriptGroupListRdkservice.length > 1) || (IndividualRepeat.checked)){ 
				 document.getElementById("scheduleBtnPythonID").disabled = true;
			 }else{
				 document.getElementById("scheduleBtnPythonID").disabled = false;
			 }
		 }
	 }
}

function showEditableExecName(){
	$("#givenExcName").show();
	$("#defExcName").hide();
}

function showDefaultExecName(){
	$("#defExcName").show();
	$("#givenExcName").hide();	
	$('#newexecName').val($('#defexecName').val());
}

function displayWaitSpinner(){		
	$("#spinnr").show();
}

function hideWaitSpinner(){	
	$("#spinnr").hide();
}

function showSpinner(){		
	$("#spinner1").show();
}

function hideSpinner(){	
	$("#spinner1").hide();
}

var repeatTask;

var repeatTaskThunder;

function showWaitSpinner(){	
	$("#popup").show();
	$("#executeBtn").hide();
	$("#executeBtnPython").hide();
	var execId = $('#exId').val();
	var deviceList= $('#devices').val();
	if(deviceList  && deviceList.length > 1 )
	{
		$('#resultDiv'+execId).show();	
		$('#resultDiv'+execId).html('Multiple Device Execution ');
		//$('#dynamicResultDiv').show();
	}
	else
	{	
	$('#resultDiv'+execId).hide();
	$('#dynamicResultDiv').show();
	$('#dynamicResultDiv').html('Starting the script execution...');
	repeatTask = setInterval("updateLog()",5000);
	}
}

/**
 * Function to display the spinner gif for thunder executions
 */
function showWaitSpinnerThunder(){
	$("#popup").show();
	$("#executeBtnThunder").hide();
	
	var execId = $('#exId').val();
	var deviceList= $('#devices').val();
	if(deviceList  && deviceList.length > 1 )
	{
		$('#resultDiv'+execId).show();	
		$('#resultDiv'+execId).html('Multiple Device Execution ');
	}
	else
	{
		$('#resultDiv'+execId).hide();
		$('#dynamicResultDiv').show();
		$('#dynamicResultDiv').html('Starting the script execution...');
		repeatTaskThunder = setInterval("updateLogThunder()",1000);
	}
}

/**
 * Function to update thunder logs in UI
 */
function updateLogThunder(){
	var execName = "";
	execName = $('#defexecName').val();
	var suite = "single"
	var scriptNameArray
	var scriptname = ""
	if ($('input[name=myGroupThunder]:checked').val()=='TestSuiteThunder'){
		suite = "suite"
	}else{
		scriptNameArray = $('#scriptsThunder').val();
		if(scriptNameArray.length > 1){
			suite = "multiple"
		}else{
			scriptname = scriptNameArray[0]
		}
	}
	$.get('readOutputFileDataThunder', {executionName: execName, scriptName: scriptname, suiteName: suite}, function(data) {
		$("#dynamicResultDiv").html(data); 
	});
}

/**
 * Function to show the static result div once execution gets completed
 * @param id
 */
function completedThunder(id) {
	if (repeatTaskThunder) {
		clearInterval(repeatTaskThunder);
	}
	showDateTime();
	var execId = $('#exId').val();
	if (id == execId) {
		$('#resultDiv' + execId).show();
		$('#dynamicResultDiv').hide();
	}
}

/**
 * Function to hide wait spinner and show Execute button once execution is completed
 */
function changeStylesThunder(){
	showDateTime();
	$("#popup").hide();
	$("#executeBtnThunder").show();
}

function showSpinner(){
	$("#delspinnr").show();
}

function hideSpinnerForDelete(){
	$("#delspinnr").hide();
	 $( "#cleanFromDate" ).datepicker();
	 $( "#cleanToDate" ).datepicker();
}

function updateLog(){
	var execName = "";
	if(  $("#defexecName").is(":visible") == true )
	{  
		execName = $('#defexecName').val();
	}
	
	if (  $("#newexecName").is(":visible") == true )
	{  
		execName = $('#newexecName').val();       
	}
	$.get('readOutputFileData', {executionName: execName}, function(data) {
		$("#dynamicResultDiv").html(data); 
	});
}

function completed(id) {
	if (repeatTask) {
		clearInterval(repeatTask);
	}
	showDateTime();
	var execId = $('#exId').val();
	if (id == execId) {
		$('#resultDiv' + execId).show();
		$('#dynamicResultDiv').hide();
	}

}
function changeStyles(){
	showDateTime();
	$("#popup").hide();
	var thunderExecutionType = document.getElementById("thunderExecutionType");
	if(thunderExecutionType.value == "javascript"){
		$("#executeBtn").show();
	}else if(thunderExecutionType.value == "rdkservice"){
		$("#executeBtnPython").show();
	}
}

function baseScheduleTableRemove(){		
	$("#baseScheduleTable").hide();
	$('.hello').remove();
	alert("script/ScriptGroup unScheduled");
}
function baseScheduleTableSave()
{
	alert(" Script/ScriptGroup Scheduled");
	$("#baseScheduleTable").hide();
	$('.hello').remove();
	
}
function baseScheduleTableDelete()
{
	
	$("#baseScheduleTable").hide();
	$('.hello').remove();
	
}

/**
 * Dynamic page refresh call. First time called from the document ready of list
 * page
 */
function timedRefresh() {
	if(flagMark == true){
		$('.markAll').prop('checked', true);
	}
	setTimeout("loadXMLDoc();", 5 * 1000);	
}


/**
 * Ajax call to refresh only the list table when dynamic refresh is enabled
 */

var prevCategory = null;

function loadXMLDoc() {
	var xmlhttp;	
	var url = $("#url").val();
	var paginateOffset = $("#pageOffset").val();
	if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			document.getElementById("list-executor").innerHTML = xmlhttp.responseText;
			timedRefresh();			
		}
	} 
	if(paginateOffset != undefined){
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
		var category = document.getElementById("filter").value;
		xmlhttp.open("GET", url+"/execution/create?t=" + Math.random()+"&max=10&offset="+paginateOffset+"&devicetable=true&flagMark="+flagMark+"&category="+category, true);
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
	}
	xmlhttp.send();
}

function categoryChange() {
	
	var xmlhttp;	
	var url = $("#url").val();
	var paginateOffset = $("#pageOffset").val();
	if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			document.getElementById("list-executor").innerHTML = xmlhttp.responseText;
			timedRefresh();			
		}
	} 
	if(paginateOffset != undefined){
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
		
		var category = document.getElementById("filter").value;
		var prevCategory = document.getElementById("selectedFilter").value;
		if(prevCategory == null || prevCategory != category){
			paginateOffset = 0;
		}
		xmlhttp.open("GET", url+"/execution/create?t=" + Math.random()+"&max=10&offset="+paginateOffset+"&devicetable=true&flagMark="+flagMark+"&category="+category, true);
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
	}
	xmlhttp.send();
}

/**
 * Function used to check box enabled / Disabled
 * 
 */
function callFunc(select) {
	var option =""	
		$('#root_menu').contextMenu('enable_menu', {
			bindings : {
				'thunderDisabled' : function(node) {
					option = "thunderDisabled"
						thunderDisabled(select);
				},
				'thunderEnabled' : function(node) {
					option = "thunderEnabled"
						thunderEnabled(select);
				},
				'copyDeviceIp' : function(node) {
					copyDeviceIp(select);
				},
				'installTDK': function(node) {
	                option = "installTDK";
	                installTDK(select); // Ensure tabType is passed
	            }
			}
		});
}
var deviceeeId;
let selectedTab = 'TDK'; // Default to TDK

function switchTab(tabType) {  
    
    selectedTab = tabType;
    

    // Toggle visibility
    document.getElementById('tdkTab').style.display = tabType === 'TDK' ? 'block' : 'none';
    document.getElementById('vtsTab').style.display = tabType === 'VTS' ? 'block' : 'none';

    // Update button styles
    document.getElementById("tdkTabButton").classList.toggle('active', tabType === 'TDK');
    document.getElementById("vtsTabButton").classList.toggle('active', tabType === 'VTS');


    // API Call to notify backend about tab switch
   
}



function installTDK(deviceId) {
    

    $.get('tdkpackages', { deviceId: deviceId }, function(data) {
       
        deviceeeId=deviceId
        // Clear previous modal content
        $('#popup-container').empty();

        // Append new content
        $('#popup-container').html(data);

        // Check backend flags from hidden inputs
        var deviceNotFree = $('#deviceNotFreeFlag').val() === 'true';
        var noFiles = $('#noFilesFlag').val() === 'true';
		
		
		 if (deviceNotFree) {
            alert("Device is down or busy. Please try later.");
            return; // Stop further processing
        }

        // Proceed only if no issues
        $("#popup-container").modal({
            opacity: 0.7,
            overlayCss: { backgroundColor: "#000" },
            containerCss: {
                width: "550px",
                height: "350px",
                padding: "10px",
                backgroundColor: "#fff",
                borderRadius: "8px"
            },
            onClose: function(dialog) {
                $.modal.close();
                clearInterval(refreshInterval);
            }
        });

        if (typeof refreshInterval !== "undefined") {
            clearInterval(refreshInterval);
        }

        refreshInterval = setInterval(function() {
            refreshFileList(selectedTab);
        }, 2000);
    });
}




/**
 * Dynamic page refresh call. First time called from the document ready of list
 * page
 */
function deviceStatusRefresh() {
	
	setTimeout("loadXMLDoc1();", 5 * 1000);	
	var selectedId = $("#selectedDevice").val();
	var deviceInstanceTotal = $("#deviceInstanceTotal").val();	
	highlightTreeElement('deviceExecutionList_', selectedId, deviceInstanceTotal);
}
/**
 * function used to change the box status as disabled 
 * @param id
 * @param option
 * @param select
 */
function deviceDisabledStatus(id,option,select){		
	$.get('getTDKDeviceStatus', {id:id,option:option,select:select}, function(data) {});// {refreshDevices(data);});
}
/**
 * function used to change the box status as enabled 
 * @param id
 * @param option
 * @param select
 */

function deviceEnabledStatus(id,option,select){
	$.get('getTDKDeviceStatus', {id:id,option:option, select:select}, function(data) {}); //{refreshDevices(data);});
}

/**
 * Function for copying device IP to clipboard
 * @param deviceId
 */
function copyDeviceIp(deviceId){		
	$.get('copyDeviceIp', {deviceId:deviceId}, function(data) {
		if(navigator.clipboard){
			navigator.clipboard.writeText(data)
		}else{
			alert("Sorry! Unable to copy device IP to clipboard. Please copy from here : "+data);
		}
	});
}

function thunderEnabled(deviceId){		
	$.get('thunderEnabled', {deviceId:deviceId}, function() {
		alert(" Thunder Enabled with Port Number 9998");
	});
}

function thunderDisabled(deviceId){		
	$.get('thunderDisabled', {deviceId:deviceId}, function() {
		alert(" Thunder disabled");
	});
}


/**
 * Ajax call to refresh only the list table when dynamic refresh is enabled
 */
function loadXMLDoc1() {
	$.get('create',{t:Math.random(),max:10,offset:0,devicestatustable:true,category:'RDKV'},function(data,status){
		document.getElementById("device_statusV").innerHTML = "";
		document.getElementById("device_statusV").innerHTML = data;
	});
	$.get('create',{t:Math.random(),max:10,offset:0,devicestatustable:true,category:'RDKB'},function(data,status){
		document.getElementById("device_statusB").innerHTML = "";
		document.getElementById("device_statusB").innerHTML = data;
	});
	$.get('create',{t:Math.random(),max:10,offset:0,devicestatustable:true,category:'RDKC'},function(data,status){
		document.getElementById("device_statusC").innerHTML = "";
		document.getElementById("device_statusC").innerHTML = data;
	});
	/*$.get('create',{t:Math.random(),max:10,offset:0,devicestatustable:true},function(data,status){
		//alert(data);
		document.getElementById("device_status").innerHTML = "";
		document.getElementById("device_status").innerHTML = data;
	});*/
	
	deviceStatusRefresh();	
}

function hideSearchoptions(){
	$("#advancedSearch").hide();
	$("#minSearch").show();
	$('.veruthe').empty();
}

function hideAllSearchoptions(){
	$("#advancedSearch").hide();
	$("#minSearch").hide();
	$('.veruthe').empty();
}

function displayAdvancedSearch(){		
	$("#advancedSearch").show();
	$("#minSearch").hide();
	$('.veruthe').empty();
	$('.responseclass').empty();
	$("#listscript").hide();
	$("#scriptValue").val('');	
}

function showMinSearch(){	
	$("#advancedSearch").hide();
	$("#minSearch").show();
	$('.veruthe').empty();
	$("#listscript").show();
}

function hideExectionHistory(){
	$("#listscript").hide();
}

function showOther(){
	$("#otherBased").show();
	$("#dateBased").hide()
	$('.veruthe').empty();
	
}

function showDateBased(){
	$("#dateBased").show();
	$("#otherBased").hide();
	$('.veruthe').empty();
}

function showScriptTypes(){
	var choice = $( "#scriptType" ).val()
	if((choice == "")){
		$("#scriptLabel").hide();
		$("#scriptVal").hide();
		$("#scriptValue").val('');
	}
	else{
		$("#scriptLabel").show();
		$("#scriptVal").show();
		$("#scriptValue").val('');
	}
}

/**
 * Method to display the script field based on script type in combined excel popup
 */
function showScriptTypesForCombined(){
	var choice = $( "#scriptTypeField" ).val()
	if((choice == "")){
		$("#scriptLabelId").hide();
		$("#scriptFieldId").hide();
		$("#scriptValueId").val('');
	}
	else{
		$("#scriptLabelId").show();
		$("#scriptFieldId").show();
		$("#scriptValueId").val('');
	}
}

function showFulltextDeviceDetails(k){
	$("#fulltext"+k).show();
	$("#firstfourlines"+k).hide();
	$("#showlessdd"+k).show();	
}

function showMintextDeviceDetails(k){
	$("#fulltext"+k).hide();
	$("#firstfourlines"+k).show();
	$("#showlessdd"+k).hide();	
}


/**
 * Function to perform deletion of marked execution results. This will invoke an
 * ajax method and perform deletion of corresponding execution instance.
 */
function deleteResults() {

	var notChecked = [];
	var checkedRows;
	$(":checkbox").each(function() {
		if (this.checked) {
			checkedRows = checkedRows + "," + this.id;
		} else {
			notChecked.push(this.id);
		}
	});
	if (checkedRows != null && checkedRows != "") {
		
		var result = confirm("Are you sure you want to delete?");
		if (result==true) {
			$.get('deleteExecutioResults', {
				checkedRows : checkedRows
			}, function(data) {
	
				$(":checkbox").each(function() {
					$('.resultCheckbox').prop('checked', false);
	
				});
				$('.markAll').prop('checked', false);
				location.reload();
			});
		}
	}
	else 
	{
		alert("Please select the execution entries")
	}	
}

/**
 * Function to generate combined excel report of selected execution results. The selected executions
 * must be repeat and rerun executions of the original execution.
 */
function combinedExcelReportGeneration(executionIdList) {
	var notChecked = [];
	var checkedRows = "";
	var url = $("#url").val();
	var executionIdArray = JSON.parse(executionIdList);
	for(i=0;i<=executionIdArray.length;i++){
		if ($('#combinedExecutionCheckbox_'+executionIdArray[i]).is(":checked"))
		{
		  checkedRows =  executionIdArray[i] + "," + checkedRows;
		}
	}
	var status 
	if (checkedRows != null && checkedRows != "") {
		var request = new XMLHttpRequest();
		request.open("GET",url+"/execution/checkValidExecutions?checkedRows="+checkedRows, false);
		request.send(null);
		if (request.status === 200) {
			status = request.responseText
		}
		else{
			alert("Some problem occured while processing request")
		}
		if(status == "true"){
			for(i=0;i<=executionIdArray.length;i++){
				$.get('updateMarkStatus', {
					markStatus : 0,
					id : executionIdArray[i]
				}, function(data) {
				});
			}
			alert("Going to generate the report")
			window.open(url+"/execution/combinedExcelReportGeneration/?checkedRows="+checkedRows, '_blank');
			window.focus();
			return false
		}
		else if(status == "overFlow"){
			alert("Maximum number of executions that can be combined is 10 and minimum number is 2")
			return false
		}
	}
	else {
		alert("Please select the execution entries for report generation")
		return false
	}	
}

/**
 * Function to show the combined Excel PopUp
 */
function showCombinedExcelPopUp(){
	$("#combinedExcelPopUp").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 1200,
	            height: 450	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	 $( "#generateFromDate" ).datepicker();
	 $( "#generateToDate" ).datepicker();
	 var today = new Date();
	 var priorDate = new Date();
	 priorDate.setDate(today.getDate() - 30)
	 var ddtoday = String(today.getDate()).padStart(2, '0');
	 var mmtoday = String(today.getMonth() + 1).padStart(2, '0');
	 var yyyytoday = today.getFullYear();
	 today = mmtoday + '/' + ddtoday + '/' + yyyytoday;
	 var ddprior = String(priorDate.getDate()).padStart(2, '0');
	 var mmprior = String(priorDate.getMonth() + 1).padStart(2, '0');
	 var yyyyprior = priorDate.getFullYear();
	 priorDate = mmprior + '/' + ddprior + '/' + yyyyprior;
	 document.getElementById("generateFromDate").value = priorDate
	 document.getElementById("generateToDate").value = today
	 var category_id = "RDKV"
	 var url = $("#url").val();
	 $.get(url+'/boxType/getBoxTypeFromCategory', {category: category_id}, function(data) {
		var select = '<select id="boxType" name="boxType"><option value="">Please Select</option>';
		for(var index = 0; index < data.length; index ++ ) {
			select += '<option value="' + data[index].name + '">' + data[index].name + '</option>';
		}
		select += '</select>';
		$("#boxTypeId").html(''); 
		$("#boxTypeId").html(select); 
	 });
}

/**
 * Function to validate all input fields in combined Excel PopUp
 */
function validateInputFields(){
	document.getElementById("validate").value = "";
	var fromDateString = document.getElementById("generateFromDate").value;
	var toDateString = document.getElementById("generateToDate").value;
	var boxType = document.getElementById("boxType").value;
	var category = document.getElementById("categoryId").value;
	if (fromDateString == "" || toDateString == "" || boxType == "" || category == "") {
	    alert("Please select all the fields");
	    document.getElementById("validate").value = "false";
	}
	var today = new Date();
	var fromDate = new Date(fromDateString);
	var toDate = new Date(toDateString);
	if((fromDate > today) || (toDate > today)){
	    alert('Selected date cannot be greater than todays date');
	    document.getElementById("validate").value = "false";
	}
	if(fromDate > toDate){
		alert('From Date cannot be greater than To Date');
		document.getElementById("validate").value = "false";
	}
}
/**
 * Function to toggle the div containing the combined report feature explanation
 */
function helpDivToggle(){
	  var x = document.getElementById("helpDiv");
	  if (x.style.display === "none") {
	    x.style.display = "block";
	  } else {
	    x.style.display = "none";
	  }
}

/**
 * Function to perform mark all operation in execution page.
 * 
 * @param me
 */
function clickCheckbox(me) {
	

	var $this = $(this);
	if (me.checked) {
		$(":checkbox").each(function() {
			$('.resultCheckbox').prop('checked', true);
			if(this.id != "benchmarkId" && this.id != "rerunId" && this.id != "systemDiagId"){
				mark(this);
			}
		});
		flagMark = true
	} else {
		$(":checkbox").each(function() {
			$('.resultCheckbox').prop('checked', false);
			if(this.id != "benchmarkId" && this.id != "rerunId" && this.id != "systemDiagId"){
			mark(this);
			}
		});
		flagMark = false
	}
}


/**
 * Function to mark individual execution results in execution page.
 * 
 * @param me
 */
function mark(me) {

	if (me.id != 'undefined' && me.id != 'markAll1' && me.id != 'markAll2'
			&& me.id != "" && me.id != null) {
		if (me.checked) {
			$.get('updateMarkStatus', {
				markStatus : 1,
				id : me.id
			}, function(data) {
			});
		} else {
			$.get('updateMarkStatus', {
				markStatus : 0,
				id : me.id
			}, function(data) {
			});
		}
	}	
}

/**
 * Function used to check the current device status is FREE  and available or not
 * @param deviceStatus
 */

function deviceStatusCheck(device,deviceStatus){
	if((deviceStatus != "FREE" && deviceStatus !=  'null')){
		alert("Device is currently not available for execution");
	}else if(device == 'null' ){ 
		 alert("Device name is not configured")
	 }else{
		 executionTriggeredPopUp()		 
	 }
	
}
/**
 * Function check failed scripts available in execution
 * @param executionInstance
 */
function failureScriptCheck(executionName,device,deviceStatus){
	$.get('failureScriptCheck', {
		executionName : executionName,
	}, function(data) {
		if(data == 'false'){
			alert(" No Failed scripts availble for rerun execution");			
		}else{
			deviceStatusCheck(device,deviceStatus)			
		}			
	});
		
}

/**
 * function will shows pop up 
 */
function  executionTriggeredPopUp(){
	alert("Execution Triggered ");	
}
/**
 * function to install packages
 */
function submitForm(event) {
    event.preventDefault();
    var result = confirm("Device is going to reboot. Do you want to proceed?");
    
    $('#outputDiv').hide();
    $('#LogsFetched').hide();
    $('#progressContainer').hide();
    $('#InstalltionCompleted').hide();
    $('#installation').show();

    if (result) {
        $("#popup").show();

        var selectedFiles = [];
        var checkboxes = document.getElementsByName('selectedFiles');

        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                selectedFiles.push(checkboxes[i].value);
            }
        }

        $('#progressContainer').show();
        $('#progressBar').show();
        simulateProgress();
        $('#progressBar').css('width', '100%');

        var testFiles = JSON.stringify(selectedFiles);
        $('#copyFiles').show();

        $.get('installPackages', { deviceeeId: deviceeeId, selectedFiles: testFiles }, function(response) {
            $("#popup").show();
            $('#copyFiles').hide();
            $("#LogsFetched").hide();
            $('#installButton').hide();
            $("#InstalltionCompleted").show();
            $('#outputDiv').show();
            
            if (response.trim() !== "") {
                $('#LogsFetched').show();
                $('#installation').hide();
                
                var logsHtml = "<pre style='text-align: left; margin: 0; padding: 10px;'>" + response + "</pre>";
                $('#outputDiv').html(logsHtml); // first show only logs
                
                // Then append the success or failure message
                if (response.trim().includes("running")) {
                  
                    $('#outputDiv').append(
                        "<div style='margin-top: 20px; font-weight: bold; color: green; font-size: 1.2em;'>TDK Installed Successfully</div>"
                    );
                } else {
                    
                    $('#outputDiv').append(
                        "<div style='margin-top: 20px; font-weight: bold; color: red; font-size: 1.2em;'>TDK Installation Failed</div>"
                    );
                }

            } else {
                $('#LogsFetched').hide();
                $('#outputDiv').hide();
                $('#installation').hide();
            }

            $("#popup").hide();

            var flashMessage = $("<div>").html(response).find('#flashMessage').text();
            if (flashMessage.trim() !== "") {
                alert(flashMessage);
            }
        });

        if ($('.shell-script-container').find('p').length > 0) {
            $('.shell-script-container').css('border', 'none');
        } else {
            $('.shell-script-container').css('border', '1px solid #ccc');
        }
    } else {
        alert("Installation cancelled.");
    }
}

/**
 * function will show progess for packages installation
 */
function simulateProgress() {
            var progress = 0;
            var interval = setInterval(function() {
                if (progress < 100) {
                    progress += 1;
                    $('#progressBar').css('width', progress + '%');
                } else {
                    clearInterval(interval);
                }
            }, 100); // Adjust the interval as needed to match your backend process time
        }	


/**
 * function will close pop up 
 */
// Function to close the script output popup
function closePopup() {
    $("#outputModal").hide();
}
/**
 * function to create TDK package
 */
function createTDKPackage() {
    // Clear previous logs before new request
    $("#scriptOutput").text(""); 
    $("#packageSuccess").hide();
    $("#packageError").hide();
    $("#uploadSuccess").hide();
    $("#uploadError").hide();
    $("#uploadButton").hide();

    // Show progress message and disable button
    $("#createPackageButton").prop("disabled", true).css("cursor", "not-allowed");

    // Make AJAX call to backend API
    $.ajax({
        url: "createTDKPackage",
        type: "GET",
        data: { deviceeeId: deviceeeId },
        success: function (response) {
            document.getElementById("scriptOutput").style.display = "block";
            const output = response.output || "";
            if (!output.includes("not")) {
                $("#packageSuccess").show();
                $("#scriptOutput").text(output || "TDK Package Created Successfully!");
            } else if (output.includes("not")) {
                $("#packageError").show().html(`
    ? Failed to create package. Please upload a generic package manually.
    <br>
    <a href="javascript:void(0)" onclick="document.getElementById('packageFilee').click()" 
       style="color: #007BFF; text-decoration: underline; font-size: 1em; display: inline-flex; align-items: center; margin-top: 8px;">
        <img src="../images/reorder_up.png" alt="Upload Icon" 
             style="width: 16px; height: 16px; vertical-align: middle; margin-right: 6px;">
        Upload Generic Package
    </a>
    <input type="file" id="packageFilee" name="packageFilee" style="display: none;" onchange="uploadGenericPackage()">
`);


                $("#scriptOutput").text(output).show();
            } else {
                $("#packageError").show().text("Package creation failed.");
                $("#scriptOutput").text(output).show();
            }
        },
        error: function () {
            $("#packageError").show().text("Error processing the request.");
        },
        complete: function () {
            $("#createPackageButton").prop("disabled", false).css("cursor", "pointer");
        }
    });
}
/**
 * function will create TDK Generic package
 */
function uploadGenericPackage() {
    const fileInput = document.getElementById('packageFilee');
    const file = fileInput.files[0];

    if (!file) {
        $("#uploadError").show().text("Please select a package file.");
        return;
    }
	$("#packageError").hide()
    const formData = new FormData();
    formData.append("packageFilee", file);
    formData.append("deviceeeId", deviceeeId);

    $.ajax({
        url: "uploadGenericTDKPackage",
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response.status === "success") {
                $("#uploadSuccess").show().text("Generic TDK Package uploaded successfully.");
            } else {
                $("#uploadError").show().text(response.message || "Upload failed.");
            }
        },
        error: function () {
            $("#uploadError").show().text("Error while uploading the package.");
        }
    });
}

/**
 * function will upload the package
 */
function uploadPackage() {
    var uploadedFile = $("#packageFile")[0].files[0]; 
    
    if (!uploadedFile) {
        alert("Please upload a file first.");
        return;
    }

    var formData = new FormData();
    formData.append("packageFile", uploadedFile);
    formData.append("deviceeeId", deviceeeId); 

    // Clear previous logs
    $("#scriptOutput").hide().text(""); 
    $("#uploadSuccess").hide();
    $("#uploadError").hide();
    $("#packageSuccess").hide();
    $("#packageError").hide();

    // Show progress message
    $("#uploadProgress").show();

    $.ajax({
        url: "processPackage", 
        type: "POST",
        data: formData,
        processData: false, 
        contentType: false, 
        success: function(response) {
            $("#uploadProgress").hide();

            if (response.status === "success") {
                $("#uploadSuccess").show();

                // Show output only if it's not empty
                if (response.output && response.output.trim() !== "") {
                    $("#scriptOutput").show().text(response.output);
                } else {
                    $("#scriptOutput").hide();
                }
            } else {
                $("#uploadError").show().text(response.message || "Failed to upload package.");
                $("#scriptOutput").hide(); // Hide output on failure
            }
        },
        error: function() {
            $("#uploadProgress").hide();
            $("#uploadError").show().text("Error while processing.");
            $("#scriptOutput").hide();
        }
    });
}

/**
 * function will refresh with latest packages
 */
function refreshFileList() {
  
    // Store selected checkboxes before refreshing
    let selectedTdkFiles = new Set();
    let selectedVtsFiles = new Set();


    $("#fileListTable input[name='selectedFiles']:checked").each(function () {
        selectedTdkFiles.add($(this).val());
    });

    $("#vtsFileListTable input[name='selectedVtsFiles']:checked").each(function () {
        selectedVtsFiles.add($(this).val());
    });



    $("#fileListTable tbody").load(`tdkpackages?deviceId=${deviceeeId} #fileListTable tbody > *`, function(response, status, xhr) {
        if (status === "error") {
            console.error("Error refreshing TDK file list:", xhr.status, xhr.statusText);
        } else {
           
            $("#fileListTable input[name='selectedFiles']").each(function () {
                if (selectedTdkFiles.has($(this).val())) {
                    $(this).prop("checked", true);
                }
            });

            bindCheckboxLogic();
        }
    });

    $.get(`getvtsPackages?deviceId=${deviceeeId}`, function(data) {

        let vtsFiles = data.allVtsFilesList || [];

        let html = vtsFiles.length
            ? vtsFiles.map(file => `
                <tr>
                    <td>
                        <label class="checkbox-container">
                            <input type="checkbox" name="selectedVtsFiles" value="${file}" class="checkbox-custom" />
                            <span>${file}</span>
                        </label>
                    </td>
                </tr>
            `).join("")
            : `<tr><td style="text-align: center; font-weight: bold; color: red;">No files available</td></tr>`;

        $("#vtsFileListTable tbody").html(html);

        bindCheckboxLogic(); // Ensure logic is applied to new checkboxes
    });

}

/**
 * function will add the checkbox for selected files
 */
function bindCheckboxLogic() {

    // Handle TDK files
    let tdkCheckboxes = document.querySelectorAll('input[name="selectedFiles"]');
    handleCheckboxSelection(tdkCheckboxes, "lastSelectedFile");

    // Handle VTS files
    let vtsCheckboxes = document.querySelectorAll('input[name="selectedVtsFiles"]');
    handleCheckboxSelection(vtsCheckboxes, "lastSelectedVtsFile");
}
/**
 * function will restore the package selection
 */
function handleCheckboxSelection(checkboxes, storageKey) {
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            console.log(`Checkbox clicked: ${this.value}, Checked: ${this.checked}`);

            if (this.checked) {
                // Disable all other checkboxes when one is selected
                checkboxes.forEach(function (otherCheckbox) {
                    if (otherCheckbox !== checkbox) {
                        otherCheckbox.checked = false;
                        otherCheckbox.disabled = true;
                    }
                });

                // Save the selected file immediately
                sessionStorage.setItem(storageKey, checkbox.value);
                
            } else {
                // Re-enable all checkboxes when none are selected
                let anyChecked = Array.from(checkboxes).some(cb => cb.checked);
                if (!anyChecked) {
                    checkboxes.forEach(cb => cb.disabled = false);
                }

                // Clear stored selection if none are checked
                sessionStorage.removeItem(storageKey);
                
            }
        });
    });

    // Restore last selected checkbox if exists
    let lastSelectedFile = sessionStorage.getItem(storageKey);
    if (lastSelectedFile) {
        checkboxes.forEach(cb => {
            if (cb.value === lastSelectedFile) {
                cb.checked = true;
                cb.dispatchEvent(new Event('change')); // Trigger change event
                
            }
        });
    }
}

// Ensure checkbox logic is applied on page load
bindCheckboxLogic();
/**
 * function will create VTS package
 */
function createVTSPackage() {
    // Clear previous logs before new request
    $("#scriptVTSOutput").text(""); 
    $("#vtspackageSuccess").hide();
    $("#vtspackageError").hide();
    $("#vtsuploadSuccess").hide();
    $("#vtsuploadError").hide();

    // Show progress message and disable button
    $("#createVTSPackageButton").prop("disabled", true).css("cursor", "not-allowed");

    // Make AJAX call to backend API
    $.ajax({
        url: "createVTSPackage",
        type: "GET",
        data: { deviceeeId: deviceeeId }, // Ensure correct deviceId
        success: function (response) {
            
            if (response.status === "success") {
            	 document.getElementById("vtsscriptOutput").style.display = "block";
                $("#vtspackageSuccess").show();
                $("#vtsscriptOutput").text(response.output || "VTS Package Created Successfully!");
            } else {
            	 document.getElementById("vtsscriptOutput").style.display = "block";
                $("#vtspackageError").show().text(response.message || "VTS Package creation failed.");
            }
        },
        error: function (xhr, status, error) {
            $("#vtspackageError").show().text("Error processing the request.");
        },
        complete: function () {
            $("#createVTSPackageButton").prop("disabled", false).css("cursor", "pointer");
        }
    });
}
/**
 * function will upload VTS package
 */
function uploadVTSPackage() {
    var uploadedFile = $("#vtspackageFile")[0].files[0]; 
    
    if (!uploadedFile) {
        alert("Please upload a file first.");
        return;
    }

    var formData = new FormData();
    formData.append("vtspackageFile", uploadedFile);
    formData.append("deviceeeId", deviceeeId); 

    // Clear previous logs
    $("#vtsscriptOutput").hide().text(""); 
    $("#vtsuploadSuccess").hide();
    $("#vtsuploadError").hide();
    $("#vtspackageSuccess").hide();
    $("#vtspackageError").hide();

    // Show progress message
    $("#vtsuploadProgress").show();

    $.ajax({
        url: "processVtsPackage", 
        type: "POST",
        data: formData,
        processData: false, 
        contentType: false, 
        success: function(response) {
            $("#vtsuploadProgress").hide();

            if (response.status === "success") {
                $("#vtsuploadSuccess").show();

                // Show output only if it's not empty
                if (response.output && response.output.trim() !== "") {
                    $("#vtsscriptOutput").show().text(response.output);
                } else {
                    $("#vtsscriptOutput").hide();
                }
            } else {
                $("#vtsuploadError").show().text(response.message || "Failed to upload VTS package.");
                $("#vtsscriptOutput").hide(); // Hide output on failure
            }
        },
        error: function() {
            $("#vtsuploadProgress").hide();
            $("#vtsuploadError").show().text("Error while processing.");
            $("#vtsscriptOutput").hide();
        }
    });
}
/**
 * function will install the VTS packages
 */
function submitVtsForm(event) {
    event.preventDefault();

    var result = confirm("Device is going to reboot for VTS installation. Do you want to proceed?");
    
    // Hide previous logs or messages
    $('#vtsoutputDiv').hide();
    $('#vtsLogsFetched').hide();
    $('#vtsinstallation').show();
    $('#vtssuccess').hide();

    if (result) {
        var selectedVtsFiles = [];
        var checkboxes = document.getElementsByName('selectedVtsFiles');

        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                selectedVtsFiles.push(checkboxes[i].value);
            }
        }

        if (selectedVtsFiles.length === 0) {
            alert("Please select at least one VTS package to install.");
            $('#vtsinstallation').hide();
            return;
        }

        var testFiles = JSON.stringify(selectedVtsFiles);
        $('#vtsinstallation').show();

        // Replace `deviceeeId` with actual value or dynamically get it if needed
        $.get('installPackages', {
            deviceeeId: deviceeeId,
            selectedVtsFiles: testFiles
        }, function(response) {
            $('#vtsinstallation').hide();

            if (response.trim() !== "") {
                $('#vtsLogsFetched').show();
                $('#vtssuccess').show();

                var finalVtsLogs = "<div style='background-color: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 14px; white-space: pre-wrap; overflow-x: auto;'>"
                                    + response
                                    + "</div>";

                // Add success or failure message after VTS logs
                if (response.trim().includes("enabled")) {
                    finalVtsLogs += "<div style='margin-top: 20px; font-weight: bold; color: green; font-size: 1.2em;'> VTS Installed Successfully</div>";
                } else {
                    finalVtsLogs += "<div style='margin-top: 20px; font-weight: bold; color: red; font-size: 1.2em;'> VTS Installation Failed</div>";
                }

                // Show logs and final status message
                $('#vtsoutputDiv').show().html(finalVtsLogs);
            } else {
                $('#vtsLogsFetched').hide();
                $('#vtsoutputDiv').hide();
            }

            // Optional: extract flash message
            var flashMessage = $("<div>").html(response).find('#flashMessage').text();
            if (flashMessage.trim() !== "") {
                alert(flashMessage);
            }
        });
    } else {
        $('#vtsinstallation').hide();
        alert("VTS installation cancelled.");
    }
}








    