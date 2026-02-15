# AppManager Test Cases - Quick Reference

## Summary
- **Total Tests**: 34
- **Total APIs**: 21
- **Categories**: 9
- **Positive Tests**: 16 | **Negative Tests**: 12 | **Query/Property**: 6

## Test Categories at a Glance

| # | Category | Tests | APIs | Files |
|---|----------|-------|------|-------|
| 1 | Activation | 1 | activate | 01 |
| 2 | App Control | 10 | launchApp, preloadApp, closeApp, terminateApp, killApp | 02-11 |
| 3 | App Query | 4 | isInstalled, getInstalledApps, getLoadedApps | 12-15 |
| 4 | Communication | 2 | sendIntent | 16-17 |
| 5 | System Apps | 4 | startSystemApp, stopSystemApp | 18-21 |
| 6 | Data Mgmt | 3 | clearAppData, clearAllAppData | 22-24 |
| 7 | Metadata | 2 | getAppMetadata | 25-26 |
| 8 | Properties | 4 | getAppProperty, setAppProperty | 27-30 |
| 9 | Resources | 4 | getMaxRunningApps, getMaxHibernatedApps, getMaxHibernatedFlashUsage, getMaxInactiveRamUsage | 31-34 |

## All 34 Tests

### Activation (1)
- **01** - TC_AppManager_activate - RDKV_AppManager_01_Activate.py

### App Control (10)
- **02** - TC_AppManager_launchApp (Pos) - RDKV_AppManager_02_LaunchApp_Positive.py
- **03** - TC_AppManager_launchApp (Neg) - RDKV_AppManager_03_LaunchApp_Negative.py
- **04** - TC_AppManager_preloadApp (Pos) - RDKV_AppManager_04_PreloadApp_Positive.py
- **05** - TC_AppManager_preloadApp (Neg) - RDKV_AppManager_05_PreloadApp_Negative.py
- **06** - TC_AppManager_closeApp (Pos) - RDKV_AppManager_06_CloseApp_Positive.py
- **07** - TC_AppManager_closeApp (Neg) - RDKV_AppManager_07_CloseApp_Negative.py
- **08** - TC_AppManager_terminateApp (Pos) - RDKV_AppManager_08_TerminateApp_Positive.py
- **09** - TC_AppManager_terminateApp (Neg) - RDKV_AppManager_09_TerminateApp_Negative.py
- **10** - TC_AppManager_killApp (Pos) - RDKV_AppManager_10_KillApp_Positive.py
- **11** - TC_AppManager_killApp (Neg) - RDKV_AppManager_11_KillApp_Negative.py

### App Query (4)
- **12** - TC_AppManager_isInstalled (Pos) - RDKV_AppManager_12_IsInstalled_Positive.py
- **13** - TC_AppManager_isInstalled (Neg) - RDKV_AppManager_13_IsInstalled_Negative.py
- **14** - TC_AppManager_getInstalledApps (Query) - RDKV_AppManager_14_GetInstalledApps.py
- **15** - TC_AppManager_getLoadedApps (Query) - RDKV_AppManager_15_GetLoadedApps.py

### Communication (2)
- **16** - TC_AppManager_sendIntent (Pos) - RDKV_AppManager_16_SendIntent_Positive.py
- **17** - TC_AppManager_sendIntent (Neg) - RDKV_AppManager_17_SendIntent_Negative.py

### System Apps (4)
- **18** - TC_AppManager_startSystemApp (Pos) - RDKV_AppManager_18_StartSystemApp_Positive.py
- **19** - TC_AppManager_startSystemApp (Neg) - RDKV_AppManager_19_StartSystemApp_Negative.py
- **20** - TC_AppManager_stopSystemApp (Pos) - RDKV_AppManager_20_StopSystemApp_Positive.py
- **21** - TC_AppManager_stopSystemApp (Neg) - RDKV_AppManager_21_StopSystemApp_Negative.py

### Data Management (3)
- **22** - TC_AppManager_clearAppData (Pos) - RDKV_AppManager_22_ClearAppData_Positive.py
- **23** - TC_AppManager_clearAppData (Neg) - RDKV_AppManager_23_ClearAppData_Negative.py
- **24** - TC_AppManager_clearAllAppData (Query) - RDKV_AppManager_24_ClearAllAppData.py

### Metadata (2)
- **25** - TC_AppManager_getAppMetadata (Pos) - RDKV_AppManager_25_GetAppMetadata_Positive.py
- **26** - TC_AppManager_getAppMetadata (Neg) - RDKV_AppManager_26_GetAppMetadata_Negative.py

### Properties (4)
- **27** - TC_AppManager_getAppProperty (Pos) - RDKV_AppManager_27_GetAppProperty_Positive.py
- **28** - TC_AppManager_getAppProperty (Neg) - RDKV_AppManager_28_GetAppProperty_Negative.py
- **29** - TC_AppManager_setAppProperty (Pos) - RDKV_AppManager_29_SetAppProperty_Positive.py
- **30** - TC_AppManager_setAppProperty (Neg) - RDKV_AppManager_30_SetAppProperty_Negative.py

### Resources (4)
- **31** - TC_AppManager_getMaxRunningApps (Prop) - RDKV_AppManager_31_GetMaxRunningApps.py
- **32** - TC_AppManager_getMaxHibernatedApps (Prop) - RDKV_AppManager_32_GetMaxHibernatedApps.py
- **33** - TC_AppManager_getMaxHibernatedFlashUsage (Prop) - RDKV_AppManager_33_GetMaxHibernatedFlashUsage.py
- **34** - TC_AppManager_getMaxInactiveRamUsage (Prop) - RDKV_AppManager_34_GetMaxInactiveRamUsage.py

## API Methods (21)
1. `activate` - TC_AppManager_activate
2. `launchApp` - TC_AppManager_launchApp (2 tests)
3. `preloadApp` - TC_AppManager_preloadApp (2 tests)
4. `closeApp` - TC_AppManager_closeApp (2 tests)
5. `terminateApp` - TC_AppManager_terminateApp (2 tests)
6. `killApp` - TC_AppManager_killApp (2 tests)
7. `isInstalled` - TC_AppManager_isInstalled (2 tests)
8. `getInstalledApps` - TC_AppManager_getInstalledApps
9. `getLoadedApps` - TC_AppManager_getLoadedApps
10. `sendIntent` - TC_AppManager_sendIntent (2 tests)
11. `startSystemApp` - TC_AppManager_startSystemApp (2 tests)
12. `stopSystemApp` - TC_AppManager_stopSystemApp (2 tests)
13. `clearAppData` - TC_AppManager_clearAppData (2 tests)
14. `clearAllAppData` - TC_AppManager_clearAllAppData
15. `getAppMetadata` - TC_AppManager_getAppMetadata (2 tests)
16. `getAppProperty` - TC_AppManager_getAppProperty (2 tests)
17. `setAppProperty` - TC_AppManager_setAppProperty (2 tests)
18. `getMaxRunningApps` - TC_AppManager_getMaxRunningApps
19. `getMaxHibernatedApps` - TC_AppManager_getMaxHibernatedApps
20. `getMaxHibernatedFlashUsage` - TC_AppManager_getMaxHibernatedFlashUsage
21. `getMaxInactiveRamUsage` - TC_AppManager_getMaxInactiveRamUsage

## Run Commands

```bash
# All tests
./run_appmanager_tests.sh all

# Category-specific
./run_appmanager_tests.sh category activation
./run_appmanager_tests.sh category control
./run_appmanager_tests.sh category query
./run_appmanager_tests.sh category communication
./run_appmanager_tests.sh category system
./run_appmanager_tests.sh category data
./run_appmanager_tests.sh category metadata
./run_appmanager_tests.sh category property
./run_appmanager_tests.sh category resources

# Show help
./run_appmanager_tests.sh help

# Show coverage
./run_appmanager_tests.sh coverage
```

## Files in This Directory

- `RDKV_AppManager_01_Activate.py` through `RDKV_AppManager_34_GetMaxInactiveRamUsage.py` (34 test files)
- `TEST_CASES_SUMMARY.md` - Detailed documentation
- `test_cases.csv` - CSV format test list
- `test_cases.json` - JSON format test data
- `run_appmanager_tests.sh` - Test execution script
- `README.md` - Complete guide
- `QUICK_REFERENCE.md` - This file

## Key Info

- **Interface**: org.rdk.AppManager.1
- **Stub**: librdkservicesstub.so
- **Platform**: RDKV (RPI-Client, Video_Accelerator)
- **RDK Version**: RDK2.0
- **Release**: M128
- **Execution Time**: ~60 seconds per test

## Prerequisites

1. TDK Agent running
2. AppManager plugin activated
3. Required apps installed
4. Compatible device

## Test Type Codes

- **(Pos)** = Positive test (valid inputs)
- **(Neg)** = Negative test (error handling)
- **(Query)** = Query/information retrieval
- **(Prop)** = Property query
- **(Act)** = Activation

---

For detailed information, see:
- [TEST_CASES_SUMMARY.md](TEST_CASES_SUMMARY.md) - Full descriptions
- [README.md](README.md) - Complete documentation
- [test_cases.csv](test_cases.csv) - Machine-readable list
- [test_cases.json](test_cases.json) - Structured data
