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
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { AuthService } from '../../../auth/auth.service';
import { Router } from '@angular/router';
import { testGroupModel } from '../../models/manageusermodel';
import { ModulesService } from '../../../services/modules.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-function-create',
  standalone: true,
  imports: [CommonModule, HttpClientModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './function-create.component.html',
  styleUrl: './function-create.component.css'
})
export class FunctionCreateComponent {

  configureName!:string;
  functionForm!:FormGroup;
  functionFormSubmitted = false;
  testGroupArr:testGroupModel[] = [];
  dynamicModuleName!: string;

  constructor(private authservice: AuthService,private router: Router,
    private moduleservice: ModulesService,private _snakebar :MatSnackBar,
  ) { }

  /**
   * Initializes the component and sets up the initial values.
   */
  ngOnInit(): void {
    let data = JSON.parse(localStorage.getItem('modules') || '{}');
    this.dynamicModuleName = data.moduleName;
    this.configureName = this.authservice.selectedConfigVal;
    this.functionForm = new FormGroup({
      functionName: new FormControl<string | null>('', { validators: Validators.required }),
      moduleName: new FormControl<string | null>({value: this.dynamicModuleName, disabled: true}, { validators: Validators.required}),
    })
  }
  /**
   * This method is Submit the create function form.
   */
  functionSubmit():void{    
    this.functionFormSubmitted = true;
    if(this.functionForm.invalid){
      return;
    }else{
      let functionObj = {
        functionName: this.functionForm.value.functionName,
        moduleName: this.dynamicModuleName,
        functionCategory: this.configureName
      }
      this.moduleservice.createFunction(functionObj).subscribe({
        next:(res)=>{
          this._snakebar.open(res, '', {
          duration: 3000,
          panelClass: ['success-msg'],
          verticalPosition: 'top'
          })
          setTimeout(() => {
            this.functionForm.reset();
            this.router.navigate(["/configure/function-list"]);
          }, 1000);
        },
        error:(err)=>{
          this._snakebar.open(err.message, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
      });
    }
  }

  /**
   * Navigates back to the function list page.
   */
  goBack():void{
    this.router.navigate(["/configure/function-list"]);
  }

  /**
   * Resets the function form to its initial state.
   */
  reset():void{
    this.functionForm.reset();
  }

}
