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
import { Component } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { ScriptsService } from '../../../services/scripts.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-custom-testsuite',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule,FormsModule,],
  templateUrl: './custom-testsuite.component.html',
  styleUrl: './custom-testsuite.component.css'
})
export class CustomTestsuiteComponent {

  masterSelected = false;
  modulesArr:any[] = [];
  selected :string[] = [];
  messages = [];

  constructor(private scriptservice:ScriptsService,private router: Router){}

  ngOnInit() {
    this.masterSelected = false;
    this.getAllModule();
  }

  categoryChange(val:any){

  }

  getAllModule(){
    this.scriptservice.getModuleCustomTestSuite('RDKV').subscribe(res=>{
      console.log(res);
      this.modulesArr = JSON.parse(res);
    })
  }


  checked(item: string): boolean {
    return this.selected.includes(item);
  }
  // when checkbox change, add/remove the item from the array
  onChange(event:any, item:any){
    let checkVal = event.target.checked
    if(checkVal){
    this.selected.push(item);
    } else {
      const index = this.selected.indexOf(item);
      if (index !== -1) {
        this.selected.splice(index, 1);
      }
    }
    this.updateSelectAllCheckbox();
  }

  checkUncheckAll(event:any,) {
    const isChecked = event.target.checked;
    this.selected = isChecked ? this.modulesArr.slice() : [];
  }

  updateSelectAllCheckbox(): void {
    const selectAllCheckbox = document.querySelector('.selectall input[type="checkbox"]') as HTMLInputElement;
    selectAllCheckbox.checked = this.selected.length === this.modulesArr.length;
  }

  goBack():void{
    localStorage.removeItem('category');
    this.router.navigate(['/script']);
  }



}
