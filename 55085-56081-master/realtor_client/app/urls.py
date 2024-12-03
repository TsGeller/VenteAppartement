# urls for login register and appartements

from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [

    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('offer/<int:appartment_id>', views.offer, name='offer', ),
    path('logout', views.logout, name='logout'),

    path('make_offer/<int:appartment_id>', views.make_offer, name='makeoffer'),
    
    path('appartements', views.appartements, name='appartements'),
]


