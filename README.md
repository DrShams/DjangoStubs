[[Python]]
[[Django]]
#### Создать проект
```shell
django-admin startproject DjangoStubs
cd DjangoStubs
python manage.py startapp api
```

Установить необходимые dependency для REST приложений
```shell
pip install djangorestframework
```

Добавить в INSTALLED_APPS эти зависимости
```python
#-> DjangoStubs/settings.py
INSTALLED_APPS = [
    # default apps...
    'rest_framework',
    'api',
]
```

Создать сериализатор
```python
#-> api/serializers.py
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    userId = serializers.IntegerField()
    id = serializers.IntegerField(required=False)
    
```

Создать views
```python
#-> api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, PostSerializer
import random
import string

class UserView(APIView):
    def get(self, request, id):
        # generate random text for name
        name = ''.join(random.choices(string.ascii_letters, k=8))
        data = {"id": id, "name": name}
        serializer = UserSerializer(data)
        return Response(serializer.data)

class PostView(APIView):
    def post(self, request, id):
        # get input JSON
        input_data = request.data
        input_data["id"] = id
        serializer = PostSerializer(data=input_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Создать URLs
```python
#-> api/urls
from django.urls import path
from .views import UserView, PostView

urlpatterns = [
    path('users/<int:id>/', UserView.as_view()),
    path('posts/<int:id>/', PostView.as_view()),
]

#далее включить эти url
#-> DjangoStubs/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]
```

#### Запустить сам сервер
```shell
python manage.py migrate
python manage.py runserver
```

#### Тестирование endpoints

##### GET запрос/ответ
```python
#URL
http://127.0.0.1:8000/users/1/

#Body(Response)
{
  "id": 1,
  "name": "AbcDefGh"
}
```

##### POST запрос/ответ
```python
#URL 
http://127.0.0.1:8000/posts/6/

#Body(Request)
{
  "title": "Ruslan",
  "body": "MyStub",
  "userId": 3
}

#Body(Response)
{
  "title": "foo",
  "body": "bar",
  "userId": 5,
  "id": 1
}
```