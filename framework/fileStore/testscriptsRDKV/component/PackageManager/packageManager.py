import sys
import os

try:
    import tdklib
except Exception as e:
    raise ImportError(
        "tdklib not found. Ensure the TDK environment provides tdklib on PYTHONPATH.\n"
        f"Original error: {e}")

# Create TDK scripting object for PackageManager component
obj = tdklib.TDKScriptingLibrary("PackageManager", "1")

# IP and Port of DUT (Device Under Test)
# Use quoted placeholders so the file remains valid Python while the TDK harness
# replaces these placeholder strings at runtime when executing the test.
ip = "<ipaddress>"
port = "<port>"
obj.configureTestCase(ip, port, 'PackageManagerRDKEMS')

# Load module
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")

    # Invoke PackageManager XML via standard rdkservice_test primitive
    tdkTestObj = obj.createTestStep('rdkservice_test')
    tdkTestObj.addParameter("xml_name", "PackageManagerRDKEMS")
    tdkTestObj.executeTestCase("SUCCESS")
    obj.unloadModule("PackageManager")
else:
    print("[ERROR] Failed to load PackageManager module")
    obj.setLoadModuleStatus("FAILURE")
