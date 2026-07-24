import re
from pathlib import Path

def get_next_id(directory="docs/product-specs/prds"):
    path = Path.cwd() / directory

    if not path.exists():
        return "0001"

    ids = []
    for f in path.glob("*.md"):
        match = re.match(r"^prd-(\d{4})-", f.name)
        if match:
            ids.append(int(match.group(1)))

    if not ids:
        return "0001"

    next_id = max(ids) + 1
    return f"{next_id:04d}"

if __name__ == "__main__":
    print(get_next_id())
