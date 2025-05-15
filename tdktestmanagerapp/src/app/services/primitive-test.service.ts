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
import { Inject, inject, Injectable } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PrimitiveTestService {

  currentUrl: any;
  allPassedData: BehaviorSubject<any> = new BehaviorSubject<any>([]);
  private dropdownValueSubject = new BehaviorSubject<any>(null); 

  constructor(private http: HttpClient, private authService: AuthService,
    @Inject('APP_CONFIG') private config: any
  ) { }
  private options = { headers: new HttpHeaders().set('Authorization', this.authService.getApiToken()) };

  getlistofModules(category: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/module/findAllModuleNamesByCategory?category=${category}`, { headers});

  }

  getlistofFunction(moduleName: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/function/getlistoffunctionbymodulename?moduleName=${moduleName}`, { headers});

  }

  createPrimitiveTest(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${this.config.apiUrl}api/v1/primitivetest/create`, data, { headers })
  }

  getParameterNames(moduleName: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/primitivetest/getlistbymodulename?moduleName=${moduleName}`, { headers });
  }

  getParameterList(functionName: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/parameter/findAllByFunction?functionName=${functionName}`, { headers});
  }

  getParameterListUpdate(id: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/primitivetest/findbyid?id=${id}`, { headers });
  }

  updatePrimitiveTest(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.put(`${this.config.apiUrl}api/v1/primitivetest/update`, data, { headers, observe: 'response'})
  }

  deletePrimitiveTest(id: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${this.config.apiUrl}api/v1/primitivetest/delete?id=${id}`, { headers});
  }
 
  dropdownValue$ = this.dropdownValueSubject.asObservable();

  setDropdownValue(value: string) {
    this.dropdownValueSubject.next(value);
  }

  getDropdownValue() {
    return this.dropdownValueSubject.value;
  }
}