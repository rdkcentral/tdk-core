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

  /**
   * Represents the logged in user.
   */
  loggedInUser: any = {};
  isChecked = false;
  constructor(private loginService: LoginService, private router: Router,
    private service: AuthService, public themeService: ThemeService
  ) { }

  /**
   * Initializes the component.
   */
  ngOnInit(): void {
    this.loggedInUser = this.loginService.getAuthenticatedUser();
    if(JSON.parse(localStorage.getItem('theme')||'') === 'dark'){
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
    this.router.navigate(['/']);
    localStorage.removeItem('theme');
    const theme = this.themeService.selectedTheme;
    if (theme === "dark") {
      this.isChecked = true;
    }else {
      this.isChecked = false;
    }
  }

  /**
   * Navigates to a specific page.
   */
  navigateToPage() {
    this.service.selectedConfigVal = 'RDKV';
  }
  navigateToScript(){
    this.service.selectedCategory = 'RDKV';
    localStorage.removeItem('scriptCategory');
  }
  toggleTheme(){
    this.themeService.selectedTheme = this.themeService.themeSignal();
    this.themeService.updateTheme();
    this.isChecked = !this.isChecked;
    if(this.isChecked){
      this.isChecked = true;
      localStorage.setItem('theme', 'dark');
    }else{
      this.isChecked = false;
      localStorage.setItem('theme', 'light');
    }
  }
}
