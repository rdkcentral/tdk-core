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
import { Component, Inject, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MaterialModule } from '../../../material/material.module';
import { AgGridAngular } from 'ag-grid-angular';
import { HttpClientModule } from '@angular/common/http';
import { DeviceService } from '../../../services/device.service';
import {
  ColDef,
  IMultiFilterParams,
} from 'ag-grid-community';
import { InputComponent } from '../ag-grid-buttons/input/input.component';
/**
 * @title Dialog elements
 */

@Component({
  selector: 'dialog-data',
  templateUrl: 'dialog.component.html',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule,AgGridAngular],
  encapsulation: ViewEncapsulation.None
})

export class DialogDelete implements OnInit{

  public columnDefs: ColDef[] = [
    {
      headerName: 'Steam Id',
      field: 'streamingDetailsId',
      filter: 'agMultiColumnFilter',
      flex: 2,
      filterParams: {
        filters: [
          {
            filter: 'agTextColumnFilter',
            display: 'subMenu',
          },
          {
            filter: 'agSetColumnFilter',
          },
        ],
      } as IMultiFilterParams,
    },
    {
      headerName: 'Channel Type',
      field: 'channelType',
      filter: 'agMultiColumnFilter',
      flex: 2,
      filterParams: {
        filters: [
          {
            filter: 'agTextColumnFilter',
            display: 'accordion',
            title: 'Expand Me for Text Filters',
          },
          {
            filter: 'agSetColumnFilter',
            display: 'accordion',
          },
        ],
      } as IMultiFilterParams,
    },
    {
      headerName: 'Audio Format',
      field: 'audioType',
      filter: 'agMultiColumnFilter',
      flex: 2,
      filterParams: {
        filters: [
          {
            filter: 'agTextColumnFilter',
            display: 'accordion',
            title: 'Expand Me for Text Filters',
          },
          {
            filter: 'agSetColumnFilter',
            display: 'accordion',
          },
        ],
      } as IMultiFilterParams,
    },
    {
      headerName: 'Video Format',
      field: 'videoType',
      filter: 'agMultiColumnFilter',
      flex: 2,
      filterParams: {
        filters: [
          {
            filter: 'agTextColumnFilter',
            display: 'accordion',
            title: 'Expand Me for Text Filters',
          },
          {
            filter: 'agSetColumnFilter',
            display: 'accordion',
          },
        ],
      } as IMultiFilterParams,
    },
    {
      headerName: 'Ocap Id',
      field: 'ocapId',
      cellRenderer:'inputCellRenderer',
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };
  uploadConfigForm!: FormGroup;
  configData:any;
  configFileName!:string;
  stbNameChange!: string;
  visibleDeviceconfigFile = false;
  newFileName!: string;
  rowData:any = [];
  public frameworkComponents :any;
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 5;
  public paginationPageSizeSelector: number[] | boolean = [5,10, 50, 100];
  public tooltipShowDelay = 500;
  gridApi!: any;
  isGateway!: any;
  isrecorderId = false;
  showTable= false;

  constructor(
    public dialogRef: MatDialogRef<DialogDelete>,
    @Inject(MAT_DIALOG_DATA) public data: any ,private service:DeviceService,private fb:FormBuilder) {
      this.frameworkComponents = {
        inputCellRenderer: InputComponent
      }
    }

  ngOnInit(): void {
    this.visibilityConfigFile();
    this.getTableUpdateData();
    this.uploadConfigForm = this.fb.group({
      editorFilename:['',{disabled: true}],
      editorContent: [''],
    });
  }
  onGridReady(params: any) {
    this.gridApi = params.api;
  }
  onCancelDelete(): void {
    localStorage.removeItem('streamData');
    this.dialogRef.close(false); // Send false on selecting Cancel
  }

  onConfirmDelete(): void {
    this.dialogRef.close(true); // Send true on selecting Delete|Okay
  }
  visibilityConfigFile(): void{
    let boxNameConfig = this.data.stbName;
    let boxTypeConfig = this.data.boxTypeName; 
    this.service.downloadDeviceConfigFile(boxNameConfig,boxTypeConfig)
    .subscribe((res)=>{ 
      this.configFileName = res.filename;
      if(this.configFileName !== `${boxNameConfig}.config` && this.stbNameChange !== undefined && this.stbNameChange !== ""){
        this.visibleDeviceconfigFile = true;
      }else{
        this.visibleDeviceconfigFile = false;
      }
      if(this.configFileName === `${boxTypeConfig}.config`){
        this.visibleDeviceconfigFile = true;
      }
      if(this.configFileName !== `${boxNameConfig}.config` && this.configFileName !== `${boxTypeConfig}.config`){
        this.visibleDeviceconfigFile = false;
        this.newFileName =`${boxNameConfig}.config`;
      }

      this.readFileContent(res.content);
      // this.uploadConfigForm.patchValue({
      //   editorFilename: this.configFileName,
      //   editorContent: this.configData
      // })
      // this.readDeviceFileContent(res.content); 
      // this.uploadDeviceConfigForm.patchValue({
      //   editorFilename: this.stbNameChange+'.config',
      //   editorContent: this.configData
      // })
    })
  }
  readFileContent(file:Blob): void{
    let boxNameConfig = this.data.stbname;
    const reader = new FileReader();
    reader.onload = ()=>{
      let htmlContent = reader.result
      this.configData = this.formatContent(htmlContent);
      if(this.configData){
          this.uploadConfigForm.patchValue({
            editorFilename: this.configFileName ===`${boxNameConfig}.config`?this.configFileName:this.newFileName,
            editorContent: this.configData
          })
      }
    }
    reader.readAsText(file)
  }

  formatContent(content:any){
    return content.replace(/#/g, '<br># ');
  }
  // isBoxtypeGateway(value:any){
  //   this.service.isBoxtypeGateway(value).subscribe(res=>{
  //     this.isGateway = res;
  //     if(this.isGateway === 'true'){
  //       this.isrecorderId = true;
  //       this.showTable = true;
  //       // this.getTableUpdateData();
  //     }else{
  //       this.isrecorderId = false;
  //       this.showTable = false;
  //     }
  //   })
  // }
  getTableUpdateData(){
    this.service.getStreamsForDeviceForUpdate(this.data.id).subscribe(res=>{
      this.rowData = JSON.parse(res);
      if(this.rowData.length>0){
        this.showTable = true;
      }else{
        this.showTable = false;
      }
    })
  }
}
