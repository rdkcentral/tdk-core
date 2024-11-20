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
import { ApplicationRef, ChangeDetectorRef, Component, ElementRef, EventEmitter, HostListener, NgZone, Output, Renderer2, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { Router } from '@angular/router';
import { AuthService } from '../../../auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { AgGridAngular } from 'ag-grid-angular';
import { ColDef,GridApi,GridReadyEvent } from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
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
  @ViewChild('filterInputSuite') filterInputSuite!: ElementRef;
  @ViewChild('filterButton') filterButton!: ElementRef;
  @ViewChild('filterButtonSuite') filterButtonSuite!: ElementRef;
  @ViewChild('staticBackdrop', {static: false}) staticBackdrop?:ElementRef;
  @ViewChild('testSuiteModal', {static: false}) testSuiteModal?:ElementRef;
  categories = ['Video', 'Broadband', 'Camera'];
  selectedCategory : string = 'RDKV';
  categoryName: string = 'Video';
  uploadScriptForm!:FormGroup;
  uploadtestSuiteForm!:FormGroup;
  uploadFormSubmitted = false;
  xmlFormSubmitted = false;
  uploadFileName! :File | null;
  xmlFileName!:File | null;
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
  filterTextSuite: string = '';
  globalSearchTerm: string = '';
  showFilterInput = false;
  showFilterInputsuite = false;
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
  uploadFileError: string | null = null;
  loggedinUser:any;
  preferedCategory!:string;
  userCategory!:string;
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
  ];
  gridOptions = {
    rowHeight: 30
  };

  constructor(private router: Router, private authservice: AuthService,private fb:FormBuilder,
    private _snakebar: MatSnackBar, public dialog: MatDialog, private cdRef: ChangeDetectorRef, 
    private scriptservice: ScriptsService, private renderer: Renderer2,private appRef: ApplicationRef) { 
      this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
      this.userCategory = this.loggedinUser.userCategory;
      this.preferedCategory = localStorage.getItem('preferedCategory')|| '';
    }

  ngOnInit(): void {
    let localcategory = this.preferedCategory?this.preferedCategory:this.userCategory;
    let localViewName = localStorage.getItem('viewName') || '';
    let localcategoryName = localStorage.getItem('categoryname') || '';
    this.selectedCategory = localcategory?localcategory:'RDKV';
    this.viewName = localViewName?localViewName:'scripts';
    this.categoryName = localcategoryName?localcategoryName:'Video';
    if(this.viewName === 'testsuites'){
      this.testsuitTable = true;
      this.scriptTable = false;
      this.allTestSuilteListByCategory();
      this.toggleSortSuite();
    }else{
      this.testsuitTable = false;
      this.scriptTable = true;
      this.findallScriptsByCategory(this.selectedCategory);
      this.scriptSorting();
    }
    this.viewChange(this.viewName);
    this.categoryChange(localcategory);
    this.uploadScriptForm = new FormGroup({
      uploadZip: new FormControl<string | null>('', { validators: Validators.required }),
    })
    this.uploadtestSuiteForm = this.fb.group({
      uploadXML: [null, Validators.required]
    }) 
  }

  onGridReady(params:GridReadyEvent<any>) {
    this.gridApi = params.api;
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
    this.testSuiteDataArr = [];
    this.paginatedSuiteData = [];
    this.viewName = localStorage.getItem('viewName') || '{}';
    if(this.viewName ==='testsuites'){
      if (val === 'RDKB') {
        this.categoryName = 'Broadband';
        this.selectedCategory = 'RDKB';
        this.authservice.selectedCategory = this.selectedCategory;
        this.allTestSuilteListByCategory();
      } else if (val === 'RDKC') {
        this.categoryName = 'Camera';
        this.selectedCategory = 'RDKC';
        this.authservice.selectedCategory = this.selectedCategory;
        this.allTestSuilteListByCategory();
      } else {
        this.selectedCategory = 'RDKV';
        this.categoryName = 'Video';
        this.authservice.selectedCategory = this.selectedCategory;
        this.allTestSuilteListByCategory();
      }
    }
    if(this.viewName ==='scripts'){
      if (val === 'RDKB') {
        this.categoryName = 'Broadband';
        this.selectedCategory = 'RDKB';
        this.findallScriptsByCategory(this.selectedCategory);
      } else if (val === 'RDKC') {
        this.categoryName = 'Camera';
        this.selectedCategory = 'RDKC';
        this.findallScriptsByCategory(this.selectedCategory);
      } else {
        this.selectedCategory = 'RDKV';
        this.categoryName = 'Video';
        this.findallScriptsByCategory(this.selectedCategory);
      }
    }
    localStorage.setItem('category', this.selectedCategory);
    localStorage.setItem('categoryname',this.categoryName);
    this.authservice.videoCategoryOnly = "";
  }


  viewChange(name: string): void {
    this.viewName = name;
    this.globalSearchTerm ='';
    localStorage.setItem('viewName',this.viewName);
    if (name === 'testsuites') {
      this.testsuitTable = true;
      this.scriptTable = false;
      this.allTestSuilteListByCategory();
    } 
    if (name === 'scripts') {
      this.testsuitTable = false;
      this.scriptTable = true;
      this.findallScriptsByCategory(this.selectedCategory);
    }
  }
  allTestSuilteListByCategory(){
    this.scriptservice.getAllTestSuite(this.selectedCategory).subscribe({
      next:(res)=>{
        if(res){
          this.testSuiteDataArr = JSON.parse(res);
          this.cdRef.detectChanges();
          this.applyFilterSuite();
          this.toggleSortSuite();
          
        }else{
          this.cdRef.detectChanges();
          this.testSuiteDataArr =[];
        }

      },
      error:(err)=>{
        let errmsg = JSON.parse(err.error);
        this.noScriptFound = errmsg.message;
      }
    })
  }
  scriptDataPagination(){
    if (!this.paginator) {
      return;
    }
    const start = this.paginator.pageIndex * this.paginator.pageSize;
    const end = start + this.paginator.pageSize;
    this.scriptFilteredData = this.scriptFilteredData.slice(start, end);
    this.cdRef.detectChanges();
  }
 
  paginateSuiteData() {
    if (!this.paginator) {
      return;
    }
    const start = this.paginator.pageIndex * this.paginator.pageSize;
    const end = start + this.paginator.pageSize;
    this.paginatedSuiteData = this.testSuiteFilteredData.slice(start, end);
    this.cdRef.detectChanges();
  }
  onPageChange(event: any): void {
    this.currentPage = event.pageIndex;
    if(this.viewName ==='testsuites'){
      this.paginateSuiteData();
    }else{
      this.scriptDataPagination();
    }
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
    this.scriptDataPagination();
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
  toggleFilterInputSuite(){
    this.showFilterInputsuite = !this.showFilterInputsuite;
    if (!this.showFilterInputsuite) {
      this.filterTextSuite = '';
      this.applyFilterSuite();
      this.toggleSortSuite();
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
    this.scriptDataPagination();
  }
  applyFilterSuite() {
    if (this.filterTextSuite) {
      this.testSuiteFilteredData = this.testSuiteDataArr.filter((parent: any) =>
        parent.name.toLowerCase().includes(this.filterTextSuite.toLowerCase())
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
      if(this.viewName ==='testsuites'){
        if(searchTerm){
          this.paginatedSuiteData = this.testSuiteDataArr.map((suite:SuiteModule)=>{
            const filteredScripts = suite.scripts.filter((script) =>
              script.name.toLowerCase().includes(searchTerm)
            );
            return {
              ...suite,
              scripts: filteredScripts, 
              expanded: filteredScripts.length > 0,
            };
          });
          this.paginatedSuiteData = this.paginatedSuiteData.filter(
            (suite) => suite.scripts.length > 0
          );
        }else{
          this.paginatedSuiteData = [...this.testSuiteDataArr];
          this.paginateSuiteData();
        }

      }else{
        
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
        this.scriptDataPagination();
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
    this.uploadtestSuiteForm.value.uploadXML = '';
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
    if(file){
      if (file.name.endsWith('.zip')) {
        this.uploadScriptForm.patchValue({ file: file });
        this.uploadFileName = file;
        this.uploadFileError = null;
      } else {
        this.uploadScriptForm.patchValue({ file: null });
        this.uploadFileError = 'Please upload a valid zip file.';
      }
    }  
  }
  
  uploadScriptSubmit(){
    this.uploadFormSubmitted = true;
    if(this.uploadScriptForm.invalid){
      return
     }else{
      if(this.uploadFileName){
        this.uploadFileError = null;
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
            let errmsg = JSON.parse(err.error);
            this._snakebar.open(errmsg.message, '', {
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
  testSuiteXMLFile(event:any){
    this.xmlFileName = event.target.files[0].name;
    const file: File = event.target.files[0];
    if(file){
      if (file.type === 'text/xml') {
        this.uploadtestSuiteForm.patchValue({ file: file });
        this.xmlFileName = file;
        this.uploadFileError = null;
      } else {
        this.uploadtestSuiteForm.patchValue({ file: null });
        this.uploadFileError = 'Please upload a valid XML file.';
      }
    }
  }
  testSuiteFileSubmit(){
    this.xmlFormSubmitted = true;
    if(this.uploadtestSuiteForm.invalid){
      return
     }else{
      if(this.xmlFileName){
        this.uploadFileError = null;
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
            let errmsg = JSON.parse(err.error);
            this._snakebar.open(errmsg.message, '', {
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
  createScriptVideo(value:string){
    let onlyVideoCategory = value;
    this.authservice.videoCategoryOnly = onlyVideoCategory;
    this.router.navigate(['script/create-script-group']);
  }
  customTestSuite(){
    this.router.navigate(['script/custom-testsuite']);
  }
  editScript(editData: any): void {
    this.scriptservice.scriptFindbyId(editData.id).subscribe(res=>{
      this.scriptDetails = JSON.parse(res);
      localStorage.setItem('scriptDetails', JSON.stringify(this.scriptDetails));
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
              const rowToRemove = this.paginatedSuiteData.find((row:any) => row.id === params.id);
              if (rowToRemove) {
                this.cdRef.detectChanges();
                this.allTestSuilteListByCategory();
              }
          },
          error:(err)=>{
            let errmsg = JSON.parse(err.error)
            this._snakebar.open(errmsg, '', {
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
    this.router.navigate(['script/edit-testsuite'], {state:{testSuiteData}});
  }
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
