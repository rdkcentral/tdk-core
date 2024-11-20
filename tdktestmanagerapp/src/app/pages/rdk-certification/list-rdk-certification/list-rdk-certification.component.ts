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
import { Component, ElementRef,Renderer2, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  GridApi,
  GridReadyEvent,
  IMultiFilterParams,
} from 'ag-grid-community';
import { HttpClient } from '@angular/common/http';
import { ButtonComponent } from '../../../utility/component/ag-grid-buttons/button/button.component';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { AuthService } from '../../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MaterialModule } from '../../../material/material.module';
import { RdkService } from '../../../services/rdk-certification.service';
import { saveAs } from 'file-saver';
import { CdkStepperModule } from '@angular/cdk/stepper';

@Component({
  selector: 'app-list-rdk-certification',
  standalone: true,
  imports: [MaterialModule, CommonModule, ReactiveFormsModule, AgGridAngular, CdkStepperModule],
  templateUrl: './list-rdk-certification.component.html',
  styleUrl: './list-rdk-certification.component.css'
})
export class ListRdkCertificationComponent {

  @ViewChild('staticBackdrop', {static: false}) staticBackdrop?:ElementRef;
  public rowSelection: 'single' | 'multiple' = 'single';
  lastSelectedNodeId: string | undefined;
  rowData: any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 7;
  public paginationPageSizeSelector: number[] | boolean = [7, 15, 30, 50];
  public tooltipShowDelay = 500;
  isRowSelected: any;
  selectedRow: any;
  isCheckboxSelected: boolean = false;
  public gridApi!: GridApi;
  rowIndex!: number | null;
  selectedRowCount = 0;
  showUpdateButton = false;
  categoryName!: string;
  uploadConfigurationForm!:FormGroup;
  uploadFormSubmitted = false;
  uploadFileName! :File;

  /**
   * The column definitions for the grid.
   */
  public columnDefs: ColDef[] = [
    {
      headerName: 'Name',
      field: 'name',   
      filter: 'agTextColumnFilter',  
      flex: 1,
      filterParams: {} as IMultiFilterParams
  },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      cellRenderer: ButtonComponent,
      cellRendererParams: (params: any) => ({
        onEditClick: this.userEdit.bind(this),
        onDownloadClick:this.downloadConfigFile.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };
  configureName!: string;

  constructor(private http: HttpClient, private router: Router, private renderer: Renderer2,
    private authservice: AuthService, private service:RdkService, private _snakebar: MatSnackBar) { }


  /**
   * Initializes the component.
   */
  ngOnInit(): void {
    this.service.getallRdkCertifications().subscribe(res => {
      const certificationNames = JSON.parse(res); 
      this.rowData = certificationNames.map((name: any) => ({ name })); 
    })
    this.configureName = this.authservice.selectedConfigVal;
    this.categoryName = this.authservice.showSelectedCategory;
    this.uploadConfigurationForm = new FormGroup({
      uploadConfig: new FormControl<string | null>('', { validators: Validators.required }),
    })
  }

  /**
   * Event handler for when the grid is ready.
   * @param params The grid ready event parameters.
   */
  onGridReady(params: GridReadyEvent<any>) {
    this.gridApi = params.api;
  }

  /**
   * Edit the user.
   * @param user The user to edit.
   * @returns The edited user.
   */
  userEdit(user: any): void {
    localStorage.setItem('user', JSON.stringify(user))
    this.router.navigate(['configure/edit-rdk-certifications']);
  }

  /**
   * Create Rdk certifications
   */
  createRdkCertification():void {
    this.router.navigate(["configure/create-rdk-certifications"]);
  }

   /**
   * Handles the file change event when a file is selected for upload.
   * @param event - The file change event object.
   */
   onFileChange(event:any){
    this.uploadFileName = event.target.files[0].name;
    const file: File = event.target.files[0];
    if (file && file.name.toLowerCase().endsWith('.py')) {
      this.uploadFileName = file;
    } else {
      alert('Please select a valid Python (.py) file.');
    }
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
   * 
   * @returns 
   */
  uploadConfigurationSubmit(){
    this.uploadFormSubmitted = true;
    if(this.uploadConfigurationForm.invalid){
      return
     }else{
      if(this.uploadFileName){
        this.service.uploadConfigFile(this.uploadFileName).subscribe({
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
            this.uploadConfigurationForm.reset();
          }
        })
      }
     }
  }

  /**
   * 
   * @param params 
   */
  downloadConfigFile(params:any):void{
    if(params.name){
      this.service.downloadConfig(params.name).subscribe({
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

  /**
   * Go back to the previous page.
   */  
  goBack():void {
    this.authservice.selectedConfigVal = 'RDKV';
    this.authservice.showSelectedCategory = "Video";
    this.router.navigate(["/configure"]);
  }



}
