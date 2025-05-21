# File: mmap/mmap_layer.py

import os
import mmap
import json
import threading

# Lock to handle concurrent access
mmap_lock = threading.Lock()

# Root memory directory
MEMORY_ROOT = "memory_tiers/hot"
MMAP_FILE = os.path.join(MEMORY_ROOT, "memory.mmap")
INDEX_FILE = os.path.join(MEMORY_ROOT, "index.json")

# Ensure memory root exists
os.makedirs(MEMORY_ROOT, exist_ok=True)

# Create empty memory.mmap if not present
if not os.path.exists(MMAP_FILE):
    with open(MMAP_FILE, "wb") as f:
        f.write(b"\0" * 1024 * 1024)  # 1MB initial size

# Initialize index
if not os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, "w") as f:
        json.dump({}, f)

def load_index():
    with open(INDEX_FILE, "r") as f:
        return json.load(f)

def save_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

def write_memory_block(key, content):
    with mmap_lock:
        index = load_index()
        encoded = content.encode("utf-8")

        with open(MMAP_FILE, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0)
            mm.seek(0, os.SEEK_END)
            start = mm.tell()
            mm.resize(start + len(encoded))
            mm.write(encoded)
            mm.flush()
            mm.close()

        index[key] = {
            "start": start,
            "length": len(encoded)
        }
        save_index(index)

def read_memory_block(key):
    with mmap_lock:
        index = load_index()
        meta = index.get(key)
        if not meta:
            return None

        with open(MMAP_FILE, "rb") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            mm.seek(meta["start"])
            data = mm.read(meta["length"])
            mm.close()

        return data.decode("utf-8")

def delete_memory_block(key):
    with mmap_lock:
        index = load_index()
        if key in index:
            del index[key]
            save_index(index)

        # NOTE: does not compact mmap file (future optimization)

def list_memory_keys():
    index = load_index()
    return list(index.keys())

