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
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../auth/auth.service';
import { interval, Observable, switchMap } from 'rxjs';


const apiUrl: string = GlobalConstants.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class ExecutionService {

  constructor(private http: HttpClient,private authService: AuthService) { }

  getAllexecution(category: any,page: number, size: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionsByCategory?category=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers, responseType: 'text' });
  }

  getDeviceStatus(category: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/device/getalldevicestatus?category=${category}`, { headers, responseType: 'text' });
  }

  toggleThunderEnabled(deviceIp:any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/device/toggleThunderEnabledStatus?deviceIp=${deviceIp}`, { headers, responseType: 'text' });
  }
  
  getDeviceByCategory(category:string,isThunderEnabled:boolean): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/device/getdevicebycategoryandthunderstatus?category=${category}&isThunderEnabled=${isThunderEnabled}`, { headers, responseType: 'text' });
  }
  
  getscriptByCategory(category:string,isThunderEnabled:boolean): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/getListofScriptByCategory?category=${category}&isThunderEnabled=${isThunderEnabled}`, { headers, responseType: 'text' });
  }
  gettestSuiteByCategory(category:string,isThunderEnabled:boolean): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/testsuite/getListofTestSuiteByCategory?category=${category}&isThunderEnabled=${isThunderEnabled}`, { headers, responseType: 'text' });
  }
  geExecutionName(data:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/getExecutionName`,data, { headers, responseType: 'text' });
  }

  executioTrigger(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/trigger`,data, { headers, responseType: 'text' });
  }

  resultDetails(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionDetails/${id}`, { headers, responseType: 'text' });
  }

  scriptResultDetails(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionResult?execResultId=${id}`, { headers, responseType: 'text' });
  }
  schedularExecution(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/executionScheduler/create`,data, { headers, responseType: 'text' });
  }

  getAllexecutionScheduler(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/executionScheduler/getAll?category=${category}`,{ headers, responseType: 'text' });
  }

  getlistofUsers(): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getusers`, { headers, responseType: 'text' });
  }
 
  getAllExecutionByDevice(SearchString: any,category: any,page: number, size: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionsByDevice/${SearchString}?categoryName=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers, responseType: 'text' });
  }
 
  getAllExecutionByScript(SearchString: any,category: any,page: number, size: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionsByScriptTestsuite/${SearchString}?categoryName=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers, responseType: 'text' });
  }
  getAllExecutionByUser(userName: any,category: any,page: number, size: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionsByUsername/${userName}?categoryName=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers, responseType: 'text' });
  }
  deleteExecutions(data:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/deletelistofexecutions`,data,{ headers, responseType: 'text' });
  }

  rerunOnFailure(id:string,user:string): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/rerunFailedScript?execId=${id}&user=${user}`,{},{ headers, responseType: 'text' });
  }

  repeatExecution(id:string,user:string): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/repeatExecution?execId=${id}&user=${user}`,{},{ headers, responseType: 'text' });
  }

  modulewiseSummary(id:string): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getModulewiseExecutionSummary?executionId=${id}`,{ headers, responseType: 'text' });
  }

  getLiveLogs(data:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionLogs?executionResultID=${data}`,{ headers, responseType: 'text' });
  }
 
  getDeviceLogs(data:any):  Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getDeviceLogFileNames?executionResultId=${data}`,{ headers, responseType: 'text' });
  }

  getCrashLogs(data:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getCrashLogFileNames?executionResultId=${data}`, { headers, responseType: 'text' });
  }
  downloadLogFile(executioResultId:any, logFileName:any){
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/downloadDeviceLogFile?executionResId=${executioResultId}&fileName=${logFileName}`, { headers, responseType: 'blob' })
  }
  downloadCrashLogFile(executioResultId:any, logFileName:any){
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/downloadCrashLogFile?executionResId=${executioResultId}&fileName=${logFileName}`, { headers, responseType: 'blob' })
  }
  deleteScheduleExe(id:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/executionScheduler/delete?executionScueduleID=${id}`,{ headers, responseType: 'text' });
  }

  datewiseDeleteExe(fromdate:any,toDate:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}execution/deletebydaterange?fromDate=${fromdate}&toDate=${toDate}`, { headers, responseType: 'text' }); 
  }

  getAllExecutionByName(SearchString: any,category: any,page: number, size: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionsByExecutionName/${SearchString}?categoryName=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers, responseType: 'text' });
  }

  getDefectTypes(): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getAnalysisDefectTypes`, { headers, responseType: 'text' });
  }

  saveAnalysisResult(resultId:string, data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/analysis/saveAnalysisResult?executionResultID=${resultId}`, data, { headers, responseType: 'text' });
  }

  getModulewiseAnalysisSummary(resultId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getModulewiseAnalysisSummary?executionID=${resultId}`,  { headers, responseType: 'text' });
  }
  
  getAnalysisResult(resultId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getAnalysisResult?executionResultID=${resultId}`,  { headers, responseType: 'text' });
  }

  abortExecution(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/abortexecution?execId=${exeId}`,{}, { headers, responseType: 'text' });
  }
  excelReportConsolidated(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/${exeId}/download-excel`, { headers, responseType: 'blob' });
  }
  rawExcelReport(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/raw/${exeId}`, { headers, responseType: 'blob' });
  }
  XMLReport(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/${exeId}/XMLReport`, { headers, responseType: 'blob' });
  }
  resultsZIP(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/${exeId}/results-zip`, { headers, responseType: 'blob' });
  }
  failedResultsZIP(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/${exeId}/failed-results-zip`, { headers, responseType: 'blob' });
  }
}
