# AI 2.0 Configuration Guide

## Overview

The `ai_2_0_cpe.json` configuration file has been updated to support **environment variable overrides** and **default values**. This prevents hardcoding of sensitive credentials, server URLs, and device-specific settings.

## Configuration Format

Configuration values now support the following format:

```
${ENVIRONMENT_VARIABLE:default_value}
```

**Where:**
- `ENVIRONMENT_VARIABLE` - Name of the environment variable to read
- `default_value` - Optional fallback value if the environment variable is not set

**Examples:**
```json
"host": "${THUNDER_HOST:127.0.0.1}"   // Uses THUNDER_HOST env var, defaults to 127.0.0.1
"port": "${THUNDER_PORT:9998}"         // Uses THUNDER_PORT env var, defaults to 9998
"password": "${APPSTORE_CATALOG_PASSWORD}"  // REQUIRED - No default, must be set via env var
```

## Environment Variables

### Security Credentials (REQUIRED)

These variables MUST be set in your environment. No defaults provided for security reasons.

```bash
export APPSTORE_CATALOG_PASSWORD="your_password_here"
```

**Variables:**
- `APPSTORE_CATALOG_PASSWORD` - DAC catalog authentication password (required)

### Server Configuration

These variables control server endpoints and can be overridden per environment.

| Variable | Default | Purpose |
|----------|---------|---------|
| `APPSTORE_CATALOG_URL` | `https://dac.dev.rdkinnovation.com` | DAC catalog server URL |
| `APPSTORE_CATALOG_USER` | `dac-cloud-rdkm-user` | DAC catalog username |
| `DAC_CONFIG_URL` | `https://dac.config.dev.fireboltconnect.com/configuration/cpe.json` | DAC configuration endpoint |
| `THUNDER_HOST` | `127.0.0.1` | Thunder/WPEFramework host |
| `THUNDER_PORT` | `9998` | Thunder JSON-RPC port |

### Port Configuration

Configure ports for different services:

| Variable | Default | Purpose |
|----------|---------|---------|
| `PACKAGE_MANAGER_PORT` | `9998` | PackageManager JSON-RPC port |
| `DOWNLOAD_MANAGER_PORT` | `9998` | DownloadManager JSON-RPC port |

### Test File/Directory Configuration

These variables configure test data locations:

| Variable | Default | Purpose |
|----------|---------|---------|
| `TEST_DOWNLOAD_DIR` | `/opt/CDL/` | Download test directory |
| `TEST_FILE` | `/tmp/downloadmanager_test_file.tmp` | Test file path |
| `INVALID_FILE` | `/invalid/nonexistent/file/path.invalid` | Invalid file path for error testing |
| `DOWNLOAD_MANAGER_CONFIG` | `/etc/WPEFramework/plugins/DownloadManager.json` | DownloadManager config file path |

### Test URL Configuration

Configure URLs used in download tests:

| Variable | Default | Purpose |
|----------|---------|---------|
| `TEST_URL_SMALL` | `https://jsonplaceholder.typicode.com/posts/1` | Small test file URL |
| `TEST_URL_MEDIUM` | (no default) | Medium-sized file URL |
| `TEST_URL_LARGE` | (no default) | Large file URL for stress testing |
| `TEST_URL_LARGE_ALT` | `https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4` | Alternative large URL |

## Usage Examples

### Setting Environment Variables

**On Linux/macOS:**
```bash
export THUNDER_HOST="192.168.1.100"
export THUNDER_PORT="9998"
export APPSTORE_CATALOG_PASSWORD="secure_password_123"
export APPSTORE_CATALOG_URL="https://production-dac.example.com"

# Run tests
python /path/to/test_script.py
```

**On Windows (PowerShell):**
```powershell
$env:THUNDER_HOST = "192.168.1.100"
$env:THUNDER_PORT = "9998"
$env:APPSTORE_CATALOG_PASSWORD = "secure_password_123"
$env:APPSTORE_CATALOG_URL = "https://production-dac.example.com"

# Run tests
python /path/to/test_script.py
```

**On Windows (Command Prompt):**
```cmd
set THUNDER_HOST=192.168.1.100
set THUNDER_PORT=9998
set APPSTORE_CATALOG_PASSWORD=secure_password_123
set APPSTORE_CATALOG_URL=https://production-dac.example.com

REM Run tests
python /path/to/test_script.py
```

### Loading Configuration in Python

The `ai2_0_utils.py` module provides helper functions to load configuration:

```python
from ai2_0_utils import get_ai2_setting

# Get configuration value with default
jsonrpc_port = get_ai2_setting('thunder.port', 9998)

# Get configuration from appstore-catalog
catalog_url = get_ai2_setting('appstore-catalog.url')
```

## Default Behavior

If an environment variable is not set:
1. **With default value** - Uses the default specified in the variable syntax
2. **Without default value** - May return `None` or raise an error depending on usage

**Example:**

```json
{
  "host": "${THUNDER_HOST:127.0.0.1}",      // Defaults to 127.0.0.1 if THUNDER_HOST not set
  "password": "${APPSTORE_CATALOG_PASSWORD}" // Error if APPSTORE_CATALOG_PASSWORD not set
}
```

## Configuration Hierarchy

The configuration is loaded in the following order (later values override earlier):

1. **ai_2_0_cpe.json defaults** - Default values in the config file
2. **Environment variables** - Values in system environment variables
3. **Local overrides** - Runtime modifications in code (if applicable)

## Security Best Practices

1. **Never commit sensitive credentials** to version control
2. **Always use environment variables** for passwords and tokens
3. **Rotate credentials regularly** in production environments
4. **Use vaults/secrets managers** (e.g., AWS Secrets Manager, HashiCorp Vault) in production
5. **Log configuration safely** - Don't log passwords or sensitive values
6. **Validate configuration** before using it in tests

## Example Environment Configuration File

Create a `.env` file (NOT committed to git) with your settings:

```bash
# .env file (add to .gitignore)
THUNDER_HOST=192.168.1.100
THUNDER_PORT=9998
APPSTORE_CATALOG_URL=https://production-dac.example.com
APPSTORE_CATALOG_USER=prod_user
APPSTORE_CATALOG_PASSWORD=your_secure_password
DAC_CONFIG_URL=https://production-config.example.com/cpe.json
TEST_URL_MEDIUM=https://your-test-server.com/medium_file.tar.gz
TEST_URL_LARGE=https://your-test-server.com/large_file.tar.gz
PACKAGE_MANAGER_PORT=9998
DOWNLOAD_MANAGER_PORT=9998
TEST_DOWNLOAD_DIR=/opt/CDL/
```

Load it in your shell:
```bash
# Linux/macOS
set -a
source .env
set +a

# Or using grep to export all variables
export $(grep -v '#' .env | xargs)
```

## Troubleshooting

### Issue: "TypeError: expected string or bytes-like object"

**Cause:** Port numbers are now strings in JSON and need to be converted.

**Solution:** Convert to int when needed:
```python
port = int(get_ai2_setting('thunder.port', 9998))
```

### Issue: Required variable not set

**Error:** Configuration loading fails because `APPSTORE_CATALOG_PASSWORD` is not set.

**Solution:** Set the environment variable:
```bash
export APPSTORE_CATALOG_PASSWORD="your_password"
```

### Issue: Using default values when custom values needed

**Solution:** Ensure environment variables are set before running tests:
```bash
echo $THUNDER_HOST  # Verify it's set
env | grep THUNDER  # See all THUNDER_ variables
```

## Migration from Old Configuration

If you're migrating from hardcoded values:

1. **Extract hardcoded values** from your test scripts
2. **Define environment variables** for your environment
3. **Update ai_2_0_cpe.json** to use environment variables (already done)
4. **Test with defaults** first, then override with env vars for your setup

## Configuration Template

For a new environment, use this template:

```bash
# Required
export APPSTORE_CATALOG_PASSWORD="[SET THIS]"

# Optional - defaults used if not set
export THUNDER_HOST="127.0.0.1"           # default
export THUNDER_PORT="9998"                 # default
export APPSTORE_CATALOG_URL="https://dac.dev.rdkinnovation.com"  # default

# Custom URLs for your test files
export TEST_URL_MEDIUM="https://your-server.com/medium_file.tar.gz"
export TEST_URL_LARGE="https://your-server.com/large_file.tar.gz"
```

## Further Reading

- [12-Factor App: Config](https://12factor.net/config)
- [Environment Variables Best Practices](https://12factor.net/config)
- [Secrets Management](https://docs.docker.com/engine/swarm/secrets/)
