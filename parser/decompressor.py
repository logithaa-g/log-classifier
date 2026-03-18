import zstandard as zstd

def read_log_lines(file_path):
    
    # If file is compressed
    if file_path.endswith(".zst"):
        with open(file_path, 'rb') as f:
            dctx = zstd.ZstdDecompressor()

            with dctx.stream_reader(f) as reader:
                for line in reader:
                    yield line.decode('utf-8', errors='ignore').strip()

    # If file is normal text
    else:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                yield line.strip()