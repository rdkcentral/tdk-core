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
import { Component, ElementRef,Renderer2, ViewChild } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { ColDef,GridApi,GridReadyEvent,IMultiFilterParams } from 'ag-grid-community';
import '../../../../node_modules/ag-grid-community/styles/ag-grid.css';
import '../../../../node_modules/ag-grid-community/styles/ag-theme-quartz.css';
import { ButtonComponent } from '../../utility/component/ag-grid-buttons/button/button.component';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DeviceService } from '../../services/device.service';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../material/material.module';
import { MatDialog } from '@angular/material/dialog';
import { DialogDelete } from '../../utility/component/dialog-component/dialog.component';

@Component({
  selector: 'app-devices',
  standalone: true,
  imports: [CommonModule,AgGridAngular,FormsModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './devices.component.html',
  styleUrl: './devices.component.css'
})
export class DevicesComponent {

  @ViewChild('staticBackdrop', {static: false}) staticBackdrop?:ElementRef;
  rowData: any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 10;
  public paginationPageSizeSelector: number[] | boolean = [10, 20, 50];
  configureName!: string;
  selectedRowCount = 0;
  selectedDeviceCategory : string = 'RDKV';
  uploadXMLForm!:FormGroup;
  uploadFormSubmitted = false;
  uploadFileName! :File | null ;
  categoryName!: string | null;
  uploadFileError: string | null = null;
  loggedinUser:any;
  preferedCategory!:string;
  userCategory!:string;
  loaderDisplay = false;

  public gridApi!: GridApi;  public columnDefs: ColDef[] = [
    {
      headerName: 'Name',
      field: 'deviceName',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Device IP',
      field: 'deviceIp',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Device Type',
      field: 'deviceTypeName',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      headerClass: 'no-sort',
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
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };
  gridOptions = {
    rowHeight: 36,
  };

  constructor(private router: Router, private service:DeviceService, private fb:FormBuilder,
    private _snakebar :MatSnackBar, public dialog:MatDialog,private renderer: Renderer2){
      this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
      this.userCategory = this.loggedinUser.userCategory;
      this.preferedCategory = localStorage.getItem('preferedCategory')|| '';
  }
  
  /**
   * Closes the modal  by click on button .
   */
  close(){
    (this.staticBackdrop?.nativeElement as HTMLElement).style.display = 'none';
    this.renderer.removeStyle(document.body, 'overflow');
    this.renderer.removeStyle(document.body, 'padding-right');
  }

  /**
   * Initializes the component and performs necessary setup tasks.
   */
  ngOnInit(): void {
    this.selectedDeviceCategory = this.userCategory;
    this.categoryName = 'Video';
    const deviceCategory = this.preferedCategory?this.preferedCategory:this.userCategory;
    // const name = localStorage.getItem('deviceCategoryName');
    // this.categoryName = name;
    // this.categoryChange(deviceCategory);
    if(deviceCategory === null){
      // this.categoryName = name;/
      this.configureName = this.selectedDeviceCategory;
      this.findallbyCategory();
    }
    if(deviceCategory){
      this.selectedDeviceCategory = deviceCategory;
      this.findallbyCategory();
    }
    this.uploadXMLForm = this.fb.group({
      uploadXml: [null, Validators.required]
    })
  }

  /**
   * Finds all devices by category.
   */
  findallbyCategory(){
    this.loaderDisplay = true;
    this.service.findallbyCategory(this.selectedDeviceCategory).subscribe({
      next: (res) => {
        let data = JSON.parse(res);
        this.rowData = data;
        this.rowData = data.sort((a: any, b: any) =>a.deviceName.toString().localeCompare(b.deviceName.toString()));
        this.loaderDisplay = false;
      },
      error: (err) => {
        this.loaderDisplay = false;
      }
    })
  }
  /**
   * Handles the event when a device category is checked.
   * @param event - The event object containing the checked value.
   */
  // ischecked(val:any):void{
  //   this.rowData = [];
  //   this.categoryChange(val);
  // }
  categoryChange(event:any){
    let val = event.target.value;
    if(val === 'RDKB'){
      this.categoryName = 'Broadband';
      this.selectedDeviceCategory = 'RDKB';
      localStorage.setItem('deviceCategory', this.selectedDeviceCategory);
      localStorage.setItem('deviceCategoryName', this.categoryName);
      this.findallbyCategory();
    }
    else{
      this.selectedDeviceCategory = 'RDKV';
      this.categoryName = 'Video';
      localStorage.setItem('deviceCategory', this.selectedDeviceCategory);
      localStorage.setItem('deviceCategoryName', this.categoryName);
      this.findallbyCategory();
    }

  }

  /**
   * Event handler for when the grid is ready.
   * @param params - The GridReadyEvent object containing the grid API.
   */
  onGridReady(params: GridReadyEvent<any>) {
    this.gridApi = params.api;
  }

  /**
   * Event handler for when the filter text box value changes.
   */
  onFilterTextBoxChanged() {
    this.gridApi.setGridOption(
      "quickFilterText",
      (document.getElementById("filter-text-box") as HTMLInputElement).value,
    );
  }

  /**
   * Edits the user and navigates to the device edit page.
   * @param user - The user object to be edited.
   * @returns The edited user object.
   */
  userEdit(user: any): void {
    localStorage.setItem('user', JSON.stringify(user));
    this.router.navigate(['/devices/device-edit'])
  }

  /**
   * Deletes a device.
   * @param data - The data of the device to be deleted.
   */
  delete(data: any) {
    if (confirm("Are you sure to delete ?")) {
      if(data){
        this.service.deleteDevice(data.id).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
              })
              const rowToRemove = this.rowData.find((row:any) => row.id === data.id);
              if (rowToRemove) {
                this.gridApi.applyTransaction({ remove: [rowToRemove] });
              }
          },
          error:(err)=>{
            this._snakebar.open(err.message, '', {
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
   * Navigates to the device creation page.
   */
  createDevice(){
    this.router.navigate(['/devices/device-create']);
  }

  /**
   * Handles the file change event when a file is selected for upload.
   * @param event - The file change event object.
   */
  onFileChange(event:any){
    this.uploadFileName = event.target.files[0].name;
    const file: File = event.target.files[0];
    if(file){
      if (file.type === 'text/xml') {
        this.uploadXMLForm.patchValue({ file: file });
        this.uploadFileName = file;
        this.uploadFileError = null;
      } else {
        this.uploadXMLForm.patchValue({ file: null });
        this.uploadFileError = 'Please upload a valid XML file.';
      }
    }

  }

  /**
   * Handles the submission of the uploadXMLForm.
   */
  uploadXMLSubmit(){
    this.uploadFormSubmitted = true;
    if(this.uploadXMLForm.invalid){
     }else{
      if(this.uploadFileName){
        this.uploadFileError = null;
        this.service.uploadXMLFile(this.uploadFileName).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
              this.close();
              this.ngOnInit();
          },
          error:(err)=>{
            let errmsg = JSON.parse(err.error);
            this._snakebar.open(errmsg.message, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
            })
            this.ngOnInit();
            this.close();
            this.uploadXMLForm.reset();
          }
        })
      }
     }
  }
 /**
   * Download all device details as zip format based on device category selection
   */
  downloadAllDevice(){
    if(this.rowData.length > 0){
      this.service.downloadDeviceByCategory(this.selectedDeviceCategory);
    }else{
      this._snakebar.open('No data available for download', '', {
        duration: 2000,
        panelClass: ['err-msg'],
        horizontalPosition: 'end',
        verticalPosition: 'top'
      })
    }
  }
   /**
   * Download device details as xml format based on device name
   */
  downloadXML(params:any):void{
    if(params.deviceName){
      this.service.downloadDevice(params.deviceName).subscribe(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${params.deviceName}.xml`; 
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });
    }
  }


}
