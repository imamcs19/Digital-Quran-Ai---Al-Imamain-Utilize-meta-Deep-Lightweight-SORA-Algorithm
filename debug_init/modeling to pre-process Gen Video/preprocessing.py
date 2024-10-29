import pandas as pd
import json
from collections import OrderedDict

# Deklarasi variabel umum
input_no_surah = 108
# path_file_json = "dataset/info_audio/data_init_audio.json"

# topk_pada_dataset = 15
# topk_pada_hasil_target = 5  # Misalnya, ambil 5 nilai tertinggi

# n_input = 475   # Jumlah kolom yang akan diambil
# input_file_path = 'dataset/quran_json_ekstrak/dataset_translations-top_15_to_model_v1.xlsx'
# sheet_name = 'list_model_comb_all_unique'

def get_info_audio(input_no_surah):
    # Load data dari file JSON
    with open("dataset/info_audio/data_init_audio.json", 'r') as json_file:
        data_init = json.load(json_file)

    # Mengambil data berdasarkan input_no_surah
    key = f"key{input_no_surah}"
    if key in data_init:
        audio_data = data_init[key]
        
        # Mengambil audio_name
        audio_name = audio_data['audio_name']
        file_path_mp3 = f"dataset/Alquran + Terjemahan/{audio_name}"
        
        # Mengambil srt dan membentuk path file srt
        srt_file_name = audio_data['srt']
        file_path_save_srt_file = f"dataset/srt/{srt_file_name}"
        
        # Mengambil time_intervals_fund dan time_intervals_complete
        time_intervals_fund = audio_data['time_intervals_fund']
        time_intervals_complete = audio_data['time_intervals_complete']
        
        # Mengambil durasi dari time_intervals_complete
        duration = time_intervals_complete[-1]  # Mengambil durasi sebagai nilai terakhir
        
        total_ayah = audio_data['total_ayah']

        # Output untuk verifikasi
        # print("Time Intervals Fund:", time_intervals_fund)
        # print("Time Intervals Complete:", time_intervals_complete)
        # print("MP3 File Path:", file_path_mp3)
        # print("SRT File Path:", file_path_save_srt_file)
        # print("Duration:", duration)
        # print("Total Ayah:", total_ayah)
    else:
        print(f"Data untuk key '{key}' tidak ditemukan.")
        
    return file_path_mp3, file_path_save_srt_file, time_intervals_fund, duration, total_ayah    

def get_bg_resource(input_no_surah, time_intervals):
    
    n_input = 475   # Jumlah kolom yang akan diambil
    n_output = 114
    input_file_path = 'dataset/quran_json_ekstrak/dataset_translations-top_15_to_model_v1.xlsx'
    sheet_name = 'list_model_comb_all_unique'
    
    # Fungsi utama untuk memuat dan memproses data berdasarkan parameter yang diberikan
    def get_data_test(input_no_surah, jenis_top_k):
        # print('input_no_surah = ', input_no_surah)
        # Membuat path file JSON sesuai input_no_surah
        input_file_path_json = f'dataset/quran_json_ekstrak/output_{input_no_surah}.json'

        # Memuat file Excel dan menghapus kolom yang tidak dibutuhkan
        df = pd.read_excel(input_file_path, sheet_name=sheet_name)
        # df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Menghapus kolom "Unnamed"
        # Menghapus kolom "Unnamed: 0" jika ada
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])

        # Menyimpan DataFrame ke dalam dictionary dataframes
        dataframes = {sheet_name: df}

        # Mendapatkan header dari sheet
        header_example_sheet = dataframes[sheet_name]
        num_of_terms = header_example_sheet.shape[1] - 114  # Menghitung jumlah kolom terms sebelum 114 kolom terakhir
        list_term_header_sheet = header_example_sheet.columns[:num_of_terms].tolist()

        # Membaca data dari file JSON
        with open(input_file_path_json, 'r') as json_file:
            json_data = json.load(json_file)

        # Mendapatkan terms dari JSON untuk jenis_text_trans_tafsir dan jenis_top_k
        terms_data_row = {item[0] for item in json_data["translations"]["top_frequencies"][f"top_{jenis_top_k}"]}

        # Membuat list data_test_row berdasarkan list_term_header_sheet
        data_test_row = [1 if term in terms_data_row else 0 for term in list_term_header_sheet]

        # Menampilkan hasil
        # print(f"Data Test Row untuk jenis '{jenis_text_trans_tafsir}', input_no_surah '{input_no_surah}', dan top_k '{jenis_top_k}':")
        # print(data_test_row)
        return data_test_row

    def get_y_gt(input_no_surah):
        # Memuat file Excel
        df = pd.read_excel(input_file_path, sheet_name=sheet_name)

        # Menghapus kolom "Unnamed: 0" jika ada
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Hapus semua kolom yang namanya mengandung 'Unnamed'

        # Ambil baris sesuai input_no_surah, dan 114 kolom terakhir
        y_gt_row = df.iloc[input_no_surah - 1, -n_output:]  # Indeks dimulai dari 0, jadi kurangi 1
        y_gt = y_gt_row.tolist()  # Mengonversi ke dalam bentuk list

        return y_gt

    # Contoh penggunaan fungsi
    # jenis_text_trans_tafsir = 'translations' # 'text' atau 'translations' atau 'tafsir'
    # input_no_surah = 108
    topk_pada_dataset = 15
    data_test_row = get_data_test(input_no_surah, topk_pada_dataset)

    test_data = data_test_row  # Contoh data uji
    # print("Data Uji: ")  # Tampilkan data uji
    # print(test_data)
    # print('panjang fitur input = ',len(test_data))
    print('Data no. surah = ',input_no_surah)
    print()

    # List model yang akan diuji
    list_model = ['model_list_model_comb_all_unique', 'model_list_model_sheet1', 'model_list_model_sheet2', 'model_list_model_sheet3']
    topk_pada_hasil_target = 5  # Misalnya, ambil 5 nilai tertinggi

    y_true_test_data = get_y_gt(input_no_surah)


    def test_single_data_return_loss(model, X_tensor, y_true):
        model.eval()
        with torch.no_grad():
            predictions = model(torch.FloatTensor(X_tensor))
            mse_loss = nn.MSELoss()(predictions, torch.FloatTensor(y_true))
            # print(f'Testing Loss: {mse_loss.item()}')

        return mse_loss.item()

    def test_single_data_return_pred(model, single_data_test):
        model.eval()  # Set model ke mode evaluasi
        with torch.no_grad():  # Matikan gradient calculation
            input_tensor = torch.FloatTensor(single_data_test).unsqueeze(0)  # Tambahkan dimensi batch
            prediction = model(input_tensor)  # Lakukan prediksi
            # print(f"Data Uji: {single_data}")  # Tampilkan data uji
            # print(f"Hasil Regresi: {prediction.numpy().flatten()}")  # Tampilkan hasil regresi

        return prediction.numpy().flatten()

    # Fungsi untuk mendapatkan nilai dan indeks tertinggi dari hasil prediksi
    def get_topk_values_and_indices(predictions, topk):
        top_values, top_indices = torch.topk(torch.FloatTensor(predictions), topk)
        return top_values.numpy(), top_indices.numpy()

    # List untuk menyimpan semua pasangan nilai dan indeks dari tiap model
    all_top_values_indices = []
    # all_top_indices = []

    # Loop untuk memuat model, menjalankan prediksi, dan mengambil top-K indeks dari hasil prediksi
    for model_name in list_model:
        # Inisialisasi model dan memuat parameter dari file JSON
        elm_model = ELMRegression(n_input, n_hidden1, n_hidden2, n_output)
        model_path = f'output_model/{model_name}.json'
        load_model_json(model_path, elm_model)

        # Jalankan prediksi untuk satu data uji
        hasil_pred = test_single_data_return_pred(elm_model, test_data)
        # print(f"Hasil Regresi: {hasil_pred}") 
        # print(f"Panjang dim Hasil Regresi: {len(hasil_pred)}") 

        # test_single_data
        nilai_loss = test_single_data_return_loss(elm_model, test_data, y_true_test_data)
        # print(f"Hasil nilai loss: {nilai_loss}") 

        # Dapatkan top-K nilai dan indeks dari hasil prediksi
        top_values, top_indices = get_topk_values_and_indices(hasil_pred, topk_pada_hasil_target)
        # print(f"Top-{topk} values for {model_name}: {top_values}")
        # print(f"Top-{topk} indices for {model_name}: {top_indices}")

        # tipe output 1 => Tambahkan pasangan nilai dan indeks ke dalam daftar, untuk base descending
        all_top_values_indices.extend(zip(top_values, top_indices))

        # # tipe output 2 => Tambahkan indeks ke daftar semua indeks, tanpa base desc, hanyak topk tiap model
        # all_top_indices.extend(top_indices)

    # ------------------------
    # untuk tipe output 1:
    # ------------------------
    # Tambahkan nilai input_no_surah (dengan nilai prediksi yang pasti dimasukkan)
    all_top_values_indices.append((1.0, input_no_surah))

    # Urutkan semua pasangan berdasarkan nilai secara descending dan ambil indeks unik + dari input_no_surah
    sorted_unique_indices = sorted(set(all_top_values_indices), key=lambda x: x[0], reverse=True)
    unique_top_indices_type1 = [int(index) for _, index in sorted_unique_indices]

    # Menghapus duplikat dengan mempertahankan urutan
    unique_indices_preserving_order = list(OrderedDict.fromkeys(unique_top_indices_type1))

    # Menampilkan hasil
    # print()
    # print("Unique top indices - type 1 :", unique_indices_preserving_order)

    # Deklarasi variabel path list dan direktori utama
    list_path_bg = unique_indices_preserving_order
    main_dir = 'dataset/bg_object'
    # time_intervals = [0, 1, 2, 3, 4, 5]  # Contoh daftar interval waktu
    bank_of_background_options = ['static_image', 'audio_wave_animation', 'animated_from_static_image', 'animated_from_gif_webp_image', 'animated_from_video']
    bank_of_transition_types = ['curtains', 'fade', 'wipe', 'push', 'split', 'random_bars']

    # Dictionary untuk menyimpan file path lengkap dari setiap file di direktori sesuai list_path_bg
    list_files_by_dir = {}

    # Looping melalui setiap item dalam list_path_bg
    for dir_num in list_path_bg:
        # Key dalam format "list_path_bg_<dir_num>"
        key = f"list_path_bg_{dir_num}"
        list_files_by_dir[key] = []  # Inisialisasi sebagai list kosong

        # Path direktori
        dir_path = os.path.join(main_dir, str(dir_num))

        # Cek apakah direktori ada
        if os.path.exists(dir_path):
            # Dapatkan semua file di dalam direktori dan tambahkan path lengkap ke list dalam key
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                if os.path.isfile(file_path):
                    list_files_by_dir[key].append(file_path)  # Tambahkan path lengkap file ke list pada key yang sesuai
        else:
            print(f"Direktori {dir_path} tidak ditemukan.")  # Informasi jika direktori tidak ada

    # Menggabungkan semua isi dari files ke dalam satu list
    merged_files = []
    weights = []  # List untuk menyimpan bobot masing-masing direktori
    total_files = 0  # Total semua file untuk persentase prioritas

    # Assign bobot berdasarkan urutan elemen pada list_path_bg
    for idx, (key, files) in enumerate(list_files_by_dir.items()):
        priority_weight = max(1, len(list_path_bg) - idx)  # Bobot lebih tinggi di elemen awal
        weights.extend([priority_weight] * len(files))  # Tambahkan bobot ke list untuk tiap file dalam direktori
        merged_files.extend(files)  # Menggabungkan isi files ke merged_files

    # Pilih file secara acak dari merged_files berdasarkan bobot prioritas
    image_paths = random.choices(merged_files, weights=weights, k=len(time_intervals))

    # Generate background_options berdasarkan ekstensi file di image_paths
    background_options = []
    for file_path in image_paths:
        ext = os.path.splitext(file_path)[-1].lower()  # Ambil ekstensi file dalam lowercase
        if ext in ['.gif', '.webp']:
            background_options.append(random.choice(['animated_from_gif_webp_image', 'animated_from_video']))
        elif ext == '.mp4':
            background_options.append('animated_from_video')
        elif ext in ['.jpg', '.png']:
            background_options.append(random.choice(['animated_from_static_image', 'static_image']))
        else:
            background_options.append('static_image')  # Default jika ekstensi tidak sesuai bank_of_background_options

    # Generate transition_types berdasarkan nilai background_options
    transition_types = [
        random.choice(bank_of_transition_types) if option == 'animated_from_static_image' else 'fade'
        for option in background_options
    ]
    
    return unique_indices_preserving_order, image_paths, background_options, transition_types

