## PackageManager Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `PKG‑REQ‑001` | SHALL return the list of installed packages via listPackages |
| `PKG‑REQ‑002` | SHALL successfully install a package with valid parameters, confirm the package appears in the package list after installation, and confirm it is absent after uninstallation; SHALL handle attempting to uninstall the same package twice |
| `PKG‑REQ‑003` | SHALL return the current package state for a valid packageId and version via getPackageState, and SHALL return an error response when getPackageState is invoked with empty, invalid, mismatched, or missing parameters |
| `PKG‑REQ‑004` | SHALL return an error response when install is invoked with empty, invalid, or missing parameters |
| `PKG‑REQ‑005` | SHALL return an error response when uninstall is invoked with empty, invalid, or missing parameters |
| `PKG‑REQ‑006` | SHALL successfully lock a package with valid packageId, version, and lock reason, confirm the locked information via getLockedInfo, and successfully unlock it; SHALL return an error response when lock or unlock is invoked with empty, invalid, or missing parameter combinations |
| `PKG‑REQ‑007` | SHALL return the configuration data for a valid packageId and version via the config API, and SHALL return an error response when config is invoked with empty, invalid, or missing parameter combinations |
| `PKG‑REQ‑008` | SHALL emit the onAppInstallationStatus event during a package installation operation |
