## TestScript Name
RDKV_CERT_AVS_PersistentStore

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [PersistentStore_Set_and_Get_Value](#persistentstore_set_and_get_value)
   - [PersistentStore_Delete_Key](#persistentstore_delete_key)
   - [PersistentStore_Delete_Namespace](#persistentstore_delete_namespace)
   - [PersistentStore_Get_Storage_Size](#persistentstore_get_storage_size)
   - [PersistentStore_Flush_Cache](#persistentstore_flush_cache)
   - [PersistentStore_Check_On_Value_Changed_Event](#persistentstore_check_on_value_changed_event)
   - [PersistentStore_Set_And_Get_Storage_Limits](#persistentstore_set_and_get_storage_limits)
   - [PersistentStore_Check_Set_And_Get_Empty_Storage_Limits](#persistentstore_check_set_and_get_empty_storage_limits)
   - [PersistentStore_Verify_SetValue_And_GetValue_API_with_Empty_Key_Operations](#persistentstore_verify_setvalue_and_getvalue_api_with_empty_key_operations)
   - [PersistentStore_Verify_SetValue_And_GetValue_API_with_Empty_Namespce_Operations](#persistentstore_verify_setvalue_and_getvalue_api_with_empty_namespce_operations)
   - [PersistentStore_GetStorage_NamespaceLimit_For_DeletedNamespace](#persistentstore_getstorage_namespacelimit_for_deletednamespace)
   - [PersistentStore_ActivateDeactivate_Event_Test](#persistentstore_activatedeactivate_event_test)
4. [Plugin Post-conditions](#plugin-post-conditions)
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

## APIs Under Test

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

## Events Under Test

| Event | Description |
|-------|-------------|
| `onValueChanged` | Triggered whenever any of the values stored are changed using setValue |

---

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of PersistentStore Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PersistentStore Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of PersistentStore Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_On_Value_Changed` on `PersistentStore` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

---

## Test Cases

<a id="persistentstore_set_and_get_value"></a>
### TestCase Name
PersistentStore_Set_and_Get_Value

### TestCase ID
PS_01

### TestCase Objective
Sets and gets the particular key value

### Test Steps

> **Value Loop (Steps 1–2):** Steps 1–2 repeat **3 times**, once for each value of `value`: `Value_1`, `Value_2`, `Value_3`

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke setValue on org.rdk.PersistentStore with namespace: "Namespace_1", key: "Key_1", value: "<VALUE_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_1", "key": "Key_1", "value": "<VALUE_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get Value | Invoke getValue on org.rdk.PersistentStore with namespace: "Namespace_1", key: "Key_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Namespace_1", "key": "Key_1"}}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` returned value matches the iterated value set in the previous step |

---

<a id="persistentstore_delete_key"></a>
### TestCase Name
PersistentStore_Delete_Key

### TestCase ID
PS_02

### TestCase Objective
Deletes the key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke setValue on org.rdk.PersistentStore with namespace: "Namespace_1", key: "Key_2", value: "Value_2"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_1", "key": "Key_2", "value": "Value_2"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get Keys | Invoke getKeys on org.rdk.PersistentStore with namespace: "Namespace_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Namespace_1"}}' http://127.0.0.1:9998/jsonrpc` | `success` : `true`, `Key_2` present in the returned keys list |
| 3 | Delete Key | Invoke deleteKey on org.rdk.PersistentStore with namespace: "Namespace_1", key: "Key_2"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteKey", "params": {"namespace": "Namespace_1", "key": "Key_2"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the key is deleted successfully |
| 4 | Get Keys | Invoke getKeys on org.rdk.PersistentStore with namespace: "Namespace_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Namespace_1"}}' http://127.0.0.1:9998/jsonrpc` | `success` : `true`, `Key_2` absent from the returned keys list |

---

<a id="persistentstore_delete_namespace"></a>
### TestCase Name
PersistentStore_Delete_Namespace

### TestCase ID
PS_03

### TestCase Objective
Deletes the Namespace

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke setValue on org.rdk.PersistentStore with namespace: "Namespace_2", key: "Key_1", value: "Value_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_2", "key": "Key_1", "value": "Value_1"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get Namespaces | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Expected `Namespace_2` |
| 3 | Delete Namespace | Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "Namespace_2"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "Namespace_2"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace is deleted successfully |
| 4 | Get Namespaces | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Expected `Namespace_2` absent from the namespaces list |

---

<a id="persistentstore_get_storage_size"></a>
### TestCase Name
PersistentStore_Get_Storage_Size

### TestCase ID
PS_04

### TestCase Objective
Gets the storage size of the available namespaces

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Namespaces | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that namespaces are returned successfully |
| 2 | Get Storage Size | Invoke getStorageSize on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getStorageSize"}' http://127.0.0.1:9998/jsonrpc` | Verify that the storage size is returned successfully |

---

<a id="persistentstore_flush_cache"></a>
### TestCase Name
PersistentStore_Flush_Cache

### TestCase ID
PS_05

### TestCase Objective
flushes the database cache

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Flush Cache | Invoke flushCache on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.flushCache"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the cache is cleared successfully |

---

<a id="persistentstore_check_on_value_changed_event"></a>
### TestCase Name
PersistentStore_Check_On_Value_Changed_Event

### TestCase ID
PS_06

### TestCase Objective
Sets and gets the particular key value

### Test Steps

> **Value Loop (Steps 1–3):** Steps 1–3 repeat **3 times**, once for each value of `value`: `Value_1`, `Value_2`, `Value_3`

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke setValue on org.rdk.PersistentStore with namespace: "Namespace_3", key: "Key_1", value: "<VALUE_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_3", "key": "Key_1", "value": "<VALUE_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get Value | Invoke getValue on org.rdk.PersistentStore with namespace: "Namespace_3", key: "Key_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Namespace_3", "key": "Key_1"}}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` returned value matches the iterated value set in the previous step |
| 3 | Check On Value Changed Event | Listen for Event_On_Value_Changed event (wait 2s) | `success` : `true` returned value matches the iterated value set in the previous step |

---

<a id="persistentstore_set_and_get_storage_limits"></a>
### TestCase Name
PersistentStore_Set_And_Get_Storage_Limits

### TestCase ID
PS_07

### TestCase Objective
Set and get storage limits for available namespaces

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Namespaces | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that namespaces are returned successfully |
| 2 | Delete Namespace | *(Conditional statement executed only if previous step condition is met)*<br>Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace is deleted successfully |
| 3 | Set Namespace Storagelimit | Invoke setNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "username", "storageLimit": 20}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace storage limit is set successfully |
| 4 | Get Namespace Storagelimit | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Expected `20` |
| 5 | Delete Namespace | Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace is deleted successfully |

---

<a id="persistentstore_check_set_and_get_empty_storage_limits"></a>
### TestCase Name
PersistentStore_Check_Set_And_Get_Empty_Storage_Limits

### TestCase ID
PS_08

### TestCase Objective
Verify persistent store handles empty, sets and retrieves storage namespace limits

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Namespace Storagelimit | Invoke setNamespaceStorageLimit on org.rdk.PersistentStore with namespace: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "", "storageLimit": 20}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |
| 2 | Get Namespace Storagelimit | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_verify_setvalue_and_getvalue_api_with_empty_key_operations"></a>
### TestCase Name
PersistentStore_Verify_SetValue_And_GetValue_API_with_Empty_Key_Operations

### TestCase ID
PS_09

### TestCase Objective
Verify persistent store handles empty key, set and get operatins across namespaces

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke setValue on org.rdk.PersistentStore with namespace: "username", key: "", value: "user"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "username", "key": "", "value": "user"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |
| 2 | Get Value | Invoke getValue on org.rdk.PersistentStore with namespace: "username", key: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "username", "key": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_UNKNOWN_KEY` |

---

<a id="persistentstore_verify_setvalue_and_getvalue_api_with_empty_namespce_operations"></a>
### TestCase Name
PersistentStore_Verify_SetValue_And_GetValue_API_with_Empty_Namespce_Operations

### TestCase ID
PS_10

### TestCase Objective
Verify persistent store handles empty namespace, set and get operatins

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke setValue on org.rdk.PersistentStore with namespace: "", key: "username", value: "user"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "", "key": "username", "value": "user"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |
| 2 | Get Value | Invoke getValue on org.rdk.PersistentStore with namespace: "", key: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "", "key": "username"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getstorage_namespacelimit_for_deletednamespace"></a>
### TestCase Name
PersistentStore_GetStorage_NamespaceLimit_For_DeletedNamespace

### TestCase ID
PS_11

### TestCase Objective
Verify that attempting to retrieve the storage namespace limit for a namespace that has already been deleted results in an appropriate error or indication, such as a null response or a specific error message

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Namespaces | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that namespaces are returned successfully |
| 2 | Delete Namespace | *(Conditional statement executed only if previous step condition is met)*<br>Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace is deleted successfully |
| 3 | Get Namespace Storagelimit | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_activatedeactivate_event_test"></a>
### TestCase Name
PersistentStore_ActivateDeactivate_Event_Test

### TestCase ID
PS_12

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of PersistentStore Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PersistentStore Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of PersistentStore Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate PersistentStore Plugin | Invoke deactivate on Controller with callsign: "org.rdk.PersistentStore"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | `statechange` event received; callsign = `org.rdk.persistentstore`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate org.rdk.PersistentStore Plugin | Invoke activate on Controller with callsign: "org.rdk.PersistentStore"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | `statechange` event received; callsign = `org.rdk.persistentstore`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

---

## Plugin Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M88 |