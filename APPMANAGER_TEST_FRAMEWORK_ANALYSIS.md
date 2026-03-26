# AppManager Test Framework Analysis vs Existing Components

## Issue
**Comment Received:** "This is not the way to develop test scripts/cases for Ent services, it is a separate XML based test framework"

## Root Cause Analysis

The AppManager test implementation does **NOT** follow the proper XML-based test framework pattern used by other enterprise service components.

---

## Comparison: Correct vs Incorrect Approach

### ✅ CORRECT APPROACH (PackageManager, rdkvmemcr, iarmbus)

#### 1. **Separate XML File with Primitive Test Definitions**
Example: `PackageManager.xml`
```xml
<xml>
  <module name="PackageManagerRDKEMS" testGroup="Component">
    <primitiveTests>
      <primitiveTest name="PackageManager_Install" id="" version="1">
        <function>TestMgr_PackageManager_Install</function>
        <parameters>
          <parameter name="packageId" value=""/>
          <parameter name="version" value=""/>
        </parameters>
      </primitiveTest>
      <!-- More primitive tests defined here -->
    </primitiveTests>
  </module>
</xml>
```

#### 2. **Python Test File References XML Primitive Tests**
```python
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <name>RDKV_PackageManager_Install_Positive</name>
  <primitive_test_name>PackageManager_Install</primitive_test_name>  <!-- KEY: References XML definition -->
  <primitive_test_version>1</primitive_test_version>
  <!-- Rest of metadata -->
</xml>
'''

obj.setLoadModuleStatus(result.upper())

if "SUCCESS" in result.upper():
    # KEY: Use createTestStep() with XML-defined primitive test name
    tdkTestObj = obj.createTestStep('PackageManager_Install')
    tdkTestObj.addParameter("packageId", "test_app")
    tdkTestObj.addParameter("version", "1.0")
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
```

**Key Characteristics:**
- ✅ Separate XML file with primitive test definitions
- ✅ Python file references `<primitive_test_name>` from XML
- ✅ Uses TDK framework's `createTestStep()` method
- ✅ Uses `addParameter()` to set parameters
- ✅ Uses `executeTestCase()` to run the test
- ✅ Returns structured result for analysis

**Real Examples in Repository:**
- `framework/fileStore/testscriptsRDKV/component/PackageManager/PackageManager.xml`
- `framework/fileStore/testscriptsRDKV/component/rdkvmemcr/rdkvmemcr.xml`
- `framework/fileStore/testscriptsRDKV/component/iarmbus/iarmbus.xml`

---

### ❌ INCORRECT APPROACH (Current AppManager Implementation)

#### 1. **No Separate XML File**
AppManager directory has NO `.xml` file with primitive test definitions.

#### 2. **XML Metadata Embedded in Python File**
```python
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <name>RDKV_AppManager_02_LaunchApp_Positive</name>
  <primitive_test_name>RdkService_Test</primitive_test_name>  <!-- Generic, not component-specific -->
  <primitive_test_version>1</primitive_test_version>
  <!-- All test metadata in same file -->
</xml>
'''

import tdklib
from ai2_0_utils import (
    get_ai2_setting,
    thunder_is_plugin_active,
    thunder_call,  # Direct API call utility
)

# Direct API call without using TDK framework's test step mechanism
if not thunder_is_plugin_active(plugin_name, jsonrpc_url=jsonrpc_url):
    print("[ERROR] AppManager plugin is not active")
else:
    # Directly calling API without createTestStep()
    response = thunder_call(obj, "org.rdk.AppManager.1", "launchApp", params)
    
    if response and "handle" in response:
        print(f"  [PASS] Launch returned valid handle: {handle}")
        obj.setLoadModuleStatus("SUCCESS")
```

**Key Issues:**
- ❌ No separate XML file for primitive test definitions
- ❌ Generic primitive_test_name (RdkService_Test) instead of component-specific
- ❌ Direct `thunder_call()` usage instead of TDK framework
- ❌ Does NOT use `createTestStep()` method
- ❌ Does NOT use TDK framework's parameter management
- ❌ Doesn't follow enterprise service test framework pattern

---

## Directory Structure Comparison

### ✅ Correct Pattern - PackageManager
```
framework/fileStore/testscriptsRDKV/component/PackageManager/
├── PackageManager.xml                          ← Primitive test definitions
├── PackageManager_Testcase.xml                 ← Additional test cases
├── RDKV_PackageManager_01_Activate.py
├── RDKV_PackageManager_02_Download_Positive.py
├── RDKV_PackageManager_03_Download_Negative.py
└── ... (more test files)
```

### ✅ Correct Pattern - rdkvmemcr
```
framework/fileStore/testscriptsRDKV/component/rdkvmemcr/
├── rdkvmemcr.xml                              ← Primitive test definitions
├── RDKV_Memcr_Check_Service_Status.py
├── RDKV_Memcr_Validate_Cobalt_Launch_After_Reboot.py
└── ... (more test files)
```

### ❌ Incorrect Pattern - AppManager (Current)
```
framework/fileStore/testscriptsRDKV/component/AppManager/
├── RDKV_AppManager_01_Activate.py
├── RDKV_AppManager_02_LaunchApp_Positive.py
├── RDKV_AppManager_03_LaunchApp_Negative.py
└── ... (more test files)

❌ MISSING: AppManager.xml (primitive test definitions file)
```

---

## Code Flow Comparison

### ✅ Correct - Using TDK Framework (rdkvmemcr example)
```python
obj.setLoadModuleStatus(result.upper())

if "SUCCESS" in result.upper():
    # Step 1: Create test using framework's createTestStep()
    tdkTestObj = obj.createTestStep('memcr_getTR181Value')
    
    # Step 2: Add parameters using TDK method
    tdkTestObj.addParameter("basePath", obj.realpath)
    tdkTestObj.addParameter("configKey", "MEMCR_APPHIBERNATE_PARAMETER")
    
    # Step 3: Execute using TDK framework
    tdkTestObj.executeTestCase(expectedResult)
    
    # Step 4: Get results from framework
    result = tdkTestObj.getResultDetails()
    
    # Step 5: Set result status
    if "SUCCESS" in result:
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        tdkTestObj.setResultStatus("FAILURE")
```

### ❌ Incorrect - Direct API Calling (AppManager current)
```python
if thunder_is_plugin_active(plugin_name, jsonrpc_url=jsonrpc_url):
    # Direct utility function call - bypasses TDK framework
    response = thunder_call(obj, "org.rdk.AppManager.1", "launchApp", params)
    
    # Manual response checking - no framework validation
    if response and "handle" in response:
        handle = response.get("handle")
        print(f"  [PASS] Launch returned valid handle: {handle}")
        obj.setLoadModuleStatus("SUCCESS")
    else:
        print(f"  [FAIL] Launch did not return valid handle")
        obj.setLoadModuleStatus("FAILURE")
```

---

## What Needs to Be Fixed

### For AppManager to be compliant with the TDK Enterprise Service Framework:

1. **Create AppManager.xml file** with primitive test definitions
   - Reference: `PackageManager.xml` or `rdkvmemcr.xml`
   - Define all AppManager API methods as primitive tests
   - Include parameter definitions for each method

2. **Update Python Test Files**
   - Change `<primitive_test_name>RdkService_Test</primitive_test_name>` to actual primitive test names
   - Replace `thunder_call()` with `createTestStep()` + `addParameter()` pattern
   - Use `executeTestCase()` for framework-based execution
   - Use TDK's `setResultStatus()` instead of manual status setting

3. **Remove Embedded API Details**
   - Move API endpoint details to XML configuration
   - Let the framework manage parameter passing
   - Use framework's result handling mechanisms

---

## Example: AppManager.xml (Template)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
Copyright 2025 RDK Management
Licensed under the Apache License, Version 2.0
-->
<xml>
  <module name="AppManagerRDK" testGroup="Component">
    <primitiveTests>
      <primitiveTest name="AppManager_LaunchApp" id="" version="1">
        <function>TestMgr_AppManager_LaunchApp</function>
        <parameters>
          <parameter name="appId" value=""/>
          <parameter name="appVersion" value=""/>
        </parameters>
      </primitiveTest>
      <primitiveTest name="AppManager_CloseApp" id="" version="1">
        <function>TestMgr_AppManager_CloseApp</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      <primitiveTest name="AppManager_IsInstalled" id="" version="1">
        <function>TestMgr_AppManager_IsInstalled</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      <!-- Add other AppManager API methods as primitive tests -->
    </primitiveTests>
  </module>
</xml>
```

---

## Summary

| Aspect | Correct (PackageManager/rdkvmemcr) | Incorrect (Current AppManager) |
|--------|-----------------------------------|-------------------------------|
| **XML File** | ✅ Separate XML with definitions | ❌ No separate XML file |
| **Primitive Tests** | ✅ Defined in XML | ❌ Generic/missing |
| **Framework Usage** | ✅ createTestStep() | ❌ Direct API calls |
| **Parameter Handling** | ✅ Via addParameter() | ❌ Manual python dicts |
| **Test Execution** | ✅ executeTestCase() | ❌ Thunder_call() utility |
| **Result Management** | ✅ TDK framework | ❌ Manual checking |
| **Compliance** | ✅ Enterprise Service Pattern | ❌ Non-compliant |

---

## References
- **Correct Examples:** 
  - `framework/fileStore/testscriptsRDKV/component/PackageManager/PackageManager.xml`
  - `framework/fileStore/testscriptsRDKV/component/rdkvmemcr/rdkvmemcr.xml`
  - `framework/fileStore/testscriptsRDKV/component/iarmbus/iarmbus.xml`
  
- **Compliant Test Examples:**
  - `framework/fileStore/testscriptsRDKV/component/rdkvmemcr/RDKV_Memcr_Check_Service_Status.py`
  - `framework/fileStore/testscriptsRDKV/component/iarmbus/IARMBUS_Query_Key_Repeat_Interval_test.py`
