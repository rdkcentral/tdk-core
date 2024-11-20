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
import { Component } from '@angular/core';
import { FooterComponent } from '../../layout/footer/footer.component';
import { MaterialModule } from '../../material/material.module';
import { Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { LoginService } from '../../services/login.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-prefered-category',
  standalone: true,
  imports: [FooterComponent,MaterialModule, RouterLink, ReactiveFormsModule, CommonModule],
  templateUrl: './prefered-category.component.html',
  styleUrl: './prefered-category.component.css'
})
export class PreferedCategoryComponent {

  submitted = false;
  categoryForm!: FormGroup;
  categorySelect!:string;
  loggedinUser:any;
  preferedCategory!:string;
  userCategory!:string;

  constructor(private fb: FormBuilder, private router: Router,
    private loginservice: LoginService, private _snakebar: MatSnackBar) {

      this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser')|| '{}');
      this.preferedCategory = localStorage.getItem('preferedCategory')|| '';
      this.userCategory = this.loggedinUser.userCategory;
  }

  ngOnInit(): void {
    this.categorySelect = this.preferedCategory?this.preferedCategory:this.userCategory;
    this.categoryForm = this.fb.group({
      catgegory: [this.categorySelect, Validators.required]
    });
    
  }

  changeCategory(event:any):void{
    let val = event.target.value;
    console.log(val);
    this.categorySelect = val?val:this.loggedinUser.userCategory;
  }

  categorySubmit():void{
    this.submitted = true;
    if(this.categoryForm.invalid){
      return ;
    }else{
      let userName = this.loggedinUser.userName;
      this.loginservice.changePrefernce(userName,this.categorySelect).subscribe({
        next:(res)=>{
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
            })
            localStorage.setItem('preferedCategory', this.categorySelect);
            setTimeout(() => {
            this.router.navigate(["/configure"]);
            }, 1000);
          },
          error:(err)=>{
            let errmsg = JSON.parse(err.error);
              this._snakebar.open(errmsg.message, '', {
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
