#!/bin/bash

# Check if the file name is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename="$1"

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File not found: $filename"
    exit 1
fi

# Get the total number of lines in the file
total_lines=$(wc -l < "$filename")

# Calculate the number of lines per split file
lines_per_file=$((total_lines / 30))

# Handle the case where the number of lines is not perfectly divisible by 30
remainder=$((total_lines % 30))

# Initialize a counter for split files
split_count=1

# Use 'split' command to split the file
split -l $lines_per_file "$filename" "$filename.part"

# Append any remaining lines to the last split file
if [ $remainder -gt 0 ]; then
    tail -n $remainder "$filename" >> "$filename.part$((split_count - 1))"
fi

echo "File split into 30 parts."
