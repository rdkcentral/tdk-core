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
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';
import { ModuleButtonComponent } from '../../../utility/component/modules-buttons/button/button.component';
import { ModulesService } from '../../../services/modules.service';
import { MatDialog } from '@angular/material/dialog';
import { MaterialModule } from '../../../material/material.module';

@Component({
  selector: 'app-function-list',
  standalone: true,
  imports: [ MaterialModule, CommonModule, ReactiveFormsModule, AgGridAngular, HttpClientModule],
  templateUrl: './function-list.component.html',
  styleUrl: './function-list.component.css'
})
export class FunctionListComponent {
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 10;
  public paginationPageSizeSelector: number[] | boolean = [10, 15, 30, 50];
  public tooltipShowDelay = 500;
  public gridApi!: GridApi;
  public columnDefs: ColDef[] = [
    {
      headerName: 'Function Name',
      field: 'functionName',
      filter: 'agTextColumnFilter',
      sort: 'asc',
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
        onParameterClick:this.createParameter.bind(this),
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
  categoryName: any;

  constructor(private router: Router, private authservice: AuthService, 
    private _snakebar: MatSnackBar,private moduleservice:ModulesService, public dialog:MatDialog,
  ) { }

  /**
   * Initializes the component.
  */
  ngOnInit(): void {
    let data = JSON.parse(localStorage.getItem('modules') || '{}');
    this.dynamicModuleName = data.moduleName;
    this.configureName = this.authservice.selectedConfigVal;
    this.functionListByModule();
    this.categoryName = this.authservice.showSelectedCategory;
  }
  /**
   * Function to get the list of function by module name.
  */
  functionListByModule():void{
    this.moduleservice.functionList(this.dynamicModuleName).subscribe( res=>{
      this.rowData = JSON.parse(res);
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
    onRowSelected(event: RowSelectedEvent):void{
      this.isRowSelected = event.node.isSelected();
      this.rowIndex = event.rowIndex
    }
  
  /**
     * Event handler for when the selection is changed.
     * @param event The selection changed event.
  */
  onSelectionChanged(event: SelectionChangedEvent) :void{
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
  goTocreateFunctionPage() :void{
    this.router.navigate(['/configure/function-create']);
  }
  
    /**
   * Edits a user.
   * @param user The user to edit.
   * @returns The edited user.
   */
  userEdit(functions: any):void{
      localStorage.setItem('functions', JSON.stringify(functions));
      this.router.navigate(['configure/function-edit']);
  }
  /**
   * Deletes a record.
   * @param data The data of the record to delete.
   */
  delete(data: any):void{
    if (confirm("Are you sure to delete ?")) {
      if(data){
        this.moduleservice.deleteFunction(data.id).subscribe({
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
            const error = JSON.parse(err.error);
            this._snakebar.open(error.message, '', {
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
   * Navigates to parameter list page.
   */
  createParameter(data:any):void{
    localStorage.setItem('function', JSON.stringify(data));
    this.router.navigate(['/configure/parameter-list']);
  }
  /**
   * Navigates back to the previous page.
   */
  goBack() :void{
    this.router.navigate(["/configure/modules-list"]);
  }

}
