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
import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MaterialModule } from '../../../material/material.module';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { ScriptsService } from '../../../services/scripts.service';
import { LoaderComponent } from '../loader/loader.component';

@Component({
  selector: 'app-execute-dialog',
  standalone: true,
  imports: [CommonModule,LoaderComponent,ReactiveFormsModule,FormsModule, MaterialModule,NgMultiSelectDropDownModule],
  templateUrl: './execute-dialog.component.html',
  styleUrl: './execute-dialog.component.css'
})
export class ExecuteDialogComponent {

  executeForm!:FormGroup;
  FormSubmitted = false;
  devicetypeSettings = {};
  deviceList =[];
  selectedScriptType!:string;
  showHideSuite = false;
  showHideScript = true;
  showReRun = false;
  showLogs = false;
  showLoader = false;

  constructor(
    public dialogRef: MatDialogRef<ExecuteDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, private fb:FormBuilder,private scriptservice:ScriptsService) {
  }

  ngOnInit(): void {
    this.devicetypeSettings = {
      singleSelection: false,
      idField: 'id',
      textField: 'name',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      itemsShowLimit: 3,
      allowSearchFilter: true,
    };
    let executionName = this.data;
    console.log(executionName.name);
    this.executeForm = this.fb.group({
      executionName:[this.data.name,{disabled: true}],
      selectType: [''],
      device:[''],
      selectScript:['']
    });
    this.scriptservice.getAllDevice().subscribe((res:any)=>{
      this.deviceList = res[0].childData;
      console.log(this.deviceList);
    }) 
 
  }

  close(): void {
    this.dialogRef.close(false); 
  }

  scriptType(val:any){
    console.log(val);
    if (val === 'testsuite'){
      this.showHideScript = false;
      this.showHideSuite = true;
    }else{
      this.showHideScript = true;
      this.showHideSuite = false;
    }
    
  }
  reRunChange(event:any){
    if(event.target.checked){
      this.showReRun = true;
    }else{
      this.showReRun = false;
    }
  }

  formSubmit(){
    this.showLoader = true;
    this.showLogs = false;
  //  setTimeout(() => {
  //   this.showLogs = true;
  //   this.showLoader = false;
  //  }, 3000);
  }
  
  scheduleOpen(){

  }

}
