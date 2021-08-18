from django.urls import path , re_path
from . import views

urlpatterns = [
    path('', views.Index.as_view() , name='index'),
    path('detail/<slug:slug>/', views.BookDetailView.as_view() , name='detail'),
    re_path(r'cart/add/(?P<slug>[\w-]+)/$' , views.cart_add , name='cart_add'),
    re_path(r'cart/delete/(?P<slug>[\w-]+)/$' , views.cart_delete , name='cart_delete'),
    path('card/edit/' , views.edit_qty , name='edit_qty'),
    path('cart/list/', views.cart_list , name='cart_list'),
]