# AppManager Test Framework Remediation Steps

## Overview
This document provides step-by-step instructions to convert AppManager tests from the current non-compliant approach to the proper Enterprise Service XML-based test framework pattern.

---

## Step 1: Create AppManager.xml File

**File Location:** `framework/fileStore/testscriptsRDKV/component/AppManager/AppManager.xml`

**Template (based on PackageManager.xml and rdkvmemcr.xml):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:
 Copyright 2025 RDK Management
 Licensed under the Apache License, Version 2.0
-->
<xml>
  <module name="AppManagerRDK" testGroup="Component">
    <primitiveTests>
      <!-- Application Lifecycle Management -->
      <primitiveTest name="AppManager_LaunchApp" id="" version="1">
        <function>TestMgr_AppManager_LaunchApp</function>
        <parameters>
          <parameter name="appId" value=""/>
          <parameter name="appVersion" value=""/>
          <parameter name="metadata" value=""/>
        </parameters>
      </primitiveTest>
      
      <primitiveTest name="AppManager_PreloadApp" id="" version="1">
        <function>TestMgr_AppManager_PreloadApp</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      
      <primitiveTest name="AppManager_CloseApp" id="" version="1">
        <function>TestMgr_AppManager_CloseApp</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      
      <primitiveTest name="AppManager_TerminateApp" id="" version="1">
        <function>TestMgr_AppManager_TerminateApp</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      
      <primitiveTest name="AppManager_KillApp" id="" version="1">
        <function>TestMgr_AppManager_KillApp</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      
      <!-- Application Query Methods -->
      <primitiveTest name="AppManager_IsInstalled" id="" version="1">
        <function>TestMgr_AppManager_IsInstalled</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      
      <primitiveTest name="AppManager_GetInstalledApps" id="" version="1">
        <function>TestMgr_AppManager_GetInstalledApps</function>
        <parameters/>
      </primitiveTest>
      
      <primitiveTest name="AppManager_GetLoadedApps" id="" version="1">
        <function>TestMgr_AppManager_GetLoadedApps</function>
        <parameters/>
      </primitiveTest>
      
      <!-- System App Management -->
      <primitiveTest name="AppManager_StartSystemApp" id="" version="1">
        <function>TestMgr_AppManager_StartSystemApp</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      
      <primitiveTest name="AppManager_StopSystemApp" id="" version="1">
        <function>TestMgr_AppManager_StopSystemApp</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      
      <!-- Application Data Management -->
      <primitiveTest name="AppManager_ClearAppData" id="" version="1">
        <function>TestMgr_AppManager_ClearAppData</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      
      <primitiveTest name="AppManager_ClearAllAppData" id="" version="1">
        <function>TestMgr_AppManager_ClearAllAppData</function>
        <parameters/>
      </primitiveTest>
      
      <!-- Application Metadata & Configuration -->
      <primitiveTest name="AppManager_GetAppMetadata" id="" version="1">
        <function>TestMgr_AppManager_GetAppMetadata</function>
        <parameters>
          <parameter name="appId" value=""/>
        </parameters>
      </primitiveTest>
      
      <primitiveTest name="AppManager_GetAppProperty" id="" version="1">
        <function>TestMgr_AppManager_GetAppProperty</function>
        <parameters>
          <parameter name="appId" value=""/>
          <parameter name="propertyName" value=""/>
        </parameters>
      </primitiveTest>
      
      <primitiveTest name="AppManager_SetAppProperty" id="" version="1">
        <function>TestMgr_AppManager_SetAppProperty</function>
        <parameters>
          <parameter name="appId" value=""/>
          <parameter name="propertyName" value=""/>
          <parameter name="propertyValue" value=""/>
        </parameters>
      </primitiveTest>
      
      <!-- System Resource Queries -->
      <primitiveTest name="AppManager_GetMaxRunningApps" id="" version="1">
        <function>TestMgr_AppManager_GetMaxRunningApps</function>
        <parameters/>
      </primitiveTest>
      
      <primitiveTest name="AppManager_GetMaxHibernatedApps" id="" version="1">
        <function>TestMgr_AppManager_GetMaxHibernatedApps</function>
        <parameters/>
      </primitiveTest>
      
      <primitiveTest name="AppManager_GetMaxInactiveRamUsage" id="" version="1">
        <function>TestMgr_AppManager_GetMaxInactiveRamUsage</function>
        <parameters/>
      </primitiveTest>
      
      <primitiveTest name="AppManager_GetMaxHibernatedFlashUsage" id="" version="1">
        <function>TestMgr_AppManager_GetMaxHibernatedFlashUsage</function>
        <parameters/>
      </primitiveTest>
      
      <!-- Intent Handling -->
      <primitiveTest name="AppManager_SendIntent" id="" version="1">
        <function>TestMgr_AppManager_SendIntent</function>
        <parameters>
          <parameter name="action" value=""/>
          <parameter name="uri" value=""/>
        </parameters>
      </primitiveTest>
    </primitiveTests>
  </module>
</xml>
```

---

## Step 2: Update Python Test Files

### Example: Convert RDKV_AppManager_02_LaunchApp_Positive.py

#### BEFORE (Current - Non-compliant)
```python
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <name>RDKV_AppManager_02_LaunchApp_Positive</name>
  <primitive_test_name>RdkService_Test</primitive_test_name>  <!-- ❌ Generic -->
  <!-- ... other metadata ... -->
</xml>
'''

import tdklib
from ai2_0_utils import thunder_call

obj = tdklib.TDKScriptingLibrary("AppManager", "1", standAlone=True)

if "SUCCESS" in loadmodulestatus.upper():
    # ❌ Direct API call
    response = thunder_call(obj, "org.rdk.AppManager.1", "launchApp", params)
    
    if response and "handle" in response:
        print(f"  [PASS] Launch returned valid handle")
        obj.setLoadModuleStatus("SUCCESS")
```

#### AFTER (Compliant)
```python
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <name>RDKV_AppManager_02_LaunchApp_Positive</name>
  <primitive_test_name>AppManager_LaunchApp</primitive_test_name>  <!-- ✅ From AppManager.xml -->
  <primitive_test_version>1</primitive_test_version>
  <!-- ... other metadata ... -->
</xml>
'''

import tdklib
import sys

obj = tdklib.TDKScriptingLibrary("AppManager", "1", standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_AppManager_02_LaunchApp_Positive')

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" % result)

obj.setLoadModuleStatus(result.upper())
expectedResult = "SUCCESS"

if "SUCCESS" in result.upper():
    # ✅ Use TDK framework's createTestStep()
    tdkTestObj = obj.createTestStep('AppManager_LaunchApp')
    
    # ✅ Add parameters using TDK's addParameter()
    tdkTestObj.addParameter("appId", "com.rdkcentral.youtube")
    tdkTestObj.addParameter("appVersion", "1.0")
    
    # ✅ Execute using TDK framework
    tdkTestObj.executeTestCase(expectedResult)
    
    # ✅ Get structured results from framework
    result = tdkTestObj.getResultDetails()
    
    if "SUCCESS" in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"  [PASS] LaunchApp returned success: {result}")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"  [FAIL] LaunchApp failed: {result}")
else:
    print("[ERROR] Failed to load AppManager module")
    obj.setLoadModuleStatus("FAILURE")

obj.unloadModule("AppManager")
```

---

## Step 3: Update All AppManager Python Test Files

### Files to Update (34 test files)

| File Name | Primitive Test Name | Parameters |
|-----------|-------------------|------------|
| RDKV_AppManager_02_LaunchApp_Positive.py | AppManager_LaunchApp | appId, appVersion |
| RDKV_AppManager_03_LaunchApp_Negative.py | AppManager_LaunchApp | appId (invalid) |
| RDKV_AppManager_04_PreloadApp_Positive.py | AppManager_PreloadApp | appId |
| RDKV_AppManager_05_PreloadApp_Negative.py | AppManager_PreloadApp | appId (invalid) |
| RDKV_AppManager_06_CloseApp_Positive.py | AppManager_CloseApp | appId |
| RDKV_AppManager_07_CloseApp_Negative.py | AppManager_CloseApp | appId (invalid) |
| RDKV_AppManager_08_TerminateApp_Positive.py | AppManager_TerminateApp | appId |
| RDKV_AppManager_09_TerminateApp_Negative.py | AppManager_TerminateApp | appId (invalid) |
| RDKV_AppManager_10_KillApp_Positive.py | AppManager_KillApp | appId |
| RDKV_AppManager_11_KillApp_Negative.py | AppManager_KillApp | appId (invalid) |
| RDKV_AppManager_12_IsInstalled_Positive.py | AppManager_IsInstalled | appId |
| RDKV_AppManager_13_IsInstalled_Negative.py | AppManager_IsInstalled | appId (invalid) |
| RDKV_AppManager_14_GetInstalledApps.py | AppManager_GetInstalledApps | (none) |
| RDKV_AppManager_15_GetLoadedApps.py | AppManager_GetLoadedApps | (none) |
| RDKV_AppManager_16_SendIntent_Positive.py | AppManager_SendIntent | action, uri |
| RDKV_AppManager_17_SendIntent_Negative.py | AppManager_SendIntent | action (invalid), uri |
| RDKV_AppManager_18_StartSystemApp_Positive.py | AppManager_StartSystemApp | appId |
| RDKV_AppManager_19_StartSystemApp_Negative.py | AppManager_StartSystemApp | appId (invalid) |
| RDKV_AppManager_20_StopSystemApp_Positive.py | AppManager_StopSystemApp | appId |
| RDKV_AppManager_21_StopSystemApp_Negative.py | AppManager_StopSystemApp | appId (invalid) |
| RDKV_AppManager_22_ClearAppData_Positive.py | AppManager_ClearAppData | appId |
| RDKV_AppManager_23_ClearAppData_Negative.py | AppManager_ClearAppData | appId (invalid) |
| RDKV_AppManager_24_ClearAllAppData.py | AppManager_ClearAllAppData | (none) |
| RDKV_AppManager_25_GetAppMetadata_Positive.py | AppManager_GetAppMetadata | appId |
| RDKV_AppManager_26_GetAppMetadata_Negative.py | AppManager_GetAppMetadata | appId (invalid) |
| RDKV_AppManager_27_GetAppProperty_Positive.py | AppManager_GetAppProperty | appId, propertyName |
| RDKV_AppManager_28_GetAppProperty_Negative.py | AppManager_GetAppProperty | appId (invalid), propertyName |
| RDKV_AppManager_29_SetAppProperty_Positive.py | AppManager_SetAppProperty | appId, propertyName, propertyValue |
| RDKV_AppManager_30_SetAppProperty_Negative.py | AppManager_SetAppProperty | appId (invalid), propertyName, propertyValue |
| RDKV_AppManager_31_GetMaxRunningApps.py | AppManager_GetMaxRunningApps | (none) |
| RDKV_AppManager_32_GetMaxHibernatedApps.py | AppManager_GetMaxHibernatedApps | (none) |
| RDKV_AppManager_33_GetMaxHibernatedFlashUsage.py | AppManager_GetMaxHibernatedFlashUsage | (none) |
| RDKV_AppManager_34_GetMaxInactiveRamUsage.py | AppManager_GetMaxInactiveRamUsage | (none) |

---

## Step 4: Remove Non-Framework Components

### Remove from Python Files:
1. ❌ Remove `from ai2_0_utils import thunder_call` - not needed with TDK framework
2. ❌ Remove direct `thunder_call()` function calls
3. ❌ Remove manual JSON-RPC URL construction
4. ❌ Remove direct plugin activation checks (framework handles this)

### Keep in Python Files:
1. ✅ TDK library import: `import tdklib`
2. ✅ Test configuration: `obj.configureTestCase()`
3. ✅ Test step creation: `obj.createTestStep()`
4. ✅ Parameter management: `tdkTestObj.addParameter()`
5. ✅ Test execution: `tdkTestObj.executeTestCase()`

---

## Step 5: Verify Compliance

### Checklist:
- [ ] AppManager.xml file created
- [ ] All primitive tests defined in XML
- [ ] All 34 Python files updated
- [ ] Each file references correct `<primitive_test_name>` from XML
- [ ] Removed all `thunder_call()` imports and usage
- [ ] All files use `createTestStep()` pattern
- [ ] All files use `addParameter()` for parameters
- [ ] All files use `executeTestCase()` for execution
- [ ] All files use TDK framework's result handling
- [ ] Removed ai2_0_utils imports related to direct API calls
- [ ] Module loading/unloading uses `obj.unloadModule()`
- [ ] Result status set via `tdkTestObj.setResultStatus()`

---

## Step 6: Validate Against Reference Components

Compare against these proven implementations:
- **PackageManager:** `framework/fileStore/testscriptsRDKV/component/PackageManager/`
- **rdkvmemcr:** `framework/fileStore/testscriptsRDKV/component/rdkvmemcr/`
- **iarmbus:** `framework/fileStore/testscriptsRDKV/component/iarmbus/`

---

## Benefits of Compliance

1. ✅ **Framework Integration:** Proper TDK framework integration for test management
2. ✅ **Standardization:** Follows RDK test framework conventions
3. ✅ **Maintainability:** Centralized test definitions in XML
4. ✅ **Scalability:** Easy to add new test cases by updating XML
5. ✅ **Validation:** Framework validates test execution results
6. ✅ **Reporting:** Proper test result reporting and analysis
7. ✅ **Consistency:** Aligns with other enterprise service tests

---

## Quick Reference: Core Changes

### Pattern Change 1: Module Loading
```python
# BEFORE ❌
obj.configureTestCase(ip, port, 'RDKV_AppManager_02_LaunchApp_Positive')
result = obj.getLoadModuleResult()

# AFTER ✅ (Same, keep this)
obj.configureTestCase(ip, port, 'RDKV_AppManager_02_LaunchApp_Positive')
result = obj.getLoadModuleResult()
```

### Pattern Change 2: Test Execution
```python
# BEFORE ❌
response = thunder_call(obj, "org.rdk.AppManager.1", "launchApp", params)

# AFTER ✅
tdkTestObj = obj.createTestStep('AppManager_LaunchApp')
tdkTestObj.addParameter("appId", "com.rdkcentral.youtube")
tdkTestObj.executeTestCase(expectedResult)
result = tdkTestObj.getResultDetails()
```

### Pattern Change 3: Result Status
```python
# BEFORE ❌
if response and "handle" in response:
    obj.setLoadModuleStatus("SUCCESS")

# AFTER ✅
if "SUCCESS" in result:
    tdkTestObj.setResultStatus("SUCCESS")
```

---

## Timeline Estimate

| Task | Effort | Time |
|------|--------|------|
| Create AppManager.xml | 2-3 hours | 1-2 days |
| Update 34 test files | 4-6 hours | 2-3 days |
| Validation & Testing | 2-3 hours | 1-2 days |
| **Total** | **8-12 hours** | **4-7 days** |

---

## Questions?

Reference the comparison analysis in `APPMANAGER_TEST_FRAMEWORK_ANALYSIS.md` for detailed differences between approaches.
