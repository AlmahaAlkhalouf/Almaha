#!/usr/bin/env python3

import hashlib
import struct
import sys
import json


def compute_hashes(file_path):
    hasher_md5 = hashlib.md5()
    hasher_sha256 = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher_md5.update(chunk)
            hasher_sha256.update(chunk)
    
    with open(f"MD5-{file_path}.txt", 'w') as f:
        f.write(hasher_md5.hexdigest())
    
    with open(f"SHA-256-{file_path}.txt", 'w') as f:
        f.write(hasher_sha256.hexdigest())


def print_partition_info(partition_type, start_lba, size):
    formatted_hex = '{:02X}'.format(partition_type)
    print(f"({formatted_hex}) {json_file.get(partition_type)} , {start_lba}, {size}")


json_file = {}

def print_boot_record_info(partition_number, boot_record):
    print(f"Partition number: {partition_number}")
    print("First 16 bytes of boot record:", ' '.join(f'{byte:02X}' for byte in boot_record))
    ascii_text = '  '.join([chr(byte) if 32 <= byte <= 126 else '.' for byte in boot_record])
    print("ASCII:                         ", ascii_text)



def print_partition_info_gpt(partition_number, partition_type_guid, start_lba_hex, end_lba_hex, start_lba_dec, end_lba_dec):
    print(f"Partition number: {partition_number+1}")
    print(f"Partition Type GUID: {partition_type_guid}")
    print(f"Starting LBA address in hex: {start_lba_hex}")
    print(f"ending LBA address in hex: {end_lba_hex}")
    print(f"starting LBA address in Decimal: {start_lba_dec}")
    print(f"ending LBA address in Decimal: {end_lba_dec}")

def read_mbr(file_path):
    with open(file_path, 'rb') as f:
        # Read the first sector (512 bytes)
        mbr_data = f.read(512)
        mbr_data_second = f.read(512)
        
        # Check for MBR signature (0x55AA) at the end of the sector
        if mbr_data_second[0:8] == b'EFI PART':
            
            # Extract GPT partition information
            # You'll need to implement GPT parsing logic here
            # See below for an example of how to proceed
            
            # Seek to the GPT header location (usually at LBA 1)
            f.seek(512 + 512)  # GPT partition entries start at LBA 2
            
            # Read and process each GPT partition entry
            for i in range(0, 4):
                partition_entry = f.read(128)
                
                # Extract and print relevant information from the entry
                partition_type_guid = ''.join(['{:02X}'.format(b) for b in partition_entry[0:16]])
                start_lba_hex = '0x{:x}'.format(struct.unpack("<Q", partition_entry[32:40])[0])
                end_lba_hex = '0x{:x}'.format(struct.unpack("<Q", partition_entry[40:48])[0])
                start_lba_dec = struct.unpack("<Q", partition_entry[32:40])[0]
                end_lba_dec = struct.unpack("<Q", partition_entry[40:48])[0]
                
                # Print partition information in the desired format
                print_partition_info_gpt(i, partition_type_guid, start_lba_hex, end_lba_hex, start_lba_dec, end_lba_dec)
                if(i != 3):
                    print("")
                
                # No boot records in GPT, so there's no need to call print_boot_record_info

        elif mbr_data[-2:] == b'\x55\xAA':
            # It's an MBR
            
            # Parse MBR structure and extract partition information
            # Iterate through the partition entries (4 entries)
            for i in range(4):
                entry_start = 446 + i * 16
                entry = mbr_data[entry_start:entry_start + 16]
                
                # Parse partition type, starting LBA, and size from the entry
                partition_type = entry[4]
                start_lba = struct.unpack("<I", entry[8:12])[0]
                size = struct.unpack("<I", entry[12:16])[0]
                
                # Print partition information
                print_partition_info(partition_type, start_lba, size*512)

            for i in range(4):
                entry_start = 446 + i * 16
                entry = mbr_data[entry_start:entry_start + 16]
                
                # Parse partition type, starting LBA, and size from the entry
                partition_type = entry[4]
                start_lba = struct.unpack("<I", entry[8:12])[0]
                size = struct.unpack("<I", entry[12:16])[0]
                
                # Read and print boot record information
                boot_record_start = start_lba * 512  # Convert LBA to byte offset
                f.seek(boot_record_start)
                boot_record = f.read(16)  # Read the first 16 bytes of the boot record
                print_boot_record_info(i + 1, boot_record)

        else:
            print("Unknown partition scheme detected")

def main():
    if len(sys.argv) != 3 or sys.argv[1] != '-f':
        print("Usage: ./boot_info -f <raw_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[2]

    # Compute the MD5 and SHA-256 hashes
    compute_hashes(file_path)

    f = open('PartitionTypes.json', 'r')
    json_file_content = json.loads(f.read())
    for i in json_file_content:
        json_file[int(str(i.get('hex')), 16)] = i.get("desc")

    # Read the MBR or GPT structure
    read_mbr(file_path)

if __name__ == "__main__":
    main()
