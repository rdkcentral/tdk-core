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
import { Component, OnInit} from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { StreamingDetailsService } from '../../../services/streaming-details.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../auth/auth.service';

/**
 * Component for editing stream details.
 */
@Component({
  selector: 'app-edit-stream-details',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, FormsModule],
  templateUrl: './edit-stream-details.component.html',
  styleUrl: './edit-stream-details.component.css'
})
export class EditStreamDetailsComponent implements OnInit {

  /**
   * The user object.
   */
  user: any={};

  /**
   * The form group for editing stream details.
   */
  editStreamForm!: FormGroup;

  /**
   * Flag to indicate if the edit streaming form has been submitted.
   */
  editStreamingFormsubmitted = false;

  /**
   * The ID of the stream.
   */
  id!: number;

  /**
   * Error message.
   */
  errormessage!: string;

  /**
   * The logged-in user object.
   */
  loggedinUser: any={};

  /**
   * Constructor for EditStreamDetailsComponent.
   * @param formBuilder - The form builder service.
   * @param service - The streaming details service.
   * @param _snakebar - The snackbar service.
   * @param authservice - The authentication service.
   * @param route - The activated route service.
   * @param router - The router service.
   */
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
    this.editStreamForm = this.formBuilder.group({
      streamid: [this.user.streamingDetailsId, Validators.required],
      channelType: [this.user.channelType, Validators.required],
      audioType: [this.user.audioType, Validators.required],
      videoType: [this.user.videoType, Validators.required]
    });

  }

  /**
   * Method to edit the stream.
   */
  editStream() :void{
    this.editStreamingFormsubmitted = true;
    if (this.editStreamForm.invalid) {
      return
    } else {
      let obj = {
        streamingDetailsId: this.user.streamId,
        streamId: this.editStreamForm.value.streamid,
        channelType: this.editStreamForm.value.channelType,
        videoType: this.editStreamForm.value.videoType,
        audioType: this.editStreamForm.value.audioType,
        userGroup: this.user.userGroupName,
        streamType: "VIDEO"
      }
      this.service.updateStreamingDetails(obj).subscribe({
        next: (res) => {
          this._snakebar.open('Streaming details updated successfully', '', {
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
  get f() { return this.editStreamForm.controls; }

  /**
   * Method to reset the form.
   */
  reset() :void{
    this.editStreamForm.reset({
      username: ''
    });
  }

  /**
   * Method to navigate back to the list of stream details.
   */
  goBack() :void{
    this.router.navigate(["configure/list-streamdetails"]);
  }

}
