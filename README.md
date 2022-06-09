# PCA & AutoEncoder
# Dimensionality Reduction comparison (Artificial Intelligence class, 2021-2) #

## 0. Intro ##
사용한 데이터
(Iris : setosa, versicolor, virginica 의 꽃받침(sepal) 과 꽃잎(petal) 의 길이를 정리)


![image](https://user-images.githubusercontent.com/82162578/172845076-a2d8f656-fd82-47c4-8a6b-3dffe90de31f.png)

(왼쪽부터 꽃받침 길이, 너비 , 꽃잎의 길이 너비)

---


## 1. PCA Dimensionality Reduction ##

주성분 분석 (Principal Component Analysis) : 데이터를 hyperplane에 투영 (projection) 하는 방식

![image](https://user-images.githubusercontent.com/82162578/172846469-4eda65b5-043d-4493-8b94-d6df367ff718.png)

## 2-1. AutoEncoder with Linear Activation Function ##

Activation Func : Linear, Optimization : Adam , Loss Func : MSE 

![image](https://user-images.githubusercontent.com/82162578/172847479-e0718c5e-1122-4b4f-ac1d-0d536f89d809.png)
![image](https://user-images.githubusercontent.com/82162578/172847468-5ce7ccbd-1ac2-4b00-8d3e-2be4c2b535a6.png)



## 2-2. AutoEncoder with NonLinear Activation Function ##

Activation Func : Sigmoid , Optimization : Adam , Loss Func : MSE 

![image](https://user-images.githubusercontent.com/82162578/172847906-f798427a-cdca-4140-a5c9-981749a73d10.png)
![image](https://user-images.githubusercontent.com/82162578/172847888-c029d4d0-65fa-4782-b854-4203ea661230.png)


## 3. Performance Comparison (Cluster = 2 , Cluster = 3 case) ##

Homogeneity (균질성) : [0,1] , Bigger is better 

Completeness (완전성) 

V - measure (균질성과 완전성의 조합 평균치) 

Adjusted Rand Index : 가능한 모든 쌍에서 정답인 쌍의 개수 비율 (정확도), 이때 기존 Rand Index 에서 기댓값과 분산을 재조정함 

Adjusted Mutual Information : 두 확률변수간의 상호 의존성 측정 (높을수록 우위) 

Silhouette Coefficient : 정답(groundtruth) 가 존재하지 않을 때 군집화가 잘 되었는지 판단하는 기준이다. 이를 이용해 군집의 개수를 사용자가 정할 수 있다. (높을수록 우위) 

![image](https://user-images.githubusercontent.com/82162578/172848968-94fba40c-b58f-4455-9c3a-40f5d49ba157.png)
![image](https://user-images.githubusercontent.com/82162578/172848981-fbc9ef52-2be8-4fdb-82ab-cc2080b9b3f1.png)

PCA 방식이 대체적으로 우위를 점하고 있으나, Silhouette Coefficient 즉 정답이 존재하지 않을 경우에는   
Sigmoid 함수를 사용한 AutoEncoder가 더 성능이 좋게 측정됨     
배운 내용을 토대로 유추해보면, PCA 방식의 경우 정답 라벨이 존재하는 상태에서 군집화를 진행할 경우 이득을 볼 수 있으며 (지도학습)   
AutoEncoder의 경우 정답 라벨이 없는 상태에서 군집화 진행시 유리하다 (비지도학습)  
