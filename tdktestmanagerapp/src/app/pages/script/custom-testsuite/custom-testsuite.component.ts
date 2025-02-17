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
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { ScriptsService } from '../../../services/scripts.service';
import { Router } from '@angular/router';
import { AuthService } from '../../../auth/auth.service';
import { DevicetypeService } from '../../../services/devicetype.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-custom-testsuite',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule,FormsModule,],
  templateUrl: './custom-testsuite.component.html',
  styleUrl: './custom-testsuite.component.css'
})
export class CustomTestsuiteComponent {

  formSubmitted = false;
  customFormGroup!:FormGroup;
  masterSelected = false;
  modulesArr:any[] = [];
  messages = [];
  getCategory!: string;
  videoCategory!:string;
  allDeviceType:any;
  selectedVideoCategory : string = 'RDKV';
  loggedinUser:any;

  constructor(private scriptservice:ScriptsService,private router: Router, private deviceTypeService:DevicetypeService,
    private fb:FormBuilder,private authservice: AuthService,private _snakebar: MatSnackBar){
      this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
    }
  /**
   * Initializes the component.
  */
  ngOnInit() :void{
    this.masterSelected = false;
    this.customFormGroup = this.fb.group({
      category:[],
      name:['', Validators.required],
      description:['', Validators.required],
      deviceType:['', Validators.required],
      longdurationtest:[],
      modules:[[], [Validators.required, this.arrayNotEmptyValidator]]
    })
   
    this.getCategory = this.loggedinUser.userCategory;
    this.getAllModule(this.getCategory);
    this.getAlldeviceType();
  }
  /**
   * Validation for empty array for module.
  */
  arrayNotEmptyValidator(control: any) {
    return Array.isArray(control.value) && control.value.length > 0 ? null : { required: true };
  }
  /**
   * category change click on radio button
  */
  categoryChange(val:any):void{
    this.selectedVideoCategory = val;
    this.getAllModule(this.selectedVideoCategory);
    this.customFormGroup.controls['modules'].setValue([]);
    this.updateSelectAllCheckbox();
  }
  /**
   * method for get all module list
  */
  getAllModule(category:string):void{
    this.scriptservice.getModuleCustomTestSuite(category).subscribe(res=>{
      this.modulesArr = JSON.parse(res);
    })
  }
  /**
   * method for get all device type list
  */  
  getAlldeviceType(): void{
    this.deviceTypeService.getfindallbycategory(this.getCategory).subscribe(res=>{
      this.allDeviceType = JSON.parse(res);
    })
  }
  /**
   * method for change device type
  */  
  devicetypeChange(event:any): void{
    let value = event.target.value;
  }
  /**
   * method for check module
  */   
  modulesChecked(item: string): boolean {
    const modules = this.customFormGroup.value.modules || [];
    return modules.includes(item);
  }
  // when checkbox change, add/remove the item from the array
  onChange(event:any, item:any):void{
    const isChecked = event.target.checked;
    let selectedModules: string[] = this.customFormGroup.value.modules || [];

    if (isChecked) {
      if (!selectedModules.includes(item)) {
        selectedModules.push(item);
      }
    } else {
      const index = selectedModules.indexOf(item);
      if (index !== -1) {
        selectedModules.splice(index, 1);
      }
    }
    this.customFormGroup.controls['modules'].setValue([...selectedModules]);
    this.updateSelectAllCheckbox();
  }
  /**
   * method for check/uncheck all module
  */ 
  checkUncheckAll(event:any) :void{
    const isChecked = event.target.checked;
    const allModules = isChecked ? [...this.modulesArr] : [];
    this.customFormGroup.controls['modules'].setValue(allModules);
  }
  /**
   * Update for check all module
  */ 
  updateSelectAllCheckbox(): void {
    const selectAllCheckbox = document.querySelector('.selectall input[type="checkbox"]') as HTMLInputElement;
    const selectedModules = this.customFormGroup.value.modules || [];
    selectAllCheckbox.checked = selectedModules.length === this.modulesArr.length;
    selectAllCheckbox.indeterminate = selectedModules.length > 0 && selectedModules.length < this.modulesArr.length;
  }
  /**
   * method for durationChecked
  */ 
  durationChecked(event:any):void{
    let duration = event.target.checked;
  }
  /**
   * Navigate to script page
  */ 
  goBack():void{
    this.router.navigate(['/script']);
  }
  /**
   * Submission for customSuite create
  */ 
  customFormSubmit():void{
    this.formSubmitted= true;
    if(this.customFormGroup.invalid){
      return
    }else{
      let obj={
        testSuiteName: this.customFormGroup.value.name,
        description:this.customFormGroup.value.description,
        deviceType:this.customFormGroup.value.deviceType,
        modules: this.customFormGroup.value.modules,
        category: this.selectedVideoCategory,
        userGroup: this.loggedinUser.userGroupName,
        longDurationScripts: this.customFormGroup.value.longdurationtest,
      }
      this.scriptservice.createCustomTestSuite(obj).subscribe({
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
  }

}
