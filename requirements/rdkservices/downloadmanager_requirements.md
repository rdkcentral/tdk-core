# RDK Services — DownloadManager Plugin Requirements

> **Module:** DownloadManager (`org.rdk.DownloadManager.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_DownloadManager.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_DownloadManager.md)
> **Total requirements:** 7 | **Total test cases:** 23

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | API Category | Classification | # Tests | Test Cases |
|--------|-------------|----------------|---------|------------|
| RDKSVC-REQ-001 | Download initiation — download | Download API | 4 | DownloadManager_Download_ValidParameters, DownloadManager_Download_Empty_URL, DownloadManager_Download_Invalid_URL, DownloadManager_Download_Optional_Parameters |
| RDKSVC-REQ-002 | Storage information — getStorageDetails | Query API | 1 | DownloadManager_GetStorageDetails_Functionality |
| RDKSVC-REQ-003 | Download pause and resume — pause, resume | Download Control API | 4 | DownloadManager_Pause_Empty_Parameter, DownloadManager_Pause_Invalid_Parameter, DownloadManager_Resume_Empty_Parameter, DownloadManager_Resume_Invalid_Parameter |
| RDKSVC-REQ-004 | Download cancellation — cancel | Download Control API | 3 | DownloadManager_Cancel_EmptyParameters, DownloadManager_Cancel_Package_Empty_Parameter, DownloadManager_Cancel_Package_Invalid_Parameter |
| RDKSVC-REQ-005 | Downloaded file deletion — delete | File Management API | 3 | DownloadManager_Delete_EmptyFileLocator, DownloadManager_Delete_InvalidFileLocator, DownloadManager_Delete_Package_TwoTimes |
| RDKSVC-REQ-006 | Download progress tracking — progress | Query API | 2 | DownloadManager_Progress_Empty_Parameter, DownloadManager_Progress_Invalid_Parameter |
| RDKSVC-REQ-007 | Combined download lifecycle sequences — pause, resume, cancel, delete, rate-limit | Lifecycle API | 6 | DownloadManager_Download_Pause_Resume_Delete_Package, DownloadManager_Download_Pause_Cancel_Package, DownloadManager_Download_Multiple_Pause_Resume_Operations, DownloadManager_Download_Cancel_Package, DownloadManager_Download_Pause_Delete_Resume_Delete_Package, DownloadManager_Download_Ratelimit_Pause_Resume_Delete_Package |
| | **Total** | | **23** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL implement the DownloadManager `download` JSON-RPC method to initiate a file download with a valid URL, support optional download parameters, and return correct error codes for empty URL and invalid URL inputs. |
| `RDKSVC-REQ-002` | SHALL implement the DownloadManager `getStorageDetails` JSON-RPC method to return current storage availability and usage details with correct response schema. |
| `RDKSVC-REQ-003` | SHALL implement the DownloadManager `pause` and `resume` JSON-RPC methods and return correct error codes for pause and resume requests submitted with empty and invalid download ID parameters. |
| `RDKSVC-REQ-004` | SHALL implement the DownloadManager `cancel` JSON-RPC method and return correct error codes for cancel requests submitted with empty parameters, empty download ID, and invalid download ID inputs. |
| `RDKSVC-REQ-005` | SHALL implement the DownloadManager `delete` JSON-RPC method and return correct error codes for delete requests with empty and invalid file locator inputs, and correctly handle a second delete request for an already-deleted package. |
| `RDKSVC-REQ-006` | SHALL implement the DownloadManager `progress` JSON-RPC method and return correct error codes for progress queries submitted with empty and invalid download ID parameters. |
| `RDKSVC-REQ-007` | SHALL execute combined download lifecycle operation sequences — including pause-resume-delete, pause-cancel, multiple pause-resume cycles, direct cancel, pause-delete-resume-delete, and rate-limited pause-resume-delete — without state error or data corruption. |
