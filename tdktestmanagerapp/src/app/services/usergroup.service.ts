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
import { GlobalConstants } from '../utility/global-constants';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { AuthService } from '../auth/auth.service';
import { Observable } from 'rxjs';

const apiUrl: string = GlobalConstants.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class UsergroupService {
  currentUrl: any;
  isEdit = false;
  constructor(private http: HttpClient, private authService: AuthService) {
  }

  private options = { headers: new HttpHeaders().set('Authorization', this.authService.getApiToken()) };

  getuserGroupList(): Observable<any> {
    return this.http.get(`${apiUrl}api/v1/usergroup/findall`, this.options);
  }

  createuserGroup(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    let params = new HttpParams();
    params = params.set('userGroupName', data);

    return this.http.post(`${apiUrl}api/v1/usergroup/create`, params, { headers, responseType: 'text' })
  }

  updateUserGroup(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': this.authService.getApiToken()
    });
    return this.http.put(`${apiUrl}api/v1/usergroup/update`, data, { headers, responseType: 'text' })
  }

  deleteUserGroup(id: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/usergroup/delete/${id}`, { headers, responseType: 'text' });
  }

}
