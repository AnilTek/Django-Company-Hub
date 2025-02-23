from django.urls import include, path
from . import views

urlpatterns = [
    path('login/',views.login_site,name='login'),
    path('logout/',views.logout_site,name='logout'),
    path('',views.register_site,name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password/<uidb64>/<token>/', views.reset, name='reset'),
    path('new_password/<user_id>/', views.new_password, name='new_password'),
    
]
