# DownloadManager CURL Commands Reference

## Device Configuration
- Device IP: 192.168.29.123
- JSON-RPC Endpoint: http://127.0.0.1:9998/jsonrpc
- Default Download URL: https://tools.rdkcentral.com:8443/images/lib32-middleware-test-image-RPI4-raspberrypi4-64-rdke-feature-RDKECOREMW-584-OTA.wic.tar.gz

---

## POSITIVE TEST SCENARIOS

### 1. Get Storage Details
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.getStorageDetails"}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** quotaKb and usedKb values

---

### 2. Start Download (Default)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.DownloadManager.download", "params": {"url": "https://tools.rdkcentral.com:8443/images/lib32-middleware-test-image-RPI4-raspberrypi4-64-rdke-feature-RDKECOREMW-584-OTA.wic.tar.gz", "options": {"priority": true, "retries": 2, "rateLimit": 0}}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** downloadId (e.g., "2002")

---

### 3. Query Download Progress
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.progress", "params": {"downloadId": "2002"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** percent (0-100)

---

### 4. Set Rate Limit (1 MB/s)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 4, "method": "org.rdk.DownloadManager.rateLimit", "params": {"downloadId": "2002", "limit": 1048576}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** null (success)

---

### 5. Pause Download
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 5, "method": "org.rdk.DownloadManager.pause", "params": {"downloadId": "2002"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** null (success)

---

### 6. Resume Download
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 6, "method": "org.rdk.DownloadManager.resume", "params": {"downloadId": "2002"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** null (success)

---

### 7. Cancel Download
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 7, "method": "org.rdk.DownloadManager.cancel", "params": {"downloadId": "2002"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** null (success)

---

## NEGATIVE TEST SCENARIOS (Error Handling - Expected to Return Errors)

### 8. Download from Invalid URL
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 8, "method": "org.rdk.DownloadManager.download", "params": {"url": "http://invalid.nonexistent.url.host/file.tar.gz", "options": {"priority": false, "retries": 0, "rateLimit": 0}}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** error (invalid URL handling)

---

### 9. Query Progress with Invalid Download ID
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.DownloadManager.progress", "params": {"downloadId": "invalid.nonexistent.id.12345"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR_UNKNOWN_KEY error

---

### 10. Pause Non-Existent Download
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 10, "method": "org.rdk.DownloadManager.pause", "params": {"downloadId": "fake.download.id.xyz"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR error

---

### 11. Resume Non-Existent Download
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 11, "method": "org.rdk.DownloadManager.resume", "params": {"downloadId": "unknown.download.12345"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR error

---

### 12. Cancel Non-Existent Download
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 12, "method": "org.rdk.DownloadManager.cancel", "params": {"downloadId": "phantom.id.notfound"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR error

---

### 13. Set Rate Limit on Non-Existent Download
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 13, "method": "org.rdk.DownloadManager.rateLimit", "params": {"downloadId": "missing.download.id", "limit": 512000}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR error

---

### 14. Delete Non-Existent File
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 14, "method": "org.rdk.DownloadManager.delete", "params": {"fileLocator": "/nonexistent/invalid/path/file.tar.gz"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR_GENERAL error

---

## AppManager CURL Commands

### Get Installed Apps
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.1.getInstalledApps"}' http://127.0.0.1:9998/jsonrpc
```

### Launch App (Positive)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "com.rdk.app.cobalt25_rpi4"}}' http://127.0.0.1:9998/jsonrpc
```

### Launch App (Negative - Invalid App ID)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "invalid.nonexistent.app12345"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR_UNKNOWN_KEY error

### Check if App Installed (Positive)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 4, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "com.rdk.app.cobalt25_rpi4"}}' http://127.0.0.1:9998/jsonrpc
```

### Check if App Installed (Negative - Non-Existent App)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 5, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "nonexistent.invalid.app"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR_UNKNOWN_KEY error

### Close App (Positive)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 6, "method": "org.rdk.AppManager.1.closeApp", "params": {"appId": "com.rdk.app.cobalt25_rpi4"}}' http://127.0.0.1:9998/jsonrpc
```

### Close App (Negative - Non-Existent App)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 7, "method": "org.rdk.AppManager.1.closeApp", "params": {"appId": "phantom.nonexistent.app"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR error

### Get App Metadata (Positive)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 8, "method": "org.rdk.AppManager.1.getAppMetadata", "params": {"appId": "com.rdk.app.cobalt25_rpi4"}}' http://127.0.0.1:9998/jsonrpc
```

### Get App Metadata (Negative)
```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.getAppMetadata", "params": {"appId": "fake.app.invalid"}}' http://127.0.0.1:9998/jsonrpc
```
**Expected Response:** ERROR error

---

## Error Codes Reference

- **ERROR_UNKNOWN_KEY**: Key not found / Resource doesn't exist (error code 22)
- **ERROR_GENERAL**: General error / Operation failed (error code 1)
- **ERROR**: Generic error response from plugin

---

## Notes for Testing

1. **Negative tests should expect errors** - if no error is returned, the test actually FAILED
2. **Download URLs** can be from any accessible HTTP/HTTPS source
3. **Download IDs** are assigned by the plugin (e.g., "2002", "2003", etc.)
4. **Rate Limit** is in bytes per second (1048576 = 1 MB/s, 512000 = ~500 KB/s)
5. **File Locator** for delete operation should be the full path returned from download operation or manually known location
