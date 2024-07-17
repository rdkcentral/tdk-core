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
import { MaterialModule } from '../../../../material/material.module';

interface customcellRenderparams extends ICellRendererParams{
  selectedRowCount:()=> number;
  lastSelectedNodeId:string;
}

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [MaterialModule],
  template: `
    <!-- <button [disabled]="isButtonDisabled()" class="btn btn-primary btn-sm delete-btn" (click)="onEditClick($event)"><mat-icon class="delete-icon">edit</mat-icon></button> -->
    <button  class="btn btn-primary btn-sm delete-btn" (click)="onEditClick($event)" matTooltip="Edit"><mat-icon class="delete-icon">edit</mat-icon></button>
    &nbsp;
    <button  class="btn btn-danger btn-sm delete-btn" (click)="onDeleteClick($event)" matTooltip="Delete"><mat-icon class="delete-icon">delete_forever</mat-icon></button>
    &nbsp;
    <button  class="btn btn-primary btn-sm delete-btn" (click)="onViewClick($event)" matTooltip="View"><mat-icon class="delete-icon">remove_red_eye</mat-icon></button>
  `,  
  styles:[
    `.delete-btn{
        border: none;
        padding: 0px;
    }
    .delete-icon{
      color: white;
      font-size: 1rem;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    `
  ]
})
export class ButtonComponent implements OnInit{
  params:any
  selectedRowCount :number = 0;
  lastSelectedNodeId:string ='';
  currentNodeId: string | undefined;

  agInit(params:customcellRenderparams): void {
    this.params = params;
    this.selectedRowCount = params.selectedRowCount();
    this.lastSelectedNodeId = params.lastSelectedNodeId;
    this.currentNodeId = params.node.id
    
  }
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
}
