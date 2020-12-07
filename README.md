# stock
- 실시간으로 각 주식시장별 종목의 시세 조회 및 분석
- 누적된 데이터와 머신러닝 모델을 기반으로 예측.  
위의 두 가지 기능을 중점으로 하는 웹 사이트를 목표로 합니다.

## 사용될 스택
- Django & DRF (Django Rest Framework)  
>> 백엔드서버로써 사용합니다.  

- React.js
>> 프론트엔드로써 사용합니다.  

- Selenium  
>> 데이터 크롤링 엔진.  

- MongoDB  
>> MongoDB를 채택한 이유는 스키마의 제약을 덜 받기 위함입니다. 

- Logistic Regression (Sklearn)  
>> 주가 데이터를 선형회귀 분석을 통해 예측.  
전체적인 서비스가 구현이 되면 다른 모델을 도입하며 정확도를 높여나갈 예정입니다.  

- Matplotlib  
>> 데이터 시각화 모듈.

## 계획 및 진행과정  

### 1. 백엔드서버 구축  
#### 1-1. 앱 설계  
django 프로젝트는 여러 app들로 구성되어 있다. 즉, 프로젝트는 하나의 웹사이트이고, 각 앱들은 하나의 웹사이트에 속해있는 기능들이라고 생각하면 된다. e.g) 게시판, 이메일, 결제..  
현재 진행할 주제에는 기능이 **실시간 주가 정보 조회, 주가 정보 예측**이 있다. 고로 두 가지의 앱을 생성할 것이다.  

```
python manage.py startapp stock_inquiry
python manage.py startapp stock_prediction
```  

2020-12-04 : API 서버로 사용할 rest_api 앱도 생성한다.  

```
python manage.py startapp rest_api
```

#### 1-2. DRF 적용  

```
pip install djangorestframework
```  

DRF를 설치한 후 settings.py에 다음과 같이 적어준다.  

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stock_inquiry',
    'stock_prediction',
    'rest_framework', # DRF를 앱으로 등록
    'rest_api' # api 서버로 사용할 앱
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```  

rest_api앱에 urls.py를 생성한 뒤, 루트 urls.py에 다음과 같은 경로를 매핑한다.  

```
urlpatterns = [
    ...
    path('rest_api/', include('rest_api.urls')),
]
```  

rest_api의 models.py를 작성해보자.  

```
from django.db import models


# Create your models here.
class Post(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name
```  

그 다음 해당 모델을 serialize해야 한다.  
그 이유는 Django ORM의 Queryset은 Context로써 Django template으로 넘겨지며, HTML로 렌더링되어 Response로 보내지게 된다.
하지만 **JSON으로 데이터를 보내야 하는 RESTful API**는 HTML로 렌더링 되는 Django template를 사용할 수 없다. 그래서 Queryset을 Nested한 JSON
으로 매핑하는 과정을 거쳐야 하기 때문이다. (Queryset >> Json : Serialize)  

rest_api앱에 serializers.py를 작성해보자.  

```
from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'user_id',
            'user_name'
        )

```  

model과 serializer를 완성시켰으니 이제 view를 작성할 차례이다.  
rest_api/views.py  

```
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import PostSerializer
from .models import Post


# Create your views here.
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

```  

url을 매핑시켜보자.  
rest_api/urls.py  

```
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostView


post_list = PostView.as_view({
    'post': 'create',
    'get': 'list'
})

post_detail = PostView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:pk>/', post_detail, name='post_detail')
])

```


#### 1-2 뷰 설계  
##### 1-2-1 실시간 주가 정보 조회앱의 뷰 설계  

- 기능 패널  
모든 뷰의 우측에 패널로써 존재. 해당 패널에는 기능(Util)들이 속해있다.  
깔끔한 디자인을 위해 무한스크롤형 리스트에 기능을 추가한다. (기능의 확장 고려)  

- 즐겨찾기 관리    
기능 패널에 속해있는 기능.  
사용자가 등록해둔 종목의 상세 정보 조회 뷰로 이동할 수 있게 한다.  

- 종목별 주가 비교  
기능 패널에 속해있는 기능.  
종목별 주가 비교 뷰로 이동할 수 있게 한다.  

- 주식시장 선택 뷰 (무한스크롤형)  
각 주식시장별 그래프를 띄우며, 해당 주식시장(코스피200, 코스닥150)의 종목별 주가 정보 조회 뷰로 접근할 수 있게 해준다.  
무한스크롤형을 선택한 이유는 주식시장이 추가되는 경우를 고려한 것이다.  

- 종목별 주가 정보 조회 뷰 (List)  
현재 시점 해당 주식시장의 여러 종목의 주가를 조회 가능.  
해당 종목에 하이퍼링크를 달아 상세 정보 조회 뷰로 넘어갈 수 있게 한다.  

- 해당 종목 상세 정보 조회 뷰 (Detail)  
해당 종목의 주가를 기간별로 조회 가능 (그래프 적용)  
e.g) 1년전, 6개월전, 3개월전, 1개월전  

- 종목별 주가 비교 뷰  
사용자가 원하는 종목을 추가하면 그래프를 겹쳐서 그림  

##### 1-2-1 주가 정보 예측앱의 뷰 설계  
- 해당 종목 주가 예측 뷰  
해당 종목의 예측주가를 그래프로 시각화  
종목별로 뷰가 동일할 것으로 예상되므로 **템플릿** 적용  

#### 1-3 모델 설계  
- 사용자 정보 모델 (즐겨찾기 종목 포함)  
- 주식시장 모델  
- 주식종목 모델  

### 2. DB 연동  

### 3. 네이버 금융 주가 데이터 크롤링  
#### 3-1. CRUD 테스트 : MongoDB  

### 4. 프론트엔드 뷰 구축  

### 5. Logistic Regression 적용  

### 6. 데이터 시각화  

### 7. 다른 머신러닝 모델 적용 및 테스트
