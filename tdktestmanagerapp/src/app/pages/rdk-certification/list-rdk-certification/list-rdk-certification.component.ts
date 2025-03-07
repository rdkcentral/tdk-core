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
import { Component, ElementRef, Renderer2, ViewChild } from '@angular/core';
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
/**
 * Component for listing RDK certifications.
 */
export class ListRdkCertificationComponent {

  @ViewChild('certificateModal', { static: false }) certificateModal?: ElementRef;
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
  uploadConfigurationForm!: FormGroup;
  uploadFormSubmitted = false;
  uploadFileName!: File;
  configureName!: string;

  /**
   * Column definitions for the ag-Grid table in the RDK Certification List component.
   * 
   * @type {ColDef[]}
   * @property {ColDef} columnDefs[].headerName - The header name of the column.
   * @property {ColDef} columnDefs[].field - The field name of the column.
   * @property {ColDef} columnDefs[].filter - The filter type for the column.
   * @property {ColDef} columnDefs[].flex - The flex property to adjust column width.
   * @property {IMultiFilterParams} columnDefs[].filterParams - Parameters for the filter.
   * @property {boolean} columnDefs[].sortable - Indicates if the column is sortable.
   * @property {any} columnDefs[].cellRenderer - The component used to render cells in this column.
   * @property {Function} columnDefs[].cellRendererParams - Function to return parameters for the cell renderer.
   * @property {Function} columnDefs[].cellRendererParams.onEditClick - Callback for the edit button click event.
   * @property {Function} columnDefs[].cellRendererParams.onDownloadClick - Callback for the download button click event.
   * @property {Function} columnDefs[].cellRendererParams.selectedRowCount - Function to get the count of selected rows.
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
        onDownloadClick: this.downloadConfigFile.bind(this),
        onDeleteClick: this.delete.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };

  constructor(private http: HttpClient, private router: Router, private renderer: Renderer2,
    private authservice: AuthService, private service: RdkService, private _snakebar: MatSnackBar) { }

  /**
   * Initializes the component by fetching all RDK certifications and setting up the form.
   * 
   * - Fetches all RDK certifications from the service and maps them to `rowData`.
   * - Sets the `configureName` and `categoryName` from the authentication service.
   * - Initializes the `uploadConfigurationForm` with a required `uploadConfig` control.
   * 
   * @returns {void}
   */
  ngOnInit(): void {

    this.configureName = this.authservice.selectedConfigVal;
    this.categoryName = this.authservice.showSelectedCategory;
    this.uploadConfigurationForm = new FormGroup({
      uploadConfig: new FormControl<string | null>('', { validators: Validators.required }),
    })
    this.getAllCerificate();
  }

  getAllCerificate():void{
    this.service.getallRdkCertifications().subscribe(res => {
      const certificationNames = JSON.parse(res);
      this.rowData = certificationNames.map((name: any) => ({ name }));
    })
  }
  /**
   * Event handler for when the grid is ready.
   * 
   * @param {GridReadyEvent<any>} params - The event parameters containing the grid API.
   */
  onGridReady(params: GridReadyEvent<any>) : void {
    this.gridApi = params.api;
  }

  /**
   * Navigates to the edit RDK certifications page after storing the user information in local storage.
   *
   * @param user - The user object containing information to be stored in local storage.
   * @returns void
   */
  userEdit(user: any): void {
    localStorage.setItem('user', JSON.stringify(user))
    this.router.navigate(['configure/edit-rdk-certifications']);
  }

  /**
   * Navigates to the "create RDK certifications" configuration page.
   * This method is triggered when the user wants to create a new RDK certification.
   * It uses the Angular Router to navigate to the specified route.
   */
  createRdkCertification(): void {
    this.router.navigate(["configure/create-rdk-certifications"]);
  }


  /**
   * Handles the file input change event.
   * 
   * This method is triggered when a user selects a file. It checks if the selected file
   * is a Python (.py) file. If it is, the file is assigned to `uploadFileName`. Otherwise,
   * an alert is shown to the user indicating that a valid Python file must be selected.
   * 
   * @param event - The file input change event containing the selected file.
   */
  onFileChange(event: any) : void {
    this.uploadFileName = event.target.files[0].name;
    const file: File = event.target.files[0];
    if (file && file.name.toLowerCase().endsWith('.py')) {
      this.uploadFileName = file;
    } else {
      alert('Please select a valid Python (.py) file.');
    }
  }


  /**
   * Closes the certificate modal by setting its display style to 'none'.
   * Also removes the 'overflow' and 'padding-right' styles from the document body.
   */
  close(): void {
    (this.certificateModal?.nativeElement as HTMLElement).style.display = 'none';
    this.renderer.removeStyle(document.body, 'overflow');
    this.renderer.removeStyle(document.body, 'padding-right');
  }

  /**
   * Handles the submission of the upload configuration form.
   * 
   * This method sets the `uploadFormSubmitted` flag to true and checks if the form is valid.
   * If the form is invalid, it returns early. If the form is valid and a file name is provided,
   * it calls the `uploadConfigFile` method of the service with the file name.
   * 
   * On successful upload, it displays a success message using `_snakebar`, closes the form,
   * and reinitializes the component by calling `ngOnInit`.
   * 
   * On error, it displays an error message using `_snakebar`, reinitializes the component,
   * closes the form, and resets the upload configuration form.
   */
  uploadConfigurationSubmit() : void {
    this.uploadFormSubmitted = true;
    if (this.uploadConfigurationForm.invalid) {
      return
    } else {
      if (this.uploadFileName) {
        this.service.uploadConfigFile(this.uploadFileName).subscribe({
          next: (res) => {
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
            this.close();
            this.ngOnInit();
          },
          error: (err) => {
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
   * Downloads a configuration file based on the provided parameters.
   * 
   * @param params - The parameters containing the name of the configuration file to download.
   * 
   * If the `params` object contains a `name` property, this method will call the `downloadConfig` 
   * method of the service with the provided name. Upon successful download, it will create a 
   * Blob from the response content and trigger a file save with the appropriate filename.
   * 
   * In case of an error during the download process, an error message will be displayed using 
   * a snackbar with a duration of 2000 milliseconds.
   */
  downloadConfigFile(params: any): void {
    if (params.name) {
      this.service.downloadConfig(params.name).subscribe({
        next: (res) => {
          const filename = res.filename;
          const blob = new Blob([res.content], { type: res.content.type || 'application/json' });
          saveAs(blob, filename);
        },
        error: (err) => {
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
   * Navigates back to the configuration page and sets the selected configuration
   * value and category in the authentication service.
   *
   * @remarks
   * This method updates the `selectedConfigVal` to 'RDKV' and the `showSelectedCategory`
   * to 'Video' in the `authservice`. It then navigates to the '/configure' route.
   */
  goBack(): void {
    this.authservice.selectedConfigVal = 'RDKV';
    this.authservice.showSelectedCategory = "Video";
    this.router.navigate(["/configure"]);
  }

  delete(data: any):void{
    if (confirm("Are you sure to delete ?")) {
      this.service.deleteRdkCertification(data.name).subscribe({
        next: (res) => {
          this.rowData = this.rowData.filter((row: any) => row.name !== data.name);
          this.rowData = [...this.rowData];
          this._snakebar.open(res, '', {
            duration: 1000,
            panelClass: ['success-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        },
        error: (err) => {
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

}
