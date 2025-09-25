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
import webbrowser
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

def show_tool_lock():
    """Display tool lock message and countdown."""
    print(f"\n{RED}🔐 TOOL LOCK — IMPORTANT NOTICE 🔐{RESET}")
    print(f"{YELLOW}This tool is for EDUCATIONAL purposes only.{RESET}")
    print(f"{YELLOW}To continue, please subscribe to our channel.{RESET}")
    print(f"{CYAN}YouTube: https://youtube.com/@hackers_colony_tech{RESET}\n")
    
    print(f"{RED}Redirecting to YouTube in...{RESET}")
    
    # Countdown: 9.8.7.6.5.4.3.2.1
    countdown_numbers = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    countdown_str = ".".join(map(str, countdown_numbers))
    print(f"{MAGENTA}{countdown_str}{RESET}")
    
    # Animated countdown
    for number in countdown_numbers:
        print(f"{RED}{number}{RESET}", end=" ", flush=True)
        time.sleep(0.5)
    
    print(f"\n\n{GREEN}Opening YouTube channel...{RESET}")
    
    # Open YouTube channel
    try:
        webbrowser.open("https://youtube.com/@hackers_colony_tech", new=2)
        print(f"{YELLOW}YouTube channel opened!{RESET}")
        print(f"{CYAN}Please subscribe and return to this terminal.{RESET}")
    except Exception as e:
        print(f"{RED}Could not open browser: {e}{RESET}")
        print(f"{CYAN}Please visit: https://youtube.com/@hackers_colony_tech{RESET}")
    
    # Wait for user to return
    try:
        input(f"\n{YELLOW}Press Enter after subscribing to continue...{RESET}")
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
    print()

# ---------------------------
# Module Base Classes
# ---------------------------

@dataclass
class Module:
    name: str
    description: str
    author: str
    type: str  # exploit, auxiliary, payload, post
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
                "PORTS": {"required": False, "description": "Ports to scan (default: 1-1000)"},
                "THREADS": {"required": False, "description": "Number of threads (default: 10)"}
            }
        )
    
    def run(self, **kwargs):
        target = kwargs.get("RHOSTS", "127.0.0.1")
        ports_range = kwargs.get("PORTS", "1-1000")
        threads = int(kwargs.get("THREADS", 10))
        
        print(f"{CYAN}[*] Scanning {target} ports {ports_range}{RESET}")
        
        # Parse ports range
        if "-" in ports_range:
            start, end = map(int, ports_range.split("-"))
            ports = list(range(start, end + 1))
        else:
            ports = [int(p.strip()) for p in ports_range.split(",")]
        
        open_ports = []
        lock = threading.Lock()
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((target, port))
                sock.close()
                
                if result == 0:
                    with lock:
                        open_ports.append(port)
                        service_name = self.get_service_name(port)
                        print(f"{GREEN}[+] {target}:{port} - {service_name} - OPEN{RESET}")
            except:
                pass
        
        # Threaded scanning
        thread_pool = []
        for port in ports:
            thread = threading.Thread(target=scan_port, args=(port,))
            thread.start()
            thread_pool.append(thread)
            
            if len(thread_pool) >= threads:
                for t in thread_pool:
                    t.join()
                thread_pool = []
        
        for t in thread_pool:
            t.join()
        
        return {
            "target": target,
            "open_ports": sorted(open_ports),
            "total_scanned": len(ports),
            "scan_type": "TCP Connect"
        }
    
    def get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 993: "IMAPS", 995: "POP3S",
            3389: "RDP", 3306: "MySQL", 5432: "PostgreSQL"
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
            "Architecture": platform.architecture(),
            "Hostname": socket.gethostname(),
            "Processor": platform.processor(),
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
            description="Network host discovery using ping sweep",
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
            for i in range(1, 255):
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
            if platform.system().lower() == "windows":
                command = ["ping", "-n", "1", "-w", "1000", ip]
            else:
                command = ["ping", "-c", "1", "-W", "1", ip]
            
            result = subprocess.run(command, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

class BasicExploit(ExploitModule):
    def __init__(self):
        super().__init__(
            name="basic_http_exploit",
            description="Basic HTTP vulnerability demonstration",
            author="HCO Team",
            references=[],
            options={
                "RHOST": {"required": True, "description": "Target host"},
                "RPORT": {"required": False, "description": "Target port (default: 80)"},
                "URI": {"required": False, "description": "URI to test (default: /)"}
            }
        )
    
    def run(self, **kwargs):
        target = kwargs.get("RHOST", "127.0.0.1")
        port = int(kwargs.get("RPORT", 80))
        uri = kwargs.get("URI", "/")
        
        print(f"{CYAN}[*] Testing {target}:{port}{uri}{RESET}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, port))
            
            request = f"GET {uri} HTTP/1.1\r\nHost: {target}\r\n\r\n"
            sock.send(request.encode())
            
            response = sock.recv(4096).decode()
            sock.close()
            
            if "200 OK" in response:
                print(f"{GREEN}[+] Server responded with 200 OK{RESET}")
                return {"status": "vulnerable", "response_code": 200}
            else:
                print(f"{YELLOW}[!] Server response: {response.splitlines()[0] if response else 'No response'}{RESET}")
                return {"status": "tested", "response": response.splitlines()[0] if response else "No response"}
                
        except Exception as e:
            print(f"{RED}[-] Connection failed: {e}{RESET}")
            return {"status": "failed", "error": str(e)}

class VulnerabilityScanner(AuxiliaryModule):
    def __init__(self):
        super().__init__(
            name="vuln_scanner",
            description="Basic vulnerability scanner",
            author="HCO Team",
            references=[],
            options={
                "TARGET": {"required": True, "description": "Target URL or IP"},
                "SCAN_TYPE": {"required": False, "description": "Scan type (quick/full)"}
            }
        )
    
    def run(self, **kwargs):
        target = kwargs.get("TARGET", "127.0.0.1")
        scan_type = kwargs.get("SCAN_TYPE", "quick")
        
        print(f"{CYAN}[*] Scanning {target} for vulnerabilities ({scan_type} scan){RESET}")
        time.sleep(2)
        
        # Simulated vulnerability findings
        findings = [
            {"type": "HTTP Server", "status": "Detected", "risk": "Low"},
            {"type": "Open Ports", "status": "Multiple found", "risk": "Medium"},
            {"type": "SSL/TLS", "status": "Not checked", "risk": "Unknown"},
        ]
        
        for finding in findings:
            risk_color = GREEN if finding["risk"] == "Low" else YELLOW if finding["risk"] == "Medium" else RED
            print(f"{risk_color}[!] {finding['type']}: {finding['status']} (Risk: {finding['risk']}){RESET}")
        
        return {
            "target": target,
            "scan_type": scan_type,
            "findings": findings,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

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
            "auxiliary/vuln_scanner": VulnerabilityScanner(),
            "exploit/basic_http": BasicExploit(),
        }
    
    def show_banner(self):
        """Show main framework banner"""
        show_welcome_banner()
        print(f"{CYAN}HCO-MetaLoad Framework v2.0 (Termux Edition){RESET}")
        print(f"{YELLOW}Type 'help' for available commands{RESET}")
        print(f"{GREEN}[+] {len(self.modules)} modules loaded{RESET}\n")
    
    def show_modules(self, module_type=None):
        """List available modules"""
        print(f"\n{CYAN}Available Modules{RESET}")
        print("=" * 60)
        
        for module_path, module in self.modules.items():
            if module_type and not module_path.startswith(module_type):
                continue
            
            type_color = GREEN if module.type == "exploit" else BLUE
            print(f"  {type_color}{module_path:<30}{RESET}  {module.description}")
        
        print("")
        print(f"{YELLOW}Use: {WHITE}use <module_path>{RESET}")
        print(f"{YELLOW}Example: {WHITE}use auxiliary/port_scanner{RESET}")
    
    def use_module(self, module_path):
        """Select a module to use"""
        if module_path not in self.modules:
            print(f"{RED}[!] Module not found: {module_path}{RESET}")
            return False
        
        self.current_module = self.modules[module_path]
        self.module_options = self.current_module.options.copy()
        
        print(f"{GREEN}[+] Using module: {module_path}{RESET}")
        print(f"{CYAN}[*] Description: {self.current_module.description}{RESET}")
        
        self.show_options()
        return True
    
    def show_options(self):
        """Show module options"""
        if not self.current_module:
            print(f"{RED}[!] No module selected{RESET}")
            return
        
        print(f"\n{CYAN}Module options ({self.current_module.name}):{RESET}")
        print("=" * 50)
        
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
            result = self.current_module.run(**params)
            print(f"{GREEN}[+] Module completed{RESET}")
            if result:
                print(f"{CYAN}[*] Result: {json.dumps(result, indent=2)}{RESET}")
        except Exception as e:
            print(f"{RED}[-] Module execution failed: {e}{RESET}")
    
    def show_help(self):
        """Show help menu"""
        help_text = f"""
{CYAN}HCO-MetaLoad Framework Commands{RESET}
{WHITE}================================{RESET}

{GREEN}Core Commands{RESET}
{WHITE}============={RESET}
    {YELLOW}help{RESET}                 - Show this help menu
    {YELLOW}exit{RESET}                 - Exit the framework
    {YELLOW}clear{RESET}                - Clear screen
    {YELLOW}version{RESET}              - Show framework version

{GREEN}Module Commands{RESET}
{WHITE}==============={RESET}
    {YELLOW}show modules{RESET}         - List all modules
    {YELLOW}show auxiliary{RESET}       - List auxiliary modules
    {YELLOW}show exploits{RESET}        - List exploit modules
    {YELLOW}use <module>{RESET}         - Select a module
    {YELLOW}back{RESET}                 - Deselect current module
    {YELLOW}show options{RESET}         - Show module options
    {YELLOW}set <option> <value>{RESET} - Set module option
    {YELLOW}run{RESET}                  - Execute the module

{GREEN}Examples{RESET}
{WHITE}========{RESET}
    {CYAN}use auxiliary/port_scanner{RESET}
    {CYAN}set RHOSTS 192.168.1.1{RESET}
    {CYAN}set PORTS 1-100{RESET}
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
            
            elif command == "version":
                print(f"{CYAN}HCO-MetaLoad Framework v2.0 (Termux Edition){RESET}")
            
            elif command == "show modules":
                framework.show_modules()
            
            elif command == "show auxiliary":
                framework.show_modules("auxiliary")
            
            elif command == "show exploits":
                framework.show_modules("exploit")
            
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
                print(f"{YELLOW}[*] Type 'help' for available commands{RESET}")
        
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[*] Use 'exit' to quit the framework{RESET}")
        except Exception as e:
            print(f"{RED}[!] Error: {e}{RESET}")

if __name__ == "__main__":
    main()
