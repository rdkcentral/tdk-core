# Proposed AppManager Combination & Performance Test Cases

**Document Version:** 1.0  
**Date:** February 9, 2026  
**Status:** PROPOSED FOR REVIEW

---

## Part 1: Combination/Scenario Test Cases (18 tests)

These tests combine multiple AppManager API methods to validate realistic workflows and state transitions.

### Group A: App Launch & Lifecycle Scenarios (5 tests)

#### **SC_01: Launch, Check State, and Close Workflow**
- **Test ID:** TC_AppManager_Scenario_LaunchStateClose
- **File Name:** RDKV_AppManager_35_Scenario_LaunchStateClose.py
- **Type:** Positive Scenario
- **API Methods:** launchApp → getLoadedApps → closeApp
- **Objective:** Verify app launches, appears in loaded apps list, and closes gracefully
- **Expected Behavior:** 
  - launchApp returns success
  - App appears in getLoadedApps result
  - closeApp succeeds and app disappears from loaded apps

#### **SC_02: Launch, Verify Metadata, Verify Properties, Terminate**
- **Test ID:** TC_AppManager_Scenario_LaunchMetadataTerminate  
- **File Name:** RDKV_AppManager_36_Scenario_LaunchMetadataTerminate.py
- **Type:** Positive Scenario
- **API Methods:** launchApp → getAppMetadata → getAppProperty → terminateApp
- **Objective:** Verify app properties and metadata are consistent after launch
- **Expected Behavior:**
  - launchApp succeeds
  - getAppMetadata returns valid metadata
  - getAppProperty shows correct state (running)
  - terminateApp succeeds

#### **SC_03: Preload, Launch, Verify State, Kill**
- **Test ID:** TC_AppManager_Scenario_PreloadLaunchKill
- **File Name:** RDKV_AppManager_37_Scenario_PreloadLaunchKill.py
- **Type:** Positive Scenario  
- **API Methods:** preloadApp → launchApp → getLoadedApps → killApp
- **Objective:** Verify preloaded apps launch faster and state transitions work correctly
- **Expected Behavior:**
  - preloadApp succeeds
  - launchApp completes (should be faster)
  - App in getLoadedApps
  - killApp removes app from loaded apps immediately
- **Performance Metric:** Measure time difference between preloaded and non-preloaded launch

#### **SC_04: Multiple Apps Lifecycle (Sequential)**
- **Test ID:** TC_AppManager_Scenario_MultipleAppsSequential
- **File Name:** RDKV_AppManager_38_Scenario_MultipleAppsSequential.py
- **Type:** Positive Scenario
- **API Methods:** launchApp (App1) → launchApp (App2) → getLoadedApps → closeApp (App1) → closeApp (App2)
- **Objective:** Verify multiple apps can run concurrently and be individually managed
- **Expected Behavior:**
  - Both apps launch successfully
  - Both appear in getLoadedApps
  - Individual close operations work
  - Only remaining app in getLoadedApps after close
- **Performance Metric:** Measure CPU and memory with 2 concurrent apps

#### **SC_05: Launch After Clear Data**
- **Test ID:** TC_AppManager_Scenario_LaunchAfterClearData
- **File Name:** RDKV_AppManager_39_Scenario_LaunchAfterClearData.py
- **Type:** Positive Scenario
- **API Methods:** launchApp → clearAppData → closeApp → launchApp
- **Objective:** Verify app restarts cleanly after data is cleared
- **Expected Behavior:**
  - App launches normally
  - clearAppData succeeds
  - App closes successfully
  - App relaunches with fresh state (no errors)

---

### Group B: System App Management Scenarios (3 tests)

#### **SC_06: Start System App, Send Intent, Stop System App**
- **Test ID:** TC_AppManager_Scenario_SystemAppIntent
- **File Name:** RDKV_AppManager_40_Scenario_SystemAppIntent.py
- **Type:** Positive Scenario
- **API Methods:** startSystemApp → sendIntent → getLoadedApps → stopSystemApp
- **Objective:** Verify system apps can be controlled and receive intents
- **Expected Behavior:**
  - startSystemApp succeeds
  - sendIntent delivery succeeds
  - App appears in getLoadedApps
  - stopSystemApp removes app cleanly

#### **SC_07: Verify System App Properties During Lifecycle**
- **Test ID:** TC_AppManager_Scenario_SystemAppProperties
- **File Name:** RDKV_AppManager_41_Scenario_SystemAppProperties.py
- **Type:** Positive Scenario
- **API Methods:** startSystemApp → getAppProperty → setAppProperty → stopSystemApp
- **Objective:** Verify system app properties can be queried and modified during runtime
- **Expected Behavior:**
  - startSystemApp succeeds
  - getAppProperty retrieves valid properties
  - setAppProperty updates properties
  - Property change affects app behavior appropriately
  - stopSystemApp succeeds

#### **SC_08: Multiple System Apps Concurrent**
- **Test ID:** TC_AppManager_Scenario_MultipleSystemApps
- **File Name:** RDKV_AppManager_42_Scenario_MultipleSystemApps.py
- **Type:** Positive Scenario
- **API Methods:** startSystemApp (App1) → startSystemApp (App2) → getLoadedApps → stopSystemApp (App1) → stopSystemApp (App2)
- **Objective:** Verify resource limits when multiple system apps run concurrently
- **Expected Behavior:**
  - Both system apps start
  - Both appear in getLoadedApps
  - getMaxRunningApps indicates current load
  - Individual stops work correctly
- **Performance Metric:** CPU, memory, and system resource usage

---

### Group C: Error Handling & State Recovery (5 tests)

#### **SC_09: Launch Nonexistent App, Verify Error, Then Launch Valid App**
- **Test ID:** TC_AppManager_Scenario_ErrorRecovery
- **File Name:** RDKV_AppManager_43_Scenario_ErrorRecovery.py
- **Type:** Mixed (Negative → Positive)
- **API Methods:** launchApp (invalid) → launchApp (valid) → closeApp
- **Objective:** Verify system recovers from failed launch and continues functioning
- **Expected Behavior:**
  - Invalid launchApp returns error
  - Valid launchApp still succeeds (no system corruption)
  - App state is clean
  - closeApp works normally

#### **SC_10: Close Non-running App, Then Close Running App**
- **Test ID:** TC_AppManager_Scenario_StateValidation
- **File Name:** RDKV_AppManager_44_Scenario_StateValidation.py
- **Type:** Mixed Scenario
- **API Methods:** closeApp (invalid ID) → launchApp → closeApp (valid)
- **Objective:** Verify API validates app state properly
- **Expected Behavior:**
  - closeApp on invalid app returns error
  - launchApp succeeds
  - closeApp on running app succeeds
  - No state corruption

#### **SC_11: Rapid Launch-Close-Launch Cycles**
- **Test ID:** TC_AppManager_Scenario_RapidLifecycle
- **File Name:** RDKV_AppManager_45_Scenario_RapidLifecycle.py
- **Type:** Stability Scenario
- **API Methods:** [launchApp → closeApp] × 5 cycles
- **Objective:** Verify system stability under rapid app lifecycle transitions
- **Expected Behavior:**
  - All 5 cycles complete without errors
  - App states remain consistent
  - No memory leaks observed
- **Performance Metric:** Track app launch time degradation across cycles

#### **SC_12: Property Set on Invalid App Followed by Valid Set**
- **Test ID:** TC_AppManager_Scenario_PropertyValidation
- **File Name:** RDKV_AppManager_46_Scenario_PropertyValidation.py
- **Type:** Mixed Scenario
- **API Methods:** setAppProperty (invalid) → launchApp → setAppProperty (valid) → getAppProperty
- **Objective:** Verify property operations handle invalid app IDs gracefully
- **Expected Behavior:**
  - setAppProperty on invalid app returns error
  - launchApp succeeds
  - setAppProperty on valid app succeeds
  - getAppProperty confirms change

#### **SC_13: Clear App Data While App Running vs. After Closed**
- **Test ID:** TC_AppManager_Scenario_ClearDataStates
- **File Name:** RDKV_AppManager_47_Scenario_ClearDataStates.py
- **Type:** Positive Scenario
- **API Methods:** launchApp (App1) → clearAppData (App1) → terminateApp (App1) → launchApp (App2) → clearAppData (App2) → closeApp (App2)
- **Objective:** Verify clearAppData works regardless of app state
- **Expected Behavior:**
  - clearAppData succeeds both while app running and after closed
  - App restart shows clean state
  - No errors in state transitions

---

### Group D: Data Integrity & Metadata Scenarios (2 tests)

#### **SC_14: Verify Installed/Loaded App Consistency**
- **Test ID:** TC_AppManager_Scenario_AppListConsistency
- **File Name:** RDKV_AppManager_48_Scenario_AppListConsistency.py
- **Type:** Positive Query Scenario
- **API Methods:** getInstalledApps → launchApp (one of them) → getLoadedApps → closeApp
- **Objective:** Verify app lists remain consistent and logically correct
- **Expected Behavior:**
  - Launched app appears in getLoadedApps
  - All loaded apps exist in getInstalledApps
  - Closed apps disappear from getLoadedApps
  - Total loaded never exceeds getMaxRunningApps

#### **SC_15: Metadata Consistency Before/After Operations**
- **Test ID:** TC_AppManager_Scenario_MetadataConsistency
- **File Name:** RDKV_AppManager_49_Scenario_MetadataConsistency.py
- **Type:** Positive Query Scenario
- **API Methods:** getAppMetadata → launchApp → getAppMetadata → closeApp → getAppMetadata
- **Objective:** Verify app metadata does not change inappropriately
- **Expected Behavior:**
  - Metadata before launch, running, and after close is identical (except state)
  - appId, name, version unchanged
  - Only state property changes based on app status

---

## Part 2: Performance Test Cases (14 tests)

Performance tests measure system response times, resource usage, and scalability limits.

### Group E: App Launch Performance (4 tests)

#### **PF_01: App Launch Time Baseline (Single App)**
- **Test ID:** TC_AppManager_Performance_LaunchBaseline
- **File Name:** RDKV_AppManager_50_Performance_LaunchBaseline.py
- **Type:** Performance Baseline
- **API Methods:** launchApp
- **Metrics to Capture:**
  - Time from API call to app appearing in getLoadedApps
  - First-launch vs. subsequent launch times
  - Memory footprint increase
- **Success Criteria:** Launch time < 5 seconds, memory increase < 50MB
- **Test Duration:** 60 seconds
- **Note:** Baseline for comparison with other scenarios

#### **PF_02: Preload Performance vs. Cold Start**
- **Test ID:** TC_AppManager_Performance_PreloadVsColdStart
- **File Name:** RDKV_AppManager_51_Performance_PreloadVsColdStart.py
- **Type:** Performance Comparison
- **API Methods:** preloadApp → launchApp (preloaded) vs. launchApp (cold)
- **Metrics to Capture:**
  - Launch time with preload
  - Launch time without preload
  - Preload overhead
- **Success Criteria:** Preloaded launch < cold launch, preload overhead < 1 second
- **Test Duration:** 120 seconds

#### **PF_03: Sequential App Launches Impact on Performance**
- **Test ID:** TC_AppManager_Performance_SequentialLaunches
- **File Name:** RDKV_AppManager_52_Performance_SequentialLaunches.py
- **Type:** Performance Degradation Analysis
- **API Methods:** launchApp (N times)
- **Metrics to Capture:**
  - Launch time for 1st, 2nd, 3rd, 4th, 5th app
  - CPU usage trend
  - Memory usage trend
  - System response time degradation
- **Success Criteria:** Degradation < 20%, no crashes
- **Test Duration:** 300 seconds
- **Parameters:** Test with 3, 5, 10 apps

#### **PF_04: Close/Terminate/Kill Performance Comparison**
- **Test ID:** TC_AppManager_Performance_StopMethodsComparison
- **File Name:** RDKV_AppManager_53_Performance_StopMethodsComparison.py
- **Type:** Performance Comparison
- **API Methods:** closeApp, terminateApp, killApp
- **Metrics to Capture:**
  - Time to execute each method
  - Time for app to disappear from getLoadedApps
  - Resource cleanup time
- **Success Criteria:** All methods complete under 2 seconds
- **Test Duration:** 180 seconds

---

### Group F: Concurrent Operations Performance (4 tests)

#### **PF_05: Concurrent App Operations (Launch Parallel)**
- **Test ID:** TC_AppManager_Performance_ConcurrentLaunch
- **File Name:** RDKV_AppManager_54_Performance_ConcurrentLaunch.py
- **Type:** Performance Scalability
- **API Methods:** Multiple launchApp calls in parallel (threading)
- **Metrics to Capture:**
  - Total time to launch N apps in parallel
  - Throughput (apps/second)
  - Error rate
  - System resource limits hit
- **Success Criteria:** 5 concurrent launches complete, error rate < 5%
- **Test Duration:** 180 seconds
- **Parameters:** Test with 3, 5, 10 concurrent threads

#### **PF_06: Mixed Operations Performance (Launch, Query, Close simultaneously)**
- **Test ID:** TC_AppManager_Performance_MixedOpsParallel
- **File Name:** RDKV_AppManager_55_Performance_MixedOpsParallel.py
- **Type:** Performance Concurrency
- **API Methods:** launchApp, getLoadedApps, closeApp (concurrent)
- **Metrics to Capture:**
  - API response times under concurrent load
  - Consistency of getLoadedApps output
  - Lock contention observations
- **Success Criteria:** No deadlocks, all operations < 2s response time
- **Test Duration:** 300 seconds

#### **PF_07: Rapid State Transitions (Launch-Close-Launch cycles)**
- **Test ID:** TC_AppManager_Performance_RapidTransitions
- **File Name:** RDKV_AppManager_56_Performance_RapidTransitions.py
- **Type:** Performance Stress
- **API Methods:** [launchApp → closeApp] in rapid succession
- **Metrics to Capture:**
  - Minimum time between launch and close
  - System stability indicators
  - Memory leak detection
  - Error rate
- **Success Criteria:** 100 cycles complete, no memory growth pattern, error rate 0%
- **Test Duration:** 600 seconds

#### **PF_08: Query Performance Under Load**
- **Test ID:** TC_AppManager_Performance_QueryUnderLoad
- **File Name:** RDKV_AppManager_57_Performance_QueryUnderLoad.py
- **Type:** Performance Query
- **API Methods:** getLoadedApps, getInstalledApps (rapidly, while apps launching/closing)
- **Metrics to Capture:**
  - Query response time vs. system load
  - Data consistency of results
  - Query throughput (queries/second)
- **Success Criteria:** Response time < 500ms even under load
- **Test Duration:** 300 seconds

---

### Group G: Resource Management Performance (3 tests)

#### **PF_09: Memory Profile - App Lifecycle**
- **Test ID:** TC_AppManager_Performance_MemoryProfile
- **File Name:** RDKV_AppManager_58_Performance_MemoryProfile.py
- **Type:** Performance Resource Profile
- **API Methods:** launchApp, getAppProperty (monitor), closeApp
- **Metrics to Capture:**
  - Memory before launch
  - Memory during running
  - Memory after close
  - Leaked memory (if any)
  - RSS vs. VSZ tracking
- **Success Criteria:** Memory returns to baseline ±10% after close
- **Test Duration:** 120 seconds per app
- **Parameters:** Test multiple apps

#### **PF_10: CPU Impact Analysis**
- **Test ID:** TC_AppManager_Performance_CPUProfile
- **File Name:** RDKV_AppManager_59_Performance_CPUProfile.py
- **Type:** Performance Resource Profile
- **API Methods:** launchApp, monitor CPU, closeApp
- **Metrics to Capture:**
  - Average CPU % during running
  - CPU % during API calls
  - CPU peaks
  - System CPU vs. app CPU
- **Success Criteria:** Average CPU < 50%, peaks < 80%
- **Test Duration:** 120 seconds
- **Parameters:** Light app vs. heavy app

#### **PF_11: Scalability - Maximum Concurrent Apps**
- **Test ID:** TC_AppManager_Performance_MaxConcurrentApps
- **File Name:** RDKV_AppManager_60_Performance_MaxConcurrentApps.py
- **Type:** Performance Limit Testing
- **API Methods:** launchApp (until limit), getMaxRunningApps
- **Metrics to Capture:**
  - Actual max concurrent apps
  - System degradation at limit
  - Error when exceeding limit
  - Recovery after limit reached
- **Success Criteria:** Respects getMaxRunningApps limit, graceful error
- **Test Duration:** 300 seconds

---

### Group H: API Response Time Performance (3 tests)

#### **PF_12: Individual API Response Time Baseline**
- **Test ID:** TC_AppManager_Performance_APIBaseline
- **File Name:** RDKV_AppManager_61_Performance_APIBaseline.py
- **Type:** Performance Baseline
- **API Methods:** All AppManager APIs (individual calls)
- **Metrics to Capture:**
  - Response time for each API
  - P50, P95, P99 latencies
  - Error rate
- **Success Criteria:** All APIs < 2 seconds
- **Test Duration:** 300 seconds

#### **PF_13: API Consistency - Same Call Multiple Times**
- **Test ID:** TC_AppManager_Performance_APIConsistency
- **File Name:** RDKV_AppManager_62_Performance_APIConsistency.py
- **Type:** Performance Consistency
- **API Methods:** Repeated calls to same API
- **Metrics to Capture:**
  - Response time variance
  - Result consistency
  - Outliers/jitter
- **Success Criteria:** Response time variance < 20%
- **Test Duration:** 300 seconds

#### **PF_14: Metadata Size Impact on Performance**
- **Test ID:** TC_AppManager_Performance_MetadataSize
- **File Name:** RDKV_AppManager_63_Performance_MetadataSize.py
- **Type:** Performance Scalability
- **API Methods:** getAppMetadata (apps with varied metadata)
- **Metrics to Capture:**
  - Response time vs. metadata size
  - Network payload impact
  - Parsing overhead
- **Success Criteria:** No significant degradation with large metadata
- **Test Duration:** 120 seconds

---

## Summary Statistics

### Combination/Scenario Test Cases
- **Total:** 15 tests (SC_01 - SC_15)
- **Positive:** 12
- **Mixed/Negative:** 3
- **Estimated Execution Time:** ~45 minutes
- **API Methods Covered:** All 21 APIs
- **Real-world Workflows:** 13 scenarios

### Performance Test Cases  
- **Total:** 14 tests (PF_01 - PF_14)
- **Baseline:** 2
- **Comparison:** 2
- **Stress:** 2
- **Resource Profile:** 3
- **Scalability:** 2
- **API Response:** 3
- **Estimated Execution Time:** ~180 minutes (3 hours)
- **Key Metrics:** Response time, throughput, resource usage, stability

### Grand Total
- **Combination Tests:** 15
- **Performance Tests:** 14
- **Total New Tests:** 29
- **Combined with existing 34 tests:** 63 total test cases
- **Total Estimated Execution Time:** ~225 minutes (3.75 hours)

---

## Recommendations

### High Priority (Can't Skip)
1. **SC_01, SC_02, SC_03** - Core lifecycle workflows
2. **SC_08** - System app management critical
3. **SC_09, SC_10, SC_11** - Error handling essential
4. **PF_01, PF_02** - Performance baselines needed
5. **PF_05, PF_06** - Concurrency critical for RDK devices

### Medium Priority (Important for Robustness)
1. **SC_04, SC_05, SC_14, SC_15** - Data consistency
2. **SC_06, SC_07** - System app intents
3. **PF_03, PF_04** - Degradation analysis
4. **PF_09, PF_10, PF_11** - Resource limits

### Nice to Have (Can be deferred)
1. **SC_12, SC_13** - Edge cases
2. **PF_07, PF_08** - Stress testing
3. **PF_12, PF_13, PF_14** - API detailed profiling

---

## Next Steps

**For User Review:**
1. Which combination tests would you like to keep?
2. Which combination tests should be removed?
3. Which performance tests are relevant for your use case?
4. Should we add more tests for specific scenarios?

**Upon Approval:**
1. Create Python test files following existing patterns
2. Add to TDK test execution framework
3. Document expected baselines
4. Set up performance regression tracking

