import zstandard as zstd

input_file = "sample.log"
output_file = "sample.log.zst"

with open(input_file, "rb") as f_in:
    data = f_in.read()

cctx = zstd.ZstdCompressor()

with open(output_file, "wb") as f_out:
    f_out.write(cctx.compress(data))

print("sample.log.zst created")