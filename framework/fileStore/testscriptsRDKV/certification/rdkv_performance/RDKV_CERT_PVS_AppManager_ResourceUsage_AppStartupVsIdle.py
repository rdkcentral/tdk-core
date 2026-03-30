##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
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


##########################################################################
# Copyright 2026 RDK Management
##########################################################################

import tdklib
from StabilityTestUtility import *
from rdkv_performancelib import *
import json
import time

obj = tdklib.TDKScriptingLibrary("rdkv_performance", "1", standAlone=True)
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_CERT_PVS_AppManager_ResourceUsage_AppStartupVsIdle')
pre_requisite_reboot(obj, "no")

# ============================================================
# LOAD MODULE
# ============================================================
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  : %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    print("\n Check Pre conditions\n")
    final_status = "SUCCESS"
    app_id = application_name
    app_download_url = application_url

    # ========================================================
    # INSTALL + LAUNCH
    # ========================================================
    print("\nInstalling and Launching App...\n")

    status = rdkservice_install_launch_app(obj, app_id, app_id, app_download_url)

    if status != "SUCCESS":
        print("App install/launch failed")
        final_status = "FAILURE"

    # ========================================================
    # STARTUP RESOURCE VALIDATION
    # ========================================================
    if final_status == "SUCCESS":

        print("\nValidating Startup Resource Usage...\n")

        tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
        tdkTestObj.executeTestCase(expectedResult)

        result = tdkTestObj.getResult()
        resource_usage = tdkTestObj.getResultDetails()

        if expectedResult in result and resource_usage != "ERROR":
            print("\nStartup Resource usage validated\n")
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("\nStartup Resource validation failed\n")
            tdkTestObj.setResultStatus("FAILURE")
            final_status = "FAILURE"

    # ========================================================
    # IDLE PHASE
    # ========================================================
    if final_status == "SUCCESS":

        print("\nWaiting for Idle state...\n")
        time.sleep(30)

        print("\nValidating Idle Resource Usage...\n")

        tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
        tdkTestObj.executeTestCase(expectedResult)

        result = tdkTestObj.getResult()
        resource_usage = tdkTestObj.getResultDetails()

        if expectedResult in result and resource_usage != "ERROR":
            print("\nIdle Resource usage validated\n")
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("\nIdle Resource validation failed\n")
            tdkTestObj.setResultStatus("FAILURE")
            final_status = "FAILURE"

    # ========================================================
    # TERMINATE APP
    # ========================================================
    print("\nTerminating App...\n")

    tdkTestObj = obj.createTestStep('rdkservice_terminateApp')
    tdkTestObj.addParameter("appId", app_id)
    tdkTestObj.executeTestCase(expectedResult)

    if tdkTestObj.getResult() == "SUCCESS":
        print("App terminated successfully")
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("App termination failed")
        tdkTestObj.setResultStatus("FAILURE")

    # ========================================================
    # FINAL STATUS
    # ========================================================
    if final_status == "SUCCESS":
        obj.setLoadModuleStatus("SUCCESS")
    else:
        obj.setLoadModuleStatus("FAILURE")

    # ========================================================
    # CLEANUP
    # ========================================================
    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")

'''import tdklib
from StabilityTestUtility import *
from PerformanceTestVariables import *
from rdkv_performancelib import *
import rdkv_performancelib
import json
import time


def get_resource_usage():
    info = rdkservice_getValue("org.rdk.DeviceInfo.1.getSystemResourceInfo")
    cpu = 0.0
    memory = 0.0
    if info and "SUCCESS" in info.upper():
        try:
            payload = json.loads(info)
            result = payload.get("result") or {}
            cpu = float(result.get("cpuUsage", result.get("CPU", 0)))
            memory = float(result.get("memoryUsage", result.get("memory", 0)))
        except Exception as e:
            print("Could not parse resource info:", e)
    return {"cpu": cpu, "memory": memory}


def ensure_app_installed(app_id, url):
    installed_apps_result = rdkservice_getValue("org.rdk.AppManager.1.getInstalledApps")
    installed = False
    if installed_apps_result and "SUCCESS" in installed_apps_result.upper():
        try:
            response = json.loads(installed_apps_result)
            for app in response.get("result", []):
                if app.get("appId") == app_id:
                    installed = True
                    break
        except Exception as e:
            print("Could not parse installed apps:", e)
    if not installed:
        bundle_name = url.split('/')[-1]
        status = rdkservice_install_launch_app(obj, bundle_name, app_id, url)
        if status != "SUCCESS":
            return False
        time.sleep(5)
        rdkv_terminate_app(app_id)
    return True


obj = tdklib.TDKScriptingLibrary("rdkv_performance", "1", standAlone=True)

ip = <ipaddress>
port = <port>
obj.configureTestCase(ip, port, 'RDKV_CERT_PVS_AppManager_ResourceUsage_AppStartupVsIdle')
pre_requisite_reboot(obj, "no")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  : %s" % result)
obj.setLoadModuleStatus(result)

if "SUCCESS" not in result.upper():
    obj.setLoadModuleStatus("FAILURE")
    raise SystemExit("Module load failure")

app_id = application_name

if not ensure_app_installed(app_id, lightning_test_app_url):
    print("App install failed")
    obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance")
    raise SystemExit(1)

# Idle baseline
idle_samples = []
for i in range(4):
    sample = get_resource_usage()
    idle_samples.append(sample)
    print(f"Idle sample {i+1}: CPU {sample['cpu']}%, Mem {sample['memory']} MB")
    time.sleep(5)

idle_cpu_avg = round(sum(s['cpu'] for s in idle_samples) / len(idle_samples), 2)
idle_mem_avg = round(sum(s['memory'] for s in idle_samples) / len(idle_samples), 2)
print(f"Idle baseline: CPU {idle_cpu_avg}%, Mem {idle_mem_avg} MB")

# Startup phase
print(f"Launching app {app_id} for startup measurement")
start_time = time.time()
rdkservice_launch_app(app_id)

startup_samples = []
startup_duration = 30
interval = 5
for i in range(int(startup_duration / interval)):
    time.sleep(interval)
    sample = get_resource_usage()
    startup_samples.append(sample)
    print(f"Startup sample {i+1}: CPU {sample['cpu']}%, Mem {sample['memory']} MB")

# Steady state phase
steady_samples = []
steady_duration = 60
steady_interval = 10
for i in range(int(steady_duration / steady_interval)):
    time.sleep(steady_interval)
    sample = get_resource_usage()
    steady_samples.append(sample)
    print(f"Steady sample {i+1}: CPU {sample['cpu']}%, Mem {sample['memory']} MB")

startup_cpu_avg = round(sum(s['cpu'] for s in startup_samples) / len(startup_samples), 2)
startup_mem_avg = round(sum(s['memory'] for s in startup_samples) / len(startup_samples), 2)
steady_cpu_avg = round(sum(s['cpu'] for s in steady_samples) / len(steady_samples), 2)
steady_mem_avg = round(sum(s['memory'] for s in steady_samples) / len(steady_samples), 2)

print(f"App startup average: CPU {startup_cpu_avg}%, Mem {startup_mem_avg} MB")
print(f"App steady average: CPU {steady_cpu_avg}%, Mem {steady_mem_avg} MB")

# Done. Evaluate simple check: app loaded and steady rate stable
loaded_apps = rdkservice_get_loaded_apps()
if app_id in loaded_apps:
    print("Scenario result: SUCCESS")
    obj.setLoadModuleStatus("SUCCESS")
else:
    print("Scenario result: FAILURE")
    obj.setLoadModuleStatus("FAILURE")

# cleanup
rdkv_terminate_app(app_id)
obj.unloadModule("rdkv_performance")
'''