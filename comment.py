import os

def comment_block_in_file(filepath, start_marker, end_marker):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    inside_block = False
    new_lines = []
    for line in lines:
        if start_marker in line:
            inside_block = True
            new_lines.append(line)
            continue
        if end_marker in line:
            inside_block = False
            new_lines.append(line)
            continue
        if inside_block and not line.strip().startswith('#'):
            new_lines.append('#' + line)
        else:
            new_lines.append(line)

    with open(filepath, 'w') as f:
        f.writelines(new_lines)

def comment_blocks_in_all_S_files(start_marker, end_marker):
    for filename in os.listdir('.'):
        if filename.endswith('.S') and os.path.isfile(filename):
            print(f"Processing: {filename}")
            comment_block_in_file(filename, start_marker, end_marker)

if __name__ == "__main__":
    # Define your markers
    start_marker = 'Initialize Vector Register'
    end_marker = 'setup_medeleg'
    comment_blocks_in_all_S_files(start_marker, end_marker)
