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
import { MatSort } from '@angular/material/sort';
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

interface FlatNode {
  expandable: boolean;
  name: string;
  level: number;
  childCount: number;
  testgroup:string;
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

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
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
  private _liveAnnouncer = inject(LiveAnnouncer);

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
    
   }

  ngOnInit(): void {
    let functiondata = JSON.parse(localStorage.getItem('function') || '{}');
    this.dynamicModuleName = functiondata.moduleName;
    this.dynamicFunctionName = functiondata.functionName;
    this.authservice.selectedCategory = this.selectedCategory;

    this.updatePaginatedData();
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

  hasChild = (_: number, node: FlatNode) => node.expandable;

  updatePaginatedData() {
    const start = this.currentPage * this.pageSize;
    const end = start + this.pageSize;
    this.paginatedData = this.treeData.slice(start, end);
    this.dataSource.data = this.paginatedData;
  }

  // Handle page change event from paginator
  onPageChange(event: any) {
    this.currentPage = event.pageIndex;
    this.updatePaginatedData();
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
  // applyFilter(event: Event) {
  //   const filterValue = (event.target as HTMLInputElement).value;
  //   this.dataSource.filter = filterValue.trim().toLowerCase();
  // }
  downloadEXcel(params:any):void{

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
  announceSortChange(sortState: any) {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }
  filterTree(filterValue: string) {
    if(filterValue){
      const filteredTreeData = this.filterRecursive(this.treeData, filterValue);
      this.dataSource.data = filteredTreeData;
      this.treeControl.expandAll(); // Expands all the nodes after filtering
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
}
