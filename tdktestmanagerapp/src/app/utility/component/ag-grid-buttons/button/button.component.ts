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
import { ICellRendererParams } from "ag-grid-community";
import { MaterialModule } from '../../../../material/material.module';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';

interface customcellRenderparams extends ICellRendererParams {
  selectedRowCount: () => number;
  lastSelectedNodeId: string;
}

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [MaterialModule, CommonModule],
  template: `
    <!-- <button [disabled]="isButtonDisabled()" class="btn btn-primary btn-sm delete-btn" (click)="onEditClick($event)"><mat-icon class="delete-icon">edit</mat-icon></button> -->
    <button   class="btn  btn-sm delete-btn" (click)="onEditClick($event)" matTooltip="{{textforedit}}"><mat-icon class="extra-icon edit">edit</mat-icon></button>
    &nbsp;
    <button *ngIf="deleteShowHide" class="btn  btn-sm delete-btn" (click)="onDeleteClick($event)" matTooltip="Delete"><mat-icon class="delete-icon extra-icon">delete_forever</mat-icon></button>
   
    <!-- <button *ngIf="viewShowHide"  class="btn  btn-sm delete-btn" (click)="onViewClick($event)" matTooltip="View"><mat-icon class=" view extra-icon">remove_red_eye</mat-icon></button> -->
    &nbsp;
    <button *ngIf="downloadShowHide" class="btn  btn-sm delete-btn" (click)="onDownloadClick($event)" matTooltip="Download XML" ><i class="bi bi-cloud-arrow-down-fill extra-icon download"></i></button>
    &nbsp;
    <button *ngIf="downloadSriptZip" class="btn  btn-sm delete-btn" (click)="onDownloadZip($event)" matTooltip="Download Zip" ><i class="bi bi-cloud-arrow-down-fill extra-icon download"></i></button>
    &nbsp;
    <button *ngIf="downloadScriptMd" class="btn  btn-sm delete-btn" (click)="onDownloadMd($event)" matTooltip="Download MD" ><i class="bi bi-cloud-arrow-down-fill extra-icon download"></i></button>
    &nbsp;
    <button *ngIf="downloadConfigShow" class="btn  btn-sm delete-btn download-config" (click)="onDownloadClick($event)" matTooltip="Download Config File" ><i class="bi bi-cloud-arrow-down-fill extra-icon download"></i></button>

  `,
  styles: [
    `.delete-btn{
        border: none;
        padding: 0px;
        background:none;
    }
    .extra-icon{
      font-size: 1.3rem;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .edit{
      color: #00B2DC;
    }
    .delete-icon{
      color: #808080;
    }
    .view{
      color: #fdb73b;
    }
    .download{
      color: #00B2DC;
    }
    .download-config{
      margin-left: -15px;
    }
    `
  ]
})
export class ButtonComponent implements OnInit {
  params: any
  selectedRowCount: number = 0;
  lastSelectedNodeId: string = '';
  currentNodeId: string | undefined;
  downloadShowHide = false
  viewShowHide = true;
  textforedit!: string;
  downloadSriptZip = false;
  downloadScriptMd = false;
  deleteShowHide = true;
  downloadConfigShow = false;

  agInit(params: customcellRenderparams): void {
    this.params = params;
    this.selectedRowCount = params.selectedRowCount();
    this.lastSelectedNodeId = params.lastSelectedNodeId;
    this.currentNodeId = params.node.id

  }
  constructor(private route: ActivatedRoute) { }

  ngOnInit(): void {
    if (this.route.snapshot.url[0].path === 'devices') {
      this.downloadShowHide = true;
      this.textforedit = 'Edit/View';
    } else {
      this.downloadShowHide = false;
      this.textforedit = 'Edit/View';
    }
    if (this.route.snapshot.url[0].path === 'script') {
      this.downloadSriptZip = true;
      this.downloadScriptMd = true;
    } else {
      this.downloadSriptZip = false;
    }
    if (this.route.snapshot.url[1]) {
      if (this.route.snapshot.url[1].path === 'list-devicetype' ||
        this.route.snapshot.url[1].path === 'list-oem' ||
        this.route.snapshot.url[1].path === 'list-soc' ||
        this.route.snapshot.url[1].path === 'create-group' ||
        this.route.snapshot.url[1].path === 'user-management' ||
        this.route.snapshot.url[1].path === 'list-primitivetest') {
        this.viewShowHide = false;
        this.textforedit = 'Edit/View';
      } else {
        this.viewShowHide = true;
        this.textforedit = 'Edit/View';
      }
      if (this.route.snapshot.url[1].path === 'list-rdk-certifications') {
        this.deleteShowHide = true;
        this.viewShowHide = false;
        this.downloadConfigShow = true;
        this.viewShowHide = false;
      }
    }

  }
  //** Condition for disable edit and delete button to own user */
  isButtonDisabled(): boolean {
    return !(this.selectedRowCount === 1 && this.lastSelectedNodeId === this.currentNodeId);
  }

  refresh(params: customcellRenderparams): boolean {
    this.selectedRowCount = params.selectedRowCount();
    this.lastSelectedNodeId = params.lastSelectedNodeId;
    this.currentNodeId = params.node.id
    return true;
  }

  onEditClick($event: any) {
    if (this.params.onEditClick instanceof Function) {
      this.params.onEditClick(this.params.node.data);
    }
  }
  onDeleteClick($event: any) {
    if (this.params.onDeleteClick instanceof Function) {
      this.params.onDeleteClick(this.params.node.data);
    }

  }
  onViewClick($event: any) {
    if (this.params.onViewClick instanceof Function) {
      this.params.onViewClick(this.params.node.data);
    }
  }
  onDownloadClick($event: any) {
    if (this.params.onDownloadClick instanceof Function) {
      this.params.onDownloadClick(this.params.node.data);
    }
  }
  onDownloadZip($event: any) {
    if (this.params.onDownloadZip instanceof Function) {
      this.params.onDownloadZip(this.params.node.data);
    }
  }

  onDownloadMd(data: any) {
    if (this.params.onDownloadMd) {
      this.params.onDownloadMd(this.params.node.data);
    }
  }


}
