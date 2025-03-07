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
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  IMultiFilterParams,
  RowSelectedEvent,
  SelectionChangedEvent
} from 'ag-grid-community';

import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../../material/material.module';
import { ButtonComponent } from '../../../utility/component/ag-grid-buttons/button/button.component';
import { Router } from '@angular/router';
import { UserManagementService } from '../../../services/user-management.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [AgGridAngular, HttpClientModule, MaterialModule, CommonModule],
  templateUrl: './user-list.component.html',
  styleUrl: './user-list.component.css'
})
export class UserListComponent implements OnInit {
  public rowSelection: 'single' | 'multiple' = 'single';
  lastSelectedNodeId: string | undefined;
  public columnDefs: ColDef[] = [
    {
      headerName: 'User Name',
      field: 'userName',
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
      headerName: 'Email',
      field: 'userEmail',
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
      headerName: 'Display Name',
      field: 'userDisplayName',
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
      headerName: 'Role',
      field: 'userRoleName',
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
      headerName: 'Action',
      field: '', sortable: false,
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
  gridOptions = {
    rowHeight: 36
  }; 
  rowData: any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 10;
  public paginationPageSizeSelector: number[] | boolean = [10, 15, 30, 50];
  public tooltipShowDelay = 500;
  isRowSelected: any;
  selectedRow: any;
  isCheckboxSelected: boolean = false;
  gridApi!: any;
  rowIndex!: number | null;
  selectedRowCount = 0;

  constructor(private http: HttpClient, private router: Router, private usermanageservice: UserManagementService, private _snakebar: MatSnackBar) { }
  
  /**
   * The method to initialize the component.
   */
  ngOnInit(): void {
    this.usermanageservice.getAlluser().subscribe((data) => (this.rowData = data));
  }

  /**
   * The method to create a user.
   */
  createUser() : void {
    this.router.navigate(["configure/create-user"]);
  }

  /**
   * The method to navigate back to the configure page.
   */
  goBack(): void  {
    this.router.navigate(["/configure"]);
  }

  /**
   * Called when the grid is ready to be used.
   * @param params - The grid parameters.
   */
  onGridReady(params: any): void  {
    this.gridApi = params.api;
  }

  /**
   * Handles the event when a row is selected.
   * @param event The RowSelectedEvent object containing information about the selected row.
   */
  onRowSelected(event: RowSelectedEvent): void  {
    this.isRowSelected = event.node.isSelected();
    this.rowIndex = event.rowIndex
  }

  /**
   * Handles the selection changed event.
   * @param event - The selection changed event object.
   */
  onSelectionChanged(event: SelectionChangedEvent) : void {
    this.selectedRowCount = event.api.getSelectedNodes().length;
    const selectedNodes = event.api.getSelectedNodes();
    this.lastSelectedNodeId = selectedNodes.length > 0 ? selectedNodes[selectedNodes.length - 1].id : '';
    this.selectedRow = this.isRowSelected ? selectedNodes[0].data : null;
    if (this.gridApi) {
      this.gridApi.refreshCells({ force: true })
    }
  }

  /**
   * Deletes a user.
   * @param data - The user data to be deleted.
   */
  delete(data: any) : void {
    if (confirm("Are you sure want to delete ? ")) {
      this.usermanageservice.deleteUser(data.userId).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
          this.ngOnInit();
        },
        error: (err) => {
          this._snakebar.open(err, 'Something went wrong', {
            duration: 3000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
      })
    }

  }

  /**
   * Edits the user and navigates to the edit user configuration page.
   * @param user - The user object to be edited.
   * @returns - Returns any value.
   */
  userEdit(user: any): void {
    localStorage.setItem('user', JSON.stringify(user))
    this.router.navigate(['configure/edit-user']);
  }



}
