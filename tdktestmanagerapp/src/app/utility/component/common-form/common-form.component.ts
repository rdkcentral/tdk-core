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
import { HttpClientModule } from '@angular/common/http';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../../auth/auth.service';
import { UsergroupService } from '../../../services/usergroup.service';

@Component({
  selector: 'app-common-form',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule],
  templateUrl: './common-form.component.html',
  styleUrl: './common-form.component.css'
})
export class CommonFormComponent implements OnChanges{
  @Output() formSubmitted = new EventEmitter<any>();
  @Input() initialValue: any;
  @Input() isEdit = false;
  @Input() formTitle:any
  @Input()validationName:any;
  @Input()placeholderName:any;
  createUpdateForm!: FormGroup;
  user:any;
  

  constructor(private fb: FormBuilder,private router: Router,
    private route:ActivatedRoute, private authservice:AuthService,
    public usergroupService:UsergroupService
  ) {
    this.createUpdateForm = this.fb.group({
      name: ['', Validators.required],
    });
  }


  ngOnChanges(changes: SimpleChanges) {
    if(this.route.snapshot.url[1].path ==='group-edit'){
      if (changes['initialValue'] && this.initialValue) {
        this.createUpdateForm.controls['name'].patchValue(this.initialValue.userGroupName);
      }
    }
    if(this.route.snapshot.url[1].path ==='boxManufacturer-edit'){
      if (changes['initialValue'] && this.initialValue) {
        this.createUpdateForm.controls['name'].patchValue(this.initialValue.boxManufacturerName);
      }
    }
    if(this.route.snapshot.url[1].path ==='edit-socvendor'){
      if (changes['initialValue'] && this.initialValue) {
        this.createUpdateForm.controls['name'].patchValue(this.initialValue.socVendorName);
      }
    }

  }
  onSubmit(): void {
    if (this.createUpdateForm.invalid) {
      return
    }else{
      this.formSubmitted.emit(this.createUpdateForm.value.name);
    }
  }
  goBack(){
    if(this.route.snapshot.url[1].path ==='group-add' || this.route.snapshot.url[1].path ==='group-edit'){
      this.router.navigate(['configure/create-group']);
    }
    if(this.route.snapshot.url[1].path ==='create-boxManufacturer'|| this.route.snapshot.url[1].path === 'boxManufacturer-edit'){
      this.router.navigate(['configure/list-boxManufacturer']);
    }
    if(this.route.snapshot.url[1].path ==='create-socvendor'|| this.route.snapshot.url[1].path === 'edit-socvendor'){
      this.router.navigate(['configure/list-socvendor']);
    }

  }
  reset(){
    this.formSubmitted.emit(this.createUpdateForm.reset());
  }

}
