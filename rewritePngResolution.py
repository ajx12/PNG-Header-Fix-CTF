# fix_png_resolution.py
import struct
import binascii

filename = "image.png"
outfile  = "imageResized.png"

with open(filename, "rb") as f:
    data = bytearray(f.read())

# IHDR starts at byte offset 8+8 = 16 (after PNG sig + length/type fields)
# Here we wil extract the resolution fields 
ihdr_offset = 8 + 8
width_bytes = data[ihdr_offset:ihdr_offset+4]
height_bytes = data[ihdr_offset+4:ihdr_offset+8]
width  = struct.unpack(">I", width_bytes)[0]
height = struct.unpack(">I", height_bytes)[0]

print(f"Current IHDR width={width}, height={height}")

# Here we will try a new height for the image. 
new_height = 1100  # change this until the image looks correct
data[ihdr_offset+4:ihdr_offset+8] = struct.pack(">I", new_height)

# recalc IHDR CRC as now it should be different.
chunk_type = b"IHDR"
ihdr_data = data[ihdr_offset:ihdr_offset+13]
calc_crc = binascii.crc32(chunk_type + ihdr_data) & 0xffffffff
crc_offset = ihdr_offset + 13
data[crc_offset:crc_offset+4] = struct.pack(">I", calc_crc)

with open(outfile, "wb") as f:
    f.write(data)

print("Wrote", outfile, "with height =", new_height)
