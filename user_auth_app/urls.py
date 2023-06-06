from django.urls import path
from . import views

urlpatterns = [

    path('index', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('home', views.home, name='home'),
]