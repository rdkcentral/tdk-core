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
import { Component} from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonFormComponent } from '../../../utility/component/common-form/common-form.component';
import { AuthService } from '../../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ScriptTagService } from '../../../services/script-tag.service';

/**
 * Component for creating a script tag.
 */
@Component({
  selector: 'app-create-script-tag',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, CommonFormComponent],
  templateUrl: './create-script-tag.component.html',
  styleUrl: './create-script-tag.component.css'
})
export class CreateScriptTagComponent {

  userGroupName: string | undefined;
  commonFormName = 'Create';
  errormessage!: string;
  validationName = 'script tag'
  placeholderName = 'ScriptTag Name'
  labelName = 'Name'
  loggedinUser: any = {};

  constructor(private router: Router, public service: ScriptTagService,
    private route: ActivatedRoute, private _snakebar: MatSnackBar, private authservice: AuthService) {
    this.commonFormName = this.route.snapshot.url[1].path === 'scripttag-create' ? this.commonFormName + ' ' + `${this.authservice.selectedConfigVal.toUpperCase()}` + ' ' + 'ScriptTag' : this.commonFormName;
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser') || '{}');

  }

  /**
   * Initializes the component.
   */
  ngOnInit(): void {
  }

  /**
   * 
   * @param name 
   */
  onFormSubmitted(name: string): void {

    let obj = {
      "scriptTagName": name,
      "scriptTagCategory": this.authservice.selectedConfigVal,
      "scriptTagUserGroup": this.loggedinUser.userGroupName
    }
    if(name !== undefined){
      this.service.createScriptTag(obj).subscribe({
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
            duration: 4000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
  
      })
    }


  }

}
