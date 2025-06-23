import os

# Source and destination directories
src_dir = "/home/harikrishna/Tenstorrent/c-class/sv39_tt/test_sv39"
dst_dir = "/home/harikrishna/Tenstorrent/c-class/sv39_tt/reduced_lines_c-dump"
max_lines = 6000

# Create destination directory if it does not exist
os.makedirs(dst_dir, exist_ok=True)

# Iterate over all files in the source directory
for filename in os.listdir(src_dir):
    src_path = os.path.join(src_dir, filename)
    dst_path = os.path.join(dst_dir, filename)

    # Only process files (skip directories)
    if os.path.isfile(src_path):
        with open(src_path, "r") as src_file:
            lines = []
            for i, line in enumerate(src_file):
                if i >= max_lines:
                    break
                lines.append(line)
        with open(dst_path, "w") as dst_file:
            dst_file.writelines(lines)

print("All files processed. Reduced files are in:", dst_dir)

