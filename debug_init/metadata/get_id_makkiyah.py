from difflib import SequenceMatcher

# Data as provided
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

# Similarity threshold
similarity_threshold = 0.8

# Check similarity and get indices
id_makkiyah = []
for term in makkiyah:
    best_similarity = 0
    best_index = -1

    # Compare with surah_name_latin
    for i, surah in enumerate(surah_name_latin):
        similarity = SequenceMatcher(None, term, surah).ratio()
        if similarity > best_similarity and similarity >= similarity_threshold:
            best_similarity = similarity
            best_index = i + 1  # 1-based index

    # Compare with surah_name_latin_alias
    for i, alias in enumerate(surah_name_latin_alias):
        similarity = SequenceMatcher(None, term, alias).ratio()
        if similarity > best_similarity and similarity >= similarity_threshold:
            best_similarity = similarity
            best_index = i + 1  # 1-based index

    # Add matched index
    if best_index != -1:
        id_makkiyah.append(best_index)

print(id_makkiyah)
print(len(id_makkiyah))
print(len(makkiyah))
