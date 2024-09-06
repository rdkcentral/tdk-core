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
import { Routes } from '@angular/router';
import { LoginComponent } from './login/login/login.component';
import { ForgotPasswordComponent } from './login/forgot-password/forgot-password.component';
import { RegisterComponent } from './login/register/register.component';
import { MainComponent } from './layout/main/main.component';
import { ConfigureComponent } from './pages/configure/configure.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { ChangePasswordComponent } from './login/change-password/change-password.component';
import { UserListComponent } from './pages/user-management/user-list/user-list.component';
import { UserAddComponent } from './pages/user-management/user-add/user-add.component';
import { UserEditComponent } from './pages/user-management/user-edit/user-edit.component';
import { GroupListComponent } from './pages/create-group/group-list/group-list.component';
import { GroupAddComponent } from './pages/create-group/group-add/group-add.component';
import { GroupEditComponent } from './pages/create-group/group-edit/group-edit.component';
import { ListBoxManufacturerComponent } from './pages/box-manufacturer/list-box-manufacturer/list-box-manufacturer.component';
import { CreateBoxManufacturerComponent } from './pages/box-manufacturer/create-box-manufacturer/create-box-manufacturer.component';
import { roleGuard } from './auth/role.guard';
import { EditBoxManufacturerComponent } from './pages/box-manufacturer/edit-box-manufacturer/edit-box-manufacturer.component';
import { ListSocVendorComponent } from './pages/soc-vendor/list-soc-vendor/list-soc-vendor.component';
import { CreateSocVendorComponent } from './pages/soc-vendor/create-soc-vendor/create-soc-vendor.component';
import { EditSocVendorComponent } from './pages/soc-vendor/edit-soc-vendor/edit-soc-vendor.component';
import { ListBoxtypeComponent } from './pages/box-type/list-box-type/list-boxtype.component';
import { CreateBoxtypeComponent } from './pages/box-type/create-box-type/create-boxtype.component';
import { EditBoxTypeComponent } from './pages/box-type/edit-box-type/edit-box-type.component';
import { authGuard } from './auth/auth.guard';
import { DevicesComponent } from './pages/devices/devices.component';
import { DeviceCreateComponent } from './pages/devices/device-create/device-create.component';
import { ListStreamDetailsComponent } from './pages/stream-details/list-stream-details/list-stream-details.component';
import { CreateStreamDetailsComponent } from './pages/stream-details/create-stream-details/create-stream-details.component';
import { CreateRadioStreamDetailsComponent } from './pages/stream-details/create-radio-stream-details/create-radio-stream-details.component';
import { EditStreamDetailsComponent } from './pages/stream-details/edit-stream-details/edit-stream-details.component';
import { EditRadioStreamDetailsComponent } from './pages/stream-details/edit-radio-stream-details/edit-radio-stream-details.component';
import { StreamingtemplatesListComponent } from './pages/streaming-templates/streamingtemplates-list/streamingtemplates-list.component';
import { StreamingtemplatesCreateComponent } from './pages/streaming-templates/streamingtemplates-create/streamingtemplates-create.component';
import { StreamingtemplatesEditComponent } from './pages/streaming-templates/streamingtemplates-edit/streamingtemplates-edit.component';
import { DeviceEditComponent } from './pages/devices/device-edit/device-edit.component';
import { ModulesListComponent } from './pages/modules/modules-list/modules-list.component';
import { ParameterListComponent } from './pages/modules/parameter-list/parameter-list.component';
import { FunctionListComponent } from './pages/modules/function-list/function-list.component';
import { ModulesCreateComponent } from './pages/modules/modules-create/modules-create.component';
import { FunctionCreateComponent } from './pages/modules/function-create/function-create.component';
import { ParameterCreateComponent } from './pages/modules/parameter-create/parameter-create.component';
import { ListScriptTagComponent } from './pages/script-tag/list-script-tag/list-script-tag.component';
import { CreateScriptTagComponent } from './pages/script-tag/create-script-tag/create-script-tag.component';
import { EditScriptTagComponent } from './pages/script-tag/edit-script-tag/edit-script-tag.component';
import { CreateRdkVersionsComponent } from './pages/rdk-versions/create-rdk-versions/create-rdk-versions.component';
import { ListRdkVersionsComponent } from './pages/rdk-versions/list-rdk-versions/list-rdk-versions.component';
import { EditRdkVersionsComponent } from './pages/rdk-versions/edit-rdk-versions/edit-rdk-versions.component';
import { ListPrimitiveTestComponent } from './pages/primitive-test/list-primitive-test/list-primitive-test.component';
import { CreatePrimitiveTestComponent } from './pages/primitive-test/create-primitive-test/create-primitive-test.component';
import { ModulesEditComponent } from './pages/modules/modules-edit/modules-edit.component';
import { ModulesViewComponent } from './pages/modules/modules-view/modules-view.component';
import { FunctionEditComponent } from './pages/modules/function-edit/function-edit.component';
import { FunctionViewComponent } from './pages/modules/function-view/function-view.component';
import { ParameterEditComponent } from './pages/modules/parameter-edit/parameter-edit.component';
import { ParameterViewComponent } from './pages/modules/parameter-view/parameter-view.component';
import { ScriptListComponent } from './pages/script/script-list/script-list.component';
import { CreateScriptsComponent } from './pages/script/create-scripts/create-scripts.component';
import { EditPrimitiveTestComponent } from './pages/primitive-test/edit-primitive-test/edit-primitive-test.component';

export const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'login', title: 'Login', component: LoginComponent },
    { path: 'register', title: 'Register', component: RegisterComponent },
    { path: 'forgot-password', title: 'Forgot-password', component: ForgotPasswordComponent },
    { path: 'change-password', title: 'Change-password', component: ChangePasswordComponent, canActivate: [authGuard] },
    {
        path: '',
        component: MainComponent,
        canActivate: [authGuard],
        children: [
            { path: 'dashboard', title: 'Dashboard', component: DashboardComponent },
            { path: 'configure', title: 'Configure', component: ConfigureComponent },
            { path: 'configure/user-management', title: 'UserManagement', component: UserListComponent, data: { role: ['admin'] }, canActivate: [roleGuard] },
            { path: 'configure/create-user', title: 'Create User', component: UserAddComponent },
            { path: 'configure/edit-user', title: 'Edit User', component: UserEditComponent },
            { path: 'configure/create-group', title: 'Group List', component: GroupListComponent, data: { role: ['admin'] }, canActivate: [roleGuard] },
            { path: 'configure/group-add', title: 'Group Add', component: GroupAddComponent },
            { path: 'configure/group-edit/:id', title: 'Group Edit', component: GroupEditComponent },
            { path: 'configure/list-boxManufacturer', title: 'BoxManufacturer', component: ListBoxManufacturerComponent },
            { path: 'configure/create-boxManufacturer', title: 'BoxManufacturer Add', component: CreateBoxManufacturerComponent },
            { path: 'configure/boxManufacturer-edit', title: 'BoxManufacturer Edit', component: EditBoxManufacturerComponent },
            { path: 'configure/list-socvendor', title: 'SocVendor', component: ListSocVendorComponent },
            { path: 'configure/create-socvendor', title: 'SocVendor Add', component: CreateSocVendorComponent },
            { path: 'configure/edit-socvendor', title: 'SocVendor Edit', component: EditSocVendorComponent },
            { path: 'configure/list-boxtype', title: 'BoxType', component: ListBoxtypeComponent },
            { path: 'configure/create-boxtype', title: 'BoxType Add', component: CreateBoxtypeComponent },
            { path: 'configure/edit-boxtype', title: 'BoxType Edit', component: EditBoxTypeComponent },
            { path: 'configure/list-streamdetails', title: 'StreamDetails', component: ListStreamDetailsComponent },
            { path: 'configure/create-streamdetails', title: 'StreamDetails Add', component: CreateStreamDetailsComponent },
            { path: 'configure/create-radiostreamdetails', title: 'RadioStreamDetails Add', component: CreateRadioStreamDetailsComponent },
            { path: 'cofigure/edit-streamdetails', title: 'StreamDetails Edit', component: EditStreamDetailsComponent },
            { path: 'configure/edit-radiostreamdetails', title: 'RadioStreamDetails Edit', component: EditRadioStreamDetailsComponent },
            { path: 'devices', title: 'Devices', component: DevicesComponent },
            { path: 'devices/device-create', title: 'Device Create', component: DeviceCreateComponent },
            { path: 'devices/device-edit', title: 'Device Edit', component: DeviceEditComponent },
            { path: 'configure/streamingtemplates-list', title: 'StreamingTemplates', component: StreamingtemplatesListComponent },
            { path: 'configure/streamingtemplates-create', title: 'StreamingTemplatesCreate', component: StreamingtemplatesCreateComponent },
            { path: 'configure/streamingtemplates-edit', title: 'StreamingTemplatesEdit', component: StreamingtemplatesEditComponent },
            { path: 'configure/modules-list', title: 'Modules', component: ModulesListComponent },
            {path: 'configure/function-list', title: 'Function', component:FunctionListComponent},
            {path: 'configure/parameter-list', title: 'Parameter', component:ParameterListComponent},
            {path: 'configure/modules-create', title: 'Module Create', component:ModulesCreateComponent},
            {path: 'configure/modules-edit', title: 'Module Edit', component:ModulesEditComponent},
            {path: 'configure/modules-view', title: 'Module View', component:ModulesViewComponent},
            {path: 'configure/function-create', title: 'Function Create', component:FunctionCreateComponent},
            {path: 'configure/function-edit', title: 'Function Edit', component:FunctionEditComponent},
            {path: 'configure/function-view', title: 'Function View', component:FunctionViewComponent},
            {path: 'configure/parmeter-create', title: 'Parmeter Create', component:ParameterCreateComponent},
            {path: 'configure/parameter-edit', title: 'Parmeter Edit', component:ParameterEditComponent},
            {path: 'configure/parameter-view', title: 'Parmeter View', component:ParameterViewComponent},
            {path: 'configure/scripttag-list', title: 'Script Tags ', component:ListScriptTagComponent},
            {path: 'configure/scripttag-create', title: 'ScriptTags Create', component: CreateScriptTagComponent},
            {path: 'configure/scripttag-edit', title: 'ScriptTags Edit', component: EditScriptTagComponent},
            {path: 'configure/list-rdkversions',title:'List RDK Versions',component:ListRdkVersionsComponent},
            {path: 'configure/create-rdkversions',title:'Create RDK Versions',component:CreateRdkVersionsComponent},
            {path: 'configure/edit-rdkversions',title:'Edit RDK Versions',component:EditRdkVersionsComponent},
            {path: 'configure/list-primitivetest',title:'List PrimitiveTest',component:ListPrimitiveTestComponent},
            // {path:'configure/create-primitivetest', title:'Create PrimitiveTest', component:CreatePrimitiveTestComponent},
            {path: 'configure/edit-primitivetest',title:'Edit PrimitiveTest',component:EditPrimitiveTestComponent},
            {path:'configure/create-primitivetest', title:'Create PrimitiveTest', component:CreatePrimitiveTestComponent},
            {path:'script', title:'Script', component:ScriptListComponent},
            {path:'script/create-scripts', title:'Cretae Script', component:CreateScriptsComponent}
        ]
    }
];
