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
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { MonacoEditorModule } from '@materia-ui/ngx-monaco-editor';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { AuthService } from '../../../auth/auth.service';
import { Router } from '@angular/router';
import { ModulesService } from '../../../services/modules.service';
import { PrimitiveTestService } from '../../../services/primitive-test.service';
import { ScriptsService } from '../../../services/scripts.service';
import { DevicetypeService } from '../../../services/devicetype.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatStepperIntl } from '@angular/material/stepper';
import { Validators } from 'ngx-editor';

@Component({
  selector: 'app-edit-scripts',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule,FormsModule,
    NgMultiSelectDropDownModule,MonacoEditorModule],
  templateUrl: './edit-scripts.component.html',
  styleUrl: './edit-scripts.component.css'
})
export class EditScriptsComponent {
  firstFormGroup!:FormGroup;
  secondFormGroup!:FormGroup;
  thirdFormGroup!:FormGroup;
  configureName!: string;
  allDeviceType:any;
  selectedDeviceCategory : string = 'RDKV';
  allsocVendors!:any[]
  deviceTypeSettings = {};
  code:string='';
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
  scriptDeatilsObj:any;
  RDKFlavor: any;

  constructor(private authservice : AuthService,private router: Router, private fb : FormBuilder,
    public dialog:MatDialog, private modulesService:ModulesService, private deviceTypeService:DevicetypeService,
    private primitiveTestService: PrimitiveTestService,private scriptservice: ScriptsService, private _snakebar: MatSnackBar,) {
    this.userGroupName = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
    this.scriptDeatilsObj = JSON.parse(localStorage.getItem('scriptDetails') || '{}');
   }
  ngOnInit(): void {
    this.deviceTypeSettings = {
      singleSelection: false,
      idField: 'deviceTypeName',
      textField: 'deviceTypeName',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      itemsShowLimit: 3,
      allowSearchFilter: false,
    };
    const selectedCategory = localStorage.getItem('category');
    this.RDKFlavor = selectedCategory;
    if(selectedCategory === 'RDKB'){
      this.selectedCategoryName = 'Broadband';
    }else if(selectedCategory === 'RDKC'){
      this.selectedCategoryName = 'Camera';
    }else{
      this.selectedCategoryName = 'Video';
    }
    this.getAllModules();
    this.getAlldeviceType();
    this.allDeviceType = this.scriptDeatilsObj.deviceTypes.map((deviceType: string) => ({ deviceTypeId: deviceType, deviceTypeName: deviceType }));
    
    this.firstFormGroup = this.fb.group({
      scriptname: [this.scriptDeatilsObj.name, [Validators.required,this.noSpacesValidator]],
      module:[{value:this.scriptDeatilsObj.moduleName, disabled: true}],
      primitiveTest: [{value:this.scriptDeatilsObj.primitiveTestName, disabled: true}],
      devicetype: [[], [Validators.required]],
      executiontimeout: [this.scriptDeatilsObj.executionTimeOut, [Validators.required]],
      longdurationtest: [this.scriptDeatilsObj.longDuration],
      skipexecution: [this.scriptDeatilsObj.skipExecution],
      synopsis: [this.scriptDeatilsObj.synopsis, [Validators.required,this.noSpacesValidator]]
    });
    this.secondFormGroup = this.fb.group({
      testcaseID: [this.scriptDeatilsObj.testId, Validators.required],
      testObjective: [this.scriptDeatilsObj.objective, Validators.required],
      inputParameters: [this.scriptDeatilsObj.inputParameters, Validators.required],
      automationApproach: [this.scriptDeatilsObj.automationApproach, Validators.required],
      priority: [this.scriptDeatilsObj.priority,Validators.required],
      testStub:[this.scriptDeatilsObj.testStubInterface,Validators.required],
      testType: [this.scriptDeatilsObj.testType,Validators.required],
      rdkInterface: [this.scriptDeatilsObj.testStubInterface, Validators.required],
      expectedOutput: [this.scriptDeatilsObj.expectedOutput,Validators.required],
      testPreRequisites: [this.scriptDeatilsObj.prerequisites],
      remarks: [this.scriptDeatilsObj.remarks],
      releaseVersion:[this.scriptDeatilsObj.releaseVersion],
    });
    this.thirdFormGroup = this.fb.group({
      pythonEditor: [ this.scriptDeatilsObj.scriptContent, Validators.required],
    });
    this.getAllPrimitiveTest(this.scriptDeatilsObj.moduleName);
    this.code = this.scriptDeatilsObj.scriptContent;
    this.firstFormGroup.patchValue({ devicetype: this.scriptDeatilsObj.deviceTypes });
    this.deviceNameArr = this.firstFormGroup.value.devicetype;
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
  getAllModules(): void{
    this.configureName=this.RDKFlavor;
    this.modulesService.findallbyCategory(this.configureName).subscribe(res=>{
      this.allModules = JSON.parse(res); 
    })
  }

changeModule(event:any): void {
  let moduleName = event.target.value;
  this.getAllPrimitiveTest(moduleName);
}
getAllPrimitiveTest(value: any): void{
    this.primitiveTestService.getParameterNames(value).subscribe({
      next: (res) => {
        this.allPrimitiveTest = JSON.parse(res);
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
onChangePrimitive(event:any): void {
  let primitiveValue = event.target.value;
  this.defaultPrimitive = primitiveValue;
}
changePriority(event:any): void {
  const priorityValue = event.target.value;
  this.changePriorityValue = priorityValue;
}

  getAlldeviceType(): void{
    this.configureName=this.RDKFlavor;
    this.deviceTypeService.getfindallbycategory(this.configureName).subscribe(res=>{
      this.allDeviceType = (JSON.parse(res));
    })
  }

  onItemSelect(item:any): void {
    if (!this.deviceNameArr.some(selectedItem => selectedItem.deviceTypeName === item.deviceTypeName)) {
      this.deviceNameArr.push(item.deviceTypeName);
    }
  }

  onDeSelect(item:any): void {
    let filterDevice = this.deviceNameArr.filter(name => name != item.deviceTypeName);
    this.deviceNameArr = filterDevice;
  }

  onSelectAll(items: any[]): void {
    let devices = this.allDeviceType.filter(
      (item:any)=> !this.deviceNameArr.find((selected)=>selected.deviceTypeId === item.deviceTypeId)
     );
     this.deviceNameArr = devices.map((item:any)=>item.deviceTypeName)
  }
  onDeSelectAll(item:any): void {
    this.deviceNameArr=[];
  }

  // You can also change editor options dynamically if needed
  onCodeChange(value: string): void {
    let val = value;
  }
  /**
   * navigate to script page
  */ 
  back(): void {
    this.router.navigate(["/script"]);
    localStorage.removeItem('scriptCategory');
  }

  updateOptionalLabel() : void {
    this._matStepperIntl.optionalLabel = this.optionalLabelText;
    this._matStepperIntl.changes.next();
  }
  /**
   * Submission for customSuite update
  */   
  onSubmit(): void {
    const scriptUpdateData = {
      id:this.scriptDeatilsObj.id,
      name: this.firstFormGroup.value.scriptname,
      synopsis : this.firstFormGroup.value.synopsis,
      executionTimeOut : this.firstFormGroup.value.executiontimeout,
      primitiveTestName: this.defaultPrimitive?this.defaultPrimitive:this.scriptDeatilsObj.primitiveTestName,
      deviceTypes:this.deviceNameArr?this.deviceNameArr:this.scriptDeatilsObj.deviceTypes,
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
      priority:this.changePriorityValue?this.changePriorityValue:this.scriptDeatilsObj.priority,
      testStubInterface:this.secondFormGroup.value.testStub,
      releaseVersion:this.secondFormGroup.value.releaseVersion,
      remarks:this.secondFormGroup.value.remarks,
      userGroup:this.userGroupName.userGroupName,
    };
    const pythonContent = this.thirdFormGroup.value.pythonEditor;
    const filename = `${this.firstFormGroup.value.scriptname}.py`;
    const scriptFile = new File([pythonContent],filename,{type: 'text/x-python'});
    this.scriptservice.updateScript(scriptUpdateData,scriptFile).subscribe({
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
goBack(): void {
  localStorage.removeItem('scriptDetails');
  this.router.navigate(["/script"]);
}


}
