# -*- coding: utf-8 -*-
"""PCA vs Autoencoder

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_EldxHiS0qmf1VZsUr4YZqdv0rQtoDuW
"""

# Commented out IPython magic to ensure Python compatibility.
import keras
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint
from keras import regularizers
from tensorflow.keras.optimizers import Adam
from keras import regularizers
from sklearn import datasets
from sklearn import decomposition
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics



# %matplotlib inline

RANDOM_SEED = 37117
np.random.seed(RANDOM_SEED)

import functools
import tensorflow as tf

from google.colab import drive
drive.mount('/content/drive')

data =pd.read_csv('/content/drive/MyDrive/숙제3_데이터 (1).csv')

type(data)
data

pca = decomposition.PCA(n_components = 2)

pca.fit(data)

pca_data = pca.transform(data)
print(pca_data.shape)

pca_comp = ['pca_component1', 'pca_component2']

#0 데이터 사전 준비작업 (iris 데이터사용)

iris = datasets.load_iris()
X = iris.data
y = iris.target
target_names = iris.target_names

scaler = MinMaxScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

print(y)
print(type(target_names))

#1 PCA 를 이용한 차원 축소

def plot3clusters(X, title, vtitle):
  plt.figure()
  colors = ['navy', 'turquoise', 'darkorange']
  lw = 2

  for color, i, target_name in zip(colors, [0, 1, 2], target_names):
      plt.scatter(X[y == i, 0], X[y == i, 1], color=color, alpha=1., lw=lw,
                  label=target_name)
  plt.legend(loc='best', shadow=False, scatterpoints=1)
  plt.title(title)  
  plt.xlabel(vtitle + "1")
  plt.ylabel(vtitle + "2")
  plt.show()

pca = decomposition.PCA()
pca_transformed = pca.fit_transform(X_scaled)
plot3clusters(pca_transformed[:,:2], 'PCA', 'PC')

#2 오토 인코더 (선형 활성함수 사용) 를 이용한 차원 축소

# 기본 구성 : 활성함수 - 선형, optimizer : adam 사용, 손실함수는 평균제곱오차

'''
인코딩 시 2차원으로 변환
'''
input_dim = X_scaled.shape[1]
encoding_dim = 2  
input_img = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='linear')(input_img)
decoded = Dense(input_dim, activation='linear')(encoded)
autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='mse')
print(autoencoder.summary())

history = autoencoder.fit(X_scaled, X_scaled,
                epochs=1000,
                batch_size=16,
                shuffle=True,
                validation_split=0.1,
                verbose = 0)


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model train vs validation loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper right')
plt.show()


encoder = Model(input_img, encoded)
encoded_input = Input(shape=(encoding_dim,))
decoder_layer = autoencoder.layers[-1]
decoder = Model(encoded_input, decoder_layer(encoded_input))
encoded_data = encoder.predict(X_scaled)

plot3clusters(encoded_data[:,:2], 'Linear AE', 'AE')

#3 오토 인코더 (비선형 시그모이드 함수 사용) 를 이용한 차원 축소

# 기본 구성 : 활성함수 - sigmoid, optimizer : adam 사용, 손실함수는 평균제곱오차
input_dim2 = X_scaled.shape[1]
encoding_dim2 = 2  
input_img2 = Input(shape=(input_dim2,))
encoded2 = Dense(encoding_dim2, activation='sigmoid')(input_img2)
decoded2 = Dense(input_dim2, activation='sigmoid')(encoded2)
autoencoder2 = Model(input_img2, decoded2)
autoencoder2.compile(optimizer='adam', loss='mse')
print(autoencoder2.summary())

history2 = autoencoder2.fit(X_scaled, X_scaled,
                epochs=2000,
                batch_size=16,
                shuffle=True,
                validation_split=0.1,
                verbose = 0)

plt.plot(history2.history['loss'])
plt.plot(history2.history['val_loss'])
plt.title('model train vs validation loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper right')
plt.show()

encoder2 = Model(input_img2, encoded2)
encoded_input2 = Input(shape=(encoding_dim2,))
decoder_layer2 = autoencoder2.layers[-1]
decoder2 = Model(encoded_input2, decoder_layer2(encoded_input2))
encoded_data2 = encoder2.predict(X_scaled)

plot3clusters(encoded_data2[:,:2], 'Non-Linear sigmoid-based AE', 'AE')

plot3clusters(pca_transformed[:,:2], 'PCA', 'PC')  
plot3clusters(encoded_data[:,:2], 'Linear AE', 'AE')  
plot3clusters(encoded_data2[:,:2], 'Non-Linear sigmoid-based AE', 'AE')

# Commented out IPython magic to ensure Python compatibility.
#4 성능 비교 (군집 개수 2개일때와 3개일때를 각각 비교한다.)

'''보고서에는 분량 문제로 cluster=3 일때 기준으로 작성했습니다.
cluster 개수에 따른 각각의 성능 차이는 다르지 않습니다.'''

'''
균질성(homogeneity) : 0~1 사이 값이며 클수록 우위 
완전성(completeness) 
V- measure : 균질성, 완전성의 조합 평균
Adjusted Rand Index : 가능한 모든 쌍에서 정답인 쌍의 개수 비율 (정확도), 이때 기존 Rand Index 에서 기댓값과 분산을 재조정함
Adjusted Mutual Information : 두 확률변수간의 상호 의존성 측정 (높을수록 우위)
Silhouette Coefficient : 정답(groundtruth) 가 존재하지 않을 때 군집화가 잘 되었는지 판단하는 기준이다. 
이를 이용해 군집의 개수를 사용자가 정할 수 있다. (높을수록 우위)
'''



labels_true = y 
titles = ['PCA', 'Linear AE', 'Sigmoid AE']
for n_clusters_ in [2,3]:
  estimators = [('PCA'    , KMeans(n_clusters=n_clusters_), pca_transformed),
                ('AE linear' , KMeans(n_clusters=n_clusters_), encoded_data),
                ('AE sigmoid' , KMeans(n_clusters=n_clusters_), encoded_data2),]


  print('Number of clusters: %d' % n_clusters_)
  for name, est, data in estimators:
      X = data
      est.fit(X)
      labels = est.labels_
      print(name,':')
      print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
      print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
      print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
      print("Adjusted Rand Index: %0.3f"
#             % metrics.adjusted_rand_score(labels_true, labels))
      print("Adjusted Mutual Information: %0.3f"
#             % metrics.adjusted_mutual_info_score(labels_true, labels))
      print("Silhouette Coefficient: %0.3f"
#             % metrics.silhouette_score(X, labels))
      print()
  print()
  print('----------------------------------------------------------------------------------')
  print()