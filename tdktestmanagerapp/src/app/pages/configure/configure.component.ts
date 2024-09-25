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
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-configure',
  standalone: true,
  imports: [CommonModule, MaterialModule, RouterLink, RouterLinkActive],
  templateUrl: './configure.component.html',
  styleUrl: './configure.component.css'
})
export class ConfigureComponent implements OnInit {
  rdkvVisible = true;
  rdkbVisible = false;
  rdkcVisible = false;
  privileges!: string | null;

  constructor(private router: Router, private service: AuthService) { }

   /**
   * Handles the checkbox change event.
   * @param val - The value of the checkbox.
   */
  ischecked(val: any): void {
    this.service.selectedConfigVal = 'RDKV'
    if (val === 'RDKB') {
      this.rdkbVisible = true;
      this.rdkvVisible = false;
      this.rdkcVisible = false;
      this.service.selectedConfigVal = 'RDKB'
      this.service.showSelectedCategory = "Broadband"
    } else if (val === 'RDKC') {
      this.rdkcVisible = true;
      this.rdkbVisible = false;
      this.rdkvVisible = false;
      this.service.selectedConfigVal = 'RDKC'
      this.service.showSelectedCategory = "Camera"
    } else {
      this.rdkvVisible = true;
      this.rdkbVisible = false;
      this.rdkcVisible = false;
      this.service.selectedConfigVal = 'RDKV'
      this.service.showSelectedCategory = "Video"
    }
  }

  /**
   * Navigates to the specified route based on the provided value.
   * @param val - The value representing the route to navigate to.
   */
  navigationToUser(val: any):void {
    if (val === 'groups') {
      this.router.navigate(["configure/create-group"]);
    }
    if (val === 'usermanagement') {
      this.router.navigate(["configure/user-management"]);
    }
    if (val === 'boxmanufacturers') {
      this.router.navigate(["configure/list-boxManufacturer"]);
    }
    if (val === 'socvendors') {
      this.router.navigate(["configure/list-socvendor"]);
    }
    if (val === 'boxtype') {
      this.router.navigate(["configure/list-boxtype"]);
    }
    if (val === 'streamingdetails') {
      this.router.navigate(['configure/list-streamdetails']);
    }
    if (val === 'streamingtemplates') {
      this.router.navigate(['configure/streamingtemplates-list']);
    }
    if (val === 'modules') {
      this.router.navigate(['configure/modules-list']);
    }
    if (val === 'scripttags') {
      this.router.navigate(['configure/scripttag-list']);
    }
    if (val === 'rdkversions') {
      this.router.navigate(['configure/list-rdkversions']);
    }
    if (val === 'prmitivetest') {
      this.router.navigate(['configure/list-primitivetest']);
    }
  }

  /**
   * Initializes the component.
   */ 
  ngOnInit(): void {
    this.privileges = this.service.getPrivileges();
  }
}
