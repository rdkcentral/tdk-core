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
import { Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { FormsModule } from '@angular/forms';
import { BoxtypeService } from '../../../services/boxtype.service';
import { AuthService } from '../../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-create-boxtype',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, NgMultiSelectDropDownModule, FormsModule],
  templateUrl: './create-boxtype.component.html',
  styleUrl: './create-boxtype.component.css'
})

/**
 * Component for creating a box type.
 */
export class CreateBoxtypeComponent implements OnInit {
  [x: string]: any;
  dropdownSettings = {};
  submitted = false;
  createBoxTypeForm!: FormGroup;
  dropdownList: any;
  configureName!: string;
  selectedSubBox: any[] = []
  userGroupName: any;

  constructor(private formBuilder: FormBuilder, private router: Router,
    private service: BoxtypeService, private authservice: AuthService, private _snakebar: MatSnackBar) {
    this.userGroupName = JSON.parse(localStorage.getItem('loggedinUser') || '{}');

  }

  /**
   * Initializes the component.
   */
  ngOnInit(): void {
    this.createBoxTypeForm = this.formBuilder.group({
      boxtypeName: ['', [Validators.required, Validators.minLength(3)]],
      selectBoxtype: ['', Validators.required],
      subBoxtype: ['']
    });

    this.dropdownSettings = {
      singleSelection: false,
      idField: 'subBoxtypeId',
      textField: 'subBoxtypeName',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      itemsShowLimit: 3,
      allowSearchFilter: false,
    };
    this.service.getlistbycategory(this.authservice.selectedConfigVal).subscribe(res => {
      this.dropdownList = JSON.parse(res);

    })
    this.configureName = this.authservice.selectedConfigVal;

  }

  /**
   * Getter for the form controls.
   */
  get f() { return this.createBoxTypeForm.controls; }

  /**
   * Handles the selection of an item.
   * @param item The selected item.
   */
  onItemSelect(item: any):void {
    this.selectedSubBox.push(item);

  }

  /**
   * Handles the selection of all items.
   * @param items The selected items.
   */
  onSelectAll(items: any):void {
    this.selectedSubBox = items;
  }

  /**
   * Creates a new box type.
   */
  createBoxType() :void{
    this.submitted = true;
    if (this.createBoxTypeForm.invalid) {
      return
    } else {

      let data = {
        boxTypeName: this.createBoxTypeForm.value.boxtypeName,
        type: this.createBoxTypeForm.value.selectBoxtype,
        boxCategory: this.authservice.selectedConfigVal,
        boxUserGroup: this.userGroupName.userGroupName,
        subBoxTypes: this.selectedSubBox
      }
      this.service.createBoxType(data).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["configure/list-boxtype"]);

          }, 1000);

        },
        error: (err) => {
          let errmsg = JSON.parse(err.error);
          this._snakebar.open(errmsg.message, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
      })

    }
  }

  /**
   * Resets the form.
   */
  reset():void {
    this.createBoxTypeForm.reset();
  }

  /**
   * Navigates back to the list of box types.
   */
  goBack():void {
    this.router.navigate(["/configure/list-boxtype"]);
  }

}

