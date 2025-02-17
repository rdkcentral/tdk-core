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
import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DeviceService } from '../../../services/device.service';
import { InputComponent } from '../../../utility/component/ag-grid-buttons/input/input.component';
import { Editor, NgxEditorModule } from 'ngx-editor';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { saveAs } from 'file-saver';
import { OemService } from '../../../services/oem.service';
import { DevicetypeService } from '../../../services/devicetype.service';
import { SocService } from '../../../services/soc.service';

@Component({
  selector: 'app-device-create',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule,MaterialModule,NgxEditorModule, FormsModule],
  templateUrl: './device-create.component.html',
  styleUrl: './device-create.component.css'
})
export class DeviceCreateComponent implements OnInit{
  @ViewChild('dialogTemplate', { static: true }) dialogTemplate!: TemplateRef<any>;
  @ViewChild('newDeviceTemplate', { static: true }) newDeviceTemplate!: TemplateRef<any>;
  deviceForm!: FormGroup;
  rdkBForm!:FormGroup;
  deviceFormSubmitted = false;
  rdkbFormSubmitted = false;
  rdkcFormSubmitted = false;
  showPortFile = false;
  showConfigPort = false;
  showConfigPortB = false;
  allDeviceType:any;
  alloem:any;
  allsoc:any;
  rowData:any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 5;
  public paginationPageSizeSelector: number[] | boolean = [5,10, 50, 100];
  gridApi!: any;
  showHideCreateFormV = true;
  showHideCreateFormB = false;
  rowHeight = 41;
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
  selectedDeviceCategory! : string;
  categoryName : string = 'Video';
  checkOcapId: any;
  editor!: Editor;
  editor2!: Editor;
  uploadConfigForm!: FormGroup;
  uploadDeviceConfigForm!:  FormGroup;
  uploadFormSubmitted = false;
  isEditingFile = false;
  configData:any;
  configFileName!:string;
  stbNameChange: any;
  filesList:any[]=[];
  deviceTypeValue: any;
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
  newFileName!: string;
  existingConfigEditor = true;
  uploadExistingConfig = false;
  showExistUploadButton = true;
  backToExistEditorbtn = false;
  uploadExistConfigHeading!: string;
  dialogRef!: MatDialogRef<any>;
  newDeviceDialogRef!: MatDialogRef<any>;
  isThunderPresent = false;
  // thunderTooltip: string = 'Please enter devicename and boxtype before you check this box';

  constructor( private router: Router,private fb:FormBuilder,
    private _snakebar :MatSnackBar, private oemService:OemService, 
    private service:DeviceService, private socService:SocService, private deviceTypeService:DevicetypeService,
    public dialog:MatDialog
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
    this.selectedDeviceCategory = this.loggedinUser.userCategory;
    this.categoryName = 'Video';
    if(deviceCategory){
      this.selectedDeviceCategory = deviceCategory
      this.configureName = deviceCategory;
    }
    if(deviceCategory===null){
      this.configureName = this.selectedDeviceCategory;
    }
    if(this.configureName ==='RDKV'){
      this.showHideCreateFormV = true;
      this.showHideCreateFormB = false;
      this.categoryName = 'Video';
    }
    if(this.configureName ==='RDKB'){
      this.showHideCreateFormV = false;
      this.showHideCreateFormB = true;
      this.categoryName = 'Broadband'
    }
    let ipregexp: RegExp = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    this.deviceForm = new FormGroup({
      devicename: new FormControl<string | null>('', { validators: [Validators.required,Validators.pattern(/^[a-zA-Z0-9_]+$/)] }),
      deviceip: new FormControl<string | null>('', { validators: [Validators.required,Validators.pattern(ipregexp)] }),
      macaddr: new FormControl<string | null>('', { validators: Validators.required }),
      devicetype: new FormControl<string | null>('', { validators: Validators.required }),
      oem: new FormControl<string | null>(''),
      soc: new FormControl<string | null>(''),
      streamingTemp: new FormControl<string | null>(''),
      thunderport:new FormControl<string | null>(''),
      isThunder: new FormControl<boolean | null>({value: false, disabled: false}),
      configuredevicePorts:new FormControl<boolean | null>(false),
      agentport: new FormControl<string | null>(this.agentport),
      agentstatusport: new FormControl<string | null>(this.agentStatusPort),
      agentmonitorport: new FormControl<string | null>(this.agentMonitoPort)
    })
    this.rdkBForm = new FormGroup({
      gatewayName: new FormControl<string | null>('', { validators: [Validators.required,Validators.pattern(/^[a-zA-Z0-9_]+$/)] }),
      gatewayIp: new FormControl<string | null>('', { validators: [Validators.required,Validators.pattern(ipregexp)] }),
      macaddr: new FormControl<string | null>('', { validators: Validators.required }),
      devicetype: new FormControl<string | null>('', { validators: Validators.required }),
      oem: new FormControl<string | null>(''),
      soc: new FormControl<string | null>(''),
      agentPortb: new FormControl<string | null>(''),
      agentStatusportB:new FormControl<string | null>(''),
      agentMonitorportB:new FormControl<string | null>('')
    })
    this.getAlldeviceType();
    this.getAllOem();
    this.getAllsoc();
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
    this.deviceForm.get('thunderport')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/^\s+|[^0-9]/g, '');
      if (cleanedValue !== value) {
        this.deviceForm.get('thunderport')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
    this.deviceForm.get('agentport')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/^\s+|[^0-9]/g, '');
      if (cleanedValue !== value) {
        this.deviceForm.get('agentport')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
    this.deviceForm.get('agentstatusport')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/^\s+|[^0-9]/g, '');
      if (cleanedValue !== value) {
        this.deviceForm.get('agentstatusport')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
    this.deviceForm.get('agentmonitorport')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/^\s+|[^0-9]/g, '');
      if (cleanedValue !== value) {
        this.deviceForm.get('agentmonitorport')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
    this.rdkBForm.get('agentPortb')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/^\s+|[^0-9]/g, '');
      if (cleanedValue !== value) {
        this.rdkBForm.get('agentPortb')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
    this.rdkBForm.get('agentStatusportB')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/^\s+|[^0-9]/g, '');
      if (cleanedValue !== value) {
        this.rdkBForm.get('agentStatusportB')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
    this.rdkBForm.get('agentMonitorportB')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/^\s+|[^0-9]/g, '');
      if (cleanedValue !== value) {
        this.rdkBForm.get('agentMonitorportB')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });


    this.deviceForm.get('devicename')?.valueChanges.subscribe((value) => {
      if (value) {
        this.deviceForm.get('devicename')?.setValue(value.toUpperCase());
      }
    });
    this.rdkBForm.get('gatewayName')?.valueChanges.subscribe((value) => {
      if (value) {
        this.rdkBForm.get('gatewayName')?.setValue(value.toUpperCase());
      }
    });

  }


  /**
   * Event handler for when the grid is ready.
   * @param params The grid ready event parameters.
   */
  onGridReady(params: any): void {
    this.gridApi = params.api;
  }
 /**
   * list of all boxtype.
   */
  getAlldeviceType(): void{
    this.deviceTypeService.getfindallbycategory(this.selectedDeviceCategory).subscribe(res=>{
      this.allDeviceType = (JSON.parse(res));
    })
  }
   /**
   * list of all boxmanufacturer.
   */
  getAllOem(): void{
    this.oemService.getOemByList(this.selectedDeviceCategory).subscribe(res=>{
      this.alloem = JSON.parse(res); 
    })
  }
   /**
   * list of all socVendors.
   */
  getAllsoc(): void{
    this.socService.getSoc(this.selectedDeviceCategory).subscribe(res=>{
      this.allsoc = JSON.parse(res);  
    })
  }
  /**
   * This methos is change the value of stbname inputfield
  */
  valuechange(event:any):void{
    this.visibilityConfigFile();
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
   * This methos is change the devicetype 
  */ 
    devicetypeChange(event:any): void{
      this.visibleDeviceconfigFile = false;
      let value = event.target.value;
      this.deviceTypeValue = value;
      this.visibilityConfigFile();
    }
  /**
   * Isthunder is checked or unchecked 
  */
  thunderChecked(event:any): void{
    this.isThunderPresent = event.target.checked;
    this.isThunderchecked = !this.isThunderchecked;
    if(this.isThunderchecked){
      this.isThunderPresent = true;
      this.showPortFile = true;
    }else{
      this.showPortFile = false;
      this.isThunderPresent = false;
    }
    this.visibilityConfigFile();
  }

  /**
   * Show the Config file or device.config file beased on stbname and boxtype
  */  
  visibilityConfigFile(): void{
    let boxNameConfig = this.deviceForm.value.devicename;
    let deviceTypeConfig = this.deviceForm.value.devicetype; 
    this.service.downloadDeviceConfigFile(boxNameConfig,deviceTypeConfig,this.isThunderPresent)
    .subscribe({ 
      next:(res)=>{
      this.configFileName = res.filename;
      if(this.configFileName !== `${boxNameConfig}.config` && this.stbNameChange !== undefined && this.stbNameChange !== ""){
        this.visibleDeviceconfigFile = true;
      }else{
        this.visibleDeviceconfigFile = false;
      }
      if(this.configFileName === `${deviceTypeConfig}.config`){
        this.visibleDeviceconfigFile = true;
        this.newFileName =`${deviceTypeConfig}.config`;
      }
      if(this.configFileName !== `${boxNameConfig}.config` && this.configFileName !== `${deviceTypeConfig}.config`){
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
    let boxNameConfig = this.deviceForm.value.devicename;
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
    localStorage.removeItem('deviceCategory');
    this.router.navigate(["/devices"]);
  }
  /**
   * Reset the device form.
   */
  reset(): void{
    this.deviceForm.reset();
  }
  resetFormB(): void{
    this.rdkBForm.reset();
  }
  /**
   * Submit the device form of RDKV category.
   */
  deviceVSubmit(): void{
    this.deviceFormSubmitted = true;
    if(this.deviceForm.invalid){
     return
    }else{
     let obj ={
      deviceIp : this.deviceForm.value.deviceip,
      deviceName : this.deviceForm.value.devicename,
      devicePort: this.deviceForm.value.agentport,
      statusPort: this.deviceForm.value.agentstatusport,
      agentMonitorPort: this.deviceForm.value.agentmonitorport,
      macId: this.deviceForm.value.macaddr,
      deviceTypeName: this.deviceForm.value.devicetype,
      oemName: this.deviceForm.value.oem,
      socName: this.deviceForm.value.soc,
      devicestatus : "FREE",
      thunderPort : this.deviceForm.value.thunderport,
      userGroupName : this.loggedinUser.userGroupName,
      category : this.selectedDeviceCategory,
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
        let errmsg = err.message?err.message:err.macId;
        // let errmessage = errmsg.message?errmsg.message:errmsg.macId;
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

  /**
   * Submit the device form of RDKB category.
   */
  deviceBSubmit(): void{
    this.rdkbFormSubmitted = true;
    if(this.rdkBForm.invalid){
      return
     }else{
      let rdkbObj={
        deviceIp : this.rdkBForm.value.gatewayIp,
        deviceName : this.rdkBForm.value.gatewayName,
        macId: this.rdkBForm.value.macaddr,
        deviceTypeName: this.rdkBForm.value.devicetype,
        oemName: this.rdkBForm.value.oem,
        socName: this.rdkBForm.value.soc,
        devicePort: this.rdkBForm.value.agentPortb,
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
          let errmsg = err.message?err.message:err.macId;
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
      let boxNameConfig = this.deviceForm.value.devicename;
      let deviceTypeConfig = this.deviceForm.value.devicetype;
      this.fileNameArray.push(boxNameConfig,deviceTypeConfig);
      this.currentIndex = (this.currentIndex + 1) % this.fileNameArray.length;
      this.uploadConfigForm.patchValue({
        editorFilename: `${this.fileNameArray[this.currentIndex]}.config`,
      })
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
        editorFilename: this.configFileName === 'sampleDevice.config'? this.newFileName: '',
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
      this.service.uploadConfigFile(contentFile,this.isThunderPresent).subscribe({
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
      this.service.uploadConfigFile(contentFile,this.isThunderPresent).subscribe({
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
   * The method is upload the configfile of fileupload
   */
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
        this.service.uploadConfigFile(contentFile,this.isThunderPresent).subscribe({
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
      this.service.uploadConfigFile(contentFile,this.isThunderPresent).subscribe({
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
  /**
   * open the existing device config modal onclick button.
  */
  existDeviceDialog(): void {
    this.dialogRef = this.dialog.open(this.dialogTemplate, {
      width: '90vw', 
      height: '90vh' 
    });
  }
  /**
   * close the existing device config modal.
  */
  closeDialog(): void {
    this.dialogRef.close();
  }
  /**
   * open the device config modal onclick button.
  */
  openNewDeviceDialog(): void {
    this.newDeviceDialogRef = this.dialog.open(this.newDeviceTemplate, {
      width: '90vw', 
      height: '90vh'
    });
  }
  /**
   * close the device config modal.
  */
  closeNewDeviceDialog(): void {
    this.newDeviceDialogRef.close();
  }
  /**
   * Download the  configuration file.
  */
  downloadConfigFile(){
    this.service.downloadDeviceConfigFile(this.stbNameChange,this.deviceTypeValue,this.isThunderPresent).subscribe({
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
