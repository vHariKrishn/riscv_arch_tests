import os
import subprocess

build_dir = "/home/harikrishna/riscv_arch_tests/riscv_tests/log/build"
dump_dir = os.path.join(build_dir, "sv39_spike_dump")
os.makedirs(dump_dir, exist_ok=True)

for filename in os.listdir(build_dir):
    elf_path = os.path.join(build_dir, filename)
    if os.path.isfile(elf_path):
        dump_file = os.path.join(dump_dir, f"{filename}.spike.dump")
        cmd = [
            "spike",
            "--isa=rv64gcZicsr_Zifencei",
            "--log-commits",
            "--log", dump_file,
            elf_path
        ]
        print(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running {filename}:")
            print(f"Exit code: {e.returncode}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
