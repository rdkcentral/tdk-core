import { CommonModule } from '@angular/common';
import { ApplicationRef, ChangeDetectionStrategy, ChangeDetectorRef, Component, Inject, NgZone } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../../material/material.module';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { AnalysisService } from '../../../../services/analysis.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-update-jira',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, MaterialModule],
  templateUrl: './update-jira.component.html',
  styleUrl: './update-jira.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UpdateJiraComponent {

    jiraUpdateSubmitted = false;
    jiraUpdateForm!: FormGroup;
    allLabels:any;
    loggedinUser:any;

  constructor(
    public dialogRef: MatDialogRef<UpdateJiraComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private analysiservice: AnalysisService,
    private fb: FormBuilder,
    private _snakebar: MatSnackBar,
    private cdRef: ChangeDetectorRef,
    private appRef: ApplicationRef,
    private ngZone: NgZone
  ) {
    this.loggedinUser = JSON.parse(
      localStorage.getItem('loggedinUser') || '{}'
    );
    console.log(data);
  }
    ngOnInit(): void {
      this.ListLabels();
      this.initialForms();

    }

    initialForms(){
      this.jiraUpdateForm = this.fb.group({
        ticketNumber:[this.data.update.ticketNumber, Validators.required],
        label:['', Validators.required],
        comments:['', Validators.required],
        user:['', Validators.required],
        password:['', Validators.required],
        exelogs:[false],
        devlogs:[false]
      })
    }
    ListLabels(){
      this.analysiservice.ListOfLabels().subscribe((res) => {
        this.allLabels = JSON.parse(res);
      });
    }

    onJiraUpdate(){
      this.jiraUpdateSubmitted = true;
      // this.cdRef.markForCheck();
      this.ngZone.run(() => { // Run in Angular's zone
        this.cdRef.detectChanges(); // Or this.appRef.tick();
    });
      // this.cdRef.detectChanges();
      if (this.jiraUpdateForm.invalid) {
        return 
      } else {
        console.log(this.jiraUpdateForm.value);
        let updateObj = {
          "executionResultId": this.data.updateDetails.executionResultID,
          "ticketNumber":this.jiraUpdateForm.value.ticketNumber,
          "comments": this.jiraUpdateForm.value.comments,
          "label": this.jiraUpdateForm.value.label,
          "user": this.jiraUpdateForm.value.user,
          "password": this.jiraUpdateForm.value.password,
          "executionLogNeeded": this.jiraUpdateForm.value.exelogs,
          "deviceLogNeeded": this.jiraUpdateForm.value.devlogs
        }
        this.analysiservice.updateJiraTicket(updateObj).subscribe({
          next:(res)=>{
            this._snakebar.open(res, '', {
              duration: 1000,
              panelClass: ['success-msg'],
              verticalPosition: 'top'
            })
            setTimeout(() => {
            this.close();
            }, 2000);
          },
          error:(err)=>{
            this._snakebar.open(err, '', {
              duration: 1000,
              panelClass: ['err-msg'],
              horizontalPosition: 'end',
              verticalPosition: 'top'
            })
          }
        })
      }
    }
    close(): void {
      this.dialogRef.close(false);
    }
}
