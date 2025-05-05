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
import { Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
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

import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';
import { ModuleButtonComponent } from '../../../utility/component/modules-buttons/button/button.component';
import { ModulesService } from '../../../services/modules.service';
import { MatDialog } from '@angular/material/dialog';
import { MaterialModule } from '../../../material/material.module';
import { LoaderComponent } from '../../../utility/component/loader/loader.component';


@Component({
  selector: 'app-parameter-list',
  standalone: true,
  imports: [ MaterialModule, CommonModule, ReactiveFormsModule, AgGridAngular, HttpClientModule,
    LoaderComponent],
  templateUrl: './parameter-list.component.html',
  styleUrl: './parameter-list.component.css'
})
export class ParameterListComponent {
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 10;
  public paginationPageSizeSelector: number[] | boolean = [10, 15, 30, 50];
  public tooltipShowDelay = 500;
  public gridApi!: GridApi;
  public columnDefs: ColDef[] = [
    {
      headerName: 'Parameter Name',
      field: 'parameterName',
      filter: 'agTextColumnFilter',
      sort: 'asc',
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Parameter Type',
      field: 'parameterDataType',
      filter: 'agTextColumnFilter',
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Range Value',
      field: 'parameterRangeVal',
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
        selectedRowCount: () => this.selectedRowCount,
        lastSelectedNodeId: this.lastSelectedNodeId,
      })
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };
  gridOptions = {
    rowHeight: 36
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
  dynamicModuleName!:string;
  dynamicFunctionName!:string;
  categoryName: any;
  showLoader = false;

  constructor(private router: Router, private authservice: AuthService, 
    private _snakebar: MatSnackBar,private moduleservice: ModulesService,
    public dialog:MatDialog
  ) { }
  /**
   * Initializes the component.
  */
  ngOnInit(): void {
    let functiondata = JSON.parse(localStorage.getItem('function') || '{}');
    this.dynamicModuleName = functiondata.moduleName;
    this.dynamicFunctionName = functiondata.functionName;
    this.configureName = this.authservice.selectedConfigVal;
    if(this.configureName === 'RDKB'){
      this.categoryName = 'Broadband';
    }else{
      this.categoryName = 'Video';
    }
    this.parameterByFunction();
  }
  parameterByFunction():void{
    this.showLoader = true;
    this.moduleservice.findAllByFunction(this.dynamicFunctionName).subscribe({
      next:(data)=>{
        this.rowData = data.data;
        if(this.rowData == null || this.rowData == undefined|| this.rowData.length>0 ) {
        this.showLoader = false;
        }
      },
      error:(err)=>{
        this.showLoader = false;
        this._snakebar.open(err, '', {
          duration: 2000,
          panelClass: ['err-msg'],
          horizontalPosition: 'end',
          verticalPosition: 'top'
        })
      }

    })
  }
  /**
   * Event handler for when the grid is ready.
   * @param params The grid ready event parameters.
   */
  onGridReady(params: GridReadyEvent<any>):void{
    this.gridApi = params.api;
  }
    /**
   * Event handler for when a row is selected.
   * @param event The row selected event.
   */
    onRowSelected(event: RowSelectedEvent):void{
      this.isRowSelected = event.node.isSelected();
      this.rowIndex = event.rowIndex
    }
  
  /**
     * Event handler for when the selection is changed.
     * @param event The selection changed event.
  */
  onSelectionChanged(event: SelectionChangedEvent):void{
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
  createParameterName() :void{
    this.router.navigate(['/configure/parmeter-create']);
  }
  
  /**
   * Edits a user.
   * @param user The user to edit.
   * @returns The edited user.
   */
  userEdit(parameter: any):void{
      localStorage.setItem('parameters', JSON.stringify(parameter));
      this.router.navigate(['configure/parameter-edit']);
  }
  /**
   * Deletes a record.
   * @param data The data of the record to delete.
   */
  delete(data: any):void{
    if (confirm("Are you sure to delete ?")) {
      if(data){
        this.moduleservice.deleteParameter(data.id).subscribe({
          next:(res)=>{
            this.rowData = this.rowData.filter((row: any) => row.id !== data.id);
            this.rowData = [...this.rowData];
            this._snakebar.open(res.message, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
              })
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
   * Navigates back to the previous page.
   */
  goBack():void{
    this.router.navigate(["/configure/function-list"]);
  }

}
