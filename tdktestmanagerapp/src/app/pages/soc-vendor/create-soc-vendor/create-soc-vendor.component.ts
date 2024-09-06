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
import { SocVendorService } from '../../../services/soc-vendor.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-create-soc-vendor',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, CommonFormComponent],
  templateUrl: './create-soc-vendor.component.html',
  styleUrl: './create-soc-vendor.component.css'
})
export class CreateSocVendorComponent {

  socVendorName: string | undefined;
  commonFormName = 'Create';
  loggedinUser: any={};
  errormessage!: string;
  validationName = 'soc vendor';
  placeholderName = 'Soc Vendor Name';
  labelName = 'Name';
  
  constructor(private router: Router, private route: ActivatedRoute, public service: SocVendorService,
    private _snakebar: MatSnackBar, private authservice: AuthService) {
    this.commonFormName = this.route.snapshot.url[1].path === 'create-socvendor' ? this.commonFormName + ' ' + `${this.authservice.selectedConfigVal.toUpperCase()}` + ' ' + 'SoCVendor' : this.commonFormName;
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
  }

  /**
   * Handles the form submission event.
   * @param name - The SOC vendor name.
   */
  onFormSubmitted(name: string): void {
    let obj = {
      "socVendorName": name,
      "socVendorCategory": this.authservice.selectedConfigVal,
      "socVendorUserGroup": this.loggedinUser.userGroupName
    }
    if(name !== undefined && name !== null){
      this.service.createSocVendor(obj).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["configure/list-socvendor"]);
  
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

  /**
   * Initializes the component.
   */  
  ngOnInit(): void {
  }

}
