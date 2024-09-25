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
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';
import { UsergroupService } from '../../../services/usergroup.service';
import { CommonFormComponent } from '../../../utility/component/common-form/common-form.component';
import { ScriptTagService } from '../../../services/script-tag.service';

/**
 * Represents the EditScriptTagComponent class.
 */
@Component({
  selector: 'app-edit-script-tag',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, CommonFormComponent],
  templateUrl: './edit-script-tag.component.html',
  styleUrl: './edit-script-tag.component.css'
})
export class EditScriptTagComponent {

  record: any;
  id!: number;
  commonFormName = 'Update';
  errormessage!: string;
  validationName = 'script tag'
  placeholderName = 'Script Tag Name'
  labelName = 'Name'

  constructor(private route: ActivatedRoute, private router: Router,
    public service: UsergroupService, private _snakebar: MatSnackBar,
    private scripttagservice: ScriptTagService,
    private authservice: AuthService
  ) {
    this.service.currentUrl = this.route.snapshot.url[1].path
    this.commonFormName = this.route.snapshot.url[1].path === 'scripttag-edit' ? this.commonFormName + ' ' + `${this.authservice.showSelectedCategory}` + ' ' + 'Script Tag' : this.commonFormName;
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
   * 
   * @param name 
   */
  onFormSubmitted(name: any): void {
    let obj = {
      scriptTagId: this.record.scriptTagId,
      scriptTagName: name,
      scriptTagCategory: this.authservice.selectedConfigVal
    }
    if (name != undefined && name != null) {
      this.scripttagservice.updateScriptTag(obj).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["configure/scripttag-list"]);
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
