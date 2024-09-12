import pandas as pd
import os
from cleaningData import *


df = pd.read_csv("data/train.csv",low_memory=False)

deleteColumns = [
                "Burs Aldigi Baska Kurum",
                "Baska Kurumdan Aldigi Burs Miktari",
                "Uye Oldugunuz Kulubun Ismi",
                "Hangi STK'nin Uyesisiniz?",
                "Girisimcilikle Ilgili Deneyiminizi Aciklayabilir misiniz?",
                "Universite Adi",
                "Bölüm",
                "Lise Adi",
                "Lise Adi Diger",
                "Lise Bolum Diger",
                "Lise Sehir",
                "Lise Bolumu",
                "Daha Önceden Mezun Olunduysa, Mezun Olunan Üniversite"]

df = df.drop(columns=deleteColumns)

string_columns = df.select_dtypes(include='object').columns
df[string_columns] = df[string_columns].apply(lambda col: col.str.lower())

df.loc[(df['Universite Turu'] == 'devlet') & (df['Burs Aliyor mu?'] == 'hayır'), 'Burslu ise Burs Yuzdesi'] = -1
df['Daha Once Baska Bir Universiteden Mezun Olmus'] = df['Daha Once Baska Bir Universiteden Mezun Olmus'].fillna('hayır')

df = cleanEducation(df)
df = cleanFatherEducation(df)
df = cleanLise(df)
df = cleanAnneWork(df)
df = cleanBabaWork(df)

df['Lise Mezuniyet Notu'] = df['Lise Mezuniyet Notu'].apply(convert_to_standard_scale)
df['Lise Mezuniyet Notu'] = df['Lise Mezuniyet Notu'].apply(categorize_grade)
df['Lise Mezuniyet Notu'].value_counts()

df['Universite Not Ortalamasi'] = df['Universite Not Ortalamasi'].apply(normalize_grade_range)

df['Universite Kacinci Sinif'] = df['Universite Kacinci Sinif'].replace({
    '0': '1',         # 0 olanları 1 yap
    'hazırlık': '1',  # hazırlık olanları 1 yap
    'tez': 'yüksek lisans'  # tez olanları yüksek lisans yap
})

df['Spor Dalindaki Rolunuz Nedir?'] = df['Spor Dalindaki Rolunuz Nedir?'].replace({
    '0': 'yok',
    '-': 'yok',
    "Lider/Kaptan":"kaptan",
    "Kaptan":"kaptan",
    "KAPTAN / LİDER":"kaptan"
})

df['Kardes Sayisi'] = df['Kardes Sayisi'].replace(r'\.0$', '', regex=True)
df['Kardes Sayisi'] = pd.to_numeric(df['Kardes Sayisi'], errors='coerce')

df['Dogum Tarihi'] = df['Dogum Tarihi'].apply(combined_normalization)
df['Dogum Yeri'] = df['Dogum Yeri'].apply(process_dogum_yeri)

# df['Kardes Sayisi'] = df['Kardes Sayisi'].astype(object)
# df['Kardes Sayisi'] = df['Kardes Sayisi'].fillna('Bilinmiyor')
# df.fillna("Bilinmiyor", inplace=True)

excluded_columns = ['Dogum Tarihi']
string_columns = df.select_dtypes(include=['object']).columns
columns_to_fill = [col for col in string_columns if col not in excluded_columns]
df[columns_to_fill] = df[columns_to_fill].fillna("Bilinmiyor", inplace=False)

df = df.reset_index(drop=True)
df.to_csv("cleanedData.csv",index=False)