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
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { MaterialModule } from '../../../material/material.module';
import { HttpClientModule } from '@angular/common/http';
import { Validators } from '@angular/forms';
import { CommonFormComponent } from '../../../utility/component/common-form/common-form.component';
import { UsergroupService } from '../../../services/usergroup.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SocVendorService } from '../../../services/soc-vendor.service';
import { AuthService } from '../../../auth/auth.service';

@Component({
  selector: 'app-edit-soc-vendor',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, HttpClientModule, MaterialModule, CommonFormComponent],
  templateUrl: './edit-soc-vendor.component.html',
  styleUrl: './edit-soc-vendor.component.css'
})
export class EditSocVendorComponent {

  record: any;
  id!: number;
  commonFormName = 'Update';
  errormessage!: string;
  validationName = 'soc vendor';
  placeholderName = 'Soc Vendor Name';
  labelName = 'Name';

  constructor(private route: ActivatedRoute, private router: Router, private _snakebar: MatSnackBar,
    public service: SocVendorService, private authservice: AuthService) {
    this.service.currentUrl = this.route.snapshot.url[1].path
    this.commonFormName = this.route.snapshot.url[1].path === 'edit-socvendor' ? this.commonFormName + ' ' + 'SoCVendor' : this.commonFormName;
  }

   /**
   * Initializes the component.
   */ 
  ngOnInit(): void {
    this.id = +this.route.snapshot.params['id'];
    this.service.currentUrl = this.id;
    let data = JSON.parse(localStorage.getItem('user') || '{}');
    this.record = data;

  }

  /**
   * Handles the form submission.
   * @param name - The name of the SOC vendor.
   */
  onFormSubmitted(name: any): void {
    let obj = {
      socVendorId: this.record.boxManufacturerId,
      socVendorName: name,
      socVendorCategory: this.authservice.selectedConfigVal
    }
    if (name !== undefined && name !== null) {
      this.service.updateSocVendor(this.record.socVendorId, obj).subscribe({
        next: (res) => {
          this._snakebar.open('Soc Vendor updated successfully', '', {
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
          this._snakebar.open(this.errormessage, 'Something went wrong', {
            duration: 3000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }

      })
    }
  }

}

