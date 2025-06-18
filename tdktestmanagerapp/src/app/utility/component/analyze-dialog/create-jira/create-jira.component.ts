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
import { ApplicationRef, ChangeDetectorRef, Component, Inject, NgZone } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../../../material/material.module';
import { AnalysisService } from '../../../../services/analysis.service';

@Component({
  selector: 'app-create-jira',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './create-jira.component.html',
  styleUrl: './create-jira.component.css',
})
export class CreateJiraComponent {
  jiraSubmitted = false;
  jiraCreateForm!: FormGroup;
  loggedinUser: any;
  allProjectNames: any[] = [];
  allPriorites:any;
  allLabels:any;
  allReleaseVersion:any;
  allHardwares:any;
  allImpPlatforms:any;
  allFixVersion:any;
  allServerities:any;
  allCompImpacted:any;
  ticketDetailsOBJ:any;
  setReproduce:any;
  isPlatFormProject:any;
  showHardware = false;
  showCompImpacted = false;
  showReproduce = false;
  showFixVersion = false;
  showReleaseVersion = false;
  showEveSetup = false;
  showdependency = false;
  showSeverites = false;
  showPlatform = false;
  showReproducibitity = false;
  showAdditionalFields = false;
  showTDKVersion = false;

  constructor(
    public dialogRef: MatDialogRef<CreateJiraComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private analysiservice: AnalysisService,
    private fb: FormBuilder,
    private _snakebar: MatSnackBar,
    public jiraCreateDialog: MatDialog,
    private cdRef: ChangeDetectorRef,
    private appRef: ApplicationRef,
    private ngZone: NgZone
  ) {
    this.loggedinUser = JSON.parse(
      localStorage.getItem('loggedinUser') || '{}'
    );
    console.log(data);
    
  }

  ngOnInit(): void {
    this.formInitial();
    this.listProjectNAmes();
    this.listPriorities();
    this.ListLabels();
    this.releaseVersions();
    this.ticketDetails();
    this.getHardwareDetails();
    this.getImpPlatforms();
    this.getFixedVersions();
    this.getAllServerities();
    this.getAllCompImpacted();
    this.getSetpstoReproduce();
  }

  formInitial(){
    // if(this.ticketDetailsOBJ){
      this.jiraCreateForm = this.fb.group({
        projectname: ['' ,Validators.required],
        summary: ['',Validators.required],
        imageversion:['',Validators.required],
        description: ['',Validators.required],
        version: ['',Validators.required],
        hardware: ['',Validators.required],
        impacted: ['',Validators.required],
        reproduce: ['',Validators.required],
        fixversion: ['',Validators.required],
        exelogs: [''],
        devlogs: [''],
        issuetype: ['BUG' ,Validators.required],
        priority: ['',Validators.required],
        label: ['',Validators.required],
        releaseversion: ['',Validators.required],
        reproducibitity:['',Validators.required],
        setup: ['',Validators.required],
        dependency: [{value: 'YES', disabled: false},Validators.required],
        severities: ['',Validators.required],
        platforms: ['',Validators.required],
        user: ['',Validators.required],
        password: ['',Validators.required],
      });
    this.validationBasedonProject();

  }

  validationBasedonProject(){
    this.jiraCreateForm.get('projectname')?.valueChanges.subscribe(value => {
      this.showAdditionalFields = value === 'false';

      if (this.showAdditionalFields) {
        this.addRequiredValidators();
      } else {
        this.removeAdditionalValidators();
      }
      this.jiraCreateForm.updateValueAndValidity();
    });
  }
  addRequiredValidators() {
    const additionalFields = [
      'hardware', 'impacted', 'reproduce', 'fixversion', 'version',
      'releaseversion', 'reproducibitity', 'setup',
      'dependency', 'severities', 'platforms', 
    ];

    additionalFields.forEach(field => {
      this.jiraCreateForm.get(field)?.addValidators(Validators.required);
      this.jiraCreateForm.get(field)?.updateValueAndValidity();
    });
  }
  removeAdditionalValidators() {
    const additionalFields = [
      'hardware', 'impacted', 'reproduce', 'fixversion','version',
      'releaseversion', 'reproducibitity', 'setup',
      'dependency', 'severities', 'platforms', 
    ];
    additionalFields.forEach(field => {
      this.jiraCreateForm.get(field)?.clearValidators();
      this.jiraCreateForm.get(field)?.updateValueAndValidity();
    });
  }
  listProjectNAmes() {
    this.analysiservice.getProjectNames().subscribe((res) => {
      this.allProjectNames = res.data;
    });
  }

  listPriorities(){
    this.analysiservice.getPriorities().subscribe((res) => {
      this.allPriorites = res.data;
    });
  }
  ListLabels(){
    this.analysiservice.ListOfLabels().subscribe((res) => {
      this.allLabels = res.data
    });
  }
  releaseVersions(){
    this.analysiservice.getReleaseVersions().subscribe((res) => {
      this.allReleaseVersion = res.data;
    });
  }
  getHardwareDetails(){
    this.analysiservice.getHardware().subscribe((res) => {
      this.allHardwares = res.data;
    });
  }
  ticketDetails(){
    this.analysiservice.ticketDetails(this.data.executionResultID).subscribe((res) => {
      let details = res.data
      console.log(details);
      this.ticketDetailsOBJ = details;
      if(this.ticketDetailsOBJ){
        this.jiraCreateForm.patchValue({
          imageversion: this.ticketDetailsOBJ.imageVersion || '',
          description: this.ticketDetailsOBJ.description
        });
      }
    });
  }
  getSetpstoReproduce(){
    this.analysiservice.setpstoReproduce(this.data.name).subscribe((res) => {
      let reproduce = res;
      console.log(reproduce);
      this.setReproduce = reproduce;
      if(this.setReproduce){
        this.jiraCreateForm.patchValue({
          reproduce: this.setReproduce|| ''
        });
      }
    });
  }

  getImpPlatforms(){
    this.analysiservice.getImpactedPlatforms().subscribe((res) => {      
      this.allImpPlatforms = res.data;
    });
  }

  getFixedVersions(){
    this.analysiservice.getFixedInVersions().subscribe((res) => {
      this.allFixVersion = res.data;
    });
  }

  getAllServerities(){
    this.analysiservice.getSeverities().subscribe((res) => {
      this.allServerities = res.data
    });
  }
  getAllCompImpacted(){
    this.analysiservice.getComponentsImpacted().subscribe((res) => {
      this.allCompImpacted = res.data;
    });
  }
  onProjectChange(event:any){
    let name = event.target.value;
    console.log(name);
    this.jiraCreateForm.controls['priority'].setValidators([Validators.required]);
    this.jiraCreateForm.controls['user'].setValidators([Validators.required]);
    this.jiraCreateForm.controls['password'].setValidators([Validators.required]);
    this.analysiservice.isPlatform(name).subscribe(res=>{
      this.isPlatFormProject = res.data;
      this.ngZone.run(() => {
        this.cdRef.detectChanges();
    });
    if(this.isPlatFormProject === false){
        this.showHardware = false;
        this.showCompImpacted = false;
        this.showReproduce = false;
        this.showFixVersion = false;
        this.showReleaseVersion = false;
        this.showEveSetup = false;
        this.showdependency = false;
        this.showSeverites = false;
        this.showPlatform = false;
        this.showReproducibitity = false;
        this.showTDKVersion = false;

      }else{
        this.showHardware = true;
        this.showCompImpacted = true;
        this.showReproduce = true;
        this.showFixVersion = true;
        this.showReleaseVersion = true;
        this.showEveSetup = true;
        this.showdependency = true;
        this.showSeverites = true;
        this.showPlatform = true;
        this.showReproducibitity = true;
        this.showTDKVersion = true;

        if (this.showTDKVersion) {
          this.jiraCreateForm.controls['version'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['version'].clearValidators();
          this.jiraCreateForm.controls['version'].setValue('');
        }
        if (this.showReproducibitity) {
          this.jiraCreateForm.controls['reproducibitity'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['reproducibitity'].clearValidators();
          this.jiraCreateForm.controls['reproducibitity'].setValue('');
        }
        if (this.showPlatform) {
          this.jiraCreateForm.controls['platforms'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['platforms'].clearValidators();
          this.jiraCreateForm.controls['platforms'].setValue('');
        }
        if (this.showSeverites) {
          this.jiraCreateForm.controls['severities'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['severities'].clearValidators();
          this.jiraCreateForm.controls['severities'].setValue('');
        }
        if (this.showdependency) {
          this.jiraCreateForm.controls['dependency'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['dependency'].clearValidators();
          this.jiraCreateForm.controls['dependency'].setValue('');
        }
        if (this.showEveSetup) {
          this.jiraCreateForm.controls['setup'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['setup'].clearValidators();
          this.jiraCreateForm.controls['setup'].setValue('');
        }
        if (this.showReleaseVersion) {
          this.jiraCreateForm.controls['releaseversion'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['releaseversion'].clearValidators();
          this.jiraCreateForm.controls['releaseversion'].setValue('');
        }
        if (this.showFixVersion) {
          this.jiraCreateForm.controls['fixversion'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['fixversion'].clearValidators();
          this.jiraCreateForm.controls['fixversion'].setValue('');
        }
        if (this.showReproduce) {
          this.jiraCreateForm.controls['reproduce'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['reproduce'].clearValidators();
          this.jiraCreateForm.controls['reproduce'].setValue('');
        }
        if (this.showCompImpacted) {
          this.jiraCreateForm.controls['impacted'].setValidators([Validators.required]);
        } else {
          this.jiraCreateForm.controls['impacted'].clearValidators();
          this.jiraCreateForm.controls['impacted'].setValue('');
        }
        if (this.showHardware) {
          this.jiraCreateForm.controls['hardware'].setValidators([Validators.required]);
        } 
        else {
          this.jiraCreateForm.controls['hardware'].clearValidators();
          this.jiraCreateForm.controls['hardware'].setValue('');
        }


        this.jiraCreateForm.controls['version'].updateValueAndValidity();
        this.jiraCreateForm.controls['reproducibitity'].updateValueAndValidity();
        this.jiraCreateForm.controls['platforms'].updateValueAndValidity();
        this.jiraCreateForm.controls['severities'].updateValueAndValidity();
        this.jiraCreateForm.controls['dependency'].updateValueAndValidity();
        this.jiraCreateForm.controls['setup'].updateValueAndValidity();
        this.jiraCreateForm.controls['hardware'].updateValueAndValidity();
        this.jiraCreateForm.controls['impacted'].updateValueAndValidity();
        this.jiraCreateForm.controls['fixversion'].updateValueAndValidity();
        this.jiraCreateForm.controls['releaseversion'].updateValueAndValidity();
      }
    })

  }
  onJiraSubmit() {
    this.jiraSubmitted = true;

    if (this.jiraCreateForm.invalid) {
      this.jiraCreateForm.markAllAsTouched();
      return ;
    } else {
      if(this.isPlatFormProject == false){
        let createObj = {
          "executionResultId": this.data.executionResultID,
          "projectName": this.jiraCreateForm.value.projectname,
          "issueSummary": this.jiraCreateForm.value.summary,
          "imageVersion":this.jiraCreateForm.value.imageversion,
          "issueDescription": this.jiraCreateForm.value.description,
          "issueType": this.jiraCreateForm.value.issuetype,
          "priority": this.jiraCreateForm.value.priority,
          "label": this.jiraCreateForm.value.label,
          "user": this.jiraCreateForm.value.user,
          "password": this.jiraCreateForm.value.password,
          "deviceLogRequired": this.jiraCreateForm.value.devlogs,
          "executionLogRequired": this.jiraCreateForm.value.exelogs,
        }
        this.analysiservice.createJira(createObj).subscribe({
          next:(res)=>{
            this._snakebar.open(res.data, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              verticalPosition: 'top'
            })
            setTimeout(() => {
            this.close();
            }, 2000);
          },
          error: (err) => {
      
              this._snakebar.open(err.message, '', {
                duration: 4000,
                panelClass: ['err-msg'],
                horizontalPosition: 'end',
                verticalPosition: 'top'
              });
            
          }
        })
      }else{
        let createObj = {
          "executionResultId": this.data.executionResultID,
          "projectName": this.jiraCreateForm.value.projectname,
          "issueSummary": this.jiraCreateForm.value.summary,
          "issueDescription": this.jiraCreateForm.value.description,
          "issueType": this.jiraCreateForm.value.issuetype,
          "priority": this.jiraCreateForm.value.priority,
          "label": this.jiraCreateForm.value.label,
          "releaseVersion": this.jiraCreateForm.value.releaseversion,
          "hardwareConfig": this.jiraCreateForm.value.hardware,
          "impactedPlatforms": this.jiraCreateForm.value.platforms,
          "environmentForTestSetup": this.jiraCreateForm.value.setup,
          "reproducability":this.jiraCreateForm.value.reproducibitity,
          "stepsToReproduce": this.jiraCreateForm.value.reproduce,
          "componentsImpacted": this.jiraCreateForm.value.impacted,
          "fixedInVersion": this.jiraCreateForm.value.fixversion,
          "thirdPartyDependency": this.jiraCreateForm.value.dependency,
          "severity": this.jiraCreateForm.value.severities,
          "rdkVersion": this.jiraCreateForm.value.label,
          "tdkVersion": this.jiraCreateForm.value.version,
          "user": this.jiraCreateForm.value.user,
          "password": this.jiraCreateForm.value.password,
          "deviceLogRequired": this.jiraCreateForm.value.devlogs,
          "executionLogRequired": this.jiraCreateForm.value.exelogs,
        }
        this.analysiservice.createJira(createObj).subscribe({
          next:(res)=>{
            this._snakebar.open(res.data, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              verticalPosition: 'top'
            })
            setTimeout(() => {
            this.close();
            }, 2000);
          },
          error: (err) => {
        
              this._snakebar.open(err.message, '', {
                duration: 4000,
                panelClass: ['err-msg'],
                horizontalPosition: 'end',
                verticalPosition: 'top'
              });
            
          }
        })
      }
    }
  }
  close(): void {
    this.dialogRef.close(false);
  }
}
