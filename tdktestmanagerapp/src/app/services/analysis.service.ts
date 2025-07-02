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
import { AuthService } from '../auth/auth.service';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root',
})
export class AnalysisService {
  constructor(private http: HttpClient, private authService: AuthService,
    @Inject('APP_CONFIG') private config: any
  ) {}

  getcombinedByFilter(details: any): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.post(
      `${this.config.apiUrl}execution/getExecutionDetailsByFilter`,
      details,
      { headers }
    );
  }

  combinnedReportGenerate(data: any): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.post(`${this.config.apiUrl}execution/combinedExcel`, data, {
      headers,
      responseType: 'blob',
    });
  }

  compReportGenerate(execId: string, data: any): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.post(
      `${this.config.apiUrl}execution/comparisonExcel?baseExecId=${execId}`,
      data,
      {
        headers,
        responseType: 'blob',
      }
    );
  }

  getProjectNames(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getListOfProjectIDs?category=${category}`, {
      headers
    });
  }

  getPriorities(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getPriorities?category=${category}`, {
      headers
    });
  }

  listOfLabels(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getListOfLabels?category=${category}`, {
      headers
    });
  }

  getReleaseVersions(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getReleaseVersions?category=${category}`, {
      headers
    });
  }

  getHardware(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getHardwareConfiguration?category=${category}`, {
      headers
    });
  }
  ticketDetails(exeId:string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getDetailsForPopulatingTicketDetails?execResultID=${exeId}`, {
      headers
  });
  }
  getImpactedPlatforms(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getImpactedPlatforms?category=${category}`, {
      headers
    });
  }
  getFixedInVersions(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getFixedInVersions?category=${category}`, {
      headers
    });
  }

  getRDKVersions(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getRDKVersions?category=${category}`, {
      headers
    });
  }

  getSeverities(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getSeverities?category=${category}`, {
      headers
    });
  }

  getComponentsImpacted(category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getComponentsImpacted?category=${category}`, {
      headers
    });
  }

  setpstoReproduce(scriptName:string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getStepsToReproduce?scriptName=${scriptName}`, {
      headers,
      responseType: 'text',
    });
  }
  isPlatform(prjectId:string ,category: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/isPlatformProjectID?projectID=${prjectId}&category=${category}`, {
      headers
    });
  }

  createJira(data:any): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.post(`${this.config.apiUrl}api/v1/analysis/createJiraTicket`, data ,{
      headers
    });
  }
  getTicketDetaisFromJira(exeId:string, projectname:string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: this.authService.getApiToken(),
    });
    return this.http.get(`${this.config.apiUrl}api/v1/analysis/getTicketDetaisFromJira?executionResultID=${exeId}&projectName=${projectname}`, {
      headers
    });
  }

  updateJiraTicket(data:any): Observable<any> {
  const headers = new HttpHeaders({
    Authorization: this.authService.getApiToken(),
  });
  return this.http.post(`${this.config.apiUrl}api/v1/analysis/updateJiraTicket`, data ,{
    headers
  });
}

isJiraAutomation():Observable<any>{
  const headers = new HttpHeaders({
    'Authorization': this.authService.getApiToken()
  });
  return this.http.get(`${this.config.apiUrl}api/v1/analysis/isJiraAutomationImplemented`, { headers});
 }
  comparisonExcelByNames(baseExecutionName: string, comparisonExecutionNames: string[]): Observable<any> {
    const headers = new HttpHeaders({
        Authorization: this.authService.getApiToken(),
    });

    // Construct the API endpoint with baseExecName as a query parameter
    const url = `${this.config.apiUrl}execution/comparisonExcelByNames?baseExecName=${baseExecutionName}`;

    // Send executionNames in the request body
    return this.http.post(url, comparisonExecutionNames, {
        headers,
        responseType: 'blob', // Expecting a file (Excel) as the response
    });
}
}
