import zstandard as zstd
import io

def read_log_lines(file_path):

    if file_path.endswith(".zst"):
        with open(file_path, 'rb') as f:
            dctx = zstd.ZstdDecompressor()

            with dctx.stream_reader(f) as reader:
                text_stream = io.TextIOWrapper(reader, encoding='utf-8')

                for line in text_stream:
                    yield line.strip()

    else:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                yield line.strip()