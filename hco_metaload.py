#!/usr/bin/env python3
"""
HCO MetaLoad - APK Creator & Security Tool (Termux edition)

A tool that provides APK creation options + security assessment features.

Author: Azhar / Hackers Colony
License: For authorized testing only

Features:
- APK creation from Python scripts
- Basic security assessment tools
- Termux-compatible
"""

import os
import sys
import time
import platform
import socket
import getpass
import json
import subprocess
import shutil
from pathlib import Path

# ---------------------------
# Colors
# ---------------------------
GREEN = "\033[32m"
BLUE = "\033[34m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"

# ---------------------------
# APK Creation Functions
# ---------------------------

def check_buildozer():
    """Check if Buildozer is available for APK creation."""
    try:
        result = subprocess.run(["buildozer", "--version"], 
                              capture_output=True, text=True)
        return "Buildozer" in result.stdout
    except:
        return False

def create_basic_apk_template(project_name="MyApp", output_dir="."):
    """Create a basic Kivy app template that can be converted to APK."""
    template = f'''
import kivy
kivy.require("2.0.0")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class {project_name}App(App):
    def build(self):
        self.title = "{project_name}"
        layout = BoxLayout(orientation="vertical", padding=20)
        
        label = Label(
            text="Welcome to {project_name}",
            font_size="24sp",
            color=(0.2, 0.6, 1, 1)
        )
        
        button = Button(
            text="Click Me!",
            size_hint=(1, 0.2),
            background_color=(0.1, 0.8, 0.3, 1)
        )
        button.bind(on_press=self.on_button_click)
        
        layout.add_widget(label)
        layout.add_widget(button)
        return layout
    
    def on_button_click(self, instance):
        instance.text = "Hello from HCO MetaLoad!"

if __name__ == "__main__":
    {project_name}App().run()
'''

    main_py = os.path.join(output_dir, "main.py")
    with open(main_py, "w") as f:
        f.write(template)
    
    return main_py

def create_buildozer_spec(project_name="MyApp", package_name="com.hco.metaload"):
    """Create a basic buildozer.spec file."""
    spec_content = f'''
[app]
title = {project_name}
package.name = {package_name}
package.domain = org.hco
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.0.0
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app]
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
'''
    
    with open("buildozer.spec", "w") as f:
        f.write(spec_content)

def setup_apk_project():
    """Setup a new APK project."""
    print(f"{CYAN}[*] Setting up APK project...{RESET}")
    
    project_name = input(f"{YELLOW}Enter project name: {RESET}").strip() or "HCOApp"
    package_name = input(f"{YELLOW}Enter package name (com.example.app): {RESET}").strip() or "com.hco.metaload"
    
    project_dir = f"{project_name}_apk"
    
    try:
        # Create project directory
        os.makedirs(project_dir, exist_ok=True)
        os.chdir(project_dir)
        
        # Create main.py
        create_basic_apk_template(project_name, ".")
        
        # Create buildozer.spec
        create_buildozer_spec(project_name, package_name)
        
        print(f"{GREEN}[+] APK project created in: {project_dir}{RESET}")
        print(f"{GREEN}[+] Files created: main.py, buildozer.spec{RESET}")
        print(f"{YELLOW}[!] Next steps:{RESET}")
        print(f"   1. cd {project_dir}")
        print(f"   2. buildozer android debug")
        print(f"   3. Find APK in bin/ directory")
        
    except Exception as e:
        print(f"{RED}[!] Error creating project: {e}{RESET}")
        return False
    
    return True

def build_apk():
    """Build APK using Buildozer."""
    if not check_buildozer():
        print(f"{RED}[!] Buildozer not found!{RESET}")
        print(f"{YELLOW}[*] Install with: pkg install python buildozer{RESET}")
        return False
    
    print(f"{CYAN}[*] Building APK (this may take 10-30 minutes)...{RESET}")
    print(f"{YELLOW}[!] Make sure you have good internet connection{RESET}")
    
    try:
        # Start build process
        process = subprocess.Popen(
            ["buildozer", "android", "debug"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Stream output with progress indication
        for line in process.stdout:
            if "Downloading" in line or "Building" in line:
                print(f"{CYAN}[BUILD] {line.strip()}{RESET}")
            elif "error" in line.lower():
                print(f"{RED}[ERROR] {line.strip()}{RESET}")
            elif "warning" in line.lower():
                print(f"{YELLOW}[WARN] {line.strip()}{RESET}")
        
        process.wait()
        
        if process.returncode == 0:
            print(f"{GREEN}[+] APK built successfully!{RESET}")
            print(f"{GREEN}[+] APK location: bin/{RESET}")
            return True
        else:
            print(f"{RED}[!] APK build failed{RESET}")
            return False
            
    except Exception as e:
        print(f"{RED}[!] Build error: {e}{RESET}")
        return False

# ---------------------------
# Security Modules (Optional)
# ---------------------------

def module_system_info(**_):
    """Basic system information."""
    return {
        "system": platform.platform(),
        "hostname": socket.gethostname(),
        "user": getpass.getuser(),
        "python_version": platform.python_version(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def check_port_scanner(target="127.0.0.1", **_):
    """Simple port checker."""
    ports = [21, 22, 80, 443, 8080]
    results = {}
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                results[port] = "OPEN" if s.connect_ex((target, port)) == 0 else "CLOSED"
        except:
            results[port] = "ERROR"
    return {"target": target, "ports": results}

MODULES = {
    "system_info": module_system_info,
    "port_check": check_port_scanner
}

# ---------------------------
# CLI Interface
# ---------------------------

def display_banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""{MAGENTA}
╔════════════════════════════════════════════════════╗
║              HCO MetaLoad - APK Creator            ║
║                 & Security Toolkit                 ║
║                                                    ║
║    [1] Create APK from Python Script              ║
║    [2] Build APK with Buildozer                   ║
║    [3] Security Tools                             ║
║    [4] Exit                                       ║
╚════════════════════════════════════════════════════╝
{RESET}""")

def show_apk_menu():
    print(f"""
{CYAN}APK Creation Options:{RESET}

{GREEN}[1]{RESET} Setup new APK project
{BLUE}[2]{RESET} Build APK (requires existing project)
{YELLOW}[3]{RESET} Check Buildozer installation
{RED}[4]{RESET} Back to main menu
""")

def show_security_menu():
    print(f"""
{YELLOW}Security Tools:{RESET}

{GREEN}[1]{RESET} System Information
{BLUE}[2]{RESET} Port Scanner
{CYAN}[3]{RESET} List all modules
{RED}[4]{RESET} Back to main menu
""")

def apk_creation_flow():
    """Handle APK creation menu."""
    while True:
        show_apk_menu()
        choice = input(f"{GREEN}apk> {RESET}").strip()
        
        if choice == "1":
            setup_apk_project()
            input(f"{YELLOW}Press Enter to continue...{RESET}")
            
        elif choice == "2":
            if not os.path.exists("buildozer.spec"):
                print(f"{RED}[!] No buildozer.spec found in current directory{RESET}")
                print(f"{YELLOW}[*] Run option 1 first or cd to your project directory{RESET}")
            else:
                build_apk()
            input(f"{YELLOW}Press Enter to continue...{RESET}")
            
        elif choice == "3":
            if check_buildozer():
                print(f"{GREEN}[+] Buildozer is installed and ready{RESET}")
            else:
                print(f"{RED}[!] Buildozer not found{RESET}")
                print(f"{YELLOW}[*] Install with: pkg install python buildozer{RESET}")
            input(f"{YELLOW}Press Enter to continue...{RESET}")
            
        elif choice == "4":
            break
        else:
            print(f"{RED}[!] Invalid choice{RESET}")

def security_tools_flow():
    """Handle security tools menu."""
    while True:
        show_security_menu()
        choice = input(f"{GREEN}security> {RESET}").strip()
        
        if choice == "1":
            result = module_system_info()
            print(json.dumps(result, indent=2))
            input(f"{YELLOW}Press Enter to continue...{RESET}")
            
        elif choice == "2":
            target = input(f"{YELLOW}Enter target (default: 127.0.0.1): {RESET}").strip() or "127.0.0.1"
            result = check_port_scanner(target=target)
            print(json.dumps(result, indent=2))
            input(f"{YELLOW}Press Enter to continue...{RESET}")
            
        elif choice == "3":
            print(f"{CYAN}Available modules:{RESET}")
            for name in MODULES:
                print(f"  {GREEN}{name}{RESET}")
            input(f"{YELLOW}Press Enter to continue...{RESET}")
            
        elif choice == "4":
            break
        else:
            print(f"{RED}[!] Invalid choice{RESET}")

def main_menu():
    """Main menu loop."""
    while True:
        display_banner()
        print(f"{CYAN}Main Menu:{RESET}")
        print(f"{GREEN}[1]{RESET} APK Creation Tools")
        print(f"{BLUE}[2]{RESET} Security Assessment Tools")
        print(f"{RED}[3]{RESET} Exit")
        
        choice = input(f"\n{GREEN}hco-metaload> {RESET}").strip()
        
        if choice == "1":
            apk_creation_flow()
        elif choice == "2":
            security_tools_flow()
        elif choice == "3":
            print(f"{GREEN}Thank you for using HCO MetaLoad!{RESET}")
            break
        else:
            print(f"{RED}[!] Please choose 1, 2, or 3{RESET}")
            time.sleep(1)

def main():
    """Main entry point."""
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Program interrupted by user.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")

if __name__ == "__main__":
    main()
