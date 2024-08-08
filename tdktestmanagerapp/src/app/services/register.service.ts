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
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { GlobalConstants } from '../utility/global-constants';
import { Observable, catchError, map, throwError } from 'rxjs';

const apiUrl: string = GlobalConstants.apiUrl;

@Injectable({
  providedIn: 'root',
})
export class RegisterService {
  constructor(private http: HttpClient) { }

  registerUser(user: any): Observable<any> {

    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });

    return this.http.post(`${apiUrl}api/v1/auth/signup`, user, { headers: headers, responseType: 'text' }).pipe(
      map(res => {
        try {
          return JSON.stringify(res)
        } catch (e) {
          return res
        }
      })
    );
    // return this.http.post(`${apiUrl}api/v1/auth/signup`, user,{ headers: headers,responseType: 'text' }).pipe(
    //   catchError((error: HttpErrorResponse) => {
    //     let errorMessage = 'An unknown error occurred!';
    //     if (error.error) {
    //       try {
    //         const parsedError = JSON.parse(error.error);
    //         if (parsedError.message) {
    //           errorMessage = parsedError.message;
    //         }
    //       } catch (e) {
    //         errorMessage = 'Error parsing error response';
    //       }
    //     } else if (error.message) {
    //       errorMessage = error.message;
    //     }
    //     return throwError(() => new Error(errorMessage));
    //   })
    // );
  }

}
