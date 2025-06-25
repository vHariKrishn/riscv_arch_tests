import os
import subprocess

# Directories
spike_dir = "/home/harikrishna/riscv_arch_tests/riscv_tests/log/build/sv39_spike_dump"
rtl_dir = "/home/harikrishna/Tenstorrent/c-class/sv39_tt/red_c-class_dump"
diff_dir = "/home/harikrishna/riscv_arch_tests/riscv_tests/log/build/difference"

# Ensure the difference directory exists
os.makedirs(diff_dir, exist_ok=True)

# Collect all spike.dump files
for spike_file in os.listdir(spike_dir):
    if spike_file.endswith(".spike.dump"):
        base_name = spike_file.replace(".spike.dump", "")
        rtl_file_name = f"{base_name}_rtl.dump"
        rtl_file_path = os.path.join(rtl_dir, rtl_file_name)
        spike_file_path = os.path.join(spike_dir, spike_file)
        diff_file_name = f"{base_name}_diff.dump"
        diff_file_path = os.path.join(diff_dir, diff_file_name)

        if os.path.exists(rtl_file_path):
            # Run diff -iw and write output to the difference file
            with open(diff_file_path, "w") as diff_out:
                subprocess.run(
                    ["diff", "-iw", spike_file_path, rtl_file_path],
                    stdout=diff_out
                )
            print(f"Compared: {spike_file} <-> {rtl_file_name} -> {diff_file_name}")
        else:
            print(f"RTL file not found for: {spike_file}")

print("Comparison complete.")

