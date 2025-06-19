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
import { Component, ElementRef, Inject, ViewChild } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { MaterialModule } from '../../../../material/material.module';
import { FormsModule } from '@angular/forms';
import { ExecutionService } from '../../../../services/execution.service';
import { interval, startWith, Subject, Subscription, switchMap, takeUntil } from 'rxjs';
import { LoaderComponent } from '../../loader/loader.component';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-livelog-dialog',
  standalone: true,
  imports: [CommonModule, MaterialModule, FormsModule],
  templateUrl: './livelog-dialog.component.html',
  styleUrl: './livelog-dialog.component.css'
})
export class LivelogDialogComponent {
  @ViewChild('logArea') logArea!: ElementRef<HTMLTextAreaElement>;
  logs: string = '';
  executionResultId: any;
  loader = false;
  liveLogInterval: any;
  private destroy$ = new Subject<void>();

  constructor(
    public dialogRef: MatDialogRef<LivelogDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, public dialog: MatDialog, private executionservice: ExecutionService,
    public liveLogDialog: MatDialog, private _snakebar: MatSnackBar) {
  }

  ngOnInit(): void {
    this.logs = this.data.logs;
    this.refreshLiveLogs(); // Initial fetch
    this.liveLogInterval = setInterval(() => {
      this.autoRefreshLiveLogs();
    }, 60000); // 30 seconds
  }

  scrollToBottom() {
    const logArea = this.logArea.nativeElement;
    logArea.scrollTop = logArea.scrollHeight;
  }

  refreshLiveLogs() {
    this.loader = true;
    this.executionservice.getLiveLogs(this.data.executionId).subscribe(
      (response) => {
        setTimeout(() => {
          this.logs = response;
          this.loader = false;         
        }, 1500);
      });
  }

  autoRefreshLiveLogs() {
    this.loader = true;
    this.executionservice.getLiveLogs(this.data.executionId).subscribe(
      (response) => {
        setTimeout(() => {
          this.logs = response;
          this.loader = false;
          setTimeout(() => {
            this.scrollToBottom();
          }, 0);
        }, 1500);
      });
  }


  ngOnDestroy(): void {
    if (this.liveLogInterval) {
      clearInterval(this.liveLogInterval);
    }
    this.destroy$.next();    // <-- This notifies the subscription to unsubscribe
    this.destroy$.complete(); // Complete the destroy$ subject
  }

  onClose(): void {
    this.destroy$.next(); // Notify all subscriptions to complete
    this.dialogRef.close(false);
  }
}
