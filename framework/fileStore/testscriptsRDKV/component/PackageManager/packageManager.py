import sys
import os

try:
    import tdklib
except Exception as e:
    raise ImportError(
        "tdklib not found. Ensure the TDK environment provides tdklib on PYTHONPATH (see RDKV_CERT_* scripts).\n"
        "Example (bash): export TDK_ROOT=/path/to/tdk && export PYTHONPATH=$TDK_ROOT/framework/web-app/fileStore:$TDK_ROOT/utilities/TDK_Automation_Scripts/python-lib\n"
        f"Original error: {e}")
 
# Create TDK scripting object for rdkservices component
obj = tdklib.TDKScriptingLibrary("rdkservices", "1")
 
# IP and Port of DUT (Device Under Test)
# Use quoted placeholders so the file remains valid Python while the TDK harness
# replaces these placeholder strings at runtime when executing the test.
ip = "<ipaddress>"
port = "<port>"
obj.configureTestCase(ip, port, 'RDKV_CERT_PackageManagerRDKEMS')
 
# Load module
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" % loadmodulestatus)
 
if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
 
    # Primitive test step to invoke XML
    tdkTestObj = obj.createTestStep('rdkservice_test')
    tdkTestObj.addParameter("xml_name", "PackageManagerRDKEMS")
    expectedresult = "SUCCESS"
 
    # Execute the XML-defined test steps
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
 
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS")
        print("[DETAILS] : %s" % details)
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE")
        print("[DETAILS] : %s" % details)
 
    obj.unloadModule("rdkservices")
 
else:
    print("[ERROR] Failed to load rdkservices module")
    obj.setLoadModuleStatus("FAILURE")