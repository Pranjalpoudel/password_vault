"""
Quick start guide for Secure Password Vault.
This script handles the setup process.
"""

import subprocess
import sys
import os

def run_command(command, description):
"""Run a shell command and report status."""
print(f"\n{description}...")
try:
result = subprocess.run(command, shell=True, capture_output=True, text=True)
if result.returncode == 0:
print(f"✓ {description} completed successfully")
return True
else:
print(f"✗ {description} failed")
if result.stderr:
print(f" Error: {result.stderr[:200]}")
return False
except Exception as e:
print(f"✗ {description} error: {e}")
return False

def main():
"""Run setup steps."""
print("=" _ 60)
print("Secure Password Vault - Quick Start Setup")
print("=" _ 60)

    # Step 1: Install dependencies
    print("\nStep 1: Installing dependencies...")
    run_command(f"{sys.executable} -m pip install -q -r requirements.txt", "Dependency installation")

    # Step 2: Initialize database
    print("\nStep 2: Initialize PostgreSQL database...")
    print("Run the following command:")
    print("  python setup_database.py")
    print("\nThen fill in your PostgreSQL credentials when prompted.")

    # Step 3: Launch application
    print("\nStep 3: Launch the application...")
    print("Run the following command:")
    print("  python main.py")

    print("\n" + "=" * 60)
    print("Setup complete! Follow the steps above to get started.")
    print("=" * 60)

if **name** == "**main**":
main()
