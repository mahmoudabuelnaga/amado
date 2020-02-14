from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('shop/<slug>/', views.CatagoryDetailView.as_view(), name='catagory_detail'),
    # path('shop/', views.ProductListView.as_view(), name='product_list'),
    path('shop/', views.product_list_view , name='product_list'),
    path('shop/<pk>/<slug>/', views.ProductDetailView.as_view(), name='product_detail'),


]