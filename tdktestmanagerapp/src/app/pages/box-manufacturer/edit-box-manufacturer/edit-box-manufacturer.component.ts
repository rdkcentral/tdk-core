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
import { BoxManufactureService } from '../../../services/box-manufacture.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';
import { UsergroupService } from '../../../services/usergroup.service';
import { CommonFormComponent } from '../../../utility/component/common-form/common-form.component';

@Component({
  selector: 'app-edit-box-manufacturer',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, CommonFormComponent],
  templateUrl: './edit-box-manufacturer.component.html',
  styleUrl: './edit-box-manufacturer.component.css'
})

/**
 * Represents the component for editing a box manufacturer.
 */
export class EditBoxManufacturerComponent implements OnInit {

  record: any;
  id!: number;
  commonFormName = 'Update';
  errormessage!: string;
  validationName = 'box manufacturer'
  placeholderName = 'Box Manufacturer Name'
  labelName = "Name";

  constructor(private route: ActivatedRoute, private router: Router,
    public service: UsergroupService, private _snakebar: MatSnackBar,
    private boxmanufactureservice: BoxManufactureService,
    private authservice: AuthService
  ) {
    this.service.currentUrl = this.route.snapshot.url[1].path
    this.commonFormName = this.route.snapshot.url[1].path === 'boxManufacturer-edit' ? this.commonFormName + ' ' + 'Box Manufacturer' : this.commonFormName;
  }

   /**
   * Initializes the component.
   * Retrieves the 'id' parameter from the route snapshot and assigns it to the 'id' property.
   * Sets the current URL in the service.
   * Retrieves the user data from local storage and assigns it to the 'record' property.
   */
  ngOnInit(): void {
    this.id = +this.route.snapshot.params['id'];
    this.service.currentUrl = this.id;
    let data = JSON.parse(localStorage.getItem('user') || '{}');
    this.record = data;
  }

    /**
   * Handles the form submission event.
   * @param name - The name of the box manufacturer.
   */
  onFormSubmitted(name: any): void {
    let obj = {
      boxManufacturerId: this.record.boxManufacturerId,
      boxManufacturerName: name,
      boxManufacturerCategory: this.authservice.selectedConfigVal
    }
    if (name != undefined && name != null) {
      this.boxmanufactureservice.updateBoxManufacture(this.record.boxManufacturerId, obj).subscribe({
        next: (res) => {
          this._snakebar.open('Box Manufacturer updated successfully', '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["configure/list-boxManufacturer"]);
          }, 1000);

        },
        error: (err) => {
          this._snakebar.open('Something went wrong', '', {
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

