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
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  GridApi,
  GridReadyEvent,
  IMultiFilterParams
} from 'ag-grid-community';
import { Router } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ButtonComponent } from '../../../utility/component/ag-grid-buttons/button/button.component';
import { StreamingTemplatesService } from '../../../services/streaming-templates.service';

@Component({
  selector: 'app-streamingtemplates-list',
  standalone: true,
  imports: [RouterLink, CommonModule, ReactiveFormsModule, AgGridAngular, HttpClientModule],
  templateUrl: './streamingtemplates-list.component.html',
  styleUrl: './streamingtemplates-list.component.css'
})
export class StreamingtemplatesListComponent {

  public columnDefs: ColDef[] = [
    {
      headerName: 'Name',
      field: 'name',
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
      })
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };
  public rowSelection: 'single' | 'multiple' = 'single';
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
  rowData: any = [];

  constructor(private router: Router, private _snakebar: MatSnackBar,
    private service: StreamingTemplatesService) {

  }

  /**
   * Initializes the component.
   */
  ngOnInit(): void {

    this.service.getstreamingtemplateList().subscribe(res => {
      this.rowData = res;
      this.rowData = this.rowData.map((str: any, index: number) => ({ id: index + 1, name: str }));
    })

  }

  /**
   * Navigates back to the configure page.
   */
  goBack():void  {
    this.router.navigate(["/configure"]);
  }

  /**
   * Navigates to the streaming templates create page.
   */
  createStreamingTemplates():void  {
    this.router.navigate(['/configure/streamingtemplates-create']);
  }

  /**
   * Event handler for when the grid is ready.
   * 
   * @param params - The GridReadyEvent object containing the grid API.
   */  
  onGridReady(params: GridReadyEvent<any>):void  {
    this.gridApi = params.api;
  }

  /**
   * Edits the user and navigates to the streaming templates edit page.
   * @param user - The user object to be edited.
   * @returns The edited user object.
   */  
  userEdit(user: any):void  {
    localStorage.setItem('user', JSON.stringify(user))
    this.service.getStreamingtemplateUpdate(user.name).subscribe(res => {
      this.service.allPassedData.next(JSON.parse(res));
    })

    this.router.navigate(['configure/streamingtemplates-edit']);
  }
  
  /**
   * Deletes a streaming template.
   * @param data - The data of the streaming template to be deleted.
   */
  delete(data: any):void {
    if (confirm("Are you sure to delete ?")) {
      this.service.deleteStreamingTemplate(data.name).subscribe({
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
