import pandas as pd
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from pandas.api.types import CategoricalDtype

df = pd.read_csv("cleanedData.csv")
df = df.dropna()

# Label Encoding işlemini yapan fonksiyon
def encode_label(df, column):
    label_encoder = LabelEncoder()
    df[column] = label_encoder.fit_transform(df[column])

# Sıralı kategorik veriyi düzenleyen fonksiyon
def set_categorical(df, column, categories):
    cat_type = CategoricalDtype(categories=categories, ordered=True)
    df[column] = df[column].astype(cat_type)

# Cinsiyet sütununu encode işlemi
encode_label(df, 'Cinsiyet')

# Yaş hesaplama
df['Dogum Tarihi'] = pd.to_datetime(df['Dogum Tarihi'], errors='coerce', dayfirst=True)
df['Yas'] = (datetime.now() - df['Dogum Tarihi']).dt.days // 365.25
df = df.drop(columns=["Dogum Tarihi"])

# Diğer label encoding işlemleri
encode_label(df, 'Dogum Yeri')
encode_label(df, 'Ikametgah Sehri')
encode_label(df, 'Universite Turu')

# Burs yüzdesini kategorize etme
df['Burslu ise Burs Yuzdesi'] = df['Burslu ise Burs Yuzdesi'].replace(-1.0, 100.0)
bins = [0, 25, 50, 75, 100, 101]
labels = ['Düşük', 'Orta', 'Yüksek', 'Çok Yüksek', 'En Önemli']
df['Burslu ise Burs Yuzdesi'] = pd.cut(df['Burslu ise Burs Yuzdesi'], bins=bins, labels=labels, right=False)

# Diğer burs, üniversite ve eğitim durumu sütunları için label encoding
encode_label(df, 'Burs Aliyor mu?')
encode_label(df, 'Universite Kacinci Sinif')

# Sıralı kategoriler
set_categorical(df, 'Universite Not Ortalamasi', ['Bilinmiyor', '0.00-1.00', '1.00-2.00', '2.00-3.00', '3.00-4.00'])
encode_label(df, 'Daha Once Baska Bir Universiteden Mezun Olmus')
encode_label(df, 'Lise Turu')
set_categorical(df, 'Lise Mezuniyet Notu', ['Bilinmiyor', '0.00-1.00', '1.00-2.00', '2.00-3.00', '3.00-4.00'])

# Anne ve baba eğitim durumu için sıralı kategoriler
set_categorical(df, 'Anne Egitim Durumu', ['Bilinmiyor','egitimi yok', 'ilkokul', 'ortaokul', 'lise', 'üniversite', 'yüksek li̇sans', 'doktora'])
encode_label(df, 'Anne Calisma Durumu')
encode_label(df, 'Anne Sektor')

set_categorical(df, 'Baba Egitim Durumu', ['Bilinmiyor','egitimi yok', 'ilkokul', 'ortaokul', 'lise', 'üniversite', 'yüksek li̇sans', 'doktora'])
encode_label(df, 'Baba Calisma Durumu')
encode_label(df, 'Baba Sektor')

# Diğer sütunlar için label encoding
encode_label(df, 'Girisimcilik Kulupleri Tarzi Bir Kulube Uye misiniz?')
encode_label(df, 'Profesyonel Bir Spor Daliyla Mesgul musunuz?')
set_categorical(df, 'Spor Dalindaki Rolunuz Nedir?', ['Bilinmiyor', 'yok', 'diger', 'bireysel', 'takım oyuncusu', 'kaptan'])
encode_label(df, 'Aktif olarak bir STK üyesi misiniz?')
encode_label(df, 'Stk Projesine Katildiniz Mi?')
encode_label(df, 'Girisimcilikle Ilgili Deneyiminiz Var Mi?')
encode_label(df, 'Ingilizce Biliyor musunuz?')

# İngilizce seviyesi sıralı kategorik veri
set_categorical(df, 'Ingilizce Seviyeniz?', ['Bilinmiyor', '0', 'başlangıç', 'orta', 'ileri'])

df.to_csv("proccesingData.csv",index=False)