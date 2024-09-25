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
  RowSelectedEvent,
  SelectionChangedEvent
} from 'ag-grid-community';
import { Router } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ButtonComponent } from '../../../utility/component/ag-grid-buttons/button/button.component';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { SocVendorService } from '../../../services/soc-vendor.service';
import { AuthService } from '../../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ExecFileSyncOptionsWithBufferEncoding } from 'child_process';

@Component({
  selector: 'app-list-soc-vendor',
  standalone: true,
  imports: [FooterComponent, RouterLink, CommonModule, ReactiveFormsModule, AgGridAngular, HttpClientModule],
  templateUrl: './list-soc-vendor.component.html',
  styleUrl: './list-soc-vendor.component.css'
})
export class ListSocVendorComponent implements OnInit {

  constructor(private router: Router, private service: SocVendorService,
    private authservice: AuthService, private _snakebar: MatSnackBar) { }

  public rowSelection: 'single' | 'multiple' = 'single';
  lastSelectedNodeId: string | undefined;
  rowData: any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 7;
  public paginationPageSizeSelector: number[] | boolean = [7, 15, 30, 50];
  public tooltipShowDelay = 500;
  isRowSelected: any;
  selectedRow: any;
  configureName!: string;
  isCheckboxSelected: boolean = false;
  public gridApi!: GridApi;
  rowIndex!: number | null;
  selectedRowCount = 0;
  showUpdateButton = false; 
  categoryName!: string;
  public columnDefs: ColDef[] = [
    {
      headerName: 'Name',
      field: 'socVendorName',
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


  /**
   * Initializes the component.
   */
  ngOnInit(): void {
    this.configureName = this.authservice.selectedConfigVal;
    this.categoryName = this.authservice.showSelectedCategory;
    this.authservice.currentRoute = this.router.url.split('?')[0];
    this.service.getSocVendor(this.authservice.selectedConfigVal).subscribe(res => {
      this.rowData = JSON.parse(res);
    })
  }
  /**
   * Event handler for when the grid is ready.
   * @param params The grid ready event parameters.
   */
  onGridReady(params: GridReadyEvent<any>) :void{
    this.gridApi = params.api;
  }

  /**
   * Deletes a SOC vendor.
   * @param data The data of the SOC vendor to delete.
   */  
  delete(data: any):void {
    if (confirm("Are you sure to delete ?")) {
      this.service.deleteSocVendor(data.socVendorId).subscribe({
        next: (res) => {
          this.rowData = this.rowData.filter((row: any) => row.socVendorId !== data.socVendorId);
          this.rowData = [...this.rowData];
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
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
   * Event handler for when a row is selected.
   * @param event The row selected event.
   */  
  onRowSelected(event: RowSelectedEvent) :void{
    this.isRowSelected = event.node.isSelected();
    this.rowIndex = event.rowIndex
  }

  /**
   * Event handler for when the selection is changed.
   * @param event The selection changed event.
   */
  onSelectionChanged(event: SelectionChangedEvent):void {
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
   */
  userEdit(user: any): void {
    localStorage.setItem('user', JSON.stringify(user))
    this.router.navigate(['configure/edit-socvendor']);
  }

  /**
   * Creates a SOC vendor.
   */
  createSocVendor() :void{
    this.router.navigate(["configure/create-socvendor"]);
  }

  /**
   * Navigates back to the previous page.
   */  
  goBack() :void{
    this.authservice.selectedConfigVal = 'rdkv';
    this.router.navigate(["/configure"]);
  }



}

