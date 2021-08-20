from django.urls import path , re_path
from . import views
# Check login
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', views.Index.as_view() , name='index'),
    path('login/', views.login_view , name='login'),
    path('logout/', views.logout_view , name='logout'),
    path('signup/', views.signup_view , name='signup'),
    path('detail/<slug:slug>/', login_required(views.BookDetailView.as_view() , login_url='/login') , name='detail'),
    path('add' , views.book_add , name='book_add'),
    re_path(r'cart/add/(?P<slug>[\w-]+)/$' , views.cart_add , name='cart_add'),
    re_path(r'cart/delete/(?P<slug>[\w-]+)/$' , views.cart_delete , name='cart_delete'),
    path('delete_all' , views.cart_delete_all , name='cart_delete_all'),
    path('card_edit' , views.edit_qty , name='edit_qty'),
    path('cart/list/', views.cart_list , name='cart_list'),
    path('create/salesorder/', views.create_salesorder , name='create_salesorder'),
]