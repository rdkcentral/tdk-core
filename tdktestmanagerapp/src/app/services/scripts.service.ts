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
export class ScriptsService {

  private dataSubjectTestSuite   = new BehaviorSubject<any>(null);
  data$ = this.dataSubjectTestSuite.asObservable();

  constructor(private http: HttpClient,private authService: AuthService) { }

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
    return this.http.get(`${apiUrl}api/v1/script/findallbymodulewithcategory?category=${category}`, { headers, responseType: 'text' });
  }

  downloadTestcases(moduleName: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/downloadtestcaseasexcelbymodule?moduleName=${moduleName}`, { headers, responseType: 'blob' })
  }

  uploadZipFile(file: File): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post(`${apiUrl}api/v1/script/uploadscriptdatazip`, formData, { headers, responseType: 'text' });
  }

  downloadScript(name: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/downloadscriptdatazip?scriptName=${name}`, { headers, responseType: 'blob' })
  }

  downloadTestCasesZip(category:any) :Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/downloadalltestcasezipbycategory?category=${category}`, { headers, responseType: 'blob' })
  }

  scriptTemplate(name:string){
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/template/${name}`, { headers, responseType: 'text' })
  }
  
  createScript(scriptCreateData:any,scriptFile:File):Observable<any>{
    const formData = new FormData();
    formData.append('scriptCreateData', new Blob([JSON.stringify(scriptCreateData)], { type: 'application/json' }));
    formData.append('scriptFile', scriptFile); 
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
   return this.http.post(`${apiUrl}api/v1/script/create`,formData,  { headers,responseType: 'text'  });
  }

  updateScript(scriptUpdateData:any,scriptFile:File):Observable<any>{
    const formData = new FormData();
    formData.append('scriptUpdateData', new Blob([JSON.stringify(scriptUpdateData)], { type: 'application/json' }));
    formData.append('scriptFile', scriptFile); 
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
   return this.http.put(`${apiUrl}api/v1/script/update`,formData,  { headers,responseType: 'text'  });
  }

  delete(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/script/delete/${id}`, { headers, responseType: 'text' });
  }

  scriptFindbyId(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/findbyid/${id}`, { headers, responseType: 'text' });
  }

  downloadSriptZip(name:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/downloadscriptdatazip?scriptName=${name}`, { headers, responseType: 'blob' })
  }

  findTestSuitebyCategory(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/findlistbycategory?category=${category}`, { headers, responseType: 'text' });
  }

  cretaeTestSuite(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
   return this.http.post(`${apiUrl}api/v1/testsuite/create`,data,  { headers,responseType: 'text'  });
  }
  getModuleCustomTestSuite(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/module/getlistofmodulenamebycategory/${category}`, { headers, responseType: 'text' }); 
  }

  getAllTestSuite(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/testsuite/findallbycategory?category=${category}`, { headers, responseType: 'text' }); 
  }

  downloadalltestsuitexmlZip(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/testsuite/downloadalltestsuitexml?category=${category}`, { headers, responseType: 'blob' })
  }

  downloadTestSuiteXML(testsuite:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/testsuite/downloadtestsuitexml?testSuite=${testsuite}`, { headers, responseType: 'blob' })
  }

  downloadTestSuiteXLSX(testsuite:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/testsuite/downloadtestcases?testSuite=${testsuite}`, { headers, responseType: 'blob' })
  }
  deleteTestSuite(id:any){
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/testsuite/delete/${id}`, { headers, responseType: 'text' }); 
  }

  uploadTestSuiteXML(file:File): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    const formData: FormData = new FormData();
    formData.append('testSuite', file, file.name);
    return this.http.post(`${apiUrl}api/v1/testsuite/uploadtestsuitexml`, formData, { headers, responseType: 'text' });
  }

  updateTestSuite(data:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
   return this.http.post(`${apiUrl}api/v1/testsuite/update`,data,  { headers,responseType: 'text'  });
  
  }



}
