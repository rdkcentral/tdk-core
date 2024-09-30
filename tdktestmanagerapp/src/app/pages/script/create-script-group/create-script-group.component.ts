import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { Router } from '@angular/router';

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
  container1: string[]  = [
    'AAMP_HLS_GetPlayback_Duration ', 
    'ACM_AudioPropertiesPersists', 
    'BluetoothHAL_Find_Device', 
    'BluetoothHAL_Get_Adapters', 
    'CC_Hide_22', 
    'CC_Initialization_22', 
    'DSHal_GetAudioFormat',
    'DSHal_GetCPUTemperature', 
    'E2E_LinearTV_TuneSD_01', 
    'E2E_RMF_DVR_TrickPlay_55', 
    'FCS_Playback_DASH', 
    'FCS_Playback_Dolby'
  ];
  container2: string[]  = [];
  scriptGrous: string[] = [];

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.testSuiteFrom = new FormGroup({
      search: new FormControl(''),
      testSuiteName: new FormControl(''),
      scriptGroupArr: new FormControl(''),
    });
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
  }
  get filteredContainer1(): string[] {
    const searchTerm = this.testSuiteFrom.get('search')?.value || ''; 
    let filteredList = this.container1;
    if (searchTerm) {
      filteredList = this.container1.filter(name =>
        name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    return filteredList.sort((a, b) => {
      if (this.sortOrder === 'asc') {
        return a.localeCompare(b);
      } else {
        return b.localeCompare(a);
      }
    });
  }
  toggleSortOrder() :void{
    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
  }
  goBack():void{
    this.router.navigate(['script']);
  }
  reset():void{
    this.testSuiteFrom.reset();
  }
  testSuiteSubmit():void{
    console.log(this.testSuiteFrom.value);
    console.log("Final List in Container :", this.scriptGrous);
  }





}
