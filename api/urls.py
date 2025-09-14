from django.urls import path
#from .views import UserView, PostView
from .views import UserView, PostView, LoginView, LogoutView

urlpatterns = [
    path('users/<int:id>/', UserView.as_view()),
    path('posts/<int:id>/', PostView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
