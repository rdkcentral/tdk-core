# FNCS_iCrypto_Vault_Tests Test Case Documentation

## TestCase ID
FNCS_ICRYPTO_02

## TestCase Name
FNCS_iCrypto_Vault_Tests

## Objective
Validate iCrypto secure vault storage and key lifecycle management including import/export and set/get operations. The test verifies that cryptographic key material can be securely stored in the vault using import operations and correctly retrieved using export operations, with proper verification of stored data. The test also validates alternative vault storage using set/get operations for sealed key material management. The test ensures the IVault interface correctly implements secure key storage, retrieval, deletion, and state transitions for cryptographic material lifecycle.

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | iCrypto_Package should be installed in DUT |
| 2 | cgfacetests application (iCrypto Vault interface test binary) must be available in DUT at standard system path |
| 3 | ICryptography instance must be successfully acquired from Thunder framework |
| 4 | Default or Platform vault instance must be accessible for key storage, retrieval, and lifecycle management |
| 5 | Vault must support import operation to store raw key material and allocate unique key IDs (>0x80000000U) |
| 6 | Vault must support export operation to retrieve stored key material with correct size tracking |
| 7 | Vault must support key ID allocation with size tracking (Size() returning 0 for non-existent keys, variable sizes for stored keys) |
| 8 | Vault must support set/get operations for sealed key material with USHRT_MAX size reporting for sealed data |
| 9 | Vault must support deletion of stored keys with proper cleanup and size tracking confirmation |
| 10 | Test vector data must be available: 16-byte test data (0x74, 0x74, 0x74... x16) for import/export operations |
| 11 | Vault must support both OpenSSL backend (with full export data verification) and SecApi backend (with reference semantics) |
| 12 | Device must support minimum 16KB sealed buffer size for set/get operations |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Cryptography Environment | Acquire ICryptography instance from Thunder framework and obtain appropriate vault instance (Default or Platform based on test requirements). Verify vault state operations are available and accessible. Execute cgfacetests application to initialize the vault test environment. | ICryptography instance must be acquired successfully, vault instance must be accessible and ready for storage operations, cgfacetests application must start without errors, and all vault lifecycle operations must be available |
| 2 | Query Initial Vault State | Check vault size for non-existent key IDs (0 and 0x80000000U). Attempt to delete non-existent keys. Verify vault properly returns zero size and delete failure for invalid keys. | Vault->Size(0) must return 0, Vault->Size(0x80000000U) must return 0, Vault->Delete(0) must fail and return false, Vault->Delete(0x80000000U) must fail, confirming proper validation of invalid key IDs |
| 3 | Import Test Data into Vault | Store 16-byte test vector data (0x74, 0x74, 0x74... x16) into secure vault using vault->Import(). Capture the returned key ID. Verify key ID is allocated properly (must be greater than 0x80000000U). | Test data must be imported successfully into vault, returned key ID must be greater than 0x80000000U indicating vault-allocated storage, and import operation must complete without errors |
| 4 | Verify Imported Key Size Tracking | Query vault->Size() for the imported key ID. Verify returned size matches imported data size (16 bytes). | Vault->Size() must return exactly 16 for the imported key ID, confirming vault correctly tracks stored data size |
| 5 | Export Imported Data from Vault | Retrieve stored key material using vault->Export() operation. Allocate output buffer matching imported data size (16 bytes). Export data into buffer. Verify export size returned by operation. | Export operation must complete successfully, returned export size must be exactly 16 bytes matching imported data, and exported data buffer must contain key material bytes |
| 6 | Verify Exported Data Matches Original | Compare exported data byte-by-byte against original test vector (0x74, 0x74, 0x74... x16). For OpenSSL backend only, data must match exactly. For SecApi backend, reference semantics may apply but size must be correct. | Exported data must match original test vector (OpenSSL backend), size verification must pass (all backends), confirming export returns correct key material |
| 7 | Delete Imported Key from Vault | Call vault->Delete() with the imported key ID. Verify delete operation returns true indicating successful deletion. | Delete operation must complete successfully and return true, indicating key was removed from vault storage |
| 8 | Verify Key Removal After Delete | Query vault->Size() for the deleted key ID. Verify size returns 0 indicating key is no longer in vault. | Vault->Size() must return 0 for deleted key ID, confirming key material was completely removed from secure storage |
| 9 | Perform Set Operation on Test Data | Store test data using vault->Set() operation instead of import. Capture returned key ID. Verify key ID is properly allocated. | Set operation must complete successfully, returned key ID must be greater than 0x80000000U indicating vault-allocated storage, and operation must return valid key reference |
| 10 | Verify Set Operation Size Reporting | Query vault->Size() for the key created with Set operation. For OpenSSL backend, size should be USHRT_MAX. | Vault->Size() must return USHRT_MAX for sealed keys, confirming set operation properly marks data as sealed/sensitive |
| 11 | Retrieve Data Using Get Operation | Call vault->Get() with the set-created key ID and output buffer (minimum 16KB). Retrieve sealed data. | Get operation must complete successfully, returned size must be valid and non-zero, and output buffer must contain retrieved key material bytes |
| 12 | Verify Get Operation Returns Correct Data | Compare retrieved data from get operation against original test vector (0x74, 0x74, 0x74... x16). Verify byte-for-byte match. | Retrieved data must match original test vector, all bytes must correspond to stored values, confirming get operation returns sealed key material correctly |
| 13 | Delete Set-Created Key | Call vault->Delete() with the set-created key ID. Verify delete returns success. | Delete operation must complete successfully and return true, indicating sealed key was removed from vault |
| 14 | Confirm Set-Created Key Removal | Query vault->Size() for the deleted set-created key. Verify size returns 0. | Vault->Size() must return 0 for deleted sealed key ID, confirming sealed key material was completely removed |
| 15 | Validate Test Execution Results | Execute cgfacetests and capture output. Parse output to extract Vault test section and search for test summary containing "TOTAL:" and failure count. | Output must contain "TOTAL:" summary with "0 FAILED" indicating all vault import/export and set/get tests passed, confirming vault lifecycle management is correct |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 5 minutes

**Priority:** High

**Release Version:** M121
