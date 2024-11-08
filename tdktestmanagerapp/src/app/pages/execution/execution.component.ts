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
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../material/material.module';
import { AgGridAngular } from 'ag-grid-angular';
import { ColDef,GridApi,GridReadyEvent,IDateFilterParams,IMultiFilterParams } from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { ButtonComponent } from '../../utility/component/ag-grid-buttons/button/button.component';
import { Router, RouterOutlet } from '@angular/router';
import { AuthService } from '../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ScriptsService } from '../../services/scripts.service';
import { MatDialog } from '@angular/material/dialog';
import { ExecuteDialogComponent } from '../../utility/component/execute-dialog/execute-dialog.component';
import { ExecutionButtonComponent } from '../../utility/component/execution-button/execution-button.component';
import { DetailsExeDialogComponent } from '../../utility/component/details-execution/details-exe-dialog/details-exe-dialog.component';
@Component({
  selector: 'app-execution',
  standalone: true,
  imports: [RouterOutlet,CommonModule,AgGridAngular, FormsModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './execution.component.html',
  styleUrl: './execution.component.css'
})
export class ExecutionComponent {
  executeName:string ="Execute";
  selectedCategory: string = 'All';
  public themeClass: string = "ag-theme-quartz";
  rowData: any = [];
  rowDataSchudle:any =[];
  selectedRowCount = 0;
  public paginationPageSize = 9;
  public paginationPageSizeSelector: number[] | boolean = [5, 9, 15, 30, 50];
  public gridApi!: GridApi;
  filterParams: IDateFilterParams = {
    comparator: (filterLocalDateAtMidnight: Date, cellValue: string) => {
      var dateAsString = cellValue;
      if (dateAsString == null) return -1;
      var dateParts = dateAsString.split("-");
      var cellDate = new Date(
        Number(dateParts[2]),
        Number(dateParts[1]) - 1,
        Number(dateParts[0]),
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
    inRangeFloatingFilterDateFormat: "Do MMM YYYY",
  }
  public columnDefs: ColDef[] = [
    {
      headerName: 'Execution Name',
      field: 'executionName',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Scripts/Testsuite',
      field: 'scriptsTestsuite',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Device',
      field: 'device',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Date Of Execution',
      field: 'date',
      filter: 'agDateColumnFilter',
      filterParams: this.filterParams,
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Result',
      field: 'results',
      filter: 'agTextColumnFilter',
      width:110,
      sortable: true,
      cellRenderer:(params:any)=>{
        const status = params.value;
        let iconHtml = '';
        switch(status){
          case 'Success':
            iconHtml = `<i class="bi bi-check-circle-fill" style="color:green;" title="Success"></i>`;
            break;
          case 'Failure':
            iconHtml =  `<i class="bi bi-x-circle-fill" style="color:red;" title="Failure"></i>`;
            break;
          case 'Inprogress':
            iconHtml =  `<div class="spinner-border spinner-border-sm text-warning" role="status" title="Inprogress">
                      <span class="visually-hidden">Loading...</span>
                    </div>`;
            break;
          case 'abort':
            iconHtml =  `<i class="bi bi-ban" style="color:red;" title="Aborted"></i>`;
            break;
          case 'pause':
            iconHtml =  `<i class="bi bi-pause-circle-fill" style="color:gray;" title="Paused"></i>`;
            break;
          default:
            return;
        }
        return iconHtml;
      }
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      headerClass: 'no-sort',
      cellRenderer: ExecutionButtonComponent,
      cellRendererParams: (params: any) => ({
        onEditClick: this.userEdit.bind(this),
        onDeleteClick: this.delete.bind(this),
        onViewClick:this.openDetailsModal.bind(this),
        onDownloadClick:this.downloadXML.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    }
  ];
  

  gridOptions = {
    // domLayout: 'autoHeight' 
    rowHeight:30
  };
  parentData = [ ];
  paginatedParentData: any[] = [];
  panelOpenState = false;
  executionList:any[]=[];
  selectedValue!:string;

  constructor(private router: Router, private authservice: AuthService, 
    private _snakebar: MatSnackBar, private scriptservice:ScriptsService,public dialog:MatDialog
  ) {   }

  public columnSchudle: ColDef[] = [
    {
      headerName: 'Job Name',
      field: 'jobname',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'StartDate',
      field: 'startdate',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Scripts/Testsuite',
      field: 'ScriptsTestsuite',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Device',
      field: 'device',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Details',
      field: 'details',
      filter: 'agDateColumnFilter',
      filterParams: this.filterParams,
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'EndDate',
      field: 'enddate',
      filter: 'agTextColumnFilter',
      width:110,
      sortable: true,
    },
    {
      headerName: 'Status',
      field: 'status',
      filter: 'agTextColumnFilter',
      width:110,
      sortable: true,
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      headerClass: 'no-sort',
      width:130,
      cellRenderer: ButtonComponent,
      cellRendererParams: (params: any) => ({
        onEditClick: this.userEdit.bind(this),
        onDeleteClick: this.delete.bind(this),
        // onViewClick:this.openModal.bind(this),
        onDownloadClick:this.downloadXML.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    }
  ];

  ngOnInit(): void {
    this.executionList=[
      {name: 'Execute Now'},
      {name: 'Schedule Execution'}
    ];
    // this.selectedValue = this.executionList[0].name;
    this.scriptservice.getAllexecution().subscribe(res=>{
      this.rowData = res;
      console.log(this.rowData);
      
    }) 
    this.scriptservice.getAllDevice().subscribe(res=>{
      this.parentData = res;
      console.log(this.parentData);
      this.paginatedParentData = this.parentData;
    }) 
  }
    /**
   * Event handler for when the grid is ready.
   * @param params - The GridReadyEvent object containing the grid API.
   */
    onGridReady(params: GridReadyEvent<any>) {
      this.gridApi = params.api;
    }
  onCategoryChange(newValue: string): void {
    this.selectedCategory = newValue;
    localStorage.setItem('scriptCategory', this.selectedCategory);
    if(this.selectedCategory){
      this.authservice.selectedCategory = this.selectedCategory;
    }
  }
  onChangeExecute(event:any){
    console.log(event.target.value);
    this.selectedValue = event.target.value;
  }

  onFilterTextBoxChanged() {
    this.gridApi.setGridOption(
      "quickFilterText",
      (document.getElementById("filter-text-box") as HTMLInputElement).value,
    );
  }

  userEdit(){

  }
  delete(){
    
  }
  openDetailsModal(params:any){
    this.dialog.open( DetailsExeDialogComponent,{
      width: '99%',
      height: '96vh',
      maxWidth:'100vw',
      panelClass: 'custom-modalbox',
      data:{
        agentMonitorPort: params.agentMonitorPort,
        oemName : params.oemName,
        deviceTypeName : params.deviceTypeName,
        category :  params.category,
        id :  params.id,
        logTransferPort  :  params.logTransferPort,
        macId :  params.macId,
        socName :  params.socName,
        statusPort :  params.statusPort,
        stbIp : params.stbIp,
        stbName :   params.stbName,
        stbPort :  params.stbPort,
        thunderEnabled :  params.thunderEnabled,
        thunderPort :  params.thunderPort,
        userGroupName :  params.userGroupName,
        devicePortsConfigured: params.devicePortsConfigured
      }
    })
  }
  downloadXML(){

  }
  togglePanel(parent:any) {
    parent.isOpen = !parent.isOpen;
    this.panelOpenState = !this.panelOpenState;
  }


  openDialog() {
    this.dialog.open( ExecuteDialogComponent,{
      width: '68%',
      height: '96vh',
      maxWidth:'100vw',
      panelClass: 'custom-modalbox',
      data:{
        name:''
      }
    })
  }
 
}
