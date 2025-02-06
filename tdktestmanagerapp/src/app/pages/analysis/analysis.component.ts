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
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { AuthService } from '../../auth/auth.service';
import { MaterialModule } from '../../material/material.module';
import { MatDialog } from '@angular/material/dialog';
import { BaseModalComponent } from './base-modal/base-modal.component';
import { ComparisonModalComponent } from './comparison-modal/comparison-modal.component';
import { DevicetypeService } from '../../services/devicetype.service';
import moment from 'moment-timezone';
import { AnalysisService } from '../../services/analysis.service';
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

@Component({
  selector: 'app-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, MaterialModule,AgGridAngular],
  templateUrl: './analysis.component.html',
  styleUrl: './analysis.component.css',
})
export class AnalysisComponent {
  selectedDfaultCategory!: string;
  categoryName!: string;
  loggedinUser: any;
  userCategory!: string;
  preferedCategory!: string;
  scriptShow = true;
  showTestSuite = false;
  reportSubmitted = false;
  reportForm!: FormGroup;
  combinedSubmitted = false;
  combinedForm!: FormGroup;
  selectExecutionName!: string;
  selectComparisonNames: string = '';
  baseCombinedName!: string;
  CombinedExecutions: string = '';
  tabName: string = 'Comparsion Report';
  allDeviceType: any;
  deviceName!: string;
  executionTypeName!: string;
  showScript = false;
  testSuiteShow = false;
  combinedFromUTC!: string;
  combinedToUTC!: string;
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
  showTable = false;

  constructor(
    private authservice: AuthService,
    private fb: FormBuilder,
    public baseDialog: MatDialog,
    public comparisonDialog: MatDialog,
    private deviceTypeService: DevicetypeService,
    private anlysisService:AnalysisService
  ) {
    this.loggedinUser = JSON.parse(
      localStorage.getItem('loggedinUser') || '{}'
    );
    this.userCategory = this.loggedinUser.userCategory;
    this.preferedCategory = localStorage.getItem('preferedCategory') || '';
  }

  ngOnInit(): void {
    let localcategory = this.preferedCategory
      ? this.preferedCategory
      : this.userCategory;
    this.categoryChange(localcategory);
    this.reportForm = this.fb.group({
      baseName: ['', Validators.required],
      comparisonName: ['', Validators.required],
    });
    this.combinedForm = this.fb.group(
      {
        fromDate: ['', Validators.required],
        toDate: ['', Validators.required],
        deviceType: ['', Validators.required],
        executionType: ['', Validators.required],
        category: [this.selectedDfaultCategory, Validators.required],
        scriptSingle: [''],
        testSuiteSingke: [''],
      },
      {
        validators: this.dateRangeValidator,
      }
    );
    this.getDeviceByCategory();
  }

  onGridReady(params: GridReadyEvent):void {
    this.gridApi = params.api;
  }

  dateRangeValidator(group: AbstractControl): { [key: string]: any } | null {
    const fromDate = group.get('fromDate')?.value;
    const toDate = group.get('toDate')?.value;
    if (fromDate && toDate) {
      const diff = moment(toDate).diff(moment(fromDate), 'days');
      return diff > 30 ? { maxDaysExceeded: true } : null;
    }
    return null;
  }
  getDeviceByCategory(): void {
    this.deviceTypeService
      .getfindallbycategory(this.selectedDfaultCategory)
      .subscribe((res) => {
        this.allDeviceType = JSON.parse(res);
        console.log(this.allDeviceType);
      });
  }
  categoryChange(val: string): void {
    if (val === 'RDKB') {
      this.categoryName = 'Broadband';
      this.selectedDfaultCategory = 'RDKB';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
      this.getDeviceByCategory();
    } else if (val === 'RDKC') {
      this.categoryName = 'Camera';
      this.selectedDfaultCategory = 'RDKC';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
    } else {
      this.selectedDfaultCategory = 'RDKV';
      this.categoryName = 'Video';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
      this.getDeviceByCategory();
    }
  }

  resultChange(event: any): void {}

  deviceChange(event: any): void {
    let val = event.target.value;
    this.deviceName = val;
    console.log(this.deviceName);
  }
  changeExecutionType(event: any): void {
    let val = event.target.value;
    this.executionTypeName = val;
    if (this.executionTypeName === 'SINGLESCRIPT') {
      this.showScript = true;
    } else {
      this.showScript = false;
    }
    if (this.executionTypeName === 'TESTSUITE') {
      this.testSuiteShow = true;
    } else {
      this.testSuiteShow = false;
    }
  }

  onTabClick(event: any): void {
    const label = event.tab.textLabel;
    if (label === 'Combined Report') {
      this.tabName = 'Combined Report';
    } else {
      this.tabName = 'Comparsion Report';
    }
  }
  reportSubmit(): void {
    this.reportSubmitted = true;
    if (this.reportForm.invalid) {
      return;
    }
  }
  openModal() {
    const dialogRef = this.baseDialog.open(BaseModalComponent, {
      width: '85%',
      height: '90vh',
      maxWidth: '100vw',
      panelClass: 'report-modalbox',
      data: this.tabName,
    });
    dialogRef.afterClosed().subscribe((res) => {
      if (res) {
        this.selectExecutionName = res;
      }
    });
  }
  comparisonModal() {
    const dialogRef = this.comparisonDialog.open(ComparisonModalComponent, {
      width: '85%',
      height: '90vh',
      maxWidth: '100vw',
      panelClass: 'report-modalbox',
      data: this.tabName,
    });
    dialogRef.afterClosed().subscribe((res: string[]) => {
      if (res) {
        this.selectComparisonNames = res.join(', ');
      }
    });
  }

  onCombinedSubmit(): void {
    this.combinedSubmitted = true;
    if (this.combinedForm.invalid) {
      return;
    } else {
      const locaFromDateTime = this.combinedForm.get('fromDate')?.value;
      const locaToDateTime = this.combinedForm.get('toDate')?.value;
      if (locaFromDateTime) {
        const utcMoment = moment.tz(locaFromDateTime, moment.tz.guess()).utc();
        this.combinedFromUTC = utcMoment.format('YYYY-MM-DDTHH:mm:ss[Z]');
      }
      if (locaToDateTime) {
        const utcMoment = moment.tz(locaToDateTime, moment.tz.guess()).utc();
        this.combinedToUTC = utcMoment.format('YYYY-MM-DDTHH:mm:ss[Z]');
      }
      let obj = {
        "startDate": this.combinedFromUTC,
        "endDate": this.combinedToUTC,
        "executionType": this.executionTypeName,
        "scriptTestSuite": '',
        "deviceType": this.deviceName,
        "category": this.selectedDfaultCategory
        
      };
      console.log(obj);
      this.anlysisService.getcombinedByFilter(obj).subscribe(res=>{
        let response = JSON.parse(res);
        if(response){
          this.rowData = response;
          this.showTable = true;
        }else{
          this.showTable = false;
        }
      })
    }
  }
}
