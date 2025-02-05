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
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../auth/auth.service';
import { MaterialModule } from '../../material/material.module';
import { MatDialog } from '@angular/material/dialog';
import { BaseModalComponent } from './base-modal/base-modal.component';
import { ComparisonModalComponent } from './comparison-modal/comparison-modal.component';

@Component({
  selector: 'app-analysis',
  standalone: true,
  imports: [CommonModule,FormsModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './analysis.component.html',
  styleUrl: './analysis.component.css'
})
export class AnalysisComponent {

  selectedDfaultCategory!: string;
  categoryName!:string;
  loggedinUser:any;
  userCategory!:string;
  preferedCategory!:string;
  scriptShow = true;
  showTestSuite = false;
  reportSubmitted = false;
  reportForm!: FormGroup;
  combinedSubmitted = false;
  combinedForm!: FormGroup;
  selectExecutionName!: string;
  selectComparisonNames: string ='';
  baseCombinedName!:string;
  CombinedExecutions : string ='';
  tabName:string = 'Comparsion Report';

  constructor(private authservice: AuthService, private fb: FormBuilder,
    public baseDialog :MatDialog, public comparisonDialog :MatDialog,
  ) { 
      this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
      this.userCategory = this.loggedinUser.userCategory;
      this.preferedCategory = localStorage.getItem('preferedCategory')|| '';
      
    }

  ngOnInit(): void {
    let localcategory = this.preferedCategory?this.preferedCategory:this.userCategory;
    this.categoryChange(localcategory);
    this.reportForm = this.fb.group({
      baseName:['', Validators.required],
      comparisonName:['', Validators.required],
    })
    this.combinedForm = this.fb.group({
      fromDate:['', Validators.required],
      toDate:['', Validators.required],
      deviceType:['', Validators.required],
      scriptType:['', Validators.required],
      category:['', Validators.required]
    },
    {
      
    });
  }
  
  categoryChange(val:string): void {
    if (val === 'RDKB') {
      this.categoryName = 'Broadband';
      this.selectedDfaultCategory = 'RDKB';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
    } else if (val === 'RDKC') {
      this.categoryName = 'Camera';
      this.selectedDfaultCategory = 'RDKC';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
    } else {
      this.selectedDfaultCategory = 'RDKV';
      this.categoryName = 'Video';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
    }
  }

  resultChange(event:any): void {

  }
  resultCategory(event:any): void {

  }
  deviceChange(event:any): void {

  }
  scriptType(value:string): void {
    if(value ==='testsuites'){
      this.scriptShow = false;
      this.showTestSuite = true;
    }else{
      this.scriptShow = true;
      this.showTestSuite = false;
    }
  }

  onTabClick(event: any): void {
    const label = event.tab.textLabel;
    if(label === 'Combined Report'){
      this.tabName = 'Combined Report';
    }else{
      this.tabName = 'Comparsion Report';
    }
    
  }
  reportSubmit():void{
    this.reportSubmitted = true;
    if(this.reportForm.invalid){
      return;
    }
  }
  openModal(){
    const dialogRef = this.baseDialog.open( BaseModalComponent,{
      width: '85%',
      height: '90vh',
      maxWidth:'100vw',
      panelClass: 'report-modalbox',
      data: this.tabName
    });
    if(this.tabName === 'Combined Report'){
      dialogRef.afterClosed().subscribe(res=>{
        if(res){
          this.baseCombinedName = res;
        }
      })
    }else{
      dialogRef.afterClosed().subscribe(res=>{
        if(res){
          this.selectExecutionName = res;
        }
      })
    }
  }
  comparisonModal(){
    const dialogRef = this.comparisonDialog.open( ComparisonModalComponent,{
      width: '85%',
      height: '90vh',
      maxWidth:'100vw',
      panelClass: 'report-modalbox',
      data: this.tabName
    });
    if(this.tabName === 'Combined Report'){
      dialogRef.afterClosed().subscribe((res:string[])=>{
        if(res){
          this.CombinedExecutions = res.join(', ');
        }
      })
    }else{
      dialogRef.afterClosed().subscribe((res:string[])=>{
        if(res){
          this.selectComparisonNames = res.join(', ');
        }
      })
    }

  }
}
