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
  testGroupArr:testGroupModel[] = [];

  constructor(private authservice: AuthService,private router: Router) { }

  /**
   * Initializes the component and sets up the initial state.
   */
  ngOnInit(): void {
    this.configureName = this.authservice.selectedConfigVal;
    this.parameterForm = new FormGroup({
      parameterName: new FormControl<string | null>('', { validators: Validators.required }),
      module: new FormControl<string | null>('', { validators: Validators.required }),
      function: new FormControl<string | null>('', { validators: Validators.required }),
      parameterType: new FormControl<string | null>('', { validators: Validators.required }),
      rangeVal: new FormControl<string | null>('', { validators: Validators.required })
    })
    this.testGroupArr=[
      {id:1, name:'E2E'},
      {id:2, name:'Component'},
      {id:3, name:'OpenSource'},
      {id:4, name:'Certification'},
    ];
  }

  /**
   * Handles the form submission for creating a parameter.
   */
  parameterFormSubmit(){
    
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
