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
import { Component, inject, signal } from '@angular/core';
import { MaterialModule } from '../../../material/material.module';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../auth/auth.service';
import { testGroupModel } from '../../models/manageusermodel';
import { Router } from '@angular/router';
import { MatChipInputEvent } from '@angular/material/chips';
import { LiveAnnouncer } from '@angular/cdk/a11y';

@Component({
  selector: 'app-modules-create',
  standalone: true,
  imports: [CommonModule, HttpClientModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './modules-create.component.html',
  styleUrl: './modules-create.component.css'
})
export class ModulesCreateComponent {

  configureName!:string;
  createModuleForm!:FormGroup;
  moduleFormSubmitted = false;
  testGroupArr:testGroupModel[] = [];
  crashFilesArr: string[] = [];
  logFilesArr: string[] = [];
  isThunder :boolean = false;


  constructor(private authservice: AuthService,private router: Router) { }

  /**
   * Initializes the component and sets up the initial values.
   */
  ngOnInit(): void {
    this.configureName = this.authservice.selectedConfigVal;
    this.testGroupArr=[
      {id:1, name:'E2E'},
      {id:2, name:'Component'},
      {id:3, name:'OpenSource'},
      {id:4, name:'Certification'},
    ];
    this.createModuleForm = new FormGroup({
      moduleName: new FormControl<string | null>('', { validators: Validators.required }),
      testGroup: new FormControl<string | null>('', { validators: Validators.required }),
      executionTime: new FormControl<string | null>('', { validators: Validators.required }),
      thundrShowHide: new FormControl<boolean | null>({value: false, disabled: false}),
      crashFiles: new FormControl<string | null>(''),
      logFiles: new FormControl<string | null>('')
    })
  }

  moduleSubmit():void{
  }

  /**
   * Navigates back to the modules list page.
   */
  goBack():void{
    this.router.navigate(["/configure/modules-list"]);
  }

  /**
   * Resets the createModuleForm to its initial state.
   */
  reset():void{
    this.createModuleForm.reset();
  }

  /**
   * Toggles the value of `thundrEnable` property.
   * @param event - The event object triggered by the checkbox.
   */
  thundrEnable(event: any):void{
    const inputEle = event.target as HTMLInputElement;
    this.isThunder = inputEle.checked;
  }

  /**
   * Removes a crash file from the `crashFilesArr` array at the specified index.
   * @param index - The index of the crash file to remove.
   */
  removeCrash(index: number):void {
    this.crashFilesArr.splice(index, 1);
  }
  /**
   * Removes a log file from the logFilesArr array at the specified index.
   * @param index - The index of the log file to remove.
   */
  removeLogs(index: number):void {
    this.logFilesArr.splice(index, 1);
  }
  /**
   * Adds a crash file to the `crashFilesArr` array.
   */
  addCrash(): void {
    const value = this.createModuleForm.get('crashFiles')?.value.trim();
    if (value) {
      this.crashFilesArr.push(value);
      this.createModuleForm.get('crashFiles')?.setValue('');
    }
  
  }
  /**
   * Adds logs to the logFilesArr array.
   */
  addLogs(): void {
    const value = this.createModuleForm.get('logFiles')?.value.trim();
    if (value) {
      this.logFilesArr.push(value);
      this.createModuleForm.get('logFiles')?.setValue('');
    }
  }



}
