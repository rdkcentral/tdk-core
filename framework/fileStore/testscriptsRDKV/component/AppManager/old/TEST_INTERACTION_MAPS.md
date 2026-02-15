# AppManager Test Cases - Visual Method Interaction Map

## Combination Tests: API Method Dependencies

### SC_01: Launch → Check State → Close

```
┌──────────────┐
│  launchApp   │───────┐
└──────────────┘       │
                       ▼
               ┌──────────────────────┐
               │ getLoadedApps        │ ◄─── Validates state after launch
               └──────────────────────┘
                       │
                       ▼
               ┌──────────────────────┐
               │ closeApp             │ ◄─── Graceful shutdown
               └──────────────────────┘

WORKFLOW: Start → Verify Running → Stop Gracefully
VALUE: Core functionality, state consistency
```

---

### SC_02: Launch → Metadata → Properties → Terminate

```
┌──────────────┐
│  launchApp   │
└──────────────┘
       │
       ▼
┌──────────────────────┐
│ getAppMetadata       │ ◄─── What is this app?
└──────────────────────┘
       │
       ▼
┌──────────────────────┐
│ getAppProperty       │ ◄─── State during execution
└──────────────────────┘
       │
       ▼
┌──────────────────────┐
│ terminateApp         │ ◄─── Force stop
└──────────────────────┘

WORKFLOW: Launch → Introspect → Verify State → Force Stop
VALUE: App metadata validity, property consistency
```

---

### SC_03: Preload → Launch → Kill

```
┌──────────────┐
│ preloadApp   │ ◄─── Pre-cache into memory
└──────────────┘
       │
       ▼
┌──────────────┐
│  launchApp   │ ◄─── Should be faster
└──────────────┘
       │
       ▼
┌──────────────────────┐
│ getLoadedApps        │ ◄─── Verify presence
└──────────────────────┘
       │
       ▼
┌──────────────┐
│   killApp    │ ◄─── Immediate termination
└──────────────┘

WORKFLOW: Optimize Launch → Verify → Immediate Kill
VALUE: Preload benefit measurement, fast termination
PERFORMANCE: Baseline vs. Preload
```

---

### SC_06: Start System App → Send Intent → Stop

```
┌──────────────┐
│startSystemApp│
└──────────────┘
       │
       ▼
┌──────────────────────┐
│   sendIntent         │ ◄─── Inter-process communication
└──────────────────────┘
       │
       ▼
┌──────────────────────┐
│ getLoadedApps        │ ◄─── Verify still running
└──────────────────────┘
       │
       ▼
┌──────────────┐
│stopSystemApp │ ◄─── Clean shutdown
└──────────────┘

WORKFLOW: System App Lifecycle with IPC
VALUE: Intent delivery works, app responsive to intents
```

---

### SC_08: Multiple System Apps Concurrent

```
┌──────────────┐
│startSystemApp│ ◄─── App 1
│  (App 1)     │
└──────────────┘
       │
       ├─────────┐
       │         ▼
       │   ┌──────────────┐
       │   │startSystemApp│ ◄─── App 2 (parallel)
       │   │  (App 2)     │
       │   └──────────────┘
       │         │
       └─────┬───┴──────┐
             │          ▼
             │   ┌──────────────────────┐
             │   │ getLoadedApps        │ ◄─── Both registered
             │   └──────────────────────┘
             │          │
             ▼          ▼
      ┌──────────────────────────────┐
      │ getMaxRunningApps vs actual   │ ◄─── Resource check
      └──────────────────────────────┘
             │
             ├─────┬─────┐
             ▼     ▼     ▼
      Stop App1, Check, Stop App2

WORKFLOW: Concurrent System App Management
VALUE: Resource limits, scalability, consistency
PERFORMANCE: CPU/memory under load
```

---

### SC_09: Error Recovery

```
┌──────────────┐
│  launchApp   │ X ERROR (invalid app)
│  (INVALID)   │
└──────────────┘
       │
       ▼ (system should recover)
┌──────────────┐
│  launchApp   │ ✓ SUCCESS (valid app)
│   (VALID)    │
└──────────────┘
       │
       ▼
┌──────────────────────┐
│ closeApp             │ ✓ Works fine
└──────────────────────┘

WORKFLOW: Error → Recovery → Normal Operation
VALUE: Error doesn't corrupt system state
```

---

### SC_10: State Validation

```
┌──────────────┐
│   closeApp   │ X ERROR (app not running)
│  (INVALID)   │
└──────────────┘
       │
       ▼ (system validates state)
┌──────────────┐
│  launchApp   │ ✓ SUCCESS
└──────────────┘
       │
       ▼
┌──────────────┐
│   closeApp   │ ✓ SUCCESS (app running)
│   (VALID)    │
└──────────────┘

WORKFLOW: Invalid Operation → Valid State → Correct Operation
VALUE: API validates preconditions before action
```

---

### SC_14: App List Consistency

```
┌─────────────────────────────┐
│ getInstalledApps            │ ◄─── Full app inventory
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│ launchApp (one of them)      │ ◄─── Launch installed app
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│ getLoadedApps               │ ◄─── Should include launched app
└─────────────────────────────┘
        │
        ├─── Verify: App in getLoadedApps ⊆ getInstalledApps
        │
        ▼
┌─────────────────────────────┐
│ closeApp                    │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│ getLoadedApps (after close) │ ◄─── App should be removed
└─────────────────────────────┘

INVARIANTS VERIFIED:
✓ Loaded ⊆ Installed (every running app is installed)
✓ Launch adds to Loaded
✓ Close removes from Loaded
✓ Loaded ≤ MaxRunningApps always
```

---

### SC_15: Metadata Consistency

```
              TIME SEQUENCE
        │
┌───────┴─────────────────────────┐
│(1) Before Launch                │
├─────────────────────────────────┤
│ getAppMetadata                  │ ◄─── Metadata (static)
│ {name, version, icon, ...}      │
└─────────────────────────────────┘
                │
                ▼
        ┌─────────────────────────────────┐
        │(2) Launch & Running             │
        ├─────────────────────────────────┤
        │ launchApp                       │
        │ getAppMetadata                  │ ◄─── Same metadata
        │ {same name, version, icon, ...} │
        │                                 │
        │ getAppProperty("state")         │ ◄─── CHANGED (running)
        │ {state: "running"}              │
        └─────────────────────────────────┘
                │
                ▼
        ┌─────────────────────────────────┐
        │(3) After Close                  │
        ├─────────────────────────────────┤
        │ closeApp                        │
        │ getAppMetadata                  │ ◄─── Same metadata
        │ {same name, version, icon, ...} │
        │                                 │
        │ getAppProperty("state")         │ ◄─── CHANGED (closed)
        │ {state: "closed"}               │
        └─────────────────────────────────┘

INVARIANTS:
✓ Metadata never changes (name, version, icon immutable)
✓ Only state property changes with lifecycle
✓ Metadata from (1) = Metadata from (2) = Metadata from (3)
```

---

## Performance Tests: Metric Relationships

### PF_01: Launch Time Baseline → Comparison Reference

```
BASELINE MEASUREMENT:
Launch Time = T₁
App not loaded → API call → App loaded (in getLoadedApps)

Used as reference for:
├─ PF_02: Preload vs Cold (compare: T_preloaded vs T_cold)
├─ PF_03: Sequential impact (compare: T₁ vs T₂ vs T₃...)
├─ PF_04: Method differences (compare closeApp vs killApp time)
└─ PF_05: Concurrent impact (compare: parallel vs sequential)
```

---

### PF_02: Preload Performance

```
                    PRELOAD BENEFIT
        │
        ├──┬─ Without Preload ─┬──┐
        │  │                   │  │
    T₀  │  │ ←── Launch Time───│  │ T=(baseline)
        │  │                   │  │
        │  └───────────────────┘  │
        │                         │
        │  ┌───── Preload ──┐     │
        │  │ T=preload_time │     │
        │  └────────────────┘     │
        │       ↓ (app cached)    │
        │  ┌───── Launch ──┐      │
        │  │ T=faster!     │      │ T=(reduced)
        │  └───────────────┘      │
        │                         │
        └─────────────────────────┘

METRICS:
├─ Preload overhead (T_preload)
├─ Cold launch time (T_cold)
├─ Preloaded launch time (T_warm)
├─ Benefit ratio (T_cold / T_warm) 
└─ Break-even point (when preload pays off)
```

---

### PF_05 & PF_06: Concurrent Operations Impact

```
SEQUENTIAL:           CONCURRENT (Parallel):
┌─Launch1─┐           ┌─Launch1──┐
│  10s    │           │  10s     │─┐
└────┬────┘           └──────────┘ │
     └─Launch2─┐                    │ (overlapping)
     │  10s    │                    │
     └────┬────┘      ┌─Launch2──┐ │
          └─Launch3─┐ │  10s     │─┤
          │  10s    │ └──────────┘ │
          └────┘                    │
                     ┌─Launch3──┐  │
Total: 30s           │  10s     │─┘
                     └──────────┘
                    Total: ~15s

SPEEDUP METRIC: Sequential / Concurrent = Parallelism efficiency
BOTTLENECK DETECTION: If concurrent ≈ sequential → serialized internally
```

---

### PF_09: Memory Profile Over Lifecycle

```
MEMORY USAGE (MiB)

100├──────────────────────────────────┐
   │                                  │
 90├─────────┐                        │
   │         │ ↑ Launch               │ ↓ Close
 80├─────────┤ (app loads)            │ (cleanup)
   │ Baseline│                        │
 70├─────┬───┤                ┌───────┼──
   │ 50  │70 │                │ app   │ Leaked?
 60├─────┼───┤       Running   │ ends  │
   │     │   │       ┌────────┴───────┼─
 50├─────┴───┤   100 │               │
   │         │   MiB │               │
 40├─────────┴─────┬─┴───────────────┘
   │               │
 30├───────────────┴─────────────────
   │ Baseline restored (±10%)
 20├───────────────────────────────
   │
 10├───────────────────────────────
   │
  0└───────────────────────────────
    0    5s   20s           50s

SUCCESS: Memory returns to baseline after close
FAILURE: Memory doesn't return → MEMORY LEAK
```

---

### PF_11: Resource Limits

```
RUNNING APPS VS SYSTEM LIMITS

   # Apps
    10├─────────────────┬── getMaxRunningApps
      │                 │
    8 ├──────┐          │
      │      │          │
    6 ├──┬───┤      ┌───┘ (hitting limit)
      │  │   │      │
    4 ├──┴───┴──┐   │  ┌── Error returned
      │         │   │  │   (graceful)
    2 ├─────────┴───┼──┤
      │             │  │
    0 └─────────────▼──┴──
      0    5   10  15  20 attempts

SUCCESS: 
├─ getMaxRunningApps = 6
├─ Can launch 6 apps successfully
├─ 7th launch returns error (not crash)
└─ No corruption after hitting limit
```

---

## Test Dependency Chain

```
┌─ Individual API Tests (34 existing)
│
├─ Combination Tests (15 new)
│  ├─ SC_01: Requires launchApp, getLoadedApps, closeApp ✓
│  ├─ SC_02: Requires launchApp, getAppMetadata, getAppProperty, terminateApp ✓
│  ├─ SC_03: Requires preloadApp, launchApp, getLoadedApps, killApp ✓
│  └─ ... (all others have dependencies)
│
├─ Performance Tests (14 new)
│  ├─ PF_01: Baseline (depends on none, sets baseline)
│  ├─ PF_02: Depends on PF_01 baseline
│  ├─ PF_03: Depends on PF_01 baseline
│  └─ ... (most depend on baselines)
│
└─ Shell Scripts
   ├─ run_appmanager_validation.sh (uses 34 tests)
   ├─ run_appmanager_comprehensive.sh (uses 34 tests)
   ├─ run_appmanager_scenario_tests.sh (uses 15 combo tests)
   ├─ run_appmanager_performance_tests.sh (uses 14 perf tests)
   └─ run_appmanager_full_test_suite.sh (uses all 63 tests)

EXECUTION ORDER:
1. Individual API tests (establishes functionality)
2. Combination tests (validates workflows)
3. Performance tests (measures specific baselines)
4. Performance tests again (regression detection)
```

---

## Suggested Test Prioritization

### CRITICAL PATH (must have)
1. SC_01, SC_02, SC_03 - Core workflows
2. SC_09, SC_10 - Error handling
3. SC_14 - Consistency
4. PF_01, PF_02 - Performance baselines

### IMPORTANT (should have)
1. SC_06, SC_08 - System apps
2. PF_05, PF_06 - Concurrency
3. PF_09, PF_11 - Resource limits

### NICE-TO-HAVE (good to have)
1. SC_04, SC_05, SC_07 - Edge cases
2. PF_03, PF_04, PF_07, PF_08 - Detailed analysis
3. PF_10, PF_12, PF_13, PF_14 - Profiling

---

## Total Test Suite Architecture

```
┌─────────────────────────────────────────────────────────┐
│         COMPLETE AppManager Test Suite (63 tests)       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Layer 1: Individual API Tests (34 tests)              │
│  └─ Verify each API works correctly                    │
│     Execution time: ~2 hours                            │
│                                                         │
│  Layer 2: Combination Tests (15 tests) ← NEW            │
│  └─ Verify workflow combinations work                  │
│     Execution time: ~45 minutes                         │
│                                                         │
│  Layer 3: Performance Tests (14 tests) ← NEW            │
│  └─ Measure and baseline performance                   │
│     Execution time: ~3 hours                            │
│                                                         │
│  Total Test Coverage:                                  │
│  ├─ 21 unique APIs                                     │
│  ├─ 15+ real-world workflows                           │
│  ├─ 14 performance baselines                           │
│  └─ ~225 minutes total automated testing               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

