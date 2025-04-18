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
  ValidationErrors,
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
  GridReadyEvent,
  IDateFilterParams,
} from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { AgGridAngular } from 'ag-grid-angular';
import { MatSnackBar } from '@angular/material/snack-bar';
import { LoaderComponent } from '../../utility/component/loader/loader.component';

@Component({
  selector: 'app-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, MaterialModule,AgGridAngular,LoaderComponent],
  templateUrl: './analysis.component.html',
  styleUrl: './analysis.component.css',
})
export class AnalysisComponent {
  selectedDfaultCategory: string = '';
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
  finalBaseName!: string;
  compNamesArr:any;
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
      flex:2,
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
      flex:2,
      tooltipField: 'scriptTestSuite',
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
     flex:1,
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
 
  ];
  defaultColDef ={
    sortable:true,
    headerClass: 'header-center',
  };
  selectedRowName: string | null = null;
  pageSize = 10;
  pageSizeSelector: number[] | boolean = [10, 20, 30, 50];
  showTable = false;
  selectedExecutions: any[] = [];
  selectedExecutionNames: string[] = [];
  selectionErrorMessage: string = '';
  showReportBtn = false;
  showLoader = false;

  constructor(
    private authservice: AuthService,
    private fb: FormBuilder,
    public baseDialog: MatDialog,
    public comparisonDialog: MatDialog,
    private deviceTypeService: DevicetypeService,
    private anlysisService:AnalysisService,
    private _snakebar: MatSnackBar,
  ) {
    this.loggedinUser = JSON.parse(
      localStorage.getItem('loggedinUser') || '{}'
    );
    this.userCategory = this.loggedinUser.userCategory;
    this.preferedCategory = localStorage.getItem('preferedCategory') || '';
    // this.selectedDfaultCategory = this.loggedinUser.userCategory;
  }

  ngOnInit(): void {
    this.selectedDfaultCategory = this.preferedCategory
      ? this.preferedCategory
      : this.userCategory;
    this.reportForm = this.fb.group({
      baseName: ['', Validators.required],
      comparisonName: ['', [Validators.required, this.validateBaseNotInComparison.bind(this)]],
    });
    this.combinedForm = this.fb.group(
      {
        fromDate: ['', Validators.required],
        toDate: ['', Validators.required],
        deviceType: ['', Validators.required],
        executionType: ['', Validators.required],
        category: [{value:this.selectedDfaultCategory, disabled:true}],
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
      });
  }
  categoryChange(event:any): void {
    let val = event.target.value;
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
  /** Custom Validator: Check if baseName exists in comparisonName */
  validateBaseNotInComparison(control: AbstractControl): ValidationErrors | null {
    const comparisonIds = this.compNamesArr?.map((item:any) => item.id) || [];

    if (this.finalBaseName && comparisonIds.includes(this.finalBaseName)) {
      return { baseFoundInComparison: true };
    }
    return null;
  }

/** Update Form Control when the user edits the textarea manually */
    updateComparisonFormValue(event: Event) {
      const inputValue = (event.target as HTMLTextAreaElement).value;
      const newNames = inputValue.split(',').map(name => name.trim()).filter(name => name);
      this.compNamesArr = this.compNamesArr.filter((item:any) => newNames.includes(item.name));
  
      this.selectComparisonNames = newNames.join(', ');
      this.reportForm.patchValue({ comparisonName: this.selectComparisonNames });
      this.reportForm.get('comparisonName')?.updateValueAndValidity();
    }
  compReportSubmit(): void {
    this.reportSubmitted = true;
    if (this.reportForm.invalid) {
      return;
    }else{
        this.anlysisService.compReportGenerate(this.finalBaseName,this.compNamesArr.map((item:any) => item.id)).subscribe({
          next:(blob)=>{
            const xmlBlob = new Blob([blob], { type: 'application/xml' }); 
            const url = window.URL.createObjectURL(xmlBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${this.selectExecutionName}_comparisionreport.xlsx`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
          },
          error:(err)=>{
          }
        });
    }
  }
  openModal() {
    const dialogRef = this.baseDialog.open(BaseModalComponent, {
      width: '85%',
      height: '97vh',
      maxWidth: '100vw',
      panelClass: 'report-basemodal',
      data: {
        tabname:this.tabName,
        category:this.selectedDfaultCategory
      }
    });
    dialogRef.afterClosed().subscribe((res) => {
      if (res) {
        this.finalBaseName = res.executionId;
        this.selectExecutionName = res.executionName;
        this.reportForm.patchValue({
          baseName: this.selectExecutionName
        });
      }
    });
  }
  comparisonModal() {
    const dialogRef = this.comparisonDialog.open(ComparisonModalComponent, {
      width: '85%',
      height: '97vh',
      maxWidth: '100vw',
      panelClass: 'report-modalbox',
      data:  {
        tabname:this.tabName,
        category:this.selectedDfaultCategory
      }
    });
    dialogRef.afterClosed().subscribe((res: any[]) => {
      if (res) {
        const selectedNames = res.map((row:any)=>row.executionName);
        const selectExecutionId = res.map((row:any)=>row.executionId);
        this.compNamesArr = selectExecutionId.map((id, index) => ({ id, name: selectedNames[index] }));
        this.selectComparisonNames = selectedNames.join(', ');
        this.reportForm.patchValue({
          comparisonName: this.selectComparisonNames
        });
        this.reportForm.get('comparisonName')?.updateValueAndValidity();
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
        const utcMoment = moment.tz(locaFromDateTime, moment.tz.guess()).startOf('day');
        this.combinedFromUTC = utcMoment.format('YYYY-MM-DDTHH:mm:ss[Z]');
      }
      if (locaToDateTime) {
        const utcMoment = moment.tz(locaToDateTime, moment.tz.guess()).endOf('day');
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
      this.showLoader = true;
      this.anlysisService.getcombinedByFilter(obj).subscribe(res=>{
        let response = JSON.parse(res);
        if(response){
          this.rowData = response;
          this.showTable = true;
          this.showLoader = false;
        }else{
          this.rowData = [];
          this.showTable = true;
          this.showLoader = false;
        }
      })
    }
  }

  onSelectionChanged() {
    this.selectedExecutions = this.gridApi.getSelectedRows();
    this.updateSelectedExecutionNames();
  }
  updateSelectedExecutionNames() {
    this.selectionErrorMessage = '';
    if (this.selectedExecutions.length < 2 || this.selectedExecutions.length > 10) {
      this.selectionErrorMessage = 'Number of executions selected must be between 2 and 10';
      this.showReportBtn = false;
      this.selectedExecutionNames = [];
      return;
    }
    if(this.selectedExecutions.length > 2 || this.selectedExecutions.length <= 10){
      this.showReportBtn = true;
    }else{
      this.showReportBtn = false;
    }
    this.selectedExecutionNames = this.selectedExecutions.map(execution => execution.executionId);
  }

  generateReport():void{
    if(this.selectedExecutionNames){
      this.anlysisService.combinnedReportGenerate(this.selectedExecutionNames).subscribe({
        next:(blob)=>{
          const xmlBlob = new Blob([blob], { type: 'application/xml' }); 
          const url = window.URL.createObjectURL(xmlBlob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `CombinedResultExecution.xlsx`;
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
}
