import { Component } from '@angular/core';
import { IHeaderParams } from 'ag-grid-community';
import { MaterialModule } from '../../../../material/material.module';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-execution-checkbox',
  standalone: true,
  imports: [MaterialModule,CommonModule],
  template: `
      <div class="header-container">
      <button class="btn btn-sm delete-btn" (click)="onDelete()"><mat-icon class="delete-icon">delete_forever</mat-icon></button>
    </div>
  
  `,
  styles: [`
      .header-container {
        display: flex;
        align-items: center;
        gap: 5px;
      }
      .delete-btn{
        border:none;
        padding:0;
      }
      .delete-icon{
        background-color: transparent;
        color: #dc3545;
        font-size: 1rem;
        display: flex;
        margin-top: 5px;
      }

    `]
})
export class ExecutionCheckboxComponent {
  params:any
  isAllSelected = false;

  agInit(params: IHeaderParams & { label: string }): void {
    this.params = params;
  }

  onSelectAll(event: Event) {
    this.isAllSelected = (event.target as HTMLInputElement).checked;
    this.params.api.forEachNode((node:any) => (node.setSelected(this.isAllSelected)));
  }

  onDelete() {
    if (this.params.deleteCallback) {
      this.params.deleteCallback();
    }
  }

  refresh(): boolean {
    return false;
  }

}
