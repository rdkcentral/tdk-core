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
import { Component, OnInit } from '@angular/core';
import { MaterialModule } from '../../material/material.module';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { LoginService } from '../../services/login.service';
import { AuthService } from '../../auth/auth.service';
import { ThemeService } from '../../services/theme.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [MaterialModule, RouterLink, RouterLinkActive],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})

/**
 * Represents the HeaderComponent of the application.
 */
export class HeaderComponent implements OnInit {

  loggedInUser: any = {};
  isChecked = false;
  userloggedIn:any;
  currentTheme: string = 'LIGHT';

  constructor(private loginService: LoginService, private router: Router,private service: AuthService, 
    public themeService: ThemeService) { 
    this.userloggedIn = JSON.parse(localStorage.getItem('loggedinUser') || '{}');
  }

  /**
   * Initializes the component.
   */
  ngOnInit(): void {
    this.loggedInUser = this.loginService.getAuthenticatedUser();
    if(this.userloggedIn.userID){
      this.themeService.getTheme(this.userloggedIn.userID);
    }
    this.themeService.currentTheme.subscribe(theme => {
      this.currentTheme = theme;
      this.applyTheme(theme);
      if(this.currentTheme == 'DARK'){
        this.isChecked = !this.isChecked;
        this.isChecked = true;
      }else{
        this.isChecked = false;
      }
    });
    if(this.currentTheme == 'DARK'){
      this.isChecked = !this.isChecked;
      this.isChecked = true;
    }else{
      this.isChecked = false;
    }
  }
  /**
   * This method is add class and remove class based on theme selection.
   */
  applyTheme(theme: string): void {
    if (theme === 'DARK') {
      document.body.classList.add('dark');
      document.body.classList.remove('light');
    } else {
      document.body.classList.add('light');
      document.body.classList.remove('dark');
    }
  }
  /**
   * This method is toggle themecolor from light to dark and vice-versa.
   */  
  toggleTheme(): void {
    const newTheme = this.currentTheme === 'LIGHT' ? 'DARK' : 'LIGHT';
    this.themeService.themeUpdateService(this.userloggedIn.userID, newTheme);
    if(this.currentTheme == 'DARK'){
      this.isChecked = !this.isChecked;
      this.isChecked = true;
    }else{
      this.isChecked = false;
    }
  }

  /**
   * Logs out the user and navigates to the home page.
   */
  logOut() {
    this.loginService.logoutUser();
    localStorage.removeItem('preferedCategory');
    this.router.navigate(['/']);
  }

  /**
   * Navigates to a specific page.
   */
  navigateToPage() {
    this.service.selectedConfigVal = 'RDKV';
  }
  /**
   * Navigates to a script page.
   */
  navigateToScript(){
    this.service.selectedCategory = 'RDKV';
    localStorage.removeItem('scriptCategory');
  }

}
