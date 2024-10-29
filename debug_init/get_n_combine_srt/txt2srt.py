### English ambil file 114_english.txt dr AddIns Kemenag 2023
import os

# Define the path to the input and output files
input_no_surah = 114
input_txt_file = f"dataset/srt_raw/{input_no_surah}_english.txt"
output_srt_file = f"dataset/srt_raw/{input_no_surah}_{surah_name_latin_alias[input_no_surah-1]}_english.srt"

# Check if the input file exists
if not os.path.exists(input_txt_file):
    raise FileNotFoundError(f"The file {input_txt_file} does not exist.")

# Read the content from the .txt file
with open(input_txt_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Initialize the SRT content
srt_content = []

# Process each line to create SRT entries
for line in lines:
    line = line.strip()
    if line:  # Skip empty lines
        # Split the line into number and verse
        number, verse = line.split(".", 1)
        number = number.strip()
        verse = verse.strip()
        
        # Create SRT timing (adjust timing as needed)
        start_time = f"{int(number)-1:02}:00:00,000"  # Start time
        end_time = f"{int(number):02}:00:00,000"      # End time
        
        # Append the formatted SRT entry
        srt_content.append(f"{number}\n{start_time} --> {end_time}\n{verse}\n")

# Join the SRT content into a single string
srt_output = "".join(srt_content)

# Save the SRT content to a file
with open(output_srt_file, "w", encoding="utf-8") as srt_file:
    srt_file.write(srt_output)

print(f"SRT file '{output_srt_file}' created successfully.")