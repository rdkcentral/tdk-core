import { Component } from '@angular/core';
import { SocService } from '../../../services/soc.service';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';
import { CommonFormComponent } from "../../../utility/component/common-form/common-form.component";

@Component({
  selector: 'app-edit-soc',
  standalone: true,
  imports: [CommonFormComponent],
  templateUrl: './edit-soc.component.html',
  styleUrl: './edit-soc.component.css'
})
export class EditSocComponent {

  record: any;
  id!: number;
  commonFormName = 'Update';
  errormessage!: string;
  validationName = 'soc';
  placeholderName = 'Soc Name';
  labelName = 'Name';

  constructor(private route: ActivatedRoute, private router: Router, private _snakebar: MatSnackBar,
    public service: SocService, private authservice: AuthService) {
    this.service.currentUrl = this.route.snapshot.url[1].path
    this.commonFormName = this.route.snapshot.url[1].path === 'edit-soc' ? this.commonFormName + ' ' + `${this.authservice.showSelectedCategory}` + ' ' + 'SoC' : this.commonFormName;
  }

   /**
   * Initializes the component.
   */ 
  ngOnInit(): void {
    this.id = +this.route.snapshot.params['id'];
    this.service.currentUrl = this.id;
    let data = JSON.parse(localStorage.getItem('user') || '{}');
    this.record = data;

  }

  /**
   * Handles the form submission.
   * @param name - The name of the SOC.
   */
  onFormSubmitted(name: any): void {
    let obj = {
      socId: this.record.socId,
      socName: name,
      socCategory: this.authservice.selectedConfigVal
    }
    if (name !== undefined && name !== null) {
      this.service.updateSoc(obj).subscribe({
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
          this._snakebar.open(errmsg.message, '', {
            duration: 3000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }
 
      })
    }
  }

}
