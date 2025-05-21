# chunked_file_reader.py
# Part of the AkashicPlaything system — supports reading large files in chunks

import os

CHUNK_REGISTRY = {}


def register_chunks(filepath, lines_per_chunk=200):
    """
    Splits the file into line-based chunks and registers them by part number.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    chunks = [
        lines[i:i + lines_per_chunk]
        for i in range(0, total_lines, lines_per_chunk)
    ]

    registry_key = os.path.basename(filepath)
    CHUNK_REGISTRY[registry_key] = chunks
    return len(chunks)


def get_chunk(filepath, chunk_index):
    """
    Retrieves a specific chunk from the registered file.
    """
    registry_key = os.path.basename(filepath)

    if registry_key not in CHUNK_REGISTRY:
        raise RuntimeError("File not registered. Call register_chunks() first.")

    chunks = CHUNK_REGISTRY[registry_key]
    if chunk_index < 0 or chunk_index >= len(chunks):
        raise IndexError(f"Chunk index {chunk_index} out of range for {filepath}")

    return ''.join(chunks[chunk_index])


def list_registered_chunks():
    return {
        fname: len(chunks)
        for fname, chunks in CHUNK_REGISTRY.items()
    }


if __name__ == "__main__":
    # Example usage for testing
    path = "./examples/server/server.cpp"
    parts = register_chunks(path, 150)
    print(f"{parts} chunks available.")
    print(get_chunk(path, 0))

