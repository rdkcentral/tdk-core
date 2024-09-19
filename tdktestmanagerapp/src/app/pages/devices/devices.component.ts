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
import { Component, ElementRef, Input, Renderer2, ViewChild } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { ColDef,GridApi,GridReadyEvent,IMultiFilterParams } from 'ag-grid-community';
import '../../../../node_modules/ag-grid-community/styles/ag-grid.css';
import '../../../../node_modules/ag-grid-community/styles/ag-theme-quartz.css';
import { ButtonComponent } from '../../utility/component/ag-grid-buttons/button/button.component';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DeviceService } from '../../services/device.service';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../material/material.module';
import { MatDialog } from '@angular/material/dialog';
import { DialogDelete } from '../../utility/component/dialog-component/dialog.component';

@Component({
  selector: 'app-devices',
  standalone: true,
  imports: [CommonModule,AgGridAngular, FormsModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './devices.component.html',
  styleUrl: './devices.component.css'
})
export class DevicesComponent {

  @ViewChild('staticBackdrop', {static: false}) staticBackdrop?:ElementRef;
  rowData: any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 7;
  public paginationPageSizeSelector: number[] | boolean = [7, 15, 30, 50];
  configureName!: string;
  selectedRowCount = 0;
  selectedDeviceCategory : string = 'RDKV';
  uploadXMLForm!:FormGroup;
  uploadFormSubmitted = false;
  uploadFileName! :File;
  
  public gridApi!: GridApi;  public columnDefs: ColDef[] = [
    {
      headerName: 'Name',
      field: 'stbName',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true,
    },
    {
      headerName: 'Device IP',
      field: 'stbIp',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Box Type',
      field: 'boxTypeName',
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
        onViewClick:this.openModal.bind(this),
        onDownloadClick:this.downloadXML.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    }
  ];


  constructor(private router: Router, private service:DeviceService,
    private _snakebar :MatSnackBar, public dialog:MatDialog,private renderer: Renderer2){
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
    const deviceCategory = localStorage.getItem('deviceCategory');
    if(deviceCategory === null){
      this.configureName = this.selectedDeviceCategory;
      localStorage.setItem('deviceCategory', this.selectedDeviceCategory);
      this.findallbyCategory();
    }
    if(deviceCategory){
      this.selectedDeviceCategory = deviceCategory;
      this.configureName = this.selectedDeviceCategory;
      this.findallbyCategory();
    }
    this.uploadXMLForm = new FormGroup({
      uploadXml: new FormControl<string | null>('', { validators: Validators.required }),
    })
  }

  /**
   * Finds all devices by category.
   */
  findallbyCategory(){
    this.service.findallbyCategory(this.selectedDeviceCategory).subscribe(res=>{
      // this.rowData =JSON.parse(res);
      let data = JSON.parse(res)
      this.rowData = data.sort((a: any, b: any) =>a.stbName.toString().localeCompare(b.stbName.toString()));
    })
  }
  /**
   * Handles the event when a device category is checked.
   * @param event - The event object containing the checked value.
   */
  ischecked(event:any):void{
    this.selectedDeviceCategory = event.target.value;
    localStorage.setItem('deviceCategory', this.selectedDeviceCategory);
    if(this.selectedDeviceCategory){
      this.configureName = this.selectedDeviceCategory;
      this.service.deviceCategory = this.selectedDeviceCategory;
      this.findallbyCategory();
    }
  }
  gridOptions = {
    domLayout: 'autoHeight'
  };
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
    localStorage.setItem('user', JSON.stringify(user))
    this.service.getStreamsForDeviceForUpdate(user.id).subscribe(res=>{
     this.service.saveStreamingData(res)
    })
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
              this.ngOnInit();
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
    if (file && file.type === 'text/xml') {
      this.uploadFileName = file;
    } else {
      alert('Please select a valid XML file.');
    }
  }

  /**
   * Handles the submission of the uploadXMLForm.
   */
  uploadXMLSubmit(){
    this.uploadFormSubmitted = true;
    if(this.uploadXMLForm.invalid){
      return
     }else{
      if(this.uploadFileName){
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
            let errmsg = err.error;
            this._snakebar.open(errmsg, '', {
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
  openModal(params:any){
    this.service.getStreamsForDeviceForUpdate(params.id).subscribe(res=>{
      this.service.saveStreamingData(res)
     })
    this.dialog.open( DialogDelete,{
      width: '99%',
      height: '93vh',
      maxWidth:'100vw',
      panelClass: 'custom-modalbox',
      data:{
        agentMonitorPort: params.agentMonitorPort,
        boxManufacturerName : params.boxManufacturerName,
        boxTypeName : params.boxTypeName,
        category :  params.category,
        gatewayDeviceName :  params.gatewayDeviceName,
        id :  params.id,
        logTransferPort  :  params.logTransferPort,
        macId :  params.macId,
        recorderId :  params.recorderId,
        socVendorName :  params.socVendorName,
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
  downloadXML(params:any):void{
    if(params.stbName){
      this.service.downloadDevice(params.stbName).subscribe(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${params.stbName}.xml`; 
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });
    }
  }

}
