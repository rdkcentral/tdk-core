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
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
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
  /**
   * Initialize the component and forms
   */ 
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
      scriptname: ['', [Validators.required, this.noSpacesValidator]],
      module:['',Validators.required],
      primitiveTest: [{value:this.defaultPrimitive, disabled: true}],
      devicetype: ['', Validators.required],
      executiontimeout: ['', Validators.required],
      longdurationtest: [''],
      skipexecution: [''],
      synopsis: ['', [Validators.required, this.noSpacesValidator]]
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
  /**
   * Get the controls of the register form.
   * @returns The controls of the register form.
   */  
  get f() { return this.firstFormGroup.controls; }
  /**
     * This method is no space is allow.
     */
  noSpacesValidator(control: AbstractControl): ValidationErrors | null {
    const value = control.value ? control.value.toString() : '';
    return value.trimStart().length !== value.length ? { noLeadingSpaces: true } : null;
  }
  
  onInput(event: Event): void {
    const inputElement = event.target as HTMLTextAreaElement;
    const value = inputElement.value;
    if (value.startsWith(' ')) {
      this.firstFormGroup.get('synopsis')?.setValue(value.trimStart(), { emitEvent: false });
    }
  }
  onScritName(event: Event): void {
    const inputElement = event.target as HTMLTextAreaElement;
    const value = inputElement.value;
    if (value.startsWith(' ')) {
      this.firstFormGroup.get('scriptname')?.setValue(value.trimStart(), { emitEvent: false });
    }
  }
  onTestcaseID(event: Event): void {
    const inputElement = event.target as HTMLTextAreaElement;
    const value = inputElement.value;
    if (value.startsWith(' ')) {
      this.secondFormGroup.get('testcaseID')?.setValue(value.trimStart(), { emitEvent: false });
    }
  }
  onTestObjective(event: Event): void {
    const inputElement = event.target as HTMLTextAreaElement;
    const value = inputElement.value;
    if (value.startsWith(' ')) {
      this.secondFormGroup.get('testObjective')?.setValue(value.trimStart(), { emitEvent: false });
    }
  }
  onInputParameters(event: Event): void {
    const inputElement = event.target as HTMLTextAreaElement;
    const value = inputElement.value;
    if (value.startsWith(' ')) {
      this.secondFormGroup.get('inputParameters')?.setValue(value.trimStart(), { emitEvent: false });
    }
  }
  onAutomationApproach(event: Event): void {
    const inputElement = event.target as HTMLTextAreaElement;
    const value = inputElement.value;
    if (value.startsWith(' ')) {
      this.secondFormGroup.get('automationApproach')?.setValue(value.trimStart(), { emitEvent: false });
    }
  }
  onTestStub(event: Event): void {
    const inputElement = event.target as HTMLTextAreaElement;
    const value = inputElement.value;
    if (value.startsWith(' ')) {
      this.secondFormGroup.get('testStub')?.setValue(value.trimStart(), { emitEvent: false });
    }
  }
  onInterface(event: Event): void {
    const inputElement = event.target as HTMLTextAreaElement;
    const value = inputElement.value;
    if (value.startsWith(' ')) {
      this.secondFormGroup.get('rdkInterface')?.setValue(value.trimStart(), { emitEvent: false });
    }
  }
  onExpectedOutput(event: Event): void {
    const inputElement = event.target as HTMLTextAreaElement;
    const value = inputElement.value;
    if (value.startsWith(' ')) {
      this.secondFormGroup.get('expectedOutput')?.setValue(value.trimStart(), { emitEvent: false });
    }
  }
  /**
   * Method to get all modules
   */   
  getAllModules(): void{
    this.modulesService.findallbyCategory(this.selectedCategory).subscribe(res=>{
      this.allModules = JSON.parse(res);
    })
  }

getSelectedModule(event: any):void{
    this.allPrimitiveTest = [];
    let selectedValue = event.target.value;
    if(!selectedValue){
      this.firstFormGroup.get('primitiveTest')?.disable();
    }else{
      this.getAllPrimitiveTest(selectedValue);
    }
  }
  /**
   * Method to get primitive test based on module select
   */ 
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
  /**
   * onChange primitive test 
   */ 
onChangePrimitive(event:any):void{
  let primitiveValue = event.target.value;
  this.defaultPrimitive = primitiveValue;
  this.getCode();
}
  /**
   * Method to get longDuration value
   */ 
longDuration(event:any):void{
  this.longDurationValue = event.target.checked;
}
  /**
   * Method to get skipExecution value
   */ 
skipExecution(event:any):void{
  this.skipExecutionValue = event.target.checked;
}
  /**
   * Method to get priority value 
   */ 
changePriority(event:any):void{
  const priorityValue = event.target.value;
  this.changePriorityValue = priorityValue;
}
  /**
   * Method to get pycode value from monaco editor 
   */ 
getCode():void{
  let temp = this.defaultPrimitive;
  if(temp){
    this.scriptservice.scriptTemplate(temp).subscribe(res=>{
      this.sampleFile = res;
    })
  }
}
  /**
   * Method to get all device type
   */ 
getAlldeviceType(): void{
    this.deviceTypeService.getfindallbycategory(this.selectedCategory).subscribe(res=>{
      this.allDeviceType = (JSON.parse(res));
    })
  }
  /**
   * Method to select device type
   */   
  onItemSelect(item:any):void{
    if (!this.deviceNameArr.some(selectedItem => selectedItem.deviceTypeName === item.deviceTypeName)) {
      this.deviceNameArr.push(item.deviceTypeName);
    }
  }
  /**
   * Method to deselect device type
   */  
  onDeSelect(item:any):void{
    let filterDevice = this.deviceNameArr.filter(name => name != item.deviceTypeName);
    this.deviceNameArr = filterDevice;
  }
  /**
   * Method to selectall device type
   */  
  onSelectAll(items: any[]):void{
   let devices = this.allDeviceType.filter(
    (item:any)=> !this.deviceNameArr.find((selected)=>selected.deviceTypeId === item.deviceTypeId)
   );
   this.deviceNameArr = devices.map((item:any)=>item.deviceTypeName)
  }
  /**
   * Method to deselectall device type
   */   
  onDeSelectAll(item:any):void{
    this.deviceNameArr=[];
  }
// You can also change editor options dynamically if needed
  onCodeChange(value: string) :void{
    let val = value;
  }

  updateOptionalLabel() :void{
    this._matStepperIntl.optionalLabel = this.optionalLabelText;
    this._matStepperIntl.changes.next();
  }
  /**
   * Submission for create script
   */     
  onSubmit():void{
      const scriptCreateData = {
        name: this.firstFormGroup.value.scriptname,
        synopsis : this.firstFormGroup.value.synopsis,
        executionTimeOut : this.firstFormGroup.value.executiontimeout,
        primitiveTestName: this.defaultPrimitive,
        deviceTypes: this.firstFormGroup.value.devicetype,
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
  /**
   * Navigate to script page
   */ 
  goBack():void{
    localStorage.removeItem('category');
    this.router.navigate(["/script"]);
  }


}
