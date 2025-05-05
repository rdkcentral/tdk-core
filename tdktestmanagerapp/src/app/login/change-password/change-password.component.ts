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
import { Component, OnInit } from '@angular/core';
import { FooterComponent } from '../../layout/footer/footer.component';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormGroup, ReactiveFormsModule, Validators, FormBuilder, AbstractControl } from '@angular/forms';
import { LoginService } from '../../services/login.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MaterialModule } from '../../material/material.module';

@Component({
  selector: 'app-change-password',
  standalone: true,
  imports: [FooterComponent, MaterialModule, RouterLink, ReactiveFormsModule, CommonModule],
  templateUrl: './change-password.component.html',
  styleUrl: './change-password.component.css'
})

/**
 * Represents the ChangePasswordComponent of the application.
 */
export class ChangePasswordComponent implements OnInit {
  /**
   * Represents the showPassword of the application.
   */
  public showPassword: boolean | undefined;
  /**
   * Represents the showNewPassword of the application.
   */
  public showPasswordOnPress: boolean = true;
  /**
   * Represents the showConfirmPassword of the application.
   */
  public showNewPasswordOnPress:boolean = true;
  /**
   * Represents the showConfirmPassword of the application.
   */
  public showConfirmPasswordOnPress:boolean = true;
  /**
   * Represents the passwordIcon of the application.
   */
  passwordIcon = "TDKTestManagerApp/src/assets/password show.png"
  /**
   * Represents the submitted of the application.
   */
  submitted = false;
  /**
   * Represents the changePasswordForm of the application.
   */
  changePasswordForm!: FormGroup;
  /**
   * Represents the visible of the application.
   */
  visible = true;
  /**
   * Represents the errorMessage of the application.
   */
  errorMessage: any = {};
  loggedInUser: any={};

  constructor(private formBuilder: FormBuilder, private router: Router,
    private loginservice: LoginService, private _snakebar: MatSnackBar,
  ) {
    this.loggedInUser = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
  }

  /**
   * Initializes the component.
   */
  ngOnInit(): void {

    this.changePasswordForm = this.formBuilder.group({
      username: [{value:this.loggedInUser.userName, disabled: true}],
      oldpassword: ['', [Validators.required, Validators.minLength(6)]],
      newpassword: ['', [Validators.required, Validators.minLength(6)]],
      confirmpassword: ['', Validators.required],
    }, { validators: this.passwordMatchValidator('newpassword', 'confirmpassword') });

    this.changePasswordForm.get('username')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/\s+/g, '');
      if (cleanedValue !== value) {
        this.changePasswordForm.get('username')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
    this.changePasswordForm.get('oldpassword')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/\s+/g, '');
      if (cleanedValue !== value) {
        this.changePasswordForm.get('oldpassword')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
    this.changePasswordForm.get('newpassword')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/\s+/g, '');
      if (cleanedValue !== value) {
        this.changePasswordForm.get('newpassword')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
    this.changePasswordForm.get('confirmpassword')?.valueChanges.subscribe((value) => {
      const cleanedValue = value.replace(/\s+/g, '');
      if (cleanedValue !== value) {
        this.changePasswordForm.get('confirmpassword')?.setValue(cleanedValue, {
          emitEvent: false,
        });
      }
    });
  }

  /**
   * Represents the f of the application.
   */
  get f() { return this.changePasswordForm.controls; }

  /**
   * Custom validator for password match.
   * @param newPassword - The new password form control.
   * @param cnfrmPassword - The confirm password form control.
   * @returns 
   */
  passwordMatchValidator(newPassword: any, cnfrmPassword: any) {
    return (formGroup: FormGroup) => {
      let password = formGroup['controls'][newPassword] as AbstractControl;
      let confirmPassword = formGroup['controls'][cnfrmPassword] as AbstractControl;
      if (confirmPassword.errors && !confirmPassword.errors['passwordMatchValidator']) {
        return
      }
      if (password.value !== confirmPassword.value) {
        confirmPassword.setErrors({ passwordMatchValidator: true })
      } else {
        confirmPassword.setErrors(null)
      }
    }
  }

  /**
  * Method to reset the password.
  */
  resetPassword(): void {
    this.submitted = true;
    if (this.changePasswordForm.invalid) {
      return
    } else {
      let obj = {
        userName: this.loggedInUser.userName,
        oldPassword: this.changePasswordForm.value.oldpassword,
        newPassword: this.changePasswordForm.value.newpassword
      }
      this.loginservice.restPassword(obj).subscribe({
        next: (res) => {
          this._snakebar.open(res.message, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["/"]);
          }, 1000);

        },
        error: (err) => {
          let errMsgDisplay = err.message;
          this._snakebar.open(errMsgDisplay, '', {
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
   * Method to view the password.
   */
  viewPassword(): void {
    this.showPasswordOnPress = !this.showPasswordOnPress;
    if (this.showPasswordOnPress) {
      this.showPasswordOnPress = true;
    }
  }
  /**
   * Method to view the new password.
   */

  viewNewPassword(): void {
    this.showNewPasswordOnPress = !this.showNewPasswordOnPress;
    if (this.showNewPasswordOnPress) {
      this.showNewPasswordOnPress = true;
    }
  }

  /**
   * Method to view the confirm password.
   */
  viewConfirmPassword() : void {
    this.showConfirmPasswordOnPress = !this.showConfirmPasswordOnPress;
    if (this.showConfirmPasswordOnPress) {
      this.showConfirmPasswordOnPress = true;
    }
  }
  /**
   * Method to reset the form.
   */
  reset(): void {
    this.changePasswordForm.reset();
  }

}
