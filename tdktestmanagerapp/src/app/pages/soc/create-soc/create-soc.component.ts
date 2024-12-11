import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../../auth/auth.service';
import { SocService } from '../../../services/soc.service';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonFormComponent } from '../../../utility/component/common-form/common-form.component';

@Component({
  selector: 'app-create-soc',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, CommonFormComponent],
  templateUrl: './create-soc.component.html',
  styleUrl: './create-soc.component.css'
})
export class CreateSocComponent {

  socVendorName: string | undefined;
  commonFormName = 'Create';
  loggedinUser: any={};
  errormessage!: string;
  validationName = 'SoC';
  placeholderName = 'SoC Name';
  labelName = 'Name';
  
  constructor(private router: Router, private route: ActivatedRoute, public service: SocService,
    private _snakebar: MatSnackBar, private authservice: AuthService) {
    this.commonFormName = this.route.snapshot.url[1].path === 'create-soc' ? this.commonFormName + ' ' + `${this.authservice.showSelectedCategory}` + ' ' + 'SoC' : this.commonFormName;
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
  }

  /**
   * Handles the form submission event.
   * @param name - The SOC name.
   */
  onFormSubmitted(name: string): void {
    let obj = {
      "socName": name,
      "socCategory": this.authservice.selectedConfigVal,
      "socUserGroup": this.loggedinUser.userGroupName
    }
    if(name !== undefined && name !== null){
      this.service.createSoc(obj).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["configure/list-soc"]);
  
          }, 1000);
  
        },
        error: (err) => {
          let errmsg = JSON.parse(err.error);
          this._snakebar.open(errmsg.socName?errmsg.socName:errmsg.message, '', {
            duration: 4000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
  
      })
    }
  
  }

  /**
   * Initializes the component.
   */  
  ngOnInit(): void {
  }

}
