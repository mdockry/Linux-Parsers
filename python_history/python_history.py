
entries_count = 0
input_path = ".python_history"

try:
    with open(input_path, "r", encoding="utf-8") as python_history:
        for line in python_history:
            line = line.strip()
            if not line:
                continue
            print(line)
            entries_count += 1
except FileNotFoundError:
    print(f"File not found: {input_path}")

print(f"Total entries: {entries_count}")