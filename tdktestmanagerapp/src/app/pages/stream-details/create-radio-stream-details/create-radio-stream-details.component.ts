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
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { StreamingDetailsService } from '../../../services/streaming-details.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';

/**
 * Component for creating radio stream details.
 */
@Component({
  selector: 'app-create-radio-stream-details',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, FormsModule],
  templateUrl: './create-radio-stream-details.component.html',
  styleUrl: './create-radio-stream-details.component.css'
})
/**
 * Component for creating radio stream details.
*/
export class CreateRadioStreamDetailsComponent implements OnInit {

  /**
   * Form group for creating radio stream.
   */
  createRadioStreamForm!: FormGroup;

  /**
   * Flag to indicate if the form has been submitted.
   */
  radioStreamingFormSubmitted = false;

  /**
   * The logged-in user.
   */
  loggedinUser: any={};

  /**
   * Error message.
   */
  errormessage!: string;

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    public service: StreamingDetailsService,
    private _snakebar: MatSnackBar,
    private authservice: AuthService
  ) {
    this.loggedinUser = JSON.parse(localStorage.getItem('loggedinUser') || '{}')
  }

  /**
   * Initializes the component.
   */
  ngOnInit(): void {
    this.createRadioStreamForm = this.formBuilder.group({
      radiostreamid: ['', Validators.required]
    });
  }


  /**
   * Creates a radio stream.
   * 
   * This method is responsible for creating a radio stream by submitting the form data.
   * If the form is invalid, the method will return early without performing any action.
   * 
   * @returns void
   */
  createRadioStream():void {
    this.radioStreamingFormSubmitted = true;
    if (this.createRadioStreamForm.invalid) {
      return
    } else {
      let obj2 = {
        "streamingDetailsId": this.createRadioStreamForm.value.radiostreamid,
        "streamType": "RADIO"
      }
      this.service.createRadioStreamingDetails(obj2).subscribe({
        next: (res) => {
          this._snakebar.open(res, '', {
            duration: 3000,
            panelClass: ['success-msg'],
            verticalPosition: 'top'
          })
          setTimeout(() => {
            this.router.navigate(["configure/list-streamdetails"]);

          }, 1000);

        },
        error: (err) => {
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

  /**
   * Getter for form controls.
   */
  get f() { return this.createRadioStreamForm.controls; }

  /**
   * Resets the form.
   */
  reset() :void{
    this.createRadioStreamForm.reset({
      radiostreamid: ''
    });
  }

  /**
   * Navigates back to the list of stream details.
   */
  goBack():void {
    this.router.navigate(["configure/list-streamdetails"]);
  }

}
