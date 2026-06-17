## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [PersistentStore_Set_and_Get_Value (PS_01)](#persistentstore_set_and_get_value-ps_01)
   - [PersistentStore_Delete_Key (PS_02)](#persistentstore_delete_key-ps_02)
   - [PersistentStore_Delete_Namespace (PS_03)](#persistentstore_delete_namespace-ps_03)
   - [PersistentStore_Get_Storage_Size (PS_04)](#persistentstore_get_storage_size-ps_04)
   - [PersistentStore_Flush_Cache (PS_05)](#persistentstore_flush_cache-ps_05)
   - [PersistentStore_Check_On_Value_Changed_Event (PS_06)](#persistentstore_check_on_value_changed_event-ps_06)
   - [PersistentStore_Set_And_Get_Storage_Limits (PS_07)](#persistentstore_set_and_get_storage_limits-ps_07)
   - [PersistentStore_Check_Set_And_Get_Empty_Storage_Limits (PS_08)](#persistentstore_check_set_and_get_empty_storage_limits-ps_08)
   - [PersistentStore_Verify_SetValue_And_GetValue_API_with_Empty_Key_Operations (PS_09)](#persistentstore_verify_setvalue_and_getvalue_api_with_empty_key_operations-ps_09)
   - [PersistentStore_Verify_SetValue_And_GetValue_API_with_Empty_Namespce_Operations (PS_10)](#persistentstore_verify_setvalue_and_getvalue_api_with_empty_namespce_operations-ps_10)
   - [PersistentStore_GetStorage_NamespaceLimit_For_DeletedNamespace (PS_11)](#persistentstore_getstorage_namespacelimit_for_deletednamespace-ps_11)
   - [PersistentStore_ActivateDeactivate_Event_Test (PS_12)](#persistentstore_activatedeactivate_event_test-ps_12)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **PersistentStore** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.PersistentStore` (version 1)

**API Coverage**

- **State / Query APIs**: `getKeys`, `getNamespaceStorageLimit`, `getNamespaces`, `getStorageSize`, `getValue`
- **Configuration APIs**: `deleteKey`, `deleteNamespace`, `setNamespaceStorageLimit`, `setValue`
- **Events**: `onValueChanged`
- **Other APIs**: `flushCache`

### APIs Under Test

| API | Description |
|-----|-------------|
| `deleteKey` | Deletes the key for given namespace |
| `deleteNamespace` | Deletes the given Namespace |
| `flushCache` | flushes the database cache |
| `getKeys` | Gets the keys list for given namespace |
| `getNamespaceStorageLimit` | Returns the storage limit for a given namespace |
| `getNamespaces` | Gets the available namespaces |
| `getStorageSize` | Returns the size occupied by each namespace |
| `getValue` | Gets the value of the key for given namespace |
| `setNamespaceStorageLimit` | Sets the storage limit for a given namespace |
| `setValue` | Sets the value of the key for given the namespace |

### Events Under Test

| Event | Description |
|-------|-------------|
| `onValueChanged` | Triggered whenever any of the values stored are changed using setValue |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.PersistentStore"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_On_Value_Changed` on `PersistentStore` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

---

## Test Cases

<a id="persistentstore_set_and_get_value-ps_01"></a>
### PersistentStore_Set_and_Get_Value (PS_01)

**Objective:** Sets and gets the particular key value

**Test Steps:**

> **Value Loop (Steps 1–2):** Steps 1–2 repeat **3 times**, once for each value of `value`: `Value_1`, `Value_2`, `Value_3`

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke `setValue` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_1"`, `key`: `"Key_1"`, `value`: each of `Value_1`, `Value_2`, `Value_3`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_1", "key": "Key_1", "value": "<VALUE_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Value set successfully |
| 2 | Get Value | Invoke `getValue` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_1"`, `key`: `"Key_1"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Namespace_1", "key": "Key_1"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` returned value matches the iterated value set in the previous step |

---

<a id="persistentstore_delete_key-ps_02"></a>
### PersistentStore_Delete_Key (PS_02)

**Objective:** Deletes the key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke `setValue` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_1"`, `key`: `"Key_2"`, `value`: `"Value_2"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_1", "key": "Key_2", "value": "Value_2"}}' http://127.0.0.1:9998/jsonrpc` | Value set successfully |
| 2 | Get Keys | Invoke `getKeys` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_1"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Namespace_1"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, `Key_2` present in the returned keys list |
| 3 | Delete Key | Invoke `deleteKey` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_1"`, `key`: `"Key_2"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteKey", "params": {"namespace": "Namespace_1", "key": "Key_2"}}' http://127.0.0.1:9998/jsonrpc` | Key deleted successfully |
| 4 | Get Keys | Invoke `getKeys` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_1"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Namespace_1"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, `Key_2` absent from the returned keys list |

---

<a id="persistentstore_delete_namespace-ps_03"></a>
### PersistentStore_Delete_Namespace (PS_03)

**Objective:** Deletes the Namespace

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke `setValue` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_2"`, `key`: `"Key_1"`, `value`: `"Value_1"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_2", "key": "Key_1", "value": "Value_1"}}' http://127.0.0.1:9998/jsonrpc` | Value set successfully |
| 2 | Get Namespaces | Invoke `getNamespaces` on `org.rdk.PersistentStore`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Expected `Namespace_2` |
| 3 | Delete Namespace | Invoke `deleteNamespace` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_2"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "Namespace_2"}}' http://127.0.0.1:9998/jsonrpc` | Namespace deleted successfully  |
| 4 | Get Namespaces | Invoke `getNamespaces` on `org.rdk.PersistentStore`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Expected `Namespace_2` absent from the namespaces list |

---

<a id="persistentstore_get_storage_size-ps_04"></a>
### PersistentStore_Get_Storage_Size (PS_04)

**Objective:** Gets the storage size of the available namespaces 

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Namespaces | Invoke `getNamespaces` on `org.rdk.PersistentStore`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Namespaces returned successfully |
| 2 | Get Storage Size | Invoke `getStorageSize` on `org.rdk.PersistentStore`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getStorageSize"}' http://127.0.0.1:9998/jsonrpc` | Storage Size returned successfully |

---

<a id="persistentstore_flush_cache-ps_05"></a>
### PersistentStore_Flush_Cache (PS_05)

**Objective:** flushes the database cache

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Flush Cache | Invoke `flushCache` on `org.rdk.PersistentStore`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.flushCache"}' http://127.0.0.1:9998/jsonrpc` | Cache cleared successfully |

---

<a id="persistentstore_check_on_value_changed_event-ps_06"></a>
### PersistentStore_Check_On_Value_Changed_Event (PS_06)

**Objective:** Sets and gets the particular key value

**Test Steps:**

> **Value Loop (Steps 1–3):** Steps 1–3 repeat **3 times**, once for each value of `value`: `Value_1`, `Value_2`, `Value_3`

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke `setValue` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_3"`, `key`: `"Key_1"`, `value`: each of `Value_1`, `Value_2`, `Value_3`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_3", "key": "Key_1", "value": "<VALUE_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Value set successfully |
| 2 | Get Value | Invoke `getValue` on `org.rdk.PersistentStore` with `namespace`: `"Namespace_3"`, `key`: `"Key_1"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Namespace_3", "key": "Key_1"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` returned value matches the iterated value set in the previous step |
| 3 | Check On Value Changed Event | Listen for `Event_On_Value_Changed` event (wait 2s) | `success`: `true` returned value matches the iterated value set in the previous step |

---

<a id="persistentstore_set_and_get_storage_limits-ps_07"></a>
### PersistentStore_Set_And_Get_Storage_Limits (PS_07)

**Objective:** Set and get storage limits for available namespaces 

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Namespaces | Invoke `getNamespaces` on `org.rdk.PersistentStore`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Namespaces returned successfully |
| 2 | Delete Namespace | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deleteNamespace` on `org.rdk.PersistentStore` with `namespace`: `"username"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Namespace deleted successfully |
| 3 | Set Namespace Storagelimit | Invoke `setNamespaceStorageLimit` on `org.rdk.PersistentStore` with `namespace`: `"username"`, `storageLimit`: `20`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "username", "storageLimit": 20}}' http://127.0.0.1:9998/jsonrpc` | Namespace Storage Limit set successfully |
| 4 | Get Namespace Storagelimit | Invoke `getNamespaceStorageLimit` on `org.rdk.PersistentStore` with `namespace`: `"username"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Expected `20` |
| 5 | Delete Namespace | Invoke `deleteNamespace` on `org.rdk.PersistentStore` with `namespace`: `"username"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Namespace deleted successfully |

---

<a id="persistentstore_check_set_and_get_empty_storage_limits-ps_08"></a>
### PersistentStore_Check_Set_And_Get_Empty_Storage_Limits (PS_08)

**Objective:** Verify persistent store handles empty, sets and retrieves storage namespace limits

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Namespace Storagelimit | Invoke `setNamespaceStorageLimit` on `org.rdk.PersistentStore` with `namespace`: `""`, `storageLimit`: `20`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "", "storageLimit": 20}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |
| 2 | Get Namespace Storagelimit | Invoke `getNamespaceStorageLimit` on `org.rdk.PersistentStore` with `namespace`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_verify_setvalue_and_getvalue_api_with_empty_key_operations-ps_09"></a>
### PersistentStore_Verify_SetValue_And_GetValue_API_with_Empty_Key_Operations (PS_09)

**Objective:** Verify persistent store handles empty key, set and get operatins across namespaces

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke `setValue` on `org.rdk.PersistentStore` with `namespace`: `"username"`, `key`: `""`, `value`: `"user"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "username", "key": "", "value": "user"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |
| 2 | Get Value | Invoke `getValue` on `org.rdk.PersistentStore` with `namespace`: `"username"`, `key`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "username", "key": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_UNKNOWN_KEY` |

---

<a id="persistentstore_verify_setvalue_and_getvalue_api_with_empty_namespce_operations-ps_10"></a>
### PersistentStore_Verify_SetValue_And_GetValue_API_with_Empty_Namespce_Operations (PS_10)

**Objective:** Verify persistent store handles empty namespace, set and get operatins

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke `setValue` on `org.rdk.PersistentStore` with `namespace`: `""`, `key`: `"username"`, `value`: `"user"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "", "key": "username", "value": "user"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |
| 2 | Get Value | Invoke `getValue` on `org.rdk.PersistentStore` with `namespace`: `""`, `key`: `"username"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "", "key": "username"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getstorage_namespacelimit_for_deletednamespace-ps_11"></a>
### PersistentStore_GetStorage_NamespaceLimit_For_DeletedNamespace (PS_11)

**Objective:** Verify that attempting to retrieve the storage namespace limit for a namespace that has already been deleted results in an appropriate error or indication, such as a null response or a specific error message

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Namespaces | Invoke `getNamespaces` on `org.rdk.PersistentStore`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Namespaces returned successfully |
| 2 | Delete Namespace | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deleteNamespace` on `org.rdk.PersistentStore` with `namespace`: `"username"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Namespace deleted successfully |
| 3 | Get Namespace Storagelimit | Invoke `getNamespaceStorageLimit` on `org.rdk.PersistentStore` with `namespace`: `"username"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_activatedeactivate_event_test-ps_12"></a>
### PersistentStore_ActivateDeactivate_Event_Test (PS_12)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.PersistentStore"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate PersistentStore Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.PersistentStore"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `org.rdk.persistentstore`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate org.rdk.PersistentStore Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.PersistentStore"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `org.rdk.persistentstore`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M88 |