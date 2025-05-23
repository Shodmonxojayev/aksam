from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('about_us/', views.AboutPageView.as_view(), name='about-us'),
    path('calculator/', views.add_to_cart_view, name='calculator_page'),
    path('cart/', views.cart_page, name='cart_page'),
    path('news/', views.NewPageView.as_view(),name='news'),
    path('products/', views.ProductsPageView.as_view(),name='products'),
    path('profile/', views.ProfilePageView.as_view(),name='profile'),
    path('send_order/', views.send_order, name='send_order'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('add-to-cart/', views.add_to_cart_view, name='add_to_cart'),
    path('login/', views.login_page_view, name='login')

]
