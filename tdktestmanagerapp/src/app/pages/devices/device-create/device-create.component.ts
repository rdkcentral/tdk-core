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
import { Component, ElementRef, OnInit, Renderer2, TemplateRef, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AgGridAngular } from 'ag-grid-angular';
import { ColDef,IMultiFilterParams } from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { BoxManufactureService } from '../../../services/box-manufacture.service';
import { DeviceService } from '../../../services/device.service';
import { SocVendorService } from '../../../services/soc-vendor.service';
import { BoxtypeService } from '../../../services/boxtype.service';
import { InputComponent } from '../../../utility/component/ag-grid-buttons/input/input.component';
import { StreamingTemplatesService } from '../../../services/streaming-templates.service';
import {  Editor, NgxEditorModule } from 'ngx-editor';
import { Modal } from 'bootstrap';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-device-create',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ReactiveFormsModule,MaterialModule,
    AgGridAngular,NgxEditorModule, FormsModule],
  templateUrl: './device-create.component.html',
  styleUrl: './device-create.component.css'
})
export class DeviceCreateComponent implements OnInit{
  @ViewChild('dialogTemplate', { static: true }) dialogTemplate!: TemplateRef<any>;
  @ViewChild('newDeviceTemplate', { static: true }) newDeviceTemplate!: TemplateRef<any>;
  deviceForm!: FormGroup;
  rdkBForm!:FormGroup;
  rdkCForm!:FormGroup;
  deviceFormSubmitted = false;
  rdkbFormSubmitted = false;
  rdkcFormSubmitted = false;
  showPortFile = false;
  showConfigPort = false;
  showConfigPortB = false;
  allBoxType:any;
  allboxManufacture:any;
  allsocVendors:any;
  allGatewayDevices:any;
  streamingTable= false;
  errormessage!:string;
  rowData:any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 5;
  public paginationPageSizeSelector: number[] | boolean = [5,10, 50, 100];
  gridApi!: any;
  showHideCreateFormV = true;
  showHideCreateFormB = false;
  showHideCreateFormC = false;
  rowHeight = 41;

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
      headerName: 'Audio Type',
      field: 'audioType',
      filter: 'agMultiColumnFilter',
      valueGetter:(params)=>params.data.audioType ?params.data.audioType:'NA',
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
      headerName: 'Video Type',
      field: 'videoType',
      filter: 'agMultiColumnFilter',
      valueGetter:(params)=>params.data.videoType ?params.data.videoType:'NA',
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
      cellRenderer:'inputCellRenderer',
   
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    autoHeight: true,
    menuTabs: ['filterMenuTab'],
  };
  configureName!: string;
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
  selectedDeviceCategory : string = 'RDKV';
  checkOcapId: any;
  editor!: Editor;
  editor2!: Editor;
  uploadConfigForm!: FormGroup;
  uploadDeviceConfigForm!:  FormGroup;
  uploadFormSubmitted = false;
  isMaximized = false;
  isEditingFile = false;
  configData:any;
  configFileName!:string;
  stbNameChange: any;
  filesList:any[]=[];
  boxTypeValue: any;
  visibleDeviceconfigFile = false;
  deviceEditor = true;
  uploadConfigSec = false;
  backToEditorbtn = false;
  showUploadButton = true;
  uploadCreateHeading: string ='Create New Device Config File';
  uploadFileName! :File;
  configDevicePorts = false;
  submitted = false;
  existConfigSubmitted = false;
  uploadFileContent! : string ;
  uploadExistFileContent!: string;
  uploadFileNameConfig!: string;
  fileNameArray:string[]=[];
  currentIndex: number = 0;
  extension: string = '.config';
  newFileName!: string;
  existingConfigEditor = true;
  uploadExistingConfig = false;
  showExistUploadButton = true;
  backToExistEditorbtn = false;
  uploadExistConfigHeading!: string;
  dialogRef!: MatDialogRef<any>;
  newDeviceDialogRef!: MatDialogRef<any>;
  selectedBoxType:any;
  isThunderPresent: any;
  streamingTempList:any[]=[];
  visibleStreamingList = false;
  thunderTooltip: string = 'Please enter stbname and boxtype before you check this box';

  constructor( private router: Router,private fb:FormBuilder,
    private _snakebar :MatSnackBar, private boxManufactureService:BoxManufactureService, 
    private service:DeviceService, private socVendorService:SocVendorService, private boxtypeService:BoxtypeService,
    private streamingService :StreamingTemplatesService, private renderer:Renderer2,public dialog:MatDialog
  ) { 
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
    this.frameworkComponents = {
      inputCellRenderer: InputComponent
    }
  }
  /**
   * The method to initialize the component.
   */
  ngOnInit(): void {
    const deviceCategory = localStorage.getItem('deviceCategory');
    if(deviceCategory){
      this.selectedDeviceCategory = deviceCategory;
      this.configureName = deviceCategory;
    }
    if(deviceCategory===null){
      this.configureName = this.selectedDeviceCategory;
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
    this.deviceForm = new FormGroup({
      stbname: new FormControl<string | null>('', { validators: Validators.required }),
      stbip: new FormControl<string | null>('', { validators: [Validators.required,Validators.pattern(ipregexp)] }),
      macaddr: new FormControl<string | null>('', { validators: Validators.required }),
      boxtype: new FormControl<string | null>('', { validators: Validators.required }),
      boxmanufacturer: new FormControl<string | null>('', { validators: Validators.required }),
      socvendor: new FormControl<string | null>('', { validators: Validators.required}),
      gateway: new FormControl<string | null>(''),
      streamingTemp: new FormControl<string | null>(''),
      thunderport:new FormControl<string | null>(''),
      isThunder: new FormControl<boolean | null>({value: false, disabled: true}),
      configuredevicePorts:new FormControl<boolean | null>(false),
      agentport: new FormControl<string | null>(this.agentport),
      agentstatusport: new FormControl<string | null>(this.agentStatusPort),
      agentmonitorport: new FormControl<string | null>(this.agentMonitoPort),
      recorderId: new FormControl<string | null>('')
    })
    this.rdkBForm = new FormGroup({
      gatewayName: new FormControl<string | null>('', { validators: Validators.required }),
      gatewayIp: new FormControl<string | null>('', { validators: [Validators.required,Validators.pattern(ipregexp)] }),
      macaddr: new FormControl<string | null>('', { validators: Validators.required }),
      boxtype: new FormControl<string | null>('', { validators: Validators.required }),
      boxmanufacturer: new FormControl<string | null>('', { validators: Validators.required }),
      socvendor: new FormControl<string | null>('', { validators: Validators.required}),
      agentPortb: new FormControl<string | null>(''),
      agentStatusportB:new FormControl<string | null>(''),
      agentMonitorportB:new FormControl<string | null>('')
    })
    this.rdkCForm = new FormGroup({
      cameraName: new FormControl<string | null>('', { validators: Validators.required }),
      stbIp: new FormControl<string | null>('', { validators: [Validators.required,Validators.pattern(ipregexp)] }),
      macaddr: new FormControl<string | null>('', { validators: Validators.required }),
      boxtype: new FormControl<string | null>('', { validators: Validators.required }),
      boxmanufacturer: new FormControl<string | null>('', { validators: Validators.required }),
      socvendor: new FormControl<string | null>('', { validators: Validators.required}),
      agentPortb: new FormControl<string | null>(this.agentport),
      agentStatusportB:new FormControl<string | null>(this.agentStatusPort),
      agentMonitorportB: new FormControl<string | null>(this.agentMonitoPort)
    })
    this.streamingService.getstreamingdetails().subscribe(res=>{
      this.rowData = res;
    })
    this.getAllboxType();
    this.getAllboxmanufacture();
    this.getAllsocVendors();
    this.editor = new Editor();
    this.editor2 = new Editor();
    this.uploadConfigForm = this.fb.group({
      editorFilename:['',{disabled: true}],
      editorContent: ['',[Validators.required]],
    });
    this.filesList =[];
    this.uploadDeviceConfigForm = this.fb.group({
      editorFilename:['',{disabled: true}],
      editorContent: ['',[Validators.required]],
      uploadConfigFileModal:['']
    });
    this.getTemplatelist();

  }

  /**
   * The method to check thunder enable or disable.
   */
  checkIsThunderValidity(): void{
    const stbName = this.stbNameChange;
    const boxType = this.boxTypeValue;
    if(stbName && boxType){
      this.deviceForm.get('isThunder')?.enable();
      this.thunderTooltip = 'Check the box for devices with Rdkservice image';
    }else{
      this.deviceForm.get('isThunder')?.disable();
      this.deviceForm.get('isThunder')?.setValue(false);
      this.showPortFile = false;
      this.isThunderchecked = false;
      this.thunderTooltip = 'Please enter stbname and boxtype before you check this box';
    }
  }

  /**
   * Event handler for when the grid is ready.
   * @param params The grid ready event parameters.
   */
  onGridReady(params: any): void {
    this.gridApi = params.api;
  }
  /**
   * The method render the list of streaming template.
   */
  getTemplatelist():void{
    this.service.streamingTemplateList().subscribe(res=>{
      this.streamingTempList = JSON.parse(res);
    })
  }
 /**
   * list of all boxtype.
   */
  getAllboxType(): void{
    this.boxtypeService.getfindallbycategory(this.selectedDeviceCategory).subscribe(res=>{
      this.allBoxType = (JSON.parse(res));
    })
  }
   /**
   * list of all boxmanufacturer.
   */
  getAllboxmanufacture(): void{
    this.boxManufactureService.getboxManufactureByList(this.selectedDeviceCategory).subscribe(res=>{
      this.allboxManufacture = JSON.parse(res); 
    })
  }
   /**
   * list of all socVendors.
   */
  getAllsocVendors(): void{
    this.socVendorService.getSocVendor(this.selectedDeviceCategory).subscribe(res=>{
      this.allsocVendors = JSON.parse(res);  
    })
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
  streamTempChange(event:any):void{
    const tempName = event.target.value;
    if(tempName != null || tempName != ''){
      this.service.streamingDetailsByTemplate(tempName).subscribe(res=>{
        this.rowData = JSON.parse(res);
      })
    }
    if(tempName === null || tempName === ''){
      this.streamingService.getstreamingdetails().subscribe(res=>{
        this.rowData = res;
      })
    }
  }
  /**
   * This methos is change the boxtype 
  */ 
    boxtypeChange(event:any): void{
      this.visibleDeviceconfigFile = false;
      let value = event.target.value;
      this.boxTypeValue = value;
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
      const selectedType = this.allBoxType.find((item:any) => item.boxTypeName === dropdown.value)
      this.selectedBoxType = selectedType;
      localStorage.setItem('boxtypeDropdown',JSON.stringify(selectedType));
      if( selectedType.type === 'CLIENT' || selectedType.type ==='STAND_ALONE_CLIENT'){
        this.visibleGateway = true;
        this.visibleStreamingList = false;
        this.service.getlistofGatewayDevices(this.selectedDeviceCategory).subscribe(res=>{
          this.allGatewayDevices = JSON.parse(res)
        })
      }else{
        this.visibleGateway = false;
        this.visibleStreamingList = true;
      }
      if(this.isThunderchecked){
        this.showPortFile = true;
        this.visibilityConfigFile();
      }
      if (this.selectedBoxType.type ==='STAND_ALONE_CLIENT' || this.selectedBoxType.type ==='GATEWAY') {
        this.streamingTable = !this.isThunderchecked;
      } else if (this.selectedBoxType.type ==="CLIENT") {
        this.streamingTable = false;
      }
    }
  /**
   * Isthunder is checked or unchecked 
  */
  thunderChecked(event:any): void{
    this.isThunderPresent = event.target.checked;
    this.isThunderchecked = !this.isThunderchecked;
    if(this.isThunderchecked){
      this.showPortFile = true;
      this.streamingTable = false;
      this.visibilityConfigFile();
    }else{
      this.showPortFile = false;
      this.streamingTable = false;
    }
    if (this.selectedBoxType.type ==='STAND_ALONE_CLIENT' || this.selectedBoxType.type ==='GATEWAY') {
      this.streamingTable = !this.isThunderchecked;
    } else if (this.selectedBoxType.type ==="CLIENT") {
      this.streamingTable = false;
    }
  }

  /**
   * Show the Config file or device.config file beased on stbname and boxtype
  */  
  visibilityConfigFile(): void{
    let boxNameConfig = this.deviceForm.value.stbname;
    let boxTypeConfig = this.deviceForm.value.boxtype; 
    this.service.downloadDeviceConfigFile(boxNameConfig,boxTypeConfig)
    .subscribe({ 
      next:(res)=>{
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
  
      this.readDeviceFileContent(res.content); 
      this.uploadDeviceConfigForm.patchValue({
        editorFilename: this.stbNameChange+'.config',
        editorContent: this.configData
      })
    },
    error(err){
      const sts = err.status;
    }

    })
  }
  /**
   * Reading the configfile
  */ 
  readFileContent(file:Blob): void{
    let boxNameConfig = this.deviceForm.value.stbname;
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

  isConfigDevicePorts(event:any): void{
    if(event.target.checked){
      this.showConfigPort = true;
      this.configDevicePorts = true;
    }else{
      this.showConfigPort = false;
      this.configDevicePorts = false;
    }
  }
  isCheckedConfigB(event:any): void{
    if(event.target.checked){
      this.showConfigPortB = true;
    }else{
      this.showConfigPortB = false;
    }
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
   * Go back to the previous page.
   */
  goBack(): void{
    this.router.navigate(["/devices"]);
  }
  /**
   * Reset the device form.
   */
  reset(): void{
    this.deviceForm.reset();
  }
  /**
   * Submit the device form of RDKV category.
   */
  deviceVSubmit(): void{
    this.deviceFormSubmitted = true;
    if(this.deviceForm.invalid){
     return
    }else{
     if(this.streamingTable==true){
      const tableData :any[]=[];
      this.gridApi.forEachNode((element: any) => {
       tableData.push(element.data)
       this.streamingMapObj = tableData.map((streamingDetailsId: any, ocapId: any) => ({streamId: streamingDetailsId.streamingDetailsId ,ocapId: streamingDetailsId.ocapId}));
      });
      this.rowData.forEach((row:any)=>{
      row.showError = !row.ocapId
      })
     for (let i = 0; i < this.streamingMapObj.length; i++) {
      this.checkOcapId = this.streamingMapObj[i];
     }
      this.streamingMapObj = [...this.streamingMapObj]
    }

     let obj ={
      stbIp : this.deviceForm.value.stbip,
      stbName : this.deviceForm.value.stbname,
      stbPort: this.deviceForm.value.agentport,
      statusPort: this.deviceForm.value.agentstatusport,
      agentMonitorPort: this.deviceForm.value.agentmonitorport,
      macId: this.deviceForm.value.macaddr,
      boxTypeName: this.deviceForm.value.boxtype,
      boxManufacturerName: this.deviceForm.value.boxmanufacturer,
      socVendorName: this.deviceForm.value.socvendor,
      devicestatus : "FREE",
      recorderId : this.deviceForm.value.recorderId,
      gatewayDeviceName : this.deviceForm.value.gateway,
      thunderPort : this.deviceForm.value.thunderport,
      userGroupName : this.loggedinUser.userGroupName,
      category : this.selectedDeviceCategory,
      deviceStreams : this.streamingMapObj?this.streamingMapObj:null,
      thunderEnabled :this.isThunderchecked,
      configuredevicePorts:this.configDevicePorts
    }
      this.service.createDevice(obj).subscribe({
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
        this._snakebar.open(err.error?err.error:(JSON.parse(err.error)).message, '', {
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
   * Submit the device form of RDKB category.
   */
  deviceBSubmit(): void{
    this.rdkbFormSubmitted = true;
    if(this.rdkBForm.invalid){
      return
     }else{
      let rdkbObj={
        stbIp : this.rdkBForm.value.gatewayIp,
        stbName : this.rdkBForm.value.gatewayName,
        macId: this.rdkBForm.value.macaddr,
        boxTypeName: this.rdkBForm.value.boxtype,
        boxManufacturerName: this.rdkBForm.value.boxmanufacturer,
        socVendorName: this.rdkBForm.value.socvendor,
        stbPort: this.rdkBForm.value.agentPortb,
        statusPort: this.rdkBForm.value.agentStatusportB,
        agentMonitorPort: this.rdkBForm.value.agentMonitorportB,
        devicestatus : "FREE",
        userGroupName : this.loggedinUser.userGroupName,
        category : this.selectedDeviceCategory
      }
      this.service.createDevice(rdkbObj).subscribe({
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
          this._snakebar.open(errmsg.message?errmsg.message:errmsg.macId, '', {
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
   * Submit the device form of RDKC category.
   */
  deviceCSubmit(): void{
    this.rdkcFormSubmitted = true;
    if(this.rdkCForm.invalid){
      return
     }else{
      let rdkcObj = {
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
      this.service.createDevice(rdkcObj).subscribe({
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
          this._snakebar.open(errmsg.message?errmsg.message:errmsg.macId, '', {
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
      let boxNameConfig = this.deviceForm.value.stbname;
      let boxTypeConfig = this.deviceForm.value.boxtype;
      this.fileNameArray.push(boxNameConfig,boxTypeConfig);
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
   * The method is upload the configfile of editor modal
   */
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
            if (this.dialogRef) {
              this.dialogRef.close();
              this.visibilityConfigFile();
            }
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
  replaceTags(content:string):string{
    const replacepara = content.replace(/<\/?p>/g,'\n');
    const replacebreakes = replacepara.replace(/<br\s*\/?>/g,'\n');
    return replacebreakes.trim();
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
              this.closeNewDeviceDialog();
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
            this.closeNewDeviceDialog();
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
            this.showPortFile = true;
            this.visibilityConfigFile();
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
  downloadConfigFile(){
    this.service.downloadDeviceConfigFile(this.stbNameChange,this.boxTypeValue).subscribe({
      next:(res)=>{
        const filename = res.filename;
        const blob = new Blob([res.content], { type: res.content.type || 'application/json' });
        saveAs(blob, filename); 
      },
      error:(err)=>{
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
}
