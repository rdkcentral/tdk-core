# FNCS_iCrypto_Hash_Tests Test Case Documentation

## TestCase ID
FNCS_ICRYPTO_03

## TestCase Name
FNCS_iCrypto_Hash_Tests

## Objective
Validate iCrypto SHA256 hash and HMAC-SHA256 message authentication code functionality. The test verifies that plaintext data can be correctly hashed using SHA256 algorithm producing a known hash digest, and that HMAC-based message authentication codes can be generated using vault-stored secret keys. The test ensures the ICryptography Hash interface correctly implements both SHA256 hash computation with data ingestion and digest calculation, and HMAC-SHA256 generation with vault key management for authentication verification.

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | iCrypto_Package should be installed in DUT |
| 2 | cgfacetests application (iCrypto Hash and HMAC interface test binary) must be available in DUT at standard system path |
| 3 | ICryptography instance must be successfully acquired from Thunder framework |
| 4 | Default or Platform vault instance must be accessible for HMAC key storage and retrieval |
| 5 | SHA256 hash algorithm support must be available in ICryptography::Hash interface |
| 6 | SHA256 HMAC support must be available in vault HMAC interface |
| 7 | Vault key storage capability must support secret key material for HMAC operations |
| 8 | Hash algorithm must support data ingestion up to minimum 512-byte buffer |
| 9 | Test vector data must be available: "Etaoin Shrldu" (13 bytes) with expected SHA256 hash (0x8072A83C...7835) and Lorem ipsum text with hash (0x69E72153...4D60) |
| 10 | Device must support HMAC calculation with 16-byte secret key material and known HMAC-SHA256 test vector |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Cryptography Environment | Acquire ICryptography instance from Thunder framework and obtain appropriate vault instance (Default or Platform based on test requirements). Verify that all cryptographic interfaces including Hash and HMAC are available and accessible. Execute cgfacetests application to initialize the hash test environment. | ICryptography instance must be acquired successfully, appropriate vault instance must be accessible, cgfacetests application must start without errors, and all cryptographic hash and HMAC operation interfaces must be available for subsequent steps |
| 2 | Initialize SHA256 Hash Algorithm | Create SHA256 hash algorithm interface instance from ICryptography. Prepare 13-byte test data "Etaoin Shrldu" for hashing. Verify hash interface is ready to accept data ingestion. | SHA256 hash interface must be created successfully, hash algorithm state must be initialized and ready for data input, and no errors should occur during interface instantiation |
| 3 | Ingest Test Data into Hash Context | Feed the 13-byte plaintext data "Etaoin Shrldu" into the hash algorithm using the data ingestion interface. Verify all data bytes are accepted by the hash context. | All 13 bytes of test data must be successfully ingested into hash context, hash algorithm must transition to processing state, and ingestion must return success status indicating data acceptance |
| 4 | Calculate SHA256 Hash Digest | Request final hash digest calculation from the hash algorithm with expected output buffer size (32 bytes for SHA256). Retrieve the calculated hash output. | Hash digest calculation must complete successfully, output must be exactly 32 bytes (256 bits), and hash output must be in binary format ready for comparison |
| 5 | Verify Short Text SHA256 Against Test Vector | Compare the generated SHA256 hash digest for "Etaoin Shrldu" byte-by-byte against the known test vector (0x8072A83C 2CFBF367 A1641C22 03CD781D 2E851311 727DCE8E D7255110F E13B7835). | Generated hash must exactly match test vector output, all 32 bytes must correspond to expected values, confirming SHA256 implementation for short text is correct |
| 6 | Hash Long Text Lorem Ipsum | Prepare 445-byte Lorem ipsum text. Ingest all bytes into new SHA256 hash instance. Calculate final hash digest. | SHA256 interface must support data ingestion beyond 256-byte threshold, hash calculation must complete successfully, and digest must be 32 bytes |
| 7 | Verify Long Text SHA256 Against Test Vector | Compare generated SHA256 hash for Lorem ipsum text against known test vector (0x69E72153 EC05BD2D 5D24C164 EDD34709 7BC24CB1 7832 41F8 8A9D3D91 B6D64D60). | Generated hash must exactly match expected long-text test vector, confirming SHA256 handles variable-length input correctly |
| 8 | Import HMAC Secret Key to Vault | Store 15-byte secret key material "_Test_Password_" into secure vault using vault->Import(). Verify valid key ID is allocated and key is accessible for HMAC operations. | Secret key must be imported successfully into vault, returned key ID must be greater than 0x80000000U indicating vault-stored key, key should be retrievable for HMAC operations |
| 9 | Create HMAC-SHA256 Instance with Vault Key | Create HMAC-SHA256 authentication code generator using the vault-stored secret key. Link the vault key ID to HMAC interface. Verify HMAC instance is ready for data processing. | HMAC-SHA256 instance must be created successfully using vault-stored key, HMAC interface must be initialized with correct key context, and no errors should occur during HMAC instantiation |
| 10 | Ingest Test Data into HMAC Context | Feed 13-byte test data "Etaoin Shrldu" into HMAC algorithm using the data ingestion interface. Verify all data bytes are accepted. | All 13 bytes of test data must be successfully ingested into HMAC context, HMAC algorithm must transition to processing state with key material applied, and ingestion must return success status |
| 11 | Calculate HMAC-SHA256 Output | Request final HMAC-SHA256 output calculation with expected buffer size (minimum 128 bytes). Retrieve the calculated HMAC authentication code. | HMAC calculation must complete successfully, output must be at least 32 bytes (SHA256 output size), and HMAC output must contain authentication code bytes ready for comparison |
| 12 | Verify HMAC Output Against Test Vector | Compare generated HMAC-SHA256 authentication code against known test vector (0x5AFFD7A7 701D737B CC69BFDC C342C9CE 472F07E8 EA302199 B7ACC94F 7CDA1523) for secret key "_Test_Password_". | Generated HMAC must exactly match expected test vector, all bytes must correspond to values computed with secret key, confirming HMAC-SHA256 implementation is correct |
| 13 | Release HMAC Resources | Release HMAC interface resources using hashImpl->Release() to free allocated memory and cryptographic context. | HMAC interface must be released cleanly without memory leaks, and no errors should occur during resource cleanup |
| 14 | Delete Vault-Stored HMAC Key | Delete the secret key material from secure vault using vault->Delete() with the stored key ID. Verify vault returns success. Confirm vault->Size() for deleted key returns 0. | Key must be deleted successfully from vault, vault->Size() must return 0 for deleted key ID confirming removal, and vault must report successful deletion |
| 15 | Validate Test Execution Results | Execute cgfacetests and capture output. Parse output to extract Hash and HMAC test sections and search for test summary containing "TOTAL:" and failure count. | Output must contain "TOTAL:" summary with "0 FAILED" indicating all hash and HMAC tests passed, confirming SHA256 and HMAC implementations are correct |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 5 minutes

**Priority:** High

**Release Version:** M121
