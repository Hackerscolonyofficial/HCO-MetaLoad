#!/usr/bin/env python3
"""
HCO MetaLoad - HCO Security Framework (Simplified Termux edition)

A compact security assessment tool for authorized penetration testing & labs.

Author: Azhar / Hackers Colony
License: For authorized testing only (see LICENSE)

Usage:
  python hco_metaload.py
"""

import os
import sys
import time
import platform
import socket
import getpass
import json
import subprocess

# ---------------------------
# Colors
# ---------------------------
GREEN = "\033[32m"
BLUE = "\033[34m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# ---------------------------
# Helpers
# ---------------------------
def safe_run(cmd):
    """Run a shell command and return output (text)."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        return proc.stdout.strip()
    except Exception:
        return ""

def check_port(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((host, port)) == 0
    except Exception:
        return False

def get_logged_in_users():
    if platform.system().lower().startswith("win"):
        return ["Windows: not supported in this edition"]
    out = safe_run(["who"])
    return out.splitlines() if out else []

def get_system_uptime():
    if platform.system().lower().startswith("win"):
        return safe_run(["net", "stats", "server"]).splitlines()[0] if safe_run(["net", "stats", "server"]) else "Unknown"
    try:
        with open("/proc/uptime", "r") as f:
            s = float(f.readline().split()[0])
            days = int(s // 86400)
            hours = int((s % 86400) // 3600)
            return f"{days}d {hours}h"
    except Exception:
        return "Unknown"

def get_network_interfaces():
    try:
        return {name: {"index": idx} for idx, name in socket.if_nameindex()}
    except Exception:
        return {}

# ---------------------------
# Modules
# ---------------------------
def module_system_audit(**_):
    return {
        "system": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "user": getpass.getuser(),
        "python": platform.python_version(),
        "users_logged_in": get_logged_in_users(),
        "uptime": get_system_uptime(),
        "interfaces": get_network_interfaces(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def module_network_discovery(target="127.0.0.1", **_):
    # small service list for quick checks
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP"
    }
    open_ports = []
    for port, name in services.items():
        if check_port(target, port):
            open_ports.append({"port": port, "service": name})
    try:
        hostname = socket.gethostbyaddr(target)[0]
    except Exception:
        hostname = None
    return {
        "target": target,
        "hostname": hostname,
        "open_ports": open_ports,
        "scanned_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def module_security_assessment(**_):
    # lightweight checks — keep manual recommendations
    checks = [
        {"item": "SSH", "status": "Check if running and key-based auth is used"},
        {"item": "Firewall", "status": "Verify ufw/firewalld/iptables status"},
        {"item": "Packages", "status": "Ensure OS packages are up-to-date"}
    ]
    return {"checks": checks, "assessment_date": time.strftime("%Y-%m-%d")}

MODULES = {
    "system_audit": module_system_audit,
    "network_discovery": module_network_discovery,
    "security_assessment": module_security_assessment
}

# ---------------------------
# CLI UI
# ---------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def display_banner():
    clear()
    print(f"""{GREEN}
╔════════════════════════════════════════════════════╗
║                    HCO MetaLoad                    ║
║          Security Framework (Termux edition)        ║
╚════════════════════════════════════════════════════╝
{RESET}""")

def show_legal():
    print(f"{RED}⚠️  LEGAL NOTICE{RESET}")
    print("Use this tool ONLY on systems you own or have explicit written permission to test.")
    print("Unauthorized scanning or intrusion is illegal and may result in penalties.")
    try:
        input(f"\n{YELLOW}Press Enter to acknowledge and continue (Ctrl+C to exit){RESET}")
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        sys.exit(0)

def show_help():
    print(f"""
{BLUE}Commands:{RESET}
  {GREEN}help{RESET}                     - Show this help
  {GREEN}modules{RESET}                  - List modules
  {GREEN}use <module> [args]{RESET}      - Run a module, example:
       use network_discovery target=192.168.1.1
  {GREEN}exit{RESET}                     - Quit
""")

def list_modules():
    print(f"{BLUE}Available modules:{RESET}")
    for name in MODULES:
        print(f"  {GREEN}{name}{RESET}")

def parse_args(argstr):
    kwargs = {}
    if not argstr:
        return kwargs
    for token in argstr.split():
        if "=" in token:
            k, v = token.split("=", 1)
            kwargs[k.strip()] = v.strip()
    return kwargs

def run_module(name, args_str=""):
    if name not in MODULES:
        print(f"{RED}[!] Module not found: {name}{RESET}")
        return
    kwargs = parse_args(args_str)
    print(f"{YELLOW}[*] Running {name}...{RESET}")
    start = time.time()
    try:
        result = MODULES[name](**kwargs)
        elapsed = time.time() - start
        print(f"{GREEN}[+] Completed in {elapsed:.2f}s{RESET}")
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")

def main_loop():
    while True:
        try:
            cmd = input(f"{GREEN}hco-metaload>{RESET} ").strip()
            if not cmd:
                continue
            if cmd in ("exit", "quit"):
                print("Bye.")
                break
            if cmd == "help":
                show_help(); continue
            if cmd == "modules":
                list_modules(); continue
            if cmd.startswith("use "):
                parts = cmd.split(maxsplit=2)
                mod = parts[1]
                args = parts[2] if len(parts) > 2 else ""
                run_module(mod, args)
                continue
            print(f"{RED}Unknown command. Type 'help'.{RESET}")
        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"{RED}Unexpected error: {e}{RESET}")

def main():
    display_banner()
    show_legal()
    print(f"{YELLOW}Type 'help' to get started.{RESET}\n")
    main_loop()

if __name__ == "__main__":
    main()
