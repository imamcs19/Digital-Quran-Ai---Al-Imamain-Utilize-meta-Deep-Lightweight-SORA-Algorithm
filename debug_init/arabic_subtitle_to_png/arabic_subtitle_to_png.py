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
def generate_image(text, font_path, output_image_path, screen_size, alignment='right', shadow_color=(128, 128, 128), shadow_thickness=3, padding=20, vertical_offset=30):
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

# Konfigurasi jalur font, teks Arab, dan ukuran layar pengguna
# Path to the custom font (make sure it exists on your system)
# font_path ="/Users/imamcs/Library/Fonts/Tajawal-Regular.ttf"
# font_path="/Users/imamcs/Library/Fonts/traditional-arabic.ttf"
# font_path="/Users/imamcs/Library/Fonts/Amiri-Regular.ttf"
# font_path="/Users/imamcs/Library/Fonts/ZekrQuran.ttf" # => look good enough
font_path="/Users/imamcs/Library/Fonts/LPMQ IsepMisbah.ttf" # => In Syaa Allah almost perfect


# Arabic text to render
# arabic_text = "يَكَادُ الْبَرْقُ يَخْطَفُ اَبْصَارَهُمْ ۗ كُلَّمَآ اَضَاۤءَ لَهُمْ مَّشَوْا فِيْهِ ۙ وَاِذَآ اَظْلَمَ عَلَيْهِمْ قَامُوْا ۗوَلَوْ شَاۤءَ اللّٰهُ لَذَهَبَ بِسَمْعِهِمْ وَاَبْصَارِهِمْ ۗ اِنَّ اللّٰهَ عَلٰى كُلِّ شَيْءٍ قَدِيْرٌ ࣖ"
arabic_text = "۞ اِنَّ اللّٰهَ لَا يَسْتَحْيٖٓ اَنْ يَّضْرِبَ مَثَلًا مَّا بَعُوْضَةً فَمَا فَوْقَهَا ۗ فَاَمَّا الَّذِيْنَ اٰمَنُوْا فَيَعْلَمُوْنَ اَنَّهُ الْحَقُّ مِنْ رَّبِّهِمْ ۚ وَاَمَّا الَّذِيْنَ كَفَرُوْا فَيَقُوْلُوْنَ مَاذَآ اَرَادَ اللّٰهُ بِهٰذَا مَثَلًا ۘ يُضِلُّ بِهٖ كَثِيْرًا وَّيَهْدِيْ بِهٖ كَثِيْرًا ۗ وَمَا يُضِلُّ بِهٖٓ اِلَّا الْفٰسِقِيْنَۙ"
# screen_size = "إِيَّاكَ نَعۡبُدُ وَإِيَّاكَ نَسۡتَعِينُ"
# screen_size = "اِيَّاكَ نَعْبُدُ وَاِيَّاكَ نَسْتَعِيْنُۗ"
screen_size = (1920, 1080)

# Panggil fungsi untuk membuat gambar
generate_image(arabic_text, font_path, 'temp/output-arabic-aligned_3.png', screen_size, alignment='center', shadow_color=(50, 50, 50), shadow_thickness=5, vertical_offset=30)
