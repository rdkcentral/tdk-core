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
import {Component, Inject, OnInit, ViewChild } from '@angular/core';
import {  FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MaterialModule } from '../../../material/material.module';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  GridApi
} from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { ExecutionService } from '../../../services/execution.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DetailsExeDialogComponent } from '../details-execution/details-exe-dialog/details-exe-dialog.component';

@Component({
  selector: 'app-analyze-dialog',
  standalone: true,
  imports: [CommonModule,FormsModule, ReactiveFormsModule, MaterialModule,AgGridAngular],
  templateUrl: './analyze-dialog.component.html',
  styleUrl: './analyze-dialog.component.css'
})
export class AnalyzeDialogComponent implements OnInit{
  @ViewChild('detailsExeDialog') detailsExeDialog!: DetailsExeDialogComponent;
  public themeClass: string = 'ag-theme-quartz';
  rowData: any = [];
  selectedRowCount = 0;
  pageSize = 10;
  schedulePageSizeSelector: number[] | boolean = [5, 10, 30, 50];
  public gridApi!: GridApi;
  public columnSchudle: ColDef[] = [
    {
      headerName: 'TicketNumber',
      field: 'ticketNumber',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Summary',
      field: 'summary',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true
    },      
    {
      headerName: 'Status',
      field: 'status',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      headerClass: 'no-sort',
      width: 130,
  
    },
  ];
  gridOptions = {
    // rowHeight: 30,
  };
  allDeftesTypes:any;
  analysisFormSubmitted = false;
  analysisForm!: FormGroup;
  loggedinUser:any;

  constructor(
    public dialogRef: MatDialogRef<AnalyzeDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private executionservice:ExecutionService,
    private fb: FormBuilder,
    private _snakebar: MatSnackBar
    ) {
      this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
  }

  ngOnInit(): void {
      this.analysisForm = this.fb.group({
        scriptName: [{ value: this.data.name, disabled: true}],
        ticketDetails: [this.data.analysisTicketID || '', Validators.required],
        defectType: [this.data.analysisDefectType || '', Validators.required],
        remarks: [this.data.analysisRemark || '', Validators.required]
      });
    this.getAllDefects();
  }

  get f() { return this.analysisForm.controls; }

  onTabClick(event: any): void {
    const label = event.tab.textLabel;
  }
  onClose():void {
    this.dialogRef.close(false);
  }

  getAllDefects():void{
    this.executionservice.getDefectTypes().subscribe(res=>{
      this.allDeftesTypes = JSON.parse(res) ;
    })
  }
  

  analysisSubmit():void{
    this.analysisFormSubmitted = true;
    if (this.analysisForm.invalid) {
      return;
    } else {
      let analysisData = {
        analysisUser:this.loggedinUser.userName,
        analysisDefectType:this.analysisForm.value.defectType,
        analysisTicketID: this.analysisForm.value.ticketDetails,
        analysisRemark:this.analysisForm.value.remarks
      }
      this.executionservice.saveAnalysisResult(this.data.executionResultID,analysisData).subscribe({
        next:(res)=>{
          this._snakebar.open(res, '', {
            duration: 1000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
         
          setTimeout(() => {
          this.onClose();
          }, 2000);
        },
        error:(err)=>{
          let errmsg = JSON.parse(err.error);
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
