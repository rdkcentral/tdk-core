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

  constructor(private authservice: AuthService,private router: Router) { }

  /**
   * Initializes the component and sets up the initial values.
   */
  ngOnInit(): void {
    this.configureName = this.authservice.selectedConfigVal;
    this.functionForm = new FormGroup({
      functionName: new FormControl<string | null>('', { validators: Validators.required }),
      module: new FormControl<string | null>('', { validators: Validators.required })
    })
    this.testGroupArr=[
      {id:1, name:'E2E'},
      {id:2, name:'Component'},
      {id:3, name:'OpenSource'},
      {id:4, name:'Certification'},
    ];
  }

  functionSubmit(){    
  }

  /**
   * Navigates back to the function list page.
   */
  goBack(){
    this.router.navigate(["/configure/function-list"]);
  }

  /**
   * Resets the function form to its initial state.
   */
  reset(){
    this.functionForm.reset();
  }

}
