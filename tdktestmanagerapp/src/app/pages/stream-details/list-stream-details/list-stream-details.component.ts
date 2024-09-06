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
import { StreamingDetailsService } from '../../../services/streaming-details.service';
import { AuthService } from '../../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-list-stream-details',
  standalone: true,
  imports: [FooterComponent, RouterLink, CommonModule, ReactiveFormsModule, AgGridAngular, HttpClientModule],
  templateUrl: './list-stream-details.component.html',
  styleUrls: ['./list-stream-details.component.css']
})
export class ListStreamDetailsComponent implements OnInit {

  constructor(
    private router: Router,
    private streamingservice: StreamingDetailsService,
    private authService: AuthService,
    private _snakebar: MatSnackBar
  ) { }

  public rowSelection: 'single' | 'multiple' = 'single';
  lastSelectedNodeId: string | undefined;
  rowData: any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 5;
  public paginationPageSizeSelector: number[] | boolean = [5, 10, 50, 100];
  public tooltipShowDelay = 500;
  isRowSelected: any;
  selectedRow: any;
  configureName!: string;
  isCheckboxSelected: boolean = false;
  public gridApi!: GridApi;
  rowIndex!: number | null;
  selectedRowCount = 0;
  showUpdateButton = false;
  radioDataArr: any;
  videoDataArr: any;
  public columnDefs: ColDef[] = [
    {
      headerName: 'Stream Id',
      field: 'streamingDetailsId',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {} as IMultiFilterParams,
    },
    {
      headerName: 'Channel Type',
      field: 'channelType',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {} as IMultiFilterParams,
    },
    {
      headerName: 'Audio Format',
      field: 'audioType',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {} as IMultiFilterParams,
    },
    {
      headerName: 'Video Format',
      field: 'videoType',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {} as IMultiFilterParams,
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

  public radioColumnDefs: ColDef[] = [
    {
      headerName: 'Stream Id',
      field: 'streamingDetailsId',
      filter: 'agTextColumnFilter',
      flex: 1,
      filterParams: {} as IMultiFilterParams,
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      cellRenderer: ButtonComponent,
      cellRendererParams: (params: any) => ({
        onEditClick: this.userEditRadio.bind(this),
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
   * Initializes the component and retrieves the stream details.
   */
  ngOnInit(): void {
    this.configureName = this.authService.selectedConfigVal;
    this.streamingservice.getStreamDetails().subscribe(res => {
      this.rowData = JSON.parse(res);
      let radioArr = this.rowData.filter((val: any) => val.streamType == "RADIO");
      this.radioDataArr = radioArr
      let videoArr = this.rowData.filter((val: any) => val.streamType == "VIDEO");
      this.videoDataArr = videoArr
    });
  }

  /**
   * Event handler for when the grid is ready.
   * 
   * @param params - The GridReadyEvent containing the grid API.
   */
  onGridReady(params: GridReadyEvent<any>):void {
    this.gridApi = params.api;
  }

  /**
   * Deletes the specified data.
   * @param data - The data to be deleted.
   */
  delete(data: any) :void{
    if (confirm("Are you sure to delete ?")) {
      this.streamingservice.deleteStreamingDetails(data.streamId).subscribe({
        next: (res) => { 
          this.radioDataArr = this.radioDataArr.filter((row: any) => row.streamId !== data.streamId);
          this.radioDataArr = [...this.radioDataArr];
          this.videoDataArr = this.videoDataArr.filter((row: any) => row.streamId !== data.streamId);
          this.videoDataArr = [...this.videoDataArr];
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
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

  /**
   * Handles the event when a row is selected.
   * @param event The RowSelectedEvent object containing information about the selected row.
   */
  onRowSelected(event: RowSelectedEvent) :void{
    this.isRowSelected = event.node.isSelected();
    this.rowIndex = event.rowIndex;
  }

  /**
   * Handles the selection changed event.
   * @param event The selection changed event object.
   */
  onSelectionChanged(event: SelectionChangedEvent) :void{
    this.selectedRowCount = event.api.getSelectedNodes().length;
    const selectedNodes = event.api.getSelectedNodes();
    this.lastSelectedNodeId = selectedNodes.length > 0 ? selectedNodes[selectedNodes.length - 1].id : '';
    this.selectedRow = this.isRowSelected ? selectedNodes[0].data : null;
    if (this.gridApi) {
      this.gridApi.refreshCells({ force: true });
    }
  }

  /**
   * Edits the user details and navigates to the edit stream details page.
   * @param user - The user object to be edited.
   * @returns The edited user object.
   */
  userEdit(user: any): void {
    localStorage.setItem('user', JSON.stringify(user));
    this.router.navigate(['cofigure/edit-streamdetails']);
  }

  /**
   * Sets the selected user in the local storage and navigates to the edit radio stream details page.
   * 
   * @param user - The user object to be stored in the local storage.
   * @returns - Returns any value.
   */
  userEditRadio(user: any): void {
    localStorage.setItem('user', JSON.stringify(user));
    this.router.navigate(['configure/edit-radiostreamdetails']);
  }

  /**
   * Navigates to the "create-streamdetails" route for configuring streaming details.
   */
  createStreamingDetails() :void{
    this.router.navigate(["configure/create-streamdetails"]);
  }

  /**
   * Navigates to the "create-radiostreamdetails" route to create radio streaming details.
   */
  createRadioStreamingDetails():void {
    this.router.navigate(["configure/create-radiostreamdetails"]);
  }

  /**
   * Navigates back to the configure page.
   */
  goBack() :void{
    this.router.navigate(["/configure"]);
  }
}
