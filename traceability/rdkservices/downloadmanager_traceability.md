# RDK Services — DownloadManager Plugin Traceability

> **Module:** DownloadManager (`org.rdk.DownloadManager.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Total requirements:** 7 | **Total test cases:** 23
> **Source:** [RDKV_CERT_AVS_DownloadManager.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/rdkservices/
├── downloadmanager_requirements.md
├── downloadmanager_traceability.md
└── testcases/
    ├── RDKSVC-REQ-001/   (4 tests  — Download initiation)
    ├── RDKSVC-REQ-002/   (1 test  — Storage information)
    ├── RDKSVC-REQ-003/   (4 tests  — Download pause and resume)
    ├── RDKSVC-REQ-004/   (3 tests  — Download cancellation)
    ├── RDKSVC-REQ-005/   (3 tests  — Downloaded file deletion)
    ├── RDKSVC-REQ-006/   (2 tests  — Download progress tracking)
    ├── RDKSVC-REQ-007/   (6 tests  — Combined download lifecycle sequences)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `RDKSVC-REQ-001` | 4 | [DownloadManager_Download_ValidParameters](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_validparameters) [DownloadManager_Download_Empty_URL](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_empty_url) [DownloadManager_Download_Invalid_URL](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_invalid_url) [DownloadManager_Download_Optional_Parameters](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_optional_parameters) |
| `RDKSVC-REQ-002` | 1 | [DownloadManager_GetStorageDetails_Functionality](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_getstoragedetails_functionality) |
| `RDKSVC-REQ-003` | 4 | [DownloadManager_Pause_Empty_Parameter](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_pause_empty_parameter) [DownloadManager_Pause_Invalid_Parameter](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_pause_invalid_parameter) [DownloadManager_Resume_Empty_Parameter](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_resume_empty_parameter) [DownloadManager_Resume_Invalid_Parameter](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_resume_invalid_parameter) |
| `RDKSVC-REQ-004` | 3 | [DownloadManager_Cancel_EmptyParameters](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_cancel_emptyparameters) [DownloadManager_Cancel_Package_Empty_Parameter](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_cancel_package_empty_parameter) [DownloadManager_Cancel_Package_Invalid_Parameter](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_cancel_package_invalid_parameter) |
| `RDKSVC-REQ-005` | 3 | [DownloadManager_Delete_EmptyFileLocator](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_delete_emptyfilelocator) [DownloadManager_Delete_InvalidFileLocator](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_delete_invalidfilelocator) [DownloadManager_Delete_Package_TwoTimes](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_delete_package_twotimes) |
| `RDKSVC-REQ-006` | 2 | [DownloadManager_Progress_Empty_Parameter](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_progress_empty_parameter) [DownloadManager_Progress_Invalid_Parameter](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_progress_invalid_parameter) |
| `RDKSVC-REQ-007` | 6 | [DownloadManager_Download_Pause_Resume_Delete_Package](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_pause_resume_delete_package) [DownloadManager_Download_Pause_Cancel_Package](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_pause_cancel_package) [DownloadManager_Download_Multiple_Pause_Resume_Operations](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_multiple_pause_resume_operations) [DownloadManager_Download_Cancel_Package](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_cancel_package) [DownloadManager_Download_Pause_Delete_Resume_Delete_Package](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_pause_delete_resume_delete_package) [DownloadManager_Download_Ratelimit_Pause_Resume_Delete_Package](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md#downloadmanager_download_ratelimit_pause_resume_delete_package) |
