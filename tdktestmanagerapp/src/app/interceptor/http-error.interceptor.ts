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
import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { catchError, throwError } from 'rxjs';

export const httpErrorInterceptor: HttpInterceptorFn = (req, next) => {
  const snackBar = inject(MatSnackBar);
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      let err = error.error;
      // let err = JSON.parse(error.error);
      console.log(err);
      
      let errorMessage = err.message?err.message:'Network error. Please check your internet connection.';
        if (error instanceof ProgressEvent) {
          errorMessage = 'Network error. Please check your internet connection.';
        }
         if (error instanceof HttpErrorResponse) {
          // For other HTTP errors like 404, 500, etc.
          if (error.status == 0) {
            errorMessage = 'Unable to connect to the server. Please check if the server is running.';
          } 
          if(error.status == 500){
            errorMessage = 'Internal Server Error'
          }
          if(error.status == 502){
            errorMessage = 'Something went wrong'
          }
          if(error.status == 404){
            errorMessage = err;
          }
          if(error.status == 400){
            let err = JSON.parse(error.error);
            errorMessage = err.message;
          }
        }
      snackBar.open(errorMessage || 'An error occurred', 'Close', {
        duration: 2500,
        panelClass: ['err-msg'],
        horizontalPosition: 'end',
        verticalPosition: 'top'
      });
      return throwError(() => error);
    })
  );
};
