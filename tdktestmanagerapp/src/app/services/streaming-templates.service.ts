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
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { AuthService } from '../auth/auth.service';
import { GlobalConstants } from '../utility/global-constants';

const apiUrl: string = GlobalConstants.apiUrl;

@Injectable({
  providedIn: 'root'
})

export class StreamingTemplatesService {

  allPassedData: BehaviorSubject<any> = new BehaviorSubject<any>([]);

  constructor(private http: HttpClient, private authService: AuthService) { }

  storePassedObject(passedData: any) {
    this.allPassedData.next(passedData);
  }
  retrievePassedObject() {
    return this.allPassedData;
  }

  private options = { headers: new HttpHeaders().set('Authorization', this.authService.getApiToken()) };

  getstreamingdetails(): Observable<any> {
    return this.http.get(`${apiUrl}api/v1/streamingdetail/findall`, this.options);
  }

  getstreamingtemplateList(): Observable<any> {
    return this.http.get(`${apiUrl}api/v1/streamingdetailstemplate/gettemplatelist`, this.options);
  }

  createStreamingTemplate(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/streamingdetailstemplate/create`, data, { headers, responseType: 'text' })
  }

  deleteStreamingTemplate(name: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/streamingdetailstemplate/delete?templateName=${name}`, { headers, responseType: 'text' });
  }

  getStreamingtemplateUpdate(name: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/streamingdetailstemplate/getstreamingdetailsbytemplatename?templateName=${name}`, { headers, responseType: 'text' });
  }

  streamingTeamplatesUpdate(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.put(`${apiUrl}api/v1/streamingdetailstemplate/update`, data, { headers, observe: 'response', responseType: 'text' })

  }

}
