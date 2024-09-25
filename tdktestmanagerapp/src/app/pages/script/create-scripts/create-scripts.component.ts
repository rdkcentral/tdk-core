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
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component, inject, TemplateRef, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { MONACO_PATH, MonacoEditorModule } from '@materia-ui/ngx-monaco-editor';
import { AuthService } from '../../../auth/auth.service';
import { Router } from '@angular/router';
import {MatStepperIntl} from '@angular/material/stepper';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
@Component({
  selector: 'app-create-scripts',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule,FormsModule,
    NgMultiSelectDropDownModule,MonacoEditorModule],
  templateUrl: './create-scripts.component.html',
  styleUrl: './create-scripts.component.css',
  providers: [
    { provide: MONACO_PATH, useValue: 'assets/monaco-editor/' }
  ]
})
export class CreateScriptsComponent {

  dropdownSettings = {};
  boxtypeSettings = {};
  versionSettings = {};
  firstFormGroup!:FormGroup;
  secondFormGroup!:FormGroup;
  thirdFormGroup!:FormGroup;
  allsocVendors!:any[]
  dropdownList =[
    {"subBoxtypeId":1,"subBoxtypeName":"Primitive test 1"},
    {"subBoxtypeId":2,"subBoxtypeName":"Primitive test 2"},
    {"subBoxtypeId":3,"subBoxtypeName":"Primitive test 3"},
    {"subBoxtypeId":4,"subBoxtypeName":"Primitive test 4"},
    {"subBoxtypeId":5,"subBoxtypeName":"Primitive test 5"},
    {"subBoxtypeId":6,"subBoxtypeName":"Primitive test 6"},
    {"subBoxtypeId":7,"subBoxtypeName":"Primitive test 7"},
    {"subBoxtypeId":8,"subBoxtypeName":"Primitive test 8"},
    {"subBoxtypeId":9,"subBoxtypeName":"Primitive test 9"},
    {"subBoxtypeId":10,"subBoxtypeName":"Primitive test 10"},
  ];
  code = this.getCode();
  editorOptions = { theme: 'vs-dark', language: 'python' };
  selectedCategoryName! : string ;
  private _matStepperIntl = inject(MatStepperIntl);
  optionalLabelText!: string;
  newtestDialogRef!: MatDialogRef<any>;
  @ViewChild('newtestCaseTemplate', { static: true }) newtestCaseTemplate!: TemplateRef<any>;
  isLinear = true;

  constructor(private authservice : AuthService,private router: Router, private fb : FormBuilder,
    public dialog:MatDialog
  ) { }

  ngOnInit(): void {
    this.dropdownSettings = {
      singleSelection: true,
      idField: 'subBoxtypeId',
      textField: 'subBoxtypeName',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      itemsShowLimit: 3,
      allowSearchFilter: true,
    };
    this.boxtypeSettings = {
      singleSelection: false,
      idField: 'subBoxtypeId',
      textField: 'subBoxtypeName',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      itemsShowLimit: 3,
      allowSearchFilter: true,
    };
    this.versionSettings = {
      singleSelection: false,
      idField: 'subBoxtypeId',
      textField: 'subBoxtypeName',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      itemsShowLimit: 3,
      allowSearchFilter: true,
    };
    const selectedCategory = localStorage.getItem('scriptCategory');
    this.selectedCategoryName = selectedCategory?selectedCategory:'RDKV';

    this.firstFormGroup = this.fb.group({
      scriptname: ['', Validators.required],
      module:['',Validators.required],
      primitivetest: ['', Validators.required],
      boxtype: ['', Validators.required],
      executiontimeout: ['', Validators.required],
      longdurationtest: ['', Validators.required],
      skipexecution: ['', Validators.required],
      synopsis: ['', Validators.required]
    });
    this.secondFormGroup = this.fb.group({
      // testScript: ['', Validators.required],
      testcaseID: ['', Validators.required],
      testObjective: ['', Validators.required],
      inputParameters: ['', Validators.required],
      automationApproach: ['', Validators.required],
      priority: [''],
      remarks: [''],
      testType: [''],
      // supportedBoxType: ['', Validators.required],
      rdkInterface: ['', Validators.required],
      expectedOutput: [''],
      testPreRequisites: [''],
      // skipped: [''],
      releaseVersion:[''],
      testStub:['']
    });
    this.thirdFormGroup = this.fb.group({
      pythonEditor: ['', Validators.required],
  
    });
  }


  getCode() {
    return `
      # use tdklib library,which provides a wrapper for tdk testcase script
      import tdklib;
      import aampUtilitylib;
      from time import sleep;

      streamType="hlsstream"
      expectedResult="SUCCESS"
      #pattern to be searched for event validation
      pattern="AAMP_EVENT_TUNED"
      
      #Test component to be tested
      aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");
      sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");
      
      #IP and Port of box, No need to change,
      #This will be replaced with correspoing Box Ip and port while executing script
      ip = <ipaddress>
      port = <port>
      
      aampObj.configureTestCase(ip,port,'Aamp_HLS_GetPlayback_Duration');
      sysObj.configureTestCase(ip,port,'Aamp_HLS_GetPlayback_Duration');
      
      #Get the result of connection with test component and STB
      aampLoadStatus = aampObj.getLoadModuleResult();
      print "AAMP module loading status : %s" %aampLoadStatus;
      sysLoadStatus = sysObj.getLoadModuleResult();
      print "SystemUtil module loading status : %s" %sysLoadStatus;
      
      aampObj.setLoadModuleStatus(aampLoadStatus);
      sysObj.setLoadModuleStatus(sysLoadStatus);
      
      if ("SUCCESS" in aampLoadStatus.upper()) and ("SUCCESS" in sysLoadStatus.upper()):
      
          #fetch Aamp stream from config file
          tuneURL=aampUtilitylib.getAampTuneURL(streamType);
          #Prmitive test case which associated to this Script
          tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
          tdkTestObj.addParameter("URL",tuneURL);
      
          #Execute the test case in STB
          tdkTestObj.executeTestCase(expectedResult);
          #Get the result of execution
          result = tdkTestObj.getResult();
          if expectedResult in result:
              print "AAMP Tune is success"
              #Search events in Log
              result=aampUtilitylib.searchAampEvents(sysObj, pattern);
              if expectedResult in result:
                  print "AAMP Tune events are verified"
                  print "[TEST EXECUTION RESULT] : %s" %result;
                  #Set the result status of execution
                  tdkTestObj.setResultStatus("SUCCESS");
                  sleep(10);
      
                  tdkTestObj = aampObj.createTestStep('Aamp_AampGetPlaybackDuration');
                  tdkTestObj.addParameter("URL",tuneURL);
                  tdkTestObj.executeTestCase(expectedResult);
                  result = tdkTestObj.getResult();
                  details = tdkTestObj.getResultDetails();
                  if expectedResult in result:
                      print "AAMP Get Playback Duration is executed successfully"
                      print "[TEST EXECUTION RESULT] : %s" %result;
                      print details;
                      #Set the result status of execution
                      tdkTestObj.setResultStatus("SUCCESS");
                  else:
                      print "AAMP Get Playback Duration returns invalid duration"
                      print "[TEST EXECUTION RESULT] : %s" %result;
                      print details;
                      #Set the result status of execution
                      tdkTestObj.setResultStatus("FAILURE");
              else:
                  print "No AAMP events are received"
                  #Set the result status of execution
                  tdkTestObj.setResultStatus("FAILURE");
              #AampTuneStop call
              tdkTestObj = aampObj.createTestStep('Aamp_AampStop');
              #Execute the test case in STB
              tdkTestObj.executeTestCase(expectedResult);
              #Get the result of execution
              result = tdkTestObj.getResult();
              if expectedResult in result:
                  print "AAMP Stop Success"
                  tdkTestObj.setResultStatus("SUCCESS")
              else:
                  print "AAMP Stop Failure"
                  tdkTestObj.setResultStatus("FAILURE")
      
          else:
              print "AAMP Tune is Failure"
              print "[TEST EXECUTION RESULT] : %s" %result;
              #Set the result status of execution
              tdkTestObj.setResultStatus("FAILURE");
      
          #Unload Module
          aampObj.unloadModule("aamp");
          sysObj.unloadModule("systemutil");
      else:
          print "Failed to load aamp/systemutil module";
      
    `;
  }
  // You can also change editor options dynamically if needed
  onCodeChange(value: string) {
    
  }

  back(){
    this.router.navigate(["/script"]);
    localStorage.removeItem('scriptCategory');
  }

  updateOptionalLabel() {
    this._matStepperIntl.optionalLabel = this.optionalLabelText;
    this._matStepperIntl.changes.next();
  }


}
