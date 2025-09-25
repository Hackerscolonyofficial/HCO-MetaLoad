#!/usr/bin/env python3
"""
HCO-MetaLoad - Metasploit-like Framework (Termux Edition)

A Metasploit-style framework for security testing and penetration testing.

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
        # Method 1: Try using am (Activity Manager) to open YouTube app
        result = subprocess.run([
            'am', 'start', 
            '-a', 'android.intent.action.VIEW',
            '-d', 'https://youtube.com/@hackers_colony_tech'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        
        # Method 2: Try using termux-open-url
        result = subprocess.run([
            'termux-open-url', 
            'https://youtube.com/@hackers_colony_tech'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
            
        # Method 3: Try using am with YouTube package name
        result = subprocess.run([
            'am', 'start',
            '-n', 'com.google.android.youtube/com.google.android.apps.youtube.app.WatchWhileActivity',
            '-a', 'android.intent.action.VIEW',
            '-d', 'https://youtube.com/@hackers_colony_tech'
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
    
    # Countdown: 9.8.7.6.5.4.3.2.1
    countdown_numbers = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    # Print the countdown string first
    countdown_str = ".".join(map(str, countdown_numbers))
    print(f"{MAGENTA}{countdown_str}{RESET}")
    
    # Animated countdown
    for number in countdown_numbers:
        print(f"{RED}{number}{RESET}", end=".", flush=True)
        time.sleep(0.5)
    
    print(f"\n\n{GREEN}Opening YouTube app...{RESET}")
    time.sleep(2)
    
    # Open YouTube app
    if open_youtube_app():
        print(f"{GREEN}✓ YouTube app opened successfully!{RESET}")
        print(f"{YELLOW}Please subscribe to our channel and return to Termux.{RESET}")
    else:
        print(f"{RED}✗ Could not open YouTube app automatically.{RESET}")
        print(f"{YELLOW}Please manually open YouTube and visit:{RESET}")
        print(f"{CYAN}https://youtube.com/@hackers_colony_tech{RESET}")
    
    # Wait for user to return
    print(f"\n{YELLOW}" + "="*50 + RESET)
    try:
        input(f"\n{YELLOW}After subscribing, press Enter to continue...{RESET}")
    except KeyboardInterrupt:
        print(f"\n{RED}Operation cancelled.{RESET}")
        sys.exit(1)

def show_welcome_banner():
    """Display HCO MetaLoad by Azhar in green inside red box."""
    os.system("clear" if os.name != "nt" else "cls")
    
    # Red box with green text - no ASCII art
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
        super().__init__(**kwargs)
        self.type = "exploit"
    
    def run(self, **kwargs):
        raise NotImplementedError

class AuxiliaryModule(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "auxiliary"
    
    def run(self, **kwargs):
        raise NotImplementedError

# ---------------------------
# Actual Modules
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
                "PORTS": {"required": False, "description": "Ports to scan (default: 1-100)"},
                "THREADS": {"required": False, "description": "Number of threads (default: 5)"}
            }
        )
    
    def run(self, **kwargs):
        target = kwargs.get("RHOSTS", "127.0.0.1")
        ports_range = kwargs.get("PORTS", "1-100")
        threads = int(kwargs.get("THREADS", 5))
        
        print(f"{CYAN}[*] Scanning {target} ports {ports_range}{RESET}")
        
        if "-" in ports_range:
            start, end = map(int, ports_range.split("-"))
            ports = list(range(start, end + 1))
        else:
            ports = [int(p.strip()) for p in ports_range.split(",")]
        
        open_ports = []
        
        def scan_port(port):
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
        
        # Simple scanning (threading simplified for Termux)
        for port in ports[:50]:  # Limit to first 50 ports for speed
            scan_port(port)
            time.sleep(0.1)  # Small delay to avoid overwhelming
        
        return {
            "target": target,
            "open_ports": sorted(open_ports),
            "total_scanned": len(ports[:50]),
            "scan_type": "TCP Connect"
        }
    
    def get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 443: "HTTPS", 3389: "RDP"
        }
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
            "Current User": os.getenv("USER", "Unknown"),
            "Working Directory": os.getcwd(),
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"{CYAN}[*] Gathering system information...{RESET}")
        for key, value in info.items():
            print(f"{GREEN}[+] {key}: {value}{RESET}")
        
        return info

class NetworkDiscoverer(AuxiliaryModule):
    def __init__(self):
        super().__init__(
            name="network_discovery",
            description="Network host discovery",
            author="HCO Team",
            references=[],
            options={
                "SUBNET": {"required": True, "description": "Subnet to scan (e.g., 192.168.1.0/24)"}
            }
        )
    
    def run(self, **kwargs):
        subnet = kwargs.get("SUBNET", "192.168.1.0/24")
        print(f"{CYAN}[*] Discovering hosts in {subnet}{RESET}")
        
        alive_hosts = []
        
        if "/24" in subnet:
            base_ip = subnet.replace("/24", "")
            for i in range(1, 10):  # Scan only first 10 for speed
                ip = f"{base_ip}.{i}"
                if self.ping_host(ip):
                    alive_hosts.append(ip)
                    print(f"{GREEN}[+] Host alive: {ip}{RESET}")
        
        return {
            "subnet": subnet,
            "alive_hosts": alive_hosts,
            "discovery_method": "Ping Sweep"
        }
    
    def ping_host(self, ip):
        try:
            command = ["ping", "-c", "1", "-W", "1", ip]
            result = subprocess.run(command, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

class BasicExploit(ExploitModule):
    def __init__(self):
        super().__init__(
            name="basic_http_exploit",
            description="Basic HTTP vulnerability test",
            author="HCO Team",
            references=[],
            options={
                "RHOST": {"required": True, "description": "Target host"},
                "RPORT": {"required": False, "description": "Target port (default: 80)"}
            }
        )
    
    def run(self, **kwargs):
        target = kwargs.get("RHOST", "127.0.0.1")
        port = int(kwargs.get("RPORT", 80))
        
        print(f"{CYAN}[*] Testing {target}:{port}{RESET}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, port))
            
            request = f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n"
            sock.send(request.encode())
            
            response = sock.recv(1024).decode()
            sock.close()
            
            if "200 OK" in response:
                print(f"{GREEN}[+] Server responded with 200 OK{RESET}")
                return {"status": "accessible", "response_code": 200}
            else:
                print(f"{YELLOW}[!] Server response: {response.splitlines()[0]}{RESET}")
                return {"status": "tested", "response": response.splitlines()[0]}
                
        except Exception as e:
            print(f"{RED}[-] Connection failed: {e}{RESET}")
            return {"status": "failed", "error": str(e)}

# ---------------------------
# Framework Core
# ---------------------------

class HCOMetaLoadFramework:
    def __init__(self):
        self.modules = {}
        self.current_module = None
        self.module_options = {}
        self.load_modules()
    
    def load_modules(self):
        """Load all available modules"""
        self.modules = {
            "auxiliary/port_scanner": PortScanner(),
            "auxiliary/system_info": SystemInfoGatherer(),
            "auxiliary/network_discovery": NetworkDiscoverer(),
            "exploit/basic_http": BasicExploit(),
        }
    
    def show_banner(self):
        """Show main framework banner"""
        show_welcome_banner()
        print(f"{GREEN}[+] {len(self.modules)} modules loaded{RESET}")
        print(f"{YELLOW}[*] Type 'help' for available commands{RESET}\n")
    
    def show_modules(self, module_type=None):
        """List available modules"""
        print(f"\n{CYAN}Available Modules{RESET}")
        print("=" * 50)
        
        for module_path, module in self.modules.items():
            if module_type and not module_path.startswith(module_type):
                continue
            
            type_color = GREEN if module.type == "exploit" else BLUE
            print(f"  {type_color}{module_path:<25}{RESET} {module.description}")
        
        print(f"\n{YELLOW}Use: use <module_path>{RESET}")
    
    def use_module(self, module_path):
        """Select a module to use"""
        if module_path not in self.modules:
            print(f"{RED}[!] Module not found: {module_path}{RESET}")
            return False
        
        self.current_module = self.modules[module_path]
        self.module_options = self.current_module.options.copy()
        
        print(f"{GREEN}[+] Using module: {module_path}{RESET}")
        self.show_options()
        return True
    
    def show_options(self):
        """Show module options"""
        if not self.current_module:
            print(f"{RED}[!] No module selected{RESET}")
            return
        
        print(f"\n{CYAN}Module options ({self.current_module.name}):{RESET}")
        print("-" * 40)
        
        for opt_name, opt_info in self.module_options.items():
            required = "yes" if opt_info.get("required", False) else "no"
            current_value = opt_info.get("value", "")
            print(f"   {GREEN}{opt_name:<10}{RESET} {current_value:<10} {opt_info.get('description', '')}")
    
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
        
        for opt_name, opt_info in self.module_options.items():
            if opt_info.get("required", False) and not opt_info.get("value"):
                print(f"{RED}[!] Required option not set: {opt_name}{RESET}")
                return
        
        params = {}
        for opt_name, opt_info in self.module_options.items():
            if opt_info.get("value"):
                params[opt_name] = opt_info["value"]
        
        print(f"{CYAN}[*] Running module...{RESET}")
        try:
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
    {YELLOW}help{RESET}    - Show this help
    {YELLOW}exit{RESET}    - Exit framework
    {YELLOW}clear{RESET}   - Clear screen

{GREEN}Module Commands{RESET}
    {YELLOW}show modules{RESET}    - List all modules
    {YELLOW}use <module>{RESET}    - Select module
    {YELLOW}back{RESET}           - Deselect module
    {YELLOW}show options{RESET}   - Show options
    {YELLOW}set <opt> <val>{RESET} - Set option
    {YELLOW}run{RESET}            - Execute module

{GREEN}Examples{RESET}
    {CYAN}use auxiliary/port_scanner{RESET}
    {CYAN}set RHOSTS 192.168.1.1{RESET}
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
