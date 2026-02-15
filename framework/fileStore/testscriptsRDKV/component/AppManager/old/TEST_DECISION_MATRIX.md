# AppManager Test Cases - Quick Decision Matrix

## Visual Overview

### Combination/Scenario Tests (15 total)

```
┌─────────────────────────────────────────────────────────────────┐
│           COMBINATION TEST MATRIX (15 Tests)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Group A: App Lifecycle (5 tests)                               │
│ ├─ SC_01: Launch → Check State → Close                 ✓ HIGH │
│ ├─ SC_02: Launch → Metadata → Properties → Terminate   ✓ HIGH │
│ ├─ SC_03: Preload → Launch → Kill                      ✓ HIGH │
│ ├─ SC_04: Multiple Apps (sequential)                   🔶 MED  │
│ └─ SC_05: Launch → Clear Data → Close → Launch         🔶 MED  │
│                                                                 │
│ Group B: System Apps (3 tests)                                 │
│ ├─ SC_06: Start → Send Intent → Stop                   ✓ HIGH │
│ ├─ SC_07: System App Properties during lifecycle       🔶 MED  │
│ └─ SC_08: Multiple System Apps concurrent              ✓ HIGH │
│                                                                 │
│ Group C: Error Handling (5 tests)                              │
│ ├─ SC_09: Error Recovery                               ✓ HIGH │
│ ├─ SC_10: State Validation                             ✓ HIGH │
│ ├─ SC_11: Rapid Launch-Close cycles                    🟡 LOW  │
│ ├─ SC_12: Property Validation                          🔶 MED  │
│ └─ SC_13: Clear Data (running vs. closed)              🔶 MED  │
│                                                                 │
│ Group D: Data Integrity (2 tests)                              │
│ ├─ SC_14: App List Consistency                         ✓ HIGH │
│ └─ SC_15: Metadata Consistency                         ✓ HIGH │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

LEGEND: ✓ HIGH = Essential | 🔶 MED = Important | 🟡 LOW = Nice-to-have
```

### Performance Tests (14 total)

```
┌─────────────────────────────────────────────────────────────────┐
│         PERFORMANCE TEST MATRIX (14 Tests)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Group E: Launch Performance (4 tests)                          │
│ ├─ PF_01: App Launch Time Baseline                     ✓ HIGH │
│ ├─ PF_02: Preload vs. Cold Start Comparison            ✓ HIGH │
│ ├─ PF_03: Sequential Launches Impact                   🔶 MED  │
│ └─ PF_04: Close/Terminate/Kill Comparison              🔶 MED  │
│                                                                 │
│ Group F: Concurrent Operations (4 tests)                       │
│ ├─ PF_05: Concurrent Launch (parallel)                 ✓ HIGH │
│ ├─ PF_06: Mixed Ops Parallel (launch+query+close)      ✓ HIGH │
│ ├─ PF_07: Rapid Transitions (stress)                   🟡 LOW  │
│ └─ PF_08: Query Under Load                             🔶 MED  │
│                                                                 │
│ Group G: Resource Management (3 tests)                         │
│ ├─ PF_09: Memory Profile (lifecycle)                   ✓ HIGH │
│ ├─ PF_10: CPU Impact Analysis                          🔶 MED  │
│ └─ PF_11: Max Concurrent Apps (limit testing)          ✓ HIGH │
│                                                                 │
│ Group H: API Response Time (3 tests)                           │
│ ├─ PF_12: Individual API Response Baseline              🔶 MED  │
│ ├─ PF_13: API Consistency (response variance)           🟡 LOW  │
│ └─ PF_14: Metadata Size Impact                          🟡 LOW  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Execution Time & Resource Impact

### Test Execution Timeline

```
Combination Tests:     ~45 minutes
  - Sequential execution preferred
  - Light resource usage
  
Performance Tests:     ~180 minutes (3 hours)
  - Can run in parallel (different apps)
  - Requires system monitoring
  - Resource intensive
  
Total Full Suite:      ~225 minutes (3.75 hours)
```

### Recommended Minimum Set

For a **45-minute test run** (combination only):
- **9 tests** (HIGH priority): SC_01, SC_02, SC_03, SC_06, SC_08, SC_09, SC_10, SC_14, SC_15

For a **90-minute test run** (combination + quick perf):
- **9 combination tests** (above)
- **5 performance tests**: PF_01, PF_02, PF_05, PF_06, PF_09, PF_11

For a **full test suite** (225 minutes):
- All 15 combination tests
- All 14 performance tests

---

## API Coverage Matrix

### Combination Tests Coverage

| API Method | Tests Using It | Count |
|---|---|---|
| **launchApp** | SC_01, SC_02, SC_03, SC_04, SC_05, SC_09, SC_10, SC_11, SC_14 | 9 |
| **closeApp** | SC_01, SC_05, SC_09, SC_10, SC_14 | 5 |
| **getLoadedApps** | SC_01, SC_03, SC_04, SC_06, SC_07, SC_08, SC_14 | 7 |
| **getAppMetadata** | SC_02, SC_15 | 2 |
| **getAppProperty** | SC_02, SC_07, SC_12 | 3 |
| **terminateApp** | SC_02, SC_05, SC_13 | 3 |
| **killApp** | SC_03, SC_04 | 2 |
| **clearAppData** | SC_05, SC_11, SC_13 | 3 |
| **preloadApp** | SC_03 | 1 |
| **setAppProperty** | SC_07, SC_12 | 2 |
| **startSystemApp** | SC_06, SC_07, SC_08 | 3 |
| **stopSystemApp** | SC_06, SC_07, SC_08 | 3 |
| **sendIntent** | SC_06 | 1 |
| **getInstalledApps** | SC_14 | 1 |
| **getMaxRunningApps** | SC_08, SC_14 | 2 |

### Combination Tests: API Count Hit Rate

- **All 21 APIs**: ~90% covered in 15 tests
- **Core 10 APIs**: 100% covered
- **Advanced 11 APIs**: 70-80% covered

---

## Implementation Suggestion

### Phase 1: Essential Workflows (Week 1)
Create these HIGH priority tests first:
- SC_01, SC_02, SC_03, SC_06, SC_08, SC_09, SC_10, SC_14, SC_15
- **Impact:** Covers all critical app lifecycle workflows
- **Effort:** ~16 hours
- **ROI:** Very High

### Phase 2: Performance Baselines (Week 2)
Add these HIGH priority performance tests:
- PF_01, PF_02, PF_05, PF_06, PF_09, PF_11
- **Impact:** Establishes performance baselines for regression detection
- **Effort:** ~20 hours
- **ROI:** High

### Phase 3: Comprehensive Coverage (Week 3)
Add remaining tests:
- SC_04, SC_05, SC_07, SC_11, SC_12, SC_13
- PF_03, PF_04, PF_07, PF_08, PF_10, PF_12, PF_13, PF_14
- **Impact:** Complete coverage and stress testing
- **Effort:** ~24 hours
- **ROI:** Medium-High

---

## Decision Checklist

**For User to Review:**

### Combination Tests
- [ ] Include SC_01-SC_03, SC_06, SC_08? (Product workflows)
- [ ] Include SC_04-SC_05, SC_07? (Concurrent scenarios)
- [ ] Include SC_09-SC_13? (Error handling)
- [ ] Include SC_14-SC_15? (Data consistency)
- [ ] Any tests to add/remove?

### Performance Tests
- [ ] Include PF_01-PF_02? (Launch performance baseline)
- [ ] Include PF_05-PF_06? (Concurrency testing)
- [ ] Include PF_09, PF_11? (Resource limits)
- [ ] Include PF_03, PF_04, PF_08? (Detailed profiling)
- [ ] Include PF_07, PF_10, PF_12-PF_14? (Stress & detailed analysis)
- [ ] Need custom performance metrics?

### Special Requirements
- [ ] Need memory leak testing?
- [ ] Need CPU profiling?
- [ ] Need network/IPC testing?
- [ ] Need real app vs. stub comparison?
- [ ] Need compatibility testing (different RDK versions)?

---

## File Generation Plan

Once approved, will create:

**Python Test Files (29 total):**
```
RDKV_AppManager_35_Scenario_LaunchStateClose.py
RDKV_AppManager_36_Scenario_LaunchMetadataTerminate.py
...
RDKV_AppManager_63_Performance_MetadataSize.py
```

**Documentation Files:**
```
COMBINATION_TESTS_GUIDE.md
PERFORMANCE_TESTS_GUIDE.md
PERFORMANCE_BASELINES.md  (populated with initial runs)
TROUBLESHOOTING_SCENARIOS.md
```

**Shell Script for Batch Execution:**
```
run_appmanager_scenario_tests.sh
run_appmanager_performance_tests.sh
run_appmanager_full_test_suite.sh
```

---

## Questions for User

1. **Priority:** Which test group matters most?
   - [ ] Combination/Scenario (real workflows)
   - [ ] Performance (system optimization)
   - [ ] Both equally

2. **Time Available:** How long can tests run?
   - [ ] ~45 min (Combination only)
   - [ ] ~90 min (Combo + core perf)
   - [ ] ~225 min (Full suite)
   - [ ] Other: ___

3. **Device Constraints:** What should we test for?
   - [ ] RPI4 specific optimizations
   - [ ] Low-resource handling
   - [ ] High-concurrency scenarios
   - [ ] All equally

4. **Metrics:** Which matter most for your use case?
   - [ ] Correctness/functionality
   - [ ] Response times
   - [ ] Resource usage (memory, CPU)
   - [ ] Stability under stress
   - [ ] All of above

5. **Unwanted Tests:** Any test categories to skip?
   - [ ] Remove stress tests (PF_07, PF_08)?
   - [ ] Remove detailed profiling (PF_12, PF_13, PF_14)?
   - [ ] Remove legacy scenarios?
   - [ ] Other: ___

