# Clang-Tidy Static Analysis for C Drivers

This repository provides a Python script to run **Clang-Tidy** static analysis checks on Linux driver `.c` files.  
It helps detect potential issues such as memory bugs, reserved identifiers, and performance problems.

---

##  Installation

First, update your system and install the required packages:

```
sudo apt update
sudo apt install clang-tidy -y
sudo apt install bear -y   # optional, for compile_commands.json support
```
---

## To Execute 

```
python3 run_clang_tidy.py /path/to/driver/


