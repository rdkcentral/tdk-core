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
import { Component, inject, ViewChild } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../../material/material.module';
import { Router } from '@angular/router';
import { AuthService } from '../../../auth/auth.service';
import { ModulesService } from '../../../services/modules.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { FlatTreeControl } from '@angular/cdk/tree';
import { MatTreeFlatDataSource, MatTreeFlattener } from '@angular/material/tree';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { ScrollingModule } from '@angular/cdk/scrolling';

interface TreeNode {
  name: string;
  children?: TreeNode[];
  testgroup:string;
}
interface TreeNodeTestSuite {
  name: string;
  children?: TreeNodeTestSuite[];
}
interface FlatNode {
  expandable: boolean;
  name: string;
  level: number;
  childCount: number;
  testgroup:string;
}
interface FlatNodeTestSuite {
  expandable: boolean;
  name: string;
  level: number;
  childCount: number;
}
@Component({
  selector: 'app-script-list',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, MaterialModule,ScrollingModule
],
  templateUrl: './script-list.component.html',
  styleUrl: './script-list.component.css'
})
export class ScriptListComponent {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  categories = ['Video', 'Broadband', 'Camera'];
  selectedCategory: string = 'Video';
  headingName: string = 'Video';
  dynamicModuleName!:string;
  dynamicFunctionName!:string;
  searchValue: string = '';

  displayedColumns: string[] = ['name', 'testgroup', 'action'];
  treeControl!: FlatTreeControl<FlatNode>;
  treeFlattener!: MatTreeFlattener<TreeNode, FlatNode>;
  dataSource!: MatTreeFlatDataSource<TreeNode, FlatNode>;
  flatNodeDataSource = new MatTableDataSource<FlatNode>();

  TestSuilteColumns: string[] = ['name', 'action'];
  treeControlSuite!: FlatTreeControl<FlatNodeTestSuite>;
  treeFlattenerSuite!: MatTreeFlattener<TreeNodeTestSuite, FlatNodeTestSuite>;
  dataSourceSuite!: MatTreeFlatDataSource<TreeNodeTestSuite, FlatNodeTestSuite>;
  flatNodeDataSourceSuite = new MatTableDataSource<FlatNodeTestSuite>();

  private _liveAnnouncer = inject(LiveAnnouncer);

  viewName!:string;
  testsuitTable = false;
  scriptTable = true;

  pageSize = 5; 
  currentPage = 0; 
  paginatedData: TreeNode[] = []; 
  treeData: TreeNode[] = [
    {
    name: 'Aamp',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 1', testgroup:''},
      { name: 'Script 2' , testgroup:'' },
      { name: 'Script 3' , testgroup:''},
      { name: 'Script 1', testgroup:''},
      { name: 'Script 2' , testgroup:'' },
      { name: 'Script 3' , testgroup:''},
      { name: 'Script 1', testgroup:''},
      { name: 'Script 2' , testgroup:'' },
      { name: 'Script 3' , testgroup:''},
      { name: 'Script 1', testgroup:''},
      { name: 'Script 2' , testgroup:'' },
      { name: 'Script 3' , testgroup:''},
      { name: 'Script 1', testgroup:''},
      { name: 'Script 2' , testgroup:'' },
      { name: 'Script 3' , testgroup:''},
      { name: 'Script 1', testgroup:''},
      { name: 'Script 2' , testgroup:'' },
      { name: 'Script 3' , testgroup:''},
    ],
  },
  {
    name: 'Bluetooth',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 1' , testgroup:''},
      { name: 'Script 2' , testgroup:''}
    ]
  },
  {
    name: 'module 3',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 2' , testgroup:''}
    ]
  },
  {
    name: 'module 4',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 2' , testgroup:''}
    ]
  },
  {
    name: 'module 5',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 1' , testgroup:''},
      { name: 'Script 2' , testgroup:''}
    ]
  },
  {
    name: 'module 6',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 1' , testgroup:''},
      { name: 'Script 2' , testgroup:''}
    ]
  },
  {
    name: 'module 7',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 1' , testgroup:''},
      { name: 'Script 2' , testgroup:''},
      { name: 'Script 3' , testgroup:''},
      { name: 'Script 4' , testgroup:''}
    ]
  },
  {
    name: 'module 8',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 1' , testgroup:''},
      { name: 'Script 2' , testgroup:''},
      { name: 'Script 3' , testgroup:''}
    ]
  },
  {
    name: 'module 9',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 1' , testgroup:''},
      { name: 'Script 2' , testgroup:''}
    ]
  },
  {
    name: 'module 10',
    testgroup:'OpenSource',
    children: [
      { name: 'Script 1' , testgroup:''},
      { name: 'Script 2' , testgroup:''},
      { name: 'Script 3' , testgroup:''},
      { name: 'Script 4' , testgroup:''},
      { name: 'Script 5' , testgroup:''}
    ]
  }
  ];
  paginationData:TreeNodeTestSuite[]=[];
  treeTestSuiteData: TreeNodeTestSuite[] = [
    {
    name: 'AAMP_LD',
    children: [
      { name: 'TestSuite 1'},
      { name: 'TestSuite 2'},
      { name: 'TestSuite 3' },
      { name: 'TestSuite 4'},
      { name: 'TestSuite 5' },
      { name: 'TestSuite 6'},
      { name: 'TestSuite 7'},
      { name: 'TestSuite 8' },
      { name: 'TestSuite 9'},
      { name: 'TestSuite 10'}
     
    ],
  },
  {
    name: 'AAMP',
    children: [
      { name: 'TestSuite 11'},

    ]
  },
  {
    name: 'BASICSUITE_Hybrid-1',
    children: [
      { name: 'TestSuite 12'},
      { name: 'TestSuite 13'}
    ]
  },
  {
    name: 'BASICSUITE_IPClient-3',
    children: [
      { name: 'TestSuite 14'},
      { name: 'TestSuite 15'},
      { name: 'TestSuite 16' }
    ]
  },
  {
    name: 'BASICSUITE_IPClient-4',
    children: [
      { name: 'TestSuite 17'},
      { name: 'TestSuite 18'},
      { name: 'TestSuite 19' },
      { name: 'TestSuite 20'}
    ]
  },
  {
    name: 'bluetooth',
    children: [
      { name: 'TestSuite 21'},
      { name: 'TestSuite 22'},
      { name: 'TestSuite 23' },
      { name: 'TestSuite 24'},
      { name: 'TestSuite 25' }
    ]
  },
  {
    name: 'bluetoothhal',
    children: [
      { name: 'TestSuite 26'},
      { name: 'TestSuite 27'},
      { name: 'TestSuite 28' },
      { name: 'TestSuite 29'},
      { name: 'TestSuite 30' },
      { name: 'TestSuite 31'}

    ]
  },
  {
    name: 'ComponentSuite',
    children: [
      { name: 'TestSuite 32'}
    ]
  },
  {
    name: 'dshal',
    
    children: [
      { name: 'TestSuite 33'}
    ]
  },
  {
    name: 'dshal_LD',
    children: [
      { name: 'TestSuite 34'}
    ]
  }
  ];

  constructor(private router: Router, private authservice: AuthService, 
    private _snakebar: MatSnackBar,private moduleservice: ModulesService,
    public dialog:MatDialog
  ) {
    this.treeControl = new FlatTreeControl<FlatNode>(
      node => node.level,
      node => node.expandable
    );

    this.treeFlattener = new MatTreeFlattener(
      this.transformer,
      node => node.level,
      node => node.expandable,
      node => node.children
    );

    this.dataSource = new MatTreeFlatDataSource(this.treeControl, this.treeFlattener);
    this.dataSource.data = this.treeData;
    console.log(this.dataSource.data);
    
    this.treeControlSuite = new FlatTreeControl<FlatNodeTestSuite>(
      node => node.level,
      node => node.expandable
    );

    this.treeFlattenerSuite = new MatTreeFlattener(
      this.transformerSuite,
      node => node.level,
      node => node.expandable,
      node => node.children
    );

    this.dataSourceSuite = new MatTreeFlatDataSource(this.treeControlSuite, this.treeFlattenerSuite);
    this.dataSourceSuite.data = this.treeTestSuiteData;

   }

  ngOnInit(): void {
    let functiondata = JSON.parse(localStorage.getItem('function') || '{}');
    this.dynamicModuleName = functiondata.moduleName;
    this.dynamicFunctionName = functiondata.functionName;
    this.authservice.selectedCategory = this.selectedCategory;

    this.updatePaginatedData();
    this.updatePaginatedDataSuite();
  }
  transformer = (node: TreeNode, level: number): FlatNode => {
    return {
      expandable: !!node.children && node.children.length > 0,
      name: node.name,
      level: level,
      testgroup: node.testgroup,
      childCount: node.children ? node.children.length : 0
    };
  };
  transformerSuite = (node: TreeNodeTestSuite, level: number): FlatNodeTestSuite => {
    return {
      expandable: !!node.children && node.children.length > 0,
      name: node.name,
      level: level,
      childCount: node.children ? node.children.length : 0
    };
  };

  hasChild = (_: number, node: FlatNode) => node.expandable;

  updatePaginatedData() : void{
    const start = this.currentPage * this.pageSize;
    const end = start + this.pageSize;
    this.paginatedData = this.treeData.slice(start, end);
    this.dataSource.data = this.paginatedData;
  }
  updatePaginatedDataSuite() : void{
    const start = this.currentPage * this.pageSize;
    const end = start + this.pageSize;
    this.paginationData = this.treeTestSuiteData.slice(start, end);
    this.dataSourceSuite.data = this.paginationData;
  }

  // Handle page change event from paginator
  onPageChange(event: any) : void{
    this.currentPage = event.pageIndex;
    this.updatePaginatedData();
  }

  onPageChangeSuite(event: any) : void{
    this.currentPage = event.pageIndex;
    this.updatePaginatedDataSuite();
  }

  flattenTreeData(tree: TreeNode[]): TreeNode[] {
    let result: TreeNode[] = [];
    tree.forEach(node => {
      result.push(node);
      if (node.children) {
        result = result.concat(this.flattenTreeData(node.children));
      }
    });
    return result;
  }


  createScripts():void{
    this.router.navigate(['script/create-scripts']);
  }

  onCategoryChange(newValue: string): void {
    this.headingName = newValue;
    this.selectedCategory = newValue;
    localStorage.setItem('scriptCategory', this.selectedCategory);
    if(this.selectedCategory){
      this.authservice.selectedCategory = this.selectedCategory;
    }
    
  }
  announceSortChange(sortState: any) : void {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }
  ngAfterViewInit() : void {
    if (this.sort) {
      this.sort.sortChange.subscribe((sortState: Sort) => {
        this.applySort(sortState);
      });
    }
  }
  applySort(sortState: Sort) {
    const data = this.dataSource.data.slice();

    if (!sortState.active || sortState.direction === '') {
      return;
    }

    this.dataSource.data = data.sort((a, b) => {
      let compareValue = 0;

      switch (sortState.active) {
        case 'name':
          compareValue = a.name.localeCompare(b.name);
          break;
        case 'testgroup':
          compareValue = a.testgroup?.localeCompare(b.testgroup || '') || 0;
          break;
      }

      return sortState.direction === 'asc' ? compareValue : -compareValue;
    });
  }

  filterTree(filterValue: string) :void{
    if(filterValue){
      const filteredTreeData = this.filterRecursive(this.treeData, filterValue);
      this.dataSource.data = filteredTreeData;
      this.treeControl.expandAll(); 
    }else{
      this.treeControl.collapseAll();
      this.ngOnInit();
    }

  }
  filterRecursive(data: TreeNode[], filterValue: string): TreeNode[] {
    return data
      .map((node) => ({
        ...node,
        children: node.children
          ? this.filterRecursive(node.children, filterValue)
          : [],
      }))
      .filter((node) => node.name.toLowerCase().includes(filterValue.toLowerCase()) || (node.children && node.children.length > 0));
  }

  viewChange(event:any): void {
    let name = event.target.value;
    this.viewName = name;
    if(name === 'testsuites'){
      this.testsuitTable = true;
      this.scriptTable = false;
    }else{
      this.testsuitTable = false;
      this.scriptTable = true;
    }
  }

  createScriptGroup():void{
    this.router.navigate(['script/create-script-group']);
  }



}
