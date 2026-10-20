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
   - [PersistentStore_On_Value_Changed_Event](#persistentstore_on_value_changed_event)
   - [PersistentStore_Set_And_Get_Storage_Limits](#persistentstore_set_and_get_storage_limits)
   - [PersistentStore_Set_And_Get_Empty_Storage_Limits](#persistentstore_set_and_get_empty_storage_limits)
   - [PersistentStore_SetValue_And_GetValue_API_with_Empty_Key_Operations](#persistentstore_setvalue_and_getvalue_api_with_empty_key_operations)
   - [PersistentStore_SetValue_And_GetValue_API_with_Empty_Namespce_Operations](#persistentstore_setvalue_and_getvalue_api_with_empty_namespce_operations)
   - [PersistentStore_GetStorage_NamespaceLimit_For_DeletedNamespace](#persistentstore_getstorage_namespacelimit_for_deletednamespace)
   - [PersistentStore_ActivateDeactivate_Event_Test](#persistentstore_activatedeactivate_event_test)
   - [PersistentStore_SetValue_Invalid_Scope](#persistentstore_setvalue_invalid_scope)
   - [PersistentStore_SetValue_Empty_Scope](#persistentstore_setvalue_empty_scope)
   - [PersistentStore_SetValue_Numeric_Scope](#persistentstore_setvalue_numeric_scope)
   - [PersistentStore_SetValue_Special_Scope](#persistentstore_setvalue_special_scope)
   - [PersistentStore_SetValue_Invalid_TTL](#persistentstore_setvalue_invalid_ttl)
   - [PersistentStore_SetValue_Empty_TTL](#persistentstore_setvalue_empty_ttl)
   - [PersistentStore_SetValue_Negative_TTL](#persistentstore_setvalue_negative_ttl)
   - [PersistentStore_SetValue_Special_TTL](#persistentstore_setvalue_special_ttl)
   - [PersistentStore_SetValue_Account_Invalid_TTL](#persistentstore_setvalue_account_invalid_ttl)
   - [PersistentStore_SetValue_Account_Empty_TTL](#persistentstore_setvalue_account_empty_ttl)
   - [PersistentStore_SetValue_Account_Negative_TTL](#persistentstore_setvalue_account_negative_ttl)
   - [PersistentStore_SetValue_Account_Special_TTL](#persistentstore_setvalue_account_special_ttl)
   - [PersistentStore_GetValue_Invalid_Scope](#persistentstore_getvalue_invalid_scope)
   - [PersistentStore_GetValue_Empty_Scope](#persistentstore_getvalue_empty_scope)
   - [PersistentStore_GetValue_Numeric_Scope](#persistentstore_getvalue_numeric_scope)
   - [PersistentStore_GetValue_Special_Scope](#persistentstore_getvalue_special_scope)
   - [PersistentStore_GetKeys_Invalid_Scope](#persistentstore_getkeys_invalid_scope)
   - [PersistentStore_GetKeys_Empty_Scope](#persistentstore_getkeys_empty_scope)
   - [PersistentStore_GetKeys_Numeric_Scope](#persistentstore_getkeys_numeric_scope)
   - [PersistentStore_GetKeys_Special_Scope](#persistentstore_getkeys_special_scope)
   - [PersistentStore_DeleteKey_Invalid_Scope](#persistentstore_deletekey_invalid_scope)
   - [PersistentStore_DeleteKey_Empty_Scope](#persistentstore_deletekey_empty_scope)
   - [PersistentStore_DeleteKey_Numeric_Scope](#persistentstore_deletekey_numeric_scope)
   - [PersistentStore_DeleteKey_Special_Scope](#persistentstore_deletekey_special_scope)
   - [PersistentStore_DeleteNamespace_Invalid_Scope](#persistentstore_deletenamespace_invalid_scope)
   - [PersistentStore_DeleteNamespace_Empty_Scope](#persistentstore_deletenamespace_empty_scope)
   - [PersistentStore_DeleteNamespace_Numeric_Scope](#persistentstore_deletenamespace_numeric_scope)
   - [PersistentStore_DeleteNamespace_Special_Scope](#persistentstore_deletenamespace_special_scope)
   - [PersistentStore_GetNamespaces_Invalid_Scope](#persistentstore_getnamespaces_invalid_scope)
   - [PersistentStore_GetNamespaces_Empty_Scope](#persistentstore_getnamespaces_empty_scope)
   - [PersistentStore_GetNamespaces_Numeric_Scope](#persistentstore_getnamespaces_numeric_scope)
   - [PersistentStore_GetNamespaces_Special_Scope](#persistentstore_getnamespaces_special_scope)
   - [PersistentStore_GetStorageSize_Invalid_Scope](#persistentstore_getstoragesize_invalid_scope)
   - [PersistentStore_GetStorageSize_Empty_Scope](#persistentstore_getstoragesize_empty_scope)
   - [PersistentStore_GetStorageSize_Numeric_Scope](#persistentstore_getstoragesize_numeric_scope)
   - [PersistentStore_GetStorageSize_Special_Scope](#persistentstore_getstoragesize_special_scope)
   - [PersistentStore_SetNamespaceStorageLimit_Invalid_Scope](#persistentstore_setnamespacestoragelimit_invalid_scope)
   - [PersistentStore_SetNamespaceStorageLimit_Empty_Scope](#persistentstore_setnamespacestoragelimit_empty_scope)
   - [PersistentStore_SetNamespaceStorageLimit_Numeric_Scope](#persistentstore_setnamespacestoragelimit_numeric_scope)
   - [PersistentStore_SetNamespaceStorageLimit_Special_Scope](#persistentstore_setnamespacestoragelimit_special_scope)
   - [PersistentStore_GetNamespaceStorageLimit_Invalid_Scope](#persistentstore_getnamespacestoragelimit_invalid_scope)
   - [PersistentStore_GetNamespaceStorageLimit_Empty_Scope](#persistentstore_getnamespacestoragelimit_empty_scope)
   - [PersistentStore_GetNamespaceStorageLimit_Numeric_Scope](#persistentstore_getnamespacestoragelimit_numeric_scope)
   - [PersistentStore_GetNamespaceStorageLimit_Special_Scope](#persistentstore_getnamespacestoragelimit_special_scope)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **PersistentStore** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.PersistentStore` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_PersistentStore_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of PersistentStore plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PersistentStore plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of PersistentStore plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onValueChanged event | Register a WebSocket event listener for `onValueChanged` to receive `onValueChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.register", "params": {"event": "onValueChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

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

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value in PersistentStore | Invoke setValue on org.rdk.PersistentStore with namespace: "Namespace_1", key: "Key_1", value: "<VALUE_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_1", "key": "Key_1", "value": "<VALUE_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get value from PersistentStore | Invoke getValue on org.rdk.PersistentStore with namespace: "Namespace_1", key: "Key_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Namespace_1", "key": "Key_1"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |

---

<a id="persistentstore_delete_key"></a>
### TestCase Name
PersistentStore_Delete_Key

### TestCase ID
PS_02

### TestCase Objective
Deletes the key

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value in PersistentStore | Invoke setValue on org.rdk.PersistentStore with namespace: "Namespace_1", key: "Key_2", value: "Value_2"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_1", "key": "Key_2", "value": "Value_2"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get keys from PersistentStore namespace | Invoke getKeys on org.rdk.PersistentStore with namespace: "Namespace_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Namespace_1"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, `Key_2` present in the returned keys list  |
| 3 | Delete key from PersistentStore | Invoke deleteKey on org.rdk.PersistentStore with namespace: "Namespace_1", key: "Key_2"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteKey", "params": {"namespace": "Namespace_1", "key": "Key_2"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the key is deleted successfully |
| 4 | Get keys from PersistentStore namespace | Invoke getKeys on org.rdk.PersistentStore with namespace: "Namespace_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Namespace_1"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, `Key_2` absent from the returned keys list  |

---

<a id="persistentstore_delete_namespace"></a>
### TestCase Name
PersistentStore_Delete_Namespace

### TestCase ID
PS_03

### TestCase Objective
Deletes the Namespace

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value in PersistentStore | Invoke setValue on org.rdk.PersistentStore with namespace: "Namespace_2", key: "Key_1", value: "Value_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_2", "key": "Key_1", "value": "Value_1"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get PersistentStore namespace list | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that `Namespace_2` is present in the namespaces list as expected  |
| 3 | Delete namespace from PersistentStore | Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "Namespace_2"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "Namespace_2"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace is deleted successfully |
| 4 | Get PersistentStore namespace list | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that `Namespace_2` is absent from the namespaces list, confirming successful deletion  |

---

<a id="persistentstore_get_storage_size"></a>
### TestCase Name
PersistentStore_Get_Storage_Size

### TestCase ID
PS_04

### TestCase Objective
Gets the storage size of the available namespaces

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get PersistentStore namespace list | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that namespaces are returned successfully |
| 2 | Get storage size | Invoke getStorageSize on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getStorageSize"}' http://127.0.0.1:9998/jsonrpc` | Verify that the storage size is returned successfully |

---

<a id="persistentstore_flush_cache"></a>
### TestCase Name
PersistentStore_Flush_Cache

### TestCase ID
PS_05

### TestCase Objective
flushes the database cache

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Flush PersistentStore cache | Invoke flushCache on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.flushCache"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the cache is cleared successfully |

---

<a id="persistentstore_on_value_changed_event"></a>
### TestCase Name
PersistentStore_On_Value_Changed_Event

### TestCase ID
PS_06

### TestCase Objective
Sets and gets the particular key value

### Test Steps

> **Value Loop (Steps 1–3):** Steps 1–3 repeat **3 times**, once for each value of `value`: `Value_1`, `Value_2`, `Value_3`

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value in PersistentStore | Invoke setValue on org.rdk.PersistentStore with namespace: "Namespace_3", key: "Key_1", value: "<VALUE_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Namespace_3", "key": "Key_1", "value": "<VALUE_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get value from PersistentStore | Invoke getValue on org.rdk.PersistentStore with namespace: "Namespace_3", key: "Key_1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Namespace_3", "key": "Key_1"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |
| 3 | Check on value changed event | Listen for Event_On_Value_Changed event (wait 2s) | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |

---

<a id="persistentstore_set_and_get_storage_limits"></a>
### TestCase Name
PersistentStore_Set_And_Get_Storage_Limits

### TestCase ID
PS_07

### TestCase Objective
Set and get storage limits for available namespaces

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get PersistentStore namespace list | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that namespaces are returned successfully |
| 2 | Delete namespace from PersistentStore | *(Conditional statement executed only if previous step condition is met)*<br>Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace is deleted successfully |
| 3 | Set namespace storagelimit | Invoke setNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "username", storageLimit: 20<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "username", "storageLimit": 20}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace storage limit is set successfully |
| 4 | Get namespace storagelimit | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value is `20` as expected  |
| 5 | Delete namespace from PersistentStore | Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace is deleted successfully |

---

<a id="persistentstore_set_and_get_empty_storage_limits"></a>
### TestCase Name
PersistentStore_Set_And_Get_Empty_Storage_Limits

### TestCase ID
PS_08

### TestCase Objective
Verify persistent store handles empty, sets and retrieves storage namespace limits

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set namespace storagelimit | Invoke setNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "", storageLimit: 20<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "", "storageLimit": 20}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |
| 2 | Get namespace storagelimit | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_setvalue_and_getvalue_api_with_empty_key_operations"></a>
### TestCase Name
PersistentStore_SetValue_And_GetValue_API_with_Empty_Key_Operations

### TestCase ID
PS_09

### TestCase Objective
Verify persistent store handles empty key, set and get operations across namespaces

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value in PersistentStore | Invoke setValue on org.rdk.PersistentStore with namespace: "username", key: "", value: "user"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "username", "key": "", "value": "user"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |
| 2 | Get value from PersistentStore | Invoke getValue on org.rdk.PersistentStore with namespace: "username", key: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "username", "key": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_UNKNOWN_KEY` |

---

<a id="persistentstore_setvalue_and_getvalue_api_with_empty_namespce_operations"></a>
### TestCase Name
PersistentStore_SetValue_And_GetValue_API_with_Empty_Namespce_Operations

### TestCase ID
PS_10

### TestCase Objective
Verify persistent store handles empty namespace, set and get operations

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value in PersistentStore | Invoke setValue on org.rdk.PersistentStore with namespace: "", key: "username", value: "user"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "", "key": "username", "value": "user"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |
| 2 | Get value from PersistentStore | Invoke getValue on org.rdk.PersistentStore with namespace: "", key: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "", "key": "username"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getstorage_namespacelimit_for_deletednamespace"></a>
### TestCase Name
PersistentStore_GetStorage_NamespaceLimit_For_DeletedNamespace

### TestCase ID
PS_11

### TestCase Objective
Verify that attempting to retrieve the storage namespace limit for a namespace that has already been deleted results in an appropriate error or indication, such as a null response or a specific error message

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get PersistentStore namespace list | Invoke getNamespaces on org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces"}' http://127.0.0.1:9998/jsonrpc` | Verify that namespaces are returned successfully |
| 2 | Delete namespace from PersistentStore | *(Conditional statement executed only if previous step condition is met)*<br>Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the namespace is deleted successfully |
| 3 | Get namespace storagelimit | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "username"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "username"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_activatedeactivate_event_test"></a>
### TestCase Name
PersistentStore_ActivateDeactivate_Event_Test

### TestCase ID
PS_12

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of PersistentStore plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PersistentStore plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of PersistentStore plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate PersistentStore plugin | Invoke deactivate on Controller with callsign: "org.rdk.PersistentStore"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `org.rdk.persistentstore` with state `"deactivated"` |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate org.rdk.PersistentStore plugin | Invoke activate on Controller with callsign: "org.rdk.PersistentStore"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check state change event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `org.rdk.persistentstore` with state `"activated"` |
| 6 | Check plugin active status | Invoke status on Controller for org.rdk.PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PersistentStore"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="persistentstore_setvalue_invalid_scope"></a>
### TestCase Name
PersistentStore_SetValue_Invalid_Scope

### TestCase ID
PS_13

### TestCase Objective
Set value rejects an invalid scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value invalid scope | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "invalid_scope"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "invalid_scope"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setvalue_empty_scope"></a>
### TestCase Name
PersistentStore_SetValue_Empty_Scope

### TestCase ID
PS_14

### TestCase Objective
Set value rejects an empty scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value empty scope | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setvalue_numeric_scope"></a>
### TestCase Name
PersistentStore_SetValue_Numeric_Scope

### TestCase ID
PS_15

### TestCase Objective
Set value rejects a numeric scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value numeric scope | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setvalue_special_scope"></a>
### TestCase Name
PersistentStore_SetValue_Special_Scope

### TestCase ID
PS_16

### TestCase Objective
Set value rejects special characters in scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value special scope | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setvalue_invalid_ttl"></a>
### TestCase Name
PersistentStore_SetValue_Invalid_TTL

### TestCase ID
PS_17

### TestCase Objective
Set value rejects an invalid TTL

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value invalid TTL | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "device", ttl: "invalid_ttl"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "device", "ttl": "invalid_ttl"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setvalue_empty_ttl"></a>
### TestCase Name
PersistentStore_SetValue_Empty_TTL

### TestCase ID
PS_18

### TestCase Objective
Set value rejects an empty TTL

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value empty TTL | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "device", ttl: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "device", "ttl": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_setvalue_negative_ttl"></a>
### TestCase Name
PersistentStore_SetValue_Negative_TTL

### TestCase ID
PS_19

### TestCase Objective
Set value rejects a negative TTL

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value negative TTL | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "device", ttl: -1<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "device", "ttl": -1}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_setvalue_special_ttl"></a>
### TestCase Name
PersistentStore_SetValue_Special_TTL

### TestCase ID
PS_20

### TestCase Objective
Set value rejects special characters in TTL

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value special TTL | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "device", ttl: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "device", "ttl": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setvalue_account_invalid_ttl"></a>
### TestCase Name
PersistentStore_SetValue_Account_Invalid_TTL

### TestCase ID
PS_21

### TestCase Objective
Set value rejects an invalid TTL

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value account invalid TTL | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "account", ttl: "invalid_ttl"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "account", "ttl": "invalid_ttl"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setvalue_account_empty_ttl"></a>
### TestCase Name
PersistentStore_SetValue_Account_Empty_TTL

### TestCase ID
PS_22

### TestCase Objective
Set value rejects an empty TTL

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value account empty TTL | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "account", ttl: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "account", "ttl": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_setvalue_account_negative_ttl"></a>
### TestCase Name
PersistentStore_SetValue_Account_Negative_TTL

### TestCase ID
PS_23

### TestCase Objective
Set value rejects a negative TTL

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value account negative TTL | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "account", ttl: -1<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "account", "ttl": -1}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_setvalue_account_special_ttl"></a>
### TestCase Name
PersistentStore_SetValue_Account_Special_TTL

### TestCase ID
PS_24

### TestCase Objective
Set value rejects special characters in TTL

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value account special TTL | Invoke setValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", value: "Scope_Value", scope: "account", ttl: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "value": "Scope_Value", "scope": "account", "ttl": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_getvalue_invalid_scope"></a>
### TestCase Name
PersistentStore_GetValue_Invalid_Scope

### TestCase ID
PS_25

### TestCase Objective
GetValue rejects an invalid scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get value invalid scope | Invoke getValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", scope: "invalid_scope"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "scope": "invalid_scope"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getvalue_empty_scope"></a>
### TestCase Name
PersistentStore_GetValue_Empty_Scope

### TestCase ID
PS_26

### TestCase Objective
GetValue rejects an empty scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get value empty scope | Invoke getValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", scope: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "scope": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getvalue_numeric_scope"></a>
### TestCase Name
PersistentStore_GetValue_Numeric_Scope

### TestCase ID
PS_27

### TestCase Objective
GetValue rejects a numeric scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get value numeric scope | Invoke getValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", scope: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "scope": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getvalue_special_scope"></a>
### TestCase Name
PersistentStore_GetValue_Special_Scope

### TestCase ID
PS_28

### TestCase Objective
GetValue rejects special characters in scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get value special scope | Invoke getValue on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", scope: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "scope": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getkeys_invalid_scope"></a>
### TestCase Name
PersistentStore_GetKeys_Invalid_Scope

### TestCase ID
PS_29

### TestCase Objective
GetKeys rejects an invalid scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get keys invalid scope | Invoke getKeys on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: "invalid_scope"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Scope_Namespace", "scope": "invalid_scope"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getkeys_empty_scope"></a>
### TestCase Name
PersistentStore_GetKeys_Empty_Scope

### TestCase ID
PS_30

### TestCase Objective
GetKeys rejects an empty scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get keys empty scope | Invoke getKeys on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Scope_Namespace", "scope": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getkeys_numeric_scope"></a>
### TestCase Name
PersistentStore_GetKeys_Numeric_Scope

### TestCase ID
PS_31

### TestCase Objective
GetKeys rejects a numeric scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get keys numeric scope | Invoke getKeys on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Scope_Namespace", "scope": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getkeys_special_scope"></a>
### TestCase Name
PersistentStore_GetKeys_Special_Scope

### TestCase ID
PS_32

### TestCase Objective
GetKeys rejects special characters in scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get keys special scope | Invoke getKeys on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getKeys", "params": {"namespace": "Scope_Namespace", "scope": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_deletekey_invalid_scope"></a>
### TestCase Name
PersistentStore_DeleteKey_Invalid_Scope

### TestCase ID
PS_33

### TestCase Objective
DeleteKey rejects an invalid scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete key invalid scope | Invoke deleteKey on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", scope: "invalid_scope"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteKey", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "scope": "invalid_scope"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_deletekey_empty_scope"></a>
### TestCase Name
PersistentStore_DeleteKey_Empty_Scope

### TestCase ID
PS_34

### TestCase Objective
DeleteKey rejects an empty scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete key empty scope | Invoke deleteKey on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", scope: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteKey", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "scope": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_deletekey_numeric_scope"></a>
### TestCase Name
PersistentStore_DeleteKey_Numeric_Scope

### TestCase ID
PS_35

### TestCase Objective
DeleteKey rejects a numeric scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete key numeric scope | Invoke deleteKey on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", scope: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteKey", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "scope": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_deletekey_special_scope"></a>
### TestCase Name
PersistentStore_DeleteKey_Special_Scope

### TestCase ID
PS_36

### TestCase Objective
DeleteKey rejects special characters in scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete key special scope | Invoke deleteKey on org.rdk.PersistentStore with namespace: "Scope_Namespace", key: "Scope_Key", scope: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteKey", "params": {"namespace": "Scope_Namespace", "key": "Scope_Key", "scope": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_deletenamespace_invalid_scope"></a>
### TestCase Name
PersistentStore_DeleteNamespace_Invalid_Scope

### TestCase ID
PS_37

### TestCase Objective
DeleteNamespace rejects an invalid scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete namespace invalid scope | Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: "invalid_scope"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "Scope_Namespace", "scope": "invalid_scope"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_deletenamespace_empty_scope"></a>
### TestCase Name
PersistentStore_DeleteNamespace_Empty_Scope

### TestCase ID
PS_38

### TestCase Objective
DeleteNamespace rejects an empty scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete namespace empty scope | Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "Scope_Namespace", "scope": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_deletenamespace_numeric_scope"></a>
### TestCase Name
PersistentStore_DeleteNamespace_Numeric_Scope

### TestCase ID
PS_39

### TestCase Objective
DeleteNamespace rejects a numeric scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete namespace numeric scope | Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "Scope_Namespace", "scope": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_deletenamespace_special_scope"></a>
### TestCase Name
PersistentStore_DeleteNamespace_Special_Scope

### TestCase ID
PS_40

### TestCase Objective
DeleteNamespace rejects special characters in scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete namespace special scope | Invoke deleteNamespace on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.deleteNamespace", "params": {"namespace": "Scope_Namespace", "scope": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getnamespaces_invalid_scope"></a>
### TestCase Name
PersistentStore_GetNamespaces_Invalid_Scope

### TestCase ID
PS_41

### TestCase Objective
GetNamespaces rejects an invalid scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get namespaces invalid scope | Invoke getNamespaces on org.rdk.PersistentStore with scope: "invalid_scope"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces", "params": {"scope": "invalid_scope"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getnamespaces_empty_scope"></a>
### TestCase Name
PersistentStore_GetNamespaces_Empty_Scope

### TestCase ID
PS_42

### TestCase Objective
GetNamespaces rejects an empty scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get namespaces empty scope | Invoke getNamespaces on org.rdk.PersistentStore with scope: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces", "params": {"scope": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getnamespaces_numeric_scope"></a>
### TestCase Name
PersistentStore_GetNamespaces_Numeric_Scope

### TestCase ID
PS_43

### TestCase Objective
GetNamespaces rejects a numeric scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get namespaces numeric scope | Invoke getNamespaces on org.rdk.PersistentStore with scope: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces", "params": {"scope": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getnamespaces_special_scope"></a>
### TestCase Name
PersistentStore_GetNamespaces_Special_Scope

### TestCase ID
PS_44

### TestCase Objective
GetNamespaces rejects special characters in scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get namespaces special scope | Invoke getNamespaces on org.rdk.PersistentStore with scope: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaces", "params": {"scope": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getstoragesize_invalid_scope"></a>
### TestCase Name
PersistentStore_GetStorageSize_Invalid_Scope

### TestCase ID
PS_45

### TestCase Objective
GetStorageSizes rejects an invalid scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get storage size invalid scope | Invoke getStorageSize on org.rdk.PersistentStore with scope: "invalid_scope"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getStorageSize", "params": {"scope": "invalid_scope"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getstoragesize_empty_scope"></a>
### TestCase Name
PersistentStore_GetStorageSize_Empty_Scope

### TestCase ID
PS_46

### TestCase Objective
GetStorageSizes rejects an empty scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get storage size empty scope | Invoke getStorageSize on org.rdk.PersistentStore with scope: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getStorageSize", "params": {"scope": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getstoragesize_numeric_scope"></a>
### TestCase Name
PersistentStore_GetStorageSize_Numeric_Scope

### TestCase ID
PS_47

### TestCase Objective
GetStorageSizes rejects a numeric scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get storage size numeric scope | Invoke getStorageSize on org.rdk.PersistentStore with scope: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getStorageSize", "params": {"scope": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_getstoragesize_special_scope"></a>
### TestCase Name
PersistentStore_GetStorageSize_Special_Scope

### TestCase ID
PS_48

### TestCase Objective
GetStorageSizes rejects special characters in scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get storage size special scope | Invoke getStorageSize on org.rdk.PersistentStore with scope: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getStorageSize", "params": {"scope": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="persistentstore_setnamespacestoragelimit_invalid_scope"></a>
### TestCase Name
PersistentStore_SetNamespaceStorageLimit_Invalid_Scope

### TestCase ID
PS_49

### TestCase Objective
setNamespaceStorageLimit rejects an invalid scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set storage limit invalid scope | Invoke setNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "Scope_Namespace", storageLimit: 20, scope: "invalid_scope"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "Scope_Namespace", "storageLimit": 20, "scope": "invalid_scope"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setnamespacestoragelimit_empty_scope"></a>
### TestCase Name
PersistentStore_SetNamespaceStorageLimit_Empty_Scope

### TestCase ID
PS_50

### TestCase Objective
setNamespaceStorageLimit rejects an empty scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set storage limit empty scope | Invoke setNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "Scope_Namespace", storageLimit: 20, scope: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "Scope_Namespace", "storageLimit": 20, "scope": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setnamespacestoragelimit_numeric_scope"></a>
### TestCase Name
PersistentStore_SetNamespaceStorageLimit_Numeric_Scope

### TestCase ID
PS_51

### TestCase Objective
setNamespaceStorageLimit rejects a numeric scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set storage limit numeric scope | Invoke setNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "Scope_Namespace", storageLimit: 20, scope: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "Scope_Namespace", "storageLimit": 20, "scope": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_setnamespacestoragelimit_special_scope"></a>
### TestCase Name
PersistentStore_SetNamespaceStorageLimit_Special_Scope

### TestCase ID
PS_52

### TestCase Objective
setNamespaceStorageLimit rejects special characters in scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set storage limit special scope | Invoke setNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "Scope_Namespace", storageLimit: 20, scope: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setNamespaceStorageLimit", "params": {"namespace": "Scope_Namespace", "storageLimit": 20, "scope": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_INVALID_INPUT_LENGTH` |

---

<a id="persistentstore_getnamespacestoragelimit_invalid_scope"></a>
### TestCase Name
PersistentStore_GetNamespaceStorageLimit_Invalid_Scope

### TestCase ID
PS_53

### TestCase Objective
getNamespaceStorageLimit rejects an invalid scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get storage limit invalid scope | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: "invalid_scope"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "Scope_Namespace", "scope": "invalid_scope"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getnamespacestoragelimit_empty_scope"></a>
### TestCase Name
PersistentStore_GetNamespaceStorageLimit_Empty_Scope

### TestCase ID
PS_54

### TestCase Objective
getNamespaceStorageLimit rejects an empty scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get storage limit empty scope | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "Scope_Namespace", "scope": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getnamespacestoragelimit_numeric_scope"></a>
### TestCase Name
PersistentStore_GetNamespaceStorageLimit_Numeric_Scope

### TestCase ID
PS_55

### TestCase Objective
getNamespaceStorageLimit rejects a numeric scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get storage limit numeric scope | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "Scope_Namespace", "scope": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |

---

<a id="persistentstore_getnamespacestoragelimit_special_scope"></a>
### TestCase Name
PersistentStore_GetNamespaceStorageLimit_Special_Scope

### TestCase ID
PS_56

### TestCase Objective
getNamespaceStorageLimit rejects special characters in scope

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get storage limit special scope | Invoke getNamespaceStorageLimit on org.rdk.PersistentStore with namespace: "Scope_Namespace", scope: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getNamespaceStorageLimit", "params": {"namespace": "Scope_Namespace", "scope": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_NOT_EXIST` |


## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onValueChanged event | Unregister the WebSocket event listener for `onValueChanged` to stop receiving `onValueChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.unregister", "params": {"event": "onValueChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M88

<div align="right"><a href="#testscript-name">Go to Top</a></div>
