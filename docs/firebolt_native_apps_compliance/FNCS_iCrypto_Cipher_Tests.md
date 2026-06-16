# FNCS_iCrypto_Cipher_Tests Test Case Documentation

## TestCase ID
FNCS_ICRYPTO_01

## TestCase Name
FNCS_iCrypto_Cipher_Tests

## Objective
Validate iCrypto cipher encryption and decryption functionality using AES-CBC mode with vault-stored keys. The test verifies that plaintext data can be encrypted using a 128-bit AES key with a 16-byte initialization vector (IV), producing known ciphertext output, and that ciphertext can be successfully decrypted back to the original plaintext. The test ensures the ICryptography Cipher interface correctly implements the AES-CBC encryption and decryption operations with proper key management through secure vault storage.

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | iCrypto_Package should be installed in DUT |
| 2 | cgfacetests application (iCrypto Cipher Interface test binary) must be available in DUT at standard system path |
| 3 | ICryptography instance must be successfully acquired from Thunder framework |
| 4 | Default or Platform vault instance must be accessible for key storage and retrieval |
| 5 | AES-CBC cipher support must be available in the ICryptography interface implementation |
| 6 | 128-bit AES keys must be supported in vault import/export operations |
| 7 | 16-byte initialization vector (IV) must be supported for AES-CBC mode operations |
| 8 | Vault must support minimum 48-byte buffer allocation for encrypted output (plaintext size + CBC padding) |
| 9 | Test vector data must be available: plaintext "Look behind you, a Three-Headed Monkey!" and expected AES-CBC ciphertext output |
| 10 | Device must support encryption operation returning encrypted data size matching plaintext size plus padding |
| 11 | Device must support decryption operation returning plaintext data size without padding bytes |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Cryptography Environment | Acquire ICryptography instance from Thunder framework and obtain appropriate vault instance (Netflix, Default, or Platform based on test requirements). Verify that all cryptographic interfaces are available and vault can be accessed successfully. Execute cgfacetests application to initialize the cryptography test environment. | ICryptography instance must be acquired successfully, appropriate vault instance must be accessible, cgfacetests application must start without errors, and all cryptographic cipher operations interfaces must be available for subsequent steps |
| 2 | Import AES Key into Secure Vault | Store 128-bit AES encryption key (16 bytes: 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11) into secure vault using vault->Import() operation. Verify that a valid key ID is allocated and returned by the vault. | Key must be imported successfully into vault, returned key ID must be greater than 0x80000000U indicating vault-stored key, and key should be retrievable for subsequent cipher operations |
| 3 | Create AES-CBC Cipher Instance | Create AES cipher instance in CBC (Cipher Block Chaining) mode using the vault-stored 128-bit key. Retrieve the cipher interface for encryption and decryption operations. | AES-CBC cipher instance must be created successfully, cipher interface must be accessible for encryption/decryption operations, and no errors should occur during cipher instantiation |
| 4 | Encrypt Plaintext Using AES-CBC | Prepare plaintext data "Look behind you, a Three-Headed Monkey!" (40 bytes) and 16-byte IV (0x00 through 0x0f). Call cipher->Encrypt() with IV, plaintext data, and output buffer to generate encrypted ciphertext. Verify encrypted output size matches expected PKCS7-padded size (48 bytes for 40-byte plaintext). | Encryption must complete successfully, encrypted output must be 48 bytes (40-byte plaintext + 8-byte CBC padding), encrypted data must match known test vector (B0F29FB5...BC for the expected ciphertext), and no data corruption should occur during encryption |
| 5 | Verify Encrypted Output Against Test Vector | Compare the generated encrypted ciphertext against the known expected AES-CBC ciphertext test vector. Validate byte-by-byte match for all 48 bytes of ciphertext. | Encrypted output must exactly match the expected test vector (B0F29FB555B24808...A01D60BC), confirming correct encryption implementation |
| 6 | Decrypt Ciphertext Using AES-CBC | Call cipher->Decrypt() with the same IV, encrypted ciphertext (48 bytes), and output buffer to recover plaintext. Verify decrypted output size matches original plaintext length (40 bytes without padding). | Decryption must complete successfully, decrypted output must be 40 bytes (original plaintext size without padding), decrypted data must be retrievable and ready for verification |
| 7 | Verify Decrypted Output Matches Original Plaintext | Compare the decrypted plaintext byte-by-byte against the original plaintext "Look behind you, a Three-Headed Monkey!" (40 bytes). Confirm all bytes match exactly. | Decrypted output must exactly match original plaintext "Look behind you, a Three-Headed Monkey!", confirming successful round-trip encryption and decryption |
| 8 | Release Cipher Resources | Release the cipher interface resources using aes->Release() to free allocated memory and cryptographic context. | Cipher interface must be released cleanly without memory leaks, and no errors should occur during resource cleanup |
| 9 | Delete Vault-Stored Key | Delete the AES key from secure vault using vault->Delete() with the stored key ID. Verify vault returns true indicating successful deletion. Confirm vault->Size() for deleted key ID returns 0 indicating key is removed. | Key must be deleted successfully from vault, vault->Size() must return 0 for deleted key ID confirming removal, and vault must report successful deletion operation |
| 10 | Validate Test Execution Results | Execute cgfacetests and capture output. Parse output to extract Cipher test section and search for test summary line containing "TOTAL:" and failure count. | Output must contain "TOTAL:" summary line with "0 FAILED" indicating all cipher encryption/decryption tests passed, confirming AES-CBC implementation is correct and all verification steps succeeded |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 5 minutes

**Priority:** High

**Release Version:** M121
