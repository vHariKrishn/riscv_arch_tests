#!/usr/bin/env python3

import os
import subprocess
import sys

def run_command(command, shell=True):
    """Run a shell command and print errors if any."""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Warning: Command failed with return code {result.returncode}")
            print(f"Command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error running command: {command}")
        print(f"Exception: {e}")
        return False

def process_elf_files():
    build_dir = "/home/harikrishna/riscv_arch_tests/riscv_tests/log/build"
    dump_dir = "./sv39_core_dump"
    os.makedirs(dump_dir, exist_ok=True)

    # Find all files with NO extension (no dot in filename)
    elf_files = [
        os.path.join(build_dir, f)
        for f in os.listdir(build_dir)
        if os.path.isfile(os.path.join(build_dir, f)) and '.' not in f
    ]

    if not elf_files:
        print(f"No ELF files without extension found in {build_dir}")
        return

    elf_files.sort()
    print(f"Found {len(elf_files)} ELF files to process")
    print("-" * 50)

    for i, elf_file in enumerate(elf_files, 1):
        elf_filename = os.path.basename(elf_file)
        print(f"Processing {i}/{len(elf_files)}: {elf_filename}")

        # Step 1: Run elf2hex
        elf2hex_cmd = f"elf2hex 8 268435456 {elf_file} 2147483648 > code.mem"
        if not run_command(elf2hex_cmd):
            print(f"  Failed at elf2hex for {elf_filename}")
            continue

        # Step 2: Run simulation with timeout
        timeout_cmd = "timeout --foreground 3m ./out +rtldump"
        result = subprocess.run(timeout_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 124:
            print(f"  Simulation timed out (expected for some tests)")
        elif result.returncode != 0:
            print(f"  Simulation failed with return code {result.returncode}")
            print(f"  Error: {result.stderr}")

        # Step 3: Move rtl.dump to dump_dir with unique name
        if os.path.exists("rtl.dump"):
            dump_filename = f"{elf_filename}_rtl.dump"
            destination = os.path.join(dump_dir, dump_filename)
            move_cmd = f"mv rtl.dump {destination}"
            if run_command(move_cmd):
                print(f"  Moved rtl.dump to {destination}")
            else:
                print(f"  Failed to move rtl.dump")
        else:
            print(f"  Warning: rtl.dump not found after simulation")

        print("-" * 30)

    print("\nDone. Dump files saved in:", os.path.abspath(dump_dir))

def main():
    print("RISC-V ELF File Processor")
    print("=" * 50)
    process_elf_files()

if __name__ == "__main__":
    main()
