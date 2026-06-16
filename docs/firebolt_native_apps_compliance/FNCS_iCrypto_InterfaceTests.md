# FNCS_iCrypto_InterfaceTests Test Case Documentation

## TestCase ID
FNCS_ICRYPTO_05

## TestCase Name
FNCS_iCrypto_InterfaceTests

## Objective
Comprehensive validation of iCrypto ICryptography interface implementation including all cryptographic operations (Vault, Hash, HMAC, Cipher, Diffie-Hellman). The test executes the complete iCrypto interface test suite from cgimptests application, verifying that all ICryptography interface implementations function correctly with known test vectors and expected cryptographic outputs. The test ensures the Thunder framework ICryptography interface correctly integrates all cryptographic modules and supports proper resource lifecycle management across all operations.

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | iCrypto_Package should be installed in DUT |
| 2 | cgimptests application (iCrypto interface test suite binary) must be available in DUT at standard system path |
| 3 | ICryptography interface must be successfully acquired from Thunder framework |
| 4 | All vault instances (Default, Platform, Netflix if applicable) must be accessible |
| 5 | All cryptographic algorithm interfaces must be available: Hash (SHA256), HMAC, Cipher (AES-CBC), Diffie-Hellman |
| 6 | All vault operations must be supported: import, export, set, get, delete |
| 7 | All cryptographic interfaces must support resource release and cleanup operations |
| 8 | Test vectors for Vault, Hash, HMAC, Cipher, and DH operations must be available in cgimptests |
| 9 | Device must support all cryptographic operations execution and error reporting |
| 10 | Test framework must support test enumeration and total test counting with pass/failure reporting |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Test Environment | Acquire ICryptography instance from Thunder framework. Verify all cryptographic interface modules are accessible and functional. Prepare cgimptests application for complete interface test suite execution. | ICryptography instance must be acquired successfully, all cryptographic modules must be accessible, cgimptests application must start without errors, and test framework must be ready for suite execution |
| 2 | Execute Vault Interface Tests | Run vault test subset from cgimptests covering import, export, set, get, and delete operations on test vectors. Verify vault operations complete successfully with proper key ID allocation and data verification. | Vault test subset must execute without premature termination, all key import/export operations must succeed, key deletion must properly remove stored material, and vault state transitions must be correct |
| 3 | Execute Hash Algorithm Tests | Run hash test subset from cgimptests covering SHA256 hash computation with data ingestion and digest calculation on test vectors. Verify hash operations produce expected digests. | Hash test subset must execute successfully, SHA256 digest calculations must match known test vectors, all data ingestion operations must complete, and hash interface must properly release resources |
| 4 | Execute HMAC Authentication Tests | Run HMAC test subset from cgimptests covering HMAC-SHA256 generation with vault-stored keys on test data. Verify HMAC operations produce correct authentication codes. | HMAC test subset must execute successfully, HMAC-SHA256 computations must match known test vectors, vault key storage for HMAC must function correctly, and HMAC interface resources must be properly released |
| 5 | Execute Cipher Encryption Tests | Run cipher test subset from cgimptests covering AES-CBC encryption and decryption with vault-stored keys on test plaintext. Verify cipher operations produce expected ciphertext and correctly decrypt back to plaintext. | Cipher test subset must execute successfully, AES-CBC encryption must produce ciphertext matching test vectors, decryption must recover original plaintext, and cipher interface must handle key management properly |
| 6 | Execute Diffie-Hellman Key Exchange Tests | Run DH test subset from cgimptests covering DH key pair generation with specified generator and modulus. Verify DH operations produce valid key pairs and proper key ID allocation. | DH test subset must execute successfully, key pair generation must complete without errors, generated key IDs must be properly allocated (>0x80000000U), and key properties must be valid |
| 7 | Verify All Cryptographic Operations Executed | Monitor cgimptests output for completion of all cryptographic operation test subsets (Vault, Hash, HMAC, Cipher, DH). Ensure no test subset was skipped or terminated prematurely. | All cryptographic operation test subsets must appear in output, each subset must indicate execution start and completion, no test subset should show skip or abort status |
| 8 | Parse Test Summary Results | Extract final test summary line from cgimptests output containing "TOTAL:" and test count statistics. Identify total number of tests executed. | Output must contain "TOTAL:" line with complete test statistics, test count must be available for verification, and format must be parseable for pass/failure determination |
| 9 | Verify Zero Failures in Test Results | Parse test summary to confirm no failures reported. Search for "0 FAILED" string in summary line. Verify all executed tests passed. | Summary line must indicate "0 FAILED" meaning zero test failures, all cryptographic operations must have passed verification, and no error conditions should be reported in results |
| 10 | Validate Interface Consistency | Verify that test results confirm consistent behavior across all cryptographic modules. Check for any warnings or backend-specific behavior notes in output. | All cryptographic modules must show consistent test pass rates, no selective failures should appear for specific backends, and overall interface implementation must be stable |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 5 minutes

**Priority:** High

**Release Version:** M121
