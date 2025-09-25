HCO-MetaLoad 🔐

https://img.shields.io/badge/HCO--MetaLoad-v2.0-red
https://img.shields.io/badge/Python-3.7%2B-blue
https://img.shields.io/badge/Platform-Termux-green
https://img.shields.io/badge/License-Educational%20Use-orange
https://img.shields.io/badge/Style-Metasploit%20Like-purple

A professional Metasploit-like penetration testing framework for Termux with payload generation capabilities. Designed for authorized security testing and educational purposes.

"The only secure system is one that is powered off, cast in a block of concrete and sealed in a lead-lined room with armed guards." - Gene Spafford

---

⚠️ DISCLAIMER

LEGAL WARNING

This tool is developed for EDUCATIONAL PURPOSES ONLY.

· 🚫 DO NOT use against systems you don't own or lack explicit written permission to test
· 🚫 DO NOT use for illegal activities
· 🚫 DO NOT distribute malicious payloads
· ✅ ONLY USE in authorized lab environments
· ✅ ONLY USE for learning cybersecurity concepts
· ✅ ALWAYS GET proper authorization before testing

The developers are not responsible for any misuse of this tool. Users assume full responsibility for their actions.

---

🚀 Quick Start

Step 1: Install Termux

Download Termux from F-Droid or official app store.

Step 2: Update & Install Dependencies

```bash
pkg update && pkg upgrade
pkg install python git
```

Step 3: Download HCO-MetaLoad

```bash
git clone https://github.com/Hackerscolonyofficial/HCO-MetaLoad.git
```

Step 4: Run the Tool

```bash
python hco_metaload.py
```

---

🎯 First Run Experience

When you first run HCO-MetaLoad, you'll experience:

1. 🔐 Tool Lock Screen - Educational purpose reminder
2. ⏰ Countdown - 9.8.7.6.5.4.3.2.1
3. 📱 YouTube Redirect - Opens Hackers Colony Tech channel
4. ✅ Subscription - Please subscribe to continue
5. 🎉 Welcome Banner - HCO MetaLoad by Azhar in green/red box
6. 💻 Framework Ready - Metasploit-like interface

---

🛠️ Available Modules

📡 Auxiliary Modules

Module Command Description
Port Scanner use auxiliary/port_scanner TCP port scanning
System Info use auxiliary/system_info Gather system information
Network Discovery use auxiliary/network_discovery Network host discovery

💣 Payload Modules

Module Command Description
Python Reverse Shell use payload/python_reverse Python reverse shell
Bash Reverse Shell use payload/bash_reverse Bash reverse shell
PHP Web Shell use payload/php_webshell PHP web shell with authentication
Python Keylogger use payload/python_keylogger Keylogging utility
Android Payload use payload/android Android reverse shell

⚡ Exploit Modules

Module Command Description
Basic HTTP Test use exploit/basic_http HTTP service testing

---

🎮 Usage Examples

Example 1: Create Python Reverse Shell

```bash
hco > use payload/python_reverse
hco (python_reverse_shell) > set LHOST 192.168.1.100
hco (python_reverse_shell) > set LPORT 4444
hco (python_reverse_shell) > set OUTPUT revshell.py
hco (python_reverse_shell) > run
```

Example 2: Port Scanning

```bash
hco > use auxiliary/port_scanner
hco (port_scanner) > set RHOSTS 192.168.1.1
hco (port_scanner) > set PORTS 1-1000
hco (port_scanner) > run
```

Example 3: PHP Web Shell

```bash
hco > use payload/php_webshell
hco (php_web_shell) > set PASSWORD mysecurepass
hco (php_web_shell) > set OUTPUT shell.php
hco (php_web_shell) > run
```

---

⌨️ Command Reference

Core Commands

Command Description
help Show help menu
exit / quit Exit framework
clear Clear screen
version Show version info

Module Commands

Command Description
show modules List all modules
show payloads List payload modules
show auxiliary List auxiliary modules
show exploits List exploit modules
use <module> Select a module
back Deselect current module
show options Show module options
set <option> <value> Set module option
run Execute module

Navigation Commands

Command Description
show modules Browse available modules
use <module_path> Select specific module
back Return to main menu

---

🎯 Payload Usage Guide

Reverse Shell Setup

1. Generate Payload:
   ```bash
   use payload/python_reverse
   set LHOST YOUR_IP
   set LPORT 4444
   run
   ```
2. Start Listener:
   ```bash
   nc -lvnp 4444
   ```
3. Execute Payload on target system

Web Shell Usage

1. Generate PHP Shell:
   ```bash
   use payload/php_webshell
   set PASSWORD admin123
   run
   ```
2. Upload to web server
3. Access via browser: http://target/shell.php
4. Enter password and execute commands

---

🔧 Advanced Features

Custom Payload Configuration

All payloads support custom parameters:

· LHOST/LPORT for reverse shells
· Passwords for web shells
· Output filenames
· Log file paths

Threaded Operations

Port scanner uses threading for faster results:

```bash
set THREADS 20
```

Network Discovery

Discover hosts on network:

```bash
use auxiliary/network_discovery
set SUBNET 192.168.1.0/24
run
```

---

🛡️ Security Best Practices

For Testers:

· ✅ Always get written permission
· ✅ Use in isolated lab environments
· ✅ Document all testing activities
· ✅ Follow responsible disclosure

For Defenders:

· ✅ Monitor for suspicious payloads
· ✅ Keep systems updated
· ✅ Use intrusion detection systems
· ✅ Implement proper access controls

---

❓ Troubleshooting

Common Issues & Solutions

Issue: "Module not found"

· Solution: Use show modules to see available modules

Issue: YouTube doesn't open

· Solution: Manually visit: https://youtube.com/@hackers_colony_tech

Issue: Payload not working

· Solution: Check LHOST/LPORT settings and firewall rules

Issue: Permission denied

· Solution: Run chmod +x hco_metaload.py

Dependency Issues

```bash
# Install missing Python packages
pip install keyboard  # For keylogger payload

# Fix termux issues
pkg update
pkg install python git ncurses-utils
```
---

🌟 Features Overview

✅ Metasploit-like Interface

· Familiar command structure
· Module-based architecture
· Professional output formatting

✅ Multiple Payload Types

· Reverse shells (Python, Bash)
· Web shells (PHP)
· Keyloggers (Python)
· Android payloads

✅ Security Tools

· Port scanning
· Network discovery
· System information gathering
· Vulnerability assessment

✅ User Experience

· Color-coded output
· Interactive help system
· Error handling
· Progress indicators

---

🔄 Updates & Roadmap

Current Version: v2.0

· ✅ Metasploit-style interface
· ✅ Payload generation
· ✅ Auxiliary modules
· ✅ Termux compatibility

Planned Features

· More exploit modules
· Database integration
· Reporting features
· GUI interface
· More payload types

---

🤝 Contributing

We welcome contributions from the security community:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Follow ethical guidelines

Note: All contributions must comply with ethical hacking standards.

---

📜 License

This project is licensed for Educational Use Only.

· Allowed: Learning, authorized testing, research
· Prohibited: Illegal activities, unauthorized testing
· Responsibility: Users assume full responsibility for their actions

---

🆘 Support

Documentation

· This README
· In-tool help system (help command)
· Example usage scenarios

Community

· YouTube: Hackers Colony Tech
· GitHub Issues: For bug reports
· Educational forums

Emergency

If you find vulnerabilities:

1. Stop testing immediately
2. Document findings
3. Follow responsible disclosure
4. Contact system owners


---

📊 Usage Statistics

The framework tracks:

· Module usage frequency
· Payload generation counts
· Error rates (anonymous)

No personal data is collected. Statistics help improve the tool.

---

⚡ Pro Tips

For Beginners:

· Start with auxiliary/system_info to learn
· Use simple payloads first
· Practice in lab environments
· Read the help system thoroughly

For Experts:

· Customize payload parameters
· Combine modules for advanced testing
· Develop custom modules
· Contribute to the project

Performance Tips:

· Use appropriate thread counts
· Limit scan ranges for speed
· Close unused modules with back
· Use clear to refresh interface

---

🌍 Ethical Guidelines

Always Remember:

· With great power comes great responsibility
· Knowledge is a tool - use it wisely
· Security testing should improve safety
· Education is the primary goal

The Hacker Ethic:

· Access to computers should be unlimited and total
· All information should be free
· Mistrust authority—promote decentralization
· Hackers should be judged by their hacking

---

🏆 Acknowledgments

Special Thanks To:

· The cybersecurity community
· Open source developers
· Ethical hackers worldwide
· Our YouTube subscribers

Inspired By:

· Metasploit Framework
· Kali Linux tools
· Security research community

---

📞 Contact

Developer: Azhar
Organization: Hackers Colony
YouTube: @hackers_colony_tech
Purpose: Educational Cybersecurity Content

---

💫 Final Words

"The price of freedom is eternal vigilance." - Thomas Jefferson

Remember: This tool is a double-edged sword. Use it to protect, not to harm. Strengthen defenses, expose vulnerabilities responsibly, and always prioritize ethical conduct.

Stay curious, stay ethical, stay secure.

---

Code by Azhar
HCO MetaLoad v2.0
Empowering ethical hackers since 2024

---

<div align="center">

⭐ If you find this tool helpful, please star the repository! ⭐

https://api.star-history.com/svg?repos=hackers-colony/HCO-MetaLoad&type=Date

</div>

---

Last updated: December 2024
Version: 2.0
Compatibility: Termux, Python 3.7+
