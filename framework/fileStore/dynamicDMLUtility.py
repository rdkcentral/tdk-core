
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
from xml.dom.minidom import parseString
import json
import sys
import hashlib
import itertools
import re
import sys
import os
import tdklib
import tdkutility
import tdkbDmlModuleList

# get_full_dm_list
# Syntax      : get_full_dm_list(key_in_json_initial, number_of_entries, DML_name, loop_number, config, dm_list, source = "")
# Description : Recursive function that collects all the table instances of a DM. Eg: for DM A.B.{i}.C.{j}.Enable, the function will find
#               the current value of {i}, {j} and create a list like A.B.1.C.1.Enable, A.B.1.C.2.Enable,.. etc upto {i} and {j}
# Parameters  : key_in_json_initial - the table object name - Eg: A.B. or A.B.1.C.
#               number_of_entries - the parameter to keep track of the number of current table instances
#               DML_name - the name of the DM. Eg: A.B.{i}.C.{j}.Enable
#               loop_number - the parameter to keep track of the table parts in the DM
#               config - the secondary configuration file to fetch the table number of instances
#               dm_list - the list of DMs resolved by the function. Eg: [A.B.1.C.1.Enable, A.B.1.C.2.Enable, etc]
#               source - if empty it denotes components which update a parameter "NumberOfEntries" based on number of
#                        table instances. Eg: A.BNumberOfEntries, A.B.1.CNumberOfEntries. If "source_file" it denotes components
#                        which do not have a corresponding "NumberOfEntries" parameter to update the number of table instances
# Return Value: None

def get_full_dm_list(key_in_json_initial, number_of_entries, DML_name, loop_number, config, dm_list, source = ""):
    # Index variable to keep track of the last object name
    loop_number = loop_number + 1
    if source == "":
        for i in range(1, int(number_of_entries) + 1):
            key_in_json = key_in_json_initial + "." + str(i) + "." + DML_name[loop_number]
            number_of_entries_key = f"{key_in_json}NumberOfEntries"
            pair_value = number_of_entries_key.split(".")[-1]
            try:
                if number_of_entries_key in config:
                    number_of_entries = config[number_of_entries_key].get(pair_value)
                    get_full_dm_list(key_in_json, number_of_entries, DML_name, loop_number, config, dm_list)
                else:
                    # Append to the list of DMs
                    dm_list.append(key_in_json)
            except Exception as e:
                print("ERROR: ",e)

    elif source == "source_file":
        for i in range(1, int(number_of_entries) + 1):
            key_in_json = key_in_json_initial +  str(i) + "." + DML_name[loop_number]
            number_of_entries_key = key_in_json + ".{i}."
            pair_value = "NumberOfEntries"
            try:
                if number_of_entries_key in config:
                    number_of_entries = config[number_of_entries_key].get(pair_value)
                    key_in_json = key_in_json + "."
                    get_full_dm_list(key_in_json, number_of_entries, DML_name, loop_number, config, dm_list, source)
                else:
                    # Append to the list of DMs
                    dm_list.append(key_in_json)
            except Exception as e:
                print("ERROR: ",e)

    return

# get_NumberOfEntries
# Syntax      : get_NumberOfEntries(path, json_config_filename
# Description : Wrapper function that invokes the recursive function get_full_dm_list() to collect all the table instances of a DM
# Parameters  : path - the table object name - Eg: A.B.{i}.
#               json_config_filename - the secondary configuration file to fetch the table number of instances
# Return Value: dm_list - returns the list of all table instances of a DM

def get_NumberOfEntries(path, json_config_filename):

    number_of_entries = 0

    with open(json_config_filename, 'r') as file:
        config = json.load(file)

    DML_name = path.split(".{i}.")
    key_in_json = DML_name[0]
    # Index variable to keep track of the last object name
    loop_number = 0
    # Variable to check if the Table is from a source file
    sourceFileTable = 0

    # If the config has "NumberOfEntries" for tables
    try:
        number_of_entries_key = f"{key_in_json}NumberOfEntries"
        pair_value = number_of_entries_key.split(".")[-1]
        number_of_entries = config[number_of_entries_key].get(pair_value)
    except KeyError:
        # The config uses ".{i}." for tables
        # denotes components which do not have a corresponding "NumberOfEntries" parameter to update the number of table instances
        sourceFileTable = 1

    if sourceFileTable == 1:
        try:
            number_of_entries_key = key_in_json + ".{i}."
            pair_value = "NumberOfEntries"
            number_of_entries = config[number_of_entries_key].get(pair_value)

            # Indicate that table is from source file
            if number_of_entries is not None:
                sourceFileTable = "source_file"
        except KeyError:
            # Number of Table rows not found for the DM, hence skipping
            print(f"ERROR: Number of Table rows not found, skipping {path}!!!")

    # Build the DMs
    dm_list = []
    if int(number_of_entries) != 0:
        if sourceFileTable != "source_file":
            get_full_dm_list(key_in_json, number_of_entries, DML_name, loop_number, config, dm_list)
        else:
            key_in_json = key_in_json + "."
            get_full_dm_list(key_in_json, number_of_entries, DML_name, loop_number, config, dm_list, sourceFileTable)

    return dm_list

# create_xml_tags_from_json
# Syntax      : create_xml_tags_from_json(new_parameter, name, json_config_filename)
# Description : Function to parse through the config file and create XML tags from the data stored in config
# Parameters  : new_parameter - the new element to be added to the XML
#               name - name of the DM
#               json_config_filename - the secondary configuration file to fetch all the attributes of the new parameter element
# Return Value: None

def create_xml_tags_from_json(new_parameter, name, json_config_filename):

    with open(json_config_filename, "r") as json_file:
        json_data = json.load(json_file)

        # If the DM name is found in config
        if name in json_data:
            for tag, values in json_data[name].items():
                # Consider all config fields except flags
                if tag != "flags":
                    new_tag = ET.Element(tag)

                    if isinstance(values, dict):
                        value = json_data[name][tag]

                    elif isinstance(values, list):
                        value = ", ".join(values)

                    if value:
                        new_tag.text = value

                        # Add a comment based on the tag type
                        comment = None
                        if tag == "type":
                            comment = ET.Comment("type of the parameter")
                        elif tag == "writable":
                            comment = ET.Comment("whether set is applicable or not")
                        elif tag == "defaultValue":
                            comment = ET.Comment("default value of the param after factory reset")
                        elif tag == "expectedValues":
                            comment = ET.Comment("expected value of the param")
                        elif tag == "persistentSet":
                            comment = ET.Comment("whether set value will be retained and set should be followed by a get or not")
                        else:
                            comment = "None"

                        # Append the comment before the new tag
                        if comment != "None":
                            new_parameter.append(comment)
                            # Append the new tag itself
                            new_parameter.append(new_tag)
    return

# create_xml
# Syntax      : create_xml(json_file_path, xml_file_path)
# Description : Function to create test XML based on the configuration file of a component
# Parameters  : json_file_path - os file path to the dynamic configuration file
#               xml_file_path - os file path location where the test XML needs to be created
# Return Value: DM_tracker - list of all DMs populated in the dynamic test XML

def create_xml(json_file_path, xml_file_path):

    # Create the root XML element
    root = ET.Element('parameters')
    DM_tracker = []

    try:
        # Open and read the JSON configuration file
        with open(json_file_path, 'r') as file:
            config = json.load(file)

        parameter_names = config.keys()
        if parameter_names != []:
            print("\nx--------------Start creating Dynamic XML--------------x")
            for parameter_name in parameter_names:
                DM_tracker.append(parameter_name)

                # Skip parameters that are of method type as L1 tests based on XMLs do not require these
                element_type = config[parameter_name].get("elementType", None)

                # All the DMs that are added from the source files will have the element type
                if element_type is not None:
                    if element_type[0] != "RBUS_ELEMENT_TYPE_METHOD" and element_type[0] != "bus_element_type_method":
                        append_dml_to_root(root, parameter_name, json_file_path)
                    else:
                       # Skipping element
                       continue
                else:
                    # For those DMs which do not have element_type
                    append_dml_to_root(root, parameter_name, json_file_path)

            #Converting the New XML Tree to a Bytes String
            new_xml_str = ET.tostring(root, encoding='utf-8')

            #Parsing the Bytes String into a DOM Object
            dom = parseString(new_xml_str)

            #Generates a string with added indentation for each level of the XML tree
            pretty_xml_as_string = dom.toprettyxml(indent="  ")

            # Optionally, write the new XML to a file
            with open(xml_file_path, 'w') as file:
                file.write(pretty_xml_as_string)

            if DM_tracker != []:
                print("\nx--------------Created Dynamic XML--------------x")
            else:
                print("\nx--------------Dynamic XML not created as no table entries are present--------------x\n")

    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON file.")
    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return DM_tracker

# format_json
# Syntax      : format_json(config)
# Description : Function to format the input dictionary into a json format string that can be written to files
# Parameters  : config - dictionary to be formatted to a json string
# Return Value: json_str - the json formatted dictionary as string

def format_json(config):
    json_str = json.dumps(config, indent=4)

    # Replace multiline lists with single-line lists
    json_str = re.sub(r'\[\s*([^]]*?)\s*\]', lambda m: '[' + re.sub(r'\s*,\s*', ',', m.group(1)) + ']', json_str)

    return json_str

# get_all_dms
# Syntax      : get_all_dms(dm_initial, entry_value, dm_names, loop_number, config, dm_list, source="")
# Description : Recursive function that appends all table number of entries parameters resolved dynamically to the configuration file
# Parameters  : dm_initial - the table object name - Eg: A.B. or A.B.1.C.
#               entry_value - the parameter to keep track of the number of current table instances
#               dm_names - the name of the DM. Eg: A.B.{i}.C.{j}.Enable
#               loop_number - the parameter to keep track of the table parts in the DM
#               config - the secondary configuration file to fetch the table number of instances and also to append the resolved NumberOfEntries parameters
#               dm_list - the list of DMs resolved by the function. Eg: [A.B.1.C.1.Enable, A.B.1.C.2.Enable, etc]
#               source - if empty it denotes components which update a parameter "NumberOfEntries" based on number of
#                        table instances. Eg: A.BNumberOfEntries, A.B.1.CNumberOfEntries. If "source_file" it denotes components
#                        which do not have a corresponding "NumberOfEntries" parameter to update the number of table instances
# Return Value: None

def get_all_dms(dm_initial, entry_value, dm_names, loop_number, config, dm_list, source=""):
    loop_number = loop_number + 1

    if source == "":
        for i in range (1, int(entry_value) + 1):
            dm = dm_initial + "." + str(i) + "." + dm_names[loop_number]
            if "NumberOfEntries" not in dm:
                key_in_json = dm + "NumberOfEntries"
                pair_value = key_in_json.split(".")[-1]
            else:
                dm_list.append(dm)
                pair_value = dm.split(".")[-1]
                config[dm] = { pair_value : "" }
            try:
                if key_in_json in config:
                    entry_value = config[key_in_json].get(pair_value)
                    get_all_dms(dm, entry_value, dm_names, loop_number, config, dm_list)
            except Exception as e:
                continue

    elif source == "source_file":
        for i in range (1, int(entry_value) + 1):
            dm = dm_initial + str(i) + "." + dm_names[loop_number] + "."
            pair_value = "NumberOfEntries"
            key_in_json = dm + "{i}."
            if key_in_json not in config:
                dm_list.append(dm)
                config[key_in_json] = { pair_value : "" }
            try:
                if key_in_json in config:
                    entry_value = config[key_in_json].get(pair_value)
                    get_all_dms(dm, entry_value, dm_names, loop_number, config, dm_list, "source_file")
            except Exception as e:
                continue
    return

# getNumberOfTableRows
# Syntax      : getNumberOfTableRows(rbusobj, tableName)
# Description : Function to retrieve the number of table instances using the RBUS API rbusTable_getRowNames() for tables that
#               so not have a "NumberOfEntries" parameter which holds the number of instances.
# Parameters  : rbusobj - RBUS stub object
#               tableName - the table name for which number of instances need to be determined
# Return Value: actualresult - SUCCESS if rbus_open(), rbusTable_getRowNames() and rbus_close() are successful else FAILURE
#               numberOfRows - number of table instances retrieved

def getNumberOfTableRows(rbusobj, tableName):
    numberOfRows = -1
    # Open rbus connection
    tdkTestObj = rbusobj.createTestStep('RBUS_Open')
    expectedresult = "SUCCESS"
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()

    if expectedresult in actualresult:
        # Get Number of rows for a table
        tdkTestObj = rbusobj.createTestStep('RBUS_TableRowCommands')
        tdkTestObj.addParameter("operation","rbusTable_getRowNames")
        tdkTestObj.addParameter("table_row",tableName)
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        ins_num = tdkTestObj.getResultDetails()

        if expectedresult in actualresult and ins_num.isdigit():
            numberOfRows = ins_num

            # Close rbus connection
            tdkTestObj = rbusobj.createTestStep('RBUS_Close')
            tdkTestObj.executeTestCase(expectedresult)
            actualresult = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails()

            if expectedresult not in actualresult:
                numberOfRows = -1

    return actualresult, numberOfRows

# query_param
# Syntax      : query_param(parameter_Name, tr181Obj, rbusObj, config, compName, source = "")
# Description : Wrapper function to retrieve the number of table instances either from the table's NumberOfEntries parameter
#               or from the RBUS API rbusTable_getRows()
# Parameters  : parameter_Name - name of the parameter to be queried
#               tr181Obj - TR181 stub object
#               rbusObj - RBUS stub object
#               config - secondary config of the component
#               compName - name of the component under test
#               source - if empty it denotes components which update a parameter "NumberOfEntries" based on number of
#                        table instances. Eg: A.BNumberOfEntries, A.B.1.CNumberOfEntries. If "source_file" it denotes components
#                        which do not have a corresponding "NumberOfEntries" parameter to update the number of table instances
# Return Value: None

def query_param(parameter_Name, tr181Obj, rbusObj, config, compName, source = ""):
    expectedresult = "SUCCESS"

    if source == "":
        # Create new instance of test object
        tdkTestObj = tr181Obj.createTestStep('TDKB_TR181Stub_Get')

        actualresult, details = tdkutility.getTR181Value(tdkTestObj, parameter_Name)
        print(f"{parameter_Name} : {details}")
        config_parameter_Name = parameter_Name

    elif source == "source_file":
        print(f"Parameter name for getrows: {parameter_Name}")
        actualresult, details = getNumberOfTableRows(rbusObj, parameter_Name)

        # Before adding to config, add the {i}
        config_parameter_Name = parameter_Name + "{i}."
        if int(details) != -1:
            print(f"{config_parameter_Name} : {details}")
        else:
            print(f"{config_parameter_Name} : Table Row count not fetched")

    if actualresult in expectedresult and (details != "" or int(details) != -1):

        # Check if the Table is applicable under the component
        # Eg: Device.DHCPv4.Client. table comes under PAM and WANMANAGER, hence we need to confirm with getnames
        # In this case recursive getnames query is not required
        newNamespaces, _, _ = getNames(expectedresult, rbusObj, parameter_Name, compName, recursion="false")

        # Remove the trailing ""
        newNamespaces.remove("")

        # Empty, meaning Table not applicable for the component
        if len(newNamespaces) == 0:
            update_config(config_parameter_Name, "Failed to get table row count",  config, compName, source)
        else:
            update_config(config_parameter_Name, details,  config, compName, source)
    # Due to Failure in getting param value
    # This also implies that the table is not applicable
    else:
        update_config(config_parameter_Name, "Failed to get table row count",  config, compName, source)
    return

# get_param_and_query
# Syntax      : get_param_and_query(config, tr181Obj, rbusObj, compName)
# Description : Wrapper function to parse through a runtime configuration, resolve the number of table instances dynamically and
#               update the configuration
# Parameters  : config - secondary config of the component
#               tr181Obj - TR181 stub object
#               rbusObj - RBUS stub object
#               compName - name of the component under test
# Return Value: dict_to_append - a copy of the original run-time config updated with the "NumberOfEntries" keys appended based
#               on run-time resolution of the tables

def get_param_and_query(config, tr181Obj, rbusObj, compName):

    dict_to_append = config.copy()

    # Search for keys containing 'NumberOfEntries'
    for key, _ in config.items():
        if "NumberOfEntries" in key:
            if "{i}" in key:
                dm_names =key.split(".{i}.")
                key_in_json = dm_names[0] + "NumberOfEntries"
                pair_value = key_in_json.split(".")[-1]
                dm_initial = dm_names[0]
                dm_list = []
                loop_number = 0
                # Get the key value
                try:
                    if key_in_json in config:
                        entry_value = config[key_in_json].get(pair_value)
                        if entry_value is None:
                            print(f"The value is missing from the JSON data for '{key_in_json}'. Unable to get i_value")
                        else:
                            get_all_dms(dm_initial, entry_value, dm_names, loop_number, dict_to_append, dm_list)
                            for dm in dm_list:
                                query_param(dm, tr181Obj, rbusObj, dict_to_append, compName)
                except ValueError:
                    print(f"The value for the key: {key_in_json} is empty or None. Unable to get i_value")
            else:
                query_param(key, tr181Obj, rbusObj, dict_to_append, compName)

        # Tables added via source files will end with .{i}.
        elif key.endswith(".{i}."):
            dm_names = key.split(".{i}.")
            key_in_json = dm_names[0] + ".{i}."
            dm_initial = dm_names[0] + "."
            loop_number = 0
            dm_list = []
            try:
                entry_value = config[key_in_json].get("NumberOfEntries")
                if entry_value is None:
                    print(f"The value is missing from the JSON data for '{key_in_json}'. Unable to get i_value")
                else:
                    # Ensure that entry_value has been populated for the table
                    if entry_value.isdigit():
                        get_all_dms(dm_initial, entry_value, dm_names, loop_number, dict_to_append, dm_list, "source_file")
                        for dm in dm_list:
                            query_param(dm, tr181Obj, rbusObj, dict_to_append, compName, "source_file")
                    # Else populate the entry value
                    else:
                        query_param(dm_initial, tr181Obj, rbusObj, dict_to_append, compName, "source_file")
            except ValueError:
                print(f"The value for the key: {key_in_json} is empty or None. Unable to get i_value")

    return dict_to_append

# update_config
# Syntax      : update_config(DML_name, DML_value, config, compName, source = "")
# Description : Function to update the secondary run-time config based on the values fetched from query_param()
# Parameters  : DML_name - name of the table entry DM
#               DML_value - parameter holding the number of table instance of DML_name
#               config - secondary config of the component
#               compName - name of the component under test
#               source - if empty it denotes components which update a parameter "NumberOfEntries" based on number of
#                        table instances. Eg: A.BNumberOfEntries, A.B.1.CNumberOfEntries. If "source_file" it denotes components
#                        which do not have a corresponding "NumberOfEntries" parameter to update the number of table instances
# Return Value: None

def update_config(DML_name, DML_value, config, compName, source = ""):

    for key, _ in config.items():
        if key == DML_name:
            # Need not consider the table for table validation tests
            if DML_value == "Failed to get table row count":
                config[key]["ifTestTable"] = "False"

                # Update the Number Of Entries as 0
                DML_value = "0"
            else:
                config[key]["ifTestTable"] = "True"

            if source == "":
                json_pair = DML_name.split('.')[-1]
                config[key][f"{json_pair}"] = DML_value

                # To match other table attributes (table type, add operation, delete operation, flags)
                # Regular expression to match a dot followed by digits and another dot
                pattern = r'\.(\d+)\.'

                # Replace all matches with .{i}.
                tableToCheckAttributes = re.sub(pattern, r'.{i}.', DML_name)
                config[key]["table"] = config[tableToCheckAttributes]["table"]

                # For all tables that are not writable, add and remove operations should be populated
                if config[tableToCheckAttributes]["table"] != "writableTable":
                    config[key]["addOperation"] = config[tableToCheckAttributes]["addOperation"]
                    config[key]["removeOperation"] = config[tableToCheckAttributes]["removeOperation"]
                # Determine if the writable table is rigid or not, if yes update the config accordingly
                elif config[tableToCheckAttributes]["table"] == "writableTable":
                    writableTable = tableToCheckAttributes.split("NumberOfEntries")[0] + "."
                    try:
                       if tdkbDmlModuleList.rigidWritableTables[compName] is not None:
                           if writableTable in tdkbDmlModuleList.rigidWritableTables[compName]:
                               config[key]["addOperation"] = "No"
                               config[key]["removeOperation"] = "No"
                           else:
                               config[key]["addOperation"] = "Yes"
                               config[key]["removeOperation"] = "Yes"
                    except KeyError:
                        config[key]["addOperation"] = "Yes"
                        config[key]["removeOperation"] = "Yes"

                try:
                    if config[tableToCheckAttributes]["flags"] is not None:
                        config[key]["flags"] = config[tableToCheckAttributes]["flags"]
                except KeyError:
                    # skipping flags if not present
                    break;

            else:
                config[key]["NumberOfEntries"] = DML_value

                # To match other table attributes (table type, add operation, delete operation, flags)
                # Regular expression to match a dot followed by digits and another dot
                pattern = r'\.(\d+)\.'

                # Replace all matches with .{i}.
                tableToCheckAttributes = re.sub(pattern, r'.{i}.', DML_name)
                config[key]["table"] = config[tableToCheckAttributes]["table"]

                # The below check can be removed
                # For all tables that are not writable, add and remove operations should be populated
                if config[tableToCheckAttributes]["table"] != "writableTable":
                    config[key]["addOperation"] = config[tableToCheckAttributes]["addOperation"]
                    config[key]["removeOperation"] = config[tableToCheckAttributes]["removeOperation"]

                try:
                    if config[tableToCheckAttributes]["flags"] is not None:
                        config[key]["flags"] = config[tableToCheckAttributes]["flags"]
                except KeyError:
                    # skipping flags if not present
                    break
    return

# append_dml_to_root
# Syntax      : append_dml_to_root(root, temp_DML_param, config_path)
# Description : Function to append parameter elements to the XML tree root
# Parameters  : root - root of the XML tree object
#               DML_param - DM to be added to the XML tree
#               config_path - path to the required configuration file (static/dynamic) of the component
# Return Value: None

def append_dml_to_root(root, DML_param, config_path):
    new_parameter = ET.Element('parameter')
    # Add a comment above the <name> tag
    comment_text_for_name = "the tr-181 parameter name"
    comment_for_name = ET.Comment(comment_text_for_name)
    new_parameter.append(comment_for_name)

    # Set the new name to the parameter and return it
    new_name = ET.Element('name')
    new_name.text = DML_param
    new_parameter.append(new_name)
    create_xml_tags_from_json(new_parameter, DML_param, config_path)
    root.append(new_parameter)

    return

# create_static_xml
# Syntax      : create_static_xml(path_to_static_config, output_xml_path)
# Description : Function to create test XML based on the configuration file of a component
# Parameters  : path_to_static_config - os file path to the static configuration file
#               output_xml_path - os file path location where the test XML needs to be created
# Return Value: None

def create_static_xml(path_to_static_config, output_xml_path):

    if path_to_static_config != "" and output_xml_path != "":
        # Create the root XML element
        root = ET.Element('parameters')

        try:
            # Open and read the JSON configuration file
            with open(path_to_static_config, 'r') as file:
                config = json.load(file)

            DML_params = config.keys()
            if DML_params != []:
                print("\nx--------------Start creating Static XML--------------x")
                for DML_param in DML_params:
                    element_type = config[DML_param].get("elementType", None)
                    if element_type is not None:
                        if element_type[0] != "RBUS_ELEMENT_TYPE_METHOD" and element_type[0] != "bus_element_type_method":
                            append_dml_to_root(root, DML_param, path_to_static_config)
                        else:
                            # Skipping element
                            continue
                    else:
                        # For those DMs which do not have element_type
                        append_dml_to_root(root, DML_param, path_to_static_config)

                #Converting the New XML Tree to a Bytes String
                new_xml_str = ET.tostring(root, encoding='utf-8')

                #Parsing the Bytes String into a DOM Object
                dom = parseString(new_xml_str)

                #Generates a string with added indentation for each level of the XML tree
                pretty_xml_as_string = dom.toprettyxml(indent="  ")

                # Write the new XML to a file
                with open(output_xml_path, 'w') as file:
                    file.write(pretty_xml_as_string)

                print("\nx--------------Created Static XML--------------x")
            else:
                print("\n--------------Static XML not created as config is empty--------------")

        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON file.")
        except FileNotFoundError:
            print(f"Error: The file {path_to_static_config} was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    return

# process_config_file
# Syntax      : process_config_file(config_file_path, temp_component_name, rbusobj, temp_config_type)
# Description : Function to parse through a configuration file and determine if the keys in the config are applicable DMs
#               for the device profile under test
# Parameters  : config_file_path - os file path to the configuration file (static/secondary run-time)
#               temp_component_name - name of the component under test
#               rbusobj - RBUS stub object
#               temp_config_type - static/run-time to determine the name of the new temporary configuration file to which
#                                  the applicable DMs are written to.
# Return Value: temp_config_path - the path to the config file which contains the DMs to be tested based on the device profile

def process_config_file(config_file_path, temp_component_name, rbusobj, temp_config_type):

    if temp_config_type == "static":
        temp_config_path = config_file_path.split(".json")[0] + "_temp.json"

    # in the case of run-time config, the same secondary config can be kept as temporary profile config
    elif temp_config_type == "run_time":
        temp_config_path = config_file_path

    with open(config_file_path, 'r') as file:
         config = json.load(file)

    secondary_config = {}

    expectedresult = "SUCCESS"
    tdkTestObj = rbusobj.createTestStep('RBUS_Open')
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()

    if expectedresult in actualresult:
        for key, values in config.items():
            flags = values.get("flags", [""])
            if flags == [""] or not any(flags):
                secondary_config[key] = values

            else:
                tdkTestObj = rbusobj.createTestStep("RBUS_GetElementInfo")
                tdkTestObj.addParameter("pathName",key)
                tdkTestObj.addParameter("compName",temp_component_name)
                tdkTestObj.addParameter("depth",0)
                tdkTestObj.executeTestCase(expectedresult)
                actualresult = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    newNamespaces = details.split(", ")
                    if newNamespaces[0] == key:
                        secondary_config[key] = values

                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"Unable to get the namespaces under {key}")

        # Close RBUS connection
        tdkTestObj = rbusobj.createTestStep('RBUS_Close')
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()

        if expectedresult not in actualresult:
            tdkTestObj.setResultStatus("FAILURE")
            print("RBUS close failed")

    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("RBUS open failed")

    if secondary_config != {}:
        with open(temp_config_path, "w") as json_file:
           json_file.write(format_json(secondary_config))

    return temp_config_path

# profileHandler
# Syntax      : profileHandler(path_to_config, component_name, rbusobj, config_type)
# Description : Wrapper function to call the profile handler function for static and run-time config files
# Parameters  : path_to_config - os file path to the configuration file (static/run-time)
#               component_name - name of the component under test
#               rbusobj - RBUS stub object
#               config_type - static/run-time
# Return Value: temp_config_path (in case of static) - the path to the temporary static config file which contains the DMs to be tested
#               based on the device profile. None - if run-time config.

def profileHandler(path_to_config, component_name, rbusobj, config_type):

    if config_type == "static":
        profile_config_path = ""
        profile_config_path = process_config_file(path_to_config, component_name, rbusobj, config_type)

        return profile_config_path

    elif config_type == "run_time":
        process_config_file(path_to_config, component_name, rbusobj, config_type)

# getUniqueNamespaces
# Syntax      : getUniqueNamespaces(configPath, namespaces)
# Description : Function to collect all the unique namespaces in a config file upto the first two objects in the DM tree
# Parameters  : configPath - os file path to the configuration file (static/run-time)
#               namespaces - all the unique namespaces collected from the config file
# Return Value: None

def getUniqueNamespaces(configPath, namespaces):
    with open(configPath, 'r') as file:
         config = json.load(file)

    for key in config:
        keyElements = key.split(".")[:2]
        namespace = keyElements[0] + "." + keyElements[1] + "."
        namespaces.add(namespace)
    return

# getAllParams
# Syntax      : getAllParams(configPath, params, configType)
# Description : Function to collect all DMs from a config file that do not have any flag dependency and are applicable
#               for all device profiles.
# Parameters  : configPath - os file path to the configuration file (static/run-time)
#               params - list of all DMs collected from config which are flag independent
#               configType - Static/Dynamic
# Return Value: None

def getAllParams(configPath, params, configType):
    with open(configPath, 'r') as file:
         config = json.load(file)

    if configType == "Static":
        for key in config:
            # If the parameter is flag controlled, ignore that for parameter existence test
            if config[key].get("flags") == [""]:
                params.append(key)
    elif configType == "Dynamic":
        for key in config:
            # If the parameter is flag controlled, ignore that for parameter existence test
            if config[key].get("flags") == [""]:
                if "NumberOfEntries" not in key and not key.endswith(".{i}."):
                    parameter_names = get_NumberOfEntries(key, configPath)
                    params.extend(parameter_names)
    return

# getEntry
# Syntax      : getEntry(Obj, param, oneTimeDict)
# Description : Function to fetch the number of table instances from the dictionary (if exists) or retrieve it from device
# Parameters  : Obj - TR181 stub object
#               param - the parameter that stores the number of table instances
#               oneTimeDict - dictionary to store the number of table instances for all table objects involved
#                            in the creation of the leaf node
# Return Value: entries - number of table instances

def getEntry(Obj, param, oneTimeDict):
    entries = 0
    try:
        if oneTimeDict[param] is not None:
            entries = oneTimeDict[param]
    except Exception as e:
        tdkTestObj = Obj.createTestStep('TDKB_TR181Stub_Get')
        _, details = tdkutility.getTR181Value(tdkTestObj, param)
        print(f"{param} : {details}")

        oneTimeDict[param] = details
        entries = oneTimeDict[param]

    return entries

# recursiveTableInstanceParams
# Syntax      : recursiveTableInstanceParams(Obj, parts, value, initial, loop, oneTimeDict, tableParams)
# Description : Recursive function to fetch the number of instances for tables and append to the list of table parameters
#               all the leaf nodes which are resolved
# Parameters  : Obj - TR181 stub object
#               parts - the parts of the the leaf node to be resolved
#               value - the parameter to track the number of table instances
#               initial - the initial part of the leaf node upto which it has been resolved
#               loop - the parameter to keep track of the objects in the leaf node
#               oneTimeDict - dictionary to store the number of table instances for all table objects involved
#                            in the creation of the leaf node
#               tableParams - set of all parameters under a table instance
# Return Value: None

def recursiveTableInstanceParams(Obj, parts, value, initial, loop, oneTimeDict, tableParams):
    loop = loop + 1
    for val in range(1, value + 1):
        # Device.DHCPv4.Server.Pool.5.Client.1.IPv4Address
        partial = initial + "." + str(val) + "." + parts[loop]
        # Device.DHCPv4.Server.Pool.5.Client.1.IPv4AddressNumberOfEntries
        if parts[loop] != parts[-1]:
            entriesParam = partial + "NumberOfEntries"
            entries = getEntry(Obj, entriesParam, oneTimeDict)
            # (parts, 2, Device.DHCPv4.Server.Pool.5.Client.1.IPv4Address, 1)
            recursiveTableInstanceParams(Obj, parts, int(entries), partial, loop, oneTimeDict, tableParams)
        else:
            tableParams.add(partial)
    return

# checkTableInstanceParams
# Syntax      : checkTableInstanceParams(Obj, resolvedTable, instanceNum, data)
# Description : Function to identify all the parameters under a table object. Eg: If A.B. is the table, then parameters would be like
#               A.B.1.Enable, A.B.1.Size, ..etc
# Parameters  : Obj - TR181 stub object
#               resolvedTable - table object Eg: A.B.
#               instanceNum - number of the table instance added
#               data - run-time configuration file from which the parameters under a table instance can be deduced
# Return Value: tableParams - set of all parameters under a table instance

def checkTableInstanceParams(Obj, resolvedTable, instanceNum, data):
    # From the resolvedTable, deduce the partial path
    resolvedTable = resolvedTable + instanceNum + "."

    # Regular expression to match a dot followed by digits and another dot
    pattern = r'\.(\d+)\.'

    # Replace all matches with .{i}. to get the table partial path
    tablePartialPath = re.sub(pattern, r'.{i}.', resolvedTable)

    # Find all keys that contain the partial path
    matched_keys = [key for key in data.keys() if tablePartialPath in key]

    # Find the specific params
    #params = [key.split(".")[-1] for key in matched_keys]
    params = [key.split(tablePartialPath)[-1] for key in matched_keys]

    # Append the params to the resolved table
    tableParams = set()

    # Capture the Number of entries param values
    oneTimeDict = {}

    for param in params:
        param = resolvedTable + param

        # Device.DHCPv4.Server.Pool.5.Client.{i}.IPv4Address.{i}.LeaseTimeRemaining
        if ".{i}." in param:
            loop = 0
            # [ Device.DHCPv4.Server.Pool.5.Client, IPv4Address, LeaseTimeRemaining]
            nameParts = param.split(".{i}.")

            entriesParam = nameParts[0] + "NumberOfEntries"
            entries = getEntry(Obj, entriesParam, oneTimeDict)
            #(nameParts, 3, Device.DHCPv4.Server.Pool.5.Client, 0)
            recursiveTableInstanceParams(Obj, nameParts, int(entries), nameParts[0], loop, oneTimeDict, tableParams)
        else:
            # Ignore the table object names
            if not param.endswith("."):
                tableParams.add(param)

    return tableParams

# tableConfigGenerator
# Syntax      : tableConfigGenerator(path_to_runtime_config, tableType)
# Description : Function to determine whether a run-time config file contains any tables of the required type for table testing
# Parameters  : path_to_runtime_config - os file path to the run-time configuration file
#               tableType - type of the table under test (Eg: staticTable, dynamicTable, dynWritableTable, writableTable)
# Return Value: testFlag - True - if the required table type found in config, else false

def tableConfigGenerator(path_to_runtime_config, tableType):
    testFlag = "False"

    # Open and read the JSON file
    with open(path_to_runtime_config, 'r') as file:
        config = json.load(file)

    for key, _ in config.items():
        if "NumberOfEntries" in key or key.endswith(".{i}.") or key.endswith(".{i}"):
            try:
                for table in tableType:
                    if config[key]["table"] == table:
                        testFlag = "True"
                        break
            except KeyError:
                print(f"Table type not available for {key}")

    return testFlag

# getElementInfo
# Syntax      : getElementInfo(tdkTestObj, expectedresult, getResult, partialPath, component, uniqueNamespaces, recursion)
# Description : Function to recursively traverse through a DM tree to collect all the leaf nodes using rbus_getElementInfo() API
# Parameters  : tdkTestObj - RBUS test object for the test RBUS_GetElementInfo
#               expectedresult - SUCCESS/FAILURE
#               getResult - SUCCESS/FAILURE status of DM tree traversal
#               partialPath - the object path of the current node
#               component - component under test
#               uniqueNamespaces - set of all unique leaf nodes
#               recursion - if "True" it means leaf node is not reached and recursion must go on further
# Return Value: None

def getElementInfo(tdkTestObj, expectedresult, getResult, partialPath, component, uniqueNamespaces, recursion):
    tdkTestObj.addParameter("pathName",partialPath)
    tdkTestObj.addParameter("compName",component)
    tdkTestObj.addParameter("depth",-1)
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        newNamespaces = details.split(", ")
        if recursion == "True":
            for name in newNamespaces:
                if name.endswith("."):
                    getElementInfo(tdkTestObj, expectedresult, getResult, name, component, uniqueNamespaces, recursion)
                else:
                    uniqueNamespaces.add(name)
        else:
            # To ensure that namespaces is only populated in valid cases
            if len(newNamespaces) != 1 and newNamespaces[0] != "":
                uniqueNamespaces.add(partialPath)
    else:
        getResult = "FAILURE"
        tdkTestObj.setResultStatus("FAILURE")
        print(f"Unable to fetch the namespaces under {partialPath}")
    return

# getNames
# Syntax      : getNames(expectedresult, rbusobj, tableInstance, component, recursion)
# Description : Wrapper function to invoke getElementInfo() to identify all the leaf nodes under a table instance
# Parameters  : expectedresult - SUCCESS/FAILURE
#               rbusobj - RBUS stub object
#               tableInstance - table instance under which leaf nodes are to be identified
#               component - component under test
#               recursion - if "True" it means leaf node is not reached and recursion must go on further
# Return Value: newNamespaces - set of all leaf nodes identified
#               flag - SUCCESS/FAILURE dependening on the DM tree traversal
#               tdkTestObj - RBUS test object

def getNames(expectedresult, rbusobj, tableInstance, component, recursion):
    newNamespaces = set()
    # Initialize
    # For all success cases "" will be a trailing set element which will be removed later
    newNamespaces.add("")
    flag = "SUCCESS"
    # Open RBUS connection
    tdkTestObj = rbusobj.createTestStep('RBUS_Open');
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if expectedresult in actualresult and details != "":
        tdkTestObj = rbusobj.createTestStep("RBUS_GetElementInfo")
        getElementInfo(tdkTestObj, expectedresult, flag, tableInstance, component, newNamespaces, recursion)

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

    return newNamespaces, flag, tdkTestObj

# isParamFlagDependent
# Syntax      : isParamFlagDependent(param, config)
# Description : Function to determine if a parameter is flag based from the config file
# Parameters  : param - Name of the parameter
#               config - run-time configuration of the component
# Return Value: True/False - depending on whether on not parameter is flag dependent

def isParamFlagDependent(param, config):
    #Convert the param to config specfic representation with .{i}.
    parts = param.split(".")
    convertedDM = parts[0]
    for p in parts[1:]:
        if p.isdigit():
            convertedDM = convertedDM + ".{i}"
        else:
            convertedDM = convertedDM + "."
            convertedDM = convertedDM + p

    #Check flags from config file
    if config[convertedDM]["flags"] == [""]:
        return False
    else:
        return True

# addTableRow
# Syntax      : addTableRow(tr181Obj, table)
# Description : Function to add a new instance to the table object for L2 SET use-cases
# Parameters  : tr181Obj - TR181 stub oject
#               table - table to which a new instance need to be added
# Return Value: actualresult - SUCCESS/FAILURE
#               tableRowToDel - if the instance added successfully, append the table to a list so that it can be
#                               deleted after the test
#               instanceNum - the instance number added

def addTableRow(tr181Obj, table):
    expectedresult = "SUCCESS"
    instanceNum = "-1"
    tableRowToDel = ""
    tdkTestObj = tr181Obj.createTestStep("TDKB_TR181Stub_AddObject")
    tdkTestObj.addParameter("paramName", table)
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "")

    if expectedresult in actualresult and "Instance Number is :" in details:
        tdkTestObj.setResultStatus("SUCCESS")
        instanceNum =  details.split("Instance Number is :")[1]
        tableRowToDel = table + instanceNum + "."
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"\nUnable to add a row to the table object {table} for validating L2 set test\n")

    return actualresult, tableRowToDel, instanceNum

# delTableRow
# Syntax      : delTableRow(tr181Obj, table)
# Description : Function to delete a specific instance from the table after L2 SET use-case test
# Parameters  : tr181Obj - TR181 stub oject
#               table - table from which a specific instance need to be deleted
# Return Value: actualresult - SUCCESS/FAILURE

def delTableRow(tr181Obj, table):
    expectedresult = "SUCCESS"
    tdkTestObj = tr181Obj.createTestStep("TDKB_TR181Stub_DelObject")
    tdkTestObj.addParameter("paramName", table)
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "")

    if expectedresult in actualresult and "DELETE OBJECT API Validation is Success" in details:
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"\nUnable to delete the table row {table} after validating L2 set test\n")

    return actualresult

# L2PreReq
# Syntax      : L2PreReq(tr181Obj, secondary_config, temp_runtime_config)
# Description : Function to perform the pre-requsites for L2 tests if the use case involves DMs from table objects
# Parameters  : tr181Obj - TR181 stub oject
#               secondary_config - secondary config of the component
#               temp_runtime_config - run-time config file with the DM names resolved
# Return Value: tableList - list of table instances which are added

def L2PreReq(tr181Obj, secondary_config, temp_runtime_config):
    returnStatus = "SUCCESS"
    tableList = []
    # Open and read the JSON files
    with open(secondary_config, 'r') as file:
        main_config = json.load(file)

    with open(temp_runtime_config, 'r') as file:
        temp_config = json.load(file)

    for key, values in main_config.items():
        # Pick the tables which have 0 row counts but are to be considered for L2 SET tests
        if main_config[key].get("Set_type") is not None:
            if main_config[key]["Set_type"] == "L2":
                parameter_names = get_NumberOfEntries(key, secondary_config)
                if parameter_names == []:
                    # Check the number of entries key
                    # For tables which have NumberOfEntries params
                    try:
                        numOfEntriesKey = key.split(".{i}.")[0] + "NumberOfEntries"
                        table = key.split("{i}.")[0]
                        ifTestTable = main_config[numOfEntriesKey]["ifTestTable"]
                        addOperation = main_config[numOfEntriesKey]["addOperation"]
                    # For RBUS tables
                    except KeyError:
                        numOfEntriesKey = key.split(".{i}.")[0] + ".{i}."
                        table = key.split("{i}.")[0]
                        ifTestTable = main_config[numOfEntriesKey]["ifTestTable"]
                        addOperation = main_config[numOfEntriesKey]["addOperation"]

                    # If addtable operation is supported, add a table row
                    if ifTestTable == "True" and addOperation == "Yes":
                        returnStatus, tableRowToDel, instanceNum = addTableRow(tr181Obj, table)
                        if returnStatus == "SUCCESS":
                            # collect added table rows to delete at the end
                            tableList.append(tableRowToDel)

                            # Modified key
                            suffix = key.split("{i}.")[-1]
                            key = table + instanceNum + "." + suffix

                            # Update the temp_config
                            temp_config[key] = values.copy()

                    else:
                        # add operation not supported, skip testing L2 for the DM
                        continue
                else:
                    # table rows present already
                    continue
            else:
                #skip
                continue
        else:
            continue

    # Write back to the temp config
    with open(temp_runtime_config, 'w') as file:
        file.write(format_json(temp_config))

    return tableList

# L2PostReq
# Syntax      : L2PostReq(tr181Obj, tableRowToDel)
# Description : Function to perform the post-requsites for L2 tests if the use case involves DMs from table objects
# Parameters  : tr181Obj - TR181 stub oject
#               tableRowToDel - list of table instances which needs to be deleted
# Return Value: postReq - SUCCESS/FAILURE

def L2PostReq(tr181Obj, tableRowToDel):
    postReq = "SUCCESS"
    for tableRow in tableRowToDel:
        returnStatus = delTableRow(tr181Obj, tableRow)
        if returnStatus == "FAILURE":
            postReq = "FAILURE"

    return postReq

# performPreReq
# Syntax      : performPreReq(tr181Obj, rbusobj, path_to_runtime_config)
# Description : Wrapper function to perform the pre-requsites for all components which has a run-time config. The function invokes
#               methods to resolve all table DMs based on the current table row counts and then writes the configuration to an
#               intermediate file which become the input for further processing.
# Parameters  : tr181Obj - TR181 stub oject
#               rbusobj - RBUS stub object
#               path_to_runtime_config - os path to the run-time config file of the component
# Return Value: secondary_config_name - config file generated after populating the number of table rows for all tables
#               temp_config_name - config file with all run-time DMs and tables resolved

def performPreReq(tr181Obj, rbusobj, path_to_runtime_config):

    # Open and read the JSON file
    with open(path_to_runtime_config, 'r') as file:
        config = json.load(file)

    compName = path_to_runtime_config.split("/")[-1].split("_runtime_config.json")[0]

    # Retrieve the NumberOfEntries values
    secondary_config = get_param_and_query(config, tr181Obj, rbusobj, compName)

    # Create a secondary config
    # Open and copy the runtime config to this secondary JSON file
    secondary_config_name_partial = path_to_runtime_config.split(".json")[0]
    secondary_config_name = secondary_config_name_partial + "_secondary.json"
    temp_config_name = secondary_config_name_partial + "_temp.json"

    with open(secondary_config_name, 'w') as file:
        file.write(format_json(secondary_config))

    temp_config = {}
    for DML_param, values in config.items():
        if "NumberOfEntries" not in DML_param and not DML_param.endswith(".{i}."):
            parameter_names = get_NumberOfEntries(DML_param, secondary_config_name)
            if parameter_names:
                for parameter_name in parameter_names:
                    temp_config[parameter_name] = values.copy()

    with open(temp_config_name, 'w') as file:
        file.write(format_json(temp_config))

    return temp_config_name, secondary_config_name

# createXMLFromSecondaryConfig
# Syntax      : createXMLFromSecondaryConfig(secondary_config_name, output_xml_path)
# Description : Wrapper function to invoke create_xml() to create an XML from a config file
# Parameters  : secondary_config_name - os path to the secondary config
#               output_xml_path - os path to the test XML which needs to be created
# Return Value: returnStatus - SUCCESS/FAILURE
#               DM_tracker - list of DMs using which the test XML has been created

def createXMLFromSecondaryConfig(secondary_config_name, output_xml_path):
    returnStatus = "SUCCESS"

    DM_tracker = create_xml(secondary_config_name, output_xml_path)

    try:
        ET.parse(output_xml_path)
    except ET.ParseError:
        print("\nDynamic XML is empty or parse error!!!")
        returnStatus = "FAILURE"
    except FileNotFoundError:
        print("\nDynamic XML not populated as there are no table instances")

    return returnStatus, DM_tracker

