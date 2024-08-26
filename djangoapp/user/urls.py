from django.urls import path
from user import views

appname = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('pageUser/', views.pageUser, name='pageUser'),
]



