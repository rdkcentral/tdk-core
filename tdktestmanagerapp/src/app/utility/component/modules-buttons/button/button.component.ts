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
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';

interface customcellRenderparams extends ICellRendererParams{
  selectedRowCount:()=> number;
  lastSelectedNodeId:string;
}

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [MaterialModule, CommonModule],
  template: `
    <!-- <button [disabled]="isButtonDisabled()" class="btn btn-primary btn-sm delete-btn" (click)="onEditClick($event)"><mat-icon class="delete-icon">edit</mat-icon></button> -->
    <button  class="btn btn-primary btn-sm delete-btn" matTooltip="Edit" (click)="onEditClick($event)"><i class="bi bi-pencil extra-icon edit"></i></button>
    &nbsp;
    <button  class="btn btn-danger btn-sm delete-btn" matTooltip="Delete" (click)="onDeleteClick($event)"><mat-icon class="extra-icon">delete_forever</mat-icon></button>
    &nbsp;
    <button  class="btn btn-primary btn-sm delete-btn" matTooltip="View" (click)="onViewClick($event)"><i class="bi bi-eye extra-icon view"></i></button>
    &nbsp;
    <button *ngIf="functionShowHide" class="btn btn-primary btn-sm delete-btn" matTooltip="Create Function" (click)="onFunctionClick($event)"><i class="bi bi-plus extra-icon create"></i></button>
    &nbsp;
    <button *ngIf="paraMeterShowHide" class="btn btn-primary btn-sm delete-btn" matTooltip="Create Parameter" (click)="onParameterClick($event)"><i class="bi bi-plus extra-icon create"></i></button>
    &nbsp;
    <button *ngIf="downloadShowHide" class="btn btn-primary btn-sm delete-btn" matTooltip="Download Module" ><i class="bi bi-download extra-icon download"></i></button>
  `,  
  styles:[
    `.delete-btn{
        border: none;
        padding: 0px;
        margin-right:3px;
        border-radius: 50px;
    }
    .extra-icon{
      color: white;
      font-size: 1rem;
      display: flex;
      justify-content: center;
      align-items: center;
      height:24px;
      width:24px;
    }
    .edit{
      background-color: #00B2DC;
      border-radius: 50px;
    }
    .view{
      background-color: #fdb73b;
      border-radius: 50px;
    }
    .create{
      background-color: #92c849;
      border-radius: 50px;
    }
    .download{
      background-color: #f58233;
      border-radius: 50px;
    }
    `
  ]
})
export class ModuleButtonComponent implements OnInit{
  params:any
  selectedRowCount :number = 0;
  lastSelectedNodeId:string ='';
  currentNodeId: string | undefined;
  functionShowHide = true;
  paraMeterShowHide = false;
  downloadShowHide = false;

  agInit(params:customcellRenderparams): void {
    this.params = params;
    this.selectedRowCount = params.selectedRowCount();
    this.lastSelectedNodeId = params.lastSelectedNodeId;
    this.currentNodeId = params.node.id
    
  }
  constructor(private route: ActivatedRoute) { }

  ngOnInit(): void {
    console.log(this.route.snapshot.url[1].path);
    
    if(this.route.snapshot.url[1].path === 'modules-list'){
        this.functionShowHide = true;
        this.paraMeterShowHide = true;
        this.downloadShowHide = true;
    }else if(this.route.snapshot.url[1].path === 'function-list'){
        this.functionShowHide = false;
        this.paraMeterShowHide = true;
        this.downloadShowHide = true;
    }else{
      this.functionShowHide = false;
      this.paraMeterShowHide = false;
      this.downloadShowHide = true;
    }
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
  onFunctionClick($event:any){  
    if (this.params.onFunctionClick instanceof Function) {
      this.params.onFunctionClick(this.params.node.data);
    }
  }
  onParameterClick($event:any){
    if (this.params.onParameterClick instanceof Function) {
      this.params.onParameterClick(this.params.node.data);
    }
  }
}
