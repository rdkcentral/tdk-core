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
import { ChangeDetectorRef, Component, ElementRef, EventEmitter, HostListener, inject, Output, Renderer2, ViewChild } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { Router } from '@angular/router';
import { AuthService } from '../../../auth/auth.service';
import { ModulesService } from '../../../services/modules.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { AgGridAngular } from 'ag-grid-angular';
import { ColDef,GridApi,GridReadyEvent,IMultiFilterParams } from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { MatTableDataSource } from '@angular/material/table';
import { FlatTreeControl } from '@angular/cdk/tree';
import { MatTreeFlatDataSource, MatTreeFlattener } from '@angular/material/tree';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { ButtonComponent } from '../../../utility/component/ag-grid-buttons/button/button.component';
import { ScriptsService } from '../../../services/scripts.service';

interface Script {
  id: string;
  name: string;
}

interface Module {
  moduleId: string;
  moduleName: string;
  scripts: Script[];
  testGroupName: string;
  expanded?: boolean; 
}
interface SuiteModule {
  id: string;
  name: string;
  scripts: Script[];
  description: string;
  expanded?: boolean; 
}
@Component({
  selector: 'app-script-list',
  standalone: true,
  imports: [CommonModule,AgGridAngular, FormsModule, ReactiveFormsModule, MaterialModule,ScrollingModule
],
  templateUrl: './script-list.component.html',
  styleUrl: './script-list.component.css'
})
export class ScriptListComponent {

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild('filterInput') filterInput!: ElementRef;
  @ViewChild('filterButton') filterButton!: ElementRef;
  @ViewChild('staticBackdrop', {static: false}) staticBackdrop?:ElementRef;
  @ViewChild('testSuiteModal', {static: false}) testSuiteModal?:ElementRef;
  categories = ['Video', 'Broadband', 'Camera'];
  selectedCategory : string = 'RDKV';
  categoryName: string = 'Video';
  uploadScriptForm!:FormGroup;
  uploadtestSuiteForm!:FormGroup;
  uploadFormSubmitted = false;
  xmlFormSubmitted = false;
  uploadFileName! :File;
  xmlFileName!:File;
  viewName: string = 'scripts';
  testsuitTable = false;
  scriptTable = true;
  category: any;
  selectedRowCount = 0;
  rowData: any = [];
  public themeClass: string = "ag-theme-quartz";
  scriptPageSize = 7;
  testsuitePageSize = 7;
  scriptPageSelector: number[] | boolean = [7, 15, 30, 50];
  testSuitePageSelector: number[] | boolean = [7, 15, 30, 50];
  public gridApi!: GridApi;
  allPageSize = 7;
  currentPage = 0;
  paginatedSuiteData:SuiteModule[]=[];
  filterText: string = '';
  globalSearchTerm: string = '';
  showFilterInput: boolean = false;
  scriptFilteredData: Module[] = [];
  testSuiteFilteredData:SuiteModule[]=[];
  scriptDataArr : Module[] = [];
  testSuiteDataArr:SuiteModule[] = [];
  panelOpenState = false;
  suitePanelOpen = false;
  sortOrder: 'asc' | 'desc' = 'asc';
  gridColumnApi: any;
  noScriptFound!:string;
  scriptDetails:any;
  @Output() dataEvent = new EventEmitter<any>();
  public columnDefs: ColDef[] = [
    {
      headerName: 'Sl. No.',
      valueGetter: (params) => params.node?.childIndex ? params.node?.childIndex + 1 : '1',
      width: 150,
      pinned: 'left'
    },
    {
      headerName: 'Script Name',
      field: 'name',
      filter: 'agTextColumnFilter',
      width:455,
      sortable: true
    },

    {
      headerName: 'Action',
      field: '',
      sortable: false,
      width:330,
      headerClass: 'no-sort',
      cellRenderer: ButtonComponent,
      cellRendererParams: (params: any) => ({
        onEditClick: this.editScript.bind(this),
        onDeleteClick: this.deleteScript.bind(this),
        onViewClick: this.openModal.bind(this),
        // onDownloadClick: this.downloadXML.bind(this),
        onDownloadZip: this.downloadScriptZip.bind(this),
        selectedRowCount: () => this.selectedRowCount,
      })
    }
  ];
  public testSutiteColumn: ColDef[] = [
    {
      headerName: 'Sl. No.',
      valueGetter: (params) => params.node?.childIndex ? params.node?.childIndex + 1 : '1',
      flex: 1,
      pinned: 'left'
    },
    {
      headerName: 'Script Name',
      field: 'name',
      filter: 'agTextColumnFilter',
      flex: 1,
      sortable: true
    }

    // {
    //   headerName: 'Action',
    //   field: '',
    //   sortable: false,
    //   headerClass: 'no-sort',
    //   cellRenderer: ButtonComponent,
    //   cellRendererParams: (params: any) => ({
    //     onEditClick: this.editTestSuite.bind(this),
    //     onDeleteClick: this.deleteTestSuite.bind(this),
    //     onViewClick: this.openModal.bind(this),
    //     onDownloadClick: this.downloadXML.bind(this),
    //     onDownloadScriptClick: this.downloadScript.bind(this),
    //     selectedRowCount: () => this.selectedRowCount,
    //   })
    // }
  ];
  gridOptions = {
    // domLayout: 'autoHeight' 
    rowHeight: 30
  };

  constructor(private router: Router, private authservice: AuthService,
    private _snakebar: MatSnackBar, public dialog: MatDialog, private cdRef: ChangeDetectorRef, 
    private scriptservice: ScriptsService, private renderer: Renderer2) { }

  ngOnInit(): void {
    this.selectedCategory = this.authservice.selectedConfigVal;
    localStorage.setItem('category', this.selectedCategory);
    this.findallScriptsByCategory(this.selectedCategory);
    this.scriptSorting();
    this.uploadScriptForm = new FormGroup({
      uploadZip: new FormControl<string | null>('', { validators: Validators.required }),
    })
    this.uploadtestSuiteForm = new FormGroup({
      uploadXML: new FormControl<string | null>('', { validators: Validators.required }),
    }) 
  }

  onGridReady(params:GridReadyEvent<any>) {
    this.gridApi = params.api;
    // this.gridColumnApi = params.columnApi;
  }
  findallScriptsByCategory(category:any){
    this.scriptservice.getallbymodules(category).subscribe({
      next:(res)=>{
        this.scriptDataArr = JSON.parse(res);
        this.scriptFilteredData = this.scriptDataArr;
      },
      error:(err)=>{
        let errmsg = err.error;
        this.noScriptFound = errmsg;
      }

    })
  }
 
  categoryChange(val: string): void {
    this.scriptDataArr=[];
    this.scriptFilteredData =[];
    if (val === 'RDKB') {
      this.categoryName = 'Broadband';
      this.selectedCategory = 'RDKB';
      this.findallScriptsByCategory(this.selectedCategory);
      localStorage.setItem('category', this.selectedCategory);
    } else if (val === 'RDKC') {
      this.categoryName = 'Camera';
      this.selectedCategory = 'RDKC';
      this.findallScriptsByCategory(this.selectedCategory);
      localStorage.setItem('category', this.selectedCategory);
    } else {
      this.selectedCategory = 'RDKV';
      this.categoryName = 'Video';
      this.findallScriptsByCategory(this.selectedCategory);
      localStorage.setItem('category', this.selectedCategory);
    }
    if (this.selectedCategory) {
      this.authservice.selectedCategory = this.selectedCategory;
    }

  }


  viewChange(name: string): void {
    this.viewName = name;
    localStorage.setItem('viewName',this.viewName);
    if (name === 'testsuites') {
      this.testsuitTable = true;
      this.scriptTable = false;
      this.allTestSuilteListByCategory();
    } else {
      this.testsuitTable = false;
      this.scriptTable = true;
    }
  }
  allTestSuilteListByCategory(){
    this.scriptservice.getAllTestSuite(this.selectedCategory).subscribe({
      next:(res)=>{
        this.testSuiteDataArr = JSON.parse(res);
        this.applyFilterSuite();
        this.toggleSortSuite();
      },
      error:(err)=>{
        let errmsg = JSON.parse(err.error);
        this.noScriptFound = errmsg.message;
      }
    })
  }
  ngAfterViewInit() {
    // setTimeout(() => {
    //   if (this.paginator) {
    //     this.paginator.page.subscribe(() => this.paginateParentData());
    //     this.applyFilter();
    //     this.toggleSortOrder();
    //   }
    // });
    // setTimeout(() => {
    //   if (this.paginator) {
    //     this.paginator.page.subscribe(() => this.paginateSuiteData());
    //     this.applyFilterSuite();
    //     this.toggleSortSuite();
    //   }
    // });
  }

 
  paginateSuiteData() {
    if (!this.paginator) {
      return;
    }
    const start = this.paginator.pageIndex * this.paginator.pageSize;
    const end = start + this.paginator.pageSize;
    this.paginatedSuiteData = this.testSuiteFilteredData.slice(start, end);
    console.log(this.paginatedSuiteData);
    
    this.cdRef.detectChanges();
  }
  onPageChange(event: any): void {
    this.currentPage = event.pageIndex;
    // this.scriptData();
    this.paginateSuiteData();
  }
  scriptSorting(){
    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    this.scriptFilteredData.sort((a, b) => {
      if (this.sortOrder === 'asc') {
        return a.moduleName.localeCompare(b.moduleName); 
      } else {
        return b.moduleName.localeCompare(a.moduleName);
      }
    });
  }
  toggleSortSuite(){
    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    this.testSuiteFilteredData.sort((a, b) => {
      if (this.sortOrder === 'asc') {
        return a.name.localeCompare(b.name); 
      } else {
        return b.name.localeCompare(a.name);
      }
    });
    this.paginateSuiteData();
  }
  toggleFilterInput() {
    this.showFilterInput = !this.showFilterInput;
    if (!this.showFilterInput) {
      this.filterText = '';
      this.filterScript();
      this.scriptSorting();
    }
  }
  filterScript(){
    if (this.filterText) {
      this.scriptFilteredData = this.scriptDataArr.filter((parent: any) =>
        parent.moduleName.toLowerCase().includes(this.filterText.toLowerCase())
      );
    } else {
      this.scriptFilteredData = [...this.scriptDataArr];
      this.scriptSorting();
    }
    this.paginator.firstPage();
  }
  applyFilterSuite() {
    if (this.filterText) {
      this.testSuiteFilteredData = this.testSuiteDataArr.filter((parent: any) =>
        parent.name.toLowerCase().includes(this.filterText.toLowerCase())
      );
    } else {
      this.testSuiteFilteredData = [...this.testSuiteDataArr];
      this.toggleSortSuite();
    }
    this.paginator.firstPage();
    this.paginateSuiteData(); 
  }
  
  globalSearch() {
      const searchTerm = this.globalSearchTerm.toLowerCase();
      if(searchTerm){
        this.scriptFilteredData = this.scriptDataArr.map((module:Module) => {
          const filteredScripts = module.scripts.filter((script) =>
            script.name.toLowerCase().includes(searchTerm)
          );
          return {
            ...module,
            scripts: filteredScripts, 
            expanded: filteredScripts.length > 0,
          };
        });
        this.scriptFilteredData = this.scriptFilteredData.filter(
          (module) => module.scripts.length > 0
        );
      }else{
        this.scriptFilteredData= [...this.scriptDataArr];
      }

    }

  uploadScriptSubmit(){
    this.uploadFormSubmitted = true;
    if(this.uploadScriptForm.invalid){
      return
     }else{
      if(this.uploadFileName){
        this.scriptservice.uploadZipFile(this.uploadFileName).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
              this.close();
              this.ngOnInit();
          },
          error:(err)=>{
            let errmsg = err.error;
            this._snakebar.open(errmsg, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
            })
            this.ngOnInit();
            this.close();
            this.uploadScriptForm.reset();
          }
        })
      }
     }
  }

  /**
   * Closes the modal  by click on button .
   */
  close(){
    (this.staticBackdrop?.nativeElement as HTMLElement).style.display = 'none';
    this.renderer.removeStyle(document.body, 'overflow');
    this.renderer.removeStyle(document.body, 'padding-right');
  }

  closeSuiteModal(){
    (this.testSuiteModal?.nativeElement as HTMLElement).style.display = 'none';
    this.renderer.removeStyle(document.body, 'overflow');
    this.renderer.removeStyle(document.body, 'padding-right');
  }
  /**
   * Handles the file change event when a file is selected for upload.
   * @param event - The file change event object.
   */
  onFileChange(event:any){
    this.uploadFileName = event.target.files[0].name;
    const file: File = event.target.files[0];
    if (file && file.name.endsWith('.zip')) {
      this.uploadFileName = file;
    } else {
      alert('Please select a valid ZIP file.');
    }
       
  }
  testSuiteXMLFile(event:any){
    this.xmlFileName = event.target.files[0].name;
    const file: File = event.target.files[0];
    if (file && file.type === 'text/xml') {
      this.xmlFileName = file;
    } else {
      alert('Please select a valid XML file.');
    }
  }
  testSuiteFileSubmit(){
    this.xmlFormSubmitted = true;
    if(this.uploadtestSuiteForm.invalid){
      return
     }else{
      if(this.xmlFileName){
        this.scriptservice.uploadTestSuiteXML(this.xmlFileName).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
              this.uploadtestSuiteForm.reset();
              this.closeSuiteModal();
              this.allTestSuilteListByCategory();
          },
          error:(err)=>{
            let errmsg = err.error;
            this._snakebar.open(errmsg, '', {
            duration: 2000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
            })
            this.ngOnInit();
            this.close();
            this.uploadtestSuiteForm.reset();
          }
        })
      }
     }
  }

  createScripts(): void {
    this.router.navigate(['script/create-scripts']);
  }

  createScriptGroup(): void {
    this.router.navigate(['script/create-script-group']);
  }
  customTestSuite(){
    this.router.navigate(['script/custom-testsuite']);
  }
  editScript(editData: any): void {
    console.log(editData.id);
    
    this.scriptservice.scriptFindbyId(editData.id).subscribe(res=>{
      this.scriptDetails = JSON.parse(res);
      localStorage.setItem('scriptDetails', JSON.stringify(this.scriptDetails));
      console.log(this.scriptDetails);
      this.router.navigate(['script/edit-scripts']);
    })
  }
  deleteScript(data:any) {
    if (confirm("Are you sure to delete ?")) {
      if(data){
        this.scriptservice.delete(data.id).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
              })
              this.findallScriptsByCategory(this.selectedCategory);
          },
          error:(err)=>{
            this._snakebar.open(err.error, '', {
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

  downloadScriptZip(downloadData:any){
    this.scriptservice.downloadSriptZip(downloadData.name).subscribe(blob=>{
        const xmlBlob = new Blob([blob], { type: 'application/zip' });
        const url = window.URL.createObjectURL(xmlBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${downloadData.name}.zip`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      })
  }
  openModal() {

  }
  downloadXML(params: any): void {
    if (params.moduleName) {
      this.scriptservice.downloadTestcases(params.moduleName).subscribe(blob => {
        const xmlBlob = new Blob([blob], { type: 'application/xml' }); // Ensure correct MIME type
        const url = window.URL.createObjectURL(xmlBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${params.moduleName}.xlsx`;
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });
    }
  }

  downloadScript(params:any):void{
    if(params.name){
      this.scriptservice.downloadScript(params.name).subscribe(blob => {
        const xmlBlob = new Blob([blob], { type: 'application/zip' }); // Ensure correct MIME type
        const url = window.URL.createObjectURL(xmlBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${params.name}.zip`;
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });
    }
  }

  downloadTestCases(){
    this.category =  this.authservice.selectedConfigVal;
    console.log("Testcase:", this.category);
    this.scriptservice.downloadTestCasesZip( this.category).subscribe(blob => {
      const xmlBlob = new Blob([blob], { type: 'application/zip' }); 
      const url = window.URL.createObjectURL(xmlBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Testcase_${ this.category}.zip`;
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    });

  }
  downloadAllSuitesZIP(){
    this.scriptservice.downloadalltestsuitexmlZip(this.selectedCategory).subscribe(blob => {
      const xmlBlob = new Blob([blob], { type: 'application/zip' }); 
      const url = window.URL.createObjectURL(xmlBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Testcase_${this.selectedCategory}.zip`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    });
  }

  downloadSuiteXML(params:any){
    if(params.name){
      this.scriptservice.downloadTestSuiteXML(params.name).subscribe(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${params.name}.xml`; 
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });
    }
  }
  downloadSuiteExcel(params:any){
    if(params.name){
      this.scriptservice.downloadTestSuiteXLSX(params.name).subscribe(blob => {
        const xmlBlob = new Blob([blob], { type: 'application/xml' }); 
        const url = window.URL.createObjectURL(xmlBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${params.name}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });
    }
  }
  deleteSuite(params:any){
    if (confirm("Are you sure to delete ?")) {
      if(params.id){
        this.scriptservice.deleteTestSuite(params.id).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
              })
              this.allTestSuilteListByCategory();
          },
          error:(err)=>{
            this._snakebar.open(err.error, '', {
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
  editTestSuite(testSuiteData:any){
    // this.dataEvent.emit(testSuiteData);
    this.router.navigate(['script/edit-testsuite'], {state:{testSuiteData}});
  }
  // downloadChildData(parent: any) {
  //   const csvRows = [];
  //   const headers = Object.keys(parent.childData[0]);
  //   csvRows.push(headers.join(','));

  //   for (const row of parent.childData) {
  //     csvRows.push(headers.map(header => row[header]).join(','));
  //   }

  //   const csvData = csvRows.join('\n');
  //   const blob = new Blob([csvData], { type: 'text/csv' });
  //   const url = window.URL.createObjectURL(blob);
  //   const a = document.createElement('a');
  //   a.href = url;
  //   a.download = `${parent.title}.csv`;
  //   a.click();
  //   window.URL.revokeObjectURL(url);
  // }

  @HostListener('document:click', ['$event'])
  onClickOutside(event: Event) {
    if (
      this.showFilterInput &&
      this.filterInput &&
      !this.filterInput.nativeElement.contains(event.target) &&
      this.filterButton &&
      !this.filterButton.nativeElement.contains(event.target)
    ) {
      this.showFilterInput = false;
    }
  }
  togglePanel(parent: any) {
    parent.expanded = !parent.expanded;
    this.panelOpenState = !this.panelOpenState;
  }
  toggleTestSuite(suite:any){
    suite.expanded = !suite.expanded;
    this.suitePanelOpen = !this.suitePanelOpen;
  }


}
