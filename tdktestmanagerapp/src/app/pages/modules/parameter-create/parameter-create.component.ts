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
import { ModulesService } from '../../../services/modules.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-parameter-create',
  standalone: true,
  imports: [CommonModule, HttpClientModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './parameter-create.component.html',
  styleUrl: './parameter-create.component.css'
})
export class ParameterCreateComponent {

  configureName!:string;
  parameterForm!:FormGroup;
  paraFormSubmitted = false;
  parameterType:string[] = [];
  dynamicModuleName!:string;
  dynamicFunctionName!:string;

  constructor(private authservice: AuthService,private router: Router,
    private moduleservice: ModulesService,private _snakebar :MatSnackBar,
  ) { }

  /**
   * Initializes the component and sets up the initial state.
   */
  ngOnInit(): void {
    let functiondata = JSON.parse(localStorage.getItem('function') || '{}');
    this.dynamicModuleName = functiondata.moduleName;
    this.dynamicFunctionName = functiondata.functionName;
    this.configureName = this.authservice.selectedConfigVal;
    this.parameterForm = new FormGroup({
      parameterName: new FormControl<string | null>('', { validators: Validators.required }),
      module: new FormControl<string | null>({value: this.dynamicModuleName, disabled: true}, { validators: Validators.required }),
      function: new FormControl<string | null>({value: this.dynamicFunctionName, disabled: true}, { validators: Validators.required }),
      parameterType: new FormControl<string | null>('', { validators: Validators.required }),
      rangeVal: new FormControl<string | null>('', { validators: Validators.required })
    })

    this.moduleservice.getListOfParameterEnums().subscribe((data) => {
      this.parameterType = JSON.parse(data);
      
    })
  }

  /**
   * Handles the form submission for creating a parameter.
   */
  parameterFormSubmit():void{
    this.paraFormSubmitted = true;
    if(this.parameterForm.invalid){
      return;
    }else{
      let parameterObj = {
        parameterName: this.parameterForm.value.parameterName,
        parameterDataType: this.parameterForm.value.parameterType,
        parameterRangeVal: this.parameterForm.value.rangeVal,
        function: this.dynamicFunctionName,
      }
      
      this.moduleservice.createParameter(parameterObj).subscribe({
        next:(res)=>{
          this._snakebar.open(res, '', {
          duration: 2000,
          panelClass: ['success-msg'],
          verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["/configure/parameter-list"]);
          }, 2000);
        },
        error:(err)=>{
          this._snakebar.open(err, '', {
            duration: 3000,
            panelClass: ['error-msg'],
            verticalPosition: 'top'
          })
        }
      })
    }
  }

  /**
   * Navigates back to the parameter list page.
   */
  goBack(){
    this.router.navigate(["/configure/parameter-list"]);
  }

  /**
   * Resets the parameter form to its initial state.
   */
  reset(){
    this.parameterForm.reset();
  }


}
