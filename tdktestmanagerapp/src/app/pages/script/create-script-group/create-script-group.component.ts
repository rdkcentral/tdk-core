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
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { Router } from '@angular/router';
import { ScriptsService } from '../../../services/scripts.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-create-script-group',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule,FormsModule,DragDropModule],
  templateUrl: './create-script-group.component.html',
  styleUrl: './create-script-group.component.css'
})
export class CreateScriptGroupComponent {

  testSuiteFormSubmitted = false;
  testSuiteFrom!:FormGroup;
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
  
  constructor(private fb: FormBuilder,private router: Router,private scriptservice:ScriptsService,
    private _snakebar: MatSnackBar ) {
    this.selectedCategory = localStorage.getItem('category');
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
  }

  ngOnInit(): void {
    this.testSuiteFrom = this.fb.group({
      search: [''],
      testSuiteName: ['', Validators.required],
      description:['', Validators.required],
      container2Scripts: [[], this.container2Validator()]
    });
    this.allScripts();
  }

  allScripts(){
    this.scriptservice.findTestSuitebyCategory(this.selectedCategory).subscribe(res=>{
      this.container1 = JSON.parse(res);
    })
  }
  // Handle multi-select using Ctrl (Cmd on Mac) + click
  selectItem(event: MouseEvent, item: string) :void{
    if (event.ctrlKey || event.metaKey) {
      if (this.selectedItems.has(item)) {
        this.selectedItems.delete(item);
      } else {
        this.selectedItems.add(item);
      }
    } else {
      this.selectedItems.clear();
      this.selectedItems.add(item);
    }
  }

  drop(event: CdkDragDrop<string[]>) :void{
    const selectedArray = Array.from(this.selectedItems);
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      for (let selectedItem of selectedArray) {
        const index = event.previousContainer.data.indexOf(selectedItem);
        if (index !== -1) {
          event.previousContainer.data.splice(index, 1);
          event.container.data.splice(event.currentIndex, 0, selectedItem);
        }
      }
      this.selectedItems.clear();
    }
    this.testSuiteFrom.get('container2Scripts')?.setValue(this.container2);
    this.testSuiteFrom.get('container2Scripts')?.markAsTouched();
    this.testSuiteFrom.get('container2Scripts')?.updateValueAndValidity();
  }
  get filteredContainer1(): any[] {
    const searchTerm = this.testSuiteFrom.get('search')?.value || ''; 
    let filteredList = this.container1;
    if (searchTerm) {
      filteredList = this.container1.filter((item:any) =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    return filteredList.sort((a:any, b:any) => {
      if (this.sortOrder === 'asc') {
        return a.name.localeCompare(b.name);
      } else {
        return b.name.localeCompare(a.name);
      }
    });
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
    localStorage.removeItem('category');
    this.router.navigate(['/script']);
  }
  reset():void{
    this.testSuiteFrom.reset();
  }
  testSuiteSubmit():void{
    this.testSuiteFormSubmitted = true;
    if(this.testSuiteFrom.invalid){
      return ;
    }else{
      let obj = {
        name:this.testSuiteFrom.value.testSuiteName,
        description: this.testSuiteFrom.value.description,
        category: this.selectedCategory,
        userGroup: this.loggedinUser.userGroupName,
        scripts:this.testSuiteFrom.value.container2Scripts
      }
      this.scriptservice.cretaeTestSuite(obj).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 2000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            localStorage.removeItem('category');
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
