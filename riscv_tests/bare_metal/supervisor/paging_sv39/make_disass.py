#!/usr/bin/env python3

import os
import subprocess

# Source directory containing ELF files (no extension)
src_dir = "/home/harikrishna/riscv_arch_tests/riscv_tests/log/build"
# Destination directory for disassembly files
dst_dir = "/home/harikrishna/Tenstorrent/c-class/sv39_tt/sv39_disass"

# Ensure the destination directory exists
os.makedirs(dst_dir, exist_ok=True)

# List all files in src_dir with NO extension (no dot in filename)
elf_files = [
    f for f in os.listdir(src_dir)
    if os.path.isfile(os.path.join(src_dir, f)) and '.' not in f
]

if not elf_files:
    print(f"No ELF files without extension found in {src_dir}")
    exit(1)

elf_files.sort()
print(f"Found {len(elf_files)} ELF files to disassemble.")

for i, elf_file in enumerate(elf_files, 1):
    src_path = os.path.join(src_dir, elf_file)
    disass_file = os.path.join(dst_dir, elf_file + ".disass")
    print(f"[{i}/{len(elf_files)}] Disassembling {elf_file} -> {disass_file}")

    cmd = f"riscv64-unknown-elf-objdump -d {src_path} > {disass_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Error disassembling {elf_file}: {result.stderr}")

print("All disassembly files generated in:", dst_dir)

