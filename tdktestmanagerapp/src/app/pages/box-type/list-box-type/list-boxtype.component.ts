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
import { Component, OnInit } from '@angular/core';
import { FooterComponent } from '../../../layout/footer/footer.component';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  GridApi,
  GridReadyEvent,
  IMultiFilterParams,
} from 'ag-grid-community';
import { Router } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ButtonComponent } from '../../../utility/component/ag-grid-buttons/button/button.component';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { AuthService } from '../../../auth/auth.service';
import { BoxtypeService } from '../../../services/boxtype.service';
import { MatSnackBar } from '@angular/material/snack-bar';
@Component({
  selector: 'app-list-boxtype',
  standalone: true,
  imports: [FooterComponent, RouterLink, CommonModule, ReactiveFormsModule, AgGridAngular, HttpClientModule],
  templateUrl: './list-boxtype.component.html',
  styleUrl: './list-boxtype.component.css'
})

/**
 * Component for listing box types.
 */
export class ListBoxtypeComponent implements OnInit {

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
  showUpdateButton = false; // or true, depending on when you want to show the button
  /**
   * The column definitions for the grid.
   */
  public columnDefs: ColDef[] = [
    {
      headerName: 'BoxType Name',
      field: 'boxTypeName',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Type',
      field: 'type',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      cellRenderer: ButtonComponent,
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
  configureName!: string;

  constructor(private http: HttpClient, private router: Router,
    private authservice: AuthService, private service: BoxtypeService, private _snakebar: MatSnackBar) { }


  /**
   * Initializes the component.
   */
  ngOnInit(): void {
    this.service.getfindallbycategory(this.authservice.selectedConfigVal).subscribe(res => {
      this.rowData = JSON.parse(res);
    })
    this.configureName = this.authservice.selectedConfigVal;
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
    this.router.navigate(['configure/edit-boxtype']);
  }

  /**
   * Delete the data.
   * @param data The data to delete.
   */
  delete(data: any) :void{
    if (data) {
      if (confirm("Are you sure to delete ?")) {
        this.service.deleteBoxType(data.boxTypeId).subscribe({
          next: (res) => {
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
            this.ngOnInit();
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
   * Create a group.
   */  
  createGroup():void {
    this.router.navigate(["configure/create-boxtype"]);
  }

  /**
   * Go back to the previous page.
   */  
  goBack():void {
    this.authservice.selectedConfigVal = 'RDKV';
    this.router.navigate(["/configure"]);
  }

}



