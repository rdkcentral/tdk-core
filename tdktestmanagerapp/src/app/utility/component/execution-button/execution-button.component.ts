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
import {ICellRendererParams} from "ag-grid-community";
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../../material/material.module';

interface customcellRenderparams extends ICellRendererParams{
  selectedRowCount:()=> number;
  lastSelectedNodeId:string;
}

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [MaterialModule,CommonModule],
  template: `
    <button  class="btn  btn-sm delete-btn"  matTooltip="Download Consolidated Report(Excel)" ><i class="bi bi-file-earmark-excel-fill icons report"></i></button>
    &nbsp;
    <button  class="btn  btn-sm delete-btn"  matTooltip="Download Consolidated Report(Zip)" ><i class="bi bi-file-earmark-zip-fill icons zip"></i></button>
    &nbsp;
    <button  class="btn  btn-sm delete-btn" (click)="onViewClick($event)" matTooltip="Execution Result Details" ><i class="bi bi-eye-fill icons details"></i></button>

  `,  
  styles:[
    `.delete-btn{
        border: none;
        padding: 0px;
        background:none;
    }
    .icons{
      font-size: 1rem;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .viewer{
      color: #00B2DC;
    }
    .report{
      color: green;
    }
    .zip{
      color: #f58233;
    }
    .details{
      color: #fdb73b;
    }
    `
  ]
})
export class ExecutionButtonComponent implements OnInit{
  params:any
  selectedRowCount :number = 0;
  lastSelectedNodeId:string ='';
  currentNodeId: string | undefined;
  textforedit!:string;

  agInit(params:customcellRenderparams): void {
    this.params = params;
    this.selectedRowCount = params.selectedRowCount();
    this.lastSelectedNodeId = params.lastSelectedNodeId;
    this.currentNodeId = params.node.id
    
  }
  constructor(private route: ActivatedRoute) { }

  ngOnInit(): void {
    
  }
  //** Condition for disable edit and delete button to own user */
  isButtonDisabled(): boolean {
    return !( this.selectedRowCount === 1 && this.lastSelectedNodeId === this.currentNodeId);
  }

  refresh(params: customcellRenderparams): boolean {
    this.selectedRowCount = params.selectedRowCount();
    this.lastSelectedNodeId = params.lastSelectedNodeId;
    this.currentNodeId = params.node.id
    return true;
  }

  onEditClick($event:any) {
    if (this.params.onEditClick instanceof Function) {
      this.params.onEditClick(this.params.node.data);
    }
  }
  onDeleteClick($event:any){
    if (this.params.onDeleteClick instanceof Function) {
      this.params.onDeleteClick(this.params.node.data);
    }
    
  }
  onViewClick($event:any){
    if (this.params.onViewClick instanceof Function) {
      this.params.onViewClick(this.params.node.data);
    }
  }
  onDownloadClick($event:any){
    if (this.params.onDownloadClick instanceof Function) {
      this.params.onDownloadClick(this.params.node.data);
    }
  }
}
