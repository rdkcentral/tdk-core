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
import { AuthService } from '../auth/auth.service';
import { Observable } from 'rxjs';
import { GlobalConstants } from '../utility/global-constants';
import { saveAs } from 'file-saver';
const apiUrl: string = GlobalConstants.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class ModulesService {

  constructor(private http: HttpClient, private authService: AuthService) { }

  getAllTestGroups():Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/module/getAllTestGroups`, { headers, responseType: 'text' });
  }

  createModule(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/module/create`, data, { headers, responseType: 'text' })
  }

  findallbyCategory(category:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/module/findAllByCategory/${category}`, { headers, responseType: 'text' });
  }

  updateModule(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.put(`${apiUrl}api/v1/module/update`, data, { headers, responseType: 'text' })
  }

  deleteModule(id:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/module/delete/${id}`, { headers, responseType: 'text' });
  }

  createFunction(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/function/create`, data, { headers, responseType: 'text' });
  }

  functionList(modulename:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/function/findAllByModule/${modulename}`, { headers, responseType: 'text' });
  }

  updateFunction(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.put(`${apiUrl}api/v1/function/update`, data, { headers, responseType: 'text' });
  }

  deleteFunction(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/function/delete/${id}`, { headers, responseType: 'text' });
  }
  getListOfParameterEnums():Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/parameter/getListOfParameterEnums`, { headers, responseType: 'text' });
  }

  createParameter(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/parameter/create`, data, { headers, responseType: 'text' });
  }

 findAllByFunction(functionName:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/parameter/findAllByFunction/${functionName}`, { headers, responseType: 'text' });
  }

  deleteParameter(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/parameter/delete/${id}`, { headers, responseType: 'text' });
  }

  updateParameter(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.put(`${apiUrl}api/v1/parameter/update`, data, { headers, responseType: 'text' });
  }

  downloadModuleByCategory(category:string):void{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
     this.http.get(`${apiUrl}api/v1/module/downloadzip/${category}`,{ headers, responseType: 'blob' }).subscribe(blob =>{
      saveAs(blob, `module_${category}.zip`);
    });
  }
 
  uploadXMLFile(file: File): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);
    return this.http.post(`${apiUrl}api/v1/module/parsexml`, formData,{ headers, responseType: 'text' });
  }
  
  downloadXMLModule(moduleName:any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/module/downloadxml/${moduleName}`, { headers, responseType: 'blob' })

  }

}
