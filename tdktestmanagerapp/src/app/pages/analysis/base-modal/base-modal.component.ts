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
import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { AuthService } from '../../../auth/auth.service';
import {
  ColDef,
  GridApi,
  GridOptions,
  GridReadyEvent,
  IDateFilterParams,
} from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { AgGridAngular } from 'ag-grid-angular';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import moment from 'moment-timezone';

@Component({
  selector: 'app-base-modal',
  standalone: true,
  imports: [CommonModule,FormsModule, ReactiveFormsModule, MaterialModule, AgGridAngular],
  templateUrl: './base-modal.component.html',
  styleUrl: './base-modal.component.css'
})
export class BaseModalComponent {

  filterSubmitted = false;
  filterForm!: FormGroup;
  public themeClass: string = 'ag-theme-quartz';
  rowData: any = [];
  selectedRowCount = 0;
  public gridApi!: GridApi;
  filterParams: IDateFilterParams = {
    comparator: (filterLocalDateAtMidnight: Date, cellValue: string) => {
      var dateAsString = cellValue;
      if (dateAsString == null) return -1;
      var dateParts = dateAsString.split('-');
      var cellDate = new Date(
        Number(dateParts[2]),
        Number(dateParts[1]) - 1,
        Number(dateParts[0])
      );
      if (filterLocalDateAtMidnight.getTime() === cellDate.getTime()) {
        return 0;
      }
      if (cellDate < filterLocalDateAtMidnight) {
        return -1;
      }
      if (cellDate > filterLocalDateAtMidnight) {
        return 1;
      }
      return 0;
    },
    minValidYear: 2000,
    maxValidYear: 2024,
    inRangeFloatingFilterDateFormat: 'DD MMM YYYY',
  };
public columnDefs: ColDef[] = [
      {
        headerCheckboxSelection: false,
        checkboxSelection: true,
        headerCheckboxSelectionFilteredOnly: false,
        width:40,
        resizable: false,
      },
      {
        headerName: 'Execution Name',
        field: 'executionName',
        filter: 'agTextColumnFilter',
        sortable: true,
        tooltipField: 'executionName',
        cellClass: 'selectable',
        width:265,
        cellStyle:{'white-space': 'normal',' word-break': 'break-word'},
        wrapText:true,
        headerClass: 'header-center',
        resizable: false,
      },
      {
        headerName: 'Scripts/Testsuite',
        field: 'scriptTestSuite',
        filter: 'agTextColumnFilter',
        sortable: true,
        width:305,
        tooltipField: 'scriptTestSuite',
        resizable: false,
        cellRenderer:(params:any)=>{
          const text = params.value || '';
          if(text.length > 50){
            return `${text.slice(0,50)}...`;
          }
          return text;
        },
        cellClass: (params:any)=>{
          return params.value.length > 50 ? 'text-ellipsis' : 'text-two-line';
        },
      },
      {
        headerName: 'Device',
        field: 'device',
        filter: 'agTextColumnFilter',
        sortable: true,
        tooltipField: 'device',
        width:150,
        cellClass: 'selectable',
        cellStyle:{'white-space': 'normal',' word-break': 'break-word'},
        wrapText:true,
        resizable: false
      },
      {
        headerName: 'Date Of Execution',
        field: 'executionDate',
        filter: 'agTextColumnFilter',
        filterParams: this.filterParams,
        sortable: true,
        cellClass: 'selectable',
        width:190,
        resizable: false,
        cellRenderer:(data:any)=>{
          return data.value ? (new Date(data.value)).toLocaleString() : ''; 
        }
      },
      {
        headerName: 'Result',
        field: 'status',
        filter: 'agTextColumnFilter',
        cellStyle: { textAlign: "center" },
        sortable: true,
        resizable: false,
        width:90,
        cellClass: 'selectable',
        cellRenderer:(params:any)=>{
          const status = params.value;
          let iconHtml = '';
          switch(status){
            case 'SUCCESS':
              iconHtml = `<i class="bi bi-check-circle-fill" style="color:green;" title="Success"></i>`;
              break;
            case 'FAILURE':
              iconHtml =  `<i class="bi bi-x-circle-fill" style="color:red;" title="Failure"></i>`;
              break;
            case 'INPROGRESS':
              iconHtml =  `<div class="spinner-border spinner-border-sm text-warning" role="status" title="Inprogress">
                        <span class="visually-hidden">Loading...</span>
                      </div>`;
              break;
            case 'ABORTED':
              iconHtml =  `<i class="bi bi-ban" style="color:red;" title="Aborted"></i>`;
              break;
            case 'PAUSE':
              iconHtml =  `<i class="bi bi-pause-circle-fill" style="color:gray;" title="Paused"></i>`;
              break;
            default:
              return;
          }
          return iconHtml;
        }
      },
   
    ];
    defaultColDef ={
      sortable:true,
      headerClass: 'header-center',
    };
    selectedRowName: string | null = null;
    pageSize = 10;
    pageSizeSelector: number[] | boolean = [10, 20, 30, 50];
    fromUTCTime!:string;
    toUTCTime!: string;

    constructor(private authservice: AuthService, private fb: FormBuilder,
      public dialogRef: MatDialogRef<BaseModalComponent>,@Inject(MAT_DIALOG_DATA) public data: any 
    ) { 
      }
  
    ngOnInit(): void {
      this.filterForm = this.fb.group({
        fromDate:['', Validators.required],
        toDate:['', Validators.required],
        deviceType:['', Validators.required],
        scriptType:['', Validators.required],
        category:['', Validators.required]
      },
      {
        validators: this.dateRangeValidator
      });
      this.rowData = [
        {
            "executionId": "018665c5-b5a9-465a-b157-e1c7d5015c53",
            "executionName": "Amlogic_Amlogic_CI_012725095848",
            "executionDate": "2025-01-27T09:58:55Z",
            "scriptTestSuite": "RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_4K_AV1",
            "device": "AMLOGIC_TDKCI",
            "status": "FAILURE",
            "user": "admin",
            "abortNeeded": false
        },
        {
            "executionId": "20a9f9cb-028b-409a-a5e8-2534ab652fe2",
            "executionName": "Amlogic_Amlogic_CI_012725095604",
            "executionDate": "2025-01-27T09:56:10Z",
            "scriptTestSuite": "RDKV_CERT_PVS_Functional_ResidentApp_TimeTo_Launch",
            "device": "AMLOGIC_TDKCI",
            "status": "FAILURE",
            "user": "admin",
            "abortNeeded": false
        },
        {
            "executionId": "20172fdf-60a0-421c-8a5e-1c18f1728edc",
            "executionName": "Amlogic_Amlogic_CI_012725094739",
            "executionDate": "2025-01-27T09:48:16Z",
            "scriptTestSuite": "RDKV_CERT_PVS_Functional_HtmlApp_TimeTo_SuspendResume",
            "device": "AMLOGIC_TDKCI",
            "status": "FAILURE",
            "user": "admin",
            "abortNeeded": false
        },
        {
            "executionId": "b78f45af-9a53-422a-851b-f310f58ca347",
            "executionName": "Amlogic_Amlogic_CI_012725094202",
            "executionDate": "2025-01-27T09:42:09Z",
            "scriptTestSuite": "RDKV_CERT_PVS_Functional_Check_FailedServices",
            "device": "AMLOGIC_TDKCI",
            "status": "FAILURE",
            "user": "admin",
            "abortNeeded": false
        },
        {
            "executionId": "9dd2f859-c62b-49aa-a739-9b9a3b806f8a",
            "executionName": "Amlogic_Amlogic_CI_012725093322",
            "executionDate": "2025-01-27T09:33:33Z",
            "scriptTestSuite": "RDKV_Memcr_Check_Service_Status",
            "device": "AMLOGIC_TDKCI",
            "status": "SUCCESS",
            "user": "admin",
            "abortNeeded": false
        },
        {
            "executionId": "4a383dba-377c-48c8-8660-07c94685cbac",
            "executionName": "Amlogic_Amlogic_CI_012725092637",
            "executionDate": "2025-01-27T09:26:47Z",
            "scriptTestSuite": "RDKV_CERT_PACS_Cobalt_PlayPause_Hibernate_Restore",
            "device": "AMLOGIC_TDKCI",
            "status": "FAILURE",
            "user": "admin",
            "abortNeeded": false
        },
        {
            "executionId": "aa0c47c8-8795-4123-83ea-f8a4f3608fc3",
            "executionName": "Amlogic_Amlogic_CI_012725090629",
            "executionDate": "2025-01-27T09:06:36Z",
            "scriptTestSuite": "RDKV_CERT_PACS_Cobalt_PlayPause_Hibernate_Restore",
            "device": "AMLOGIC_TDKCI",
            "status": "FAILURE",
            "user": "admin",
            "abortNeeded": false
        },
        {
            "executionId": "5cf1cda4-5137-46ae-b48d-cde81df4c96e",
            "executionName": "Amlogic_Amlogic_CI_012725085649",
            "executionDate": "2025-01-27T08:57:04Z",
            "scriptTestSuite": "RDKV_CERT_PACS_Cobalt_PlayPause_Hibernate_Restore",
            "device": "AMLOGIC_TDKCI",
            "status": "FAILURE",
            "user": "admin",
            "abortNeeded": false
        },
        {
            "executionId": "81122d78-b2fe-46c8-9d04-1539da11fd6e",
            "executionName": "Amlogic_Amlogic_CI_012725084251",
            "executionDate": "2025-01-27T08:43:06Z",
            "scriptTestSuite": "RDKV_CERT_PACS_Cobalt_PlayPause_Hibernate_Restore",
            "device": "AMLOGIC_TDKCI",
            "status": "FAILURE",
            "user": "admin",
            "abortNeeded": false
        },
        {
            "executionId": "c9ef567e-2fca-4cb9-b767-ccf1cc2c3671",
            "executionName": "Amlogic_Amlogic_CI_012725080452",
            "executionDate": "2025-01-27T08:05:10Z",
            "scriptTestSuite": "RDKV_CERT_AVS_XCast",
            "device": "AMLOGIC_TDKCI",
            "status": "FAILURE",
            "user": "admin",
            "abortNeeded": false
        }
    ];
    }
    dateRangeValidator(group: AbstractControl):{[key:string]:any}| null{
      const fromDate = group.get('fromDate')?.value;
      const toDate = group.get('toDate')?.value;
      if(fromDate && toDate){
        const diff = moment(toDate).diff(moment(fromDate), 'days');
        return diff > 30 ? {maxDaysExceeded: true}:null;
      }
      return null;
    }
  /**
   * Event handler for when the grid is ready.
   * @param params - The GridReadyEvent object containing the grid API.
   */
  onGridReady(params: GridReadyEvent):void {
    this.gridApi = params.api;
  }
  onrowSelected():void{
    const selectedNodes = (this.gridApi as any).getSelectedNodes();
    if(selectedNodes.length > 0){
      this.selectedRowName = selectedNodes[0].data.executionName;
      } else{
      this.selectedRowName = null;
    }
  }
  close():void{
    this.dialogRef.close(false);
  }
  filterDataSubmit():void{
    this.filterSubmitted = true;
    if(this.filterForm.invalid){
      return;
    }else{
      const locaFromDateTime = this.filterForm.get('fromDate')?.value;
      const locaToDateTime = this.filterForm.get('toDate')?.value;
      
      if(locaFromDateTime){
        const utcMoment =  moment.tz(locaFromDateTime, moment.tz.guess()).utc();
        this.fromUTCTime = utcMoment.format('YYYY-MM-DDTHH:mm:ss[Z]');
      }
      if(locaToDateTime){
        const utcMoment =  moment.tz(locaToDateTime, moment.tz.guess()).utc();
        this.toUTCTime = utcMoment.format('YYYY-MM-DDTHH:mm:ss[Z]');
      }
    }
  }

  onConfirm():void{
    this.dialogRef.close(this.selectedRowName);
  }
}
