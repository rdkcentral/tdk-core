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
import { Component } from '@angular/core';
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
  RowSelectedEvent,
  SelectionChangedEvent
} from 'ag-grid-community';
import { Router } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ButtonComponent } from '../../../utility/component/ag-grid-buttons/button/button.component';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { AuthService } from '../../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { RdkVersionsService } from '../../../services/rdk-versions.service';

/**
 * Represents the ListRdkVersionsComponent class.
 */
@Component({
  selector: 'app-list-rdk-versions',
  standalone: true,
  imports: [FooterComponent, RouterLink, CommonModule, ReactiveFormsModule, AgGridAngular, HttpClientModule],
  templateUrl: './list-rdk-versions.component.html',
  styleUrl: './list-rdk-versions.component.css'
})
export class ListRdkVersionsComponent {

  selectedConfig!: string | null;
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
  public columnDefs: ColDef[] = [
    {
      headerName: 'Name',
      field: 'buildVersionName',
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

  constructor(private router: Router, private authservice: AuthService,
    private service: RdkVersionsService, private _snakebar: MatSnackBar
  ) { }

  /**
   * Initializes the component.
  */
  ngOnInit(): void {
    this.service.getRdkVersionByList(this.authservice.selectedConfigVal).subscribe(res => {
      this.rowData = JSON.parse(res);
    })
    this.configureName = this.authservice.selectedConfigVal;
    this.authservice.currentRoute = this.router.url.split('?')[0];
  }

  /**
   * Event handler for when the grid is ready.
   * @param params The grid ready event parameters.
   */
  onGridReady(params: GridReadyEvent<any>) {
    this.gridApi = params.api;
  }
  /**
   * Deletes a record.
   * @param data The data of the record to delete.
   */
  delete(data: any) {
    if (confirm("Are you sure to delete ?")) {
      this.service.deleteRdkVersion(data.rdkVersionId).subscribe({
        next: (res) => {
          this.rowData = this.rowData.filter((row: any) => row.rdkVersionId !== data.rdkVersionId);
          this.rowData = [...this.rowData];
          this._snakebar.open(res, '', {
            duration: 1000,
            panelClass: ['success-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        },
        error: (err) => {
          this._snakebar.open(err, 'Something went wrong', {
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
   * Edits a user.
   * @param user The user to edit.
   * @returns The edited user.
   */
  userEdit(user: any): any {
    localStorage.setItem('user', JSON.stringify(user))
    this.service.currentUrl = user.userGroupId;
    this.router.navigate(['configure/edit-rdkversions']);
  }

  /**
   * Creates a new box manufacturer.
   */
  createRdkVersions() {
    this.router.navigate(['/configure/create-rdkversions']);
  }
  
  /**
   * Navigates back to the previous page.
   */
  goBack() {
    this.authservice.selectedConfigVal = 'RDKV';
    this.router.navigate(["/configure"]);
  }


}
