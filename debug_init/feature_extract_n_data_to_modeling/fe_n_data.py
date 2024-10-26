## Ekstrak Fitur top K berdasar text (Quran arabic, tafsir, lalu terjemahan)
import os
import json
import re
from collections import Counter
import xlsxwriter
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

# Stopwords bahasa Indonesia dan Arab
stopwords_indonesia = set(stopwords.words('indonesian'))
custom_stopwords_input = set(['dan', 'atau', 'namun', 'ke', 'dari', 'dengan', 'karena'])  # Stopwords kustom
stopwords_arabic = set(['و', 'في', 'من', 'على', 'إلى', 'عن', 'ما', 'لم', 'لن', 'مع', 'كل', 'إن', 'أن', 'هذا', 'هذه', 'ذلك', 'الذي', 'التي', 'كان', 'قد', 'هو', 'هي', 'هم', 'هن'])

folder_path = 'dataset/quran_json_init/quran-json-master/surah'
output_folder = 'dataset/quran_json_ekstrak/'

def ensure_output_folder_exists(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def remove_stopwords(words, stopword_list):
    return [word for word in words if word not in stopword_list]

def process_surah_file(file_path, top_k_values):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        surah_number = list(data.keys())[0]
        texts = {'text': '', 'translations': '', 'tafsir': ''}

        if "text" in data[surah_number]:
            for ayah_text in data[surah_number]["text"].values():
                texts['text'] += ' ' + ayah_text
        if "translations" in data[surah_number] and "id" in data[surah_number]["translations"]:
            for ayah_text in data[surah_number]["translations"]["id"]["text"].values():
                texts['translations'] += ' ' + ayah_text
        if "tafsir" in data[surah_number] and "id" in data[surah_number]["tafsir"] and "kemenag" in data[surah_number]["tafsir"]["id"]:
            for ayah_text in data[surah_number]["tafsir"]["id"]["kemenag"]["text"].values():
                texts['tafsir'] += ' ' + ayah_text

    term_frequencies = {}
    for category, text in texts.items():
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        words = clean_text.split()
        if category == 'text':
            words = remove_stopwords(words, stopwords_arabic)
        else:
            full_stopwords_indonesia = stopwords_indonesia.union(custom_stopwords_input)
            words = remove_stopwords(words, full_stopwords_indonesia)

        word_frequencies = Counter(words)
        term_frequencies[category] = {
            'merger': ' '.join(words).strip(),
            'top_frequencies': {f'top_{k}': word_frequencies.most_common(k) for k in top_k_values}
        }
    return term_frequencies

def process_all_files(folder_path, output_folder, top_k_values):
    ensure_output_folder_exists(output_folder)
    combined_frequencies = { 'text': {k: [] for k in top_k_values}, 'translations': {k: [] for k in top_k_values}, 'tafsir': {k: [] for k in top_k_values} }

    for filename in sorted(os.listdir(folder_path), key=lambda x: int(x.split('.')[0])):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            surah_number = filename.split('.')[0]
            term_frequencies = process_surah_file(file_path, top_k_values)

            output_file_path = os.path.join(output_folder, f'output_{surah_number}.json')
            with open(output_file_path, 'w', encoding='utf-8') as out_file:
                json.dump(term_frequencies, out_file, ensure_ascii=False, indent=4)

            for category in combined_frequencies.keys():
                for k in top_k_values:
                    combined_frequencies[category][k].extend(term_frequencies[category]['top_frequencies'][f'top_{k}'])
    return combined_frequencies

def get_unique_terms(combined_frequencies):
    unique_terms_data = {}
    for category, top_k_dict in combined_frequencies.items():
        unique_terms_data[category] = {}
        for k, terms in top_k_dict.items():
            words = [term[0].lower() for term in terms]
            unique_terms = set(words)
            unique_terms_data[category][f'top_{k}'] = {
                'unique_terms_count': len(unique_terms),
                'unique_terms': list(unique_terms)
            }
    return unique_terms_data

# def save_unique_terms_to_file(unique_terms_data, output_folder):
#     output_file_path = os.path.join(output_folder, 'feature_extraction.json')
#     with open(output_file_path, 'w', encoding='utf-8') as out_file:
#         json.dump(unique_terms_data, out_file, ensure_ascii=False, indent=4)
#     print(f'Hasil term unik disimpan di: {output_file_path}')

# def save_xlsx_and_convert_to_json(unique_terms_data, output_folder):
#     """Menyimpan data term unik ke dalam file Excel dan mengonversinya ke file JSON."""
#     # Menyimpan data ke dalam file Excel
#     output_xlsx_path = os.path.join(output_folder, 'feature_extraction.xlsx')
#     workbook = xlsxwriter.Workbook(output_xlsx_path)
    
#     for category in unique_terms_data:
#         for k in [5, 10, 15]:
#             sheet_name = f'{category}-top_{k}'
#             worksheet = workbook.add_worksheet(sheet_name)

#             unique_terms = unique_terms_data[category][f'top_{k}']['unique_terms']

#             # Menuliskan terms unik di baris pertama mulai dari kolom kedua
#             for col_num, term in enumerate(unique_terms, start=1):
#                 worksheet.write(0, col_num, term)

#             # Menuliskan nomor surah di kolom pertama tiap baris (1 hingga 114)
#             for surah_num in range(1, 115):
#                 worksheet.write(surah_num, 0, str(surah_num))

#             # Menuliskan kolom tambahan dengan nama 1 hingga 114 di baris pertama setelah terms unik
#             for i in range(1, 115):
#                 worksheet.write(0, len(unique_terms) + i, str(i))

#             # Mengecek kehadiran term unik di setiap surah dan menuliskan 1 atau 0
#             for surah_num in range(1, 115):
#                 file_path = os.path.join(output_folder, f'output_{surah_num}.json')
#                 if not os.path.exists(file_path):
#                     continue

#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     surah_data = json.load(f)
#                     terms_in_surah = [term[0] for term in surah_data[category]['top_frequencies'][f'top_{k}']]

#                     # Menuliskan 1 jika term ditemukan, 0 jika tidak ditemukan
#                     for col_num, term in enumerate(unique_terms, start=1):
#                         worksheet.write(surah_num, col_num, 1 if term in terms_in_surah else 0)

#                 # Menuliskan nilai 1 atau 0 pada kolom tambahan (1 hingga 114) sesuai syarat
#                 for col_index, col_value in enumerate(range(1, 115), start=len(unique_terms) + 1):
#                     worksheet.write(surah_num, col_index, 1 if surah_num == col_value else 0)
    
#     workbook.close()
#     print(f'Hasil disimpan dalam file Excel di: {output_xlsx_path}')

#     # Mengonversi data ke format JSON
#     json_output_path = os.path.join(output_folder, 'feature_extraction.json')
#     with open(json_output_path, 'w', encoding='utf-8') as json_file:
#         json.dump(unique_terms_data, json_file, ensure_ascii=False, indent=4)
#     print(f'Hasil term unik disimpan di: {json_output_path}')

# def save_xlsx_and_convert_to_json(unique_terms_data, output_folder):
#     """Menyimpan data term unik ke dalam file Excel dan mengonversinya ke file JSON."""
#     # Menyimpan data ke dalam file Excel
#     output_xlsx_path = os.path.join(output_folder, 'feature_extraction.xlsx')
#     workbook = xlsxwriter.Workbook(output_xlsx_path)
    
#     all_data = {}  # Menyimpan semua data untuk JSON

#     for category in unique_terms_data:
#         all_data[category] = {}  # Inisialisasi untuk setiap kategori
#         for k in [5, 10, 15]:
#             sheet_name = f'{category}-top_{k}'
#             worksheet = workbook.add_worksheet(sheet_name)

#             unique_terms = unique_terms_data[category][f'top_{k}']['unique_terms']

#             # Menuliskan terms unik di baris pertama mulai dari kolom kedua
#             for col_num, term in enumerate(unique_terms, start=1):
#                 worksheet.write(0, col_num, term)

#             # Menuliskan nomor surah di kolom pertama tiap baris (1 hingga 114)
#             for surah_num in range(1, 115):
#                 worksheet.write(surah_num, 0, str(surah_num))

            # # Menuliskan kolom tambahan dengan nama 1 hingga 114 di baris pertama setelah terms unik
            # for i in range(1, 115):
            #     worksheet.write(0, len(unique_terms) + i, str(i))

#             # Mengecek kehadiran term unik di setiap surah dan menuliskan 1 atau 0
#             for surah_num in range(1, 115):
#                 file_path = os.path.join(output_folder, f'output_{surah_num}.json')
#                 if not os.path.exists(file_path):
#                     continue

#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     surah_data = json.load(f)
#                     terms_in_surah = [term[0] for term in surah_data[category]['top_frequencies'][f'top_{k}']]

#                     # Menuliskan 1 jika term ditemukan, 0 jika tidak ditemukan
#                     for col_num, term in enumerate(unique_terms, start=1):
#                         if term in terms_in_surah:
#                             worksheet.write(surah_num, col_num, 1)
#                             all_data[category].setdefault(f'top_{k}', {}).setdefault(surah_num, {}).setdefault(term, 1)
#                         else:
#                             worksheet.write(surah_num, col_num, 0)
#                             all_data[category].setdefault(f'top_{k}', {}).setdefault(surah_num, {}).setdefault(term, 0)

#                 # Menuliskan nilai 1 atau 0 pada kolom tambahan (1 hingga 114) sesuai syarat
#                 for col_index, col_value in enumerate(range(1, 115), start=len(unique_terms) + 1):
#                     value = 1 if surah_num == col_value else 0
#                     worksheet.write(surah_num, col_index, value)
#                     all_data[category].setdefault(f'top_{k}', {}).setdefault(surah_num, {}).setdefault(str(col_value), value)

#     workbook.close()
#     print(f'Hasil disimpan dalam file Excel di: {output_xlsx_path}')

#     # Mengonversi data ke format JSON
#     json_output_path = os.path.join(output_folder, 'feature_extraction.json')
#     with open(json_output_path, 'w', encoding='utf-8') as json_file:
#         json.dump(all_data, json_file, ensure_ascii=False, indent=4)
#     print(f'Hasil term unik disimpan di: {json_output_path}')

def save_xlsx_and_convert_to_json(unique_terms_data, output_folder):
    """Menyimpan data term unik ke dalam file Excel dan mengonversinya ke file JSON."""
    # Menyimpan data ke dalam file Excel
    output_xlsx_path = os.path.join(output_folder, 'feature_extraction.xlsx')
    workbook = xlsxwriter.Workbook(output_xlsx_path)

    all_data = {}  # Menyimpan semua data untuk JSON

    for category in unique_terms_data:
        all_data[category] = {}  # Inisialisasi untuk setiap kategori
        for k in [5, 10, 15]:
            sheet_name = f'{category}-top_{k}'
            worksheet = workbook.add_worksheet(sheet_name)

            unique_terms = unique_terms_data[category][f'top_{k}']['unique_terms']

            # Menuliskan terms unik di baris pertama mulai dari kolom kedua
            for col_num, term in enumerate(unique_terms, start=1):
                worksheet.write(0, col_num, term)
                all_data[category].setdefault(f'top_{k}', {}).setdefault('unique_terms', []).append(term)

            # Menuliskan nomor surah di kolom pertama tiap baris (1 hingga 114)
            all_data[category].setdefault(f'top_{k}', {}).setdefault('surahs', [])
            for surah_num in range(1, 115):
                worksheet.write(surah_num, 0, str(surah_num))
                all_data[category][f'top_{k}']['surahs'].append(str(surah_num))

            # Menuliskan kolom tambahan dengan nama 1 hingga 114 di baris pertama setelah terms unik
            all_data[category].setdefault(f'top_{k}', {}).setdefault('additional_columns', [])
            for i in range(1, 115):
                worksheet.write(0, len(unique_terms) + i, str(i))
                all_data[category][f'top_{k}']['additional_columns'].append(str(i))

            # Mengecek kehadiran term unik di setiap surah dan menuliskan 1 atau 0
            for surah_num in range(1, 115):
                file_path = os.path.join(output_folder, f'output_{surah_num}.json')
                if not os.path.exists(file_path):
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    surah_data = json.load(f)
                    terms_in_surah = [term[0] for term in surah_data[category]['top_frequencies'][f'top_{k}']]

                    # Menuliskan 1 jika term ditemukan, 0 jika tidak ditemukan
                    for col_num, term in enumerate(unique_terms, start=1):
                        if term in terms_in_surah:
                            worksheet.write(surah_num, col_num, 1)
                            all_data[category].setdefault(f'top_{k}', {}).setdefault('data', {}).setdefault(surah_num, {}).setdefault(term, 1)
                        else:
                            worksheet.write(surah_num, col_num, 0)
                            all_data[category].setdefault(f'top_{k}', {}).setdefault('data', {}).setdefault(surah_num, {}).setdefault(term, 0)

                # Menuliskan nilai 1 atau 0 pada kolom tambahan (1 hingga 114) sesuai syarat
                for col_index, col_value in enumerate(range(1, 115), start=len(unique_terms) + 1):
                    value = 1 if surah_num == col_value else 0
                    worksheet.write(surah_num, col_index, value)
                    all_data[category].setdefault(f'top_{k}', {}).setdefault('data', {}).setdefault(surah_num, {}).setdefault(str(col_value), value)

    workbook.close()
    print(f'Hasil disimpan dalam file Excel di: {output_xlsx_path}')

    # Mengonversi data ke format JSON
    json_output_path = os.path.join(output_folder, 'feature_extraction.json')
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)
    print(f'Hasil term unik disimpan di: {json_output_path}')

def save_unique_terms_to_xlsx(unique_terms_data, output_folder):
    output_xlsx_path = os.path.join(output_folder, 'feature_extraction.xlsx')
    workbook = xlsxwriter.Workbook(output_xlsx_path)
    
    for category in unique_terms_data:
        for k in [5, 10, 15]:
            sheet_name = f'{category}-top_{k}'
            worksheet = workbook.add_worksheet(sheet_name)

            unique_terms = unique_terms_data[category][f'top_{k}']['unique_terms']

            # Menuliskan terms unik di baris pertama mulai dari kolom kedua
            for col_num, term in enumerate(unique_terms, start=1):
                worksheet.write(0, col_num, term)

            # Menuliskan nomor surah di kolom pertama tiap baris (1 hingga 114)
            for surah_num in range(1, 115):
                worksheet.write(surah_num, 0, str(surah_num))

            # Menuliskan kolom tambahan dengan nama 1 hingga 114 di baris pertama setelah terms unik
            for i in range(1, 115):
                worksheet.write(0, len(unique_terms) + i, str(i))

            # Mengecek kehadiran term unik di setiap surah dan menuliskan 1 atau 0
            for surah_num in range(1, 115):
                file_path = os.path.join(output_folder, f'output_{surah_num}.json')
                if not os.path.exists(file_path):
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    surah_data = json.load(f)
                    terms_in_surah = [term[0] for term in surah_data[category]['top_frequencies'][f'top_{k}']]

                    # Menuliskan 1 jika term ditemukan, 0 jika tidak ditemukan
                    for col_num, term in enumerate(unique_terms, start=1):
                        if term in terms_in_surah:
                            worksheet.write(surah_num, col_num, 1)
                        else:
                            worksheet.write(surah_num, col_num, 0)

                # Menuliskan nilai 1 atau 0 pada kolom tambahan (1 hingga 114) sesuai syarat
                for col_index, col_value in enumerate(range(1, 115), start=len(unique_terms) + 1):
                    worksheet.write(surah_num, col_index, 1 if surah_num == col_value else 0)
    
    workbook.close()
    print(f'Hasil disimpan dalam file Excel di: {output_xlsx_path}')

top_k_values = [5, 10, 15]
combined_frequencies = process_all_files(folder_path, output_folder, top_k_values)
unique_terms_data = get_unique_terms(combined_frequencies)
save_unique_terms_to_xlsx(unique_terms_data, output_folder)
save_xlsx_and_convert_to_json(unique_terms_data, output_folder)

## Extract Data from Feature Extraction to Modeling
import pandas as pd

# Load data dari file feature_extraction.xlsx
input_file_path = 'dataset/quran_json_ekstrak/feature_extraction.xlsx'
data = pd.read_excel(input_file_path, sheet_name='translations-top_15')

# Definisikan daftar baris untuk setiap model
list_model_sheet1 = [6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 50, 51, 52, 53, 54, 55, 56, 61, 64, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111]
list_model_sheet2 = [1, 2, 3, 4, 5, 6, 22, 8, 9, 24, 26, 32, 39, 33, 47, 48, 49, 57, 58, 59, 60, 61, 62, 63, 64, 73, 65, 66, 31, 99, 110, 112, 113, 114]
list_model_sheet3 = [6, 22, 26, 32, 39, 31, 73, 64, 16]
list_model_comb_all_unique = list(range(1, 115))  # Menyertakan semua baris dari 1 hingga 114

# Fungsi untuk mengambil data berdasarkan baris yang diberikan
def extract_rows(data, row_indices):
    # Mengurangi 1 dari baris karena pandas menggunakan indeks mulai dari 0
    return data.iloc[[index - 1 for index in row_indices]]

# Membuat file Excel baru dan menyimpan data ke sheet sesuai dengan daftar
output_file_path = 'dataset/quran_json_ekstrak/dataset_model_v1.xlsx'
with pd.ExcelWriter(output_file_path) as writer:
    extract_rows(data, list_model_sheet1).to_excel(writer, sheet_name='list_model_sheet1', index=False)
    extract_rows(data, list_model_sheet2).to_excel(writer, sheet_name='list_model_sheet2', index=False)
    extract_rows(data, list_model_sheet3).to_excel(writer, sheet_name='list_model_sheet3', index=False)
    extract_rows(data, list_model_comb_all_unique).to_excel(writer, sheet_name='list_model_comb_all_unique', index=False)

print(f'Data telah disimpan ke dalam {output_file_path}')
