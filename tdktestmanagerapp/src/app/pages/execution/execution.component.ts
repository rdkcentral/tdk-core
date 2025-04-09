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
import { Component, ElementRef, HostListener, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../material/material.module';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  GridApi,
  GridOptions,
  GridReadyEvent,
  IDateFilterParams,
} from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { AuthService } from '../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { ExecutionButtonComponent } from '../../utility/component/execution-button/execution-button.component';
import { DetailsExeDialogComponent } from '../../utility/component/details-execution/details-exe-dialog/details-exe-dialog.component';
import { ExecutionService } from '../../services/execution.service';
import { ExecuteDialogComponent } from '../../utility/component/execute-dialog/execute-dialog.component';
import { Subject, Subscription, takeUntil } from 'rxjs';
import { Clipboard } from '@angular/cdk/clipboard';
import { LoginService } from '../../services/login.service';
import { DateDialogComponent } from '../../utility/component/date-dialog/date-dialog.component';
import { MatPaginator } from '@angular/material/paginator';
import { ScheduleButtonComponent } from '../../utility/component/execution-button/schedule-button.component';
import { TdkInstallComponent } from '../../utility/component/tdk-install/tdk-install.component';
import { LoaderComponent } from '../../utility/component/loader/loader.component';

@Component({
  selector: 'app-execution',
  standalone: true,
  imports: [
    CommonModule,
    AgGridAngular,
    FormsModule,
    ReactiveFormsModule,
    MaterialModule,
    LoaderComponent

  ],
  templateUrl: './execution.component.html',
  styleUrl: './execution.component.css',
})
export class ExecutionComponent implements OnInit, OnDestroy{
  @ViewChild('deviceSearchInput') deviceSearchInput!: ElementRef;
  @ViewChild('tableSearchInput') tableSearchInput!: ElementRef;
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild('historyTable') historyTable: any;

  executeName: string = 'Execute';
  selectedCategory: string = 'All';
  public themeClass: string = 'ag-theme-quartz';
  rowData: any = [];
  rowDataSchudle: any = [];
  selectedRowCount = 0;
  totalItems = 0;
  currentPage = 0;
  pageSize = 10;
  schedulePageSize = 10;
  schedulePageSizeSelector: number[] | boolean = [10, 20, 50];
  public gridApi!: GridApi;
  selectedRowIds : Set<number> = new Set();

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
      headerCheckboxSelection: true,
      checkboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      headerComponentParams: {
        label: 'Select All',
      },
      width:45,
      resizable: false,
    },
    {
      headerName: 'Execution Name',
      field: 'executionName',
      filter: 'agTextColumnFilter',
      sortable: true,
      tooltipField: 'executionName',
      cellClass: 'selectable',
      flex:2,
      cellStyle:{'white-space': 'normal',' word-break': 'break-word'},
      wrapText:true,
      headerClass: 'header-center',
      resizable: false,
      valueFormatter: (params) => {
        if (params.value) {
          return params.value.toString().toUpperCase();
        }
        return '';
      },
    },
    {
      headerName: 'Scripts/Testsuite',
      field: 'scriptTestSuite',
      filter: 'agTextColumnFilter',
      sortable: true,
      tooltipField: 'scriptTestSuite',
      flex:2,
      resizable: false,
      cellRenderer:(params:any)=>{
        const text = params.value || '';
        if(text.length > 30){
          return `${text.slice(0,30)}...`;
        }
        return text;
      },
      cellClass: (params:any)=>{
        return params.value.length > 30 ? 'text-ellipsis' : 'text-two-line';
      },
      valueFormatter: (params) => {
        if (params.value) {
          return params.value.toString().toUpperCase();
        }
        return '';
      },
    },
    {
      headerName: 'Device',
      field: 'device',
      filter: 'agTextColumnFilter',
      sortable: true,
      tooltipField: 'device',
      cellClass: 'selectable',
      width:130,
      cellStyle:{'white-space': 'normal',' word-break': 'break-word'},
      wrapText:true,
      resizable: false,
      valueFormatter: (params) => {
        if (params.value) {
          return params.value.toString().toUpperCase();
        }
        return '';
      },
      
    },
    {
      headerName: 'Date Of Execution',
      field: 'executionDate',
      filter: 'agDateColumnFilter',
      filterParams: this.filterParams,
      flex:1.8,
      sortable: true,
      cellClass: 'selectable',
      resizable: false,
	    cellRenderer:(data:any)=>{
		    return data.value ? (new Date(data.value)).toLocaleString() : ''; 
	    }
    },
    {
      headerName: 'User',
      field: 'user',
      filter: 'agDateColumnFilter',
      filterParams: this.filterParams,
      width: 90,
      sortable: true,
      cellClass: 'selectable',
      resizable: false,
      valueFormatter: (params) => {
        if (params.value) {
          return params.value.toString().toUpperCase();
        }
        return '';
      },
    },
    {
      headerName: 'Result',
      field: 'status',
      filter: 'agTextColumnFilter',
      flex:1,
      cellStyle: { textAlign: "center" },
      sortable: true,
      resizable: false,
      cellClass: 'selectable',
      cellRenderer:(params:any)=>{
        const status = params.value;
        let iconHtml = '';
        switch(status){
          case 'SUCCESS':
            iconHtml = `<span style="color:#5BC866; font-size:0.66rem; font-weight:500;" title="Success">SUCCESS</span>`;
            break;
          case 'FAILURE':
            iconHtml = `<span style="color:#F87878; font-size:0.66rem; font-weight:500;" title="Failure">FAILURE</span>`;
            break;
          case 'INPROGRESS':
            iconHtml = `<span style=" color:#6460C1; font-size:0.66rem; font-weight:500;" title="Inprogress">INPROGRESS</span>`;
            break;
          case 'ABORTED':
            iconHtml = `<span style="color:#FFB237; font-size:0.66rem; font-weight:500;" title="Aborted">ABORTED</span>`;
            break;
          case 'PAUSE':
            iconHtml = `<span style="color:gray; font-size:0.66rem; font-weight:500;" title="Paused">PAUSE</span>`;
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
      width:115,
      sortable: false,
      headerClass: 'no-sort header-center',
      resizable: false,
      cellRenderer: ExecutionButtonComponent,
      cellRendererParams: (params: any) => ({
        onViewClick:this.openDetailsModal.bind(this),
        onDownloadClick:this.downloadExcel.bind(this),
        onAbortClick: this.onAbort.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    }
  ];
  defaultColDef ={
    sortable:true,
    headerClass: 'header-center',
  };
  public columnSchudle: ColDef[] = [
    {
      headerName: 'Job Name',
      field: 'jobName',
      filter: 'agTextColumnFilter',
      width:190,
      sortable: true,
      headerClass: 'header-center',
      resizable: false
    },
    {
      headerName: 'Execution Time',
      field: 'executionTime',
      filter: 'agTextColumnFilter',
      width:180,
      sortable: true,
      resizable: false,
      headerClass: 'header-center',
      cellRenderer: (params: any) => this.formatTime(params.value),
    },      
    {
      headerName: 'Scripts/Testsuite',
      field: 'scriptTestSuite',
      filter: 'agTextColumnFilter',
      flex: 2,
      sortable: true,
      resizable: false,
      headerClass: 'header-center',
    },
    {
      headerName: 'Device',
      field: 'device',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
      resizable: false,
      headerClass: 'header-center',
    },
    {
      headerName: 'Details',
      field: 'details',
      filter: 'agDateColumnFilter',
      filterParams: this.filterParams,
      flex: 1,
      sortable: true,
      resizable: false,
      headerClass: 'header-center',
    },
    {
      headerName: 'Status',
      field: 'status',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
      resizable: false,
      headerClass: 'header-center',
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      resizable: false,
      headerClass: 'no-sort header-center',
      flex: 1,
      cellRenderer: ScheduleButtonComponent,
      cellRendererParams: (params: any) => ({
        onDeleteClick: this.deleteSchedule.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    },
  ];
  gridOptions = {
    rowHeight: 45
  };
  gridOptionsHistory: GridOptions = { 
    getRowId: (params:any) => {
      return params.data.id;
   }
  };

  deviceStausArray: any[] = [];
  panelOpenState = false;
  selectedValue!: string;
  loggedinUser: any;
  userCategory!: string;
  preferedCategory!: string;
  selectedDfaultCategory!: string;
  categoryName!: string;
  toolTipText: string = "";
  resultDetailsData:any;
  private deviceStatusDestroy$ = new Subject<void>();
  executionDestroy$ = new Subject<void>();
  searchValue: string = '';
  selectedOption: string = '';
  dynamicList: string[] = [];
  defaultCategory!: string;
  private refreshSubscription!: Subscription;
  private scheduleSubscription!: Subscription;
  tabName!: string;
  searchTerm: string = '';
  filteredDeviceStausArray: any[] = []; 
  sortOrder: string = 'asc';
  private refreshdestroy$ = new Subject<void>();
  private allExecutionHistory$ = new Subject<void>();
  exeRefresh = true;
  scheduleRefresh = false;
  searchDevice ='';
  historyInterval:any;
  deviceInterval:any;
  showLoader =false;
  noDataFound : string = '';
  isNoDataVisible = false;

  constructor(
    private authservice: AuthService,
    private _snakebar: MatSnackBar,
    private loginService: LoginService,
    public resultDialog: MatDialog,
    public triggerDialog : MatDialog,
    public dialogTDK : MatDialog,
    public deleteDateDialog :MatDialog,
    private executionservice:ExecutionService,
    private clipboard: Clipboard,
  ) {
    this.loggedinUser = JSON.parse(
      localStorage.getItem('loggedinUser') || '{}'
    );
    this.userCategory = this.loggedinUser.userCategory;
    this.preferedCategory = localStorage.getItem('preferedCategory') || '';
  }
  /**
   * Initializes the component.
  */
  ngOnInit(): void {
    this.selectedDfaultCategory = this.preferedCategory?this.preferedCategory:this.userCategory;
    this.listenForLogout();
    this.getDeviceStatus();
    this.getAllExecutions();
    this.allExecutionScheduler();
    this.historyInterval = setInterval(() => {
      this.getAllExecutions();
    }, 60000);
    this.deviceInterval = setInterval(() => {
      this.getDeviceStatus();
    }, 10000);
  }
  refreshExeHistory():void{
    this.storeSelection();
    setTimeout(() => {
      this.getAllExecutions();
      setTimeout(() => {
      this.reSoreSelection();
      }, 100);
    }, 500);
  }
  refreshSchedule():void{
    this.allExecutionScheduler();
  }
  @HostListener('window:popstate', ['$event'])
  onPopState(event:Event){
   history.pushState(null, '', location.href);
  }

  /**
   * Initializes all the execution list.
  */
  getAllExecutions():void{
    this.storeSelection();
    if(this.selectedCategory === 'ExecutionName' && this.searchValue != ''){
      this.showLoader=true;
      this.executionservice.getAllExecutionByName(this.searchValue, this.selectedDfaultCategory,this.currentPage, this.pageSize).subscribe({
        next: (res) => {
          const data = JSON.parse(res);
          this.rowData = data.executions;
          this.totalItems = data.totalItems;
          this.showLoader = false; 
          setTimeout(() => {
            this.reSoreSelection();
          }, 100);
        },
        error: (err) => {
          if(err ==='No Executions available'){
            this.rowData = [];
            this.totalItems =0;
          }
        }
      })
    } else if(this.selectedCategory === 'Scripts/Testsuite' && this.searchValue != ''){
      this.showLoader=true;
      this.executionservice.getAllExecutionByScript(this.searchValue, this.selectedDfaultCategory,this.currentPage, this.pageSize).subscribe({
        next: (res) => {
          const data = JSON.parse(res);
          this.rowData = data.executions;
          this.totalItems = data.totalItems;
          this.showLoader = false; 
        },
        error: (err) => {
          if(err ==='No Executions available'){
            this.rowData = [];
            this.totalItems =0;
          }
        }
      })
    } else if(this.selectedCategory === 'Device' && this.searchValue != ''){
      this.showLoader=true;
      this.executionservice.getAllExecutionByDevice(this.searchValue, this.selectedDfaultCategory,this.currentPage, this.pageSize).subscribe({
        next: (res) => {
          const data = JSON.parse(res);
          this.rowData = data.executions;
          this.totalItems = data.totalItems;
          this.showLoader = false; 
        },
        error: (err) => {
          if(err ==='No Executions available'){
            this.rowData = [];
            this.totalItems =0;
          }
        }
      });
    } else if(this.selectedCategory === 'User' && this.selectedOption != ''){
      this.showLoader=true;
      this.executionservice.getAllExecutionByUser(this.selectedOption, this.selectedDfaultCategory, this.currentPage, this.pageSize).subscribe(res => {
        let data = JSON.parse(res);
        this.rowData = data.executions;
        this.totalItems = data.totalItems;
        this.showLoader = false; 
      });
    }
    else {
      this.showLoader=true;
      this.executionservice.getAllexecution(this.selectedDfaultCategory,this.currentPage, this.pageSize).subscribe({
        next:(res)=>{
          let data = JSON.parse(res);
          this.rowData = data.executions;
          this.totalItems = data.totalItems;
          this.showLoader = false; 
          setTimeout(() => {
            this.reSoreSelection();
          }, 0);
        },
        error:(err)=>{
          if(err ==='No Executions available'){
            this.rowData = [];
            this.totalItems =0;
          }
        }

      })
    }
    this.stayFocus();
  }
  stayFocus() {
    setTimeout(() => {
      if (document.activeElement === this.deviceSearchInput?.nativeElement) {
        this.deviceSearchInput.nativeElement.focus();
      } else if (document.activeElement === this.tableSearchInput?.nativeElement) {
        this.tableSearchInput.nativeElement.focus();
      }
    }, 100);
  }
  /**
   * This method is for change the page.
  */
  onPageChange(event: any): void {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    this.getAllExecutions();
  }
  /**
   * Event handler for when the grid is ready.
   * @param params - The GridReadyEvent object containing the grid API.
   */
  onGridReady(params: GridReadyEvent):void {
    this.gridApi = params.api;
  }

  onSelectionChange():void{
    this.selectedRowIds.clear();
    this.gridApi.getSelectedRows().forEach(node => {
      if(node.data){
        this.selectedRowIds.add(node.data.executionId)
      }
    })
    // const selectedNode = this.gridApi.getSelectedNodes()[0];
    // this.selectedRowIds = this.gridApi.getSelectedNodes().map(node => node.data.executionId);
  }
  storeSelection(){
    this.selectedRowIds.clear();
    if(this.gridApi){
      this.gridApi.getSelectedRows().forEach(row => this.selectedRowIds.add(row.executionId))
    }
  }
  reSoreSelection():void{
    if(!this.gridApi) return;
      this.gridApi.forEachNode((node:any)=>{
        if(this.selectedRowIds.has(node.data.executionId)){
          node.setSelected(true);
        }
      })
    
  }
  /**
   * This method is for change the category.
  */ 
  onCategoryChange(event:any): void {
    let val = event.target.value;
    this.deviceStausArray = [];
    this.rowData = [];
    if (val === 'RDKB') {
      this.categoryName = 'Broadband';
      this.selectedDfaultCategory = 'RDKB';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
      this.deviceStatusDestroy$.next();
      this.executionDestroy$.next();
      this.getDeviceStatus();
      this.getAllExecutions();
      this.allExecutionScheduler();
    } else if (val === 'RDKC') {
      this.categoryName = 'Camera';
      this.selectedDfaultCategory = 'RDKC';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
      this.deviceStatusDestroy$.next();
      this.executionDestroy$.next();
      this.getDeviceStatus();
      this.getAllExecutions();
      this.allExecutionScheduler();
    } else {
      this.selectedDfaultCategory = 'RDKV';
      this.categoryName = 'Video';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
      this.deviceStatusDestroy$.next();
      this.executionDestroy$.next();
      this.getDeviceStatus();
      this.getAllExecutions();
      this.allExecutionScheduler();
    }
  }
  /**
   * This method is for initialize the device status.
  */
  getDeviceStatus():void{

    const isInputFocused = document.activeElement === this.deviceSearchInput?.nativeElement;
    this.executionservice.getDeviceStatus(this.selectedDfaultCategory)
    .subscribe({
      next: (res) => {
          this.deviceStausArray = this.formatData(JSON.parse(res));
          this.filteredDeviceStausArray = [...this.deviceStausArray];
          if (isInputFocused) {
            setTimeout(() => {
              if (this.deviceSearchInput) {
                this.deviceSearchInput.nativeElement.focus();
                this.deviceSearchInput.nativeElement.setSelectionRange(
                  this.deviceSearchInput.nativeElement.value.length,
                  this.deviceSearchInput.nativeElement.value.length
                );
              }
            }, 0);
          }
          this.filterAndSortDevices(this.searchDevice);
          this.deviceStausArray[0].childData.forEach((element:any) => {
            this.toolTipText +=
            element.deviceName + '\n' +
            element.ip + '\n' +
            element.deviceType + '\n' +
            element.status + '\n';
          });
      },
      error: (err) => {
        this._snakebar.open(err, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
        })
      }

    })
    this.stayFocus();
  }
  /**
   * This method is for format the tree view of device status
  */
  formatData(data: any[]): any[]  {
    return [{
      name: 'Devices',
      childData: data,
      isOpen:true
    }];
  }
  /**
   * This method is for refresh the device status when click on refresh button.
  */
  refreshDevice():void{
    this.getDeviceStatus();
  }
  /**
   * After logout destroy the subject.
  */
  listenForLogout(): void {
    this.loginService.onLogout$.pipe(takeUntil(this.deviceStatusDestroy$)).subscribe(() => {
      this.deviceStatusDestroy$.next();
      this.deviceStatusDestroy$.complete();
    });
    this.destroyExecution();
  }
  /**
   * After logout destroy the subject.
  */  
  destroyExecution():void{
    this.loginService.onLogout$.pipe(takeUntil(this.executionDestroy$)).subscribe(() => {
      this.executionDestroy$.next();
      this.executionDestroy$.complete();
    });
  }
  /**
   * destroy the lifecycle hook.
  */  
  ngOnDestroy(): void {
    this.deviceStatusDestroy$.next();
    this.deviceStatusDestroy$.complete();
    this.executionDestroy$.next();
    this.executionDestroy$.complete();
    this.allExecutionHistory$.next();
    this.allExecutionHistory$.complete();
    if (this.refreshSubscription) {
      this.refreshSubscription.unsubscribe();
    }
    if (this.scheduleSubscription) {
      this.scheduleSubscription.unsubscribe();
    }
    this.refreshdestroy$.next();
    this.refreshdestroy$.complete();
    if (this.deviceInterval) {
      clearInterval(this.deviceInterval);
    }
    if (this.historyInterval) {
      clearInterval(this.historyInterval);
    }
  }
  /**
   * Initiallize the execution scheduler
  */
  allExecutionScheduler(){
    this.showLoader=true;
    this.isNoDataVisible = false;
    this.rowDataSchudle = [];
    this.executionservice.getAllexecutionScheduler(this.selectedDfaultCategory).subscribe({
      next:(res)=>{
        let data = JSON.parse(res);
        this.rowDataSchudle = data;
        this.showLoader = false;
        if (this.rowDataSchudle.length == 0) {
            this.isNoDataVisible = true;
            this.noDataFound = 'No Rows to Show';
        } else {
            this.isNoDataVisible = false;
        }
      },
      error:(err)=>{
          this._snakebar.open(err, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          });
        }
    })
  }
  /**
   * Conver the UTC time to local browser time.
  */
  formatTime(utcDate  : string) {
    const utcDateTime = new Date(utcDate);
   return utcDateTime.toLocaleString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
}
  /**
   * This methos is for change thunder enable/disable .
  */
  enableDisable(deviceIP:any):void{
    this.executionservice.toggleThunderEnabled(deviceIP).subscribe({
      next:(res)=>{
        this._snakebar.open(res, '', {
          duration: 3000,
          panelClass: ['success-msg'],
          verticalPosition: 'top'
        })
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
  /**
   * This method is for copy the device name .
  */    
  copyToClipboard(deviceIp: any): void {
    this.clipboard.copy(deviceIp);
    this._snakebar.open(`Copied: ${deviceIp}`, '', {
      duration: 3000,
      panelClass: ['success-msg'],
      horizontalPosition: 'end',
      verticalPosition: 'top'
    })
  }
  /**
   * Global search option method .
  */
  onFilterTextBoxChanged() {
    this.gridApi.setGridOption(
      'quickFilterText',
      (document.getElementById('filter-text-box') as HTMLInputElement).value
    );
  }

    /**
   * Handles the change event for the filter selection.
   * 
   * @param event - The event object containing the selected filter value.
   * 
   * Logs the selected filter value to the console and updates the `selectedCategory` property.
   * If the selected category is 'User', it fetches the list of users from the execution service
   * and updates the `dynamicList` property with the parsed response.
   * If the selected category is 'Device' or 'Scripts/Testsuite', it clears the `searchValue` property.
   */
    onFilterChange(event: any): void {
      this.selectedCategory = event.target.value;
      if (this.selectedCategory === 'User') {
        this.executionservice.getlistofUsers().subscribe(res => {
          this.dynamicList = JSON.parse(res)
        })
      } else if (this.selectedCategory === 'Device' || this.selectedCategory === 'Scripts/Testsuite' || this.selectedCategory === 'ExecutionName') {
        this.searchValue = '';
      }else{
        this.getAllExecutions();
      }
    }
 /**
   * Handles the search button click event.
   * Logs the search value and triggers the appropriate search function
   * based on the selected category.
   * 
   * If the selected category is 'Device', it calls `getAllExecutionByDevice`.
   * If the selected category is 'Scripts/Testsuite', it calls `getAllExecutionByScript`.
   * 
   * @returns {void}
   */
 onSearchClick(): void {
  if(this.selectedCategory === 'ExecutionName' || this.selectedCategory === 'Scripts/Testsuite' || this.selectedCategory === 'Device' && this.searchValue) {
      this.currentPage = 0;
      this.paginator.firstPage();
      this.getAllExecutions();
  }
  if(this.searchValue === ''){
    this.getAllExecutions();
  }
}
  /**
   * Handles the event when the user selection changes.
   * If a user is selected, it fetches all executions for the selected user,
   * the current category, and the current pagination settings.
   */
  onUserChange(): void {
    if (this.selectedOption != "") {
      this.currentPage = 0;
      this.paginator.firstPage();
      this.getAllExecutions();
    }else{
      this.getAllExecutions();
    }
  }

  /**
   * This method will open the result details modal.
  */
  openDetailsModal(params: any):void {
    localStorage.setItem('executionId', params.executionId);
    this.executionservice.resultDetails(params.executionId).subscribe(res=>{
       this.resultDetailsData = JSON.parse(res);
       this.resultDetailsData.executionId = params.executionId;
       if(this.resultDetailsData){
        let  resultDetailsModal  =  this.resultDialog.open(DetailsExeDialogComponent, {
          width: '99%',
          height: '96vh',
          maxWidth: '100vw',
          panelClass: 'custom-modalbox',
          data: this.resultDetailsData,
        });
        resultDetailsModal.afterClosed().subscribe(() => {
          this.getAllExecutions();
        });
      }
    })
  }

  /**
   * This method will downloadExcel of consolidated data.
  */  
  downloadExcel(params: any):void {
    if(params.executionId){
      this.executionservice.excelReportConsolidated(params.executionId).subscribe({
        next:(blob)=>{
          const xmlBlob = new Blob([blob], { type: 'application/xml' }); 
          const url = window.URL.createObjectURL(xmlBlob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${params.executionName}.xlsx`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        },
        error:(err)=>{
          let errmsg = JSON.parse(err.error);
          this._snakebar.open(errmsg,'',{
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
      });
    }
  }

  /**
   * This methos is for expand and collapse the accordian.
  */
  togglePanel(parent: any) {
    parent.isOpen = !parent.isOpen;
    // this.panelOpenState = !this.panelOpenState;
  }

  /**
   * This method will open the trigger execution modal.
  */ 
  openModalExecute(params:any){
    if(params.status ==='FREE'){
      const deviceExeModal = this.triggerDialog.open(ExecuteDialogComponent, {
        width: '68%',
        height: '96vh',
        maxWidth: '100vw',
        panelClass: 'custom-modalbox',
        data: {
          params
        },
        autoFocus: false,
      });
  
      deviceExeModal.afterClosed().subscribe(() => {
        setTimeout(() => {
        this.getAllExecutions();
        }, 2000);
      });
    }else{
      this._snakebar.open('The device is not available for execution','',{
        duration: 2000,
        panelClass: ['err-msg'],
        horizontalPosition: 'end',
        verticalPosition: 'top'
      })
    }

  }
  /**
   * This method will open the trigger execution modal.
  */  
  openDialog(normalExecutionClick:any) {
    const normalExeModal = this.triggerDialog.open(ExecuteDialogComponent, {
      width: '68%',
      height: '96vh',
      maxWidth: '100vw',
      panelClass: 'custom-modalbox',
      restoreFocus: false,
      data: {
        normalExecutionClick
      },
    });
    normalExeModal.afterClosed().subscribe(() => {
      setTimeout(() => {
      this.getAllExecutions();
      }, 2000);
    });
  }
  /**
   * Method for delete the execution single/ multiple.
   */
  deleteSelectedRows() : void {
    const selectedRows = this.gridApi.getSelectedRows();
    let executionArr = []
    for (let i = 0; i < selectedRows.length; i++) {
      const element = selectedRows[i].executionId;
      executionArr.push(element)
    }
    if (selectedRows.length === 0) {
      this._snakebar.open('Please select the executions','',{
        duration: 2000,
        panelClass: ['err-msg'],
        horizontalPosition: 'end',
        verticalPosition: 'top'
      })
    }else{
      if (confirm("Are you sure to delete ?")) {
        this.executionservice.deleteExecutions(executionArr).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 3000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
            this.getAllExecutions();
          },
          error:(err)=>{
            let errmsg = JSON.parse(err.error);
            this._snakebar.open(errmsg,'',{
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
  /**
   * This method will open the modal for delete by date.
  */  
  deleteDateModal():void{
    const deletedateModal = this.deleteDateDialog.open( DateDialogComponent,{
      width: '50%',
      height: '70vh',
      maxWidth:'100vw',
      panelClass: 'custom-modalbox',
        data:{
        }
    })
    deletedateModal.afterClosed().subscribe(() => {
      this.getAllExecutions();
    });
  }
  /**
   * This method is for delete the schedule.
  */ 
  deleteSchedule(data:any):void{
    if (confirm("Are you sure to delete ?")) {
      if(data){
        this.executionservice.deleteScheduleExe(data.id).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
              })
              this.allExecutionScheduler();
          },
          error:(err)=>{
            this._snakebar.open(err.error, '', {
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
  /**
   * This method for change the mat-tab.
  */   
  onTabClick(event: any): void {
    const label = event.tab.textLabel;
    this.tabName = label;
    if(this.tabName === 'Execution Schedules'){
      this.allExecutionScheduler();
      this.exeRefresh = false;
      this.scheduleRefresh = true;
    } else{
      this.exeRefresh = true;
      this.scheduleRefresh = false;
    }
  }
  /**
   * This method for abort the inprogress execution.
  */   
  onAbort(params: any):void{
    this.executionservice.abortExecution(params.executionId).subscribe({
      next:(res)=>{
        this._snakebar.open(res, '', {
          duration: 1000,
          panelClass: ['success-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
          })
      },
      error:(err)=>{
        this._snakebar.open(err, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
          })
      }
    })
  }
  filterAndSortDevices(seachDevice:string){
    this.performSearch(seachDevice);
    this.sortDevices();
  }

  searchDevices(event: Event) {
    const inputElement = event.target as HTMLInputElement;
    this.searchDevice = inputElement.value.toLowerCase();
    this.performSearch(this.searchDevice);
    setTimeout(() => {
      if (this.deviceSearchInput) {
        this.deviceSearchInput.nativeElement.focus();
        this.deviceSearchInput.nativeElement.setSelectionRange(
          this.deviceSearchInput.nativeElement.value.length,
          this.deviceSearchInput.nativeElement.value.length
        );
      }
    }, 0);
  }
  performSearch(term: string) :void{
    const lowerTerm = term.toLowerCase();
    const filteredChildData = this.deviceStausArray[0].childData.filter((device:any) => {
      return Object.values(device).some(value => {
        if (value === null || value === undefined) {
          return false;
        }
  
        if (typeof value === 'string') {
          return value.toLowerCase().includes(lowerTerm);
        } else if (typeof value === 'number') {
          return value.toString().includes(lowerTerm);
        } else if (typeof value === 'boolean') {
          return value.toString().includes(lowerTerm);
        }
        return false;
      });
    });

    this.filteredDeviceStausArray = [{
      name: 'Devices',
      childData: filteredChildData,
      isOpen: this.deviceStausArray[0].isOpen
    }];
    this.sortDevices();
  }
  clearSearch() :void{
    this.searchTerm = '';
    this.filteredDeviceStausArray = [...this.deviceStausArray];
    this.sortDevices();
  }
  toggleSortOrder():void{
    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    this.sortDevices();
  }
  sortDevices() :void{
    const order = this.sortOrder;
    const statusOrder : { [key: string]: number } = {
      'busy': 1,
      'in_use': 2,
      'free': 3,
      'not_found': 4,
      'hang': 5
    };
    this.filteredDeviceStausArray[0].childData.sort((a:any, b:any) => {
      const firstStatus = a.status.toLowerCase();
      const secondStatus = b.status.toLowerCase();
  
      const firstValue = statusOrder[firstStatus] || 999;
      const secondValue = statusOrder[secondStatus] || 999;
  
     if (firstValue!== secondValue) {
      return order === 'asc'? firstValue - secondValue: secondValue - firstValue;
    } else {
      const firstDeviceName = a.deviceName.toLowerCase();
      const secondDeviceName = b.deviceName.toLowerCase();
      return order === 'asc'? firstDeviceName.localeCompare(secondDeviceName): secondDeviceName.localeCompare(firstDeviceName);
    }
    });
  }

  installTDKModal(deviceName:string){
    const dialogModal = this.dialogTDK.open(TdkInstallComponent, {
      width: '68%',
      height: '96vh',
      maxWidth: '100vw',
      panelClass: 'custom-modalbox',
      restoreFocus: false,
      data:deviceName,
    });
    dialogModal.afterClosed().subscribe(() => {

    });
  }


}
