import json
import os

# Define the path to the JSON file
input_no_surah = 108
json_file_path = f"dataset/quran_json_init/quran-json-master/surah/{input_no_surah}.json"

# Check if the file exists
if not os.path.exists(json_file_path):
    raise FileNotFoundError(f"The file {json_file_path} does not exist.")

# Load the JSON data from the file
with open(json_file_path, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Function to create SRT content from verses
def create_srt_content(verses):
    srt_content = []
    for key, text in verses.items():
        # You can adjust the timing as needed
        start_time = f"{int(key)-1:02}:00:00,000"
        end_time = f"{int(key):02}:00:00,000"
        srt_content.append(f"{key}\n{start_time} --> {end_time}\n{text}\n")
    return "".join(srt_content)

# Extract verses for Arabic and Indonesian
arabic_verses = data[f"{input_no_surah}"]["text"]
indonesian_verses = data[f"{input_no_surah}"]["translations"]["id"]["text"]

# Create SRT content
arabic_srt = create_srt_content(arabic_verses)
indonesian_srt = create_srt_content(indonesian_verses)

# Save to files
arabic_srt_filename = f"dataset/srt_raw/{input_no_surah}_{surah_name_latin_alias[input_no_surah-1]}_arabic.srt"
indonesian_srt_filename = f"dataset/srt_raw/{input_no_surah}_{surah_name_latin_alias[input_no_surah-1]}_indonesia.srt"

with open(arabic_srt_filename, "w", encoding="utf-8") as arabic_file:
    arabic_file.write(arabic_srt)

with open(indonesian_srt_filename, "w", encoding="utf-8") as indonesian_file:
    indonesian_file.write(indonesian_srt)

print("SRT files created successfully.")