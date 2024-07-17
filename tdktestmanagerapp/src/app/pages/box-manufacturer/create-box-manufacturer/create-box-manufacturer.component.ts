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
import { Component, OnInit } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonFormComponent } from '../../../utility/component/common-form/common-form.component';
import { AuthService } from '../../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { BoxManufactureService } from '../../../services/box-manufacture.service';

@Component({
  selector: 'app-create-box-manufacturer',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, CommonFormComponent],
  templateUrl: './create-box-manufacturer.component.html',
  styleUrl: './create-box-manufacturer.component.css'
})

/**
 * Create Box Manufacturer Component
 */
export class CreateBoxManufacturerComponent implements OnInit {

  userGroupName: string | undefined;
  commonFormName = 'Create';
  errormessage!: string;
  validationName = 'box manufacturer'
  placeholderName = 'Box Manufacturer Name'
  loggedinUser: any={};

  constructor(private router: Router, public service: BoxManufactureService,
    private route: ActivatedRoute, private _snakebar: MatSnackBar, private authservice: AuthService) {
    this.commonFormName = this.route.snapshot.url[1].path === 'create-boxManufacturer' ? this.commonFormName + ' ' + `${this.authservice.selectedConfigVal.toUpperCase()}` + ' ' + 'Box Manufacturer' : this.commonFormName;
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser') || '{}');

  }

    /**
   * Initializes the component.
   */
    ngOnInit(): void {
    }

    
   /**
   * Handles the form submission event.
   * 
   * @param name - The name of the box manufacturer.
   */
  onFormSubmitted(name: string): void {
    let obj = {
      "boxManufacturerName": name,
      "boxManufacturerCategory": this.authservice.selectedConfigVal,
      "boxManufacturerUserGroup": this.loggedinUser.userGroupName
    }
    this.service.createBoxManufacture(obj).subscribe({
      next: (res) => {
        this._snakebar.open(res, '', {
          duration: 3000,
          panelClass: ['success-msg'],
          verticalPosition: 'top'
        })
        setTimeout(() => {
          this.router.navigate(["configure/list-boxManufacturer"]);

        }, 1000);

      },
      error: (err) => {
        let errmsg = JSON.parse(err.error);
        this.errormessage = errmsg.message ? errmsg.message : errmsg.password;
        this._snakebar.open(this.errormessage, '', {
          duration: 4000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
        })
      }

    })
  }




}


