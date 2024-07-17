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
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { AgGridAngular } from 'ag-grid-angular';
import { ColDef, IMultiFilterParams } from 'ag-grid-community';
import { Router } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { MatSnackBar } from '@angular/material/snack-bar';
import { StreamingTemplatesService } from '../../../services/streaming-templates.service';
import { InputComponent } from '../../../utility/component/ag-grid-buttons/input/input.component';

@Component({
  selector: 'app-streamingtemplates-create',
  standalone: true,
  imports: [CommonModule, HttpClientModule, ReactiveFormsModule, MaterialModule, AgGridAngular],
  templateUrl: './streamingtemplates-create.component.html',
  styleUrl: './streamingtemplates-create.component.css'
})
export class StreamingtemplatesCreateComponent {
  public columnDefs: ColDef[] = [
    {
      headerName: 'Stream Id',
      field: 'streamingDetailsId',
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
      headerName: 'Channel Type',
      field: 'channelType',
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
      headerName: 'Audio Type',
      field: 'audioType',
      valueGetter: (params) => params.data.audioType ? params.data.audioType : 'NA',
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
      headerName: 'Video Type',
      field: 'videoType',
      valueGetter: (params) => params.data.videoType ? params.data.videoType : 'NA',
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
      headerName: 'Ocap Id',
      field: 'ocapId',
      cellRenderer: 'inputCellRenderer'
    }
  ];
  public defaultColDef: ColDef = {
    flex: 1,
    menuTabs: ['filterMenuTab'],
  };
  rowData: any = [];
  public themeClass: string = "ag-theme-quartz";
  public paginationPageSize = 5;
  public paginationPageSizeSelector: number[] | boolean = [5, 10, 50, 100];
  public tooltipShowDelay = 500;
  gridApi!: any;
  streamingForm!: FormGroup;
  streamingFormSubmitted = false;
  streamingMapObj!: { streamingId: any; ocapId: any; }[];
  loggedinUser: any={};
  public frameworkComponents: any;
  errElement!: { key: any; };

  constructor(private router: Router, private _snakebar: MatSnackBar,
    private service: StreamingTemplatesService) {
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
    this.frameworkComponents = {
      inputCellRenderer: InputComponent
    }
  }

  /**
   * Initializes the component.
   */
  ngOnInit(): void {

    this.streamingForm = new FormGroup({
      streamingName: new FormControl<string | null>('', { validators: Validators.required })
    })

    this.service.getstreamingdetails().subscribe(res => {
      this.rowData = res
    })

  }

  /**
   * Event handler for when the ag-Grid is ready.
   * @param params - The ag-Grid parameters.
   */  
  onGridReady(params: any):void {
    this.gridApi = params.api;
  }

  /**
   * Event handler for when the streaming form is submitted.
   */  
  onStreamingSubmit() :void{
    this.streamingFormSubmitted = true;
    if (this.streamingForm.invalid) {
      return
    } else {
      const tableData: any[] = [];
      this.gridApi.forEachNode((element: any) => {
        tableData.push(element.data)
        this.streamingMapObj = tableData.map((streamingDetailsId: any, ocapId: any) => ({ streamingId: streamingDetailsId.streamingDetailsId, ocapId: streamingDetailsId.ocapId }));
      })
      let obj = {
        templateName: this.streamingForm.value.streamingName,
        streamingMaps: this.streamingMapObj,
        streamingTemplateUserGroup: this.loggedinUser.userGroupName
      }
      this.service.createStreamingTemplate(obj).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["configure/streamingtemplates-list"]);
          }, 1000);
        },
        error: (err) => {
          let errmsg = JSON.parse(err.error);
          const res = Object.keys(errmsg).map(key => {
            return { key: errmsg[key] }
          });
          for (let i = 0; i < res.length; i++) {
            this.errElement = res[i];
          }
          this._snakebar.open(errmsg.message ? errmsg.message : this.errElement.key, '', {
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
   * Navigates back to the streaming templates list.
   */
  goBack() :void{
    this.router.navigate(["configure/streamingtemplates-list"]);
  }
  
  /**
   * Resets the streaming form.
   */
  reset():void {
    this.streamingForm.reset();
  }



}
