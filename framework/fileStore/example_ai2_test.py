##########################################################################
# Example AI2.0 Test Script using ai2_0_utils
#
# This script demonstrates how to use the common configure_tdk_test_case
# function for both PackageManager and StorageManager tests.
##########################################################################

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
from ai2_0_utils import configure_tdk_test_case, create_tdk_test_step, set_test_step_status

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices", "1", standAlone=True)

# IP and Port of box
ip = "192.168.1.100"  # Replace with actual device IP
port = 8087           # Replace with actual device port

# Configure test case using the common utility function
# This replaces the old configureTestCase() call with all required parameters
result = configure_tdk_test_case(obj, ip, port, 'Example_AI2_Test')

if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedResult = "SUCCESS"
    
    # Example test step
    tdkTestObj = create_tdk_test_step(obj, "Test_AI2_Function", "Testing AI2.0 functionality")
    
    try:
        # Your test logic here
        print("[TEST] Executing AI2.0 test logic...")
        
        # For demonstration - this would be your actual test code
        test_passed = True  # Replace with actual test result
        
        if test_passed:
            print("[TEST] AI2.0 test passed")
            set_test_step_status(tdkTestObj, "SUCCESS", "AI2.0 functionality working correctly")
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("[TEST] AI2.0 test failed")
            set_test_step_status(tdkTestObj, "FAILURE", "AI2.0 functionality not working")
            tdkTestObj.setResultStatus("FAILURE")
            
    except Exception as e:
        print(f"[ERROR] Exception during test: {str(e)}")
        set_test_step_status(tdkTestObj, "FAILURE", f"Test exception: {str(e)}")
        tdkTestObj.setResultStatus("FAILURE")
        
    # Execute the test step
    tdkTestObj.executeTestCase(expectedResult)
    
    # Print final results
    actualResult = tdkTestObj.getResult()
    print(f"[RESULT] Expected: {expectedResult}, Actual: {actualResult}")
    
    if expectedResult in actualResult:
        obj.setLoadModuleStatus("SUCCESS")
        print("[TEST RESULT] SUCCESS")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("[TEST RESULT] FAILURE")
        
else:
    print("[ERROR] Failed to configure test case")
    obj.setLoadModuleStatus("FAILURE")

# Unload the module
obj.unloadModule("rdkservices")