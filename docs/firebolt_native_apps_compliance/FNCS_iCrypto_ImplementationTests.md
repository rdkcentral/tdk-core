# FNCS_iCrypto_ImplementationTests Test Case Documentation

## TestCase ID
FNCS_ICRYPTO_04

## TestCase Name
FNCS_iCrypto_ImplementationTests

## Objective
Comprehensive validation of iCrypto backend implementation testing covering all cryptographic operations with focus on backend-specific behavior and implementation correctness. The test executes the complete iCrypto implementation test suite from cgimptests application, verifying that backend implementations (OpenSSL, SecApi, Sage, etc.) correctly perform Vault, Hash, HMAC, Cipher, and Diffie-Hellman operations. The test ensures backend-specific features and behaviors are properly handled and reported with proper error codes and resource cleanup.

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | iCrypto_Package should be installed in DUT |
| 2 | cgimptests application (iCrypto implementation test suite binary) must be available in DUT at standard system path |
| 3 | ICryptography backend implementation must be successfully initialized (OpenSSL, SecApi, Sage, or other platform backend) |
| 4 | All vault instances appropriate for backend must be accessible and functional |
| 5 | All cryptographic algorithms must be implemented in selected backend: Hash (SHA256), HMAC, Cipher (AES-CBC), Diffie-Hellman |
| 6 | Backend-specific vault behaviors must be supported (e.g., reference semantics for SecApi, no set/get for Sage) |
| 7 | All cryptographic interfaces must support proper error reporting and result status indication |
| 8 | All cryptographic interfaces must support resource release with proper cleanup for all backends |
| 9 | Implementation test vectors must be available for all cryptographic operations across all supported backends |
| 10 | Device must support backend-specific test selection and execution with appropriate conditional test skipping |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Backend Implementation | Acquire ICryptography instance and verify which backend implementation is active (OpenSSL, SecApi, Sage, etc.). Initialize backend-specific cryptographic contexts and verify backend is ready for testing. | ICryptography instance must be acquired successfully, backend type must be identifiable, backend-specific cryptographic contexts must initialize correctly, and backend must be ready for comprehensive testing |
| 2 | Execute Backend Vault Import/Export Operations | Run vault import/export test subset from cgimptests with backend-specific semantics. For OpenSSL: verify full data export and byte-wise comparison. For SecApi: verify reference-based export and size tracking only. | Vault operations must complete according to backend semantics, OpenSSL backend must support full data verification, SecApi backend must handle reference returns correctly, and vault resource management must work for selected backend |
| 3 | Execute Backend Vault Set/Get Operations | Run vault set/get test subset from cgimptests with backend-specific support. For OpenSSL and others: execute full set/get tests. For Sage: conditionally skip or report unsupported. Verify backend-appropriate behavior. | Set/get operations must execute if backend supports them, sealed key size tracking must work correctly, data retrieval must function per backend semantics, unsupported backends must report appropriately |
| 4 | Execute Backend Hash Algorithm Tests | Run SHA256 hash test subset with backend-specific implementation. Verify hash computation produces correct digests regardless of backend. Test with short (13-byte) and long (445-byte) data. | Hash operations must complete successfully on selected backend, SHA256 digests must match test vectors, both short and long data must be processed correctly, and hash results must be backend-independent |
| 5 | Execute Backend HMAC Tests | Run HMAC-SHA256 test subset with backend-specific vault key storage and HMAC computation. Verify HMAC operations work with vault-managed keys on selected backend. | HMAC operations must complete successfully with backend vault key management, HMAC outputs must match test vectors, vault key storage must work correctly for HMAC on backend, and HMAC resource cleanup must be proper |
| 6 | Execute Backend Cipher Operations | Run AES-CBC encryption/decryption test subset with backend-specific cipher implementation. Verify cipher operations produce correct ciphertext and plaintext recovery. Test round-trip encryption and decryption. | Cipher operations must complete successfully on backend, AES-CBC encryption must produce test-vector-matching ciphertext, decryption must recover original plaintext, and cipher resources must be properly managed by backend |
| 7 | Execute Backend Diffie-Hellman Key Generation | Run DH key pair generation test subset on selected backend. Verify DH operations produce valid key pairs with proper ID allocation and key property reporting. | DH key generation must complete successfully on backend, key IDs must be properly allocated (>0x80000000U), generated keys must be valid for key exchange, and key properties must match expectations |
| 8 | Validate Backend-Specific Error Handling | Monitor cgimptests output for backend-specific error codes, warnings, or conditional test skipping messages. Verify error handling aligns with backend implementation. | Error codes must be appropriate for backend, backend limitations must be reported clearly, no unexpected errors should appear, and error handling should be consistent with implementation |
| 9 | Verify Backend Resource Cleanup | Confirm all cryptographic interfaces properly release resources after operations. Check for memory leaks or resource exhaustion warnings. Verify cleanup works consistently across all operations. | All released resources must be properly deallocated, no memory leak warnings should appear, resource cleanup must occur after each operation, and cleanup must be consistent across all backends |
| 10 | Parse Backend Implementation Test Summary | Extract final test summary from cgimptests output. Identify backend name in results if provided. Confirm all backend-appropriate tests executed successfully. | Summary must indicate backend type if identifiable, all backend-appropriate tests must show execution, failure count must be zero for all backend tests, and summary format must be standard "TOTAL:" with result count |
| 11 | Verify Backend Implementation Consistency | Cross-check test results for consistency with backend expectations and known limitations. Ensure no unexpected backend-specific failures or conditional test issues. | Results must align with known backend capabilities, no unexpected test failures for backend, all conditional tests must execute appropriately, and backend integration must be consistent |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 5 minutes

**Priority:** High

**Release Version:** M121
