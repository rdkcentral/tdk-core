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
export class DeviceService {

  deviceCategory!: string ;
  fileName!: string;
  private storageKey = 'streamData';
  typeOfboxtypeDropdown!:string;

  constructor(private http: HttpClient, private authService: AuthService) { }
    
    isBoxtypeGateway(boxtype:any):Observable<any>{
      const headers = new HttpHeaders({
        'Authorization': this.authService.getApiToken()
      });
      return this.http.get(`${apiUrl}api/v1/boxtype/istheboxtypegateway?boxType=${boxtype}`, { headers, responseType: 'text' });
  
    }

    findallbyCategory(category:any):Observable<any>{
      const headers = new HttpHeaders({
        'Authorization': this.authService.getApiToken()
      });
      return this.http.get(`${apiUrl}api/v1/device/findallbycategory?category=${category}`, { headers, responseType: 'text' });
  
    }

    createDevice(data:any):Observable<any>{
      const headers = new HttpHeaders({
        'Authorization': this.authService.getApiToken()
      });
      return this.http.post(`${apiUrl}api/v1/device/create`, data, { headers, responseType: 'text' })
    }
    
    getlistofGatewayDevices(category:any):Observable<any>{
      const headers = new HttpHeaders({
        'Authorization': this.authService.getApiToken()
      });
      return this.http.get(`${apiUrl}api/v1/device/getlistofgatewaydevices?category=${category}`, { headers, responseType: 'text' });
    }

    getStreamsForDeviceForUpdate(id:any):Observable<any>{
      const headers = new HttpHeaders({
        'Authorization': this.authService.getApiToken()
      });
      const streaminDataTable = localStorage.getItem(this.storageKey);
      if(streaminDataTable){
        return new Observable(observer =>{
          observer.next(JSON.parse(streaminDataTable));
          observer.complete();
        })
      }
      return this.http.get(`${apiUrl}api/v1/device/getStreamsForDevice/${id}`, { headers, responseType: 'text' })
    }

    saveStreamingData(data:any):void{
      localStorage.setItem(this.storageKey,JSON.stringify(data))
    }

    updateDevice(data:any):Observable<any>{
      const headers = new HttpHeaders({
        'Authorization': this.authService.getApiToken()
      });
      return this.http.put(`${apiUrl}api/v1/device/update`, data, { headers, responseType: 'text' })
    }

    deleteDevice(id:any): Observable<any>{
      const headers = new HttpHeaders({
        'Authorization': this.authService.getApiToken()
      });
      return this.http.delete(`${apiUrl}api/v1/device/deleteDeviceById/${id}`, { headers, responseType: 'text' });
    }

    downloadDevice(name:any): Observable<any>{
      const headers = new HttpHeaders({
        'Authorization': this.authService.getApiToken()
      });
      return this.http.get(`${apiUrl}api/v1/device/downloadXML/${name}`, { headers, responseType: 'blob' })
    }


    uploadXMLFile(file: File): Observable<any> {
      const headers = new HttpHeaders({
        'Authorization': this.authService.getApiToken()
      });
      const formData: FormData = new FormData();
      formData.append('file', file, file.name);
   
      return this.http.post(`${apiUrl}api/v1/device/uploadDeviceXML`, formData,{ headers, responseType: 'text' });
    }

  downloadDeviceConfigFile(boxname:string, boxtype:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/device/downloadDeviceConfigFile?boxName=${boxname}&boxType=${boxtype}`,{ headers, responseType: 'blob', observe:'response' }).pipe(
      map((response:HttpResponse<Blob>)=>{
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'device.config';
        if(contentDisposition){
          const matches = /filename="([^"]*)"/.exec(contentDisposition);
          if(matches && matches[1]){
            filename = matches[1];
          }
        }
        const status = {
          ...response.body,
          statusCode: response.status
        }
        return {filename, content:response.body,status}
      })
    )
    
  }

  downloadDeviceByCategory(category:string):void{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
     this.http.get(`${apiUrl}api/v1/device/downloadDevicesByCategory/${category}`,{ headers, responseType: 'blob' }).subscribe(blob =>{
      saveAs(blob, `device_${category}.zip`);
    });
  }
  uploadConfigFile(file: File): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    const formData: FormData = new FormData();
    formData.append('uploadFile', file, file.name);
    return this.http.post(`${apiUrl}api/v1/device/uploadDeviceConfigFile`, formData,{ headers, responseType: 'text' });
  }

  deleteDeviceConfigFile(deviceConfigFileName:any){
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.delete(`${apiUrl}api/v1/device/deleteDeviceConfigFile?deviceConfigFileName=${deviceConfigFileName}`, { headers, responseType: 'text' });
  }
   
  streamingTemplateList():Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/streamingdetailstemplate/gettemplatelist`, { headers, responseType: 'text' })
  }
  
  streamingDetailsByTemplate(templateName:string):Observable<any>{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    return this.http.get(`${apiUrl}api/v1/streamingdetailstemplate/getstreamingdetailsbytemplatename?templateName=${templateName}`, { headers, responseType: 'text' })
  }

}
