ASU ID : 1218931818
Name : Almaha Alkhalouf

This Python script is analyzes disk image files, extracts partition information and boot record data. It calculates MD5 and SHA-256 hash values for the input file and saves them in separate text files. Depending on whether it detects an MBR (Master Boot Record) or GPT (GUID Partition Table) structure in the image, it proceeds to analyze the partitions and print it on console.

For MBR, it reads the MBR structure, extracts information about up to four partitions (if present), and prints their types, starting LBA addresses, and sizes. It also reads and displays the boot record information for each partition, including the first 16 bytes in both hexadecimal and ASCII formats.

For GPT, it skips the GPT header and processes partition entries. It prints the partition number, type GUID, and starting/ending LBA addresses in both hexadecimal and decimal formats.

The script checks command-line arguments, computes hash values, and utilizes a JSON file to associate partition type codes with their descriptions.