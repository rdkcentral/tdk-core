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
import { CommonModule, JsonPipe } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component, ElementRef, Renderer2, TemplateRef, ViewChild } from '@angular/core';
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
import { DeviceService } from '../../../services/device.service';
import { InputComponent } from '../../../utility/component/ag-grid-buttons/input/input.component';
import {  Editor, NgxEditorModule } from 'ngx-editor';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { OemService } from '../../../services/oem.service';
import { DevicetypeService } from '../../../services/devicetype.service';
import { SocService } from '../../../services/soc.service';

@Component({
  selector: 'app-device-edit',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,NgxEditorModule,MaterialModule,AgGridAngular],
  templateUrl: './device-edit.component.html',
  styleUrl: './device-edit.component.css'
})
export class DeviceEditComponent {
  @ViewChild('dialogTemplate', { static: true }) dialogTemplate!: TemplateRef<any>;
  @ViewChild('newDeviceTemplate', { static: true }) newDeviceTemplate!: TemplateRef<any>;
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
  allDeviceType:any;
  allOem:any;
  allsoc:any;
  allGatewayDevices:any;
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
  categoryName!: string;
  visibleDeviceconfigFile = false;
  configFileName!:string;
  editor!: Editor;
  editor2!: Editor;
  uploadConfigForm!: FormGroup;
  uploadDeviceConfigForm!:FormGroup;
  filesList:any[]=[];
  stbNameChange!: string;
  configData:any;
  deviceTypeValue!: string;
  configDevicePorts = false;
  existConfigSubmitted = false;
  uploadExistConfigHeading!: string;
  uploadExistFileContent!: string;
  isMaximized = false;
  isEditingFile = false;
  fileNameArray:string[]=[];
  currentIndex: number = 0;
  existingConfigEditor = true;
  uploadExistingConfig = false;
  showExistUploadButton = true;
  backToExistEditorbtn = false;
  uploadFileName! :File;
  submitted = false;
  uploadCreateHeading: string ='Create New Device Config File';
  uploadFileNameConfig!: string;
  uploadFileContent! : string ;
  deviceEditor = true;
  uploadConfigSec = false;
  backToEditorbtn = false;
  showUploadButton = true;
  dialogRef!: MatDialogRef<any>;
  newDeviceDialogRef!: MatDialogRef<any>;
  localBoxType:any;
  selectedDeviceType:any;
  devicetypeInitial: any;
  thunderCheckInitial = false;
  newFileName!: string;
  findboxType: any[] = [];

  constructor(private fb:FormBuilder, private router: Router,
    private _snakebar :MatSnackBar, private oemService:OemService, 
    private service:DeviceService, private socService:SocService, private devicetypeService:DevicetypeService,
    private renderer:Renderer2, public dialog:MatDialog) { 
    this.user = JSON.parse(localStorage.getItem('user') || '{}');
    
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
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
    this.stbNameChange = this.user.deviceName;
    this.deviceTypeValue = this.user.boxTypeName;
    if(deviceCategory){
      this.selectedDeviceCategory = deviceCategory;
      this.configureName = deviceCategory;
    }
    if(this.configureName ==='RDKV'){
      this.showHideCreateFormV = true;
      this.showHideCreateFormB = false;
      this.showHideCreateFormC = false;
      this.categoryName = 'Video';
    }
    if(this.configureName ==='RDKB'){
      this.showHideCreateFormV = false;
      this.showHideCreateFormB = true;
      this.showHideCreateFormC = false;
      this.categoryName = 'Broadband';
    }
    if(this.configureName ==='RDKC'){
      this.showHideCreateFormV = false;
      this.showHideCreateFormB = false;
      this.showHideCreateFormC = true;
      this.categoryName = 'Camera';
    }
    let ipregexp: RegExp = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    this.editDeviceVForm = this.fb.group({
      stbname: [this.user.deviceName, [Validators.required]],
      stbip: [this.user.deviceIp, [Validators.required, Validators.pattern(ipregexp)]],
      macaddr: [this.user.macId, [Validators.required]],
      devicetype: [this.user.deviceTypeName, [Validators.required]],
      oem: [this.user.oemName, [Validators.required]],
      soc: [this.user.socName, [Validators.required]],
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
      gatewayName:[this.user.deviceName, [Validators.required]],
      gatewayIp: [this.user.deviceIp, [Validators.required]],
      macaddr: [this.user.macId, [Validators.required]],
      devicetype: [this.user.deviceTypeName, [Validators.required]],
      oem: [this.user.oemName, [Validators.required]],
      soc: [this.user.socName, [Validators.required]],
      agentPortb: [this.user.stbPort?this.user.stbPort:this.agentport],
      agentStatusportB: [this.user.statusPort?this.user.statusPort:this.agentStatusPort],
      agentMonitorportB: [this.user.agentMonitorPort?this.user.agentMonitorPort:this.agentMonitoPort]
    })

    this.rdkCForm = this.fb.group({
      cameraName: [this.user.deviceName, [Validators.required]],
      stbIp:[this.user.deviceIp, [Validators.required]],
      macaddr: [this.user.macId, [Validators.required]],
      devicetype: [this.user.deviceTypeName, [Validators.required]],
      oem: [this.user.oemName, [Validators.required]],
      soc: [this.user.socName, [Validators.required]],
      agentPortb: [this.user.stbPort?this.user.stbPort:this.agentport],
      agentStatusportB:[this.user.statusPort?this.user.statusPort:this.agentStatusPort],
      agentMonitorportB:[this.user.agentMonitorPort?this.user.agentMonitorPort:this.agentMonitoPort]
    })
    this.getAlldeviceType();
    this.getAllOem();
    this.getAllsoc();
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
  getAlldeviceType(){
    this.devicetypeService.getfindallbycategory(this.selectedDeviceCategory).subscribe(res=>{
      this.allDeviceType = (JSON.parse(res));
      this.findboxType = this.allDeviceType;
      for (let i = 0; i < this.findboxType.length; i++) {
        const element = this.findboxType[i];
        if(this.deviceTypeValue === element.boxTypeName){
          this.selectedDeviceType = element;
          const selectedType = this.findboxType.find((item:any) => item.type === this.selectedDeviceType.type);
        }
      }

    })
  }

  /**
   * Retrieves all box manufactures based on the selected device category.
   */
  getAllOem(){
    this.oemService.getOemByList(this.selectedDeviceCategory).subscribe(res=>{
      this.allOem = JSON.parse(res);
      
    })
  }

  /**
   * Retrieves all SOC vendors based on the selected device category.
   */
  getAllsoc(){
    this.socService.getSoc(this.selectedDeviceCategory).subscribe(res=>{
      this.allsoc = JSON.parse(res);
      
    })
  }
  /**
   * Handles the change event of the box type dropdown.
   * @param event - The event object containing the target element.
   */
  devicetypeChange(event:any){
    this.visibleDeviceconfigFile = false;
    let value = event.target.value;
    this.deviceTypeValue = value;
    const dropdown = event.target as HTMLSelectElement
    this.checkIsThunderValidity();
    this.service.isBoxtypeGateway(value).subscribe(res=>{
      this.isGateway = res;
      if(this.isGateway === 'true'){
        this.isrecorderId = true;
      }else{
        this.isrecorderId = false;
      }
    })
    if(this.isThunderchecked){
      this.showPortFile = true;
      this.visibilityConfigFile();
    }
  }
  /**
   * Handles the change event when the checkbox is checked or unchecked.
   * @param event - The event object containing information about the checkbox change.
   */
  isChecked(event:any){
    this.isThunderchecked = this.editDeviceVForm.get('isThunder')?.value;
    if(event.target.checked){
      this.isThunderchecked = true;
      this.showPortFile = true;
      this.visibilityConfigFile();
    }else{
      this.showPortFile = false;
      this.isThunderchecked = false;
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
      this.isThunderchecked = true;
    }else{
      this.showPortFile = false;
      this.isThunderchecked = false;
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
   * This methos is change the value of deviceName inputfield
  */
  valuechange(event:any):void{
    // this.checkIsThunderValidity();
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
      const boxType = this.deviceTypeValue;
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
   * Show the Config file or device.config file beased on deviceName and devicetype
  */  
    visibilityConfigFile(): void{
      let boxNameConfig = this.stbNameChange;
      let boxTypeConfig = this.deviceTypeValue;
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
          this.newFileName =`${boxTypeConfig}.config`;
        }
        if(this.configFileName !== `${boxNameConfig}.config` && this.configFileName !== `${boxTypeConfig}.config`){
          this.visibleDeviceconfigFile = false;
          this.newFileName =`${boxNameConfig}.config`;
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
    let boxNameConfig = this.editDeviceVForm.value.stbname;
    const reader = new FileReader();
    reader.onload = ()=>{
      let htmlContent = reader.result
      this.configData = this.formatContent(htmlContent);
      if(this.configData){
          this.uploadConfigForm.patchValue({
            editorFilename: this.configFileName ===`${boxNameConfig}.config`?this.configFileName:this.newFileName,
            editorContent: this.configData,
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
    return `<p>${content.replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/####/g, '#####')
      .replace(/=======/g, '=======')
      .replace(/\n/g, '<br>')
    }
    </p>`;
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
    if(this.user.deviceName){
      this.service.downloadDevice(this.user.deviceName).subscribe(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.user.deviceName}.xml`; 
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
     let obj ={
      id : this.user.id,
      deviceIp : this.editDeviceVForm.value.stbip,
      deviceName : this.editDeviceVForm.value.stbname,
      stbPort: this.editDeviceVForm.value.agentport,
      statusPort: this.editDeviceVForm.value.agentstatusport,
      agentMonitorPort: this.editDeviceVForm.value.agentmonitorport,
      macId: this.editDeviceVForm.value.macaddr,
      deviceTypeName: this.editDeviceVForm.value.devicetype,
      oemName: this.editDeviceVForm.value.oem,
      socName: this.editDeviceVForm.value.soc,
      devicestatus : "FREE",
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
     let rdkBobj ={
      id : this.user.id,
      deviceIp : this.rdkBForm.value.gatewayIp,
      deviceName : this.rdkBForm.value.gatewayName,
      stbPort: this.rdkBForm.value.agentPortb,
      statusPort: this.rdkBForm.value.agentStatusportB,
      agentMonitorPort: this.rdkBForm.value.agentMonitorportB,
      macId: this.rdkBForm.value.macaddr,
      deviceTypeName: this.rdkBForm.value.devicetype,
      oemName: this.rdkBForm.value.oem,
      socName: this.rdkBForm.value.soc,
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
        deviceName:this.rdkCForm.value.cameraName,
        deviceIp: this.rdkCForm.value.stbIp,
        macId: this.rdkCForm.value.macaddr,
        deviceTypeName: this.rdkCForm.value.devicetype,
        oemName: this.rdkCForm.value.oem,
        socName: this.rdkCForm.value.soc,
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


    /**
   * Edit icon will show/hide in editor modal
   */
    toggleIsEdit():void{
      this.isEditingFile = !this.isEditingFile;
      if(this.isEditingFile){
        this.uploadConfigForm.get('editorFilename')?.enable();
      }else{
        this.uploadConfigForm.get('editorFilename')?.disable();
      }
      if(this.configFileName ==='sampleDevice.config'){
        let deviceNameConfig = this.editDeviceVForm.value.stbname;
        let deviceTypeConfig = this.editDeviceVForm.value.devicetype;
        this.fileNameArray.push(deviceNameConfig,deviceTypeConfig);
        this.currentIndex = (this.currentIndex + 1) % this.fileNameArray.length;
        this.uploadConfigForm.patchValue({
          editorFilename: `${this.fileNameArray[this.currentIndex]}.config`,
        })
      }
    }
    /**
     * The method is editor modal will get maximize and minimize
     */
    toggleMaximize():void{
      this.isMaximized = !this.isMaximized;
      const modalElement = document.querySelector('.modal');
      if(this.isMaximized){
        this.renderer.addClass(modalElement, 'modal-maximized');
      }else{
        this.renderer.removeClass(modalElement, 'modal-maximized')
      }
    }
    toggleMaximizeDevice():void{
      this.isMaximized = !this.isMaximized;
      const modalElement = document.querySelector('.modal');
      if(this.isMaximized){
        this.renderer.addClass(modalElement, 'modal-maximized-device');
      }else{
        this.renderer.removeClass(modalElement, 'modal-maximized-device')
    }
  }
  replaceTags(content:string):string{
      const replacepara = content.replace(/<\/?p>/g,'\n');
      const replacebreakes = replacepara.replace(/<br\s*\/?>/g,'\n');
      return replacebreakes.trim();
  }
  configFileUpload(): void{
    this.existConfigSubmitted = true;
    if (this.uploadConfigForm.invalid) {
      return;
    }else if(this.uploadExistConfigHeading ==='Upload Configuration File'){
      const editorFilename = this.uploadConfigForm.get('editorFilename')!.value;
      const content = this.uploadExistFileContent;
      const editorContent  = this.replaceTags(content);
      const contentBlob = new Blob([editorContent], {type:'text/plain'});
      const contentFile = new File([contentBlob],editorFilename);
      this.service.uploadConfigFile(contentFile).subscribe({
        next:(res)=>{
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.uploadConfigForm.get('uploadExistConfigFile')?.reset();
            this.dialogRef.close();
            this.visibilityConfigFile();
            this.uploadExistConfigHeading ='';

          }, 1000);
        },
        error:(err)=>{
          let errmsg = JSON.parse(err.error);
          this._snakebar.open(errmsg.message?errmsg.message:errmsg, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
      })
    }else{
      const formData = new FormData();
      const editorFilename = this.uploadConfigForm.get('editorFilename')!.value;
      const content = this.uploadConfigForm.get('editorContent')!.value;
      const editorContent  = this.replaceTags(content);
      const contentBlob = new Blob([editorContent], {type:'text/plain'});
      const contentFile = new File([contentBlob],editorFilename);
      this.service.uploadConfigFile(contentFile).subscribe({
        next:(res)=>{
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.dialogRef.close();
            this.visibilityConfigFile();
          }, 1000);
        },
        error:(err)=>{
          let errmsg = JSON.parse(err.error);
          this._snakebar.open(errmsg.message?errmsg.message:errmsg, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
      })
    }
  }
    /**
   * Opens the upload file section and sets the necessary flags and values.
   * @param value - The value to set the uploadCreateHeading property to.
   */
    openUploadFile(value:string):void{
      this.deviceEditor = false;
      this.uploadConfigSec = true;
      this.backToEditorbtn = true;
      this.showUploadButton = false;
      this.uploadCreateHeading = value;
  
    }
    /**
   * Navigates back to the device editor and updates the component's state.
   * 
   * @param value - The value to set for the `uploadCreateHeading` property.
   */
    backToEditor(value:string):void{
      this.deviceEditor = true;
      this.uploadConfigSec = false;
      this.backToEditorbtn = false;
      this.showUploadButton = true;
      this.uploadCreateHeading = value;
    }
  /**
   * Opens the existing modal with the specified value.
   * @param val - The value to be passed to the modal.
   */
  openExistingModal(val:string) :void{
    this.existingConfigEditor = false;
    this.uploadExistingConfig = true;
    this.showExistUploadButton = false;
    this.backToExistEditorbtn = true;
    this.uploadExistConfigHeading = val;
 
  }
  /**
   * Navigates back to the existing config editor.
   */
  backToExistingEditor():void{
    this.existingConfigEditor = true;
    this.uploadExistingConfig = false;
    this.showExistUploadButton = true;
    this.backToExistEditorbtn = false;
    this.uploadExistConfigHeading = '';
  }
  onExistConfigChange(event:Event):void{
    let fileInput = event.target as HTMLInputElement;
    if(fileInput && fileInput.files){
      const file = fileInput.files[0];
      this.uploadFileName = file;
      this.uploadExistConfigContent(file)
    }
  }
  uploadExistConfigContent(file:File): void{
    const reader = new FileReader();
    reader.onload = (e:ProgressEvent<FileReader>)=>{
      const content = e.target?.result as string;
      this.uploadExistFileContent = content
      this.uploadConfigForm.patchValue({
        editorFilename: this.configFileName,
        editorContent: this.uploadExistFileContent,
      })
    }
    reader.readAsText(file)
  }
  /**
   * Deletes a device configuration file.
   * @param configFileName - The name of the configuration file to delete.
   */
  deleteDeviceConfigFile(configFileName: any) {
    if (configFileName) {
      if (confirm("Are you sure to delete ?")) {
        this.service.deleteDeviceConfigFile(configFileName).subscribe({
          next: (res) => {
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
            this.dialogRef.close();
            this.ngOnInit();
            this.showPortFile = false;
          },
          error: (err) => {
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
  onModalFileChange(event:Event):void{
    let fileInput = event.target as HTMLInputElement;
    if(fileInput && fileInput.files){
      const file = fileInput.files[0];
      this.uploadFileNameConfig = file.name
      this.uploadReadFileContent(file)
    }
  }
  uploadReadFileContent(file:File): void{
    const reader = new FileReader();
    reader.onload = (e:ProgressEvent<FileReader>)=>{
      const content = e.target?.result as string;
      this.uploadFileContent = content
    }
    reader.readAsText(file)
  }
  /**
   * The method is upload the default device configfile of editor modal
   */
  configDeviceFileUpload(): void{
    this.submitted = true;
      if(this.uploadDeviceConfigForm.invalid){
        return
      }else if(this.uploadCreateHeading ==='Upload Configuration File'){
        const editorFilename = this.uploadFileNameConfig;
        const content = this.uploadFileContent;
        const editorContent  = this.replaceTags(content);
        const contentBlob = new Blob([editorContent], {type:'text/plain'});
        const contentFile = new File([contentBlob],editorFilename);
        this.service.uploadConfigFile(contentFile).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 3000,
              panelClass: ['success-msg'],
              verticalPosition: 'top'
            })
            setTimeout(() => {
              this.uploadDeviceConfigForm.get('uploadConfigFileModal')?.reset();
              this.newDeviceDialogRef.close();
              this.visibilityConfigFile();
            }, 1000);
          },
          error:(err)=>{
            let errmsg = JSON.parse(err.error);
            this._snakebar.open(errmsg.message?errmsg.message:errmsg, '', {
              duration: 2000,
              panelClass: ['err-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
          }
        })
    }else{
      const editorFilename = this.uploadDeviceConfigForm.get('editorFilename')!.value;
      const content = this.uploadDeviceConfigForm.get('editorContent')!.value;
      const editorContent  = this.replaceTags(content);
      const contentBlob = new Blob([editorContent], {type:'text/plain'});
      const contentFile = new File([contentBlob],editorFilename);
      this.service.uploadConfigFile(contentFile).subscribe({
        next:(res)=>{
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.newDeviceDialogRef.close();
            this.visibilityConfigFile();
          }, 1000);
        },
        error:(err)=>{
          let errmsg = JSON.parse(err.error);
          this._snakebar.open(errmsg.message?errmsg.message:errmsg, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
      })
    }
  }  

  existDeviceDialog(): void {
    this.dialogRef = this.dialog.open(this.dialogTemplate, {
      width: '90vw', 
      height: '90vh' 
    });
  }
  closeDialog(): void {
    this.dialogRef.close();
  }
  openNewDeviceDialog(): void {
    this.newDeviceDialogRef = this.dialog.open(this.newDeviceTemplate, {
      width: '90vw', 
      height: '90vh'
    });
  }
  closeNewDeviceDialog(): void {
    this.newDeviceDialogRef.close();
  }


}
