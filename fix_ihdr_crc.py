#This file will fix the ihdr crc value.
import binascii
import sys

fn = "image.png"   # input copy
out = "imageFixed.png" # patched output

data = open(fn, "rb").read()

# PNG signature is 8 bytes, IHDR length is at offset 8..11, type at 12..15
offset = 8
length = int.from_bytes(data[offset:offset+4], "big") #Interpret the 32bit binary representation of the length of IHDR data (big endian)  
chunk_type = data[offset+4:offset+8] 
# check that we have the IHDR chunk
if chunk_type != b"IHDR":
    print("Unexpected chunk at expected IHDR location:", chunk_type)
    sys.exit(1)

chunk_data = data[offset+8:offset+8+length] #collect the chunks data
crc_offset = offset + 8 + length # byte offset in the file where the CRC starts
old_crc = data[crc_offset:crc_offset+4] #read the current crc
calc = binascii.crc32(chunk_type + chunk_data) & 0xffffffff #calculate the actual crc
# Then print for inspection:
print(f"IHDR length={length} type={chunk_type} old_crc=0x{int.from_bytes(old_crc,'big'):08x} calc=0x{calc:08x}")

# create bytes to patch bad header field
new_crc_bytes = calc.to_bytes(4, "big") #convert calculated value to 32bit big-endian binary
patched = data[:crc_offset] + new_crc_bytes + data[crc_offset+4:] # Create new file data with the CRC section replaced
open(out, "wb").write(patched) # Write in the new, corrected CRC value to the "fixed" file
print("Wrote patched file:", out)
