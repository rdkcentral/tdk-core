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
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { AuthService } from '../auth/auth.service';
import { interval, map, Observable, switchMap } from 'rxjs';


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
    return this.http.get(`${apiUrl}execution/getExecutionsByCategory?category=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers });
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
    return this.http.get(`${apiUrl}api/v1/device/toggleThunderEnabledStatus?deviceIp=${deviceIp}`, { headers });
  }
  
  getDeviceByCategory(category:string,isThunderEnabled:boolean): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/device/getDeviceByCategoryAndThunderstatus?category=${category}&isThunderEnabled=${isThunderEnabled}`, { headers });
  }
  
  getscriptByCategory(category:string,isThunderEnabled:boolean): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/script/getListofScriptByCategory?category=${category}&isThunderEnabled=${isThunderEnabled}`, { headers});
  }
  gettestSuiteByCategory(category:string,isThunderEnabled:boolean): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/testsuite/getListofTestSuiteByCategory?category=${category}&isThunderEnabled=${isThunderEnabled}`, { headers });
  }
  geExecutionName(data:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/getExecutionName`,data, { headers });
  }

  executioTrigger(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/trigger`,data, { headers });
  }

  resultDetails(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionDetails?id=${id}`, { headers });
  }

  scriptResultDetails(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionResult?execResultId=${id}`, { headers });
  }

  DetailsForHtmlReport(id:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionDetailsForHtmlReport?executionId=${id}`, { headers });
  }

  schedularExecution(data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/executionScheduler/create`,data, { headers});
  }

  getAllexecutionScheduler(category:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/executionScheduler/getAll?category=${category}`,{ headers});
  }

  getlistofUsers(): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getUsers`, { headers });
  }
  getAllExecutionByName(SearchString: any,category: any,page: number, size: number): Observable<any> {
    const headers = new HttpHeaders({
      // 'Content-Type': 'application/json',
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionsByExecutionName?executionName=${SearchString}&categoryName=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers });
  }
  getAllExecutionByDevice(SearchString: any,category: any,page: number, size: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionsByDevice?deviceName=${SearchString}&categoryName=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers });
  }
 
  getAllExecutionByScript(SearchString: any,category: any,page: number, size: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionsByScriptTestsuite?scriptTestSuiteName=${SearchString}&categoryName=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers});
  }
  getAllExecutionByUser(userName: any,category: any,page: number, size: number): Observable<any> {
    const headers = new HttpHeaders({
      
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getExecutionsByUsername?username=${userName}&categoryName=${category}&page=${page}&size=${size}&sortBy=createdDate&sortDir=desc`, { headers });
  }
  deleteExecutions(data:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/deleteListOfExecutions`,data,{ headers });
  }

  rerunOnFailure(id:string,user:string): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/rerunFailedScript?execId=${id}&user=${user}`,{},{ headers});
  }

  repeatExecution(id:string,user:string): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/repeatExecution?execId=${id}&user=${user}`,{},{ headers});
  }

  modulewiseSummary(id:string): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/getModulewiseExecutionSummary?executionId=${id}`,{ headers});
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
    return this.http.get(`${apiUrl}execution/getDeviceLogFileNames?executionResultId=${data}`,{ headers});
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
    return this.http.get(`${apiUrl}api/v1/executionScheduler/delete?executionScueduleID=${id}`,{ headers});
  }

  datewiseDeleteExe(fromdate:any,toDate:any): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}execution/deleteByDateRange?fromDate=${fromdate}&toDate=${toDate}`, { headers }); 
  }



  getDefectTypes(): Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getAnalysisDefectTypes`, { headers});
  }

  saveAnalysisResult(resultId:string, data:any):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}api/v1/analysis/saveAnalysisResult?executionResultID=${resultId}`, data, { headers});
  }

  getModulewiseAnalysisSummary(resultId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getModulewiseAnalysisSummary?executionID=${resultId}`,  { headers });
  }
  
  getAnalysisResult(resultId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/analysis/getAnalysisResult?executionResultID=${resultId}`,  { headers });
  }

  abortExecution(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': this.authService.getApiToken()
    });
    return this.http.post(`${apiUrl}execution/abortExecution?execId=${exeId}`,{}, { headers });
  }
  excelReportConsolidated(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/downloadConsolidatedExcelReport?executionId=${exeId}`, { headers, responseType: 'blob' });
  }
  rawExcelReport(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/rawExcelReport?executionId=${exeId}`, { headers, responseType: 'blob' });
  }
  XMLReport(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/downloadXMLReport?executionId=${exeId}`, { headers, responseType: 'blob' });
  }
  resultsZIP(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/downloadAllResultLogsZip?executionId=${exeId}`, { headers, responseType: 'blob' });
  }
  failedResultsZIP(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/downloadFailedResultLogsZip?executionId=${exeId}`, { headers, responseType: 'blob' });
  }
  isfailedExecution(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/isExecutionResultFailed?executionId=${exeId}`, { headers});
  }

  DownloadScript(exeId:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}execution/downloadScript?executionResId=${exeId}`, { headers, responseType: 'blob', observe: 'response' }).pipe(
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

getExecutionLogsLinks(exeId:string):Observable<any>{
  const headers = new HttpHeaders({
    'Authorization': this.authService.getApiToken()
  });
  return this.http.get(`${apiUrl}execution/getExecutionLogs?executionResultID=${exeId}`, { headers, responseType: 'text' });
}



}
