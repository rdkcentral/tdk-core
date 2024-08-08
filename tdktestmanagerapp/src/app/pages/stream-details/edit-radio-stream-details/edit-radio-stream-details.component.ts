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
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { StreamingDetailsService } from '../../../services/streaming-details.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';

/**
 * Component for editing radio stream details.
 */
@Component({
  selector: 'app-edit-radio-stream-details',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, FormsModule],
  templateUrl: './edit-radio-stream-details.component.html',
  styleUrl: './edit-radio-stream-details.component.css'
})
export class EditRadioStreamDetailsComponent {

  /**
   * Form group for editing radio stream details.
   */
  editRadioStreamForm!: FormGroup;

  /**
   * Flag to indicate if the form has been submitted.
   */
  editStreamingFormsubmitted = false;

  /**
   * User object.
   */
  user: any={};

  /**
   * Error message.
   */
  errormessage!: string;

  constructor(private formBuilder: FormBuilder, public service: StreamingDetailsService,
    private _snakebar: MatSnackBar, private authservice: AuthService, private route: ActivatedRoute,
    private router: Router) {

    this.user = JSON.parse(localStorage.getItem('user') || '{}');

    if (!this.user) {
      this.router.navigate(['configure/list-streamdetails']);
    }

  }

  /**
   * Lifecycle hook called after component initialization.
   */
  ngOnInit(): void {

    this.editRadioStreamForm = this.formBuilder.group({
      streamid: [this.user.streamingDetailsId, Validators.required]
    });
  }

  /**
   * Method to edit radio stream.
   */
  editRadioStream():void {

    this.editStreamingFormsubmitted = true;
    if (this.editRadioStreamForm.invalid) {
      return
    } else {
      let obj = {
        streamingDetailsId: this.user.streamId,
        streamId: this.editRadioStreamForm.value.streamid,
        streamType: "RADIO"
      }
      this.service.updateStreamingDetails(obj).subscribe({
        next: (res) => {
          this._snakebar.open('Radio streaming details updated successfully', '', {
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
          this.errormessage = errmsg.message ? errmsg.message : errmsg.password;
          this._snakebar.open(this.errormessage, '', {
            duration: 3000,
            panelClass: ['err-msg'],
            horizontalPosition: 'end',
            verticalPosition: 'top'
          })
        }

      })
    }

  }

  /**
   * Getter for accessing the form controls.
   */
  get f() { return this.editRadioStreamForm.controls; }

  /**
   * Method to reset the form.
   */
  reset():void {
    this.editRadioStreamForm.reset({
      streamid: ''
    });
  }

  /**
   * Method to navigate back to the list of stream details.
   */
  goBack():void {
    this.router.navigate(["configure/list-streamdetails"]);
  }

}
