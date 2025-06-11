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
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  isloggedIn = false;
  private logoutSubject = new Subject<void>();
  onLogout$ = this.logoutSubject.asObservable();

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    @Inject('APP_CONFIG') private config: any  // <-- Inject runtime config
  ) {}

  userlogin(data: any): Observable<any> {
    return this.http.post(`${this.config.apiUrl}api/v1/auth/signin`, data);
  }
  getuserGroup(): Observable<any> {
    return this.http.get(`${this.config.apiUrl}api/v1/auth/getList`);
  }

  getAuthenticatedUser() {
    const current_user = <string>localStorage.getItem('loggedinUser');
    return JSON.parse(current_user);
  }

  logoutUser(): void {
    this.logoutSubject.next();
    this.isloggedIn = false;
    localStorage.clear();
  }

  restPassword(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${this.config.apiUrl}api/v1/users/changepassword`, data, { headers });
  }

  changePrefernce(username:any,category:any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${this.config.apiUrl}api/v1/auth/changecategorypreference?userName=${username}&category=${category}`, {}, { headers });
  }

}
