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
import { Component, ElementRef, Renderer2, ViewChild } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  GridApi,
  GridReadyEvent,
  IMultiFilterParams,
  RowSelectedEvent,
  SelectionChangedEvent
} from 'ag-grid-community';
import { Router } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';
import { ModuleButtonComponent } from '../../../utility/component/modules-buttons/button/button.component';
import { MatDialog } from '@angular/material/dialog';
import { ModulesViewComponent } from '../modules-view/modules-view.component';
import { ModulesService } from '../../../services/modules.service';

@Component({
  selector: 'app-modules-list',
  standalone: true,
  imports: [ RouterLink, CommonModule, ReactiveFormsModule, AgGridAngular, HttpClientModule],
  templateUrl: './modules-list.component.html',
  styleUrl: './modules-list.component.css'
})
export class ModulesListComponent {

  @ViewChild('staticBackdrop', {static: false}) staticBackdrop?:ElementRef;
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 7;
  public paginationPageSizeSelector: number[] | boolean = [7, 15, 30, 50];
  public tooltipShowDelay = 500;
  public gridApi!: GridApi;
  selectedDeviceCategory : string = 'RDKV';
  uploadXMLForm!:FormGroup;
  uploadFormSubmitted = false;
  uploadFileName! :File;
  public columnDefs: ColDef[] = [
    {
      headerName: 'Module Name',
      field: 'moduleName',
      filter: 'agTextColumnFilter',
      sort: 'asc',
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Test Group',
      field: 'testGroup',
      filter: 'agTextColumnFilter',
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Execution TimeOut',
      field: 'executionTime',
      filter: 'agTextColumnFilter',
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      headerClass: 'no-sort',
      cellRenderer: ModuleButtonComponent,
      cellRendererParams: (params: any) => ({
        onEditClick: this.userEdit.bind(this),
        onDeleteClick: this.delete.bind(this),
        onViewClick:this.openModal.bind(this),
        onFunctionClick:this.createFunction.bind(this),
        selectedRowCount: () => this.selectedRowCount,
        lastSelectedNodeId: this.lastSelectedNodeId,
      })
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };
  configureName!: string;
  selectedConfig!: string | null;
  lastSelectedNodeId: string | undefined;
  rowData: any = [];
  isRowSelected: any;
  selectedRow: any;
  isCheckboxSelected: boolean = false;
  rowIndex!: number | null;
  selectedRowCount = 0;
  constructor(private router: Router, private authservice: AuthService, 
    private _snakebar: MatSnackBar, public dialog:MatDialog, private moduleservice:ModulesService,private renderer: Renderer2
  ) { }
  /**
   * Initializes the component.
  */
  ngOnInit(): void {
    this.configureName = this.authservice.selectedConfigVal;
    this.findallbyCategory(); 
    this.uploadXMLForm = new FormGroup({
      uploadXml: new FormControl<string | null>('', { validators: Validators.required }),
    })   
  }
 /**
   * Finds all devices by category.
   */
 findallbyCategory(){
  this.moduleservice.findallbyCategory(this.configureName).subscribe(res=>{
    let data = JSON.parse(res);
    this.rowData = data;
    // this.rowData = data.sort((a: any, b: any) =>a.stbName.toString().localeCompare(b.stbName.toString()));
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
   * Event handler for when a row is selected.
   * @param event The row selected event.
   */
    onRowSelected(event: RowSelectedEvent) {
      this.isRowSelected = event.node.isSelected();
      this.rowIndex = event.rowIndex
    }
  
  /**
     * Event handler for when the selection is changed.
     * @param event The selection changed event.
  */
  onSelectionChanged(event: SelectionChangedEvent) {
      this.selectedRowCount = event.api.getSelectedNodes().length;
      const selectedNodes = event.api.getSelectedNodes();
      this.lastSelectedNodeId = selectedNodes.length > 0 ? selectedNodes[selectedNodes.length - 1].id : '';
      this.selectedRow = this.isRowSelected ? selectedNodes[0].data : null;
      if (this.gridApi) {
        this.gridApi.refreshCells({ force: true })
      }
    }

  /**
   * Creates a new box manufacturer.
   */
  createModule() {
    this.router.navigate(['/configure/modules-create']);
  }
  
    /**
   * Edits a user.
   * @param user The user to edit.
   * @returns The edited user.
   */
  userEdit(modules: any): any {
      localStorage.setItem('modules', JSON.stringify(modules))
      // this.service.currentUrl = user.userGroupId;
      this.router.navigate(['configure/modules-edit']);
  }
  /**
   * Deletes a record.
   * @param data The data of the record to delete.
   */
  delete(data: any) {
    if (confirm("Are you sure to delete ?")) {
      if(data){
        this.moduleservice.deleteModule(data.id).subscribe({
          next:(res)=>{
            this.rowData = this.rowData.filter((row: any) => row.id !== data.id);
            this.rowData = [...this.rowData];
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
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
   * Displays the specified data.
   * 
   * @param data - The data to be displayed.
   */

  openModal(data:any){
    this.dialog.open( ModulesViewComponent,{
      width: '99%',
      height: '93vh',
      maxWidth:'100vw',
      panelClass: 'custom-modalbox',
      data:{
        executionTimeOut: data.executionTime,
        moduleName:data.moduleName,
        testGroup: data.testGroup,
        moduleThunderEnabled:data.moduleThunderEnabled,
        moduleAdvanced:data.moduleAdvanced,
        moduleCrashLogFiles:data.moduleCrashLogFiles,
        moduleLogFileNames: data.moduleLogFileNames
      }
    })
    
  }

  dowloadAllModule(){
    if(this.rowData.length > 0){
      this.moduleservice.downloadModuleByCategory(this.selectedDeviceCategory);
    }else{
      this._snakebar.open('No data available for download', '', {
        duration: 2000,
        panelClass: ['err-msg'],
        horizontalPosition: 'end',
        verticalPosition: 'top'
      })
    }

  }

  uploadXMLSubmit(){
    this.uploadFormSubmitted = true;
    if(this.uploadXMLForm.invalid){
      return
     }else{
      if(this.uploadFileName){
        this.moduleservice.uploadXMLFile(this.uploadFileName).subscribe({
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
   * Creates a function and stores the user data in the local storage.
   * Navigates to the '/configure/function-list' route.
   * 
   * @param data - The data to be stored in the local storage.
   */
  createFunction(data:any){
    localStorage.setItem('modules', JSON.stringify(data));
    this.router.navigate(['/configure/function-list']);
  }

  /**
   * Creates a parameter and navigates to the parameter list page.
   * @param data - The data to be stored in the local storage.
   */
  createParameter(data:any){
    localStorage.setItem('user', JSON.stringify(data));
    this.router.navigate(['/configure/parameter-list']);
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
   * Closes the modal  by click on button .
   */
  close(){
    (this.staticBackdrop?.nativeElement as HTMLElement).style.display = 'none';
    this.renderer.removeStyle(document.body, 'overflow');
    this.renderer.removeStyle(document.body, 'padding-right');
  }
  /**
   * Navigates back to the previous page.
   */
  goBack() {
    this.router.navigate(["/configure"]);
  }

}
