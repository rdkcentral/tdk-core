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
import { RdkVersionsService } from '../../../services/rdk-versions.service';

@Component({
  selector: 'app-edit-rdk-versions',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, CommonFormComponent],
  templateUrl: './edit-rdk-versions.component.html',
  styleUrl: './edit-rdk-versions.component.css'
})
export class EditRdkVersionsComponent {

  record: any;
  id!: number;
  commonFormName = 'Update';
  errormessage!: string;
  validationName = 'rdk version'
  placeholderName = 'RDKVersions Name'
  labelName = 'Build Version'

  constructor(private route: ActivatedRoute, private router: Router, private _snakebar: MatSnackBar,
    public service: RdkVersionsService, private authservice: AuthService) {
    this.service.currentUrl = this.route.snapshot.url[1].path
    this.commonFormName = this.route.snapshot.url[1].path === 'edit-rdkversions' ? this.commonFormName + ' ' + 'RDKVersions' : this.commonFormName;
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
      rdkVersionId: this.record.rdkVersionId,
      buildVersionName: name,
      rdkVersionCategory: this.authservice.selectedConfigVal
    }
    if (name != undefined && name != null) {
      this.service.updateRdkVersion(obj).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["configure/list-rdkversions"]);
          }, 1000);

        },
        error: (err) => {
          let errmsg = JSON.parse(err.error);
          this.errormessage = errmsg.message ? errmsg.message : errmsg.password;
          this._snakebar.open(this.errormessage, '', {
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
