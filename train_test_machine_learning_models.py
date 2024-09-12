import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 1. Veri Setini Yükle
df = pd.read_csv('proccesingData.csv')
df = df.dropna()

# 2. Bağımlı ve Bağımsız Değişkenleri Belirle
X = df.drop(columns=['Degerlendirme Puani'])  # Hedef sütunun adı 'Degerlendirme Puani' olarak varsayılıyor
y = df['Degerlendirme Puani']

# 3. Sayısal ve Kategorik Sütunları Ayırma
numerical_columns = X.select_dtypes(include=['float64', 'int64']).columns
categorical_columns = X.select_dtypes(include=['object', 'category']).columns

# 4. Veriyi Eğitim ve Test Setlerine Ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 5. Sayısal Verileri Ölçeklendirme
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train[numerical_columns])
X_test_scaled = scaler.transform(X_test[numerical_columns])

# 6. Kategorik Verilere Label Encoding (İsterseniz One-Hot Encoding de kullanabilirsiniz)
label_encoder = LabelEncoder()
for col in categorical_columns:
    X_train[col] = label_encoder.fit_transform(X_train[col])
    X_test[col] = label_encoder.transform(X_test[col])

# 7. Sayısal ve Kategorik Verileri Birleştirme
X_train_final = pd.concat([pd.DataFrame(X_train_scaled, columns=numerical_columns), X_train[categorical_columns].reset_index(drop=True)], axis=1)
X_test_final = pd.concat([pd.DataFrame(X_test_scaled, columns=numerical_columns), X_test[categorical_columns].reset_index(drop=True)], axis=1)

# 8. Modelleri Tanımlayın
models = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(),
    'Support Vector Machine': SVC(),
    'K-Nearest Neighbors': KNeighborsClassifier()
}

# 9. Modelleri Eğitin ve Test Edin
print("Modellerin Test Seti Performansı:")
for name, model in models.items():
    model.fit(X_train_final, y_train)
    predictions = model.predict(X_test_final)
    accuracy = accuracy_score(y_test, predictions)
    print(f"{name} Accuracy: {accuracy:.4f}")

# 10. K-Fold Cross Validation (K=5)
kf = KFold(n_splits=5, shuffle=True, random_state=42)

print("\nK-Fold Cross-Validation Sonuçları:")
for name, model in models.items():
    cv_scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')
    print(f"{name} Cross-Validation Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
