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
import { Component, Inject } from '@angular/core';
import { MaterialModule } from '../../../material/material.module';
import { ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-parameter-view',
  standalone: true,
  imports: [CommonModule, HttpClientModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './parameter-view.component.html',
  styleUrl: './parameter-view.component.css'
})
export class ParameterViewComponent {

  constructor(
    public dialogRef: MatDialogRef<ParameterViewComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) {
    }

  onCancelDelete(): void {
    this.dialogRef.close(false); 
  }
  
}
