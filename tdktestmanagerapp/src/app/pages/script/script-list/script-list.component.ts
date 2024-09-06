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
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  GridApi,
  GridReadyEvent,
  IMultiFilterParams,
  RowSelectedEvent,
  SelectionChangedEvent
} from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { MaterialModule } from '../../../material/material.module';
import { Router } from '@angular/router';
import { AuthService } from '../../../auth/auth.service';
import { ModulesService } from '../../../services/modules.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { ModuleButtonComponent } from '../../../utility/component/modules-buttons/button/button.component';

@Component({
  selector: 'app-script-list',
  standalone: true,
  imports: [CommonModule,AgGridAngular, FormsModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './script-list.component.html',
  styleUrl: './script-list.component.css'
})
export class ScriptListComponent {
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 7;
  public paginationPageSizeSelector: number[] | boolean = [7, 15, 30, 50];
  public tooltipShowDelay = 500;
  public gridApi!: GridApi;
  public columnDefs: ColDef[] = [
    {
      headerName: 'Sl No',
      field: 'slno',
      maxWidth: 80 ,
    },
    {
      headerName: 'Module Name',
      field: 'moduleName',
      filter: 'agTextColumnFilter',
      sort: 'asc',
      width: 280,
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Test Group',
      field: 'testGroup',
   
    },
    {
      headerName: 'Script Count',
      field: 'scriptCount',
    
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      headerClass: 'no-sort',
      cellRenderer: ModuleButtonComponent,
      cellRendererParams: (params: any) => ({
        onDownloadClick:this.downloadEXcel.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };

  categories = ['RDKV', 'RDKB', 'RDKC'];
  selectedCategory: string = 'RDKV';
  headingName: string = 'RDKV';
  lastSelectedNodeId: string | undefined;
  rowData: any = [];
  isRowSelected: any;
  selectedRow: any;
  isCheckboxSelected: boolean = false;
  rowIndex!: number | null;
  selectedRowCount = 0;
  dynamicModuleName!:string;
  dynamicFunctionName!:string;

  constructor(private router: Router, private authservice: AuthService, 
    private _snakebar: MatSnackBar,private moduleservice: ModulesService,
    public dialog:MatDialog
  ) { }

  ngOnInit(): void {
    let functiondata = JSON.parse(localStorage.getItem('function') || '{}');
    this.dynamicModuleName = functiondata.moduleName;
    this.dynamicFunctionName = functiondata.functionName;
    this.authservice.selectedCategory = this.selectedCategory;
    this.rowData =[
      {slno:'1',moduleName:'AAMP',scriptCount:'20' ,testGroup:'OpenSource'}
      ]
    
  }

  /**
   * Event handler for when the grid is ready.
   * @param params The grid ready event parameters.
   */
  onGridReady(params: GridReadyEvent<any>) {
    this.gridApi = params.api;
  }
  downloadEXcel(params:any):void{

  }
  createScripts():void{
    this.router.navigate(['script/create-scripts']);
  }

  onCategoryChange(newValue: string): void {
    this.headingName = newValue;
    this.selectedCategory = newValue;
    localStorage.setItem('scriptCategory', this.selectedCategory);
    if(this.selectedCategory){
      this.authservice.selectedCategory = this.selectedCategory;
    }
    
  }
}
