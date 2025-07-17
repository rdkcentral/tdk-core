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
import { NavigationEnd, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
/**
 * Provides authentication-related functionality for the application, including:
 * - Managing authentication tokens and user privileges in local storage.
 * - Tracking navigation history (previous and current URLs).
 * - Checking token expiration and login status.
 * 
 * This service is intended to be injected into Angular components and services
 * that require authentication state or navigation tracking.
 */
export class AuthService {

  /**
   * The selected configuration value.
   */
  selectedConfigVal!: string ;
  /**
   * The selected category.
   */
  selectedCategory! : string ;
  /**
   * The selected category for the video.
   */
  showSelectedCategory : string = 'Video' ;
  /**
   * The selected video category.
   */
  videoCategoryOnly!: string;
  /**
   * The selected category for the script.
   */
  categoryChange!:string;
  /**
   * The current route.
   */
  currentRoute: any;

  /**
   * The previous URL.
   */
  previousUrl!: string;

  /**
   * The current URL.
   */
  currentUrl!: string;

  /**
   * The constructor initializes the router and sets up a listener for navigation events.
   * It updates the previous and current URLs based on navigation events.
   * @param router - The Angular Router instance.
   */
  constructor(private router: Router) {
    router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.previousUrl = this.currentUrl;
        this.currentUrl = event.url;
      };
    });
  }

  /**
   * Stores the token in the local storage.
   * @param token - The token to be stored.
   */
  sendToken(token: string) {
    localStorage.setItem("token", token);
  }

  /**
   * Retrieves the token from the local storage.
   * @returns The token.
   */
  getToken() {
    return localStorage.getItem("token");
  }

  /**
   * Retrieves the API token from the local storage.
   * @returns The API token.
   */
  getApiToken() {
    var token = 'bearer ' + localStorage.getItem("token");
    return token;
  }

  /**
   * Stores the privileges in the local storage.
   * @param privileges - The privileges to be stored.
   */
  setPrivileges(privileges: string) {
    localStorage.setItem("privileges", privileges);
  }

  /**
   * Retrieves the privileges from the local storage.
   * @returns The privileges.
   */
  getPrivileges() {
    var privileges = localStorage.getItem("privileges");
    return privileges;
  }

  /**
   * Checks if the token is expired.
   * @returns True if the token is expired, false otherwise.
   */
  isTokenExpired(): any {
    const token = this.getToken()
    if (!token) return true;
    const decodedToken = JSON.parse(atob(token.split('.')[1]))
    const expirationDate = new Date(decodedToken.exp * 1000)
    if (expirationDate >= new Date()) {
      return true
    } else {
      return false;
    }
  }

  /**
   * Checks if the user is logged in.
   * @returns True if the user is logged in, false otherwise.
   */
  isLoggednIn() {
    return this.getToken() !== null && this.isTokenExpired();
  }
}
