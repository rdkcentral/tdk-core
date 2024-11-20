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
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RdkService } from '../../../services/rdk-certification.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { MonacoEditorModule } from '@materia-ui/ngx-monaco-editor';

@Component({
  selector: 'app-edit-rdk-certification',
  standalone: true,
  imports: [ReactiveFormsModule, MonacoEditorModule, CommonModule],
  templateUrl: './edit-rdk-certification.component.html',
  styleUrl: './edit-rdk-certification.component.css'
})
export class EditRdkCertificationComponent {

  certificationFormGroup!:FormGroup;
  editorOptions = { theme: 'vs-dark', language: 'python' };
  submitted = false;
  user: any;

  constructor(private fb : FormBuilder, private service: RdkService, private _snakebar: MatSnackBar, private router: Router){
    this.user = JSON.parse(localStorage.getItem('user') || '{}');
    if (!this.user) {
      this.router.navigate(['configure/list-rdk-certifications']);
    }
  }
  ngOnInit(): void {
    this.certificationFormGroup = this.fb.group({
      fileName: [this.user.name, Validators.required],
      pythonEditor: [ '', Validators.required]
    });
    const fileName = this.certificationFormGroup.get('fileName')?.value
    this.service.getFileContent(fileName).subscribe({
      next:(res)=>{
        const blob = new Blob([res.content], { type: res.content.type || 'text/plain' });
        console.log("Content",blob);
        blob.text().then((text) => {
          this.certificationFormGroup.get('pythonEditor')?.setValue(text);
        });
      },
      error:(err)=>{
        let errmsg = err.error;
        this._snakebar.open(errmsg, '', {
        duration: 2000,
        panelClass: ['err-msg'],
        horizontalPosition: 'end',
        verticalPosition: 'top'
        })
      }
    })
    
  }

  onSubmit(){
    const pythonContent = this.certificationFormGroup.value.pythonEditor;
    console.log("Content",pythonContent);
    const filename = `${this.certificationFormGroup.value.fileName}.py`;
    const scriptFile = new File([pythonContent],filename,{type: 'text/x-python'});
    console.log("Script File",scriptFile);
    this.service.createScript(scriptFile).subscribe({
      next: (res) => {
        this._snakebar.open('Config file updated sucessfully', '',{
          duration: 2000,
          panelClass: ['success-msg'],
          verticalPosition: 'top'
        })
        setTimeout(() => {
          this.router.navigate(["/configure/list-rdk-certifications"]);
        }, 1000);
      },
      error: (err) => {
        let errmsg =JSON.parse(err.error) ;
        this._snakebar.open(errmsg, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
      })
    }
  })
  }

  goBack():void {
    this.router.navigate(["configure/list-rdk-certifications"]);
  }

}
