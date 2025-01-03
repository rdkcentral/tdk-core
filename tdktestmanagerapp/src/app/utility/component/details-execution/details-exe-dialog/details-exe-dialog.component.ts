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
import { Component, Inject, ViewChild, ViewEncapsulation } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { MaterialModule } from '../../../../material/material.module';
import { ChartComponent, NgApexchartsModule } from 'ng-apexcharts';
import { FormsModule } from '@angular/forms';
import { LivelogDialogComponent } from '../livelog-dialog/livelog-dialog.component';
import { LogfileDialogComponent } from '../logfile-dialog/logfile-dialog.component';
import { ExecutionService } from '../../../../services/execution.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { interval, startWith, Subject, switchMap, takeUntil } from 'rxjs';

export type ChartOptions = {
  series: Array<{
    data: number[];
  }>;
  chart: ApexChart;
  dataLabels: ApexDataLabels;
  responsive: ApexResponsive[];
  legend: any | "";
  labels: any | "";
  colors: any | "";
  plotOptions: ApexPlotOptions;
  yaxis: ApexYAxis;
  xaxis: ApexXAxis;
  fill: ApexFill;
  title: ApexTitleSubtitle;
};

@Component({
  selector: 'app-details-exe-dialog',
  standalone: true,
  imports: [CommonModule,MaterialModule,FormsModule,NgApexchartsModule],
  templateUrl: './details-exe-dialog.component.html',
  styleUrl: './details-exe-dialog.component.css'
})
export class DetailsExeDialogComponent {
  @ViewChild("chart") chart!: ChartComponent;
  public chartOptions!: Partial<ChartOptions> | any;
  encapsulation!: ViewEncapsulation.None;
  public themeClass: string = "ag-theme-quartz";
  rowData: any = [];
  rowDataSchudle:any =[];
  executionResultData:any;
  panelOpenState = false;
  allChecked = false;
  selectedDetails: any[] = [];
  filteredData:any[] = [];
  filterStatus = 'all';
  scriptDetailsData:any;
  trendsArr : string[]=[];
  isFlipped = false;
  moduleTableTitle:any;
  moduleTableData:any;
  keys: string[] = [];
  formatLogs: any;
  executionResultId:any;
  logFileNames: string[] = [];
  executionId!: string;
  liveLogsData:any;
  liveLogDestroy$ = new Subject<void>();
  devideDetails:any;
  loggedinUser: any;

  constructor(
    public dialogRef: MatDialogRef<DetailsExeDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, public liveLogDialog:MatDialog, public logFilesDialog:MatDialog, private executionservice: ExecutionService,private _snakebar :MatSnackBar) {
    
    }
  /**
   * Lifecycle hook that is called after data-bound properties of a directive are initialized.
   * Initializes the component by calling several methods to set up result details, pie chart data,
   * and module-wise execution summary. Additionally, it processes device details by replacing
   * newline characters with HTML line break elements.
   *
   * @returns {void}
   */
  ngOnInit(): void {
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
    this.resultDetails();
    this.pieChartData();
    this.modulewiseExeSummary();
    let details = this.data.deviceDetails
    this.devideDetails = details.replace(/\n/g, '<br>');
  }
  /**
   * Generates and sets the options for a pie chart based on the summary data.
   * 
   * This method extracts data from the `summaryData` object and dynamically creates
   * the series, labels, and colors for the pie chart. It filters out any data points
   * with a value of 0 and constructs the chart options accordingly.
   * 
   * The chart options include:
   * - Series data
   * - Chart type and height
   * - Plot options to disable expand on click
   * - Labels for the pie slices
   * - Legend position
   * - Colors for the pie slices
   * - Data labels with custom formatting
   * 
   * @returns {void}
   */
  pieChartData():void{
    const summaryData = this.data?.summary || {};
    const fullLabels = [
      'Success',
      'Failure',
      'InProgress',
      'N/A',
      'Timeout',
      'Pending',
      'Skipped',
      'Aborted',
    ];

    const fullColors = [
      "#00ff00",
      "#f5425a",
      "#ffff00",
      "#cccccc",
      "#ff9933",
      "#5353c6",
      "#ffbf80",
      "#800000",
    ];

    // Extract data for series and labels dynamically
    const series = [
      summaryData.success || 0,
      summaryData.failure || 0,
      summaryData.inProgressCount || 0,
      summaryData.na || 0,
      summaryData.timeout || 0,
      summaryData.pending || 0,
      summaryData.skipped || 0,
      summaryData.aborted || 0,
    ];
    const filteredData = series.map((value, index) => ({ value, label: fullLabels[index], color: fullColors[index] }))
    .filter(item => item.value > 0);
    this.chartOptions = {
      series: filteredData.map(item => item.value),
      chart: {
        height: 270,
        type: 'pie'
      },
      plotOptions: {
        pie: {
          expandOnClick: false,
        },
      },
      labels: filteredData.map(item => item.label),
      legend: {
        position: 'bottom',
      },
      dcolors: filteredData.map(item => item.color),
      dataLabels: {
        enabled: true,
        style: {
          fontSize: "10px",
          fontWeight: "bold"
        },
        formatter: (val: number, opts: any) => {
          const index = opts.seriesIndex;
          const seriesValue = opts.w.config.series[index];
          return `${seriesValue.toString()}`;
        }
      },
    };
  }
  /**
   * Converts a date string into a localized date and time string.
   *
   * @param dateValue - The date string to be converted.
   * @returns The localized date and time string if the input is valid, otherwise an empty string.
   */  
  convertDate(dateValue: string): string {
    return dateValue ? (new Date(dateValue)).toLocaleString() : '';
  }
  /**
   * Processes the execution results data by mapping each item to a new object
   * with additional properties `checked` and `details`. The `checked` property
   * is set to `false` and the `details` property is set to `null`. The processed
   * data is then assigned to `executionResultData` and a copy of it is assigned
   * to `filteredData`.
   *
   * @returns {void}
   */
  resultDetails():void {
  this.executionResultData = this.data.executionResults.map((item:any)=>({
    ...item,
    checked: false,
    details: null
  }))
  this.filteredData = [...this.executionResultData];
  }
  /**
   * Toggles the state of the card flip.
   * If the card is currently flipped, it will be unflipped and vice versa.
   */
  flipCard():void {
    this.isFlipped = !this.isFlipped;
  }

  /**
   * Toggles the expansion state of a panel and fetches execution details if expanded.
   * 
   * @param parent - The parent object containing the panel state and execution result ID.
   * @param id - The ID of the execution result.
   * 
   * This method toggles the `expanded` state of the parent object and updates the `executionResultId` 
   * and `panelOpenState` properties. If the panel is expanded and the `details` property of the parent 
   * object is not set, it fetches the execution result details from the `executionservice` and parses 
   * the response. If the `logs` property in the details is not null, it formats the logs by replacing 
   * newline characters with `<br>` tags. If the panel is collapsed, it sets the `details` property of 
   * the parent object to null.
   */
  togglePanel(parent: any, id:any):void {
    parent.expanded = !parent.expanded;
    this.executionResultId = id;
    this.panelOpenState = !this.panelOpenState;
    if (parent.expanded && !parent.details) {
      this.executionservice.scriptResultDetails(parent.executionResultID).subscribe(res=>{
        parent.details =JSON.parse(res);
        let logs = parent.details.logs
        if(logs !== null){
          this.formatLogs = logs.replace(/\n/g, '<br>');
        }
      })
    } else {
      parent.details = null;
    }
  }
  /**
   * Toggles the checked state of all items in the execution result data.
   * 
   * @param {Event} event - The event triggered by the user interaction.
   * 
   * This method updates the `allChecked` property based on the event's target checked state.
   * It then iterates through `executionResultData` and sets each item's `checked` property
   * to the value of `allChecked`. Finally, it calls `updateSelectedDetails` and `updateFilteredData`
   * to refresh the relevant data.
   */
  toggleAll(event: Event):void {
    this.allChecked = (event.target as HTMLInputElement).checked;
    this.executionResultData.forEach((item:any) => (item.checked = this.allChecked));
    this.updateSelectedDetails();
    this.updateFilteredData();
  }
  /**
   * Toggles the checkbox state for a specific item in the execution result data.
   * 
   * @param index - The index of the item in the execution result data array.
   * @param event - The event object from the checkbox input.
   * 
   * This method updates the `checked` property of the item at the specified index
   * based on the checkbox input's checked state. It also updates the `allChecked`
   * property to true if all items in the execution result data are checked, and
   * calls the `updateSelectedDetails` method to reflect the changes.
   */
  toggleCheckbox(index: number, event: Event):void {
    this.executionResultData[index].checked = (event.target as HTMLInputElement).checked;
    this.allChecked = this.executionResultData.every((item:any) => item.checked);
    this.updateSelectedDetails();
  }
  /**
   * Clears all selections in the execution result data.
   * 
   * This method performs the following actions:
   * - Sets the `allChecked` flag to `false`.
   * - Iterates through `executionResultData` and sets the `checked` property of each item to `false`.
   * - Calls `updateSelectedDetails` to refresh the selected details.
   * - Sets the `filterStatus` to `'all'`.
   * - Calls `resultDetails` to update the result details.
   * - Calls `updateFilteredData` to refresh the filtered data.
   * 
   * @returns {void}
   */
  clearSelections():void {
    this.allChecked = false;
    this.executionResultData.forEach((item:any) => (item.checked = false));
    this.updateSelectedDetails();
    this.filterStatus = 'all';
    this.resultDetails();
    this.updateFilteredData();
  }
  /**
   * Applies a filter to the execution result data based on the current filter status.
   * If the filter status is 'all', all execution result data is included in the filtered data.
   * Otherwise, only the items with a status matching the filter status are included.
   * Additionally, updates the `allChecked` property to indicate whether all filtered items are checked,
   * and calls `updateSelectedDetails` to refresh the selected details.
   */
  applyFilter():void {
    if (this.filterStatus === 'all') {
      this.filteredData = [...this.executionResultData];
    } else {
      this.filteredData = this.executionResultData.filter((item:any) => item.status === this.filterStatus);
    }
    this.allChecked = this.filteredData.every(item => item.checked);
    this.updateSelectedDetails();
  }
  /**
   * Updates the filtered data by applying the current filter criteria.
   * This method calls the `applyFilter` function to refresh the data based on the filter settings.
   * 
   * @returns {void}
   */
  updateFilteredData():void {
    this.applyFilter();
  }
  /**
   * Updates the `selectedDetails` property by filtering the `executionResultData` array.
   * Only items with the `checked` property set to true are included in `selectedDetails`.
   *
   * @returns {void}
   */
  updateSelectedDetails():void {
    this.selectedDetails = this.executionResultData.filter((item:any) => item.checked);
  }
  /**
   * Initiates a live log polling mechanism that fetches live logs every 5 seconds.
   * The polling continues until `liveLogDestroy$` emits a value.
   * 
   * The fetched logs are stored in `liveLogsData` and if `liveLogsData` is not empty,
   * a dialog is opened to display the logs.
   * 
   * @returns {void}
   */
  liveLogs():void {
     interval(5000)
        .pipe(
          startWith(0),
          takeUntil(this.liveLogDestroy$),
          switchMap(() => {
            return this.executionservice.getLiveLogs(this.executionResultId);
          })
        )
        .subscribe({
          next:(res)=>{
            this.liveLogsData = res;

          },
          error:(err)=>{

          }
        })
        if(this.liveLogsData){
          this.liveLogDialog.open( LivelogDialogComponent,{
            width: '50%',
            height: '70vh',
            maxWidth:'100vw',
            panelClass: 'custom-modalbox',
            data: {
              logs: this.liveLogsData,
              executionId: this.executionResultId
            } 
          });
        }
  }
  /**
   * Fetches device logs for the current execution result and opens a dialog to display them.
   * 
   * This method calls the `getDeviceLogs` method of the `executionservice` with the current
   * `executionResultId`. Upon receiving the response, it opens a dialog using `logFilesDialog`
   * to display the log files. The dialog is configured with specific dimensions and a custom
   * panel class.
   * 
   * @returns {void}
   */
  logFiles():void {
    this.executionservice.getDeviceLogs(this.executionResultId).subscribe(
      (res) => {
        console.log("Response", res);
        this.logFilesDialog.open( LogfileDialogComponent,{
          width: '50%',
          height: '70vh',
          maxWidth:'100vw',
          panelClass: 'custom-modalbox',
          data:{
            logFileNames : res,
            executionId : this.executionResultId
          },
        });
      });
   
  }
  /**
   * Closes the dialog and returns a value indicating that the action was not confirmed.
   *
   * @remarks
   * This method is typically called when the user cancels or closes the dialog without confirming the action.
   *
   * @returns {void} This method does not return a value.
   */  
  onClose():void {
    this.dialogRef.close(false);
  }
  /**
   * Repeats the execution of a process using the execution service.
   * 
   * This method calls the `repeatExecution` method of the `executionservice` with the provided execution ID.
   * It subscribes to the observable returned by the service and handles the response and error cases.
   * 
   * On success, it displays a success message using the `_snakebar` service.
   * On error, it displays an error message using the `_snakebar` service.
   * 
   * @returns {void}
   */  
  repeatExecution():void{
    this.executionservice.repeatExecution(this.data.executionId,this.loggedinUser.userName).subscribe({
      next:(res)=>{
        this._snakebar.open(res, '', {
          duration: 3000,
          panelClass: ['success-msg'],
          verticalPosition: 'top'
        })
      },
      error:(err)=>{
        this._snakebar.open(err.error.text, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
        })
      }
    })
  }
  /**
   * Triggers a rerun of a failed execution using the execution service.
   * Displays a success message if the rerun is successful, or an error message if it fails.
   *
   * @returns {void}
   */  
  rerunFailure():void{
    this.executionservice.rerunOnFailure(this.data.executionId,this.loggedinUser.userName).subscribe({
      next:(res)=>{
        this._snakebar.open(res, '', {
          duration: 3000,
          panelClass: ['success-msg'],
          verticalPosition: 'top'
        })
      },
      error:(err)=>{
        this._snakebar.open(err.error.text, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
        })
      }
    })
  }
  /**
   * Fetches the module-wise execution summary data from the execution service
   * and processes it to populate the module table data and titles.
   * 
   * The method subscribes to the execution service's `modulewiseSummary` observable,
   * and on successful response, it parses the response data, extracts keys, and
   * constructs the module table title array. It also handles the 'Total' key separately
   * by pushing it to the end of the module table title array.
   * 
   * In case of an error, it parses the error message and displays it using a snackbar.
   * 
   * @returns {void}
   */  
  modulewiseExeSummary():void{
    this.executionservice.modulewiseSummary(this.data.executionId).subscribe({
      next:(res)=>{
        this.moduleTableData = JSON.parse(res);
        this.keys = Object.keys(this.moduleTableData);
        this.moduleTableTitle = this.keys
        .filter((key) => key !== 'Total')
        .map((key) => ({ name: key, ...this.moduleTableData[key] }));
  
      const totalData = this.moduleTableData['Total'];
      this.moduleTableTitle.push({ name: 'Total', ...totalData });
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
   * Updates the data by fetching result details from the execution service.
   * Parses the response and updates the component's data.
   * Calls methods to update the pie chart data and result details.
   *
   * @returns {void}
   */
  dataUpdate():void{
    this.executionservice.resultDetails(this.data.executionId).subscribe(res=>{ 
      this.data = JSON.parse(res);
      this.pieChartData();
      this.resultDetails();
    })
  }

}
