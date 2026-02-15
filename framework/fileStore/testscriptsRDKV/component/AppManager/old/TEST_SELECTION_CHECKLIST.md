# ✓ Test Case Selection Checklist

**Instructions:** Mark each row with your decision:
- ✓ = Include this test
- ✗ = Skip this test
- ? = Need more information

---

## PART A: Combination/Scenario Tests (15 total)

### Group A: App Lifecycle (5 tests)

| ID | Test Name | Description | Priority | Include? |
|---|---|---|---|---|
| SC_01 | Launch State Close | Launch → Check Running → Close | ✓ HIGH | ☐ ☐ ☐ |
| SC_02 | Launch Metadata Terminate | Launch → Metadata → Properties → Terminate | ✓ HIGH | ☐ ☐ ☐ |
| SC_03 | Preload Launch Kill | Preload → Launch → Kill (measure speedup) | ✓ HIGH | ☐ ☐ ☐ |
| SC_04 | Multiple Apps Sequential | Sequential launch/close of 2+ apps | 🔶 MED | ☐ ☐ ☐ |
| SC_05 | Launch Clear Data Close Launch | Test state after data clear | 🔶 MED | ☐ ☐ ☐ |

**Minimum Viable:** SC_01, SC_02, SC_03 (3 tests)

---

### Group B: System App Management (3 tests)

| ID | Test Name | Description | Priority | Include? |
|---|---|---|---|---|
| SC_06 | System App Intent | Start → Send Intent → Stop | ✓ HIGH | ☐ ☐ ☐ |
| SC_07 | System App Properties | System apps with property changes | 🔶 MED | ☐ ☐ ☐ |
| SC_08 | Multiple System Apps | Concurrent system apps, resource limits | ✓ HIGH | ☐ ☐ ☐ |

**Minimum Viable:** SC_06, SC_08 (2 tests)

---

### Group C: Error Handling & Recovery (5 tests)

| ID | Test Name | Description | Priority | Include? |
|---|---|---|---|---|
| SC_09 | Error Recovery | Invalid launch → Valid launch sequence | ✓ HIGH | ☐ ☐ ☐ |
| SC_10 | State Validation | Close invalid → Launch valid → Close | ✓ HIGH | ☐ ☐ ☐ |
| SC_11 | Rapid Lifecycle | 5x launch-close cycles (stress) | 🟡 LOW | ☐ ☐ ☐ |
| SC_12 | Property Validation | setAppProperty error handling | 🔶 MED | ☐ ☐ ☐ |
| SC_13 | Clear Data States | clearAppData while running vs closed | 🔶 MED | ☐ ☐ ☐ |

**Minimum Viable:** SC_09, SC_10 (2 tests)

---

### Group D: Data Integrity (2 tests)

| ID | Test Name | Description | Priority | Include? |
|---|---|---|---|---|
| SC_14 | App List Consistency | Installed/Loaded app set invariants | ✓ HIGH | ☐ ☐ ☐ |
| SC_15 | Metadata Consistency | Metadata unchanged, only state changes | ✓ HIGH | ☐ ☐ ☐ |

**Minimum Viable:** SC_14, SC_15 (2 tests)

---

## PART B: Performance Tests (14 total)

### Group E: App Launch Performance (4 tests)

| ID | Test Name | Description | Priority | Include? |
|---|---|---|---|---|
| PF_01 | Launch Time Baseline | Measure launch time (baseline) | ✓ HIGH | ☐ ☐ ☐ |
| PF_02 | Preload vs Cold Start | Compare preload benefit | ✓ HIGH | ☐ ☐ ☐ |
| PF_03 | Sequential Launches Impact | Degradation with 3/5/10 apps | 🔶 MED | ☐ ☐ ☐ |
| PF_04 | Stop Methods Comparison | closeApp vs terminateApp vs killApp times | 🔶 MED | ☐ ☐ ☐ |

**Minimum Viable:** PF_01, PF_02 (2 tests)

---

### Group F: Concurrent Operations (4 tests)

| ID | Test Name | Description | Priority | Include? |
|---|---|---|---|---|
| PF_05 | Concurrent Launch Parallel | Parallel launches, throughput | ✓ HIGH | ☐ ☐ ☐ |
| PF_06 | Mixed Ops Parallel | Launch + Query + Close concurrently | ✓ HIGH | ☐ ☐ ☐ |
| PF_07 | Rapid Transitions | 100 launch-close cycles (stress) | 🟡 LOW | ☐ ☐ ☐ |
| PF_08 | Query Under Load | Query performance during chaos | 🔶 MED | ☐ ☐ ☐ |

**Minimum Viable:** PF_05, PF_06 (2 tests)

---

### Group G: Resource Management (3 tests)

| ID | Test Name | Description | Priority | Include? |
|---|---|---|---|---|
| PF_09 | Memory Profile | Memory before/during/after lifecycle | ✓ HIGH | ☐ ☐ ☐ |
| PF_10 | CPU Impact | CPU profiling during operations | 🔶 MED | ☐ ☐ ☐ |
| PF_11 | Max Concurrent Apps | Find & verify resource limits | ✓ HIGH | ☐ ☐ ☐ |

**Minimum Viable:** PF_09, PF_11 (2 tests)

---

### Group H: API Response Time (3 tests)

| ID | Test Name | Description | Priority | Include? |
|---|---|---|---|---|
| PF_12 | API Response Baseline | Individual API latencies | 🔶 MED | ☐ ☐ ☐ |
| PF_13 | API Consistency | Response variance over 100s calls | 🟡 LOW | ☐ ☐ ☐ |
| PF_14 | Metadata Size Impact | Response time vs data size | 🟡 LOW | ☐ ☐ ☐ |

**Minimum Viable:** PF_12 (1 test)

---

## SUMMARY & QUICK SELECTIONS

### Quick Preset Options

**Option 1: Minimum (9 tests - 45 min)**
- SC_01, SC_02, SC_03, SC_06, SC_08, SC_09, SC_10, SC_14, SC_15
- ✓ All combination tests

**Option 2: Balanced (15 tests - 90 min)**  
- Option 1 (9 tests) PLUS
- PF_01, PF_02, PF_05, PF_06, PF_09, PF_11
- ✓ Essential workflows + performance baselines

**Option 3: Comprehensive (23 tests - 160 min)**
- Option 2 (15 tests) PLUS
- SC_04, SC_05, SC_07, SC_11, SC_12, SC_13, PF_03, PF_04
- ✓ Edge cases + detailed profiling

**Option 4: Complete (29 tests - 225 min)**
- All 15 combination + all 14 performance tests
- ✓ Maximum coverage & stress testing

---

## Your Selection

Please indicate your preference:

### Chosen Option:
```
[ ] Option 1: Minimum (9 tests)
[ ] Option 2: Balanced (15 tests)
[ ] Option 3: Comprehensive (23 tests)
[ ] Option 4: Complete (29 tests)
[ ] Custom: I'll mark individual tests below
```

### Custom Selections (if chosen):

**Combination Tests Include:** (mark with ✓)
```
Group A: [ ] SC_01 [ ] SC_02 [ ] SC_03 [ ] SC_04 [ ] SC_05
Group B: [ ] SC_06 [ ] SC_07 [ ] SC_08
Group C: [ ] SC_09 [ ] SC_10 [ ] SC_11 [ ] SC_12 [ ] SC_13
Group D: [ ] SC_14 [ ] SC_15
```

**Performance Tests Include:** (mark with ✓)
```
Group E: [ ] PF_01 [ ] PF_02 [ ] PF_03 [ ] PF_04
Group F: [ ] PF_05 [ ] PF_06 [ ] PF_07 [ ] PF_08
Group G: [ ] PF_09 [ ] PF_10 [ ] PF_11
Group H: [ ] PF_12 [ ] PF_13 [ ] PF_14
```

---

## Additional Questions

### Test Execution Preferences

1. **When to run these tests?**
   - [ ] Before every build
   - [ ] Before release (nightly)
   - [ ] Weekly
   - [ ] Manual only

2. **Should we track performance metrics over time?**
   - [ ] Yes, create performance regression database
   - [ ] No, just report current numbers
   - [ ] Only for critical APIs (PF_01, PF_02)

3. **Should we fail the build if tests regress?**
   - [ ] Performance regresses > 20%
   - [ ] Performance regresses > 10%
   - [ ] Only memory leaks or crashes
   - [ ] Never (just metrics for info)

4. **Device for testing?**
   - [ ] RPI4 (current device)
   - [ ] Multiple devices (RPI4 + Video_Accelerator)
   - [ ] Device-agnostic (run on whatever has AppManager)

5. **Any custom scenarios specific to your use case?**
   - [ ] No, proposed tests are sufficient
   - [ ] Yes, I have specific workflows:
     ```
     _________________________________
     _________________________________
     ```

---

## Next Steps

1. **Review** the three documentation files:
   - PROPOSAL_SUMMARY.md (this decision)
   - PROPOSED_TEST_CASES.md (detailed specs)
   - TEST_DECISION_MATRIX.md (priority matrix)

2. **Mark your selections** using the checklist above

3. **Provide this completed checklist back** to me

4. **I will immediately create** all selected test files

---

**Note:** This is a zero-risk decision. If you want to add/remove tests later, just say so. But let's get started with your priority set!

