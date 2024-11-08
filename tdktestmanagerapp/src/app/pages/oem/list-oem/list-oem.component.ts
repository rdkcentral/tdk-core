import { Component } from '@angular/core';
import { OemService } from '../../../services/oem.service';
import { Router, RouterLink } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { GridApi, ColDef, IMultiFilterParams, GridReadyEvent, RowSelectedEvent, SelectionChangedEvent } from 'ag-grid-community';
import { AuthService } from '../../../auth/auth.service';
import { ButtonComponent } from '../../../utility/component/ag-grid-buttons/button/button.component';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { AgGridAngular } from 'ag-grid-angular';
import { FooterComponent } from '../../../layout/footer/footer.component';
import { MaterialModule } from '../../../material/material.module';

@Component({
  selector: 'app-list-oem',
  standalone: true,
  imports: [FooterComponent, RouterLink,MaterialModule, CommonModule, ReactiveFormsModule, AgGridAngular, HttpClientModule],
  templateUrl: './list-oem.component.html',
  styleUrl: './list-oem.component.css'
})
export class ListOemComponent {

  selectedConfig!: string | null;
  lastSelectedNodeId: string | undefined;
  rowData: any = [];
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
  categoryName!: string;
  configureName!: string;
  public columnDefs: ColDef[] = [
    {
      headerName: 'Name',
      field: 'oemName',
      filter: 'agTextColumnFilter',
      flex: 1,
      sort: 'asc',
      filterParams: {
      } as IMultiFilterParams,
    },
    {
      headerName: 'Action',
      field: '',
      sortable: false,
      cellRenderer: ButtonComponent,
      headerClass: 'no-sort',
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
  

  constructor(private router: Router, private authservice: AuthService,
    private service: OemService, private _snakebar: MatSnackBar
  ) { }

  /**
   * Initializes the component.
  */
  ngOnInit(): void {
    this.service.getOemByList(this.authservice.selectedConfigVal).subscribe(res => {
      this.rowData = JSON.parse(res);
    })
    this.configureName = this.authservice.selectedConfigVal;
    this.categoryName = this.authservice.showSelectedCategory;
    this.authservice.currentRoute = this.router.url.split('?')[0];
  }

  /**
   * Event handler for when the grid is ready.
   * @param params The grid ready event parameters.
   */
  onGridReady(params: GridReadyEvent<any>) {
    this.gridApi = params.api;
  }
  /**
   * Deletes a record.
   * @param data The data of the record to delete.
   */
  delete(data: any) {
    if (confirm("Are you sure to delete ?")) {
      this.service.deleteOem(data.oemId).subscribe({
        next: (res) => {
          this.rowData = this.rowData.filter((row: any) => row.oemId !== data.oemId);
          this.rowData = [...this.rowData];
          this._snakebar.open(res, '', {
            duration: 1000,
            panelClass: ['success-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        },
        error: (err) => {
          const error = JSON.parse(err.error);
          this._snakebar.open(error.message, '', {
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
   * Event handler for when a row is selected.
   * @param event The row selected event.
   */
  onRowSelected(event: RowSelectedEvent) {
    this.isRowSelected = event.node.isSelected();
    this.rowIndex = event.rowIndex
  }

  /**
   * Event handler for when the selection is changed.
   * @param event The selection changed event.
   */
  onSelectionChanged(event: SelectionChangedEvent) {
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
   * @returns The edited user.
   */
  userEdit(user: any): any {
    localStorage.setItem('user', JSON.stringify(user))
    this.service.currentUrl = user.userGroupId;
    this.router.navigate(['configure/oem-edit']);
  }

  /**
   * Creates a new oem.
   */
  createOem() {
    this.router.navigate(['/configure/create-oem']);
  }
  
  /**
   * Navigates back to the previous page.
   */
  goBack() {
    this.authservice.selectedConfigVal = 'RDKV';
    this.router.navigate(["/configure"]);
  }

}
