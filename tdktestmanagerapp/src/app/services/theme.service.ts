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
import { effect, Injectable, Signal, signal, WritableSignal } from '@angular/core';
import { GlobalConstants } from '../utility/global-constants';
import { BehaviorSubject, catchError, firstValueFrom, Observable, of, tap } from 'rxjs';
import { AuthService } from '../auth/auth.service';

const apiUrl: string = GlobalConstants.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class ThemeService {

  userloggedIn:any;
  private currentThemeSubject: BehaviorSubject<string> = new BehaviorSubject<string>(this.getInitialTheme());
  public currentTheme: Observable<string> = this.currentThemeSubject.asObservable();

  constructor(private http: HttpClient,private authService: AuthService) {
    this.userloggedIn = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
   }

  getInitialTheme(): string {
      const savedTheme = localStorage.getItem('theme');
      return savedTheme ? savedTheme : 'LIGHT'; 
  }

  themeUpdateService(userId:any, theme:any): void{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    
    localStorage.setItem('theme', theme);
     this.http.put(`${apiUrl}api/v1/users/settheme?userId=${userId}&theme=${theme}`,null ,{ headers, responseType: 'text' }).subscribe(res=>{
      console.log('Theme saved to API:', res);
     })
     this.currentThemeSubject.next(theme);
  }


  getTheme(userId:any): void{
    const headers = new HttpHeaders({
      'Authorization': this.authService.getApiToken()
    });
    this.http.get(`${apiUrl}api/v1/users/gettheme?userId=${userId}`,{ headers, responseType: 'text' })
    .pipe(
      catchError(() => {
        console.log('Error fetching theme from API, defaulting to light');
        return of('LIGHT'); 
      })
    ).subscribe(response => {
      let theme = response;
      this.setTheme(theme); 
    });
  }
  setTheme(theme: string): void {
    localStorage.setItem('theme', theme);
    this.currentThemeSubject.next(theme);
    this.applyTheme(theme); 
  }
  applyTheme(theme: string): void {
    if (theme === 'DARK') {
      document.body.classList.add('dark');
      document.body.classList.remove('light');
    } else {
      document.body.classList.add('light');
      document.body.classList.remove('dark');
    }
  }
}
