import numpy as np
# from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips, vfx
import matplotlib.pyplot as plt
import tempfile
import os
from pydub import AudioSegment
from mutagen.mp3 import MP3
import pysrt  # Untuk memproses file SRT
from moviepy.config import change_settings
import time
import json
from datetime import datetime
import pytz

from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import textwrap

# from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, vfx
import random

# Set path ke ImageMagick
change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/magick"})

# Fungsi untuk mendapatkan durasi MP3
def get_mp3_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length  # Mengembalikan durasi dalam detik

def get_unique_json_filename(quality, audio_file_path):
    # Membuat string timestamp dengan timezone Asia/Jakarta
    timezone = pytz.timezone('Asia/Jakarta')
    name_unik = datetime.today().astimezone(timezone).strftime('%d-%m-%Y-%H-%M-%S')
    
    # Mendapatkan nama file mp3 tanpa ekstensi
    filename = get_filename(audio_file_path)
    
    # Membuat info parameter dan nama final untuk file JSON
    info_param = f'q-{quality}-file-{filename}'
    name_unik_final = f'./log_computation/{info_param}-{name_unik}.json'
    
    name_unik_json = name_unik_final
    name_unik_untuk_video = name_unik
    
    # Membuat folder log_computation jika belum ada
    if not os.path.exists('./log_computation'):
        os.makedirs('./log_computation')
    
    return name_unik_json, name_unik_untuk_video


def save_computation_time(data, output_json_path):
    if not os.path.exists(output_json_path):
        with open(output_json_path, 'w') as f:
            json.dump([], f, indent=4)

    with open(output_json_path, 'r+') as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
        
        # Tambahkan data baru
        existing_data.append(data)
        
        # Simpan kembali file JSON
        f.seek(0)
        json.dump(existing_data, f, indent=4)

# Fungsi untuk membuat animasi gelombang suara dari file audio
def generate_wave_animation(audio_path, duration):
    fps=24
    audio = AudioSegment.from_file(audio_path)
    samples = np.array(audio.get_array_of_samples())

    # Ambil satu saluran jika audio stereo
    if audio.channels == 2:
        samples = samples[::2]

    # Normalisasi amplitudo audio
    max_amplitude = np.max(np.abs(samples))
    if max_amplitude == 0:
        raise ValueError("Data audio tidak memiliki amplitudo, tidak bisa membuat animasi.")

    samples = samples / max_amplitude

    frames = []
    # duration = len(samples) / audio.frame_rate

    if duration <= 0:
        raise ValueError("Durasi audio tidak valid. Tidak bisa membuat animasi.")

    samples_per_frame = max(1, int(len(samples) / (fps * duration)))

    # Membuat setiap frame dari gelombang audio
    for i in range(0, len(samples), samples_per_frame):
        frame_data = samples[i:i + samples_per_frame]
        plt.figure(figsize=(8, 4))
        plt.plot(frame_data, color='blue')
        plt.ylim([-1, 1])
        plt.axis('off')

        # Simpan frame sementara di memori
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_file.name)
        plt.close()
        frames.append(temp_file.name)

    # Menghasilkan klip gambar dari frame yang dibuat
    clips = [ImageClip(f).set_duration(1/fps) for f in frames]
    animation = concatenate_videoclips(clips, method="compose")

    # Hapus file sementara
    for f in frames:
        os.remove(f)

    return animation

def create_background(size, background_option, transition_type, image_path, audio_file_path, duration):

    if background_option == 'static_image':
        return ImageClip(image_path).set_duration(duration).resize(size)

    elif background_option == 'animated_from_static_image':
        # Tambahkan variasi transisi
        clip = ImageClip(image_path).set_duration(duration).resize(size)
        
        # Menerapkan transisi berdasarkan jenis transisi yang diberikan
        if transition_type == 'curtains':
            # Transisi curtains
            return clip.fadein(duration / 2).fadeout(duration / 2)
#         elif transition_type == 'drape':
#             return clip.fx(vfx.slide_in, duration=1, side='bottom')
#         elif transition_type == 'airplane':
#             return clip.fx(vfx.slide_in, duration=1, side='left')

#         elif transition_type == 'origami':
#             # Tidak ada transisi origami langsung di MoviePy, ini adalah penggantinya dengan "slide_in"
#             return clip.fx(vfx.slide_in, duration=1, side='right')
            
        elif transition_type == 'fade':
            return clip.crossfadein(1)
            
#         elif transition_type == 'wipe':
#             # Mendekati transisi wipe dengan slide dari kanan ke kiri
#             return clip.fx(vfx.slide_in, duration=1, side='left')

#         elif transition_type == 'morph':
#             return clip.fx(vfx.fadein, duration=1)
        elif transition_type == 'wipe':
            # Transisi wipe
            return clip.crossfadein(duration / 2)
        elif transition_type == 'push':
            # Transisi push (dapat menggunakan efek translasi)
            return clip.set_position(lambda t: ('center', -100 + t * 50))
        elif transition_type == 'split':
            # Transisi split
            return clip.set_position(lambda t: ('center', 100 - t * 50))
        elif transition_type == 'reveal':
            # Transisi reveal
            return clip.set_opacity(lambda t: min(1, max(0, t / duration)))
        elif transition_type == 'random_bars':
            # Random bars transition
            return clip.set_position(lambda t: (random.randint(-50, 50), random.randint(-50, 50)))
        # Tambahkan transisi lainnya...
        else:
            # Default transition
            return clip.fadein(1).fadeout(1)
    elif background_option == 'animated_from_gif_webp_image':
         if image_path.lower().endswith(('.gif', '.webp')):
            background_clip = VideoFileClip(image_path).subclip(0, duration)
            
    elif background_option == 'animated_from_video':
         if image_path.lower().endswith(('.mp4')):
            background_clip = VideoFileClip(image_path).subclip(0, duration)
            
    elif background_option == 'audio_wave_animation':
        # Untuk 'audio_wave_animation', kita cek jika ada gambar statis yang digunakan sebagai background
        if image_path and image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            # Menggunakan gambar statis sebagai latar belakang
            static_background = ImageClip(image_path, duration=duration).resize(size)
        else:
            # Jika tidak ada gambar statis, menggunakan latar belakang warna default (misal, hitam)
            static_background = ImageClip(color=(0, 0, 0), duration=duration, size=size)
        
        # Menggunakan animasi wave dari audio
        wave_animation = generate_wave_animation(audio_file_path, duration).resize(size)
        
        # Menggabungkan background statis dengan animasi wave
        background_clip = static_background.set_duration(duration).set_opacity(1).set_position("center").fx(lambda clip: wave_animation)
        
    elif background_option == 'color':
        return ColorClip(size, color=(255, 255, 255)).set_duration(duration)

def calculate_font_size(video_size):

    # Menggunakan tinggi video untuk menentukan ukuran font yang proporsional
    height = video_size[1]

    # Ukuran font akan proporsional dengan tinggi video (sekitar 1/15 dari tinggi video)
    font_size = max(16, int(height / 15))  # Menetapkan ukuran minimal agar tidak terlalu kecil

    return font_size

def add_subtitles(video, srt_path, video_size, i_segment, font_color='white', shadow_color='gray', font='Amiri-Bold.ttf'):
    font_size = calculate_font_size(video_size)/1.5  # Menyesuaikan ukuran font berdasarkan ukuran video
    subs_v1 = load_srt(srt_path)
    subs = parse_srt(subs_v1)
    subtitle_clips = []
    
    video_width, video_height = video_size
    
    # Menghitung max_width sebagai 70% dari lebar video untuk HD
    # max_width = int(video_width * 0.7)/14
    max_width = int(video_width * 0.05)
    
     # Menghitung max_width sebagai 70% dari lebar video untuk 360p
    # max_width = int(video_width * 0.10)
    
    # Menghitung stroke_width berdasarkan lebar video (misalnya 1% dari lebar video)
    stroke_width_in = max(1, int(video_width * 0.01)/6)
    
    # print('max_width =', max_width)
    # print('stroke_width_in =', stroke_width_in)
    
    for sub in subs[i_segment:i_segment+1]:
        
        duration_in_clip = sub['duration']

        if duration_in_clip > 0:
            # Auto-wrap teks subtitle
            wrapped_text = textwrap.fill(sub['text'], width=max_width)

            # Membuat teks subtitle dengan font bold dan auto-wrap
            txt_clip = TextClip(wrapped_text, fontsize=font_size, color=font_color, stroke_color=shadow_color, stroke_width=stroke_width_in, font=font)\
                        .set_position(('center', 'bottom'))\
                        .set_duration(duration_in_clip)\
                        .set_start(0)

            subtitle_clips.append(txt_clip)

    video_with_subs = CompositeVideoClip([video] + subtitle_clips)
    
    return video_with_subs

def generate_video(input_str_path, audio_file_path, quality, background_options_list, transition_types_list, output_path, time_intervals, image_paths=None):
    
    start_time = time.time()  # Waktu mulai untuk generate_video
    
    audio = AudioFileClip(audio_file_path)

    if audio.duration is None or audio.duration <= 0:
        raise ValueError("Durasi audio tidak valid atau nol. Periksa file audio.")

    resolutions = {
        "114p": (200, 114),
        "240p": (426, 240),
        "360p": (640, 360),
        "HD": (1280, 720)
    }

    size = resolutions.get(quality, resolutions["HD"])
    
    # print('size = ', size)
    
    # Dapatkan nama file JSON dan video yang unik
    json_filename, name_unik_untuk_video = get_unique_json_filename(quality, audio_file_path)

    clips = []
    previous_time = 0

    for i, interval in enumerate(time_intervals):
        if interval is None or interval < 0:
            raise ValueError(f"Interval waktu tidak valid pada indeks {i}: {interval}. Semua interval harus positif.")

        background_option = background_options_list[i] if i < len(background_options_list) else background_options_list[-1]
        image_path = image_paths[i] if image_paths and i < len(image_paths) else None

        if previous_time < audio.duration:
            clip_duration = interval - previous_time

            if clip_duration < 0:
                raise ValueError(f"Durasi klip negatif pada interval {interval}. Periksa daftar interval.")

            clip_duration = min(clip_duration, audio.duration - previous_time)

            if clip_duration <= 0:
                previous_time = interval
                continue

            duration_per_clip = clip_duration  # Durasi tiap klip sesuai jumlah background
            background_clip = create_background(size, background_option, transition_types_list[i], image_path, audio_file_path, duration_per_clip)
            segment_with_subs = add_subtitles(background_clip, input_str_path, size, i)

            # clips.append(background_clip)
            clips.append(segment_with_subs)
            previous_time = interval

    if clips:
        final_video = concatenate_videoclips(clips, method="compose").set_audio(audio)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_filename = os.path.join(output_path, f'{get_filename(audio_file_path)}_output_{quality}_{name_unik_untuk_video}.mp4')

        fps = 24
        final_video.write_videofile(output_filename, codec='libx264', audio_codec='aac', fps=fps)

        audio.close()
        final_video.close()
        
        # Waktu selesai untuk generate_video
        end_time = time.time()
        
        # Simpan waktu komputasi dan parameter ke dalam file JSON
        computation_data = {
            'function': 'generate_video',
            'start_time': start_time,
            'end_time': end_time,
            'duration': f"{end_time - start_time} seconds",  # Menambahkan satuan waktu detik
            'params': {
                'input_str_path': input_str_path,
                'audio_file_path': audio_file_path,
                'quality': quality,
                'background_options_list': background_options_list,
                'output_path': output_path,
                'time_intervals': time_intervals,
                'image_paths': image_paths,
                'video_size': size
            }
        }

        # Dapatkan nama file JSON yang unik
        # json_filename = get_unique_json_filename(quality, audio_file_path)
        save_computation_time(computation_data, json_filename)
        
        print('time computation = ', end_time - start_time, 'seconds')
        
    else:
        raise ValueError("Tidak ada segmen video yang valid. Periksa input interval.")


def get_filename(file_path):
    # Mengambil nama file dari path
    filename_with_extension = os.path.basename(file_path)
    
    # Menghilangkan ekstensi .mp3 dari nama file
    filename = os.path.splitext(filename_with_extension)[0]
    
    return filename

def create_intervals(time_intervals, durasi):
    # Inisialisasi list dengan nilai pertama dari time_intervals
    list_intervals = [time_intervals[0]]
    
    # Mengisi nilai untuk indeks selain 0
    for i in range(1, len(time_intervals)):
        list_intervals.append(time_intervals[i] - time_intervals[i-1])
    
    # Menghitung nilai terakhir sebagai durasi - nilai terakhir dari time_intervals
    list_intervals.append(durasi - time_intervals[-1])
    
    return list_intervals

# Fungsi untuk memuat konten SRT dari file
def load_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Fungsi untuk menghitung selisih waktu dalam detik
def calculate_duration(start_time, end_time):
    # Format waktu SRT: '00:00:00,000'
    time_format = '%H:%M:%S,%f'
    
    # Mengonversi string waktu ke objek datetime
    start_dt = datetime.strptime(start_time, time_format)
    end_dt = datetime.strptime(end_time, time_format)
    
    # Menghitung selisih waktu dalam detik
    duration = (end_dt - start_dt).total_seconds()
    return duration

# Fungsi untuk menghitung waktu mulai dalam detik
def calculate_start_time_in_seconds(start_time):
    time_format = '%H:%M:%S,%f'
    start_dt = datetime.strptime(start_time, time_format)
    # Menghitung total detik sejak 00:00:00
    return start_dt.hour * 3600 + start_dt.minute * 60 + start_dt.second + start_dt.microsecond / 1e6

# Fungsi untuk mendapatkan waktu mulai, waktu akhir, durasi, dan isi subtitle
def parse_srt(srt_content):
    parsed_subs = []
    time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
    
    current_sub = {}
    for line in srt_content:
        # Cek apakah baris ini berisi waktu mulai dan akhir
        match = time_pattern.match(line)
        if match:
            current_sub['start'] = match.group(1)
            current_sub['end'] = match.group(2)
            
            # Menghitung durasi dan waktu mulai dalam detik
            current_sub['duration'] = calculate_duration(current_sub['start'], current_sub['end'])
            current_sub['start_time_in_seconds'] = calculate_start_time_in_seconds(current_sub['start'])
        elif line.isdigit():
            # Lewati baris yang berisi nomor urutan subtitle
            continue
        else:
            # Baris lain dianggap sebagai isi subtitle
            current_sub['text'] = line
            parsed_subs.append(current_sub)
            current_sub = {}  # Reset untuk subtitle berikutnya
    return parsed_subs
        
# Contoh penggunaan
file_path_mp3 = "audio/108AlKautsar.mp3"
# file_path_save_srt_file = "srt/surah_al_kautsar_combined9.srt"
file_path_save_srt_file = "srt/surah_al_kautsar_non_arabic.srt"

# Menghitung durasi MP3 dan membuat video
duration = get_mp3_duration(file_path_mp3)
time_intervals = [11, 24, 38, duration]

# background_options = ['static_image', 'audio_wave_animation', \
#                       'animated_from_static_image', 'animated_from_gif_webp_image', \
#                       'animated_from_video']

background_options = ['static_image', 'static_image', \
                      'animated_from_static_image', 'animated_from_static_image']
transition_types = ['fade', 'origami', 'airplane', 'curtains']
image_paths = ['img/108AlKautsar/1.png'] * 4

# generate_video(file_path_save_srt_file, file_path_mp3, "360p", background_options, transition_types, "output_videos/", time_intervals, image_paths)
generate_video(file_path_save_srt_file, file_path_mp3, "HD", background_options, transition_types, "output_videos/", time_intervals, image_paths)
