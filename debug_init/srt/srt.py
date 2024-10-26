import time
from datetime import timedelta
import re
from mutagen.mp3 import MP3

# Fungsi untuk mengganti interval waktu di SRT dengan time_intervals
def replace_srt_intervals(srt_list, time_intervals):
    updated_srt = []
    for i, entry in enumerate(srt_list):
        # Ambil konten asli kecuali waktu
        content = entry.split('\n')[2]  # Bagian teks SRT
        if i < len(time_intervals) - 1:
            start_time = convert_seconds_to_srt_format(time_intervals[i])
            end_time = convert_seconds_to_srt_format(time_intervals[i + 1])
        else:
            start_time = convert_seconds_to_srt_format(time_intervals[i])
            end_time = convert_seconds_to_srt_format(time_intervals[-1])
        
        updated_srt.append(f"{i+1}\n{start_time} --> {end_time}\n{content}\n")
    
    return updated_srt

# Fungsi konversi detik ke format SRT
def convert_seconds_to_srt_format(seconds):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Definisikan path file SRT
srt_files = {
    'arabic': 'data/surah_al_kautsar_arabic.srt',
    'indonesian': 'data/surah_al_kautsar_indonesian.srt',
    'javanese': 'data/surah_al_kautsar_javanese.srt',
    'english': 'data/surah_al_kautsar_english.srt'
}

# Fungsi untuk memuat konten SRT dari file
def load_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Fungsi untuk mengubah angka ke format Arab Unicode
def to_arabic_number(n):
    arabic_digits = {
        '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
        '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'
    }
    return ''.join(arabic_digits[digit] for digit in str(n))

# Fungsi untuk menambahkan "Bismillahirrohmanirrohim" di awal setiap file SRT dengan terjemahan sesuai bahasa
def add_bismillah(srt_content, lang):
    bismillah_translations = {
        'arabic': 'بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ',
        'indonesian': 'Dengan nama Allah Yang Maha Pengasih, Maha Penyayang',
        'javanese': 'Kalihan asma Allah ingkang Maha Asih, Maha Welas',
        'english': 'In the name of Allah, the Most Gracious, the Most Merciful'
    }
    
    bismillah_block = [
        '1',  # Index pertama
        '00:00:00,000 --> 00:00:05,000',  # Waktu mulai dan berakhir untuk Bismillah
        bismillah_translations[lang]  # Teks Bismillah berdasarkan bahasa
    ]
    
    updated_srt = []
    index_offset = 1
    for line in srt_content:
        if line.isdigit():  # Jika ini adalah indeks
            updated_srt.append(str(int(line) + index_offset))
        else:
            updated_srt.append(line)
    
    return bismillah_block + [''] + updated_srt

# Fungsi untuk menambahkan label ayat dalam bahasa Arab dan angka Unicode Arab
def add_verse_labels_arabic(arabic_srt_content, include_bismillah_label=False):
    total_verses = sum(1 for line in arabic_srt_content if line.isdigit())  # Hitung total ayat
    current_verse = 0
    updated_srt = []
    
    if not include_bismillah_label:
        total_verses -= 1  # Kurangi total ayat jika Bismillah tidak dilabeli

    print('total ayat = ', total_verses)
    
    skip_bismillah_count = not include_bismillah_label  # Kontrol penomoran jika Bismillah tanpa label

    for line in arabic_srt_content:
        if line.isdigit():
            current_verse += 1  # Update nomor ayat hanya saat ada angka indeks
            updated_srt.append(line)
        elif '-->' in line:
            updated_srt.append(line)
        else:
            # Cek apakah ini adalah baris Bismillah
            is_bismillah = 'بِسْمِ اللّٰهِ' in line

            if is_bismillah and not include_bismillah_label:
                # Jangan tambahkan label ayat dan jangan tambahkan nomor jika Bismillah tanpa label
                updated_srt.append(line)
            else:
                # Tambahkan label ayat sesuai aturan
                arabic_verse_label = f"{to_arabic_number(current_verse - skip_bismillah_count)}"
                updated_srt.append(f"{line} ({arabic_verse_label})")

    return updated_srt

# Fungsi untuk menggabungkan terjemahan dari setiap bahasa ke dalam satu baris
def combine_translations(arabic, indonesian, javanese, english):
    combined_srt = []
    blocks = {'arabic': [], 'indonesian': [], 'javanese': [], 'english': []}

    for ar, idn, jv, en in zip(arabic, indonesian, javanese, english):
        if ar.isdigit():  # Jika ini adalah nomor indeks
            if all(blocks.values()):  # Gabungkan blok sebelumnya
                combined_text = ' || '.join([blocks['arabic'][2], blocks['indonesian'][2], blocks['javanese'][2], blocks['english'][2]])
                combined_srt.append(f"{blocks['arabic'][0]}\n{blocks['arabic'][1]}\n{combined_text}\n")
            # Reset blok
            blocks = {'arabic': [ar], 'indonesian': [idn], 'javanese': [jv], 'english': [en]}
        elif '-->' in ar:  # Baris waktu
            for lang, line in zip(blocks.keys(), [ar, idn, jv, en]):
                blocks[lang].append(line)
        else:  # Baris teks subtitle
            for lang, line in zip(blocks.keys(), [ar, idn, jv, en]):
                blocks[lang].append(line)

    # Tambahkan blok terakhir
    if all(blocks.values()):
        combined_text = ' || '.join([blocks['arabic'][2], blocks['indonesian'][2], blocks['javanese'][2], blocks['english'][2]])
        combined_srt.append(f"{blocks['arabic'][0]}\n{blocks['arabic'][1]}\n{combined_text}\n")

    return combined_srt

def update_time_intervals(time_intervals, durasiMax):
    # Sisipkan elemen 0 di awal
    time_intervals.insert(0, 0)
    # Tambahkan durasiMax di akhir
    time_intervals.append(durasiMax)
    return time_intervals

def get_mp3_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length  # Mengembalikan durasi dalam detik

# Memuat file SRT dari setiap bahasa dan menambahkan Bismillah
srt_content = {lang: add_bismillah(load_srt(path), lang) for lang, path in srt_files.items()}

# Menambahkan label ayat pada teks Arab saja
srt_content['arabic'] = add_verse_labels_arabic(srt_content['arabic'])

# Daftar waktu yang diberikan oleh user dalam format detik
time_intervals = [11, 24, 38]  # Durasi dalam detik

# Contoh penggunaan
file_path = "audio/108AlKautsar.mp3"
file_path_save_srt_file = "dataset/srt/surah_al_kautsar_combined14.srt"

# Dapatkan durasi file MP3
duration = get_mp3_duration(file_path)

# Mulai pengukuran waktu
start_time = time.time()

# Gabungkan semua terjemahan
combined_srt_content = combine_translations(*srt_content.values())

# Ganti interval waktu dalam SRT gabungan
updated_srt_content = replace_srt_intervals(combined_srt_content, update_time_intervals(time_intervals, duration))

# Tulis ke file SRT gabungan yang diperbarui
combined_srt_file = file_path_save_srt_file
with open(combined_srt_file, 'w', encoding='utf-8') as file:
    file.write(''.join(updated_srt_content))
                                            
# Hitung waktu yang diperlukan
elapsed_time = time.time() - start_time

# Output hasil
print(f'Combined SRT file created: {combined_srt_file}')
print(f'Time taken for combining: {elapsed_time:.4f} seconds')
