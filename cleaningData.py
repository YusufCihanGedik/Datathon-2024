import pandas as pd
import re
from dateutil import parser


with open('data/sehir_ilce_listesi.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

sehir_ilce_dict = {}
ilce_sehir_dict = {} 
for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 3:
        sehir = parts[1].lower()
        ilce = parts[2].lower()
        if sehir not in sehir_ilce_dict:
            sehir_ilce_dict[sehir] = []
        sehir_ilce_dict[sehir].append(ilce)
        ilce_sehir_dict[ilce] = sehir 

def process_dogum_yeri(value):
    if pd.isnull(value) or value.strip() == "":
        return "" 
    value = value.lower()
    value = value.replace(',', ' ').replace('/', ' ').replace('\\', ' ').replace('-', ' ')
    parts = value.split()

    if len(parts) == 0:
        return "" 

    for part in parts:
        if part in sehir_ilce_dict:
            return part
        elif part in ilce_sehir_dict:
            return ilce_sehir_dict[part]
    
    return value

month_dict = {
    'ocak': '01', 'şubat': '02', 'subat': '02', 'mart': '03', 'nisan': '04', 
    'mayıs': '05', 'mayis': '05', 'haziran': '06', 'hazıran': '06', 'temmuz': '07', 
    'ağustos': '08', 'agustos': '08', 'eylül': '09', 'eylul': '09', 'ekim': '10', 
    'ekım': '10', 'kasım': '11', 'kasim': '11', 'aralık': '12', 'aralik': '12'
}

# Türkçe ayları tespit edip sayısal karşılıklarıyla değiştiren fonksiyon
def convert_turkish_date(date_str):
    if isinstance(date_str, str):  # Sadece string verilerde işlem yap
        # Veriyi split ile ayırıyoruz
        date_parts = date_str.split()
        
        if len(date_parts) == 3:  # Eğer 3 parça varsa, yani Türkçe bir tarihse
            day = date_parts[0]
            month = date_parts[1].lower()  # Ayı küçük harfe çeviriyoruz
            year = date_parts[2]
            
            # Türkçe ay ismini sayısal karşılığıyla değiştiriyoruz
            if month in month_dict:
                numeric_month = month_dict[month]
                # Gün/ay/yıl formatında döndürme
                return f"{day.zfill(2)}/{numeric_month}/{year}"
    return None

# Genel tarihleri normalize eden fonksiyon
def normalize_date(date_str):
    try:
        # dateutil.parser parse işini yapacak
        parsed_date = parser.parse(date_str, dayfirst=False)
        return parsed_date.strftime('%d/%m/%Y')  # Gün/ay/yıl formatı
    except Exception as e:
        return None  # Hatalı veriler için None döndür

def combined_normalization(date_str):
    if pd.isnull(date_str):
        return None
    turkish_date = convert_turkish_date(date_str)
    if turkish_date:
        return turkish_date
    else:
        return normalize_date(date_str)

def cleanBabaWork(df):
    replace_map = {
        "0":"calismiyor",
        "özel sektör":"özel",
        "diğer":"diger",
        "di̇ğer":"diger",
        "-":"calismiyor"
    }
    df['Baba Sektor'] = df['Baba Sektor'].replace(replace_map)
    return df

def cleanAnneWork(df):
    replace_map = {
        "0":"calismiyor",
        "özel sektör":"özel",
        "diğer":"diger",
        "di̇ğer":"diger",
        "-":"calismiyor"
    }
    df['Anne Sektor'] = df['Anne Sektor'].replace(replace_map)
    return df

def cleanLise(df):
    replace_map = {
        "diğer":"diger",
        "meslek lisesi":"meslek",
        "anadolu lisesi":"anadolu",
        "düz lise":"düz",
        "özel lisesi":"özel",
        "i̇mam hatip lisesi":"i̇mam hatip",
        "özel lise":"özel"
    }
    df['Lise Turu'] = df['Lise Turu'].replace(replace_map)
    return df

def cleanFatherEducation(df):
    replace_map = {
    'i̇lkokul mezunu': 'ilkokul',
    'ortaokul mezunu': 'ortaokul',
    'üniversite mezunu': 'üniversite',
    'lise mezunu': 'lise',
    'eğitimi yok': 'egitimi yok',
    'eği̇ti̇m yok': 'egitimi yok',
    'eğitim yok': 'egitimi yok',
    'yüksek li̇sans': 'yüksek lisans',
    'yüksek lisans / doktora': 'doktora',
    '0': 'bilinmiyor',
    "i̇lkokul":"ilkokul",
    "li̇se":"lise",
    "yüksek lisans / doktara":"doktora",
    "üni̇versi̇te":"üniversite"
    }
    df['Baba Egitim Durumu'] = df['Baba Egitim Durumu'].replace(replace_map)
    return df

def cleanEducation(df):
    replace_map = {
        'ilkokul mezunu': 'ilkokul',
        'i̇lkokul mezunu': 'ilkokul',
        'i̇lkokul': 'ilkokul',
        'li̇se': 'lise',
        'ortaokul mezunu': 'ortaokul',
        'lise mezunu ': 'lise',
        'lise mezunu': 'lise',
        'eği̇ti̇m yok': 'egitimi yok',
        'eğitim yok': 'egitimi yok',
        "eğitimi yok":"egitimi yok",
        'üni̇versi̇te': 'üniversite',
        'üniversite mezun': 'üniversite',
        'üniversite mezunu': 'üniversite',
        'yüksek lisans': 'yüksek li̇sans',
        'yüksek lisans / doktora': 'doktora',
        'yüksek lisans / doktara': 'doktora'
    }
    df['Anne Egitim Durumu'] = df['Anne Egitim Durumu'].replace(replace_map)
    return df

def clean_date(date_str):
    if pd.isnull(date_str) or date_str.strip() == "":
        return pd.NaT
    date_str = date_str.split()[0]
    
    try:
        return pd.to_datetime(date_str, errors='coerce', dayfirst=True)
    except Exception as e:
        print(f"Error parsing date: {date_str}, error: {e}")
        return pd.NaT


def convert_to_standard_scale(note):
    try:
        note_str = str(note)
        if '-' in note_str:
            min_val, max_val = map(float, note_str.split('-'))
            note = (min_val + max_val) / 2
        else:
            note = float(note)
        if 75 <= note <= 100:
            return (note - 75) / 25 * 4
        elif 3 <= note <= 4:
            return note
        elif 25 <= note <= 50:
            return (note - 25) / 25 * 4
        elif 0 <= note < 25:
            return (note / 25) * 4
        else:
            return None
    except ValueError:
        return None
    
def categorize_grade(grade):
    if 0.00 <= grade < 1.00:
        return '0.00-1.00'
    elif 1.00 <= grade < 2.00:
        return '1.00-2.00'
    elif 2.00 <= grade < 3.00:
        return '2.00-3.00'
    elif 3.00 <= grade <= 4.00:
        return '3.00-4.00'
    else:
        return None 

def normalize_grade_range(grade):
    if grade is None:
        return "Bilinmiyor"
    grade = str(grade).strip().lower()
    if "ortalama" in grade or "yok" in grade or "hazırlık" in grade:
        return "Bilinmiyor"
    if '-' in grade:
        numbers = re.findall(r'\d+\.?\d*', grade)
        if len(numbers) == 2:
            min_val = float(min(numbers))
            max_val = float(max(numbers))
            avg_val = (min_val + max_val) / 2
        elif len(numbers) == 1:
            avg_val = float(numbers[0])
        else:
            return "Bilinmiyor"
    elif "ve altı" in grade:
        numbers = re.findall(r'\d+\.?\d*', grade)
        if len(numbers) > 0:
            avg_val = float(numbers[0])
        else:
            return "Bilinmiyor"
    else:
        numbers = re.findall(r'\d+\.?\d*', grade)
        if len(numbers) > 0:
            avg_val = float(numbers[0])
        else:
            return "Bilinmiyor"
    if 0.00 <= avg_val < 1.00:
        return "0.00-1.00"
    elif 1.00 <= avg_val < 2.00:
        return "1.00-2.00"
    elif 2.00 <= avg_val < 3.00:
        return "2.00-3.00"
    elif 3.00 <= avg_val <= 4.00:
        return "3.00-4.00"
    else:
        return "Bilinmiyor"

def fill_na_with_bilinmiyor(df, column_list):
    """
    Belirli sütunlarda NaN olan hücreleri 'Bilinmiyor' ile doldurur.
    
    Args:
    df (pd.DataFrame): DataFrame üzerinde işlem yapılacak tablo.
    column_list (list): NaN değerleri doldurulacak sütun isimleri.
    
    Returns:
    pd.DataFrame: NaN değerleri 'Bilinmiyor' ile doldurulmuş DataFrame.
    """
    # Belirtilen sütunlarda NaN olan hücreleri doldur
    df[column_list] = df[column_list].fillna('Bilinmiyor')
    return df