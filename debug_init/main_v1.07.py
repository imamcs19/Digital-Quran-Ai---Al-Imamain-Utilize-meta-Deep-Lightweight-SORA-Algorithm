from PIL import Image as pil
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from pkg_resources import parse_version

if parse_version(pil.__version__)>=parse_version('11.0.0'):
    Image.ANTIALIAS=Image.LANCZOS
    
import numpy as np
import regex as re
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


import arabic_reshaper
from bidi.algorithm import get_display
# import textwrap
# from moviepy.editor import TextClip, CompositeVideoClip

# import arabic_reshaper
# from bidi.algorithm import get_display
# import textwrap
# from moviepy.editor import TextClip, CompositeVideoClip
# from PIL import Image, ImageDraw, ImageFont
# import os

from __future__ import unicode_literals

import unittest
import sys
from arabic_reshaper import ArabicReshaper
# from bidi.algorithm import get_display


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
    brightness_factor = 0.5  # Faktor untuk mengurangi kecerahan (0.0 - 1.0)

    if background_option == 'static_image':
        try:
            # Menggunakan OpenCV untuk memuat gambar
            img = cv2.imread(image_path)

            # Jika gambar tidak berhasil dimuat, maka raise error
            if img is None:
                raise ValueError(f"Error: Gambar '{image_path}' tidak dapat dimuat. File mungkin rusak.")

            # Mengubah ukuran gambar sesuai ukuran yang diinginkan
            img = cv2.resize(img, size)

            # Mengonversi gambar BGR ke RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Membuat ImageClip dari gambar yang telah diproses
            background_clip = ImageClip(img_rgb).set_duration(duration)
            return background_clip.fx(vfx.colorx, brightness_factor)  # Terapkan efek kecerahan

        except Exception as e:
            raise ValueError(f"Error saat memuat file gambar '{image_path}': {e}")

    elif background_option == 'animated_from_static_image':
        try:
            # clip = ImageClip(image_path).set_duration(duration).resize(size)
            
            # Menggunakan OpenCV untuk memuat gambar
            img = cv2.imread(image_path)

            # Jika gambar tidak berhasil dimuat, maka raise error
            if img is None:
                raise ValueError(f"Error: Gambar '{image_path}' tidak dapat dimuat. File mungkin rusak.")

            # Mengubah ukuran gambar sesuai ukuran yang diinginkan
            img = cv2.resize(img, size)

            # Mengonversi gambar BGR ke RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Membuat ImageClip dari gambar yang telah diproses
            clip = ImageClip(img_rgb).set_duration(duration)
        
            # Menerapkan transisi berdasarkan jenis transisi yang diberikan
            if transition_type == 'curtains':
                return clip.fadein(duration / 2).fadeout(duration / 2).fx(vfx.colorx, brightness_factor)
            elif transition_type == 'fade':
                return clip.crossfadein(1).fx(vfx.colorx, brightness_factor)
            elif transition_type == 'wipe':
                return clip.crossfadein(duration / 2).fx(vfx.colorx, brightness_factor)
            elif transition_type == 'push':
                return clip.set_position(lambda t: ('center', -100 + t * 50)).fx(vfx.colorx, brightness_factor)
            elif transition_type == 'split':
                return clip.set_position(lambda t: ('center', 100 - t * 50)).fx(vfx.colorx, brightness_factor)
            elif transition_type == 'reveal':
                return clip.set_opacity(lambda t: min(1, max(0, t / duration))).fx(vfx.colorx, brightness_factor)
            elif transition_type == 'random_bars':
                return clip.set_position(lambda t: (random.randint(-50, 50), random.randint(-50, 50))).fx(vfx.colorx, brightness_factor)
            else:
                return clip.fadein(1).fadeout(1).fx(vfx.colorx, brightness_factor)
        except Exception as e:
            raise ValueError(f"Error saat memuat file gambar '{image_path}': {e}")
            
#     elif background_option == 'animated_from_static_image':
#         clip = ImageClip(image_path).set_duration(duration).resize(size)
        
#         # Menerapkan transisi berdasarkan jenis transisi yang diberikan
#         if transition_type == 'curtains':
#             return clip.fadein(duration / 2).fadeout(duration / 2).fx(vfx.colorx, brightness_factor)
#         elif transition_type == 'fade':
#             return clip.crossfadein(1).fx(vfx.colorx, brightness_factor)
#         elif transition_type == 'wipe':
#             return clip.crossfadein(duration / 2).fx(vfx.colorx, brightness_factor)
#         elif transition_type == 'push':
#             return clip.set_position(lambda t: ('center', -100 + t * 50)).fx(vfx.colorx, brightness_factor)
#         elif transition_type == 'split':
#             return clip.set_position(lambda t: ('center', 100 - t * 50)).fx(vfx.colorx, brightness_factor)
#         elif transition_type == 'reveal':
#             return clip.set_opacity(lambda t: min(1, max(0, t / duration))).fx(vfx.colorx, brightness_factor)
#         elif transition_type == 'random_bars':
#             return clip.set_position(lambda t: (random.randint(-50, 50), random.randint(-50, 50))).fx(vfx.colorx, brightness_factor)
#         else:
#             return clip.fadein(1).fadeout(1).fx(vfx.colorx, brightness_factor)

    elif background_option == 'animated_from_gif_webp_image':
        if image_path.lower().endswith('.gif'):
            try:
                background_clip = VideoFileClip(image_path)
                clip_duration = min(duration, background_clip.duration)
                return background_clip.subclip(0, clip_duration).resize(size).fx(vfx.colorx, brightness_factor)
            except Exception as e:
                raise ValueError(f"Error saat memuat file GIF '{image_path}': {e}")

        elif image_path.lower().endswith('.webp'):
            try:
                img = Image.open(image_path)
                
                if img.is_animated:
                    frames = []
                    for frame in range(img.n_frames):
                        img.seek(frame)
                        frame_image = img.copy().resize(size)
                        frames.append(frame_image)
                    
                    background_clip = ImageSequenceClip([frame for frame in frames], fps=10)
                    clip_duration = min(duration, background_clip.duration)
                    return background_clip.subclip(0, clip_duration).fx(vfx.colorx, brightness_factor)
                else:
                    background_clip = ImageClip(image_path).set_duration(duration).resize(size).fx(vfx.colorx, brightness_factor)
                    return background_clip

            except Exception as e:
                raise ValueError(f"Error saat memuat file WEBP '{image_path}': {e}")
                
    elif background_option == 'animated_from_video' and image_path.lower().endswith('.gif'):
        if image_path.lower().endswith('.gif'):
            try:
                background_clip = VideoFileClip(image_path)
                clip_duration = min(duration, background_clip.duration)
                return background_clip.subclip(0, clip_duration).resize(size).fx(vfx.colorx, brightness_factor)
            except Exception as e:
                raise ValueError(f"Error saat memuat file GIF '{image_path}': {e}")
                
    elif background_option == 'animated_from_video' and image_path.lower().endswith('.webp'):
        if image_path.lower().endswith('.webp'):
            try:
                img = Image.open(image_path)
                
                if img.is_animated:
                    frames = []
                    for frame in range(img.n_frames):
                        img.seek(frame)
                        frame_image = img.copy().resize(size)
                        frames.append(frame_image)
                    
                    background_clip = ImageSequenceClip([frame for frame in frames], fps=10)
                    clip_duration = min(duration, background_clip.duration)
                    return background_clip.subclip(0, clip_duration).fx(vfx.colorx, brightness_factor)
                else:
                    background_clip = ImageClip(image_path).set_duration(duration).resize(size).fx(vfx.colorx, brightness_factor)
                    return background_clip

            except Exception as e:
                raise ValueError(f"Error saat memuat file WEBP '{image_path}': {e}")

    elif background_option == 'animated_from_video' and image_path.lower().endswith('.mp4'):
        video_clip = VideoFileClip(image_path)
        video_duration = min(duration, video_clip.duration)  # Menyesuaikan durasi agar tidak melebihi durasi video
        background_clip = video_clip.subclip(0, video_duration).resize(size).fx(vfx.colorx, brightness_factor)
        return background_clip

    elif background_option == 'audio_wave_animation':
        if image_path and image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            static_background = ImageClip(image_path, duration=duration).resize(size, PIL.Image.Resampling.LANCZOS).fx(vfx.colorx, brightness_factor)
        else:
            static_background = ImageClip(color=(0, 0, 0), duration=duration, size=size).fx(vfx.colorx, brightness_factor)
        
        wave_animation = generate_wave_animation(audio_file_path, duration).resize(size, PIL.Image.Resampling.LANCZOS)
        background_clip = static_background.set_duration(duration).set_opacity(1).set_position("center").fx(lambda clip: wave_animation)

    elif background_option == 'color':
        return ColorClip(size, color=(255, 255, 255)).set_duration(duration).fx(vfx.colorx, brightness_factor)

    return None  # Jika tidak ada opsi yang cocok

def calculate_font_size(video_size):

    # Menggunakan tinggi video untuk menentukan ukuran font yang proporsional
    height = video_size[1]

    # Ukuran font akan proporsional dengan tinggi video (sekitar 1/15 dari tinggi video)
    font_size = max(16, int(height / 15))  # Menetapkan ukuran minimal agar tidak terlalu kecil

    return font_size


# ref:
# [0] https://stackoverflow.com/questions/74608140/pillow-not-recognizing-libraqm-installation-on-mac-os
      # step by step:
      # close all jupyter lab, stop Anaconda navigator, buka terminal
      # pip uninstall Pillow  
      # pip install --upgrade Pillow  --global-option="build_ext" --global-option="--enable-raqm"
      # brew install libraqm 
      # brew install freetype harfbuzz fribidi
      # lalu buka kembali Anaconda navigator, lalu run kembali jupyter lab
      # check di jupy lab, pastikan output-nya "True"
      #  import PIL.features
      #  print(PIL.features.check('raqm'))
      # 
      # done 
     
# Function to generate image with RTL text support and shadow
from PIL import Image, ImageDraw, ImageFont

# Membagi teks berdasarkan lebar maksimum
def wrap_text(draw, text, font, max_width):
    words = text.split(' ')
    lines, current_line = [], []
    
    for word in words:
        trial_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), trial_line, font=font)
        width = bbox[2] - bbox[0]
        
        if width > max_width and current_line:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

# Menghitung ukuran gambar dan posisi teks berdasarkan ukuran layar
def calculate_image_and_text_position(screen_width, screen_height, padding=20):
    image_width = int(screen_width * 0.8)
    image_height = int(screen_height * 0.6)
    return (image_width, image_height), (padding, padding)

# Menghitung posisi teks horizontal berdasarkan perataan
def calculate_text_position(alignment, image_width, line_width, padding):
    if alignment == 'left':
        return padding
    elif alignment == 'center':
        return (image_width - line_width) // 2
    elif alignment == 'right':
        return image_width - line_width - padding
    else:
        raise ValueError("Pilih 'left', 'center', atau 'right'.")

# Menghasilkan gambar dengan teks Arab dan bayangan
def create_png_from_text(text, font_path, output_image_path, screen_size, alignment='right', shadow_color=(128, 128, 128), shadow_thickness=3, padding=20, vertical_offset=30):
   
    image_size, text_position = calculate_image_and_text_position(screen_size[0], screen_size[1], padding)
    image = Image.new('RGBA', image_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype(font_path, 50)
    except IOError:
        print(f"Font tidak ditemukan di {font_path}.")
        return

    max_width = image_size[0] - 2 * padding
    wrapped_text = wrap_text(draw, text, font, max_width)
    y_offset = text_position[1] + vertical_offset  # Tambahkan offset vertikal di sini
    
    for line in wrapped_text:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x_offset = calculate_text_position(alignment, image_size[0], line_width, padding)
        
        for i in range(1, shadow_thickness + 1):
            draw.text((x_offset + i, y_offset + i), line, font=font, fill=shadow_color, direction='rtl')
        
        draw.text((x_offset, y_offset), line, font=font, fill=(255, 255, 255), direction='rtl')
        y_offset += 120

    image.save(output_image_path)
    print(f"Gambar disimpan di {output_image_path}")
    
    return output_image_path

def add_subtitles(video, srt_path, video_size, i_segment, font_color='white', shadow_color='gray', font='Amiri-Bold.ttf'):
    font_size = calculate_font_size(video_size) / 1.5  # Menyesuaikan ukuran font berdasarkan ukuran video
    subs_v1 = load_srt(srt_path)
    subs = parse_srt(subs_v1)
    subtitle_clips = []
    
    video_width, video_height = video_size
    
    
    # Menghitung stroke_width berdasarkan lebar video (misalnya 1% dari lebar video)
    stroke_width_in = max(1, int(video_width * 0.01) / 6)
    
    #     # Menghitung max_width sebagai 5% dari lebar video
#     max_width = int(video_width * 0.05)
    
    # Menghitung max_width sebagai 70% dari lebar video untuk HD
    #     # max_width = int(video_width * 0.7)/14
    #     max_width = int(video_width * 0.05)

    #      # Menghitung max_width sebagai 70% dari lebar video untuk 360p
    max_width = int(video_width * 0.10)

    #     # Menghitung stroke_width berdasarkan lebar video (misalnya 1% dari lebar video)
    #     stroke_width_in = max(1, int(video_width * 0.01)/6)
    
    for sub in subs[i_segment:i_segment + 1]:
        
        duration_in_clip = sub['duration']
        
        if duration_in_clip > 0:
            # Split teks subtitle berdasarkan "||"
            split_text = sub['text'].split("||")
            
            # Bagian pertama dari split sebagai teks utama
            main_text = split_text[0].strip()
            
            # Cetak main_text sebelum reshaping (untuk debug)
            print(f"Original Arabic Text: {main_text}")
            
            # Jika main_text berisi teks Arabic, lakukan reshaping dan RTL
            # reshaped_main_text = arabic_reshaper.reshape(main_text)  # Menyusun ulang huruf-huruf Arabic

            # bidi_main_text = get_display(reshaped_main_text)  # Menampilkan dalam urutan RTL yang benar
            

            # Menggabungkan teks setelah bagian pertama, dipisahkan oleh newline
            if len(split_text) > 1:
                # secondary_text = "\n".join(part.strip() for part in split_text[1:])
                secondary_text = "\U0001F42A".join(part.strip() for part in split_text[1:])
                
            else:
                secondary_text = None
            
            # Auto-wrap teks subtitle utama (yang sudah diubah ke format RTL jika Arabic)
            # wrapped_main_text = textwrap.fill(bidi_main_text, width=max_width)
            
            # Menghitung posisi vertikal di tengah (sepertiga dari atas video)
            middle_position = video_height / 3
            
            # Membuat teks subtitle untuk bagian pertama (Arabic RTL as image)
            # img_path = create_png_from_text(main_text, font_size, font, font_color, shadow_color, i_segment)
            shadow_color_main_text_rtl = (128,128,128)
            shadow_thickness_main_text_rtl = 3
            # img_path = create_png_from_text(main_text, font_size, font_path, font_color, i_segment, shadow_color_main_text_rtl, shadow_thickness_main_text_rtl)
            # img_path = create_png_from_text(main_text, font_size, font_color, i_segment, max_width, shadow_color_main_text_rtl, shadow_thickness_main_text_rtl)
            
            # Konfigurasi jalur font, teks Arab, dan ukuran layar pengguna
            # Path to the custom font (make sure it exists on your system)
            # font_path ="/Users/imamcs/Library/Fonts/Tajawal-Regular.ttf"
            # font_path="/Users/imamcs/Library/Fonts/traditional-arabic.ttf"
            # font_path="/Users/imamcs/Library/Fonts/Amiri-Regular.ttf"
            # font_path="/Users/imamcs/Library/Fonts/ZekrQuran.ttf" # => look good enough
            font_path_khusus_rtl = "/Users/imamcs/Library/Fonts/LPMQ IsepMisbah.ttf" # => In Syaa Allah almost perfect


            # Arabic text to render
            # arabic_text = "يَكَادُ الْبَرْقُ يَخْطَفُ اَبْصَارَهُمْ ۗ كُلَّمَآ اَضَاۤءَ لَهُمْ مَّشَوْا فِيْهِ ۙ وَاِذَآ اَظْلَمَ عَلَيْهِمْ قَامُوْا ۗوَلَوْ شَاۤءَ اللّٰهُ لَذَهَبَ بِسَمْعِهِمْ وَاَبْصَارِهِمْ ۗ اِنَّ اللّٰهَ عَلٰى كُلِّ شَيْءٍ قَدِيْرٌ ࣖ"
            # arabic_text = "۞ اِنَّ اللّٰهَ لَا يَسْتَحْيٖٓ اَنْ يَّضْرِبَ مَثَلًا مَّا بَعُوْضَةً فَمَا فَوْقَهَا ۗ فَاَمَّا الَّذِيْنَ اٰمَنُوْا فَيَعْلَمُوْنَ اَنَّهُ الْحَقُّ مِنْ رَّبِّهِمْ ۚ وَاَمَّا الَّذِيْنَ كَفَرُوْا فَيَقُوْلُوْنَ مَاذَآ اَرَادَ اللّٰهُ بِهٰذَا مَثَلًا ۘ يُضِلُّ بِهٖ كَثِيْرًا وَّيَهْدِيْ بِهٖ كَثِيْرًا ۗ وَمَا يُضِلُّ بِهٖٓ اِلَّا الْفٰسِقِيْنَۙ"
            # arabic_text = "إِيَّاكَ نَعۡبُدُ وَإِيَّاكَ نَسۡتَعِينُ"
            # arabic_text = "اِيَّاكَ نَعْبُدُ وَاِيَّاكَ نَسْتَعِيْنُۗ"
            screen_size = video_size

            # Panggil fungsi untuk membuat gambar
            img_path = create_png_from_text(main_text, font_path_khusus_rtl, 'temp/output-arabic-aligned_3.png', screen_size, 
                                            alignment='center', shadow_color=(50, 50, 50), shadow_thickness=5, vertical_offset=30)

            
            ## ========
            # Gunakan gambar PNG dalam ImageClip
            main_txt_clip = ImageClip(img_path).set_position(('center', video_height / 3))\
                                                .set_duration(duration_in_clip)\
                                                .set_start(0)

            subtitle_clips.append(main_txt_clip)
            
            # Jika ada teks tambahan, gabungkan dengan newline dan tambahkan di posisi bawah
            if secondary_text:
                wrapped_secondary_text = textwrap.fill(secondary_text, width=max_width)
                secondary_txt_clip = TextClip(wrapped_secondary_text, fontsize=font_size, color=font_color, stroke_color=shadow_color, stroke_width=stroke_width_in, font=font)\
                                     .set_position(('center', 'bottom'))\
                                     .set_duration(duration_in_clip)\
                                     .set_start(0)

                subtitle_clips.append(secondary_txt_clip)

    # Menggabungkan subtitle dengan video
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
        
## Start Using Manual Configuration
## --------------------------
# file_path_mp3 = "audio/108AlKautsar.mp3"
# file_path_save_srt_file = "dataset/srt/surah_al_kautsar_combined14.srt"

# # Menghitung durasi MP3 dan membuat video
# duration = get_mp3_duration(file_path_mp3)
# time_intervals = [11, 24, 38, duration]

# # background_options = ['static_image', 'audio_wave_animation', \
# #                       'animated_from_static_image', 'animated_from_gif_webp_image', \
# #                       'animated_from_video']

# background_options = ['static_image', 'static_image', \
#                       'animated_from_static_image', 'animated_from_static_image']
# transition_types = ['fade', 'origami', 'airplane', 'curtains']
# image_paths = ['img/108AlKautsar/1.png'] * 4

## End Using Manual Configuration
## --------------------------


## Start Using CAML Algorithm
## --------------------------
# input_no_surah = 108
# input_no_surah = 112
# input_no_surah = 113
input_no_surah = 114

file_path_mp3, file_path_save_srt_file, \
time_intervals, duration, total_ayah  = get_info_audio(input_no_surah)

print('file_path_mp3 = ', file_path_mp3)
print('file_path_save_srt_file = ', file_path_save_srt_file)
print('time_intervals = ', time_intervals)

unique_indices_bg_using_calm_algorihtm, \
image_paths, background_options, transition_types = get_bg_resource(input_no_surah, time_intervals)

print()

print('background_options = ', background_options)
print('len background_options = ', len(background_options))
print('transition_types = ', transition_types)
print('len transition_types = ', len(transition_types))
print('image_paths = ', image_paths)
print('len image_paths = ', len(image_paths))

# background_options =  ['animated_from_video', 'animated_from_video', 'animated_from_gif_webp_image', 'animated_from_gif_webp_image']
# transition_types =  ['fade', 'fade', 'fade', 'fade']
# image_paths =  ['dataset/bg_object/108/flower.mp4', 'dataset/bg_object/108/flower.mp4', 'dataset/bg_object/108/3.webp', 'dataset/bg_object/108/3.webp']

# background_options =  ['animated_from_gif_webp_image', 'animated_from_gif_webp_image', 'animated_from_video', 'animated_from_video']
# transition_types =  ['fade', 'fade', 'fade', 'fade']
# image_paths =  ['dataset/bg_object/108/2.webp', 'dataset/bg_object/108/2.webp', 'dataset/bg_object/108/fish.mp4', 'dataset/bg_object/108/fish.mp4']

# background_options =  ['animated_from_gif_webp_image', 'animated_from_video', 'animated_from_video', 'animated_from_static_image']
# transition_types =  ['fade', 'fade', 'fade', 'push']
# image_paths =  ['dataset/bg_object/108/3.webp', 'dataset/bg_object/108/2.webp', 'dataset/bg_object/108/1.webp', 'dataset/bg_object/108/5.jpg']

## End Using CAML Algorithm
## --------------------------

generate_video(file_path_save_srt_file, file_path_mp3, "360p", background_options, transition_types, "output_videos/", time_intervals, image_paths)
# generate_video(file_path_save_srt_file, file_path_mp3, "HD", background_options, transition_types, "output_videos/", time_intervals, image_paths)