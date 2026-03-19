##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

import xml.etree.ElementTree as ET
import tdklib
import tdkbDmlModuleList
from time import sleep
import os
import os.path
import json
import dynamicDMLUtility
from datetime import datetime
import tdkutility
import random
import re
from webpaUtility import *

# Global variable to track the test step by the framework
step = 0

# getAllParams_module
# Syntax      : getAllParams_module(module, setup_type, factoryReset, objs, rbusobj, testtype = "get")
# Description : Wrapper function to invoke the L1 tests for each component under a module
#               and collect the total number of DMs tested under each component, test status of the component
#               and and the list of DMs that failed L1 tests
# Parameters  : module - name of the module as listed in tdkbDmlModuleList.py
#               setup_type - the protocol used for conducting the L1 tests
#               factoryReset - whether a factory reset needs to be triggered before commencing tests
#               objs - stub objects - [TR181 and/or sysutil] based on the setup_type; if setup_type = TDK, objs is TR181 object,
#                      if setup_type = WEBPA, objs is list of sysutil & tr181 stub objects
#               rbusobj - the RBUS stub object
#               testtype - type of the L1 test triggered (get, readOnlySet, parameterExistence, writeAccessCompliance,
#                          writeTypeCompliance, AddStaticTableRow, DeleteStaticTableRow, AddDynamicTableRow, DeleteDynamicTableRow
#                          AddAndDeleteDynWritableTableRow, AddAndDeleteWritableTableRow)
# Return Value: moduleStatus - SUCCESS/FAILURE status of the module testing. If any component under a module reports
#               a FAILURE status, failedParams_module will be FAILURE
#               failedParams_module - - the list of DMs that failed the test

def getAllParams_module(module, setup_type, factoryReset, objs, rbusobj, testtype = "get"):
    preRequisiteStatus = "SUCCESS"
    failedParams_module = []
    failedParams_component = []
    moduleStatus = "SUCCESS"
    componentStatus = "SUCCESS"
    total_component = 0
    total = 0

    if testtype == "get":
        total_component = {'total' : 0, 'typeTestCount' : 0, 'valueCheckCount' : 0}
        total_typeChecked = 0
        total_valueChecked = 0

    if module != {}:
        # Find the list of components under the module

        # Check pre-requisites based on the test setup type -
        if setup_type == "WEBPA":
            # Chose the required stub object to check pre-requisites
            obj = objs[0]
            tdkTestObj, preRequisiteStatus = webpaPreRequisite(obj)

        if preRequisiteStatus == "SUCCESS":
            for component in module:
                failedParams_component, componentStatus, total_component = testParams_component(component, setup_type, factoryReset, objs, rbusobj, testtype)
                failedParams_module.extend(failedParams_component)

                if componentStatus == "FAILURE":
                    moduleStatus = "FAILURE"

                if testtype == "get":
                    total = total + total_component['total']
                    total_typeChecked = total_typeChecked + total_component['typeTestCount']
                    total_valueChecked = total_valueChecked + total_component['valueCheckCount']
                else:
                    total = total + total_component
        else:
            print("\n!!! Test Pre-Requisites failed !!!")
            return failedParams_module, "FAILURE"

    if testtype == "get":
        print("\n---------------Total Parameters tested for Type Compliance : %d---------------\n" %total_typeChecked)
        print("\n---------------Total Parameters tested for GET Value : %d---------------\n" %total_valueChecked)
    elif testtype == "AddStaticTableRow" or testtype == "DeleteStaticTableRow":
        print("\n---------------Total Static Tables tested : %d---------------\n" %total)
    elif testtype == "AddDynamicTableRow" or testtype == "DeleteDynamicTableRow":
        print("\n---------------Total Dynamic Tables tested : %d---------------\n" %total)
    elif testtype == "AddAndDeleteDynWritableTableRow":
        print("\n---------------Total Dynamic Writable Tables tested : %d---------------\n" %total)
    elif testtype == "AddAndDeleteWritableTableRow":
        print("\n---------------Total Writable Tables tested : %d---------------\n" %total)
    else:
        print("\n---------------Total Parameters tested : %d---------------\n" %total)

    if len(failedParams_module) > 0:
        print("\n---------------Total Number of Failures : %d---------------\n" %(len(failedParams_module)))

    return failedParams_module, moduleStatus

# setParams_module
# Syntax      : setParams_module(module, setup_type, tr181Obj, rbusobj, testtype = "L2-set")
# Description : Wrapper function to invoke the L2 SET tests for each component under a module
#               and collect the total number of L2 SET use-cases tested under each component, test status of the component
#               and and the list of DMs that failed L2 tests
# Parameters  : module - name of the module as listed in tdkbDmlModuleList.py
#               setup_type - the protocol used for conducting the L2 tests
#               tr181Obj - the TR181 stub object
#               rbusobj - the RBUS stub object
#               testtype - type of the L2 test triggered (L2-set)
# Return Value: moduleStatus - SUCCESS/FAILURE status of the module testing. If any component under a module reports
#               a FAILURE status, failedParams_module will be FAILURE
#               failedParams_module - the list of DMs that failed the test

def setParams_module(module, setup_type, tr181Obj, rbusobj, testtype = "L2-set"):
    failedParams_module = []
    failedParams_component = []
    moduleStatus = "SUCCESS"
    componentStatus = "SUCCESS"
    total_component = 0
    total = 0

    if module != {}:
        # Find the list of components under the module
        for component in module:
            failedParams_component, componentStatus, total_component = setTestParams_component(component, setup_type, tr181Obj, rbusobj, testtype)
            failedParams_module.extend(failedParams_component)

            if componentStatus == "FAILURE":
                moduleStatus = "FAILURE"

            if testtype == "L2-set":
                total = total + total_component

    if testtype == "L2-set":
        print("\n---------------Total Parameters tested for L2 SET : %d---------------\n" %total)

        print("\n---------------Total Parameters failed : %d---------------\n" %(len(failedParams_module)))

    return failedParams_module, moduleStatus

# testParams_component
# Syntax      : testParams_component(component, setup_type, factoryReset, objs, rbusobj, testtype)
# Description : Function to handle individual device profiles to customize the test. Converts the static configuration file (if any)
#               of a component to a test XML and the dynamic configuration file (if any) to a dynamic XML or a dynamic secondary config
#               after resolving the run-time pre requisites. The function then proceeds to call the test handler function depending
#               on the L1 test type.
# Parameters  : component - name of the component under the specified module as listed in tdkbDmlModuleList.py
#               setup_type - the protocol used for conducting the L1 tests
#               factoryReset - whether a factory reset needs to be triggered before commencing tests
#               objs - stub objects [ TR181 and/or sysutil ] as required by setup_type
#               rbusobj - the RBUS stub object
#               testtype - type of the L1 test triggered
# Return Value: failedParams - the list of DMs that failed the test
#               componentStatus - SUCCESS/FAILURE status of the component testing. If any test step under a component reports
#               a FAILURE status, componentStatus will be FAILURE
#               total - total number of DMs tested under the component

def testParams_component(component, setup_type, factoryReset, objs, rbusobj, testtype):
    failedParams_static = []
    failedParams_dynamic = []
    failedParams = []
    intermediateFiles = []
    total_static = 0
    total_dynamic = 0
    status_static = "SUCCESS"
    status_dynamic = "SUCCESS"
    componentStatus = "SUCCESS"

    if testtype == "get":
        testtypeBanner = "GET VALUES OF ALL NAMESPACES"
        total_static = {'total' : 0, 'typeTestCount' : 0, 'valueCheckCount' : 0}
        total_dynamic = {'total' : 0, 'typeTestCount' : 0, 'valueCheckCount' : 0}
        total = {'total' : 0, 'typeTestCount' : 0, 'valueCheckCount' : 0}
    elif testtype == "readOnlySet":
        testtypeBanner = "SET VALUES FOR ALL READONLY NAMESPACES"
        total = 0
    elif testtype == "parameterExistence":
        testtypeBanner = "PARAMETER EXISTENCE CHECK"
        namespaces = set()
        configPath = ""
        total = 0
    elif testtype == "writeAccessCompliance":
        testtypeBanner = "WRITE ACCESS COMPLIANCE"
        total = 0
    elif testtype == "writeTypeCompliance":
        testtypeBanner = "WRITE TYPE COMPLIANCE"
        total = 0
    elif testtype == "AddStaticTableRow":
        testtypeBanner = "ADD ROW TO STATIC TABLE"
        total = 0
    elif testtype == "DeleteStaticTableRow":
        testtypeBanner = "DELETE ROW FROM STATIC TABLE"
        total = 0
    elif testtype == "AddDynamicTableRow":
        testtypeBanner = "ADD ROW TO DYNAMIC TABLE"
        total = 0
    elif testtype == "DeleteDynamicTableRow":
        testtypeBanner = "DELETE ROW FROM DYNAMIC TABLE"
        total = 0
    elif testtype == "AddAndDeleteDynWritableTableRow":
        testtypeBanner = "ADD AND REMOVE ROW FROM DYNAMIC WRITABLE TABLE"
        total = 0
    elif testtype == "AddAndDeleteWritableTableRow":
        testtypeBanner = "ADD AND REMOVE ROW FROM WRITABLE TABLE"
        total = 0

    # Chose the stub object to drive the test
    if setup_type == "TDK":
        # Both can use TR181 stub object
        testobj = objs
        preReqobj = objs
    elif setup_type == "WEBPA":
        # tset needs to be driven by sysutil object, for pre-requisites TR181 stub object to be used
        testobj = objs[0]
        preReqobj = objs[1]
    # For all testtypes other than table testing
    if "Table" not in testtype:
        # Get the path to static config
        staticConfig = component + "_config.json"
        configPath = os.path.dirname(os.path.realpath(__file__))
        path_to_static_config  = configPath + "/tdkbModuleConfig/" + staticConfig

        # Get the path to Dynamic XML
        xmlName = component + "_Static_TDK.XML"
        xmlPath = os.path.dirname(os.path.realpath(__file__))
        paramListXml = xmlPath + "/tdkbModuleConfig/" + xmlName

        if os.path.exists(path_to_static_config):
            config_type = "static"

            # If the test is not parameterExistence, call the profile handler to customize the test
            if "parameterExistence" not in testtype:
                # Create temporary config file to handle flags
                temp_static_config = dynamicDMLUtility.profileHandler(path_to_static_config, component, rbusobj, config_type)
                if os.path.exists(temp_static_config):
                    # Create the test XML
                    dynamicDMLUtility.create_static_xml(temp_static_config, paramListXml)
                    intermediateFiles.append(temp_static_config)
                intermediateFiles.append(paramListXml)

            # If the test is parameterExistence, call function to get all unique namespaces (till first 2 objects depth, eg: Device.DeviceInfo.) found in the config
            else:
                dynamicDMLUtility.getUniqueNamespaces(path_to_static_config, namespaces)

            # If the test XML is generated, call the XML test handler
            if os.path.exists(paramListXml) :
                print("\n-------------------------------------------------------------------------")
                print(f"{testtypeBanner} IN STATIC XML FOR COMPONENT {component}")
                print("---------------------------------------------------------------------------\n")

                print("The name of param list xml file is ", paramListXml)
                tree = ET.parse(paramListXml)
                paramsRoot = tree.getroot()

                status_static, failedParams_static, total_static = parseXMLAndExecuteTest(paramsRoot, factoryReset, setup_type, testobj, testtype)

            # For parameter existence test, call the config test handler
            elif "parameterExistence" in testtype:
                print("\n-------------------------------------------------------------------------")
                print(f"{testtypeBanner} IN STATIC CONFIG FOR COMPONENT {component}")
                print("---------------------------------------------------------------------------\n")
                expectedresult = "SUCCESS"
                status_static, failedParams_static, total_static = getParameterNames(setup_type, expectedresult, rbusobj, namespaces, path_to_static_config, component, configType="Static")

            # Cleanup
            cleanup(intermediateFiles)
        else:
            print("\n---------------------------------------------------------------------------")
            print(f"-----Static Config not applicable for the component {component}-----")
            print("---------------------------------------------------------------------------\n")

    # Invoke the pre-requisite function of the component to generate the dynamic XML
    pre_req_ret = "FAILURE"
    runtimeConfig = component + "_runtime_config.json"
    configPath = os.path.dirname(os.path.realpath(__file__))
    path_to_runtime_config = configPath + "/tdkbModuleConfig/" + runtimeConfig

    # Get the path to Dynamic XML
    xmlName = component + "_Runtime_TDK.XML"
    xmlPath = os.path.dirname(os.path.realpath(__file__))
    paramListXml = xmlPath + "/tdkbModuleConfig" + "/" + xmlName

    if os.path.exists(path_to_runtime_config):
        with open(path_to_runtime_config, 'rb') as file:
            config_data = json.load(file)
            if config_data:

                if "TableRow" not in testtype:
                    # As config is non-empty
                    print("-------------------------------------------------------------------------")
                    print(f"\nExecuting Pre-Requisites for populating Dynamic parameters\n")

                    # Resolve the table run-time dependencies
                    temp_runtime_config, secondary_config = dynamicDMLUtility.performPreReq(preReqobj, rbusobj, path_to_runtime_config)

                    # Call the profile handler to customize the test acording to device profile
                    if "parameterExistence" not in testtype:
                        config_type = "run_time"
                        dynamicDMLUtility.profileHandler(temp_runtime_config, component, rbusobj, config_type)

                        # Create test XML
                        if os.path.exists(temp_runtime_config):
                            pre_req_ret, DM_tracker = dynamicDMLUtility.createXMLFromSecondaryConfig(temp_runtime_config, paramListXml)
                            intermediateFiles.append(temp_runtime_config)
                        intermediateFiles.append(paramListXml)
                        intermediateFiles.append(secondary_config)
                    else:
                        # As XML is not required for this validation type
                        pre_req_ret = "SUCCESS"
                        DM_tracker = []
                        # If the test is parameterExistence, call function to get all unique namespaces (till first 2 objects depth, eg: Device.DeviceInfo.) found in the config
                        dynamicDMLUtility.getUniqueNamespaces(secondary_config, namespaces)
                        intermediateFiles.append(secondary_config)
                        intermediateFiles.append(temp_runtime_config)

                    print("-------------------------------------------------------------------------")

                    if pre_req_ret == "SUCCESS":
                        # If XML is created and run-time table exists under the component, call the XML test handler
                        if os.path.exists(paramListXml) and DM_tracker != [] and "parameterExistence" not in testtype:
                            print("\n-------------------------------------------------------------------------")
                            print(f"{testtypeBanner} IN DYNAMIC XML FOR COMPONENT {component}")
                            print("---------------------------------------------------------------------------\n")

                            print("The name of param list xml file is ", paramListXml)
                            tree = ET.parse(paramListXml)
                            paramsRoot = tree.getroot()

                            status_dynamic, failedParams_dynamic, total_dynamic = parseXMLAndExecuteTest(paramsRoot, factoryReset, setup_type, testobj, testtype)

                        # For parameter existence test, call the config test handler
                        elif "parameterExistence" in testtype:
                            print("\n-------------------------------------------------------------------------")
                            print(f"{testtypeBanner} IN DYNAMIC CONFIG FOR COMPONENT {component}")
                            print("---------------------------------------------------------------------------\n")
                            expectedresult = "SUCCESS"
                            status_dynamic, failedParams_dynamic, total_dynamic = getParameterNames(setup_type, expectedresult, rbusobj, namespaces, secondary_config, component, configType="Dynamic")

                    else:
                        print("\nPre Requisite for creating Dynamic XML failed")
                        status_dynamic = "FAILURE"

                    # Cleanup
                    cleanup(intermediateFiles)
                # For Table object validations Dynamic XML not required
                elif "Table" in testtype:
                    # Check if the component has the required table objects
                    if "StaticTable" in testtype:
                        tableType = ["staticTable", "rbus_No_AddDelete"]
                    elif "DynamicTable" in testtype:
                        tableType = ["dynamicTable"]
                    elif "DynWritableTable" in testtype:
                        tableType = ["dynWritableTable", "rbus_AddDelete"]
                    elif "WritableTable" in testtype:
                        tableType = ["writableTable"]

                    # Determine if the required table types are found under the dynamic configuration file
                    testFlag = dynamicDMLUtility.tableConfigGenerator(path_to_runtime_config, tableType)

                    if testFlag == "True":
                        # As config is non-empty
                        print("-------------------------------------------------------------------------")
                        print(f"\nExecuting Pre-Requisites for retrieving the run-time tables\n")
                        temp_config, secondary_config = dynamicDMLUtility.performPreReq(preReqobj, rbusobj, path_to_runtime_config)
                        # Profile handling is not required separately as when executing the pre-req for run-time config, whether to test a table or not is determined
                        print("-------------------------------------------------------------------------")

                        if os.path.exists(secondary_config):
                            print("\n-------------------------------------------------------------------------")
                            print(f"{testtypeBanner} FROM RUN-TIME CONFIG FOR COMPONENT {component}")
                            print("---------------------------------------------------------------------------\n")

                            # Call the config test handler
                            status_dynamic, failedParams_dynamic, total_dynamic = parseRuntimeConfigAndExecuteTest(setup_type, secondary_config, testobj, rbusobj, component, testtype)
                            intermediateFiles.append(secondary_config)
                            intermediateFiles.append(temp_config)
                            if total_dynamic == 0:
                                print("\n-------------------------------------------------------------------------")
                                print(f"NO TABLE TO BE TESTED FROM COMPONENT {component}")
                                print("---------------------------------------------------------------------------\n")
                        else:
                            print("\nPre Requisite for creating secondary config failed")
                            status_dynamic = "FAILURE"

                    else:
                        print("\n-------------------------------------------------------------------------")
                        print(f"NO TABLE TO BE TESTED FROM COMPONENT {component}")
                        print("---------------------------------------------------------------------------\n")
                    # Cleanup
                    cleanup(intermediateFiles)
            else:
                print("\n-----Dynamic config is empty, skipping creating the dynamic XML-----\n")
    else:
        print("\n-------------------------------------------------------------------------")
        print(f"-----Runtime config not found for the component {component}-----")
        print("---------------------------------------------------------------------------\n")

    # For get validations as both data-type compliance as well as GET values are tested
    if testtype == "get":
        total["total"] = total_static["total"] + total_dynamic["total"]
        total["typeTestCount"] = total_static["typeTestCount"] + total_dynamic["typeTestCount"]
        total["valueCheckCount"] = total_static["valueCheckCount"] + total_dynamic["valueCheckCount"]
   # Total number of parameters tested under a component
    else:
        total = total_static + total_dynamic

    failedParams = failedParams_static + failedParams_dynamic

    if status_static == "FAILURE" or status_dynamic == "FAILURE":
        componentStatus = "FAILURE"

    return failedParams, componentStatus, total

# setTestParams_component
# Syntax      : setTestParams_component(component, setup_type, tr181Obj, rbusobj, testtype)
# Description : Function to handle individual device profiles to customize the test. Converts the dynamic configuration file (if any) a dynamic secondary config
#               after resolving the run-time pre requisites. The function then proceeds to call the test handler function depending
#               on the L2 test type.
# Parameters  : component - name of the component under the specified module as listed in tdkbDmlModuleList.py
#               setup_type - the protocol used for conducting the L2 tests
#               tr181Obj - the TR181 stub object
#               rbusobj - the RBUS stub object
#               testtype - type of the L2 test triggered
# Return Value: failedParams - the list of DMs that failed the test
#               componentStatus - SUCCESS/FAILURE status of the component testing. If any test step under a component reports
#               a FAILURE status, componentStatus will be FAILURE
#               total - total number of DMs tested under the component

def setTestParams_component(component, setup_type, tr181Obj, rbusobj, testtype):
    failedParams = []
    intermediateFiles = []
    componentStatus = "SUCCESS"
    total = 0
    config = {}

    if testtype == "L2-set":
        testtypeBanner = "L2 SET VALIDATIONS"

        # Get the path to static config
        staticConfig = component + "_config.json"
        configPath = os.path.dirname(os.path.realpath(__file__))
        path_to_static_config  = configPath + "/tdkbModuleConfig/" + staticConfig
        config_static = {}

        if os.path.exists(path_to_static_config):
            print("\n-------------------------------------------------------------------------")
            print(f"PROCESSING STATIC CONFIG FOR COMPONENT {component}")
            print("---------------------------------------------------------------------------\n")
            # Call the profile handler to customize the test
            # Create temporary config file to handle flags
            temp_static_config = dynamicDMLUtility.profileHandler(path_to_static_config, component, rbusobj, config_type = "static")

            if os.path.exists(temp_static_config):
                with open(temp_static_config, 'r') as file:
                    config_static = json.load(file)
                    # Copy to the unified config
                    # If the component has only the static config then unified config = static config
                    config = config_static.copy()

                intermediateFiles.append(temp_static_config)
        else:
            print("\n---------------------------------------------------------------------------")
            print(f"-----Static Config not applicable for the component {component}-----")
            print("---------------------------------------------------------------------------\n")

        # Get the path to runtime config
        runtimeConfig = component + "_runtime_config.json"
        configPath = os.path.dirname(os.path.realpath(__file__))
        path_to_runtime_config = configPath + "/tdkbModuleConfig/" + runtimeConfig
        secondary_config = ""
        config_runtime = {}
        tableList = []

        if os.path.exists(path_to_runtime_config):
            with open(path_to_runtime_config, 'rb') as file:
                config_data = json.load(file)
                if config_data:
                    print("\n-------------------------------------------------------------------------")
                    print(f"PROCESSING DYNAMIC CONFIG FOR COMPONENT {component}")
                    print("---------------------------------------------------------------------------\n")

                    # As config is non-empty
                    print("-------------------------------------------------------------------------")
                    print(f"\nExecuting Pre-Requisites for populating Dynamic parameters\n")

                    # execute the pre requisites to get the dynamic DMs
                    temp_runtime_config, secondary_config = dynamicDMLUtility.performPreReq(tr181Obj, rbusobj, path_to_runtime_config)

                    # For tables with number of rows = 0, add a table row for performing L2 set tests and collect the tables to which rows are added
                    tableList = dynamicDMLUtility.L2PreReq(tr181Obj, secondary_config, temp_runtime_config)

                    config_type = "run_time"
                    # Call the profile handler to customize the test
                    if os.path.exists(temp_runtime_config):
                        dynamicDMLUtility.profileHandler(temp_runtime_config, component, rbusobj, config_type)
                        intermediateFiles.append(temp_runtime_config)

                        # Store the temp_runtime_config
                        with open(temp_runtime_config, 'r') as file:
                            config_runtime = json.load(file)

                        # Append to the unified config in case run-time config exists
                        config = {**config_static, **config_runtime}

                    intermediateFiles.append(secondary_config)
                else:
                    print(f"\n-----Dynamic config is empty, skipping for {component}-----\n")
        else:
            print("\n---------------------------------------------------------------------------")
            print(f"-----Dynamic Config not applicable for the component {component}-----")
            print("---------------------------------------------------------------------------\n")

        if config != {}:
            print("\n-------------------------------------------------------------------------")
            print(f"{testtypeBanner} FOR COMPONENT {component}")
            print("---------------------------------------------------------------------------\n")

            # Call the execute test method to identify the writable parameters and trigger SET operations for L2 types
            componentStatus, failedParams, total = parseConfigAndExecuteL2SET(component, setup_type, tr181Obj, config, secondary_config)

            # After L2 tests, delete table rows if they were created
            if tableList != []:
                returnStatus = dynamicDMLUtility.L2PostReq(tr181Obj, tableList)
                if returnStatus == "SUCCESS":
                    print("Successfully completed post requisites for L2 tests")
                else:
                    print("Post requisites failed after L2 tests")

        # Cleanup
        cleanup(intermediateFiles)

    else:
        print("Invalid Test Type !")
        return [], "FAILURE", 0

    return failedParams, componentStatus, total

# extractDependencyChain
# Syntax      : extractDependencyChain(tdkTestObj, config, secondary_config_data, key, valueToSet, dependencyDMDict, setlevel = "testUseCase")
# Description : Function to extract the dependencies of a L2 set use-case from the config files.
# Parameters  : tdkTestObj - TR181 test object
#               config - the unified config file that is customized for device profile
#               secondary_config_data - the secondary config file
#               key - the DM to be set
#               valueToSet - the set value of the DM
#               dependencyDMDict - the depedencies to set the "key" to "valueToSet" extracted from the configs. This dictionary will be
#               populated with dependency DMs, their SET values, dataTypes and initial values.
#               setlevel - whether it is use-case test or revert operation
# Return Value: returnStatus - SUCCESS/FAILURE based upon the extraction of dependencies

def extractDependencyChain(tdkTestObj, config, secondary_config_data, key, valueToSet, dependencyDMDict, setlevel = "testUseCase"):
    returnStatus = "SUCCESS"
    if config.get(key) is not None:
        dependencies = config[key].get("Dependencies")
    else:
        dependencies = secondary_config_data[key].get("Dependencies")
    if dependencies is not None:
        # Find the dependency for the value to be set
        if isinstance(dependencies.get(valueToSet), dict):
            dmValuePairs = dependencies[valueToSet]
            for dm, value in dmValuePairs.items():
                returnStatus = extractDependencyChain(tdkTestObj, config, secondary_config_data, dm, value, dependencyDMDict, setlevel)
                if returnStatus == "SUCCESS":
                    # In case where tables are involved
                    dm_modified = dm
                    # In cases where tables are involved, identify the table instances
                    # key = abcd.abc.2.def.3.xyz
                    # dependency dm = abcd.abc.{i}.def.{i}.Enable
                    # Extract numeric values from key
                    numbers = re.findall(r'\d+', key)

                    for num in numbers:
                        dm_modified = dm.replace("{i}", num, 1)

                    if setlevel == "testUseCase":
                        actualresult, initVal = tdkutility.getTR181Value(tdkTestObj, dm_modified)

                        if actualresult == "SUCCESS":
                            dependencyDMDict[dm_modified] = {}
                            # If initial value is empty, store as empty string
                            if initVal == "":
                                dependencyDMDict[dm_modified]["initialValue"] = " "
                            else:
                                dependencyDMDict[dm_modified]["initialValue"] = initVal
                            dependencyDMDict[dm_modified]["setValue"] = value
                            # Get the data type from either the temp_config or secondar config dependending on whether a table row is involved
                            if config.get(dm) is not None:
                                dependencyDMDict[dm_modified]["type"] = config[dm_modified]["type"][0]
                            else:
                                dependencyDMDict[dm_modified]["type"] = secondary_config_data[dm]["type"][0]
                        else:
                            returnStatus = "FAILURE"
                            print(f"Failed to get the initial value of {dm_modified}")
                            break
                    else:
                        # In the revert case
                        dependencyDMDict[dm_modified] = {}
                        dependencyDMDict[dm_modified]["setValue"] = value
                        if config.get(dm) is not None:
                            dependencyDMDict[dm_modified]["type"] = config[dm_modified]["type"][0]
                        else:
                            dependencyDMDict[dm_modified]["type"] = secondary_config_data[dm]["type"][0]
                else:
                    break
        # In case there are no dependencies for setting to a particular value and direct set is possible
        else:
            print(f"Setting {key} to {valueToSet} does not have dependencies")

    return returnStatus

# findSETDependencies
# Syntax      : findSETDependencies(tdkTestObj, config, secondary_config_data, key, initialValue, dependencyDMDict, setlevel = "testUseCase")
# Description : Function to determine the value to be set to the DM which is different from the initial value
# Parameters  : tdkTestObj - TR181 test object
#               config - the unified config file that is customized for device profile
#               secondary_config_data - the secondary config file
#               key - the DM to be set
#               initialValue - the initial value of the "key"
#               dependencyDMDict - This dictionary will be populated with dependency DMs, their SET values, dataTypes and initial values.
#               setlevel - whether it is use-case test or revert operation
# Return Value: returnStatus - SUCCESS/FAILURE based upon the extraction of dependencies
#               valueToSet - the value to be set to the "key"

def findSETDependencies(tdkTestObj, config, secondary_config_data, key, initialValue, dependencyDMDict, setlevel = "testUseCase"):
    valueToSet = ""
    returnStatus = "FAILURE"

    if setlevel == "testUseCase":
        # Check if direct L2 SET value is available, if so pick that
        if config[key].get("set_value") is not None:
            if config[key]["set_value"].get("SET") is not None:
                valueToSet = config[key]["set_value"]["SET"]
                returnStatus = "SUCCESS"
            return str(valueToSet), returnStatus

        # Identify the value to be set from expected value list
        if config[key].get("expectedValues") is not None:
            if len(config[key].get("expectedValues")) == 1:
                expectedValues = config[key].get("expectedValues")[0]
            else:
                expectedValues = config[key].get("expectedValues")

            # Check if expectedVales, set_value is empty but dependencies is non-empty - those DMs can be set to the custom value mentioned in dependencies
            if expectedValues == []:
                if config[key].get("set_value") is None and config[key].get("Dependencies") is not None:
                    for setVal in config[key]["Dependencies"]:
                        valueToSet = setVal
                        returnStatus = "SUCCESS"

            # If expected values is a comma separated list
            elif isinstance(expectedValues, list):
                for val in expectedValues:
                    if val != initialValue:
                        valueToSet = val
                        break

            # For a numeric list notation, randomly chose a SET value within the range
            elif "[" in expectedValues:
                lower_limit = expectedValues.split("[")[1].split(":")[0]
                upper_limit = expectedValues.split("]")[0].split(":")[1]

                if lower_limit.strip("-").isdigit() and upper_limit.strip("-").isdigit():
                    test_list = range(int(lower_limit), int(upper_limit) + 1)

                elif lower_limit.strip("-").isdigit() and not upper_limit.strip("-").isdigit():
                    test_list = range(int(lower_limit), 65536)

                elif not lower_limit.strip("-").isdigit() and upper_limit.strip("-").isdigit():
                    test_list = range(0, int(upper_limit) + 1)

                valueToSet = random.choice([ele for ele in test_list if ele != int(initialValue)])

            # For a numeric range notation, randomly chose a SET value within the range
            elif "range(" in expectedValues:
                if "," in expectedValues:
                    minval = expectedValues.split("range(")[1].split(",")[0].strip()
                    maxval = expectedValues.split(")")[0].split(",")[1].strip()
                    test_list = range(int(minval), int(maxval))

                else:
                    maxval = expectedValues.split(")")[0].split("range(")[1].strip()
                    test_list = range(int(maxval))

                valueToSet = random.choice([ele for ele in test_list if ele != int(initialValue)])
    else:
        # For revert operation value to be set is the initial value itself
        valueToSet = initialValue
        returnStatus = "SUCCESS"

    # Extract the dependency chain
    if valueToSet != "":
        returnStatus = extractDependencyChain(tdkTestObj, config, secondary_config_data, key, valueToSet, dependencyDMDict, setlevel)

    return str(valueToSet), returnStatus

# setValue
# Syntax      : setValue(expectedresult, tr181obj, key, valueToSet, dataType, dependencyDMDict)
# Description : Function to set the key DM along with its dependencies and to validate the set operation
# Parameters  : expectedresult - SUCCESS/FAILURE
#               tr181obj - TR181 stub object
#               key - the DM to be set
#               valueToSet - the value to which "key" is to be SET
#               dataType - dataType of "key"
#               dependencyDMDict - dictionary with the dependency DMs, their SET values, dataTypes and initial values that needs to be
#               SET along with "key"
# Return Value: returnStatus - SUCCESS/FAILURE based upon the SET & GET operations done

def setValue(expectedresult, tr181obj, key, valueToSet, dataType, dependencyDMDict):
    paramList = ""
    returnStatus = "SUCCESS"
    if dependencyDMDict != {}:
        print("*****Dependencies*****")
        for depends in dependencyDMDict:
            print("%s : %s" %(depends, str(dependencyDMDict[depends]["setValue"])))
            paramList = paramList + depends + "|" + str(dependencyDMDict[depends]["setValue"]) + "|" + dependencyDMDict[depends]["type"] + "|"

        # Include the DM to be SET
        paramList = paramList + key + "|" + str(valueToSet) + "|" + dataType + "|"

        # Invoke SET operation
        tdkTestObj = tr181obj.createTestStep("TDKB_TR181Stub_SetMultiple")
        tdkTestObj.addParameter("paramList", paramList)
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
    # If no dependencies exist and the SET operation is direct
    else:
        tdkTestObj = tr181obj.createTestStep('TDKB_TR181Stub_SetOnly')
        tdkTestObj.addParameter("ParamName",key)
        tdkTestObj.addParameter("ParamValue",valueToSet)
        tdkTestObj.addParameter("Type",dataType)
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()

    if expectedresult in actualresult:
        sleep(2)

        # Get validations
        for depends in dependencyDMDict:
            tdkTestObj = tr181obj.createTestStep("TDKB_TR181Stub_Get")

            actualresult, details = tdkutility.getTR181Value(tdkTestObj, depends)

            if expectedresult in actualresult and details != "Failed to get the value of parameter":
                details = details.strip().replace("\\n", "")
                if details == str(dependencyDMDict[depends]["setValue"]):
                    print("%s set to %s successfully" %(depends, str(dependencyDMDict[depends]["setValue"])))
                    continue
                else:
                    print("%s NOT set to %s successfully, exiting..." %(depends, str(dependencyDMDict[depends]["setValue"])))
                    returnStatus = "FAILURE"
                    break
            else:
                print(f"Unable to retrieve the value of {depends} after SET operation")
                returnStatus = "FAILURE"
                break

        # Check if the DM has been SET successfully
        tdkTestObj = tr181obj.createTestStep("TDKB_TR181Stub_Get")

        actualresult, details = tdkutility.getTR181Value(tdkTestObj, key)

        if expectedresult in actualresult and details != "Failed to get the value of parameter":
            details = details.strip().replace("\\n", "")
            if details == valueToSet:
                print(f"{key} set to {valueToSet} successfully")
            else:
                print(f"{key} NOT set to {valueToSet} successfully")
                returnStatus = "FAILURE"
        else:
            print(f"Unable to retrieve the value of {key} after SET operation")
            returnStatus = "FAILURE"

    return returnStatus

# parseConfigAndExecuteL2SET
# Syntax      : parseConfigAndExecuteL2SET(component, setup_type, tr181obj, config_data, secondary_config)
# Description : Function to parse the config file and execute the L2 set tests
# Parameters  : component - name of the component under the module as listed in tdkbDmlModuleList.py
#               setup_type - the protocol used for conducting the L2 tests
#               tr181obj - TR181 stub object
#               config_data  - unified configuration file with profile handled
#               secondary_config - secondary run-time config
# Return Value: status - SUCCESS/FAILURE test status of the component
#               failedParams - DMs that failed the L2 tests
#               total - total number L2 tests conducted under the given component

def parseConfigAndExecuteL2SET(component, setup_type, tr181obj, config_data, secondary_config):
    global step
    expectedresult = "SUCCESS"
    setFlag = 0
    total = 0
    failedParams = []
    status = "SUCCESS"

    # Open and read the JSON file
    try:
        with open(secondary_config, 'r') as file:
            secondary_config = json.load(file)
    # In case secondary config does not exist
    except FileNotFoundError:
        secondary_config = {}

    if setup_type == "TDK":
        for key in config_data:
            setFlag = 0
            # From the config, identify the writable parameters
            if config_data[key].get("writable") == ["true"]:
                # Data type
                if config_data[key].get("type") is not None:
                    dataType = config_data[key]["type"][0]
                    # Identify the parameters to be included for L2 SET
                    if config_data[key].get("Set_type") == "L2":
                        total = total + 1
                        print("*************Start L2 SET validation of %s **************" %key)

                        # Get the initial value of the parameter
                        step = step + 1
                        print(f"\nTEST STEP {step}: Get the initial value of {key}")
                        print(f"EXPECTED RESULT {step}: Should get the initial value of {key}")

                        # Create new instance of test object
                        tdkTestObj = tr181obj.createTestStep('TDKB_TR181Stub_Get')

                        # Get the initail value
                        actualresult, initialValue = tdkutility.getTR181Value(tdkTestObj, key)

                        if actualresult == "SUCCESS":
                            initialValue = initialValue.replace("\\n", "").strip()
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT: Initial value of {key} is : {initialValue}")
                            print("TEST EXECUTION RESULT: SUCCESS")

                            # Extract all dependencies involved in the use-case
                            step = step + 1
                            print(f"\nTEST STEP {step}: Get all the dependencies involved for setting {key}")
                            print(f"EXPECTED RESULT {step}: Should get all the dependencies involved for setting {key}")

                            # Find the value to be set and set dependencies
                            dependencyDMDict = {}
                            valueToSet, returnStatus = findSETDependencies(tdkTestObj, config_data, secondary_config, key, initialValue, dependencyDMDict)

                            if returnStatus == "SUCCESS":
                                if dependencyDMDict != {}:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT: All dependencies involved in the use-case are identified")
                                    print("TEST EXECUTION RESULT: SUCCESS")
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT: No dependencies for setting {key}")
                                    print("TEST EXECUTION RESULT: SUCCESS")

                                # Set the dependencies (if any) followed by parameter SET. Also validate the GET operation.
                                step = step + 1
                                print(f"\nTEST STEP {step}: Set {key} to {valueToSet}")
                                print(f"EXPECTED RESULT {step}: Should set {key} to {valueToSet} successfully")
                                returnStatus = setValue(expectedresult, tr181obj, key, valueToSet, dataType, dependencyDMDict)

                                if returnStatus == "SUCCESS":
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT: Set opreration of {key} to {valueToSet} is success")
                                    print("TEST EXECUTION RESULT: SUCCESS")

                                    # Revert
                                    step = step + 1
                                    print(f"\nTEST STEP {step}: Get all the dependencies involved for reverting {key} to {initialValue}")
                                    print(f"EXPECTED RESULT {step}: Should get all the dependencies involved for reverting {key} to {initialValue}")

                                    dependencyDMDict = {}
                                    valueToSet, returnStatus = findSETDependencies(tdkTestObj, config_data, secondary_config, key, initialValue, dependencyDMDict, "revert")

                                    if returnStatus == "SUCCESS":
                                        if dependencyDMDict != {}:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT: All dependencies involved in the revert use-case are identified")
                                            print("TEST EXECUTION RESULT: SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT: No dependencies for reverting {key}")
                                            print("TEST EXECUTION RESULT: SUCCESS")

                                        # Set the dependencies (if any) followed by parameter SET. Also validate the GET operation.
                                        step = step + 1
                                        print(f"\nTEST STEP {step}: Revert {key} to {initialValue}")
                                        print(f"EXPECTED RESULT {step}: Should revert {key} to {initialValue} successfully")
                                        returnStatus = setValue(expectedresult, tr181obj, key, initialValue, dataType, dependencyDMDict)

                                        if returnStatus == "SUCCESS":
                                            setFlag = 1
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT: Revert opreration of {key} to {initialValue} is success")
                                            print("TEST EXECUTION RESULT: SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT: Revert opreration of {key} to {initialValue} failed")
                                            print("TEST EXECUTION RESULT: FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT: Set opreration of {key} to {valueToSet} failed")
                                    print("TEST EXECUTION RESULT: FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT: Dependencies involved in the use-case are not retrieved successfully")
                                print("TEST EXECUTION RESULT: FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT: Initial value of {key} is : {initialValue}")
                            print("TEST EXECUTION RESULT: FAILURE")
                    else:
                        # Skip the set
                        continue
                else:
                    # Skip the set
                    continue
            else:
                # Skip the set
                continue
            if setFlag == 0:
                print("*************Validation of %s is FAILURE**************\n" %key)
                failedParams.append(key)
                status = "FAILURE"
            else:
                print("*************Validation of %s is SUCCESS**************\n" %key)
        # if total is 0, no L2 set operations are possible for the component
        if total == 0:
            print(f"\nL2 SET use-cases not present for the component {component}")
    else:
        print("Invalid Setup type!!!")
        status = "FAILURE"

    return status, failedParams, total

# parseRuntimeConfigAndExecuteTest
# Syntax      : parseRuntimeConfigAndExecuteTest(setup_type, secondary_config, obj, rbusobj, component, testtype)
# Description : Function to parse the config file and execute the L1 table tests
# Parameters  : setup_type - the protocol used for conducting the L1 tests
#               secondary_config - secondary run-time config
#               obj - TR181/sysutil stub object
#               rbusobj - RBUS stub object
#               component - name of the component as specified in tdkbDmlModuleList.py
#               testtype - type of the L1 test
# Return Value: status - SUCCESS/FAILURE test status of the component
#               failedTables - tables that failed the tests
#               testCount - total number L1 table tests conducted under the given component

def parseRuntimeConfigAndExecuteTest(setup_type, secondary_config, obj, rbusobj, component, testtype):
    testCount = 0
    failedTables = []
    status = "SUCCESS"
    ifTestTable = "False"
    isTableOpSupported = "False"
    global step

    if setup_type == "TDK" or setup_type == "WEBPA":
        if testtype == "AddStaticTableRow":
            # Adding row to static tables should return failure
            if setup_type == "TDK":
                expectedresult = ["FAILURE", tdkbDmlModuleList.AddStaticTableRowReturnCode, ""]
            elif setup_type == "WEBPA":
                expectedresult = ["FAILURE", tdkbDmlModuleList.AddStaticTableRowWebpaReturnCode, tdkbDmlModuleList.AddStaticTableRowWebpaReturnMsg]

            # Parse through the secondary config and identify the tables
            # Open and read the JSON file
            with open(secondary_config, 'r') as file:
                config = json.load(file)

                for key, _ in config.items():
                    # Type 1 where tables have NumberOfEntries and is fully resolved (no .{i}. present), Type 2,3 for rbus tables
                    if (key.endswith("NumberOfEntries") and ".{i}." not in key) or (key.endswith(".{i}.") and key.count(".{i}.") == 1) or (key.endswith(".{i}") and key.count(".{i}") == 1):
                        if config[key]["table"] == "staticTable":
                            ifTestTable = config[key]["ifTestTable"]
                            table = key.split("NumberOfEntries")[0] + "."

                        elif config[key]["table"] == "rbus_No_AddDelete":
                            ifTestTable = config[key]["ifTestTable"]
                            table = key.split("{i}")[0]

                        else:
                            table = ""

                        if table != "" and ifTestTable != "False":
                            print("*************Start validation of %s **************" %table)

                            testCount = testCount + 1
                            returnValue, returnMsg = AddRowToTableObject(setup_type, table, obj, expectedresult)

                            if returnValue == expectedresult[1] and returnMsg == expectedresult[2]:

                                print("*************Validation of %s is SUCCESS**************\n" %table)
                            else:
                                print("*************Validation of %s is FAILURE**************\n" %table)

                                status = "FAILURE"
                                failedTables.append(table)

                        if table != "" and ifTestTable == "False":
                            print("*************Skipping %s as table not applicable*************\n" %table)


        elif testtype == "DeleteStaticTableRow":
            # Deleting row from static tables should return failure
            if setup_type == "TDK":
                expectedresult = ["FAILURE", tdkbDmlModuleList.DeleteStaticTableRowReturnCode, ""]
            elif setup_type == "WEBPA":
                expectedresult = ["FAILURE", tdkbDmlModuleList.DeleteStaticTableRowWebpaReturnCode, tdkbDmlModuleList.DeleteStaticTableRowWebpaReturnMsg]

            # Parse through the secondary config and identify the tables
            # Open and read the JSON file
            with open(secondary_config, 'r') as file:
                config = json.load(file)

                for key, _ in config.items():
                    # Type 1 where tables have NumberOfEntries and is fully resolved (no .{i}. present), Type 2,3 for rbus tables
                    if (key.endswith("NumberOfEntries") and ".{i}." not in key) or (key.endswith(".{i}.") and key.count(".{i}.") == 1) or (key.endswith(".{i}") and key.count(".{i}") == 1):
                        if config[key]["table"] == "staticTable":
                            ifTestTable = config[key]["ifTestTable"]
                            table = key.split("NumberOfEntries")[0] + "."
                            # The instance to be deleted should be taken as the last instance
                            pairValue = key.split(".")[-1]
                            delRow = config[key][pairValue]

                        elif config[key]["table"] == "rbus_No_AddDelete":
                            ifTestTable = config[key]["ifTestTable"]
                            table = key.split("{i}")[0]
                            # The instance to be deleted should be taken as the last instance
                            pairValue = "NumberOfEntries"
                            delRow = config[key][pairValue]

                        else:
                            table = ""

                        if table != "" and ifTestTable != "False":
                            if int(delRow) > 0:
                                table = table + delRow + "."

                                print("*************Start validation of %s **************" %table)

                                testCount = testCount + 1
                                returnValue, returnMsg = DeleteRowFromTableObject(setup_type, table, obj, expectedresult)

                                if returnValue == expectedresult[1] and returnMsg == expectedresult[2]:
                                    print("*************Validation of %s is SUCCESS**************\n" %table)
                                else:
                                    print("*************Validation of %s is FAILURE**************\n" %table)

                                    status = "FAILURE"
                                    failedTables.append(table)

                            else:
                                print(f"\n*************No Table Rows to Delete under {table}*************\n")

                        if table != "" and ifTestTable == "False":
                            print("*************Skipping %s as table not applicable*************" %table)

        elif testtype == "AddDynamicTableRow":
            # Adding row to dynamic tables should return failure
            if setup_type == "TDK":
                expectedresult = ["FAILURE", tdkbDmlModuleList.AddDynamicTableRowReturnCode, ""]
            elif setup_type == "WEBPA":
                expectedresult = ["FAILURE", tdkbDmlModuleList.AddDynamicTableRowWebpaReturnCode, tdkbDmlModuleList.AddDynamicTableRowWebpaReturnMsg]

            # Parse through the secondary config and identify the tables
            # Open and read the JSON file
            with open(secondary_config, 'r') as file:
                config = json.load(file)

                for key, _ in config.items():
                    # Type 1 where tables have NumberOfEntries and is fully resolved (no .{i}. present)
                    if key.endswith("NumberOfEntries") and ".{i}." not in key:
                        if config[key]["table"] == "dynamicTable":
                            ifTestTable = config[key]["ifTestTable"]
                            table = key.split("NumberOfEntries")[0] + "."

                            if ifTestTable != "False":
                                print("*************Start validation of %s **************" %table)

                                testCount = testCount + 1
                                returnValue, returnMsg = AddRowToTableObject(setup_type, table, obj, expectedresult)

                                if returnValue == expectedresult[1] and returnMsg == expectedresult[2]:
                                    print("*************Validation of %s is SUCCESS**************\n" %table)
                                else:
                                    print("*************Validation of %s is FAILURE**************\n" %table)

                                    status = "FAILURE"
                                    failedTables.append(table)

                            else:
                                print("*************Skipping %s as table not applicable*************" %table)

        elif testtype == "DeleteDynamicTableRow":
            # Deleting row from dynamic tables should return failure
            if setup_type == "TDK":
                expectedresult = ["FAILURE", tdkbDmlModuleList.DeleteDynamicTableRowReturnCode, ""]
            elif setup_type == "WEBPA":
                expectedresult = ["FAILURE", tdkbDmlModuleList.DeleteDynamicTableRowWebpaReturnCode, tdkbDmlModuleList.DeleteDynamicTableRowWebpaReturnMsg]

            # Parse through the secondary config and identify the tables
            # Open and read the JSON file
            with open(secondary_config, 'r') as file:
                config = json.load(file)

                for key, _ in config.items():
                    # Type 1 where tables have NumberOfEntries and is fully resolved (no .{i}. present)
                    if key.endswith("NumberOfEntries") and ".{i}." not in key:
                        if config[key]["table"] == "dynamicTable":
                            ifTestTable = config[key]["ifTestTable"]
                            table = key.split("NumberOfEntries")[0] + "."

                            # The instance to be deleted should be taken as the last instance
                            pairValue = key.split(".")[-1]
                            delRow = config[key][pairValue]
                            if ifTestTable != "False":
                                if int(delRow) > 0:
                                    table = table + delRow + "."

                                    print("*************Start validation of %s **************" %table)

                                    testCount = testCount + 1
                                    returnValue, returnMsg = DeleteRowFromTableObject(setup_type, table, obj, expectedresult)

                                    if returnValue == expectedresult[1] and returnMsg == expectedresult[2]:
                                        print("*************Validation of %s is SUCCESS**************\n" %table)
                                    else:
                                        print("*************Validation of %s is FAILURE**************\n" %table)

                                        status = "FAILURE"
                                        failedTables.append(table)

                                else:
                                    print(f"\n*************No Table Rows to Delete under {table}*************\n")
                            else:
                                print("*************Skipping %s as table not applicable*************" %table)

        elif testtype == "AddAndDeleteDynWritableTableRow":
            # Deleting row from static tables should return failure
            expectedresult = ["SUCCESS"]

            # Parse through the secondary config and identify the tables
            # Open and read the JSON file
            with open(secondary_config, 'r') as file:
                config = json.load(file)

                for key, _ in config.items():
                    # Type 1 where tables have NumberOfEntries and is fully resolved (no .{i}. present), Type 2,3 for rbus tables
                     if (key.endswith("NumberOfEntries") and ".{i}." not in key) or (key.endswith(".{i}.") and key.count(".{i}.") == 1) or (key.endswith(".{i}") and key.count(".{i}") == 1):
                        if config[key]["table"] == "dynWritableTable":
                            ifTestTable = config[key]["ifTestTable"]
                            tableOperation = "FAILURE"
                            table = key.split("NumberOfEntries")[0] + "."
                            pairValue = key.split(".")[-1]
                        elif config[key]["table"] == "rbus_AddDelete":
                            ifTestTable = config[key]["ifTestTable"]
                            tableOperation = "FAILURE"
                            table = key.split("{i}")[0]
                            pairValue = "NumberOfEntries"
                        else:
                            table = ""

                        if table != "" and ifTestTable != "False":
                            print("*************Start validation of %s **************" %table)

                            testCount = testCount + 1
                            # Get the instance number
                            instanceValue, returnMsg = AddRowToTableObject(setup_type, table, obj, expectedresult)

                            # Check if the row number incremented by 1
                            if instanceValue.isdigit():
                                # The added instance may not be always equal to the number of enries + 1
                                #if int(instanceValue) == int(config[key][pairValue]) + 1:
                                tableInstance = table + instanceValue + "."
                                if int(instanceValue) >= int(config[key][pairValue]):
                                    print("\n-----Table row incremeneted-----")

                                    # Get all the required parameters that are expected to be added
                                    tableParams = dynamicDMLUtility.checkTableInstanceParams(obj, table, instanceValue, config)

                                    # Check if the table parameters are added as part of the new instance
                                    # here, recursive getnames is required
                                    paramNames, actualresult, tdkTestObj = dynamicDMLUtility.getNames(expectedresult[0], rbusobj, tableInstance, component, recursion="True")

                                    # Remove the trailing "" - empty param
                                    paramNames.remove("")
                                    step = step + 1
                                    print(f"\nTEST STEP {step}: Get the parameter names under the path : {tableInstance}")
                                    print(f"EXPECTED RESULT {step}: The parameter names under the path should be retrieved successfully")

                                    if expectedresult[0] in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT : \"{paramNames}\"")
                                        print("TEST EXECUTION RESULT: SUCCESS")

                                        step = step + 1
                                        print(f"\nTEST STEP {step}: Check if all expected parameters are found for the table instance")
                                        print(f"EXPECTED RESULT {step}: Should find {tableParams} under the newly added table instance")

                                        if tableParams == paramNames:
                                            tableOperation = "SUCCESS"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT : All required table params are found")
                                            print("TEST EXECUTION RESULT: SUCCESS")
                                        else:
                                            # Find the missing parameters
                                            missingParamList = set(tableParams) - set(paramNames)
                                            if missingParamList != set():
                                                print("\nParameter(s) not found: ", missingParamList)

                                                #Check if the missing parameters are flag dependent
                                                status = "SUCCESS"
                                                for param in missingParamList:
                                                    flagBased = dynamicDMLUtility.isParamFlagDependent(param, config)
                                                    if flagBased == True:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f'{param} is flag dependent, so skipping')
                                                    else:
                                                        status = "FAILURE"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f'{param} is NOT flag dependent but NOT found')

                                            #There might be unexpected parameters under the table which are not found in config file
                                            unexpectedParams = set(paramNames) - set(tableParams)
                                            if unecpectedParams != set():
                                                print("\nUnexpected parameter(s) found under table instance: ", unexpectedParams)
                                                status = "FAILURE"

                                            if status == "SUCCESS" and unexpectedParams == set():
                                                tableOperation = "SUCCESS"
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f'\nACTUAL RESULT : All required table params are found and there are no unexpected parameters under the table instance')
                                                print("TEST EXECUTION RESULT: SUCCESS")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"\nACTUAL RESULT : All required table params are NOT found and/or unexpected parameters found")
                                                print("TEST EXECUTION RESULT: FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT : Details : Getnames failed")
                                        print("TEST EXECUTION RESULT: FAILURE")

                                    # Delete the added instance
                                    #deltable = table + instanceValue + "."
                                    returnValue, returnMsg = DeleteRowFromTableObject(setup_type, tableInstance, obj, expectedresult)

                                    if returnValue != expectedresult[0]:
                                        print("\n-----Table row NOT deleted-----")
                                else:
                                    print(f"\n-----Table row NOT incremented from the previous row count : {config[key][pairValue]} although add operation is success-----\n")
                                    # Proceed to delete the added instance
                                    returnValue, returnMsg = DeleteRowFromTableObject(setup_type, tableInstance, obj, expectedresult)
                                    if returnValue != expectedresult[0]:
                                        print("\n-----Table row NOT deleted-----")
                            else:
                                print("\n-----Table row NOT added-----")

                            if tableOperation == "SUCCESS" and returnValue == expectedresult[0]:
                                print("*************Validation of %s is SUCCESS**************\n" %table)
                            else:
                                print("*************Validation of %s is FAILURE**************\n" %table)
                                status = "FAILURE"
                                failedTables.append(table)

                        if table != "" and ifTestTable == "False":
                            print("*************Skipping %s as table not applicable*************" %table)

        elif testtype == "AddAndDeleteWritableTableRow":
            # Deleting row from static tables should return failure
            expectedresult = ["SUCCESS"]

            # Parse through the secondary config and identify the tables
            # Open and read the JSON file
            with open(secondary_config, 'r') as file:
                config = json.load(file)

                for key, _ in config.items():
                    # Type 1 where tables have NumberOfEntries and is fully resolved (no .{i}. present), Type 2,3 for rbus tables
                    # In case of writable tables exclude the rigid tables
                    if (key.endswith("NumberOfEntries") and ".{i}." not in key):
                        if config[key]["table"] == "writableTable":
                            ifTestTable = config[key]["ifTestTable"]
                            isTableOpSupported = config[key]["addOperation"]
                            tableOperation = "FAILURE"
                            table = key.split("NumberOfEntries")[0] + "."
                            pairValue = key.split(".")[-1]
                        else:
                            table = ""

                        if table != "" and isTableOpSupported == "Yes" and ifTestTable != "False":
                            print("*************Start validation of %s **************" %table)

                            testCount = testCount + 1
                            # Get the instance number
                            instanceValue, returnMsg = AddRowToTableObject(setup_type, table, obj, expectedresult)

                            # Check if the row number incremented by 1
                            if instanceValue.isdigit():
                                # The added instance may not be always eual to the number of enries + 1
                                #if int(instanceValue) == int(config[key][pairValue]) + 1:
                                tableInstance = table + instanceValue + "."
                                if int(instanceValue) >= int(config[key][pairValue]):
                                    print("\n-----Table row incremeneted-----")

                                    # Check if all the required parameters are added
                                    tableParams = dynamicDMLUtility.checkTableInstanceParams(obj, table, instanceValue, config)

                                    # Check if the table parameters are added as part of the new instance
                                    # Here, recursive getnames is required
                                    paramNames, actualresult, tdkTestObj = dynamicDMLUtility.getNames(expectedresult[0], rbusobj, tableInstance, component, recursion="True")

                                    # Remove the trailing "" - empty param
                                    paramNames.remove("")
                                    step = step + 1
                                    print(f"\nTEST STEP {step}: Get the parameter names under the path : {tableInstance}")
                                    print(f"EXPECTED RESULT {step}: The parameter names under the path should be retrieved successfully")

                                    if expectedresult[0] in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT : \"{paramNames}\"")
                                        print("TEST EXECUTION RESULT: SUCCESS")

                                        step = step + 1
                                        print(f"\nTEST STEP {step}: Check if all expected parameters are found for the table instance")
                                        print(f"EXPECTED RESULT {step}: Should find {tableParams} under the newly added table instance")

                                        if tableParams == paramNames:
                                            tableOperation = "SUCCESS"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT : All required table params are found")
                                            print("TEST EXECUTION RESULT: SUCCESS")
                                        else:
                                            # Find the missing parameters
                                            missingParamList = set(tableParams) - set(paramNames)
                                            if missingParamList != set():
                                                print("\nParameter(s) not found: ", missingParamList)

                                                #Check if the missing parameters are flag dependent
                                                status = "SUCCESS"
                                                for param in missingParamList:
                                                    flagBased = dynamicDMLUtility.isParamFlagDependent(param, config)
                                                    if flagBased == True:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f'{param} is flag dependent, so skipping')
                                                    else:
                                                        status = "FAILURE"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f'{param} is NOT flag dependent but NOT found')


                                            #There might be unexpected parameters under the table which are not found in config file
                                            unexpectedParams = set(paramNames) - set(tableParams)
                                            if unexpectedParams != set():
                                                status = "FAILURE"
                                                print("\nUnexpected parameter(s) found under table instance: ", unexpectedParams)

                                            if status == "SUCCESS" and unexpectedParams == set():
                                                tableOperation = "SUCCESS"
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f'ACTUAL RESULT : All required table params are found and there are no unexpected parameters under the table instance')
                                                print("TEST EXECUTION RESULT: SUCCESS")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT : All required table params are NOT found and/or unexpected parameters found")
                                                print("TEST EXECUTION RESULT: FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT : Details : Getnames failed")
                                        print("TEST EXECUTION RESULT: FAILURE")

                                    # Delete the added instance
                                    #deltable = table + instanceValue + "."
                                    returnValue, returnMsg = DeleteRowFromTableObject(setup_type, tableInstance, obj, expectedresult)
                                    if returnValue != expectedresult[0]:
                                        print("\n-----Table row NOT deleted-----")
                                else:
                                    print(f"\n-----Table row NOT incremented from the previous row count : {config[key][pairValue]} although add operation is success-----")
                                    # Proceed to delete the added instance
                                    returnValue, returnMsg = DeleteRowFromTableObject(setup_type, tableInstance, obj, expectedresult)
                                    if returnValue != expectedresult[0]:
                                        print("\n-----Table row NOT deleted-----")
                            else:
                                print("\n-----Table row NOT added-----")

                            if tableOperation == "SUCCESS" and returnValue == expectedresult[0]:
                                print("*************Validation of %s is SUCCESS**************\n" %table)
                            else:
                                print("*************Validation of %s is FAILURE**************\n" %table)
                                status = "FAILURE"
                                failedTables.append(table)

                        if table != "" and ifTestTable == "False":
                            print("*************Skipping %s as table not applicable*************" %table)
    else:
        print("Invalid Setup type!!!")
        status = "FAILURE"

    return status, failedTables, testCount

# AddRowToTableObject
# Syntax      : AddRowToTableObject(setup_type, table, obj, expectedresult)
# Description : Function to add a row to a table object
# Parameters  : setup_type - type of protocol for conducting test
#               table - the table to which a new row instance is to be added
#               tr181obj - TR181/sysutil stub object
#               expectedresult - the expected result of the add row operation
# Return Value: returnValue - return the errorcode for -ve tests and the newly added table row instance for +ve tests
#               returnMsg - return the protocol message after test is conducted

def AddRowToTableObject(setup_type, table, obj, expectedresult):

    global step
    actualresult= ""
    returnValue=""
    errorCode=""
    returnMsg=""
    instanceNum=""

    # Get the current value of the parameter
    if setup_type == "TDK":
        tdkTestObj = obj.createTestStep("TDKB_TR181Stub_AddObject")
        tdkTestObj.addParameter("paramName", table)
        tdkTestObj.executeTestCase(expectedresult[0])
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails().strip().replace("\\n", "")
    elif setup_type == "WEBPA":
        queryParam = {"name": table}
        queryResponse = webpaQuery(obj, queryParam, "addTableRow")
        parsedResponse = parseWebpaResponse(queryResponse, 1, "addTableRow")
        details = parsedResponse[1].strip()

        if expectedresult[0] in parsedResponse[0]:
            actualresult = expectedresult[0]

        # To set result status
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        tdkTestObj.executeTestCase("SUCCESS")

    step = step + 1
    print(f"\nTEST STEP {step}: Add a new row to the table object {table}")

    if expectedresult[0] in actualresult:
        # For failure to add table row
        if setup_type == "TDK":
            if "Errorcode" in details:
                print(f"EXPECTED RESULT {step}: Adding new row to the table object should fail with errorcode {expectedresult[1]}")
                errorCode = details.split("Errorcode: ")[1]
                returnValue = errorCode
                if errorCode == expectedresult[1]:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT : Details: \"{details}\"")
                    print("TEST EXECUTION RESULT: SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT : Details: \"{details}\"")
                    print("TEST EXECUTION RESULT: FAILURE")

            elif "Instance Number is :" in details:
                instanceNum =  details.split("Instance Number is :")[1]
                print(f"EXPECTED RESULT {step}: Adding new row to the table object should be success and the newly added row instance should be >= 1")
                returnValue = instanceNum
                if instanceNum.isdigit():
                    if int(instanceNum) > 0:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT : Details: \"{details}\"")
                        print("TEST EXECUTION RESULT: SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT : Details: \"{details}\"")
                        print("TEST EXECUTION RESULT: FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT : Details: \"{details}\"")
                    print("TEST EXECUTION RESULT: FAILURE")
        elif setup_type == "WEBPA":
            if "row" not in details:
                print(f"EXPECTED RESULT {step}: Adding new row to the table object should fail with errorcode {expectedresult[1]} and return message should be {expectedresult[2]}")
                #print("Details: ", details)
                returnValue = details.split("statusCode: ")[1]
                returnMsg = details.split("Message: ")[1].split(",")[0]
                #print(f"{returnValue}, {expectedresult[1]}, {returnMsg}, {expectedresult[2]}")
                if returnValue == expectedresult[1] and returnMsg == expectedresult[2]:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT : Details: \"{details}\"")
                    print("TEST EXECUTION RESULT: SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT : Details: \"{details}\"")
                    print("TEST EXECUTION RESULT: FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"EXPECTED RESULT {step}: Adding new row to the table object should be {expectedresult[0]}")
        print(f"ACTUAL RESULT : Details: \"{details}\"")
        print("TEST EXECUTION RESULT: FAILURE")

    return returnValue, returnMsg

# DeleteRowFromTableObject
# Syntax      : DeleteRowFromTableObject(setup_type, table, obj, expectedresult)
# Description : Function to delete a row instance from a table object
# Parameters  : setup_type - protocol type for conducting the test
#               table - the table from which a row instance is to be deleted
#               obj - TR181/sysutil stub object
#               expectedresult - the expected result of the delete row operation
# Return Value: returnValue - return the errorcode for -ve tests and the SUCCESS/FAILURE status for +ve tests
#               returnMsg - return message from the test protocol

def DeleteRowFromTableObject(setup_type, table, obj, expectedresult):

    global step
    actualresult= ""
    returnValue=""
    errorCode=""
    returnMsg=""

    # Get the current value of the parameter
    if setup_type == "TDK":
        tdkTestObj = obj.createTestStep("TDKB_TR181Stub_DelObject")
        tdkTestObj.addParameter("paramName", table)
        tdkTestObj.executeTestCase(expectedresult[0])
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails().strip().replace("\\n", "")
    elif setup_type == "WEBPA":
        queryParam = {"name": table}
        queryResponse = webpaQuery(obj, queryParam, "deleteTableRow")
        parsedResponse = parseWebpaResponse(queryResponse, 1, "deleteTableRow")
        details = parsedResponse[1].strip()

        if expectedresult[0] in parsedResponse[0]:
            actualresult = expectedresult[0]

        # To set result status
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        tdkTestObj.executeTestCase("SUCCESS")

    step = step + 1
    print(f"\nTEST STEP {step}: Delete the table row instance {table}")

    if expectedresult[0] in actualresult:
        # For failure to delete table row
        if setup_type == "TDK":
            if "Errorcode" in details:
                print(f"EXPECTED RESULT {step}: Deleting row from the table object should fail with errorcode {expectedresult[1]}")
                errorCode = details.split("Errorcode: ")[1]
                returnValue = errorCode
                if errorCode == expectedresult[1]:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT : Details: \"{details}\"")
                    print("TEST EXECUTION RESULT: SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT : Details: \"{details}\"")
                    print("TEST EXECUTION RESULT: FAILURE")

            elif "DELETE OBJECT API Validation is Success" in details:
                returnValue = "SUCCESS"
                print(f"EXPECTED RESULT {step}: Deleting row from the table object should be success")
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT : Details: \"{details}\"")
                print("TEST EXECUTION RESULT: SUCCESS")

        elif setup_type == "WEBPA":
            print(f"EXPECTED RESULT {step}: Deleting row from the table object should fail with errorcode {expectedresult[1]} and return message should be {expectedresult[2]}")
            returnValue = details.split("statusCode: ")[1]
            returnMsg = details.split("Message: ")[1].split(",")[0]
            #print(f"{returnValue}, {expectedresult[1]}, {returnMsg}, {expectedresult[2]}")
            if returnValue == expectedresult[1] and returnMsg == expectedresult[2]:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT : Details: \"{details}\"")
                print("TEST EXECUTION RESULT: SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT : Details: \"{details}\"")
                print("TEST EXECUTION RESULT: FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"EXPECTED RESULT {step}: Deleting row from the table object should be {expectedresult[0]}")
        print(f"ACTUAL RESULT : Details: \"{details}\"")
        print("TEST EXECUTION RESULT: FAILURE")

    return returnValue, returnMsg

# getElementInfo
# Syntax      : getElementInfo(tdkTestObj, expectedresult, getResult, partialPath, component, uniqueNamespaces)
# Description : Function to collect all unique namespaces in a recursive loop for a given partial path under a component
# Parameters  : tdkTestObj - RBUS stub object
#               expectedresult - the expected test result
#               getResult - would be set to "FAILURE" in case the rbus test fails
#               partialPath - the path under a component from which unique namespaces are retrieved in a recursive loop
#               component - the component under the module as listed under tdkbDmlModuleList.py
#               uniqueNamespaces - the leaf namespaces collected under the partial path
# Return Value: None

def getElementInfo(tdkTestObj, expectedresult, getResult, partialPath, component, uniqueNamespaces):
    tdkTestObj.addParameter("pathName",partialPath)
    tdkTestObj.addParameter("compName",component)
    tdkTestObj.addParameter("depth",-1)
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        newNamespaces = details.split(", ")
        for name in newNamespaces:
            if name.endswith("."):
                getElementInfo(tdkTestObj, expectedresult, getResult, name, component, uniqueNamespaces)
            else:
                uniqueNamespaces.add(name)
    else:
        getResult = "FAILURE"
        tdkTestObj.setResultStatus("FAILURE")
        print(f"Unable to fetch the namespaces under {partialPath}")

# getParameterNames
# Syntax      : getParameterNames(setup_type, expectedresult, rbusobj, namespaces, configPath, component, configType)
# Description : Function to test parameter existence by cheching if all flag-independent DMs
#               are present under DM tree of a given component in the test device
# Parameters  : setup_type - the protocol used for conducting the tests
#               expectedresult - the expected test result
#               rbusobj - RBUS stub object
#               namespaces - all the namespaces under a component upto a depth = 2 (Ex: Device.DeviceInfo., Device.IP.)
#               configPath - the path to the specified config file
#               component - the component under the module as listed under tdkbDmlModuleList.py
#               configType - the type to the config file (static or run-time)
# Return Value: flag - SUCCESS/FAILURE state of the test
#               failedParams - the parameters that are flag independent but not available under the DM tree of the component
#               numberOfParams - the number of params tested under the component

def getParameterNames(setup_type, expectedresult, rbusobj, namespaces, configPath, component, configType):
    global step
    uniqueNamespaces = set()
    getResult = "SUCCESS"
    failedParams = []
    flag = "SUCCESS"
    params = []
    numberOfParams = 0

    if setup_type == "TDK":
        # From config get all params that are not flag dependent
        dynamicDMLUtility.getAllParams(configPath, params, configType)
        numberOfParams = len(params)
        print(f"Total DM count from Config for {component} which are not flag dependent : {numberOfParams}\n")

        # If params is considered from config which are not flag dependent
        if len(params) > 0:
            # Open RBUS connection
            tdkTestObj = rbusobj.createTestStep('RBUS_Open');
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();

            if expectedresult in actualresult:
                tdkTestObj = rbusobj.createTestStep("RBUS_GetElementInfo")
                for partialPath in namespaces:
                    if partialPath.endswith("."):
                        getElementInfo(tdkTestObj, expectedresult, getResult, partialPath, component, uniqueNamespaces)
                    else:
                        uniqueNamespaces.add(partialPath)
                # Remove the trailing "" - empty param
                uniqueNamespaces.remove("")

                for param in params:
                    step = step + 1
                    print("*************Start validation of %s **************" %param)
                    print(f"TEST STEP {step}: Check if the parameter {param} exists")
                    print(f"EXPECTED RESULT {step}: The parameter should exist")

                    if param in uniqueNamespaces:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT: {param} Exists")
                        print("TEST EXECUTION RESULT: SUCCESS")
                        print("*************Validation of %s is SUCCESS**************\n" %param)
                    else:
                        flag = "FAILURE"
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT : {param} parameter does not exist")
                        print("TEST EXECUTION RESULT: FAILURE")
                        failedParams.append(param)
                        print("*************Validation of %s is FAILURE**************\n" %param)

                # Close RBUS connection
                tdkTestObj = rbusobj.createTestStep('RBUS_Close');
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();

                if expectedresult not in actualresult:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("RBUS close failed")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("RBUS open failed")
        else:
            print("No params from config need to be tested for parameter existence")
    return flag, failedParams, numberOfParams

# parseXMLAndExecuteTest
# Syntax      : parseXMLAndExecuteTest(paramsRoot, factoryReset, setup_type, tr181Obj, testtype)
# Description : Wrapper function to invoke the L1 tests (get, readOnlySet, parameterExistence, writeAccessCompliance, writeTypeCompliance)
#               after parsing through the XML tree
# Parameters  : paramsRoot - the XML tree root
#               factoryReset - whether or not the test should start after factory resetting
#               setup_type - the protocol used for conducting the tests
#               obj - TR181/sysutil stub object
#               testtype - type of the L1 test
# Return Value: componentStatus - SUCCESS/FAILURE state of the component test
#               failedParams - list of DMs that failed the L1 test
#               totalCountflag - number of DMs tested

def parseXMLAndExecuteTest(paramsRoot, factoryReset, setup_type, obj, testtype):
    failedParams = []
    paramList = []
    componentStatus = "SUCCESS"
    total = 0
    totalCount = 0
    typeTestCount = 0
    valueCheckCount = 0

    if testtype == "get":
        totalCount = {"total" : 0, "typeTestCount" : 0, "valueCheckCount" : 0}
        for param in paramsRoot:
            paramList.append(param.find('name').text)
        print("\nPARAMS TO BE GET ARE: ",paramList)

    elif testtype == "readOnlySet":
        for param in paramsRoot:
            if param.find('writable') is not None:
                if param.find('writable').text == "false":
                    paramList.append(param.find('name').text)
        print("\nPARAMS TO BE SET ARE: ",paramList)

    elif testtype == "paraparameterExistence":
        for param in paramsRoot:
            paramList.append(param.find('name').text)
            print("\nPARAMS TO CHECK FOR EXISTENCE ARE: ",paramList)

    elif testtype == "writeAccessCompliance" or testtype == "writeTypeCompliance":
        for param in paramsRoot:
            if param.find('writable') is not None:
                if param.find('writable').text == "true":
                    paramList.append(param.find('name').text)
        print("\nPARAMS TO BE SET ARE: ",paramList)

    else:
        print("Invalid Option")
        return "FAILURE", failedParams, totalCount

    if testtype == "get":
        for param in paramsRoot:
            #for some params default value is not applicable, skip
            if factoryReset == "true" and param.find('defaultValue') is None:
                continue

            #Get the value of each param
            if param.find('defaultValue') is not None:
                defaultValue = param.find('defaultValue').text
                #if default value given xml is empty
                if defaultValue is None:
                    defaultValue = ""

            #Get the type of each param
            if param.find('type') is not None:
                paramType = param.find('type').text
            else:
                print("Type not available for ", param.find('name').text)
                # If type not found, then no point in testing the DM, so skipping
                continue

            # Some parameters will have expected set of values and some may not
            if param.find('expectedValues')is not None:
                expectedValues = param.find('expectedValues').text
                #if expectedValues in xml is non-empty
                if expectedValues is not None:
                    # For lists that come as range(0, 100) or range(10)
                    if "range(" in expectedValues:
                        if "," in expectedValues:
                            minval = expectedValues.split("range(")[1].split(",")[0].strip()
                            maxval = expectedValues.split(")")[0].split(",")[1].strip()
                            expectedValues = "[" + minval + ":" + maxval + "]"
                            expectedValues = [str(expectedValues)]
                        else:
                            maxval = expectedValues.split(")")[0].split("range(")[1].strip()
                            expectedValues = "[:" + maxval + "]"
                            expectedValues = [str(expectedValues)]
                    else:
                        expectedValues = expectedValues.split(",")
                        expectedValues = [val.strip(' ') for val in expectedValues]

            # If paramType is boolean and expectedValues is empty, create expectedValues list
            elif param.find('type') is not None:
                if param.find('type').text == "boolean":
                    expectedValues = ["true", "false"]
                # if expectedValues is not known and that tag itself is not available in xml
                else:
                    expectedValues = ""

            if setup_type in ["TDK", "WEBPA"]:
                paramName = param.find('name').text
            else:
                moduleStatus = "FAILURE"
                print("Invalid setup type passed !!!")
                return moduleStatus,failedParams

            expectedresult="SUCCESS"

            print("*************Start validation of %s **************" %paramName)
            #if get operation is to be done with factory reset, cross check parameter's get value with default value list other wise with expectedvalues list
            if factoryReset == "false":
                total = total + 1

                actualresult, typeChecked, valueChecked = getParameterValue(obj, setup_type, paramName, paramType, expectedValues)

                if typeChecked == 1:
                    typeTestCount = typeTestCount + 1
                if valueChecked == 1:
                    valueCheckCount = valueCheckCount + 1
            else:
                # TODO FR use-case
                actualresult, typeTestCount, valueCheckCount = getParameterValue(obj, setup_type, paramName, paramType, defaultValue)
            if expectedresult in actualresult:
                print("*************Validation of %s is SUCCESS**************\n" %paramName)
            else:
                print("*************Validation of %s is FAILURE**************\n" %paramName)
                componentStatus = "FAILURE"
                failedParams.append(paramName)

        # The final count dict
        totalCount = {"total" : total, "typeTestCount" : typeTestCount, "valueCheckCount" : valueCheckCount}

    elif testtype == "readOnlySet":
        setValueDict = { "boolean" : "true", "unsignedInt" : "1", "int" : "1", "string" : "stringDummy", "single" : "3.14", \
                        "double" : "3.14141414114", "dateTime" : "2000-05-24T23:28:08Z", "byte" : "A", \
                        "bytes" : "AB" }
        for param in paramsRoot:
            paramName = param.find('name').text
            if param.find('writable') is not None:
                if param.find('writable').text == "false":

                    # Get the type of parameter:
                    if param.find('type') is not None:
                        paramType = param.find('type').text
                        #String type can have the max length
                        if "string" in paramType:
                            paramType = "string"
                        # Pick the setValue from based on the type
                        setValue = setValueDict[paramType]

                        # Map the paramType to int if required
                        if setup_type == "WEBPA":
                            mapping = { "string" : 0, "int" : 1, "unsignedInt" : 2, "boolean" : 3, "dateTime" : 4, "bytes" : 5}
                            paramType = mapping.get(paramType)
                    else:
                        print("\nType not found for ", paramName)
                        # If type is not available, then no point in testing the DM
                        continue
                else:
                    continue
            else:
                # if writable tag not present, do not test
                print("\nAccess not found for ", paramName)
                continue

            #When we attempt to write read-only paramters, expected error code must be returned
            if setup_type == "TDK":
                expectedresult=["FAILURE", tdkbDmlModuleList.SetReadOnlyReturnCode, ""]
            elif setup_type == "WEBPA":
                expectedresult=["FAILURE", tdkbDmlModuleList.SetReadOnlyWebpaReturnCode, tdkbDmlModuleList.SetReadOnlyWebpaReturnMsg]

            print("*************Start validation of %s **************" %paramName)
            #Call Set function
            total = total + 1
            actualresult, errorCode, errorMsg  = setReadOnlyParameterValue(obj, setup_type, paramName, paramType, expectedresult, setValue)
            if expectedresult[0] in actualresult and expectedresult[1] == errorCode and  expectedresult[2] == errorMsg:
                print("*************Read-only compliance validation of %s is SUCCESS**************\n" %paramName)
            else:
                print("*************Read-only compliance validation of %s is FAILURE**************\n" %paramName)
                componentStatus = "FAILURE"
                failedParams.append(paramName)
        totalCount = total

    elif testtype == "writeAccessCompliance":
        for param in paramsRoot:
            paramName = param.find('name').text
            if param.find('writable') is not None:
                if param.find('writable').text == "true":

                    # Get the type of parameter:
                    if param.find('type') is not None:
                        paramType = param.find('type').text
                        #String type can have the max length
                        if "string" in paramType:
                            paramType = "string"

                        # Map the paramType to int if required
                        if setup_type == "WEBPA":
                            mapping = { "string" : 0, "int" : 1, "unsignedInt" : 2, "boolean" : 3, "dateTime" : 4, "bytes" : 5}
                            paramType = mapping.get(paramType)
                    else:
                        print("\nType not found for ", paramName)
                        # If type is not found, then no point in testing the DM
                        continue
                else:
                    continue
            else:
                print("\nAccess not found for ", paramName)
                continue

            #When we attempt to write paramters that have write access we should never get the read-only error code
            if setup_type == "TDK":
                resultCheck=["FAILURE", tdkbDmlModuleList.SetReadOnlyReturnCode, ""]
            elif setup_type == "WEBPA":
                resultCheck=["FAILURE", tdkbDmlModuleList.SetReadOnlyWebpaReturnCode, tdkbDmlModuleList.SetReadOnlyWebpaReturnMsg]

            print("*************Start validation of %s **************" %paramName)
            #Call function
            actualresult, errorCode, returnMsg, complianceChecked = writeAccessComplianceTest(obj, setup_type, paramName, paramType, resultCheck)
            if resultCheck[0] in actualresult and resultCheck[1] == errorCode and resultCheck[2] == returnMsg:
                print("*************Write access compliance validation of %s is FAILURE**************\n" %paramName)
                componentStatus = "FAILURE"
                failedParams.append(paramName)
            elif resultCheck[0] in actualresult and errorCode  == "":
                print("*************Write access compliance validation of %s is NOT done!!!**************\n" %paramName)
                componentStatus = "FAILURE"
                failedParams.append(paramName)
            else:
                print("*************Write access compliance validation of %s is SUCCESS**************\n" %paramName)

            if complianceChecked == 1:
                total = total + 1
        totalCount = total

    elif testtype == "writeTypeCompliance":
        for param in paramsRoot:
            paramName = param.find('name').text
            if param.find('writable') is not None:
                if param.find('writable').text == "true":

                    # Get the type of parameter:
                    if param.find('type') is not None:
                        paramType = param.find('type').text
                        #String type can have the max length
                        if "string" in paramType:
                            paramType = "string"

                        # Map the paramType to int if required
                        if setup_type == "WEBPA":
                            mapping = { "string" : 0, "int" : 1, "unsignedInt" : 2, "boolean" : 3, "dateTime" : 4, "bytes" : 5}
                            paramType = mapping.get(paramType)
                    else:
                        print("\nType not found for ", paramName)
                        # If type is not available, no point in testing the DM
                        continue
                else:
                    continue
            else:
                print("\nAccess not found for ", paramName)
                continue

            # When we attempt to write paramters that have write access with an invalid type, we should get the expected error code
            if setup_type == "TDK":
                resultCheck=["FAILURE", tdkbDmlModuleList.SetWithInvalidTypeReturnCode, ""]
            elif setup_type == "WEBPA":
                resultCheck=["FAILURE", tdkbDmlModuleList.SetWithInvalidTypeWebpaReturnCode, tdkbDmlModuleList.SetWithInvalidTypeWebpaReturnMsg]

            print("*************Start validation of %s **************" %paramName)
            #Call function
            actualresult, errorCode, errorMsg, complianceChecked = writeTypeComplianceTest(obj, setup_type, paramName, paramType, resultCheck)
            if resultCheck[0] in actualresult and resultCheck[1] == errorCode and resultCheck[2] == errorMsg:
                print("*************Write type compliance validation of %s is SUCCESS**************\n" %paramName)
            elif resultCheck[0] in actualresult and errorCode  == "":
                print("*************Write type compliance validation of %s is NOT done!!!**************\n" %paramName)
                componentStatus = "FAILURE"
                failedParams.append(paramName)
            else:
                print("*************Write access compliance validation of %s is FAILURE**************\n" %paramName)
                componentStatus = "FAILURE"
                failedParams.append(paramName)

            if complianceChecked == 1:
                total = total + 1
        totalCount = total

    return componentStatus, failedParams, totalCount

# writeAccessComplianceTest
# Syntax      : writeAccessComplianceTest(obj, setup_type, paramName, paramType, resultCheck)
# Description : Function to perform the write-access compliance test
# Parameters  : obj - TR181/sysutil stub object
#               setup_type - protocol used for conducting tests
#               paramName - name of the DM to be tested
#               paramType - data type of the DM
#               resultCheck - the error code returned if the complaince test failed for the DM
# Return Value: actualresult - SUCCESS/FAILURE state of the test
#               errorCode - returns empty string for success and the errorcode for failed tests
#               errorMsg - return message from the test
#               complianceChecked - whether the complaince was tested successfully for the DM

def writeAccessComplianceTest(obj, setup_type, paramName, paramType, resultCheck):

    global step
    actualresult= "FAILURE"
    expectedresult = "SUCCESS"
    errorCode = ""
    errorMsg = ""
    complianceChecked = 0

    # Get the current value of the parameter
    if setup_type == "TDK":
        tdkTestObj = obj.createTestStep("TDKB_TR181Stub_Get")
        tdkTestObj.addParameter("ParamName",paramName)
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        value = tdkTestObj.getResultDetails().replace("\\n", "")
        value = value.strip()
    elif setup_type == "WEBPA":
        queryParam = {"name": paramName}
        queryResponse = webpaQuery(obj, queryParam)
        parsedResponse = parseWebpaResponse(queryResponse, 1)
        value = parsedResponse[1].strip()

        if "SUCCESS" in parsedResponse[0]:
            actualresult = "SUCCESS"

        # To set result status
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        tdkTestObj.executeTestCase("SUCCESS")

    step = step + 1
    print(f"TEST STEP {step}: Get the current value of {paramName}")
    print(f"EXPECTED RESULT {step}: The parameter value should be successfully retrieved")

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT : Parameter value: \"{value}\"")
        print("TEST EXECUTION RESULT: SUCCESS")

        # Call the SET operation with the value retrieved from get operation above
        if setup_type == "TDK":
            tdkTestObj = obj.createTestStep("TDKB_TR181Stub_SetOnly")
            tdkTestObj.addParameter("ParamName",paramName)
            tdkTestObj.addParameter("ParamValue",value)
            tdkTestObj.addParameter("Type",paramType)
            tdkTestObj.executeTestCase(expectedresult)
            actualresult = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails().replace("\\n", "")
            complianceChecked = 1

        elif setup_type == "WEBPA":
            queryParam = {"name": paramName, "value": value, "dataType": paramType}
            queryResponse = webpaQuery(obj, queryParam,"set")
            setResponse = parseWebpaResponse(queryResponse, 1, "dmlWriteAccess")
            details = setResponse[1].strip()
            actualresult = setResponse[0]
            complianceChecked = 1

            # To set result status
            tdkTestObj = obj.createTestStep('ExecuteCmd')
            tdkTestObj.executeTestCase("SUCCESS")

        step = step + 1
        print(f"\nTEST STEP {step}: Perform write access compliance test on the writable param {paramName}")
        print(f"EXPECTED RESULT {step}: Write access compliance should not fail with errorcode : {resultCheck[1]}")

        if resultCheck[0] == actualresult:
            if setup_type == "TDK":
                errorCode = details.split("Errorcode: ")[1]
                errorMsg = ""
            elif setup_type == "WEBPA":
                print(f"In case of WEBPA testing, return message cannot be {resultCheck[2]}")
                errorCode = details.split("statusCode: ")[1]
                errorMsg = details.split("Message: ")[1].split(",")[0]

            if errorCode == resultCheck[1] and errorMsg == resultCheck[2]:
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT : Setting {paramName} to \"{value}\": {details}")
                print("TEST EXECUTION RESULT: FAILURE")
            else:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT : Setting {paramName} to \"{value}\": {details}")
                print("TEST EXECUTION RESULT: SUCCESS")
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT : Setting {paramName} to \"{value}\": {details}")
            print("TEST EXECUTION RESULT: SUCCESS")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT : {value}")
        print("TEST EXECUTION RESULT: FAILURE")

        print("--------------------------------------------------------------------------------------")
    return actualresult, errorCode, errorMsg, complianceChecked


# writeTypeComplianceTest
# Syntax      : writeTypeComplianceTest(obj, setup_type, paramName, paramType, resultCheck)
# Description : Function to perform the write-type compliance test
# Parameters  : obj - TR181/sysutil stub object
#               setup_type - protocol used for conducting tests
#               paramName - name of the DM to be tested
#               paramType - data type of the DM
#               resultCheck - the error code expected to be returned if the complaince test passes for the DM
# Return Value: actualresult - SUCCESS/FAILURE state of the test
#               errorCode - returns empty string for failed tests and the errorcode for success tests
#               errorMsg - returns the error message from the test
#               complianceChecked - whether the complaince was tested successfully for the DM

def writeTypeComplianceTest(obj, setup_type, paramName, paramType, resultCheck):

    global step
    actualresult= "FAILURE"
    expectedresult = "SUCCESS"
    errorCode = ""
    errorMsg = ""
    complianceChecked = 0

    # Call the SET operation with invalid param type
    if setup_type == "TDK":
        # For write type compliance the invalidParamType dictionary will map a given type to an invalid type for a parameter
        invalidParamType = { 'boolean' : 'string', 'int' : 'boolean', 'unsignedInt' : 'int', \
                            'string' : 'unsignedInt', 'dateTime' : 'string', 'single' : 'double', \
                            'double' : 'single', 'byte' : 'bytes', 'bytes' : 'byte'}
        invalidType = invalidParamType[paramType]
        newValue = { 'boolean' : 'false', 'int' : '-20', 'unsignedInt' : '100', 'string' : 'dummystring', \
                    'dateTime' : '2026-02-25T12:00:00Z', 'single' : '3.14', 'double' : '3.14141414114', \
                    'byte' : 'A', 'bytes' : 'AB'}
        value = newValue[invalidType]
        tdkTestObj = obj.createTestStep("TDKB_TR181Stub_SetOnly")
        tdkTestObj.addParameter("ParamName",paramName)
        tdkTestObj.addParameter("ParamValue",value)
        tdkTestObj.addParameter("Type",invalidType)
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails().replace("\\n", "")
        complianceChecked = 1

    elif setup_type == "WEBPA":
        # In case of WEBPA test type, map the type to the integer
        # { "string" : 0, "int" : 1, "unsignedInt" : 2, "boolean" : 3, "dateTime" : 4, "bytes" : 5}
        # Bytes not accepted by webpa and dmcli, but acceptable via rbus
        # mapping = { 0 : 5, 1 : 4, 2 : 3, 3 : 2, 4 : 1, 5 : 0}
        # Workaround mapping for bytes datatype
        mapping = { 0 : 1, 1 : 4, 2 : 3, 3 : 2, 4 : 1, 5 : 0}
        invalidParamType = mapping.get(paramType)
        inverseMapping = { 0 : "string", 1 : "int", 2 : "unsignedInt", 3 : "boolean", 4 : "dateTime", 5 : "bytes"}
        paramType = inverseMapping.get(paramType)
        invalidType = inverseMapping.get(invalidParamType)
        newValue = { 'boolean' : 'false', 'int' : '-20', 'unsignedInt' : '100', 'string' : 'dummystring', \
                    'dateTime' : '2026-02-25T12:00:00Z', 'bytes' : 'AB'}
        value = newValue[invalidType]

        queryParam = {"name": paramName, "value": value, "dataType": invalidParamType}
        queryResponse = webpaQuery(obj, queryParam,"set")
        setResponse = parseWebpaResponse(queryResponse, 1, "dmlSetInvalidType")
        details = setResponse[1].strip()
        actualresult = setResponse[0]
        complianceChecked = 1

        # To set result status
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        tdkTestObj.executeTestCase("SUCCESS")

    step = step + 1
    print(f"\nTEST STEP {step}: Perform write type compliance test on the writable param {paramName} of type {paramType}")
    print(f"EXPECTED RESULT {step}: Write type compliance should fail with errorcode : {resultCheck[1]} with invalid type {invalidType}")

    if resultCheck[0] == actualresult:
        if setup_type == "TDK":
            errorCode = details.split("Errorcode: ")[1]
            errorMsg = ""
        elif setup_type == "WEBPA":
            print(f"In case of WEBPA testing, return message should be {resultCheck[2]}")
            errorCode = details.split("statusCode: ")[1]
            errorMsg = details.split("Message: ")[1].split(",")[0]

        if errorCode == resultCheck[1] and errorMsg == resultCheck[2]:
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT : Setting {paramName} using type \"{invalidType}\" and value \"{value}\": {details}")
            print("TEST EXECUTION RESULT: SUCCESS")
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT : Setting {paramName} using type \"{invalidType}\" and value \"{value}\": {details}")
            print("TEST EXECUTION RESULT: FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT : Write type compliant with invalid type : {details}")
        print("TEST EXECUTION RESULT: FAILURE")

    print("--------------------------------------------------------------------------------------")
    return actualresult, errorCode, errorMsg, complianceChecked

# setReadOnlyParameterValue
# Syntax      : setReadOnlyParameterValue(obj, setup_type, paramName, paramType, expectedresult, setValue)
# Description : Function to perform the read-only DM compliance test
# Parameters  : obj - TR181/sysutil stub object
#               setup_type - protocol to conduct the tests
#               paramName - name of the DM to be tested
#               paramType - data type of the DM
#               expectedresult - the expected result and error code for the test
#               setValue - value to be SET to the DM
# Return Value: actualresult - SUCCESS/FAILURE state of the test
#               errorCode - returns empty string for failed tests and the errorcode for success tests
#               errorMsg - returns the error msg returned by the test

def setReadOnlyParameterValue(obj, setup_type, paramName, paramType, expectedresult, setValue):

    global step
    actualresult= []
    errorCode = ""
    errorMsg = ""

    if setup_type == "TDK":
        tdkTestObj = obj.createTestStep("TDKB_TR181Stub_SetOnly")
        tdkTestObj.addParameter("ParamName",paramName)
        tdkTestObj.addParameter("ParamValue",setValue)
        tdkTestObj.addParameter("Type",paramType)
        tdkTestObj.executeTestCase(expectedresult[0])
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails().replace("\\n", "")
    elif setup_type == "WEBPA":
        queryParam = {"name": paramName, "value": setValue, "dataType": paramType}
        queryResponse = webpaQuery(obj, queryParam,"set")
        setResponse = parseWebpaResponse(queryResponse, 1, "dmlSetReadOnly")
        details = setResponse[1].strip()

        if expectedresult[0] in setResponse[0]:
            actualresult = expectedresult[0]

        # To set result status
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        tdkTestObj.executeTestCase("SUCCESS")

    step = step + 1
    print(f"TEST STEP {step}: Perform set operation on the read-only param {paramName}")
    print(f"EXPECTED RESULT {step}: Set operation on the read-only param should fail with errorcode : {expectedresult[1]}")

    if expectedresult[0] in actualresult:
        if setup_type == "TDK":
            errorCode = details.split("Errorcode: ")[1]
        elif setup_type == "WEBPA":
            print(f"In case of WEBPA testing, return message should be {expectedresult[2]}")
            errorCode = details.split("statusCode: ")[1]
            errorMsg = details.split("Message: ")[1].split(",")[0]

        if errorCode == expectedresult[1] and errorMsg == expectedresult[2]:
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT : SET operation failed, errorCode: {errorCode}")
            print("TEST EXECUTION RESULT: SUCCESS")
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT : {details}")
            print("TEST EXECUTION RESULT: FAILURE")
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT : {details}")
        print("TEST EXECUTION RESULT: FAILURE")

    print("--------------------------------------------------------------------------------------")
    return actualresult, errorCode, errorMsg

# getParameterValue
# Syntax      : getParameterValue(obj, setup_type, paramName, paramType, expectedValues)
# Description : Function to perform the data-type and GET value compliance test
# Parameters  : obj - TR181/sysutil stub object
#               setup_type - protocol used for conducting tests
#               paramName - name of the DM to be tested
#               paramType - data type of the DM
#               expectedValues - the expected value list for the testtype = "get"
# Return Value: actualresult - SUCCESS/FAILURE state of the test
#               errorCode - returns empty string for failed tests and the errorcode for success tests

def getParameterValue(obj, setup_type, paramName, paramType, expectedValues):

    global step
    expectedresult="SUCCESS"
    actualresult= []
    flag = "FAILURE"
    typeChecked = 0
    valueChecked = 0
    isValueInRange = 1

    if setup_type == "TDK":
        tdkTestObj = obj.createTestStep("TDKB_TR181Stub_Get")
        tdkTestObj.addParameter("ParamName",paramName)
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        value = tdkTestObj.getResultDetails().replace("\\n", "")
        value = value.strip()
    elif setup_type == "WEBPA":
        queryParam = {"name": paramName}
        queryResponse = webpaQuery(obj, queryParam)
        parsedResponse = parseWebpaResponse(queryResponse, 1)
        value = parsedResponse[1].strip()

        if "SUCCESS" in parsedResponse[0]:
            actualresult = "SUCCESS"

        # To set result status
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        tdkTestObj.executeTestCase("SUCCESS")

    # Start the type-compliance checks followed by the expected value checks
    if (expectedresult in actualresult) and paramType != "":
        typeChecked = 1
        step = step + 1
        if paramType == "boolean":
            print(f"TEST STEP {step}: Check if {paramName} is type-compliant")
            print(f"EXPECTED RESULT {step}: The GET value of the parameter should be of type {paramType}")
            if value in ["true", "false"]:
                flag = "SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is type-compliant")
                print("TEST EXECUTION RESULT: SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is NOT type-compliant")
                print("TEST EXECUTION RESULT: FAILURE")

        # If type is int or unsigned int expectedValues could be a range. Eg: [10:20]
        elif (paramType == "unsignedInt") or (paramType == "int"):
            print(f"TEST STEP {step}: Check if {paramName} is type-compliant")
            print(f"EXPECTED RESULT {step}: The GET value of the parameter should be of type {paramType}")

            if (paramType == "unsignedInt"):
                isVal = value.isdigit()
            else:
                isVal = value.strip("-").isdigit()

            if isVal:
                flag = "SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is type-compliant")
                print("TEST EXECUTION RESULT: SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is NOT type-compliant")
                print("TEST EXECUTION RESULT: FAILURE")

            if expectedValues != "" and "[" in expectedValues[0]:
                expectedValues = expectedValues[0]
                lower_limit = expectedValues.split("[")[1].split(":")[0]
                upper_limit = expectedValues.split("]")[0].split(":")[1]
                flag = "FAILURE"
                valueChecked = 1
                # Check if the value returned is a digit for type compliance
                # As of now ranges like [-1:2^31-1], [-2^31-1:0] etc is handled, only lower limit/ upper limit will be checked which is sufficient
                if value.strip("-").isdigit():
                    # Check if lower limit exists
                    if lower_limit.strip("-").isdigit() and upper_limit.strip("-").isdigit():
                        if int(value) >= int(lower_limit) and int(value) <= int(upper_limit):
                            flag = "SUCCESS"
                    elif lower_limit.strip("-").isdigit() and not upper_limit.strip("-").isdigit():
                        if int(value) >= int(lower_limit):
                            flag = "SUCCESS"
                    elif not lower_limit.strip("-").isdigit() and upper_limit.strip("-").isdigit():
                        if int(value) <= int(upper_limit):
                            flag = "SUCCESS"
                    else:
                        isValueInRange = 0

        elif "string" in paramType:
            flag = "SUCCESS"
            # If string length is provided, check type compliance. In some cases string: val1(1), val2(2) etc could be seen
            if "string(" in paramType:
                size_limit = paramType.split("(")[1].split(")")[0]
            # If string length is not provided, check if the GET value has size less than 1024
            else:
                size_limit = "1024"

            print(f"TEST STEP {step}: Check if {paramName} is type-compliant")
            print(f"EXPECTED RESULT {step}: Should get the {paramType} value with max size {size_limit}")

            actual_size = len(value)
            if (actual_size <= int(size_limit)):
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Value - [{value}] with size - {actual_size} is type-compliant")
                print("TEST EXECUTION RESULT : SUCCESS")
            else:
                flag = "FAILURE"
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Value - [{value}] with size - {actual_size} is NOT type-compliant")
                print("TEST EXECUTION RESULT: FAILURE")

            if expectedValues != "":
                # If it is a regex pattern
                if len(expectedValues) == 1:
                    regex_chars = set("[]{}()*+?|^$.\\")
                    if any(char in regex_chars for char in expectedValues[0]):
                        valueChecked = 1
                        match = re.fullmatch(expectedValues[0], value)
                        if not match:
                            isValueInRange = 0
                # If it is not a regex pattern check if its a list
                elif isinstance(expectedValues, list):
                    if value not in expectedValues:
                        isValueInRange = 0

        elif "single" == paramType or "double" == paramType:
            flag = "SUCCESS"
            print(f"TEST STEP {step}: Check if {paramName} is type-compliant")
            print(f"EXPECTED RESULT: {step} The GET value of the parameter should be of type {paramType}")
            try:
                float(value)
            except ValueError:
                flag = "FAILURE"

            if flag != "FAILURE":
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is type-compliant")
                print("TEST EXECUTION RESULT: SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is NOT type-compliant")
                print("TEST EXECUTION RESULT: FAILURE")

        elif "dateTime" == paramType:
            flag = "SUCCESS"
            # As per CWMP spec, certain DMs should have microsecond precision (for others it may not be needed), example: 2008-04-09T15:01:05.123456Z
            # The below format will handle both precision cases
            format_data = "%Y-%m-%dT%H:%M:%SZ"
            print(f"TEST STEP {step}: Check if {paramName} is type-compliant")
            print(f"EXPECTED RESULT {step}: The GET value of the parameter should be of type {paramType} with format {format_data}")
            try:
                date = datetime.strptime(value, format_data)
            except ValueError:
                flag = "FAILURE"

            # Handle NULL datetime "0000-00-00T00:00:00Z" as a special case
            # The minimum valid year in Python's datetime is 1 (i.e., 0001-01-01T00:00:00Z)
            if value == "0000-00-00T00:00:00Z":
                date = value
                flag = "SUCCESS"

            if flag != "FAILURE":
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Parameter value [{date}] is type-compliant")
                print("TEST EXECUTION RESULT: SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is NOT type-compliant")
                print("TEST EXECUTION RESULT: FAILURE")

        # The get value will be in hex for a byte type, check if the get value is a valid hex
        elif "byte" == paramType:
            flag = "SUCCESS"
            print(f"TEST STEP {step}: Check if {paramName} is type-compliant")
            print(f"EXPECTED RESULT {step}: The GET value of the parameter should be of type {paramType}")
            try:
                # For byte data, the valid hex types are from 32-127
                conv_value = int(value, 16)
                # Allow full byte range (0-255), not just ASCII printable characters (32-127)
                if not (0 <= conv_value <= 255):
                    flag = "FAILURE"
            except ValueError:
                flag = "FAILURE"

            if flag != "FAILURE":
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is type-compliant")
                print("TEST EXECUTION RESULT: SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is NOT type-compliant")
                print("TEST EXECUTION RESULT: FAILURE")

        # The get value will be in hex for a bytes type. Eg: 4142 will be AB in bytes 41-A & 42-B
        elif "bytes" == paramType:
            flag = "SUCCESS"
            print(f"TEST STEP {step}: Check if {paramName} is type-compliant")
            print(f"EXPECTED RESULT {step}: The GET value of the parameter should be of type {paramType}")
            # Check if length of get string is a multiple of 2
            if len(value) % 2 != 0:
                flag = "FAILURE"
            else:
                # Split the entire get value into groups of 2 chars each
                for i in range(0, len(value), 2):
                    hex_value = value[i:i+2]

                    try:
                        # For byte data, the valid hex types are from 32-127
                        conv_value = int(hex_value, 16)
                        # Allow full byte range (0-255), not just ASCII printable characters (32-127)
                        if not (0 <= conv_value <= 255):
                            flag = "FAILURE"
                            break
                    except ValueError:
                        flag = "FAILURE"
                        break

            if flag != "FAILURE":
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is type-compliant")
                print("TEST EXECUTION RESULT: SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Parameter value [{value}] is NOT type-compliant")
                print("TEST EXECUTION RESULT: FAILURE")

        # Perform the expected value check only if expected value ranges are available
        if expectedValues != "":
            valueChecked = 1
            flag = "FAILURE"
            step = step + 1
            print(f"\nTEST STEP {step}: Check if the GET value of {paramName} is from the expected value list")
            print(f"EXPECTED RESULT {step}: Should get one of the values from {expectedValues}")
            # In case the GET value is a single value (with no comma separators)
            if "," not in value:
                # For int, uint paramTypes, expected value check has already been handled. In some cases for string type also it has been handled.
                if paramType == "int" or paramType == "unsignedInt" or "string" in paramType:
                    if isValueInRange == 1:
                        flag = "SUCCESS"
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Value - [{value}] is from the expected value list")
                        print("TEST EXECUTION RESULT: SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Value - [{value}] is NOT from the expected value list")
                        print("TEST EXECUTION RESULT: FAILURE")
                elif value in expectedValues and isValueInRange == 1:
                    flag = "SUCCESS"
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Value - [{value}] is from the expected value list")
                    print("TEST EXECUTION RESULT: SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Value - [{value}] is NOT from the expected value list")
                    print("TEST EXECUTION RESULT: FAILURE")
            else:
                value = value.split(',')
                outOfRangeFlag = 0

                for val in value:
                    if val not in expectedValues:
                        outOfRangeFlag = 1
                        break
                if outOfRangeFlag == 0:
                    flag = "SUCCESS"
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Value - [{value}] is from the expected value list")
                    print("TEST EXECUTION RESULT: SUCCESS")
                else:
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Value - [{value}] contains [{val}] which is not in the expected value list")
                    print("TEST EXECUTION RESULT: FAILURE")
        else:
            print("--------------------------------------------------------------------------------------")
            print("Cannot validate the return value of param as expected values are not known !!!")
            print("--------------------------------------------------------------------------------------")

    elif paramType == "":
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE")
        print("--------------------------------------------------------------------------------------")
        print("Cannot validate the value of param as type is not known !!!")
        print("--------------------------------------------------------------------------------------")

    else:
        step = step + 1
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE")
        flag = "FAILURE"
        print(f"TEST STEP {step}: Get the value of the parameter {paramName}")
        print(f"EXPECTED RESULT {step}: Should retrieve the GET value successfully")
        print(f"ACTUAL RESULT : {value}")
        print("TEST EXECUTION RESULT: FAILURE")

    return (flag, typeChecked, valueChecked)

# cleanup
# Syntax      : cleanup(files)
# Description : Function to remove all intremediate files created during the test
# Parameters  : files - the list of files to be deleted
# Return Value: None

def cleanup(files):
    # Delete the secondary config
    print("\n--------------Start cleanup--------------")
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed {file}")
    print("--------------Completed !!!--------------\n")
    return
