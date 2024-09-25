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
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../auth/auth.service';
import { BoxtypeService } from '../../../services/boxtype.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpResponse } from '@angular/common/http';


@Component({
  selector: 'app-edit-box-type',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, NgMultiSelectDropDownModule, FormsModule],
  templateUrl: './edit-box-type.component.html',
  styleUrl: './edit-box-type.component.css'
})

/**
 * Component for editing a box type.
 */
export class EditBoxTypeComponent {

  selectedItems: { item_id: number, item_text: string }[] = [];
  dropdownSettings = {};
  submitted = false;
  updateBoxTypeForm!: FormGroup;
  dropdownList: any;
  configureName!: string;
  user: any;
  selectedSubBox: any[] = []
  categoryName!: string;

  constructor(private formBuilder: FormBuilder, private router: Router,
    private authservice: AuthService, private service: BoxtypeService, private _snakebar: MatSnackBar) {
    this.user = JSON.parse(localStorage.getItem('user') || '{}');
    if (!this.user) {
      this.router.navigate(['configure/list-boxtype']);
    }
  }

  /**
   * Lifecycle hook called after component initialization.
   */  
  ngOnInit(): void {

    this.updateBoxTypeForm = this.formBuilder.group({
      boxtypeName: [this.user.boxTypeName, [Validators.required, Validators.minLength(4)]],
      selectBoxtype: [this.user.type, Validators.required],
      subBoxtype: [this.user.subBoxTypes]
    });

    this.dropdownSettings = {
      singleSelection: false,
      idField: 'item_id',
      textField: 'item_text',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      itemsShowLimit: 3,
      allowSearchFilter: false,
    };
    this.configureName = this.authservice.selectedConfigVal;
    this.categoryName = this.authservice.showSelectedCategory;
    this.getSubboxList();
  }

  /**
   * Getter for updateBoxTypeForm controls.
   */
  get f() { return this.updateBoxTypeForm.controls; }

  /**
   * Event handler for selecting an item.
   * @param item The selected item.
   */
  onItemSelect(item: any):void {
    this.selectedSubBox.push(item);

  }

  /**
   * Event handler for selecting all items.
   * @param items The selected items.
   */
  onSelectAll(items: any):void {
    this.selectedSubBox = items;
  }

  /**
   * Retrieves the list of sub boxes.
   */  
  getSubboxList():void {
    let category = this.user.boxCategory;
    this.service.getSubboxList(category.toUpperCase(), this.user.boxTypeName).subscribe(res => {
      this.dropdownList = JSON.parse(res);
    })
  }

  /**
   * Updates the box type.
   */
  updateBoxType():void {
    this.submitted = true;
    if (this.updateBoxTypeForm.invalid) {
      return
    } else {
      let data = {
        boxTypeName: this.updateBoxTypeForm.value.boxtypeName,
        boxType: this.updateBoxTypeForm.value.selectBoxtype,
        boxTypeCategory: this.user.boxCategory.toUpperCase(),
        subBoxTypes: this.updateBoxTypeForm.value.subBoxtype,
      }
      this.service.updateBoxType(this.user.boxTypeId, data).subscribe({
        next: (res:HttpResponse<any>) => {
          if(res){
            this._snakebar.open('Boxtype Update Successfully', '', {
              duration: 3000,
              panelClass: ['success-msg'],
              verticalPosition: 'top'
            })
            setTimeout(() => {
              this.router.navigate(["configure/list-boxtype"]);
            }, 1000);
          }
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
   * Resets the update box type form.
   */
  reset() :void{
    this.updateBoxTypeForm.reset()
  }

  /**
   * Navigates back to the list of box types.
   */
  goBack():void {
    this.router.navigate(["configure/list-boxtype"]);
  }

}
