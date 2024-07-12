from django.urls import path

from . import views


app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'),
    path("map/", views.map_view, name='map_view'), 
    path('new/', views.new, name='new'),
    path('<int:pk>/like/', views.like_item, name='like_item'),
    path('category/<int:category_id>/', views.category_items, name='category_items'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/renew_location/', views.renew_location, name='renew_location'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
]