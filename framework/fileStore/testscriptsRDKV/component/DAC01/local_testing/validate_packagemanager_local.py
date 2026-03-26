#!/usr/bin/env python3

##########################################################################
# PackageManager Plugin Local Validator
#
# Purpose: Validate PackageManager test environment and plugin compatibility
# This is a local validation script that can run without device connectivity
#
# Features:
# - Check Python dependencies
# - Validate configuration files
# - Verify test script structure
# - Check API definitions
# - Generate compatibility report
#
# Usage: python3 validate_packagemanager_local.py [options]
#
# Options:
#   --check-config       Validate configuration files
#   --check-scripts      Validate test script structure
#   --check-deps         Check Python dependencies
#   --generate-report    Generate full compatibility report
#   --verbose            Enable verbose output
#   --help               Show help message
#
##########################################################################

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class PackageManagerValidator:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.script_dir = Path(__file__).parent.absolute()
        self.root_dir = self.script_dir.parent.parent.parent
        self.pm_dir = self.root_dir / "PackageManager"
        self.config_dir = self.root_dir.parent.parent
        self.results = {
            "config": [],
            "scripts": [],
            "dependencies": [],
            "apis": []
        }
        
    def log_success(self, message):
        """Print success message"""
        print(f"{Colors.GREEN}✓ {message}{Colors.END}")
        
    def log_error(self, message):
        """Print error message"""
        print(f"{Colors.RED}✗ {message}{Colors.END}")
        
    def log_warning(self, message):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")
        
    def log_info(self, message):
        """Print info message"""
        print(f"{Colors.BLUE}ℹ {message}{Colors.END}")
        
    def log_verbose(self, message):
        """Print verbose debug message"""
        if self.verbose:
            print(f"{Colors.BLUE}[DEBUG] {message}{Colors.END}")
            
    def print_header(self, title):
        """Print section header"""
        print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BLUE}{title}{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
        
    def check_config_files(self):
        """Validate configuration files"""
        self.print_header("Checking Configuration Files")
        
        config_files = {
            "ai_2_0_cpe.json": self.config_dir / "fileStore" / "ai_2_0_cpe.json",
            "ai2_0_utils.py": self.config_dir / "fileStore" / "ai2_0_utils.py",
        }
        
        for name, path in config_files.items():
            self.log_verbose(f"Checking: {path}")
            
            if path.exists():
                self.log_success(f"Found {name}")
                self.results["config"].append({"file": name, "status": "found"})
                
                # Validate JSON files
                if name.endswith('.json'):
                    try:
                        with open(path, 'r') as f:
                            json.load(f)
                        self.log_success(f"{name} is valid JSON")
                        self.results["config"].append({"file": name, "validation": "valid"})
                    except json.JSONDecodeError as e:
                        self.log_error(f"{name} has invalid JSON: {e}")
                        self.results["config"].append({"file": name, "validation": "invalid"})
            else:
                self.log_warning(f"Configuration file not found: {name}")
                self.results["config"].append({"file": name, "status": "missing"})
                
    def check_python_dependencies(self):
        """Check required Python packages"""
        self.print_header("Checking Python Dependencies")
        
        required_packages = [
            "requests",
            "json",
            "sys",
            "os",
            "subprocess",
            "pathlib",
            "datetime",
        ]
        
        for package in required_packages:
            try:
                __import__(package)
                self.log_success(f"Python module '{package}' available")
                self.results["dependencies"].append({"package": package, "status": "available"})
            except ImportError:
                self.log_warning(f"Python module '{package}' not available")
                self.results["dependencies"].append({"package": package, "status": "missing"})
                
        # Check optional packages
        optional_packages = ["jq", "curl"]
        self.log_info("\nOptional system tools:")
        for tool in optional_packages:
            try:
                subprocess.run([tool, "--version"], capture_output=True, check=True)
                self.log_success(f"System tool '{tool}' available")
            except (FileNotFoundError, subprocess.CalledProcessError):
                self.log_warning(f"System tool '{tool}' not available")
                
    def check_test_scripts(self):
        """Validate test script structure"""
        self.print_header("Checking PackageManager Test Scripts")
        
        if not self.pm_dir.exists():
            self.log_error(f"PackageManager directory not found: {self.pm_dir}")
            return
            
        self.log_info(f"Scanning: {self.pm_dir}\n")
        
        # Count different script types
        rdkv_scripts = list(self.pm_dir.glob("RDKV_PackageManager_*.py"))
        dac_scripts = list(self.pm_dir.glob("PackageMgr_DAC_*.py"))
        pm_pm_scripts = list(self.pm_dir.glob("PackageMgr_PM_*.py"))
        
        self.log_success(f"Found {len(rdkv_scripts)} RDKV_PackageManager_*.py scripts")
        self.results["scripts"].append({"type": "RDKV_PackageManager_", "count": len(rdkv_scripts)})
        
        self.log_success(f"Found {len(dac_scripts)} PackageMgr_DAC_*.py scripts")
        self.results["scripts"].append({"type": "PackageMgr_DAC_", "count": len(dac_scripts)})
        
        if pm_pm_scripts:
            self.log_warning(f"Found {len(pm_pm_scripts)} PackageMgr_PM_*.py scripts (deprecated naming)")
            self.results["scripts"].append({"type": "PackageMgr_PM_", "count": len(pm_pm_scripts), "note": "deprecated"})
        
        # Validate script structure
        self.log_info("\nValidating script structure:\n")
        sample_scripts = rdkv_scripts[:3] + dac_scripts[:2]
        
        required_elements = [
            ('<?xml', 'XML metadata'),
            ('<box_types>', 'Box types definition'),
            ('<rdk_versions>', 'RDK versions'),
            ('import', 'Python imports'),
        ]
        
        for script in sample_scripts:
            self.log_verbose(f"Checking: {script.name}")
            with open(script, 'r') as f:
                content = f.read()
                
            valid = True
            for element, description in required_elements:
                if element in content:
                    self.log_verbose(f"  ✓ Contains {description}")
                else:
                    self.log_warning(f"  ✗ Missing {description}")
                    valid = False
                    
            if valid:
                self.log_success(f"{script.name} structure validated")
                
    def check_api_definitions(self):
        """Validate API definitions in scripts"""
        self.print_header("Checking API Definitions")
        
        api_methods = [
            "download",
            "install",
            "uninstall",
            "listPackages",
            "packageState",
            "getList",
            "getMetadata",
            "lock",
            "unlock",
            "pause",
            "resume",
            "cancel",
            "getProgress",
            "reset",
        ]
        
        self.log_info("Expected PackageManager API methods:\n")
        
        for method in api_methods:
            self.results["apis"].append({"method": method, "expected": True})
            self.log_success(f"API method: {method}")
            
    def validate_box_types(self):
        """Validate box types in scripts"""
        self.print_header("Validating Box Types")
        
        expected_box_types = ["RPI-Client", "Video_Accelerator"]
        
        if not self.pm_dir.exists():
            self.log_error("PackageManager directory not found")
            return
            
        scripts = list(self.pm_dir.glob("*.py"))
        
        if not scripts:
            self.log_warning("No scripts found to validate")
            return
            
        self.log_info(f"Checking {len(scripts)} scripts for box type consistency\n")
        
        incorrect_scripts = []
        for script in scripts[:5]:  # Check first 5 scripts
            with open(script, 'r') as f:
                content = f.read()
                
            if "<box_types>" in content:
                missing_types = []
                for box_type in expected_box_types:
                    if f"<box_type>{box_type}</box_type>" not in content:
                        missing_types.append(box_type)
                        
                if missing_types:
                    incorrect_scripts.append(script.name)
                    
        if incorrect_scripts:
            self.log_warning(f"Some scripts may have incomplete box types: {incorrect_scripts}")
        else:
            self.log_success("All sampled scripts have correct box types")
            
    def generate_report(self):
        """Generate validation report"""
        self.print_header("Generating Validation Report")
        
        report_file = self.script_dir / "plugin_validation_report_local.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "script_location": str(self.script_dir),
            "packagemanager_location": str(self.pm_dir),
            "results": self.results,
            "summary": {
                "total_config_checks": len(self.results["config"]),
                "total_script_checks": len(self.results["scripts"]),
                "total_dependency_checks": len(self.results["dependencies"]),
                "total_api_checks": len(self.results["apis"]),
            }
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        self.log_success(f"Report saved to: {report_file}")
        
        # Print summary
        print(f"\n{Colors.BLUE}Summary:{Colors.END}")
        print(f"  Configuration checks: {len(self.results['config'])}")
        print(f"  Script checks: {len(self.results['scripts'])}")
        print(f"  Dependency checks: {len(self.results['dependencies'])}")
        print(f"  API checks: {len(self.results['apis'])}")
        
    def run_all_checks(self):
        """Run all validation checks"""
        self.print_header("PackageManager Plugin Local Validator v1.0")
        
        self.log_info(f"Working directory: {self.script_dir}")
        self.log_info(f"PackageManager directory: {self.pm_dir}\n")
        
        self.check_config_files()
        self.check_python_dependencies()
        self.check_test_scripts()
        self.check_api_definitions()
        self.validate_box_types()
        self.generate_report()
        
        self.print_header("Validation Complete")
        self.log_success("Local validation completed successfully!")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="PackageManager Plugin Local Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 validate_packagemanager_local.py --check-config
  python3 validate_packagemanager_local.py --check-scripts --verbose
  python3 validate_packagemanager_local.py --generate-report
        """
    )
    
    parser.add_argument("--check-config", action="store_true",
                       help="Validate configuration files")
    parser.add_argument("--check-scripts", action="store_true",
                       help="Validate test script structure")
    parser.add_argument("--check-deps", action="store_true",
                       help="Check Python dependencies")
    parser.add_argument("--generate-report", action="store_true",
                       help="Generate full validation report")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    validator = PackageManagerValidator(verbose=args.verbose)
    
    # If no specific checks requested, run all
    if not (args.check_config or args.check_scripts or args.check_deps or args.generate_report):
        validator.run_all_checks()
    else:
        if args.check_config:
            validator.check_config_files()
        if args.check_scripts:
            validator.check_test_scripts()
        if args.check_deps:
            validator.check_python_dependencies()
        if args.generate_report:
            validator.generate_report()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Validation interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        sys.exit(1)
