from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin_index, name='admin_index'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin_signout', views.admin_signout, name='admin_signout'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('search', views.search, name="search"),
    path('update/<int:id>/', views.update, name="update"),
    path('update_record/<int:id>',views.update_record,name='update_user'),
    path('add/', views.add, name='add'),
    path('admin_panel/add_record', views.add_record, name='add_record1')
]