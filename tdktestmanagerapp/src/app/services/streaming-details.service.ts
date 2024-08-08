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
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { GlobalConstants } from '../utility/global-constants';
import { AuthService } from '../auth/auth.service';

const apiUrl: string = GlobalConstants.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class StreamingDetailsService {

  currentUrl: any;

  constructor(private http: HttpClient, private authService: AuthService) { }

  private options = { headers: new HttpHeaders().set('Authorization', this.authService.getApiToken()) };

  getStreamDetails(): Observable<any> {

    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(
      `${apiUrl}api/v1/streamingdetail/findall`,
      { headers, responseType: 'text' }
    );
    // return this.http.get(`${apiUrl}api/v1/socvendor/getlistbycategory?category=rdkv`, this.options);
  }

  createStreamDetails(data: any): Observable<any> {
    console.log('Data being send to the server:', data);
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': this.authService.getApiToken()
    });

    return this.http.post(`${apiUrl}api/v1/streamingdetail/create`, data, { headers, responseType: 'text' })
  }

  createRadioStreamingDetails(data: any): Observable<any> {
    console.log('Data being send to the server:', data);
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': this.authService.getApiToken()
    });

    return this.http.post(`${apiUrl}api/v1/streamingdetail/create`, data, { headers, responseType: 'text' })
  }

  updateStreamingDetails(data: any): Observable<any> {
    console.log("Data in updatefn", data);
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });

    return this.http.put(`${apiUrl}api/v1/streamingdetail/update`, data, { headers, responseType: 'text' })
  }

  deleteStreamingDetails(id: any): Observable<any> {
    console.log('Streaming details id:', id);
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/streamingdetail/delete/${id}`, { headers, responseType: 'text' });
  }

}

