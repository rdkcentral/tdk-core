import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-analysis',
  standalone: true,
  imports: [CommonModule,FormsModule, ReactiveFormsModule],
  templateUrl: './analysis.component.html',
  styleUrl: './analysis.component.css'
})
export class AnalysisComponent {

  selectedDfaultCategory!: string;
  categoryName!:string;
  loggedinUser:any;
  userCategory!:string;
  preferedCategory!:string;
  scriptShow = true;
  showTestSuite = false;

  constructor(private authservice: AuthService) { 
      this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
      this.userCategory = this.loggedinUser.userCategory;
      this.preferedCategory = localStorage.getItem('preferedCategory')|| '';
    }

  ngOnInit(): void {
    let localcategory = this.preferedCategory?this.preferedCategory:this.userCategory;
    this.categoryChange(localcategory);
  }
  categoryChange(val:string): void {
    if (val === 'RDKB') {
      this.categoryName = 'Broadband';
      this.selectedDfaultCategory = 'RDKB';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
    } else if (val === 'RDKC') {
      this.categoryName = 'Camera';
      this.selectedDfaultCategory = 'RDKC';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
    } else {
      this.selectedDfaultCategory = 'RDKV';
      this.categoryName = 'Video';
      this.authservice.selectedCategory = this.selectedDfaultCategory;
    }
  }

  resultChange(event:any): void {

  }
  resultCategory(event:any): void {

  }
  deviceChange(event:any): void {

  }
  scriptType(value:string): void {
    if(value ==='testsuites'){
      this.scriptShow = false;
      this.showTestSuite = true;
    }else{
      this.scriptShow = true;
      this.showTestSuite = false;
    }
  }
  scriptChange(event:any): void {

  }
  testSuiteChange(event:any): void {

  }
  resultNoChange(val:any): void {

  }


}
