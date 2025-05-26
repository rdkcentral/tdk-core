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
import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { AuthService } from '../auth/auth.service';


@Injectable({
  providedIn: 'root'
})
export class ScriptsService {

  private dataSubjectTestSuite   = new BehaviorSubject<any>(null);
  data$ = this.dataSubjectTestSuite.asObservable();

  constructor(private http: HttpClient,private authService: AuthService,
    @Inject('APP_CONFIG') private config: any
  ) { }

  setData(data: any) {
    this.dataSubjectTestSuite.next(data);
  }

  getAllexecution(): Observable<any> {
    return this.http.get('assets/execution.json');
  }

  getAllDevice(): Observable<any> {
    return this.http.get('assets/leftpanel.json');
  }

  getallbymodules(category: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/script/findAllByModuleWithCategory?category=${category}`, { headers });
  }

  downloadTestcases(moduleName: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/script/downloadTestCaseAsExcelByModule?moduleName=${moduleName}`, { headers, responseType: 'blob' })
  }

  uploadZipFile(file: File): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post(`${this.config.apiUrl}api/v1/script/uploadScriptDataZip`, formData, { headers});
  }

  downloadScript(name: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/script/downloadScriptDataZip?scriptName=${name}`, { headers, responseType: 'blob' })
  }

  downloadTestCasesZip(category:any) :Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/script/downloadAllTestcaseZipByCategory?category=${category}`, { headers, responseType: 'blob' })
  }

  scriptTemplate(name:string) : Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/script/getScriptTemplate?primitiveTestName=${name}`, { headers, responseType: 'text' })
  }
  
  createScript(scriptCreateData:any,scriptFile:File):Observable<any>{
    const formData = new FormData();
    formData.append('scriptCreateData', new Blob([JSON.stringify(scriptCreateData)], { type: 'application/json' }));
    formData.append('scriptFile', scriptFile); 
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
   return this.http.post(`${this.config.apiUrl}api/v1/script/create`,formData,  { headers });
  }

  updateScript(scriptUpdateData:any,scriptFile:File):Observable<any>{
    const formData = new FormData();
    formData.append('scriptUpdateData', new Blob([JSON.stringify(scriptUpdateData)], { type: 'application/json' }));
    formData.append('scriptFile', scriptFile); 
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
   return this.http.put(`${this.config.apiUrl}api/v1/script/update`,formData,  { headers  });
  }

  delete(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${this.config.apiUrl}api/v1/script/delete?id=${id}`, { headers });
  }

  scriptFindbyId(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/script/findById?id=${id}`, { headers});
  }

  downloadSriptZip(name:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/script/downloadScriptDataZip?scriptName=${name}`, { headers, responseType: 'blob' })
  }

   downloadMdFile(name:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    
    return this.http.get(`${this.config.apiUrl}api/v1/script/downloadmdfilebyname?scriptName=${name}`, { headers, responseType: 'blob' })
  }

  findTestSuitebyCategory(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/script/findListByCategory?category=${category}`, { headers });
  }

  cretaeTestSuite(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
   return this.http.post(`${this.config.apiUrl}api/v1/testsuite/create`,data,  { headers  });
  }
  getModuleCustomTestSuite(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/module/findAllModuleNamesBySubCategory?category=${category}`, { headers}); 
  }

  getAllTestSuite(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/testsuite/findAllByCategory?category=${category}`, { headers }); 
  }

  downloadalltestsuitexmlZip(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/testsuite/downloadAllTestSuiteXml?category=${category}`, { headers, responseType: 'blob' })
  }

  downloadTestSuiteXML(testsuite:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/testsuite/downloadTestSuiteXml?testSuite=${testsuite}`, { headers, responseType: 'blob' })
  }

  downloadTestSuiteXLSX(testsuite:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${this.config.apiUrl}api/v1/testsuite/downloadTestCases?testSuite=${testsuite}`, { headers, responseType: 'blob' })
  }
  deleteTestSuite(id:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${this.config.apiUrl}api/v1/testsuite/delete?id=${id}`, { headers }); 
  }

  uploadTestSuiteXML(file:File): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    const formData: FormData = new FormData();
    formData.append('testSuite', file, file.name);
    return this.http.post(`${this.config.apiUrl}api/v1/testsuite/uploadTestSuiteXml`, formData, { headers});
  }

  updateTestSuite(data:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
   return this.http.put(`${this.config.apiUrl}api/v1/testsuite/update`,data,  { headers });
  
  }

  createCustomTestSuite(data:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
   return this.http.post(`${this.config.apiUrl}api/v1/testsuite/createCustomTestSuite`,data,  { headers});
  
  }



}
