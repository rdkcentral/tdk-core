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

const apiUrl: string = GlobalConstants.apiUrl;

@Injectable({
  providedIn: 'root',
})
export class AnalysisService {
  constructor(private http: HttpClient, private authService: AuthService) {}

  getcombinedByFilter(details: any): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.post(
      `${apiUrl}execution/getExecutionDetailsByFilter`,
      details,
      { headers, responseType: 'text' }
    );
  }

  combinnedReportGenerate(data: any): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.post(`${apiUrl}execution/combined-excel`, data, {
      headers,
      responseType: 'blob',
    });
  }

  compReportGenerate(execId: string, data: any): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.post(
      `${apiUrl}execution/comparison-excel?baseExecId=${execId}`,
      data,
      {
        headers,
        responseType: 'blob',
      }
    );
  }

  getProjectNames(): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getListOfProjectIDs`, {
      headers,
      responseType: 'text',
    });
  }

  getPriorities(): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getPriorities`, {
      headers,
      responseType: 'text',
    });
  }

  ListOfLabels(): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getListOfLabels`, {
      headers,
      responseType: 'text',
    });
  }

  getReleaseVersions(): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getReleaseVersions`, {
      headers,
      responseType: 'text',
    });
  }

  getHardware(): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getHardwareConfiguration`, {
      headers,
      responseType: 'text',
    });
  }
  ticketDetails(exeId:string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getDetailsForPopulatingTicketDetails?execResultID=${exeId}`, {
      headers,
      responseType: 'text',
    });
  }
  getImpactedPlatforms(): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getImpactedPlatforms`, {
      headers,
      responseType: 'text',
    });
  }
  getFixedInVersions(): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getFixedInVersions`, {
      headers,
      responseType: 'text',
    });
  }
  getSeverities(): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getSeverities`, {
      headers,
      responseType: 'text',
    });
  }

  getComponentsImpacted(): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getComponentsImpacted`, {
      headers,
      responseType: 'text',
    });
  }

  setpstoReproduce(scriptName:string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getStepsToReproduce?scriptName=${scriptName}`, {
      headers,
      responseType: 'text',
    });
  }
  isPlatform(prjectId:string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/isPlatformProjectID?projectID=${prjectId}`, {
      headers,
      responseType: 'text',
    });
  }
  createJira(data:any): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.post(`${apiUrl}api/v1/analysis/createJiraTicket`, data ,{
      headers,
      responseType: 'text',
    });
  }
  getTicketDetaisFromJira(exeId:string, projectname:string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getTicketDetaisFromJira?executionResultID=${exeId}&projectName=${projectname}`, {
      headers,
      responseType: 'text',
    });
  }

  updateJiraTicket(data:any): Observable<any> {
  const headers = new HttpHeaders({
    Authorization: this.authService.getApiToken(),
  });
  return this.http.post(`${apiUrl}api/v1/analysis/updateJiraTicket`, data ,{
    headers,
    responseType: 'text',
  });
}

isJiraAutomation():Observable<any>{
  const headers = new HttpHeaders({
    'Authorization': this.authService.getApiToken()
  });
  return this.http.get(`${apiUrl}api/v1/analysis/isJiraAutomationImplemented`, { headers, responseType: 'text' });
 }

 
}
