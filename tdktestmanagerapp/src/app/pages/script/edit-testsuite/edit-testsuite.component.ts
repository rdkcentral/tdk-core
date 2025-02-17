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
import { Component, Input } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { ActivatedRoute, Router } from '@angular/router';
import { ScriptsService } from '../../../services/scripts.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';

@Component({
  selector: 'app-edit-testsuite',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule,FormsModule,DragDropModule],
  templateUrl: './edit-testsuite.component.html',
  styleUrl: './edit-testsuite.component.css'
})
export class EditTestsuiteComponent {
  testSuiteFormSubmitted = false;
  testSuiteEditFrom!:FormGroup;
  selectedItems: Set<string> = new Set();
  searchTerm: string = '';
  sortOrder: 'asc' | 'desc' = 'asc';
  sortOrderRight: 'asc' | 'desc' = 'asc';
  container1:any[]=[];
  container2ScriptArr: any[]  = [];
  scriptGrous: string[] = [];
  selectedCategory:any;
  testSuiteArr:any[] = [];
  loggedinUser: any;
  testSuiteEidtData:any;
  viewName!:string;
  onlyVideoCategory!:string;
  onlyVideoCategoryName!:string;
  categoryName!:string;
  selectedLeft = new Set<number>();
  selectedRight = new Set<number>();
  filteredLeftList:any;

  constructor(private fb: FormBuilder,private router: Router,private scriptservice:ScriptsService,
    private _snakebar: MatSnackBar,private route: ActivatedRoute,private authservice : AuthService ) {
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
    const dataString = this.router.getCurrentNavigation();
    this.testSuiteEidtData = dataString?.extras.state?.['testSuiteData'];
    this.viewName = localStorage.getItem('viewName') || '';
  }

  ngOnInit(): void {
    this.onlyVideoCategory = localStorage.getItem('onlyVideoCategory')||'';
    // let category = localStorage.getItem('category') || '';
    // this.selectedCategory = category?category:'RDKV';
    this.selectedCategory = this.onlyVideoCategory?this.onlyVideoCategory:this.selectedCategory;
    if(this.onlyVideoCategory){
      if(this.onlyVideoCategory === 'RDKV_RDKSERVICE'){
        this.onlyVideoCategoryName = 'Video-Thunder';
      }else if(this.onlyVideoCategory === 'RDKV'){
        this.onlyVideoCategoryName = 'Video';
      }
    }else{
      if(this.selectedCategory == 'RDKB'){
        this.categoryName = 'Broadband';
      }
       if(this.selectedCategory == 'RDKC'){
        this.categoryName = 'Camera';
      }
    }

    if(this.testSuiteEidtData){
      this.container2ScriptArr = this.testSuiteEidtData.scripts?this.testSuiteEidtData.scripts:[];
    }
    this.testSuiteEditFrom = this.fb.group({
      search: [''],
      testSuiteName: [this.testSuiteEidtData?this.testSuiteEidtData.name:'', Validators.required],
      description:[this.testSuiteEidtData?this.testSuiteEidtData.description:'', Validators.required],
      container2Scripts: [[], this.container2Validator()]
    });
    this.allScripts();
  }

  allScripts(){
    this.scriptservice.findTestSuitebyCategory(this.selectedCategory).subscribe(res=>{
      this.container1 = JSON.parse(res);
      const idsToRemove = new Set(this.container2ScriptArr.map((obj) => obj.id));
      this.container1 = this.container1.filter((obj) => !idsToRemove.has(obj.id));
    })

  }
  toggleSec(scripts:any, side: 'left' | 'right'){
    if(side === 'left'){
      this.selectedLeft.has(scripts.id)?this.selectedLeft.delete(scripts.id):this.selectedLeft.add(scripts.id);
    }else{
      this.selectedRight.has(scripts.id)?this.selectedRight.delete(scripts.id):this.selectedRight.add(scripts.id);
    }
  }
  moveToRight(){
    
    this.container2ScriptArr.push(...this.container1.filter(scripts => this.selectedLeft.has(scripts.id)));
    this.container1 = this.container1.filter(scripts => !this.selectedLeft.has(scripts.id));
    this.selectedLeft.clear();
    this.testSuiteEditFrom.get('container2Scripts')?.setValue(this.container2ScriptArr);
    this.testSuiteEditFrom.get('container2Scripts')?.markAsTouched();
    this.testSuiteEditFrom.get('container2Scripts')?.updateValueAndValidity();
  }
  moveToLeft(){
    this.container1.push(...this.container2ScriptArr.filter(scripts => this.selectedRight.has(scripts.id)));
    this.container2ScriptArr = this.container2ScriptArr.filter(scripts => !this.selectedRight.has(scripts.id));
    this.selectedRight.clear();
  }
  moveToUp(){
    const selectedIds = Array.from(this.selectedRight);
    for (let i = 1; i < this.container2ScriptArr.length; i++) {
      if(selectedIds.includes(this.container2ScriptArr[i].id)){
        [this.container2ScriptArr[i], this.container2ScriptArr[i-1]] =  [this.container2ScriptArr[i - 1], this.container2ScriptArr[i]]
      }
      
    }
  }
  moveToDown(){
    const selectedIds = Array.from(this.selectedRight);
    for (let i = this.container2ScriptArr.length -2; i >= 0; i--) {
      if(selectedIds.includes(this.container2ScriptArr[i].id)){
        [this.container2ScriptArr[i], this.container2ScriptArr[i+1]] =  [this.container2ScriptArr[i + 1], this.container2ScriptArr[i]]
      }
      
    }
  }
  get filteredContainer1(): any[] {
    const searchTerm = this.testSuiteEditFrom.get('search')?.value || ''; 
    this.filteredLeftList = this.container1;
    if (searchTerm) {
       this.filteredLeftList = this.container1.filter((item:any) =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
      return this.filteredLeftList;
  }
  toggleSortOrder() :void{
    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
  }
  get container2(): any[] {
    let filteredList2 = this.container2ScriptArr;
    this.testSuiteArr = filteredList2;
    return filteredList2.sort((a, b) => {
      if (this.sortOrderRight === 'asc') {
        return a.name.localeCompare(b.name);
      } else {
        return b.name.localeCompare(a.name);
      }
    });
  }

  container2Validator() {
    return (control: AbstractControl): ValidationErrors | null => {
      return this.container2ScriptArr.length > 0 ? null : { container2Empty: true };
    };
  }

  toggleSortRightSide() :void{
    this.sortOrderRight = this.sortOrderRight === 'asc' ? 'desc' : 'asc';
  }
  goBack():void{
    this.router.navigate(['/script']);
  }
  reset():void{
    this.testSuiteEditFrom.reset();
  }
  testSuiteEditSubmit():void{
    this.testSuiteFormSubmitted = true;
    if(this.testSuiteEditFrom.invalid){
      return ;
    }else{
      let obj = {
        id:this.testSuiteEidtData.id,
        name:this.testSuiteEditFrom.value.testSuiteName,
        description: this.testSuiteEditFrom.value.description,
        category: this.selectedCategory,
        userGroup: this.loggedinUser.userGroupName,
        scripts:this.container2ScriptArr?this.container2ScriptArr:this.testSuiteEditFrom.value.container2Scripts
      }
      this.scriptservice.updateTestSuite(obj).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 2000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["/script"]);
          }, 1000);
        },
        error: (err) => {
          let errmsg =JSON.parse(err.error) ;
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


}
