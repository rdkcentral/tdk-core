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
import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../material/material.module';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-app-upgrade',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './app-upgrade.component.html',
  styleUrl: './app-upgrade.component.css'
})
export class AppUpgradeComponent {

  appSubmitted = false;
  appForm!: FormGroup;

  /**
   * Constructor for AppUpgradeComponent
   * @param router - Router instance
   * @param _snakebar - MatSnackBar for notifications
   */
  constructor(private router: Router,
    private _snakebar: MatSnackBar
  ) { }


  /**
   * Initializes the component.
   */
  ngOnInit(): void {
    this.appForm = new FormGroup({
      backendWar: new FormControl<string | null>('', { validators: [Validators.required] }),
      dbPassword: new FormControl<string | null>('', { validators: [Validators.required] }),
      databaseFile: new FormControl<string | null>('', { validators: [Validators.required]}),
      backup: new FormControl<string | null>('', { validators: [Validators.required]})
    })
  }


  /**
   * Navigates back to the previous page.
   */
  goBack() :void{
    this.router.navigate(["/configure"]);
  }


  /**
   * Handles app upgrade form submission
   */
  onAppSubmit(){
    this.appSubmitted = true;
    if(this.appForm.invalid){
      return
    }else{
      console.log(this.appForm.value);
    }

  }

}
