import os
import json
import time
import uuid
from datetime import datetime

# Directory tiers
HOT_MEMORY_DIR = "F:/AI_HotMemory"
WARM_MEMORY_DIR = "E:/AI_WarmMemory"
COLD_MEMORY_DIR = "P:/AI_ColdMemory"

# Helper to build a full path in the correct tier
def _build_path(memory_id, tier_dir):
    return os.path.join(tier_dir, f"{memory_id}.json")

# Save to specific tier
def save_to_tier(memory_id, content, tier="hot", tags=None, use_vector=False, metadata=None):
    tier_map = {
        "hot": HOT_MEMORY_DIR,
        "warm": WARM_MEMORY_DIR,
        "cold": COLD_MEMORY_DIR
    }

    if tier not in tier_map:
        raise ValueError(f"Invalid tier: {tier}")

    path = _build_path(memory_id, tier_map[tier])
    data = {
        "memory_id": memory_id,
        "memory_content": content,
        "tier": tier,
        "tags": tags or [],
        "use_vector": use_vector,
        "metadata": metadata or {}
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    return {"status": "saved", "tier": tier, "path": path}

def save_to_memory(content, tags=None, tier="hot", use_vector=False, metadata=None):
    memory_entry = str(uuid.uuid4())
    memory_record = {
        "memory_entry": memory_entry,
        "memory_content": content,
        "tags": tags or [],
        "tier": tier,
        "use_vector": use_vector,
        "metadata": metadata or {}
    }
    return save_to_tier(memory_entry, content, tier)

# Load from specific tier
def load_from_tier(memory_id, tier="hot"):
    tier_map = {
        "hot": HOT_MEMORY_DIR,
        "warm": WARM_MEMORY_DIR,
        "cold": COLD_MEMORY_DIR
    }
    path = _build_path(memory_id, tier_map[tier])
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Sync hot memory to warm
def sync_hot_to_warm():
    files = os.listdir(HOT_MEMORY_DIR)
    for file in files:
        src = os.path.join(HOT_MEMORY_DIR, file)
        dst = os.path.join(WARM_MEMORY_DIR, file)
        with open(src, 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(dst, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    return {"status": "synced", "files_moved": len(files)}

# Decay and migrate to cold
def trigger_decay_migration(expiration_seconds=86400):
    now = time.time()
    migrated = 0
    for file in os.listdir(WARM_MEMORY_DIR):
        path = os.path.join(WARM_MEMORY_DIR, file)
        if os.path.isfile(path):
            last_modified = os.path.getmtime(path)
            if now - last_modified > expiration_seconds:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                cold_path = os.path.join(COLD_MEMORY_DIR, file)
                with open(cold_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                os.remove(path)
                migrated += 1
    return {"status": "decay_migrated", "migrated_count": migrated}

