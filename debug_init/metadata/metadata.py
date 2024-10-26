# List jumlah ayat dalam setiap surah
total_ayah = [
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52,
    99, 128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60,
    34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29,
    18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12, 12,
    30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19, 36, 25,
    22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8, 3, 9,
    5, 4, 7, 3, 6, 3, 5, 4, 5, 6
]

# List nama surah dalam tulisan Latin
surah_name_latin = [
    "Al-Fatihah", "Al-Baqarah", "Ali 'Imran", "An-Nisa'", "Al-Ma'idah",
    "Al-An'am", "Al-A'raf", "Al-Anfal", "At-Taubah", "Yunus", "Hud", "Yusuf",
    "Ar-Ra'd", "Ibrahim", "Al-Hijr", "An-Nahl", "Al-Isra'", "Al-Kahf", "Maryam",
    "Taha", "Al-Anbiya'", "Al-Hajj", "Al-Mu'minun", "An-Nur", "Al-Furqan",
    "Asy-Syu'ara'", "An-Naml", "Al-Qasas", "Al-'Ankabut", "Ar-Rum", "Luqman",
    "As-Sajdah", "Al-Ahzab", "Saba'", "Fatir", "Yasin", "As-Saffat", "Sad",
    "Az-Zumar", "Gafir", "Fussilat", "Asy-Syura", "Az-Zukhruf", "Ad-Dukhan",
    "Al-Jasiyah", "Al-Ahqaf", "Muhammad", "Al-Fath", "Al-Hujurat", "Qaf",
    "Az-Zariyat", "At-Tur", "An-Najm", "Al-Qamar", "Ar-Rahman", "Al-Waqi'ah",
    "Al-Hadid", "Al-Mujadalah", "Al-Hasyr", "Al-Mumtahanah", "As-Saff",
    "Al-Jumu'ah", "Al-Munafiqun", "At-Tagabun", "At-Talaq", "At-Tahrim",
    "Al-Mulk", "Al-Qalam", "Al-Haqqah", "Al-Ma'arij", "Nuh", "Al-Jinn",
    "Al-Muzzammil", "Al-Muddassir", "Al-Qiyamah", "Al-Insan", "Al-Mursalat",
    "An-Naba'", "An-Nazi'at", "'Abasa", "At-Takwir", "Al-Infitar",
    "Al-Mutaffifin", "Al-Insyiqaq", "Al-Buruj", "At-Tariq", "Al-A'la",
    "Al-Gasyiyah", "Al-Fajr", "Al-Balad", "Asy-Syams", "Al-Lail", "Ad-Duha",
    "Asy-Syarh", "At-Tin", "Al-'Alaq", "Al-Qadr", "Al-Bayyinah", "Az-Zalzalah",
    "Al-'Adiyat", "Al-Qari'ah", "At-Takasur", "Al-'Asr", "Al-Humazah",
    "Al-Fil", "Quraisy", "Al-Ma'un", "Al-Kausar", "Al-Kafirun", "An-Nasr",
    "Al-Lahab", "Al-Ikhlas", "Al-Falaq", "An-Nas"
]

surah_name_latin_alias = [
    "Al-Fatihah", "Al-Baqarah", "Ali 'Imran", "An-Nisa'", "Al-Ma'idah",
    "Al-An’am", "Al-A’raf", "Al-Anfal", "At-Taubah", "Yunus", "Hud", "Yusuf",
    "Ar-Ra’du", "Ibrahim", "Al-Hijr", "An-Nahl", "Bani Israil", "Al-Kahfi", "Maryam",
    "Thaha", "Al-Anbiya", "Al-Hajj", "Al-Mu’min", "An-Nur", "Al-Furqon",
    "As-Syuraa", "An-Naml", "Al-Qashash", "Al-Ankabut", "Ar-Ruum", "Luqman",
    "As-Sajadah", "Al-Ahzab", "Saba", "Fathir", "Yaasiin", "As-Shaffaat", "Shaad",
    "Az-Zumar", "Ghaafir", "Fusshilat", "Asy-Syura", "Az-Zukhruf", "Ad-Dukhan",
    "Al-Jaathiyah", "Al-Ahqaf", "Muhammad", "Al-Fath", "Al-Hujurat", "Qaaf",
    "Ad-Dzaariyaat", "At-Thuur", "An-Najm", "Al-Qamar", "Ar-Rahman", "Al-Waqi’ah",
    "Al-Hadid", "Al-Mujadalah", "Al-Hasyr", "Al-Mumtahanah", "Shaaf",
    "Al-Jumu'ah", "Al-Munafiqun", "At-Taghabun", "At-Talaq", "At-Tahrim",
    "Al-Mulk", "Al-Qalam", "Al-Haaqqah", "Al-Ma’aarij", "Nuh", "Jin",
    "Al-Muzammil", "Al-Mudatsir", "Al-Qiyaamah", "Al-Insan", "Al-Mursalat",
    "An-Naba", "An-Naazi’aat", "‘Abasa", "At-Takwir", "Al-Infithar",
    "Al-Muthaffifin", "Al-Insyiqaq", "Al-Buruj", "At-Thariq", "Al-A’la",
    "Al-Ghatsiyah", "Al-Fajr", "Al-Balad", "As-Syams", "Al-Lail", "Ad-Dhuha",
    "Alam Nasyrah", "At-Tin", "Al-‘Alaq", "Al-Qadr", "Al-Bayyinah", "Az-Zalzalah",
    "Al-‘Aadiyaat", "Al-Qaari’ah", "At-Takatsur", "Al-‘Ashr", "Al-Humazah",
    "Al-Fiil", "Al-Quraisy", "Al-Maa’uun", "Al-Kautsar", "Al-Kaafiruun", "An-Nasr",
    "Al-Lahab", "Al-Ikhlas", "Al-Falaq", "An-Nas"
]

# List nama surah dalam tulisan Arab
surah_name_arab = [
    "الفاتحة", "البقرة", "اٰل عمران", "النساۤء", "الماۤئدة", "الانعام", "الاعراف",
    "الانفال", "التوبة", "يونس", "هود", "يوسف", "الرّعد", "ابرٰهيم", "الحجر", "النحل",
    "الاسراۤء", "الكهف", "مريم", "طٰهٰ", "الانبياۤء", "الحج", "المؤمنون", "النّور",
    "الفرقان", "الشعراۤء", "النمل", "القصص", "العنكبوت", "الرّوم", "لقمٰن", "السّجدة",
    "الاحزاب", "سبأ", "فاطر", "يٰسۤ", "الصّٰۤفّٰت", "ص", "الزمر", "غافر", "فصّلت",
    "الشورى", "الزخرف", "الدخان", "الجاثية", "الاحقاف", "محمّد", "الفتح", "الحجرٰت",
    "ق", "الذّٰريٰت", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة",
    "الحشر", "الممتحنة", "الصّفّ", "الجمعة", "المنٰفقون", "التغابن", "الطلاق", "التحريم",
    "الملك", "القلم", "الحاۤقّة", "المعارج", "نوح", "الجن", "المزّمّل", "المدّثّر",
    "القيٰمة", "الانسان", "المرسلٰت", "النبأ", "النّٰزعٰت", "عبس", "التكوير", "الانفطار",
    "المطفّفين", "الانشقاق", "البروج", "الطارق", "الاعلى", "الغاشية", "الفجر", "البلد",
    "الشمس", "الّيل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البيّنة", "الزلزلة",
    "العٰديٰت", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون",
    "الكوثر", "الكٰفرون", "النصر", "اللهب", "الاخلاص", "الفلق", "الناس"
]

# List nama surah dalam bahasa Indonesia
surah_name_trans_id = [
    "Pembukaan", "Sapi", "Keluarga Imran", "Wanita", "Hidangan", "Binatang Ternak",
    "Tempat Tertinggi", "Rampasan Perang", "Pengampunan", "Yunus", "Hud", "Yusuf",
    "Guruh", "Ibrahim", "Hijr", "Lebah", "Memperjalankan Malam Hari", "Goa", "Maryam",
    "Taha", "Para Nabi", "Haji", "Orang-Orang Mukmin", "Cahaya", "Pembeda", "Para Penyair",
    "Semut-semut", "Kisah-Kisah", "Laba-Laba", "Romawi", "Luqman", "Sajdah", "Golongan Yang Bersekutu",
    "Saba'", "Maha Pencipta", "Yasin", "Barisan-Barisan", "Sad", "Rombongan", "Maha Pengampun",
    "Yang Dijelaskan", "Musyawarah", "Perhiasan", "Kabut", "Berlutut", "Bukit Pasir", "Muhammad",
    "Kemenangan", "Kamar-Kamar", "Qaf", "Angin yang Menerbangkan", "Bukit Tursina", "Bintang",
    "Bulan", "Maha Pengasih", "Hari Kiamat", "Besi", "Gugatan", "Pengusiran", "Wanita Yang Diuji",
    "Barisan", "Jumat", "Orang-Orang Munafik", "Pengungkapan Kesalahan", "Talak", "Pengharaman",
    "Kerajaan", "Pena", "Hari Kiamat", "Tempat Naik", "Nuh", "Jin", "Orang Yang Berselimut",
    "Orang Yang Berkemul", "Hari Kiamat", "Manusia", "Malaikat Yang Diutus", "Berita Besar",
    "Malaikat Yang Mencabut", "Bermuka Masam", "Penggulungan", "Terbelah", "Orang-Orang Curang",
    "Terbelah", "Gugusan Bintang", "Yang Datang Di Malam Hari", "Maha Tinggi", "Hari Kiamat",
    "Fajar", "Negeri", "Matahari", "Malam", "Duha", "Lapang", "Buah Tin", "Segumpal Darah",
    "Kemuliaan", "Bukti Nyata", "Guncangan", "Kuda Yang Berlari Kencang", "Hari Kiamat",
    "Bermegah-Megahan", "Asar", "Pengumpat", "Gajah", "Quraisy", "Barang Yang Berguna",
    "Pemberian Yang Banyak", "Orang-Orang kafir", "Pertolongan", "Api Yang Bergejolak",
    "Ikhlas", "Subuh", "Manusia"
]

# https://islam.nu.or.id/ilmu-al-quran/daftar-lengkap-surat-makkiyah-dan-madaniyah-riwayat-ibnu-abbas-7T9mT
# id Surah-surah yang turun di Madinah

id_makkiyah = [6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31,
               32, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 50, 51, 52, 53, 54, 55, 56, 61, 64, 67,
               68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
               91, 92, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111]

id_madaniyah =[1, 2, 3, 4, 5, 6, 22, 8, 9, 24, 26, 32, 39, 33, 47, 48, 49, 57, 58, 59, 60, 61, 62, 63, 64,
     73, 65, 66, 31, 99, 110, 112, 113, 114]

id_makkiyah_dan_madaniyah = [6, 22, 26, 32, 39, 31, 73, 64]

id_turun_diantara_makiyah_dan_madaniyah = [16]

# Surah-surah yang turun di Makkah
makkiyah = [
    "Al-An’am", "Al-A’raf", "Yunus", "Hud", "Yusuf", "Ar-Ra’du", "Ibrahim", "Al-Hijr", "An-Nahl",
    "Bani Israil", "Al-Kahfi", "Maryam", "Thaha", "Al-Anbiya", "Al-Hajj", "Al-Mu’min", "Al-Furqon",
    "Asy-Syu'ara'", "An-Naml", "Al-Qashash", "Al-Ankabut", "Ar-Ruum", "Luqman", "As-Sajadah",
    "Saba", "Fathir", "Yaasiin", "As-Shaffaat", "Shaad", "Az-Zumar", "Ghaafir", "Fusshilat",
    "Az-Zukhruf", "Ad-Dukhan", "Al-Jaathiyah", "Al-Ahqaf", "Qaaf", "Ad-Dzaariyaat",
    "At-Thuur", "An-Najm", "Al-Qamar", "Ar-Rahman", "Al-Waqi’ah", "Shaaf", "At-Taghabun",
    "Al-Mulk", "Al-Qalam", "Al-Haaqqah", "Al-Ma’aarij", "Nuh", "Jin", "Al-Muzammil", "Al-Mudatsir",
    "Al-Qiyaamah", "Al-Insan", "Al-Mursalat", "An-Naba", "An-Naazi’aat", "‘Abasa", "At-Takwir",
    "Al-Infithar", "Al-Muthaffifin", "Al-Insyiqaq", "Al-Buruj", "At-Thariq", "Al-A’la",
    "Al-Ghatsiyah", "Al-Fajr", "Al-Balad", "As-Syams", "Al-Lail", "Ad-Dhuha", "Alam Nasyrah",
    "At-Tin", "Al-‘Alaq", "Al-Qadr", "Al-Bayyinah", "Al-‘Aadiyaat", "Al-Qaari’ah", "At-Takatsur",
    "Al-‘Ashr", "Al-Humazah", "Al-Fiil", "Al-Quraisy", "Al-Maa’uun", "Al-Kautsar", "Al-Kaafiruun",
    "Al-Lahab"
]

# Surah-surah yang turun di Madinah
madaniyah = [
    "Al-Fatihah", "Al-Baqarah", "Ali Imran", "An-Nisa", "Al-Maa’idah", "Al-An’am", "Al-Hajj",
    "Al-Anfal", "At-Taubah", "An-Nur", "Asy-Syu'ara'", "As-Sajadah", "Az-Zumar", "Al-Ahzab",
    "Muhammad", "Al-Fath", "Al-Hujuraat", "Al-Hadiid", "Al-Mujadalah", "Al-Hasyr", "Al-Mumtahanah",
    "As-Shaff", "Al-Jumu’ah", "Al-Munafiqun", "At-Taghabun", "Al-Muzammil", "At-Thalaq",
    "At-Tahrim", "Luqman", "Al-Zalzalah", "An-Nashr", "Al-Ikhlash", "Al-Falaq", "An-Naas"
]

# Surah-surah yang termasuk dalam kedua kategori (makkiyah dan madaniyah)

makkiyah_dan_madaniyah = [
    "Al-An’am", "Al-Hajj", "Asy-Syu'ara'", "As-Sajadah", "Az-Zumar", "Luqman", "Al-Muzammil",
    "At-Taghabun"
]


# Surah yang turun di antara Makkah dan Madinah
turun_diantara_makiyah_dan_madaniyah = ["An-Nahl"]

# Verifikasi jumlah keseluruhan
total_surah = len(set(makkiyah + madaniyah + makkiyah_dan_madaniyah + turun_diantara_makiyah_dan_madaniyah))
print(f"Total surah count: {total_surah}")  # Seharusnya mencetak 114
print("Makkiyah:", len(makkiyah))
print("Madaniyah:", len(madaniyah))
print("Makkiyah dan Madaniyah:", len(makkiyah_dan_madaniyah))
print("Turun di antara Makkah dan Madinah:", len(turun_diantara_makiyah_dan_madaniyah))
