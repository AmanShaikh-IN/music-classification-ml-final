# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import scipy
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

'''
from google.colab import files
from google.colab import drive

drive.mount("/content/drive", force_remount = True)

for dir, subdir, files in os.walk("/content/drive/MyDrive"):
  print(dir, subdir, files, sep = "\n")
  print()

'''

file_path = "data/music_dataset_mod.csv"
df = pd.read_csv(file_path)

"""# Data Exploration"""

df_music_realistic = df.copy()
df_music_realistic

df_music_realistic.info()

df_music_realistic['Genre'].value_counts()

plt.figure(figsize=(8, 6))
sns.countplot(x='Genre', data=df_music_realistic)
plt.title('Distribution of Music Genres')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

"""# Correlation Analysis"""

#As seen above, since it is our target itself that showcases missing values, I can't impute the missing values or else I risk memory leaks.

df_music_realistic_nonull = df_music_realistic.dropna()
df_music_realistic_nonull

# Splitting the dataset into features and target

X = df_music_realistic_nonull.drop(columns=['Genre'])
y = df_music_realistic_nonull['Genre']

# I used ordinal encoding to feature engineer the existing categorical variables

le = LabelEncoder()
y_encoded = le.fit_transform(y)

df_with_encoded_genre = df_music_realistic_nonull.copy()
df_with_encoded_genre.drop(columns=['Genre'], inplace=True)
df_with_encoded_genre['Genre_encoded'] = y_encoded
df_with_encoded_genre

# Calculating the correlation matrix

correlation_matrix = df_with_encoded_genre.corr()

plt.figure(figsize=(15, 6))

mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k = 1)

sns.heatmap(correlation_matrix,
            mask = mask,
            vmin=-1,
            vmax=1,
            annot=True,
            cmap="RdBu",
            linewidths=0.1)

plt.title("Correlation Matrix", fontsize=18)
plt.yticks(rotation=0)
plt.show()

"""# PCA for Dimensionality Reduction"""

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA()
X_pca = pca.fit_transform(X_scaled)

explained_variance = pca.explained_variance_ratio_
explained_variance

plt.figure(figsize=(10,6))
plt.plot(range(1,13),explained_variance.cumsum(),marker='o', linestyle='--')
plt.title('Explained variance by components')
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance')
plt.show()

# Given the plot, we can observe the elbow to be around 8-9 and so I use the first eight principal components

pca = PCA(n_components=8)
X_pca = pca.fit_transform(X_scaled)

"""# PCA Data v/s Original Data Evaluation

## PCA Data Evaluation
"""

# train test split

X_train, X_test, y_train, y_test = train_test_split(X_pca, y_encoded, test_size=0.3, random_state=42)

classifier = LogisticRegression(max_iter=10000)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print("Accuracy with PCA:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))

"""## Original Data Evaluation"""

# train test split

X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(X_scaled, y_encoded, test_size=0.3, random_state=42)

logreg_orig = LogisticRegression(max_iter=10000)
logreg_orig.fit(X_train_orig, y_train_orig)

y_pred_orig = logreg_orig.predict(X_test_orig)
print("Accuracy with Original Features:", accuracy_score(y_test_orig, y_pred_orig))
print("\nClassification Report with Original Features:\n", classification_report(y_test_orig, y_pred_orig, target_names=le.classes_))

"""# Genre Prediction and Integration"""

df_unknown_genre = df_music_realistic[df_music_realistic['Genre'].isnull()].copy()
df_unknown_genre

# Prepare the data for prediction
X_unknown = df_unknown_genre.drop(columns=['Genre'])
X_unknown_scaled = scaler.transform(X_unknown)
X_unknown_pca = pca.transform(X_unknown_scaled)

y_unknown_pred = classifier.predict(X_unknown_pca)

df_unknown_genre.loc[:, 'Predicted_Genre'] = le.inverse_transform(y_unknown_pred)

print(df_unknown_genre[['Predicted_Genre']])

