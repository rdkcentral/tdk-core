import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { MaterialModule } from '../../../material/material.module';
import { ActivatedRoute } from '@angular/router';
import { ICellRendererParams } from 'ag-grid-community';

interface customcellRenderparams extends ICellRendererParams{
  selectedRowCount:()=> number;
  lastSelectedNodeId:string;
}

@Component({
  selector: 'app-schedule-button',
  standalone: true,
  imports: [MaterialModule,CommonModule],
  template: `
    <button  class="btn  btn-sm delete-btn"  matTooltip="Delete" (click)="onDeleteClick($event)"><mat-icon class="delete-icon icons extra-icon">delete_forever</mat-icon></button>
  `,  
  styles:[
    `.delete-btn{
        border: none;
        padding: 0px;
        background:none;
    }
    .icons{
      font-size: 1.3rem;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .delete-icon{
      color: #dc3545;
    }
 
    `
  ]
  })
export class ScheduleButtonComponent implements OnInit{
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

    refresh(params: customcellRenderparams): boolean {
      this.selectedRowCount = params.selectedRowCount();
      this.lastSelectedNodeId = params.lastSelectedNodeId;
      this.currentNodeId = params.node.id
      return true;
    }
  

    onDeleteClick($event:any){
      if (this.params.onDeleteClick instanceof Function) {
        this.params.onDeleteClick(this.params.node.data);
      }
      
    }



}
