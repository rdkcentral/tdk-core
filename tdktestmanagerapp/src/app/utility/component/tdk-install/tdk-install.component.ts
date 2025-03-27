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
import { Component, Inject } from '@angular/core';
import { MaterialModule } from '../../../material/material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-tdk-install',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, MaterialModule],
  templateUrl: './tdk-install.component.html',
  styleUrl: './tdk-install.component.css'
})
export class TdkInstallComponent {

  selectedPackage = 'TDK';
  packageNames: string[] = ['Package name 1', 'Package name 2', 'Package name 3', 'Package name 4', 'Package name 5'];
  selectedPackages: { [key: string]: boolean } = {};
  selectedList: string[] = [];

  constructor(
    public dialogRef: MatDialogRef<TdkInstallComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, 
  ) {
    
  }
  onTabClick(event:any){
    let label = event.tab.textLabel
    console.log(label);
    this.selectedPackage = label;
  }
  packageChange(value:string){
    console.log(value);
  }
  onCheckboxChange(name: string, event: Event) {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) {
      this.selectedList.push(name);
    } else {
      this.selectedList = this.selectedList.filter(n => n !== name);
    }
  }
  close(){
    this.dialogRef.close(false);
  }
}
