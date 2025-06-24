import os

# Source and destination directories
src_dir = "/home/harikrishna/Tenstorrent/c-class/sv39_tt/sv39_core_dump"
dst_dir = "/home/harikrishna/Tenstorrent/c-class/sv39_tt/red_c-class_dump"
spike_dir = "/home/harikrishna/riscv_arch_tests/riscv_tests/log/build/sv39_spike_dump"

# Function to extract base name (e.g., "rv32d_84" from "rv32d_84_rtl.dump" or "rv32d_84.spike.dump")
def get_base_name(filename):
    # Remove file extension
    base = filename.split('.')[0]
    # Remove "_rtl" suffix if present
    if base.endswith('_rtl'):
        base = base[:-4]
    # Handle cases like "rv32d_84.spike" -> becomes "rv32d_84"
    parts = base.split('_')
    if len(parts) >= 2:
        return '_'.join(parts[:2])  # Keep first two segments
    return base

# Build dictionary of spike dump line counts
spike_lines_count = {}
for filename in os.listdir(spike_dir):
    spike_path = os.path.join(spike_dir, filename)
    if os.path.isfile(spike_path):
        base_name = get_base_name(filename)
        with open(spike_path, "r") as f:
            spike_lines_count[base_name] = sum(1 for _ in f)

# Process source files
os.makedirs(dst_dir, exist_ok=True)
for filename in os.listdir(src_dir):
    src_path = os.path.join(src_dir, filename)
    dst_path = os.path.join(dst_dir, filename)
    
    if os.path.isfile(src_path):
        base_name = get_base_name(filename)
        max_lines = spike_lines_count.get(base_name)
        
        if max_lines is None:
            print(f"Warning: No matching spike dump for {filename} (base: {base_name})")
            continue
            
        with open(src_path, "r") as src_file:
            lines = []
            for i, line in enumerate(src_file):
                if i >= max_lines:
                    break
                lines.append(line)
                
        with open(dst_path, "w") as dst_file:
            dst_file.writelines(lines)
            
print(f"Processed {len(os.listdir(src_dir))} files. Output in: {dst_dir}")
