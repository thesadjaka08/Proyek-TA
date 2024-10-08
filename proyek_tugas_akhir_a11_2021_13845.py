# -*- coding: utf-8 -*-
"""Proyek Tugas Akhir_A11.2021.13845

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ERBFU8IpzH-P3CHScBDPQDc3SCZa5KyG

# **Thesa Permatasari Djaka - A11.2021.13845**
# **PREDIKSI KELAYAKAN PINJAMAN**
Prediksi kelayakan pinjaman adalah alat berbasis teknologi yang dirancang untuk membantu lembaga keuangan menilai kemampuan pemohon dalam membayar kembali pinjaman. Sistem ini bekerja dengan mengumpulkan, memproses, dan menganalisis data pemohon menggunakan algoritma machine learning. Berdasarkan data-data penting seperti pendapatan, riwayat kredit, dan jumlah tanggungan, sistem dapat memberikan prediksi yang akurat apakah pemohon layak atau tidak layak untuk mendapatkan pinjaman. Selain meningkatkan efisiensi, sistem ini juga mengurangi risiko gagal bayar dan menghindari bias dalam proses pengambilan keputusan.

# **Import Library**
"""

pip install pandas numpy xgboost

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, roc_auc_score
from sklearn import metrics
from sklearn import preprocessing
from sklearn.metrics import classification_report,confusion_matrix,precision_score,jaccard_score,recall_score,f1_score

import joblib
from google.colab import files

"""# **Data Understanding**"""

df = pd.DataFrame(pd.read_csv('Bank_Personal_Loan_Modelling.csv'))

df.head()

df.info()

df.nunique(axis=0, dropna=True)

df.isnull().sum()

df.isna().sum()

print('Number of duplicated data : ' , len(df[df.duplicated()]))

df.describe()

"""Seperti yang ditunjukkan dalam describe, ada nilai negatif dalam fitur 'Experience'. Experience adalah beberapa tahun, maka tidak boleh negatif dan harus benar. Oleh karena itu, kita akan mengubah nilai negatif pada fitur 'Experience' dengan nilai absolutnya."""

df['Experience'] = df['Experience'].abs()
df.describe()

""" Fitur 'Income' adalah pendapatan 'tahunan' dan fitur 'CCAvg' adalah pengeluaran 'bulanan'. Maka, akan disamakan rentang waktu pendapatan menjadi bulanan dengan membaginya dengan 12."""

df['Income'] = df['Income']/12
df

"""Selanjutnya menghapus fitur yang tidak berguna, yaitu fitur 'ID' dan 'ZIP Code'."""

df = df.drop(['ID', 'ZIP Code'],axis=1)
df

df.columns

"""# **Exploratory Data Analysis (EDA)**

Kolom yang ditargetkan, yaitu kolom 'Personal Loan'.
"""

print('*'*120)
print('number of customers : ',df.shape[0])
print('The number of Personal Loan = 0 : ',df['Personal Loan'].value_counts()[0])
print('The number of Personal Loan = 1 : ',df['Personal Loan'].value_counts()[1])
print('*'*120)

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
sns.countplot(data=df, x='Personal Loan',palette = "Dark2")
plt.title("count plot for Target(Personal Loan)")
plt.subplot(1,2,2)
plt.pie([df['Personal Loan'].value_counts()[0],df['Personal Loan'].value_counts()[1]],
        labels=['Personal Loan = 0','Personal Loan = 1'],autopct='%1.1f%%',colors=['teal','chocolate'])
plt.title("Percent of Personal Loan")
plt.tight_layout()
plt.show()

"""Berdasarkan persentase yang ada, kumpulan data kami tidak seimbang. Oleh karena itu, perlu dilakukan penanganan untuk mencapai keseimbangan dalam data.

Ada beberapa fitur diskrit dan beberapa fitur kontinu dalam dataset kami.
"""

descrete_col = df[['Family','Education','Securities Account','CD Account','Online','CreditCard']]
continuous_col = df[['Age','Experience','Income','CCAvg','Mortgage']]

for col in descrete_col :
    print('%s : ' %col , df[col].unique())

ax = sns.stripplot(data=descrete_col)
ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
plt.ylabel('Class values of descrete Features')
plt.xlabel('Name of descrete Features')
plt.title('OverView of classes of descrete Features')
plt.show()

"""Dapat dilihat pada gambar diatas terdapat 6 fitur yang bersifat diskrit:
- Family merupakan fitur multinomial dan terdiri dari minimal 1 orang dan paling banyak 4 orang : [1,2,3,4]
- Education adalah fitur multinomial dan terdapat 3 level : [1,2,3]
- 4 fitur sisanya adalah fitur biner, 0/1 berarti Tidak/Ya.
"""

display(continuous_col.describe().T)
ax = sns.stripplot(data=continuous_col)
ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
plt.ylabel('Range of Continuous Features')
plt.xlabel('Name of Continuous Features')
plt.show()

"""Terdapat 5 fitur kontinu sebagai berikut:
- Usia nasabah berada dalam rentang (23-67)
- Pengalaman nasabah maksimum adalah 43 tahun
- Pendapatan berada dalam rentang (0,67-18,66) per bulan
- Nilai CCAvg maksimum adalah 10
- Seperti yang terlihat di atas, tidak ada nilai Mortgage antara 0 dan 75; nilainya adalah 0 atau dalam rentang (75,635). Juga, kita dapat melihat bahwa sebagian besar nilai berada dalam rentang (75,400).
"""

for col in continuous_col.columns:
    plt.figure(figsize=(12,0.5))
    ax = sns.boxplot(x=df[col],color="greenyellow", linewidth=.75)
    ax.set_title(f'Distribution of {col} feature')
    plt.show()

"""- Seperti yang ditunjukkan pada box plot, pada dua fitur, Age dan Experience, sebaran datanya normal;
- Fitur lain, kami melihat beberapa outlier. Karena menyangkut jumlah uang atau nilai mortgage, jumlahnya bisa berapa pun, dan semuanya masuk akal, jadi tidak bisa menjadi noises.
"""

# Transformasi log
df['log_Income'] = np.log1p(df['Income'])
df['log_CCAvg'] = np.log1p(df['CCAvg'])
df['log_Mortgage'] = np.log1p(df['Mortgage'])

# Visualisasi distribusi sebelum dan sesudah transformasi log
plt.figure(figsize=(18, 10))

# Distribusi sebelum transformasi log
plt.subplot(3, 2, 1)
plt.hist(df['Income'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribusi Income Sebelum Transformasi Log')

plt.subplot(3, 2, 3)
plt.hist(df['CCAvg'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribusi CCAvg Sebelum Transformasi Log')

plt.subplot(3, 2, 5)
plt.hist(df['Mortgage'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribusi Mortgage Sebelum Transformasi Log')

# Distribusi setelah transformasi log
plt.subplot(3, 2, 2)
plt.hist(df['log_Income'], bins=20, color='lightgreen', edgecolor='black')
plt.title('Distribusi Income Setelah Transformasi Log')

plt.subplot(3, 2, 4)
plt.hist(df['log_CCAvg'], bins=20, color='lightgreen', edgecolor='black')
plt.title('Distribusi CCAvg Setelah Transformasi Log')

plt.subplot(3, 2, 6)
plt.hist(df['log_Mortgage'], bins=20, color='lightgreen', edgecolor='black')
plt.title('Distribusi Mortgage Setelah Transformasi Log')

plt.tight_layout()
plt.show()

df = df.drop(['Income','CCAvg','Mortgage'],axis=1)
df

"""Sebelumnya kami telah memeriksa kolom target 'Personal Loan' dan menemukan bahwa datanya tidak seimbang. Oleh karena itu, kami akan melakukan oversampling menggunakan metode SMOTE."""

from imblearn.over_sampling import SMOTE

# Pisahkan fitur dan target
X = df.drop('Personal Loan', axis=1)  # Fitur
y = df['Personal Loan']  # Target

# Terapkan SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Cek jumlah kelas setelah resampling
print("Jumlah kelas setelah SMOTE:")
print(y_resampled.value_counts())

# Visualisasi distribusi kelas setelah oversampling
plt.figure(figsize=(8, 4))
y_resampled.value_counts().plot(kind='bar', color=['lightgreen', 'orange'])
plt.title('Distribusi Kelas Setelah Oversampling dengan SMOTE')
plt.xlabel('Kelas')
plt.ylabel('Jumlah')
plt.xticks(rotation=0)
plt.show()

"""# **Data Analysis and Visualization**"""

descrete_col = df[['Family','Education','Securities Account','CD Account','Online','CreditCard']]
continuous_col = df[['Age','Experience','log_Income','log_CCAvg','log_Mortgage']]

plt.figure(figsize=(15,10))
for i,col in enumerate(list(descrete_col.columns)):
    plt.subplot(2,3,i+1)
    sns.countplot(data=df, x=col)
    plt.title(f"count plot for $\\mathbf{{{col}}}$")
plt.tight_layout()
plt.show()
#############################################################
descrete_cols_categories=[]
descrete_cols_categories_count=[]

for col in list(descrete_col.columns):
    pie_name1=[]
    pie_value1=[]
    for j in range(len(descrete_col[col].unique())) :
        pie_name1.append(descrete_col[col].unique()[j])
        pie_value1.append(descrete_col[descrete_col[col]==pie_name1[j]][col].count())
    descrete_cols_categories.append(pie_name1)
    descrete_cols_categories_count.append(pie_value1)

print('*'*120)
print('Descrete columns name : \n' , list(descrete_col.columns))
print('Descrete columns categories : \n' , descrete_cols_categories)
print('Descrete columns categories count : \n' , descrete_cols_categories_count)
print('\n')
print('*'*120)
#############################################################
rows = 3
cols = 2

# Create subplots
fig = make_subplots(rows=rows, cols=cols, specs=[[{"type": "pie"}, {"type": "pie"}],[{"type": "pie"}, {"type": "pie"}],
                                           [{"type": "pie"}, {"type": "pie"}]])


for i in range(rows * cols) :
    fig.add_trace(go.Pie(labels=descrete_cols_categories[i], values=descrete_cols_categories_count[i], name=descrete_col.columns[i]),
                  row=int(np.ceil((i+1)/2)), col=(i%2)+1)


fig.update_layout(margin=dict(t=35, b=35, l=35, r=35))
fig.update(layout_title_text='Percent Of values in descrete columns',
           layout_showlegend=True)

fig = go.Figure(fig)
fig.show()

"""Dapat dilihat pada grafik yaitu :
- dalam hal jumlah family, pelanggan dengan 1 orang keluarga memiliki jumlah pelanggan terbanyak (29,4% dari seluruh pelanggan) dan dengan 3 orang keluarga memiliki jumlah pelanggan paling sedikit (20,2% dari seluruh pelanggan).
- pada education, sebagian besar pelanggan adalah undergraduate (41,9%).
- Sebagian besar nasabah belum memiliki Securities Account(89,6%)
- Hanya sedikit pelanggan yang memiliki CD Account dan sebagian besar tidak memilikinya
- Lebih dari separuh pelanggan menggunakan Online services (59,7%)
- Hanya 29,4% pelanggan yang menggunakan credit card dan sebagian besar tidak menggunakannya
"""

plt.figure(figsize=(15,10))
for i,col in enumerate(list(descrete_col.columns)):
    plt.subplot(2,3,i+1)
    sns.countplot(data=df, x=col,hue='Personal Loan')
    plt.title(f"count plots for $\\mathbf{{{col}}}$")
plt.tight_layout()
plt.show()

"""Plot ini menunjukkan jumlah pelanggan yang diberikan pinjaman berdasarkan fitur khusus.
- sebagian besar nasabah adalah family dengan 1 orang, namun keluarga dengan 3 dan 4 orang mendapat pinjaman lebih banyak dibandingkan yang lain.
- education sebagian besar nasabah adalah undergraduate, namun nasabah graduate dan professional diberikan pinjaman lebih banyak dibandingkan yang lain.
- Sebagian besar nasabah yang diberi pinjaman tidak memiliki securities account, sehingga menyoroti pentingnya berbagai fitur dalam meningkatkan peluang diberikan pinjaman.
- Sebagian besar pelanggan yang diberikan pinjaman tidak memiliki CD Accounts.
- Kebanyakan nasabah yang diberi pinjaman tidak menggunakan Credit Card.
- Sebagian besar pelanggan yang diberikan pinjaman menggunakan Online services.
"""

# Membuat heatmap korelasi antar fitur
plt.figure(figsize=(15,8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Heatmap Korelasi')
plt.show()

plt.figure(figsize=(18,12))
for i,col in enumerate(continuous_col.columns):
    plt.subplot(3,2,i+1)
    sns.histplot(x=df[col],hue = df['Personal Loan'],kde=True)
    plt.title(f"Personal Loan Vs $\\mathbf{{{col}}}$",fontsize=18)

plt.tight_layout()
plt.show()

#############################################################################
print('\n')
print('*'*120)

plt.figure(figsize=(15,10))
for i,col in enumerate(continuous_col.columns):
    plt.subplot(3,2,i+1)
    color=['blue','orange']
    for j in list(df['Personal Loan'].unique()) :
        sns.kdeplot(df[df['Personal Loan']==j][col],color=color[j],fill=True,label=j)
        plt.legend()
    plt.title(f"Distribution of Personal Loan on $\\mathbf{{{col}}}$ feature")
plt.tight_layout()
plt.show()

"""Plot ini menunjukkan jumlah dan distribusi pelanggan berdasarkan fitur continuous
- Age nasabah yang diberi pinjaman adalah (26-65).
- Plot Experience menunjukkan bahwa pelanggan dengan jumlah pengalaman berapa pun dapat diberikan pinjaman.
- Kisaran Income nasabah yang diberi pinjaman adalah (5-17.5), sebagian besar nasabah yang menerima pinjaman memiliki pendapatan pada kisaran (7.5-16.5).
- plot Income kde dengan jelas menunjukkan bahwa peluang untuk mendapatkan pinjaman meningkat dengan meningkatnya pendapatan.
- Sebagian besar Pelanggan memiliki CCAvge <=3 (sekitar 83% dari seluruh pelanggan) sehingga di antara pelanggan tersebut 95,98% yang tidak diberikan pinjaman dan 4,02% diberikan, juga lebih sedikit pelanggan yang memiliki CCAvg >3 (sekitar 17% dari seluruh pelanggan) dibandingkan diantaranya 36,87% yang diberi pinjaman dan 63,13% tidak diberikan. Jadi, persentase ini menunjukkan bahwa nilai CCAvg yang besar meningkatkan peluang diberikan pinjaman.
- Sebagian besar pelanggan tidak memiliki mortgage apa pun (mortgage=0).

Cek data yang akan digunakan untuk pembuatan Model Machine Learning
"""

df

# Fungsi untuk mengubah logaritma ke nilai asli
def log_to_rupiah(log_value):
    return np.exp(log_value)

# Konversi nilai logaritma ke Rupiah
df['Income'] = df['log_Income'].apply(log_to_rupiah)
df['CCAvg'] = df['log_CCAvg'].apply(log_to_rupiah)
df['Mortgage'] = df['log_Mortgage'].apply(log_to_rupiah)

# Mengubah nilai ke format tanpa tanda titik
df['Income'] = (df['Income'] * 1000000).astype(int)
df['CCAvg'] = (df['CCAvg'] * 1000000).astype(int)
df['Mortgage'] = (df['Mortgage'] * 1000000).astype(int)

# Hapus kolom logaritma jika tidak diperlukan lagi
df = df.drop(columns=['log_Income', 'log_CCAvg', 'log_Mortgage'])

# Tampilkan DataFrame yang telah diperbarui
print(df)

df

df.info()

df.isna().sum()

"""# **Pelatihan Model**"""

# Fungsi untuk memberikan bobot pada fitur berdasarkan rentang nilai yang berbeda
def apply_feature_weights(df, feature_weights, binary_weights=None, default_weight=0.5):
    df_weighted = df.copy()
    for feature, ranges in feature_weights.items():
        def weight_value(x):
            for lower, upper, weight in ranges:
                if lower <= x <= upper:
                    return x * weight
            return x * default_weight

        df_weighted[feature] = df_weighted[feature].apply(weight_value)

    if binary_weights:
        for feature, (weight_0, weight_1) in binary_weights.items():
            df_weighted[feature] = df_weighted[feature].apply(
                lambda x: x * weight_0 if x == 0 else x * weight_1)

    return df_weighted

# Mendefinisikan rentang nilai dan bobot untuk fitur-fitur tertentu
feature_weights = {
    'Age': [(18, 40, 2.0), (41, 60, 1.5), (61, np.inf, 1.0)],
    'Experience': [(0, 5, 1.0), (6, 10, 1.5), (11, np.inf, 2.0)],
    'Family': [(0, 2, 2.0), (3, 5, 1.5), (6, np.inf, 1.0)],
    'Income': [(0, 15000000, 1.0), (16000000, 30000000, 1.5), (31000000, np.inf, 2.0)],
    'CCAvg': [(0, 15000000, 2.0), (15000000, 45000000, 1.5), (45000000, np.inf, 1.0)],
    'Education': [(1, 1, 1.0), (2, 2, 1.5), (3, 3, 2.0)],
    'Mortgage': [(0, 500000000, 1.0), (501000000, 900000000, 1.5), (901000000, np.inf, 2.0)]
}

# Mendefinisikan bobot untuk fitur biner
binary_weights = {
    'Securities Account': (1.0, 1.5),
    'CD Account': (1.0, 2.0),
    'Online': (1.0, 1.5),
    'CreditCard': (1.0, 2.0),
}

# Memisahkan fitur dan label
X = df.drop('Personal Loan', axis=1)
y = df['Personal Loan']

# Menerapkan bobot pada fitur-fitur tertentu
X_weighted = apply_feature_weights(X, feature_weights, binary_weights)

# Membagi data menjadi set latih dan uji
X_train, X_test, y_train, y_test = train_test_split(X_weighted, y, test_size=0.2, stratify=y, random_state=42)

# Melatih model XGBoost dengan parameter yang sesuai
scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])
model = xgb.XGBClassifier(
    scale_pos_weight=scale_pos_weight,
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42,
    max_depth=4,             # Membatasi kedalaman pohon
    min_child_weight=3,      # Membatasi jumlah minimum sampel dalam node daun
    gamma=0.2,               # Membatasi node yang terbelah
    subsample=0.8,           # Pengambilan sampel data training secara acak
    colsample_bytree=0.8,    # Pengambilan sampel kolom secara acak
    learning_rate=0.1,       # Mengatur kecepatan pembelajaran
    n_estimators=100,        # Jumlah pohon dalam model
    early_stopping_rounds=10 # Penggunaan early stopping
)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

# Memprediksi dan mengevaluasi hasil
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Menggunakan metrik evaluasi yang sesuai
print(classification_report(y_test, y_pred))
print("ROC-AUC Score:", roc_auc_score(y_test, y_pred_proba))

# Menyimpan model ke dalam file dengan format .sav
filename = 'model_xgb.sav'
joblib.dump(model, filename)
print(f"Model saved to {filename}")

# Mengunduh file secara otomatis ke komputer lokal
files.download(filename)