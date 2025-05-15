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
import { Inject, Injectable } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})

export class RdkVersionsService {

    currentUrl: any;

    constructor(private http: HttpClient, private authService: AuthService,
      @Inject('APP_CONFIG') private config: any
    ) { }
    private options = { headers: new HttpHeaders().set('Authorization', this.authService.getApiToken()) };

    createRdkVersion(data: any): Observable<any> {
        const headers = new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': this.authService.getApiToken()
        });
    
        return this.http.post(`${this.config.apiUrl}api/v1/rdkversion/create`, data, { headers, responseType: 'text' })
      }

      getRdkVersionByList(category: any): Observable<any> {
        const headers = new HttpHeaders({
          'Authorization': this.authService.getApiToken()
        });
        return this.http.get(`${this.config.apiUrl}api/v1/rdkversion/findallbycategory?category=${category}`, { headers, responseType: 'text' });
      }

      updateRdkVersion(data: any): Observable<any> {
        const headers = new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': this.authService.getApiToken()
        });
        return this.http.put(`${this.config.apiUrl}api/v1/rdkversion/update`, data, { headers,  responseType: 'text'})
      }

      deleteRdkVersion(id: any): Observable<any>{
        const headers = new HttpHeaders({
          'Authorization': this.authService.getApiToken()
        });
        return this.http.delete(`${this.config.apiUrl}api/v1/rdkversion/delete/${id}`, { headers, responseType: 'text' });
      }
}