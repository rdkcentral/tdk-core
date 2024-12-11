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
import { Component, ViewChild } from '@angular/core';
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
import { Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { ExecutionButtonComponent } from '../../utility/component/execution-button/execution-button.component';
import { DetailsExeDialogComponent } from '../../utility/component/details-execution/details-exe-dialog/details-exe-dialog.component';
import { ExecutionService } from '../../services/execution.service';
import { ExecuteDialogComponent } from '../../utility/component/execute-dialog/execute-dialog.component';
import { interval, startWith, Subject, Subscription, switchMap, takeUntil } from 'rxjs';
import { Clipboard } from '@angular/cdk/clipboard';
import { LoginService } from '../../services/login.service';
import { ExecutionCheckboxComponent } from '../../utility/component/execution-button/execution-checkbox/execution-checkbox.component';
import { DateDialogComponent } from '../../utility/component/date-dialog/date-dialog.component';
import { MatPaginator } from '@angular/material/paginator';
import { ScheduleButtonComponent } from '../../utility/component/execution-button/schedule-button.component';

@Component({
  selector: 'app-execution',
  standalone: true,
  imports: [
    CommonModule,
    AgGridAngular,
    FormsModule,
    ReactiveFormsModule,
    MaterialModule,
  ],
  templateUrl: './execution.component.html',
  styleUrl: './execution.component.css',
})
export class ExecutionComponent {

  @ViewChild(MatPaginator) paginator!: MatPaginator;
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
  schedulePageSizeSelector: number[] | boolean = [5, 10, 30, 50];
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
      headerCheckboxSelection: true,
      checkboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      headerComponent: ExecutionCheckboxComponent,
      headerComponentParams: {
        label: 'Select All',
        deleteCallback: () => this.deleteSelectedRows(),
      },
      width: 70,
    },
    {
      headerName: 'Execution Name',
      field: 'executionName',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
      tooltipField: 'executionName',
      cellClass: 'selectable',
    },
    {
      headerName: 'Scripts/Testsuite',
      field: 'scriptTestSuite',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
      tooltipField: 'scriptTestSuite',
      cellClass: 'selectable',
    },
    {
      headerName: 'Device',
      field: 'device',
      filter: 'agTextColumnFilter',
      width: 140,
      sortable: true,
      tooltipField: 'device',
      cellClass: 'selectable',
    },
    {
      headerName: 'Date Of Execution',
      field: 'executionDate',
      filter: 'agDateColumnFilter',
      filterParams: this.filterParams,
      width:180,
      sortable: true,
      cellClass: 'selectable',
	    cellRenderer:(data:any)=>{
		    return data.value ? (new Date(data.value)).toLocaleString() : ''; 
	    }
    },
    {
      headerName: 'User',
      field: 'user',
      filter: 'agDateColumnFilter',
      filterParams: this.filterParams,
      width: 80,
      sortable: true,
      cellClass: 'selectable',
    },
    {
      headerName: 'Result',
      field: 'status',
      filter: 'agTextColumnFilter',
      width: 90,
      cellStyle: { textAlign: "center" },
      sortable: true,
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
          case 'ABORT':
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
    {
      headerName: 'Action',
      field: '',
      width:130,
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
  public columnSchudle: ColDef[] = [
    {
      headerName: 'Job Name',
      field: 'jobName',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Execution Time',
      field: 'executionTime',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
      cellRenderer: (params: any) => this.formatTime(params.value),
    },      
    {
      headerName: 'Scripts/Testsuite',
      field: 'scriptTestSuite',
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
      headerName: 'Status',
      field: 'status',
      filter: 'agTextColumnFilter',
      width: 110,
      sortable: true,
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      headerClass: 'no-sort',
      width: 130,
      cellRenderer: ScheduleButtonComponent,
      cellRendererParams: (params: any) => ({
        onDeleteClick: this.deleteSchedule.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    },
  ];
  gridOptions = {
    // rowHeight: 30,
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

  constructor(
    private authservice: AuthService,
    private _snakebar: MatSnackBar,
    private loginService: LoginService,
    public resultDialog: MatDialog,
    public triggerDialog :MatDialog,
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
    let localcategory = this.preferedCategory?this.preferedCategory:this.userCategory;
    this.defaultCategory = localcategory;
    this.onCategoryChange(localcategory);
    this.listenForLogout();
    this.getDeviceStatus();
    this.getAllExecutions(localcategory, this.currentPage, this.pageSize);
    this.scheduleSubscription = interval(2000).subscribe(() => {
      this.allExecutionScheduler();
    });
  }
  /**
   * Initializes all the execution list.
  */
  getAllExecutions(category: string,page: number, size: number):void{
    this.executionservice.getAllexecution(category,page,size).subscribe({
      next:(res)=>{
        let data = JSON.parse(res);
        this.rowData = data.executions;
        this.totalItems = data.totalItems;
      },
      error:(err)=>{
      }
    })
  }
  /**
   * This method is for change the page.
  */
  onPageChange(event: any): void {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    this.getAllExecutions(this.userCategory,this.currentPage, this.pageSize);
  }
  /**
   * Event handler for when the grid is ready.
   * @param params - The GridReadyEvent object containing the grid API.
   */
  onGridReady(params: GridReadyEvent):void {
    this.gridApi = params.api;
  }
  /**
   * This method is for change the category.
  */ 
  onCategoryChange(val: string): void {
    this.deviceStausArray = [];
    this.rowData = [];
    if (val === 'RDKB') {
      this.categoryName = 'Broadband';
      this.selectedDfaultCategory = 'RDKB';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
      this.deviceStatusDestroy$.next();
      this.executionDestroy$.next();
      this.getDeviceStatus();
      this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
    } else if (val === 'RDKC') {
      this.categoryName = 'Camera';
      this.selectedDfaultCategory = 'RDKC';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
      this.deviceStatusDestroy$.next();
      this.executionDestroy$.next();
      this.getDeviceStatus();
      this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
    } else {
      this.selectedDfaultCategory = 'RDKV';
      this.categoryName = 'Video';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
      this.deviceStatusDestroy$.next();
      this.executionDestroy$.next();
      this.getDeviceStatus();
      this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
    }
  }
  /**
   * This method is for initialize the device status.
  */
  getDeviceStatus():void{
    interval(10000)
    .pipe(
      startWith(0),
      takeUntil(this.deviceStatusDestroy$),
      switchMap(() => {
        return this.executionservice.getDeviceStatus(this.selectedDfaultCategory);
      })
    )
    .subscribe({
      next: (res) => {
        setTimeout(() => {
          this.deviceStausArray = this.formatData(JSON.parse(res));
          this.deviceStausArray[0].childData.forEach((element:any) => {
            this.toolTipText +=
            element.deviceName + '\n' +
            element.ip + '\n' +
            element.deviceType + '\n' +
            element.status + '\n';
         
          });
        }, 3000);
      },
      error: (err) => {
        this._snakebar.open(err.error, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
        })
      }  
    })
  }
  /**
   * This method is for format the tree view of device status
  */
  formatData(data: any[]): any[]  {
    return [{
      name: 'Devices',
      childData: data
    }];
  }
  /**
   * This method is for refresh the device status when click on refresh button.
  */
  refreshDevice():void{
    this.executionservice.getDeviceStatus(this.selectedDfaultCategory).subscribe({
      next: (res) => {
        setTimeout(() => {
          this.deviceStausArray = this.formatData(JSON.parse(res));
          this.deviceStausArray[0].childData.forEach((element:any) => {
            this.toolTipText +=
            element.name + "\n" + element.ip + "\n" + element.deviceType + "\n" + element.status
          });
        }, 3000);
      },
      error: (err) => {
        this._snakebar.open(err.error, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
        })
      } 
    })
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
    if (this.refreshSubscription) {
      this.refreshSubscription.unsubscribe();
    }
    if (this.scheduleSubscription) {
      this.scheduleSubscription.unsubscribe();
    }
  }
  /**
   * Initiallize the execution scheduler
  */
  allExecutionScheduler(){
    this.executionservice.getAllexecutionScheduler().subscribe(res=>{
      this.rowDataSchudle = JSON.parse(res);
    })
  }
  /**
   * Conver the UTC time to local browser time.
  */
  formatTime(utcDate  : string): string {
    const parts = utcDate.split(/[T:Z-]/).map(Number);
    const localDateObj = new Date(parts[0], parts[1] - 1, parts[2], parts[3], parts[4], parts[5]);
  return localDateObj.toLocaleString('en-US', {
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
        this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
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
  if (this.selectedCategory === 'Device') {
    if(this.searchValue){
    this.getAllExecutionByDevice(this.searchValue, this.defaultCategory, this.currentPage, this.pageSize);
    }else if(this.searchValue === ''){
      this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
    }
  }
  if (this.selectedCategory === 'Scripts/Testsuite') {
    if(this.searchValue){
      this.getAllExecutionByScript(this.searchValue, this.defaultCategory, this.currentPage, this.pageSize);
    }else if(this.searchValue === ''){
      this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
    }
  }
  if(this.selectedCategory === 'ExecutionName') {
    if(this.searchValue){
    this.getAllExecutionByName(this.searchValue, this.defaultCategory, this.currentPage, this.pageSize);
    }else if(this.searchValue === ''){
      this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
    }
  }
}
  /**
   * This methos is for filter the execution by name .
  */
getAllExecutionByName(searchQuery: string, category: string, page: number, size: number): void{
  this.executionservice.getAllExecutionByName(searchQuery, category, page, size).subscribe({
    next: (res) => {
      const data = JSON.parse(res);
      this.rowData = data.executions;
      this.totalItems = data.totalItems;
    },
    error: (err) => {
      let errmsg = err.error;
      this._snakebar.open(errmsg, '', {
        duration: 2000,
        panelClass: ['err-msg'],
        horizontalPosition: 'end',
        verticalPosition: 'top'
      })
    }
  })
}
  /**
   * Handles the event when the user selection changes.
   * If a user is selected, it fetches all executions for the selected user,
   * the current category, and the current pagination settings.
   */
  onUserChange(): void {
    if (this.selectedOption) {
      this.currentPage = 0;
      this.paginator.firstPage();
      this.getAllExecutionByUser(this.selectedOption, this.defaultCategory, this.currentPage, this.pageSize);
    }
  }
  /**
   * Fetches all execution data by device based on the provided search query, category, page, and size.
   * 
   * @param searchQuery - The search query string to filter the executions.
   * @param category - The category to filter the executions.
   * @param page - The page number for pagination.
   * @param size - The number of items per page for pagination.
   * 
   * @returns void
   */
  getAllExecutionByDevice(searchQuery: string, category: string, page: number, size: number): void {
    this.executionservice.getAllExecutionByDevice(searchQuery, category, page, size).subscribe({
      next: (res) => {
        const data = JSON.parse(res);
        this.rowData = data.executions;
        this.totalItems = data.totalItems;
      },
      error: (err) => {
        let errmsg = err.error;
        this._snakebar.open(errmsg, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
        });
      }
    });
  }
    /**
   * Fetches all executions by script based on the provided search query, category, page, and size.
   * Updates the component's rowData and totalItems properties with the fetched data.
   * Displays an error message using a snackbar if the request fails.
   *
   * @param {string} searchQuery - The search query to filter executions.
   * @param {string} category - The category to filter executions.
   * @param {number} page - The page number for pagination.
   * @param {number} size - The number of items per page for pagination.
   * @returns {void}
   */
    getAllExecutionByScript(searchQuery: string, category: string, page: number, size: number): void {
      this.executionservice.getAllExecutionByScript(searchQuery, category, page, size).subscribe({
        next: (res) => {
          const data = JSON.parse(res);
          this.rowData = data.executions;
          this.totalItems = data.totalItems;
        },
        error: (err) => {
          let errmsg = err.error;
          this._snakebar.open(errmsg, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
      })
    }
  /**
   * Fetches all execution records for a specific user and category with pagination.
   *
   * @param {string} username - The username of the user whose execution records are to be fetched.
   * @param {string} category - The category of execution records to be fetched.
   * @param {number} page - The page number for pagination.
   * @param {number} size - The number of records per page.
   * @returns {void} This method does not return a value.
   */
  getAllExecutionByUser(username: string, category: string, page: number, size: number): void {
    this.executionservice.getAllExecutionByUser(username, category, page, size).subscribe(res => {
      let data = JSON.parse(res);
      this.rowData = data.executions;
      this.totalItems = data.totalItems;
    });
  }
  userEdit():void {}
  delete():void {}
  /**
   * This method will open the result details modal.
  */
  openDetailsModal(params: any):void {
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
          this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
        });
      }
    })
  }
  downloadXML():void {}
  /**
   * This methos is for expand and collapse the accordian.
  */
  togglePanel(parent: any) {
    parent.isOpen = !parent.isOpen;
    this.panelOpenState = !this.panelOpenState;
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
        this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
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
      data: {
        normalExecutionClick
      },
    });
    normalExeModal.afterClosed().subscribe(() => {
      this.getAllExecutions(this.selectedDfaultCategory, this.currentPage, this.pageSize);
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
      this._snakebar.open('Please select the execution','',{
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
            this.rowData = this.rowData.filter((row:any) => !selectedRows.includes(row));
            this.totalItems -= selectedRows.length;
            // const rowToRemove = this.rowData.find((row:any) => row.id === this.rowData);
            // if (rowToRemove) {
            //   this.gridApi.applyTransaction({ remove: [rowToRemove] });
            // }
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
    this.deleteDateDialog.open( DateDialogComponent,{
      width: '50%',
      height: '70vh',
      maxWidth:'100vw',
      panelClass: 'custom-modalbox',
        data:{
        
        }
    })
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
              const rowToRemove = this.rowDataSchudle.find((row:any) => row.id === data.id);
              if (rowToRemove) {
                this.gridApi.applyTransaction({ remove: [rowToRemove] });
              }
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
  }
}
