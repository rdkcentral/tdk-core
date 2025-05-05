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
import { AuthService } from '../auth/auth.service';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { GlobalConstants } from '../utility/global-constants';
import { BehaviorSubject, map, Observable, of } from 'rxjs';
import { saveAs } from 'file-saver';

const apiUrl: string = GlobalConstants.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class RdkService {

  constructor(private http: HttpClient, private authService: AuthService) { }

  uploadConfigFile(file: File): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    const formData: FormData = new FormData();
    formData.append('pythonFile', file, file.name);
    return this.http.post(`${apiUrl}api/v1/rdkcertification/create`, formData, { headers });
  }

  getallRdkCertifications(): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/rdkcertification/getall`, { headers});

  }

  downloadConfig(name: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/rdkcertification/download?fileName=${name}`, { headers, responseType: 'blob', observe: 'response' }).pipe(
      map((response: HttpResponse<Blob>) => {
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'script.py';
        if (contentDisposition) {
          const matches = /filename="([^"]*)"/.exec(contentDisposition);
          if (matches && matches[1]) {
            filename = matches[1];
          }
        }
        const status = {
          ...response.body,
          statusCode: response.status
        }
        return { filename, content: response.body, status }
      })
    )

  }

  scriptTemplate(name: string) {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/getScriptTemplate?primitiveTestName=${name}`, { headers, responseType: 'text' })
  }

  createScript(scriptFile: File): Observable<any> {
    const formData = new FormData();
    formData.append('pythonFile', scriptFile);
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/rdkcertification/create`, formData, { headers});
  }
  updateScript(scriptFile: File): Observable<any> {
    const formData = new FormData();
    formData.append('pythonFile', scriptFile);
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/rdkcertification/update`, formData, { headers });
  }
  getFileContent(fileName: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/rdkcertification/getconfigfilecontent?fileName=${fileName}`, { headers, responseType: 'blob', observe: 'response' }).pipe(
      map((response: HttpResponse<Blob>) => {
        const status = {
          ...response.body,
          statusCode: response.status
        }
        return { content: response.body, status }
      })
    )

  }
  deleteRdkCertification(name: any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/rdkcertification/delete?fileName=${name}`, { headers });
  }
}