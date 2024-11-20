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
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { MONACO_PATH, MonacoEditorModule } from '@materia-ui/ngx-monaco-editor';
import { Router } from '@angular/router';
import {MatStepperIntl} from '@angular/material/stepper';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { ModulesService } from '../../../services/modules.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DevicetypeService } from '../../../services/devicetype.service';
import { PrimitiveTestService } from '../../../services/primitive-test.service';
import { ScriptsService } from '../../../services/scripts.service';
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

  firstFormGroup!:FormGroup;
  secondFormGroup!:FormGroup;
  thirdFormGroup!:FormGroup;
  configureName!: string;
  allDeviceType:any;
  selectedDeviceCategory : string = 'RDKV';
  allsocVendors!:any[]
  deviceTypeSettings = {};
  sampleFile:string = '';
  editorOptions = { theme: 'vs-dark', language: 'python' };
  selectedCategoryName! : string ;
  private _matStepperIntl = inject(MatStepperIntl);
  optionalLabelText!: string;
  newtestDialogRef!: MatDialogRef<any>;
  @ViewChild('newtestCaseTemplate', { static: true }) newtestCaseTemplate!: TemplateRef<any>;
  isLinear = true;
  allModules:any;
  allPrimitiveTest:any[]=[];
  userGroupName:any;
  deviceNameArr: any[]=[]
  defaultPrimitive:any;
  changePriorityValue!:string;
  longDurationValue!:boolean;
  skipExecutionValue! :boolean;
  selectedCategory! : string;


  constructor(private router: Router, private fb : FormBuilder,
    public dialog:MatDialog, private modulesService:ModulesService, private deviceTypeService:DevicetypeService,
    private primitiveTestService: PrimitiveTestService,private scriptservice: ScriptsService, private _snakebar: MatSnackBar,) {
    this.userGroupName = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
   }

  ngOnInit(): void {
   let category = localStorage.getItem('category') || '';
   this.selectedCategory = category?category:'RDKV';
    this.deviceTypeSettings = {
      singleSelection: false,
      idField: 'deviceTypeId',
      textField: 'deviceTypeName',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      itemsShowLimit: 3,
      allowSearchFilter: false,
    };
    const selectedCategory = localStorage.getItem('category');
    if(selectedCategory === 'RDKB'){
      this.selectedCategoryName = 'Broadband';
    }else if(selectedCategory === 'RDKC'){
      this.selectedCategoryName = 'Camera';
    }else{
      this.selectedCategoryName = 'Video';
    }
    this.getAllModules();
    this.getAlldeviceType();

    this.firstFormGroup = this.fb.group({
      scriptname: ['', Validators.required],
      module:['',Validators.required],
      primitiveTest: [{value:this.defaultPrimitive, disabled: true}],
      devicetype: ['', Validators.required],
      executiontimeout: ['', Validators.required],
      longdurationtest: [''],
      skipexecution: [''],
      synopsis: ['', Validators.required]
    });
    this.secondFormGroup = this.fb.group({
      testcaseID: ['', Validators.required],
      testObjective: ['', Validators.required],
      inputParameters: ['', Validators.required],
      automationApproach: ['', Validators.required],
      priority: ['',Validators.required],
      testStub:['',Validators.required],
      testType: ['',Validators.required],
      rdkInterface: ['', Validators.required],
      expectedOutput: ['',Validators.required],
      testPreRequisites: [''],
      remarks: [''],
      releaseVersion:[''],
    });
    this.thirdFormGroup = this.fb.group({
      pythonEditor: [ this.sampleFile, Validators.required],
    });
    this.firstFormGroup.get('module')?.valueChanges.subscribe(value => {
      if(value){
        this.getAllPrimitiveTest(value);
        this.firstFormGroup.get('primitiveTest')?.enable();

      }else{
        this.allPrimitiveTest = [];
        this.firstFormGroup.get('primitiveTest')?.disable();
      }
    });

  }
  getAllModules(): void{
    this.modulesService.findallbyCategory(this.selectedCategory).subscribe(res=>{
      this.allModules = JSON.parse(res);
    })
  }

getSelectedModule(event: any) {
    this.allPrimitiveTest = [];
    let selectedValue = event.target.value;
    if(!selectedValue){
      this.firstFormGroup.get('primitiveTest')?.disable();
    }else{
      this.getAllPrimitiveTest(selectedValue);
    }
  }

getAllPrimitiveTest(value: any): void{
    this.primitiveTestService.getParameterNames(value).subscribe({
      next: (res) => {
        this.allPrimitiveTest = JSON.parse(res); 
        for (let i = 0; i < this.allPrimitiveTest.length; i++) {
          this.defaultPrimitive = this.allPrimitiveTest[0].primitiveTestName;
          this.getCode();
        }
      },
      error: (err) => {
        let errmsg = JSON.parse(err.error);
        this._snakebar.open(errmsg.message, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
      })
    }
  })
}
onChangePrimitive(event:any){
  let primitiveValue = event.target.value;
  this.defaultPrimitive = primitiveValue;
  this.getCode();
}

longDuration(event:any){
  this.longDurationValue = event.target.checked;
}

skipExecution(event:any){
  this.skipExecutionValue = event.target.checked;
}

changePriority(event:any){
  const priorityValue = event.target.value;
  this.changePriorityValue = priorityValue;
}
getCode() {
  let temp = this.defaultPrimitive;
  if(temp){
    this.scriptservice.scriptTemplate(temp).subscribe(res=>{
      this.sampleFile = res;
    })
  }

  }

  getAlldeviceType(): void{
    this.deviceTypeService.getfindallbycategory(this.selectedCategory).subscribe(res=>{
      this.allDeviceType = (JSON.parse(res));
    })
  }
  onItemSelect(item:any){
    if (!this.deviceNameArr.some(selectedItem => selectedItem.deviceTypeName === item.deviceTypeName)) {
      this.deviceNameArr.push(item.deviceTypeName);
    }
  }
  onDeSelect(item:any){
    let filterDevice = this.deviceNameArr.filter(name => name != item.deviceTypeName);
    this.deviceNameArr = filterDevice;
  }
  onSelectAll(items: any[]){
   let devices = this.allDeviceType.filter(
    (item:any)=> !this.deviceNameArr.find((selected)=>selected.deviceTypeId === item.deviceTypeId)
   );
   this.deviceNameArr = devices.map((item:any)=>item.deviceTypeName)
  }
  onDeSelectAll(item:any){
    this.deviceNameArr=[];
  }
  // You can also change editor options dynamically if needed
  onCodeChange(value: string) {
    let val = value;
  }

  back(){
    this.router.navigate(["/script"]);
  }

  updateOptionalLabel() {
    this._matStepperIntl.optionalLabel = this.optionalLabelText;
    this._matStepperIntl.changes.next();
  }
  onSubmit() {
      const scriptCreateData = {
        name: this.firstFormGroup.value.scriptname,
        synopsis : this.firstFormGroup.value.synopsis,
        executionTimeOut : this.firstFormGroup.value.executiontimeout,
        primitiveTestName: this.defaultPrimitive,
        deviceTypes: this.deviceNameArr,
        skipExecution:this.firstFormGroup.value.skipexecution,
        longDuration:this.firstFormGroup.value.longdurationtest,
        testId: this.secondFormGroup.value.testcaseID,
        objective:this.secondFormGroup.value.testObjective,
        testType:this.secondFormGroup.value.testType ,
        apiOrInterfaceUsed:this.secondFormGroup.value.rdkInterface,
        inputParameters:this.secondFormGroup.value.inputParameters,
        prerequisites:this.secondFormGroup.value.testPreRequisites,
        automationApproach:this.secondFormGroup.value.automationApproach,
        expectedOutput:this.secondFormGroup.value.expectedOutput,
        priority:this.changePriorityValue,
        testStubInterface:this.secondFormGroup.value.testStub,
        releaseVersion:this.secondFormGroup.value.releaseVersion,
        remarks:this.secondFormGroup.value.remarks,
        userGroup:this.userGroupName.userGroupName,
      };
      const pythonContent = this.thirdFormGroup.value.pythonEditor;
      const filename = `${this.firstFormGroup.value.scriptname}.py`;
      const scriptFile = new File([pythonContent],filename,{type: 'text/x-python'});
      this.scriptservice.createScript(scriptCreateData,scriptFile).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 2000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["/script"]);
          }, 1000);
        },
        error: (err) => {
          let errmsg =JSON.parse(err.error) ;
          this._snakebar.open(errmsg.message, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
        })
      }
    })
  }

  goBack(){
    this.router.navigate(["/script"]);
  }


}
