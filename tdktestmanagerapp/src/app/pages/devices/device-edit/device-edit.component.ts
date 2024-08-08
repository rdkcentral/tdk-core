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
import { HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  IMultiFilterParams,
} from 'ag-grid-community';

import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { BoxManufactureService } from '../../../services/box-manufacture.service';
import { DeviceService } from '../../../services/device.service';
import { SocVendorService } from '../../../services/soc-vendor.service';
import { BoxtypeService } from '../../../services/boxtype.service';
import { InputComponent } from '../../../utility/component/ag-grid-buttons/input/input.component';
import {  Editor, NgxEditorModule, Toolbar } from 'ngx-editor';

@Component({
  selector: 'app-device-edit',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule,AgGridAngular],
  templateUrl: './device-edit.component.html',
  styleUrl: './device-edit.component.css'
})
export class DeviceEditComponent {

  public columnDefs: ColDef[] = [
    {
      headerName: 'Steam Id',
      field: 'streamingDetailsId',
      filter: 'agMultiColumnFilter',
      flex: 2,
      filterParams: {
        filters: [
          {
            filter: 'agTextColumnFilter',
            display: 'subMenu',
          },
          {
            filter: 'agSetColumnFilter',
          },
        ],
      } as IMultiFilterParams,
    },
    {
      headerName: 'Channel Type',
      field: 'channelType',
      filter: 'agMultiColumnFilter',
      flex: 2,
      filterParams: {
        filters: [
          {
            filter: 'agTextColumnFilter',
            display: 'accordion',
            title: 'Expand Me for Text Filters',
          },
          {
            filter: 'agSetColumnFilter',
            display: 'accordion',
          },
        ],
      } as IMultiFilterParams,
    },
    {
      headerName: 'Audio Format',
      field: 'audioType',
      filter: 'agMultiColumnFilter',
      flex: 2,
      filterParams: {
        filters: [
          {
            filter: 'agTextColumnFilter',
            display: 'accordion',
            title: 'Expand Me for Text Filters',
          },
          {
            filter: 'agSetColumnFilter',
            display: 'accordion',
          },
        ],
      } as IMultiFilterParams,
    },
    {
      headerName: 'Video Format',
      field: 'videoType',
      filter: 'agMultiColumnFilter',
      flex: 2,
      filterParams: {
        filters: [
          {
            filter: 'agTextColumnFilter',
            display: 'accordion',
            title: 'Expand Me for Text Filters',
          },
          {
            filter: 'agSetColumnFilter',
            display: 'accordion',
          },
        ],
      } as IMultiFilterParams,
    },
    {
      headerName: 'Ocap Id',
      field: 'ocapId',
      cellRenderer:'inputCellRenderer'
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };

  configureName!: string;
  editDeviceVForm!: FormGroup;
  rdkBForm!:FormGroup;
  rdkCForm!:FormGroup;
  editDeviceVFormSubmitted = false;
  rdkbFormSubmitted = false;
  rdkcFormSubmitted = false;
  isthunderEnabled = false;
  showPortFile = false;
  showConfigPort = false;
  showConfigPortB = false;
  allBoxType:any;
  allboxManufacture:any;
  allsocVendors:any;
  allGatewayDevices:any;
  showTable= false;
  errormessage:any;
  rowData:any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 5;
  public paginationPageSizeSelector: number[] | boolean = [5,10, 50, 100];
  public tooltipShowDelay = 500;
  gridApi!: any;
  showHideCreateFormV = true;
  showHideCreateFormB = false;
  showHideCreateFormC = false;
  isGateway!: any;
  isrecorderId = false;
  isThunderchecked = false;
public frameworkComponents :any;
  visibleGateway = true;
  streamingMapObj!: { streamId: any; ocapId: any; }[];
  loggedinUser: any;
  agentport = "8087";
  agentStatusPort = "8088";
  agentMonitoPort = "8090";
  user: any;
  selectedDeviceCategory : string = 'RDKV';
  visibleDeviceconfigFile = false;
  configFileName!:string;
  editor!: Editor;
  editor2!: Editor;
  uploadConfigForm!: FormGroup;
  uploadDeviceConfigForm!:FormGroup;
  filesList:any[]=[];
  stbNameChange!: string;
  configData:any;
  boxTypeValue!: string;
  configDevicePorts = false;

  constructor(private fb:FormBuilder, private router: Router,
    private _snakebar :MatSnackBar, private boxManufactureService:BoxManufactureService, 
    private service:DeviceService, private socVendorService:SocVendorService, private boxtypeService:BoxtypeService) { 
    this.user = JSON.parse(localStorage.getItem('user') || '{}');
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
    
    this.frameworkComponents = {
      inputCellRenderer: InputComponent
    }
  }

  /**
   * Initializes the component and performs necessary setup tasks.
   * Retrieves device category from local storage and sets the initial values for the form fields.
   * Configures the visibility of create forms based on the selected device category.
   * Validates IP address using regular expression.
   * Initializes form groups and sets default values for form controls.
   * Retrieves data from API endpoints.
   */
  ngOnInit(): void {
    const deviceCategory = localStorage.getItem('deviceCategory');
    this.stbNameChange = this.user.stbName;
    this.boxTypeValue = this.user.boxTypeName;
    if(deviceCategory){
      this.selectedDeviceCategory = deviceCategory;
      this.configureName = deviceCategory;
    }
    if(this.configureName ==='RDKV'){
      this.showHideCreateFormV = true;
      this.showHideCreateFormB = false;
      this.showHideCreateFormC = false;
    }
    if(this.configureName ==='RDKB'){
      this.showHideCreateFormV = false;
      this.showHideCreateFormB = true;
      this.showHideCreateFormC = false;
    }
    if(this.configureName ==='RDKC'){
      this.showHideCreateFormV = false;
      this.showHideCreateFormB = false;
      this.showHideCreateFormC = true;
    }
    let ipregexp: RegExp = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    this.editDeviceVForm = this.fb.group({
      stbname: [this.user.stbName, [Validators.required]],
      stbip: [this.user.stbIp, [Validators.required, Validators.pattern(ipregexp)]],
      macaddr: [this.user.macId, [Validators.required]],
      boxtype: [this.user.boxTypeName, [Validators.required]],
      boxmanufacturer: [this.user.boxManufacturerName, [Validators.required]],
      socvendor: [this.user.socVendorName, [Validators.required]],
      gateway: [this.user.gatewayDeviceName],
      thunderport:[this.user.thunderPort],
      isThunder: [this.user.thunderEnabled],
      configuredevicePorts:[this.user.devicePortsConfigured],
      agentport: [this.user.stbPort?this.user.stbPort:this.agentport],
      agentstatusport: [this.user.statusPort?this.user.statusPort:this.agentStatusPort],
      agentmonitorport: [this.user.agentMonitorPort?this.user.agentMonitorPort:this.agentMonitoPort],
      recorderId: [this.user.recorderId]
    })

    this.rdkBForm = this.fb.group({
      gatewayName:[this.user.stbName, [Validators.required]],
      gatewayIp: [this.user.stbIp, [Validators.required]],
      macaddr: [this.user.macId, [Validators.required]],
      boxtype: [this.user.boxTypeName, [Validators.required]],
      boxmanufacturer: [this.user.boxManufacturerName, [Validators.required]],
      socvendor: [this.user.socVendorName, [Validators.required]],
      agentPortb: [this.user.stbPort?this.user.stbPort:this.agentport],
      agentStatusportB: [this.user.statusPort?this.user.statusPort:this.agentStatusPort],
      agentMonitorportB: [this.user.agentMonitorPort?this.user.agentMonitorPort:this.agentMonitoPort]
    })

    this.rdkCForm = this.fb.group({
      cameraName: [this.user.stbName, [Validators.required]],
      stbIp:[this.user.stbIp, [Validators.required]],
      macaddr: [this.user.macId, [Validators.required]],
      boxtype: [this.user.boxTypeName, [Validators.required]],
      boxmanufacturer: [this.user.boxManufacturerName, [Validators.required]],
      socvendor: [this.user.socVendorName, [Validators.required]],
      agentPortb: [this.user.stbPort?this.user.stbPort:this.agentport],
      agentStatusportB:[this.user.statusPort?this.user.statusPort:this.agentStatusPort],
      agentMonitorportB:[this.user.agentMonitorPort?this.user.agentMonitorPort:this.agentMonitoPort]
    })
    this.getAllboxType();
    this.getAllboxmanufacture();
    this.getAllsocVendors();
    this.isBoxtypeGateway(this.user.boxTypeName);
    this.getTableUpdateData();
    this.isEditChecked(this.user.thunderEnabled);
    this.isCheckedConfigPort(this.user.devicePortsConfigured)
    this.visibilityConfigFile();
    this.editor = new Editor();
    this.editor2 = new Editor();
    this.uploadConfigForm = this.fb.group({
      editorFilename:['',{disabled: true}],
      editorContent: [''],
    });
    this.filesList =[];
    this.uploadDeviceConfigForm = this.fb.group({
      editorFilename:['',{disabled: true}],
      editorContent: [''],
      uploadConfigFile:['']
    });
    this.service.getlistofGatewayDevices(this.selectedDeviceCategory).subscribe(res=>{
      this.allGatewayDevices = JSON.parse(res);
    })
  }

  /**
   * Retrieves the table update data by making a request to the service.
   */
  getTableUpdateData(){
  this.service.getStreamsForDeviceForUpdate(this.user.id).subscribe(res=>{
    this.rowData = JSON.parse(res);
    })
  }

  /**
   * Called when the grid is ready.
   * @param params - The grid ready event parameters.
   */
  onGridReady(params: any) {
    this.gridApi = params.api;
  }

  /**
   * Retrieves all box types based on the selected device category.
   */
  getAllboxType(){
    this.boxtypeService.getfindallbycategory(this.selectedDeviceCategory).subscribe(res=>{
      this.allBoxType = (JSON.parse(res));
    })
  }

  /**
   * Retrieves all box manufactures based on the selected device category.
   */
  getAllboxmanufacture(){
    this.boxManufactureService.getboxManufactureByList(this.selectedDeviceCategory).subscribe(res=>{
      this.allboxManufacture = JSON.parse(res);
      
    })
  }

  /**
   * Retrieves all SOC vendors based on the selected device category.
   */
  getAllsocVendors(){
    this.socVendorService.getSocVendor(this.selectedDeviceCategory).subscribe(res=>{
      this.allsocVendors = JSON.parse(res);
      
    })
  }

  /**
   * Handles the change event when the checkbox is checked or unchecked.
   * @param event - The event object containing information about the checkbox change.
   */
  isChecked(event:any){
    if(event.target.checked){
      this.isThunderchecked = true;
      this.showPortFile = true;
      this.showTable = false;
    }else{
      this.showPortFile = false;
      this.isThunderchecked = false;
      this.showTable = true;
    }
  }
  /**
   * Updates the state of the component based on the value of `val`.
   * If `val` is true, it shows the port file and sets the Thunder checkbox to true.
   * If `val` is false, it hides the port file and sets the Thunder checkbox to false.
   * @param val - The value to check.
   */
  isEditChecked(val:boolean){
    if(val === true){
      this.showPortFile = true;
      this.showTable = false;
      this.isThunderchecked = true;
    }else{
      this.showPortFile = false;
      this.isThunderchecked = false;
      this.showTable = true;
    }
  }
  isCheckedConfig(event:any){
    if(event.target.checked){
      this.showConfigPort = true;
    }else{
      this.showConfigPort = false;
    }
  }
  isCheckedConfigPort(val:boolean):void{
    if(val === true){
      this.showConfigPort = true;
    }else{
      this.showConfigPort = false;
    }
  }
  isCheckedConfigB(event:any){
    if(event.target.checked){
      this.showConfigPortB = true;
    }else{
      this.showConfigPortB = false;
    }
  }
  /**
   * Handles the change event of the box type dropdown.
   * @param event - The event object containing the target element.
   */
  boxtypeChange(event:any){
    this.visibleDeviceconfigFile = false;
    let value = event.target.value;
    this.boxTypeValue = value;
    const dropdown = event.target as HTMLSelectElement
    this.checkIsThunderValidity();
    this.service.isBoxtypeGateway(value).subscribe(res=>{
      this.isGateway = res;
      if(this.isGateway === 'true'){
        this.isrecorderId = true;
        this.showTable = true;
      }else{
        this.isrecorderId = false;
        this.showTable = false;
      }
    })
    if(this.boxTypeValue !== ''){
    const selectedType = this.allBoxType.find((item:any) => item.boxTypeName === dropdown.value);
      if( selectedType.type === 'CLIENT' || selectedType.type ==='STAND_ALONE_CLIENT'){
        this.visibleGateway = true;
        this.service.getlistofGatewayDevices(this.selectedDeviceCategory).subscribe(res=>{
          this.allGatewayDevices = JSON.parse(res);
        })
      }else{
        this.visibleGateway = false;
      }
    }

    if(this.isThunderchecked){
      this.showPortFile = true;
      this.visibilityConfigFile();
    }
  }
  /**
   * This methos is change the value of stbname inputfield
  */
  valuechange(event:any):void{
    this.checkIsThunderValidity();
    this.stbNameChange = event.target.value;
    if(this.isThunderchecked){
      this.showPortFile = true;
      if(this.stbNameChange === undefined || this.stbNameChange){
        this.visibilityConfigFile();
      }
      if(this.stbNameChange !== undefined && this.stbNameChange !== ""){
        this.visibleDeviceconfigFile = true;
      }
    }
  }
  /**
   * The method to check thunder enable or disable.
   */
    checkIsThunderValidity(): void{
      const stbName = this.stbNameChange;
      const boxType = this.boxTypeValue;
      if(stbName && boxType){
        this.editDeviceVForm.get('isThunder')?.enable();
      }else{
        this.editDeviceVForm.get('isThunder')?.disable();
        this.editDeviceVForm.get('isThunder')?.setValue(false);
        this.showPortFile = false;
        this.isThunderchecked = false;
      }
    }
  /**
   * Show the Config file or device.config file beased on stbname and boxtype
  */  
    visibilityConfigFile(): void{
      let boxNameConfig = this.stbNameChange?this.stbNameChange:this.user.stbName;
      let boxTypeConfig = this.boxTypeValue?this.boxTypeValue:this.user.boxTypeName; 
      this.service.downloadDeviceConfigFile(boxNameConfig,boxTypeConfig)
      .subscribe((res)=>{ 
        this.configFileName = res.filename;
        if(this.configFileName !== `${boxNameConfig}.config` && this.stbNameChange !== undefined && this.stbNameChange !== ""){
          this.visibleDeviceconfigFile = true;
        }else{
          this.visibleDeviceconfigFile = false;
        }
        if(this.configFileName === `${boxTypeConfig}.config`){
          this.visibleDeviceconfigFile = true;
        }
        if(this.configFileName !== `${boxNameConfig}.config` && this.configFileName !== `${boxTypeConfig}.config`){
          this.visibleDeviceconfigFile = false;
        }
        this.readFileContent(res.content);
        this.uploadConfigForm.patchValue({
          editorFilename: this.configFileName,
          editorContent: this.configData
        })
        this.readDeviceFileContent(res.content); 
        this.uploadDeviceConfigForm.patchValue({
          editorFilename: this.stbNameChange+'.config',
          editorContent: this.configData
        })
      })
    }
  /**
   * Reading the configfile
  */ 
  readFileContent(file:Blob): void{
    const reader = new FileReader();
    reader.onload = ()=>{
      let htmlContent = reader.result
      this.configData = this.formatContent(htmlContent);
      if(this.configData){
          this.uploadConfigForm.patchValue({
            editorFilename: this.configFileName,
            editorContent: this.configData
          })
      }
    }
    reader.readAsText(file)
  }

  /**
   * Reading the device configfile
  */ 
  readDeviceFileContent(file:Blob): void{
    const reader = new FileReader();
    reader.onload = ()=>{
      let htmlContent = reader.result
      this.configData = this.formatContent(htmlContent);
      if(this.configData){
          this.uploadDeviceConfigForm.patchValue({
            editorFilename: this.stbNameChange+'.config',
            editorContent: this.configData
          })
      }
    }
    reader.readAsText(file)
  }
   /**
   * Lifecycle hook that is called when the component is destroyed.
   * It is used to perform any necessary cleanup logic before the component is removed from the DOM.
   */
   ngOnDestroy():void{
    this.editor.destroy();
    this.editor2.destroy();
  }
  /**
   * Formats the content by replacing all occurrences of '#' with '<br># '.
   * 
   * @param content - The content to be formatted.
   * @returns The formatted content.
   */
  formatContent(content:any){
    return content.replace(/#/g, '<br># ');
  } 

  isBoxtypeGateway(value:any){
    this.service.isBoxtypeGateway(value).subscribe(res=>{
      this.isGateway = res;
      if(this.isGateway === 'true'){
        this.isrecorderId = true;
        this.showTable = true;
      }else{
        this.isrecorderId = false;
        this.showTable = false;
      }
    })
  }

  /**
   * Navigates back to the devices page and removes the 'streamData' item from localStorage.
   */
  goBack(){
    localStorage.removeItem('streamData');
    this.router.navigate(["/devices"]);
  }

  /**
   * Resets the form to its initial state.
   */
  reset(){
    this.editDeviceVForm.reset();
  }

  /**
   * Downloads a device file.
   */
  downloadFile(){
    if(this.user.stbName){
      this.service.downloadDevice(this.user.stbName).subscribe(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.user.stbName}.xml`; 
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });
    }
  }

  
  EditDeviceVSubmit(){
    this.editDeviceVFormSubmitted = true;
    if(this.editDeviceVForm.invalid){
     return
    }else{
     if(this.showTable==true){
      const tableData :any[]=[];
      this.gridApi.forEachNode((element: any) => {
       tableData.push(element.data)
       this.streamingMapObj = tableData.map((streamingDetailsId: any, ocapId: any) => ({streamId: streamingDetailsId.streamingDetailsId ,ocapId: streamingDetailsId.ocapId}));
      });
     }
  
     let obj ={
      id : this.user.id,
      stbIp : this.editDeviceVForm.value.stbip,
      stbName : this.editDeviceVForm.value.stbname,
      stbPort: this.editDeviceVForm.value.agentport,
      statusPort: this.editDeviceVForm.value.agentstatusport,
      agentMonitorPort: this.editDeviceVForm.value.agentmonitorport,
      macId: this.editDeviceVForm.value.macaddr,
      boxTypeName: this.editDeviceVForm.value.boxtype,
      boxManufacturerName: this.editDeviceVForm.value.boxmanufacturer,
      socVendorName: this.editDeviceVForm.value.socvendor,
      devicestatus : "FREE",
      recorderId : this.editDeviceVForm.value.recorderId,
      gatewayDeviceName : this.editDeviceVForm.value.gateway,
      thunderPort : this.editDeviceVForm.value.thunderport,
      userGroupName : this.loggedinUser.userGroupName,
      category : this.selectedDeviceCategory,
      deviceStreams : this.streamingMapObj?this.streamingMapObj:null,
      thunderEnabled :this.isThunderchecked,
      configuredevicePorts:this.editDeviceVForm.value.configuredevicePorts
      }
    this.service.updateDevice(obj).subscribe({
      next:(res)=>{
        this._snakebar.open(res, '', {
        duration: 3000,
        panelClass: ['success-msg'],
        verticalPosition: 'top'
        })
        setTimeout(() => {
          this.router.navigate(["/devices"]);
          localStorage.removeItem('streamData');
        }, 1000);
       
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
  editDeviceBSubmit(){
    this.editDeviceVFormSubmitted = true;
    if(this.editDeviceVForm.invalid){
     return
    }else{
     if(this.showTable==true){
      const tableData :any[]=[];
      this.gridApi.forEachNode((element: any) => {
       tableData.push(element.data)
       this.streamingMapObj = tableData.map((streamingDetailsId: any, ocapId: any) => ({streamId: streamingDetailsId.streamingDetailsId ,ocapId: streamingDetailsId.ocapId}));
      });
     }
  
     let rdkBobj ={
      id : this.user.id,
      stbIp : this.rdkBForm.value.gatewayIp,
      stbName : this.rdkBForm.value.gatewayName,
      stbPort: this.rdkBForm.value.agentPortb,
      statusPort: this.rdkBForm.value.agentStatusportB,
      agentMonitorPort: this.rdkBForm.value.agentMonitorportB,
      macId: this.rdkBForm.value.macaddr,
      boxTypeName: this.rdkBForm.value.boxtype,
      boxManufacturerName: this.rdkBForm.value.boxmanufacturer,
      socVendorName: this.rdkBForm.value.socvendor,
      userGroupName : this.loggedinUser.userGroupName,
      category : this.selectedDeviceCategory,

      }
    this.service.updateDevice(rdkBobj).subscribe({
      next:(res)=>{
        this._snakebar.open(res, '', {
        duration: 3000,
        panelClass: ['success-msg'],
        verticalPosition: 'top'
        })
        setTimeout(() => {
          this.router.navigate(["/devices"]);
        }, 1000);
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
  editDeviceCSubmit(){
    this.rdkcFormSubmitted = true;
    if(this.rdkCForm.invalid){
      return
     }else{
      let rdkcObj = {
        id : this.user.id,
        stbName:this.rdkCForm.value.cameraName,
        stbIp: this.rdkCForm.value.stbIp,
        macId: this.rdkCForm.value.macaddr,
        boxTypeName: this.rdkCForm.value.boxtype,
        boxManufacturerName: this.rdkCForm.value.boxmanufacturer,
        socVendorName: this.rdkCForm.value.socvendor,
        stbPort: this.rdkCForm.value.agentPortb,
        statusPort:this.rdkCForm.value.agentStatusportB,
        agentMonitorPort:this.rdkCForm.value.agentMonitorportB,
        category : this.selectedDeviceCategory
      }
      this.service.updateDevice(rdkcObj).subscribe({
        next:(res)=>{
          this._snakebar.open(res, '', {
          duration: 3000,
          panelClass: ['success-msg'],
          verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["/devices"]);
            
          }, 1000);
         
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
